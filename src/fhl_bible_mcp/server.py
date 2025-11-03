"""
FHL Bible MCP Server

Main server module integrating Tools, Resources, and Prompts.
"""

import asyncio
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Prompt,
    PromptMessage,
    GetPromptResult,
)

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.resources.handlers import ResourceRouter
from fhl_bible_mcp.prompts.templates import PromptManager

# Import all tool functions
from fhl_bible_mcp.tools.verse import (
    get_bible_verse,
    get_bible_chapter,
    query_verse_citation,
)
from fhl_bible_mcp.tools.search import (
    search_bible,
    search_bible_advanced,
)
from fhl_bible_mcp.tools.strongs import (
    get_word_analysis,
    lookup_strongs,
    search_strongs_occurrences,
)
from fhl_bible_mcp.tools.commentary import (
    get_commentary,
    list_commentaries,
    search_commentary,
    get_topic_study,
)
from fhl_bible_mcp.tools.info import (
    list_bible_versions,
    get_book_list,
    get_book_info,
    search_available_versions,
)
from fhl_bible_mcp.tools.audio import (
    get_audio_bible,
    list_audio_versions,
    get_audio_chapter_with_text,
)
from fhl_bible_mcp.tools.apocrypha import (
    get_apocrypha_tool_definitions,
    handle_get_apocrypha_verse,
    handle_search_apocrypha,
    handle_list_apocrypha_books,
)
from fhl_bible_mcp.tools.apostolic_fathers import (
    get_apostolic_fathers_tool_definitions,
    handle_get_apostolic_fathers_verse,
    handle_search_apostolic_fathers,
    handle_list_apostolic_fathers_books,
)
from fhl_bible_mcp.tools.footnotes import (
    get_footnotes_tool_definitions,
    handle_get_bible_footnote,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FHLBibleServer:
    """FHL Bible MCP Server"""
    
    def __init__(self):
        """Initialize FHL Bible MCP Server"""
        self.server = Server("fhl-bible-server")
        self.endpoints = FHLAPIEndpoints()
        self.resource_router = ResourceRouter(self.endpoints)
        self.prompt_manager = PromptManager()
        
        # Register handlers
        self._register_tools()
        self._register_resources()
        self._register_prompts()
        
        logger.info("FHL Bible MCP Server initialized")
    
    def _register_tools(self):
        """Register all MCP tools"""
        
        # ====================================================================
        # Verse Query Tools
        # ====================================================================
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            return [
                # Verse Query Tools
                Tool(
                    name="get_bible_verse",
                    description="查詢指定的聖經經文。支援單節、多節、節範圍查詢。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {
                                "type": "string",
                                "description": "經卷名稱（中文或英文縮寫，如：約、John、創世記、Genesis）"
                            },
                            "chapter": {
                                "type": "integer",
                                "description": "章數"
                            },
                            "verse": {
                                "type": "string",
                                "description": "節數（支援格式：'1', '1-5', '1,3,5', '1-2,5,8-10'）"
                            },
                            "version": {
                                "type": "string",
                                "description": "聖經版本代碼（預設：unv）"
                            },
                            "include_strong": {
                                "type": "boolean",
                                "description": "是否包含 Strong's Number（預設：false）"
                            },
                            "use_simplified": {
                                "type": "boolean",
                                "description": "是否使用簡體中文（預設：false）"
                            }
                        },
                        "required": ["book", "chapter", "verse"]
                    }
                ),
                Tool(
                    name="get_bible_chapter",
                    description="查詢整章聖經經文。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"},
                            "chapter": {"type": "integer", "description": "章數"},
                            "version": {"type": "string", "description": "聖經版本代碼（預設：unv）"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["book", "chapter"]
                    }
                ),
                Tool(
                    name="query_verse_citation",
                    description="解析並查詢經文引用字串（如：'約 3:16', '太 5:3-10'）。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "citation": {"type": "string", "description": "經文引用字串"},
                            "version": {"type": "string", "description": "聖經版本代碼"},
                            "include_strong": {"type": "boolean", "description": "是否包含 Strong's Number"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["citation"]
                    }
                ),
                
                # Search Tools
                Tool(
                    name="search_bible",
                    description="在聖經中搜尋關鍵字或原文編號。支援關鍵字搜尋、希臘文編號搜尋、希伯來文編號搜尋。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜尋內容"},
                            "search_type": {
                                "type": "string",
                                "enum": ["keyword", "greek", "hebrew"],
                                "description": "搜尋類型（keyword=關鍵字, greek=希臘文編號, hebrew=希伯來文編號）"
                            },
                            "scope": {
                                "type": "string",
                                "enum": ["all", "ot", "nt"],
                                "description": "搜尋範圍（all=全部, ot=舊約, nt=新約）"
                            },
                            "version": {"type": "string", "description": "聖經版本代碼"},
                            "limit": {"type": "integer", "description": "最多返回筆數"},
                            "offset": {"type": "integer", "description": "跳過筆數"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"},
                            "count_only": {"type": "boolean", "description": "是否只返回總數"}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="search_bible_advanced",
                    description="進階聖經搜尋，支援自訂書卷範圍。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜尋內容"},
                            "search_type": {"type": "string", "enum": ["keyword", "greek_number", "hebrew_number"], "description": "搜尋類型：keyword(關鍵字)/greek_number(希臘文編號)/hebrew_number(希伯來文編號)"},
                            "range_start": {"type": "integer", "description": "起始書卷編號 (1-66)"},
                            "range_end": {"type": "integer", "description": "結束書卷編號 (1-66)"},
                            "version": {"type": "string", "description": "聖經版本代碼"},
                            "limit": {"type": "integer", "description": "最多返回筆數"},
                            "offset": {"type": "integer", "description": "跳過筆數"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["query"]
                    }
                ),
                
                # Strong's Tools
                Tool(
                    name="get_word_analysis",
                    description="取得經文的原文字彙分析（希臘文/希伯來文）。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"},
                            "chapter": {"type": "integer", "description": "章數"},
                            "verse": {"type": "integer", "description": "節數"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["book", "chapter", "verse"]
                    }
                ),
                Tool(
                    name="lookup_strongs",
                    description="查詢 Strong's 原文字典。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "number": {"type": "string", "description": "Strong's Number"},
                            "testament": {
                                "type": "string",
                                "enum": ["OT", "NT"],
                                "description": "約別（OT=舊約, NT=新約）"
                            },
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["number", "testament"]
                    }
                ),
                Tool(
                    name="search_strongs_occurrences",
                    description="搜尋 Strong's 編號在聖經中的所有出現位置。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "number": {"type": "string", "description": "Strong's Number"},
                            "testament": {"type": "string", "enum": ["OT", "NT"]},
                            "limit": {"type": "integer", "description": "最多返回筆數"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["number", "testament"]
                    }
                ),
                
                # Commentary Tools
                Tool(
                    name="get_commentary",
                    description="取得經文註釋。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"},
                            "chapter": {"type": "integer", "description": "章數"},
                            "verse": {"type": "integer", "description": "節數"},
                            "commentary_id": {"type": "integer", "description": "註釋書編號（不指定則返回所有）"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["book", "chapter", "verse"]
                    }
                ),
                Tool(
                    name="list_commentaries",
                    description="列出所有可用的註釋書。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        }
                    }
                ),
                Tool(
                    name="search_commentary",
                    description="在註釋書中搜尋關鍵字。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {"type": "string", "description": "搜尋關鍵字"},
                            "commentary_id": {"type": "integer", "description": "註釋書編號"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["keyword"]
                    }
                ),
                Tool(
                    name="get_topic_study",
                    description="查詢主題查經資料（Torrey, Naves）。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {"type": "string", "description": "主題關鍵字"},
                            "source": {
                                "type": "string",
                                "enum": ["all", "torrey_en", "naves_en", "torrey_zh", "naves_zh"],
                                "description": "資料來源"
                            },
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"},
                            "count_only": {"type": "boolean", "description": "是否只返回總數"}
                        },
                        "required": ["keyword"]
                    }
                ),
                
                # Info Tools
                Tool(
                    name="list_bible_versions",
                    description="列出所有可用的聖經版本。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        }
                    }
                ),
                Tool(
                    name="get_book_list",
                    description="取得聖經書卷列表。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "testament": {
                                "type": "string",
                                "enum": ["OT", "NT"],
                                "description": "約別篩選（OT=舊約, NT=新約，不指定則返回全部）"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_book_info",
                    description="取得特定書卷的詳細資訊。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"}
                        },
                        "required": ["book"]
                    }
                ),
                Tool(
                    name="search_available_versions",
                    description="搜尋符合條件的聖經版本。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "has_strongs": {"type": "boolean", "description": "是否包含 Strong's Number"},
                            "testament": {"type": "string", "enum": ["OT", "NT", "both"]},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        }
                    }
                ),
                
                # Audio Tools
                Tool(
                    name="get_audio_bible",
                    description="取得有聲聖經音檔連結。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"},
                            "chapter": {"type": "integer", "description": "章數"},
                            "audio_version": {"type": "string", "description": "音訊版本代碼（預設：unv）"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["book", "chapter"]
                    }
                ),
                Tool(
                    name="list_audio_versions",
                    description="列出所有可用的有聲聖經版本。",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_audio_chapter_with_text",
                    description="取得有聲聖經及對應經文。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book": {"type": "string", "description": "經卷名稱"},
                            "chapter": {"type": "integer", "description": "章數"},
                            "audio_version": {"type": "string", "description": "音訊版本代碼"},
                            "text_version": {"type": "string", "description": "經文版本代碼"},
                            "use_simplified": {"type": "boolean", "description": "是否使用簡體中文"}
                        },
                        "required": ["book", "chapter"]
                    }
                ),
            ] + [
                # Dynamically add Apocrypha tools
                Tool(
                    name=tool["name"],
                    description=tool["description"],
                    inputSchema=tool["inputSchema"]
                )
                for tool in get_apocrypha_tool_definitions()
            ] + [
                # Dynamically add Apostolic Fathers tools
                Tool(
                    name=tool["name"],
                    description=tool["description"],
                    inputSchema=tool["inputSchema"]
                )
                for tool in get_apostolic_fathers_tool_definitions()
            ] + [
                # Dynamically add Footnotes tools
                Tool(
                    name=tool["name"],
                    description=tool["description"],
                    inputSchema=tool["inputSchema"]
                )
                for tool in get_footnotes_tool_definitions()
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Call a tool by name with arguments"""
            try:
                logger.info(f"Calling tool: {name} with arguments: {arguments}")
                
                # Route to appropriate tool function
                if name == "get_bible_verse":
                    result = await get_bible_verse(**arguments)
                elif name == "get_bible_chapter":
                    result = await get_bible_chapter(**arguments)
                elif name == "query_verse_citation":
                    result = await query_verse_citation(**arguments)
                elif name == "search_bible":
                    result = await search_bible(**arguments)
                elif name == "search_bible_advanced":
                    result = await search_bible_advanced(**arguments)
                elif name == "get_word_analysis":
                    result = await get_word_analysis(**arguments)
                elif name == "lookup_strongs":
                    result = await lookup_strongs(**arguments)
                elif name == "search_strongs_occurrences":
                    result = await search_strongs_occurrences(**arguments)
                elif name == "get_commentary":
                    result = await get_commentary(**arguments)
                elif name == "list_commentaries":
                    result = await list_commentaries(**arguments)
                elif name == "search_commentary":
                    result = await search_commentary(**arguments)
                elif name == "get_topic_study":
                    result = await get_topic_study(**arguments)
                elif name == "list_bible_versions":
                    result = await list_bible_versions(**arguments)
                elif name == "get_book_list":
                    result = await get_book_list(**arguments)
                elif name == "get_book_info":
                    result = await get_book_info(**arguments)
                elif name == "search_available_versions":
                    result = await search_available_versions(**arguments)
                elif name == "get_audio_bible":
                    result = await get_audio_bible(**arguments)
                elif name == "list_audio_versions":
                    result = await list_audio_versions(**arguments)
                elif name == "get_audio_chapter_with_text":
                    result = await get_audio_chapter_with_text(**arguments)
                # Apocrypha tools
                elif name == "get_apocrypha_verse":
                    result = await handle_get_apocrypha_verse(self.endpoints, arguments)
                    return result
                elif name == "search_apocrypha":
                    result = await handle_search_apocrypha(self.endpoints, arguments)
                    return result
                elif name == "list_apocrypha_books":
                    result = await handle_list_apocrypha_books(self.endpoints, arguments)
                    return result
                # Apostolic Fathers tools
                elif name == "get_apostolic_fathers_verse":
                    result = await handle_get_apostolic_fathers_verse(self.endpoints, arguments)
                    return result
                elif name == "search_apostolic_fathers":
                    result = await handle_search_apostolic_fathers(self.endpoints, arguments)
                    return result
                elif name == "list_apostolic_fathers_books":
                    result = await handle_list_apostolic_fathers_books(self.endpoints, arguments)
                    return result
                # Footnotes tools
                elif name == "get_bible_footnote":
                    result = await handle_get_bible_footnote(self.endpoints, arguments)
                    return result
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                # Format result as JSON string
                import json
                result_text = json.dumps(result, ensure_ascii=False, indent=2)
                
                return [TextContent(type="text", text=result_text)]
                
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}", exc_info=True)
                error_msg = f"錯誤: {str(e)}"
                return [TextContent(type="text", text=error_msg)]
    
    def _register_resources(self):
        """Register all MCP resources"""
        
        @self.server.list_resources()
        async def list_resources() -> list[Any]:
            """List all available resources"""
            supported = self.resource_router.list_supported_resources()
            resources = []
            
            for category, resource_list in supported.items():
                for resource in resource_list:
                    resources.append({
                        "uri": resource["example"],
                        "name": resource["uri"],
                        "description": resource["description"],
                        "mimeType": "application/json"
                    })
            
            return resources
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource by URI"""
            try:
                logger.info(f"Reading resource: {uri}")
                result = await self.resource_router.handle_resource(uri)
                
                # Format result as JSON string
                import json
                return json.dumps(result["content"], ensure_ascii=False, indent=2)
                
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}", exc_info=True)
                raise
    
    def _register_prompts(self):
        """Register all MCP prompts"""
        
        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List all available prompts"""
            prompts_info = self.prompt_manager.list_prompts()
            return [
                Prompt(
                    name=p["name"],
                    description=p["description"],
                    arguments=[
                        {
                            "name": arg["name"],
                            "description": arg["description"],
                            "required": arg["required"]
                        }
                        for arg in p["arguments"]
                    ]
                )
                for p in prompts_info
            ]
        
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
            """Get a prompt by name with arguments"""
            try:
                logger.info(f"Getting prompt: {name} with arguments: {arguments}")
                
                # Render prompt with arguments
                if arguments is None:
                    arguments = {}
                
                rendered = self.prompt_manager.render_prompt(name, **arguments)
                
                if rendered is None:
                    raise ValueError(f"Unknown prompt: {name}")
                
                return GetPromptResult(
                    description=f"Rendered prompt: {name}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=rendered
                            )
                        )
                    ]
                )
                
            except Exception as e:
                logger.error(f"Error getting prompt {name}: {e}", exc_info=True)
                raise
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting FHL Bible MCP Server...")
        logger.info("Server capabilities:")
        logger.info("  - Tools: 25 functions (18 core + 3 apocrypha + 3 apostolic fathers + 1 footnotes)")
        logger.info("  - Resources: 7 URI schemes")
        logger.info("  - Prompts: 4 templates")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main() -> None:
    """Main entry point for the FHL Bible MCP Server"""
    server = FHLBibleServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
