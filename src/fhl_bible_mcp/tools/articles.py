"""
Article Search Tools

Tools for searching and browsing Faith Hope Love (信望愛) articles.
"""

import re
from typing import Any
from mcp.types import TextContent

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


def get_articles_tool_definitions() -> list[dict[str, Any]]:
    """Get article search tool definitions"""
    return [
        {
            "name": "search_fhl_articles",
            "description": """搜尋信望愛站的文章。

可以依據標題、作者、內容、摘要、專欄、發表日期等條件搜尋。
**至少需要提供一個搜尋條件**。

**回傳內容**：
- 預設模式 (include_content=false): 返回摘要和內容預覽（約 200 字）
- 完整模式 (include_content=true): 返回完整 HTML 內容

回傳文章列表，包含：
- 標題 (title)
- 作者 (author)
- 發表日期 (pubtime)
- 專欄 (column)
- 摘要 (abst)
- 內容預覽 (content_preview) 或完整內容 (content, HTML 格式)

⚠️ **注意**: FHL API 不支援通過 ID 直接獲取文章，因此若需要完整內容，
請在搜尋時設定 include_content=true。

範例：
- 搜尋並預覽：search_fhl_articles(title="愛")
- 搜尋並獲取完整內容：search_fhl_articles(title="愛", include_content=true)
- 搜尋作者「陳鳳翔」：search_fhl_articles(author="陳鳳翔")
- 搜尋「麻辣姊妹」專欄：search_fhl_articles(column="women3")
- 組合搜尋：search_fhl_articles(title="信心", author="李", limit=10)
""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "標題關鍵字"
                    },
                    "author": {
                        "type": "string",
                        "description": "作者名稱"
                    },
                    "content": {
                        "type": "string",
                        "description": "內文關鍵字"
                    },
                    "abstract": {
                        "type": "string",
                        "description": "摘要關鍵字"
                    },
                    "column": {
                        "type": "string",
                        "description": "專欄英文代碼（如 women3）。使用 list_fhl_article_columns 工具查看可用專欄"
                    },
                    "pub_date": {
                        "type": "string",
                        "description": "發表日期，格式為 YYYY.MM.DD（如 2025.10.19）"
                    },
                    "use_simplified": {
                        "type": "boolean",
                        "description": "是否使用簡體中文（預設：false，使用繁體）",
                        "default": False
                    },
                    "include_content": {
                        "type": "boolean",
                        "description": "是否包含完整 HTML 內容（預設：false，只返回預覽）。設為 true 會返回完整文章內容，但輸出較大。",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多回傳結果數（預設：50，範圍：1-200）",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 200
                    }
                }
            }
        },
        {
            "name": "list_fhl_article_columns",
            "description": """列出信望愛站可用的文章專欄。

回傳所有可搜尋的專欄，包含：
- 專欄代碼 (code): 用於 search_fhl_articles 的 column 參數
- 專欄名稱 (name): 中文名稱
- 專欄說明 (description): 專欄內容簡介

使用專欄代碼可以精確搜尋特定專欄的文章。

範例：
- 查看所有專欄：list_fhl_article_columns()
- 然後使用代碼搜尋：search_fhl_articles(column="women3")
""",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]


async def handle_search_articles(
    endpoints: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[TextContent]:
    """Handle search_fhl_articles tool call"""
    
    try:
        result = await endpoints.search_articles(
            title=arguments.get("title"),
            author=arguments.get("author"),
            content=arguments.get("content"),
            abstract=arguments.get("abstract"),
            column=arguments.get("column"),
            pub_date=arguments.get("pub_date"),
            use_simplified=arguments.get("use_simplified", False),
            limit=arguments.get("limit", 50)
        )
        
        # Format output as JSON
        if result.get("status") == 1 and result.get("record_count", 0) > 0:
            articles = result.get("record", [])
            
            if not articles:
                response_data = {
                    "status": "no_results",
                    "query_type": "article_search",
                    "message": "未找到符合條件的文章"
                }
                import json
                response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
                return [TextContent(type="text", text=response)]
            
            # Check if full content is requested
            include_content = arguments.get("include_content", False)
            
            # Build article list
            article_list = []
            for article in articles:
                content = article.get('txt', '')
                
                article_data = {
                    "id": article.get('id', ''),
                    "aid": article.get('aid', ''),
                    "title": article.get('title', ''),
                    "author": article.get('author', ''),
                    "column": {
                        "name": article.get('column', ''),
                        "code": article.get('ptab', '')
                    },
                    "pub_date": article.get('pubtime', ''),
                    "abstract": article.get('abst', '')
                }
                
                if include_content:
                    # Include full HTML content
                    article_data["content"] = content
                    article_data["content_format"] = "HTML"
                else:
                    # Generate content preview (plain text)
                    preview = ""
                    if content:
                        # Simple HTML tag removal
                        clean_content = re.sub(r'<[^>]+>', '', content)
                        # Remove extra whitespace
                        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
                        
                        preview_length = 200
                        if len(clean_content) > preview_length:
                            preview = clean_content[:preview_length] + "..."
                        else:
                            preview = clean_content
                    article_data["content_preview"] = preview
                
                article_list.append(article_data)
            
            response_data = {
                "status": "success",
                "query_type": "article_search",
                "total_count": result['record_count'],
                "returned_count": len(articles),
                "limited": result.get("limited", False),
                "content_included": include_content,
                "articles": article_list
            }
            
            import json
            response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
            
            # Add helpful notes
            if include_content:
                notes = [
                    "\n💡 **使用提示**：",
                    "- 文章內容為 HTML 格式，包含 <pic>、<br/>、<a> 等標籤",
                    "- 圖片路徑相對於信望愛站資源目錄",
                    "- 使用 `list_fhl_article_columns` 查看可用專欄"
                ]
            else:
                notes = [
                    "\n💡 **使用提示**：",
                    "- 目前顯示內容預覽（約 200 字）",
                    "- 若要獲取完整內容，請設定 `include_content=true`",
                    "- 文章完整內容為 HTML 格式，包含圖片、連結等元素",
                    "- 使用 `list_fhl_article_columns` 查看可用專欄"
                ]
            
            return [TextContent(type="text", text=response + "\n".join(notes))]
        
        elif result.get("status") == 0:
            error_msg = result.get("result", "Unknown error")
            
            # Provide helpful error messages
            if "data too much" in error_msg.lower():
                return [TextContent(
                    type="text",
                    text="""❌ 搜尋失敗：資料量過大

💡 提示：API 要求至少提供一個搜尋條件來限縮結果。

請使用以下參數之一：
• title - 標題關鍵字
• author - 作者名稱
• content - 內文關鍵字
• abstract - 摘要關鍵字
• column - 專欄代碼（使用 list_fhl_article_columns 查看）
• pub_date - 發表日期（格式：YYYY.MM.DD）

範例：search_fhl_articles(title="愛")
"""
                )]
            elif "no data" in error_msg.lower():
                return [TextContent(
                    type="text",
                    text="""⚠️ 未找到符合條件的文章

💡 建議：
• 嘗試更廣泛的搜尋關鍵字
• 移除部分搜尋條件
• 檢查專欄代碼是否正確（使用 list_fhl_article_columns）
• 確認日期格式為 YYYY.MM.DD
"""
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 搜尋失敗：{error_msg}\n\n💡 提示：請確認搜尋參數格式正確"
                )]
        
        else:
            response_data = {
                "status": "no_results",
                "query_type": "article_search",
                "message": "未找到符合條件的文章"
            }
            import json
            response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
            return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 搜尋時發生錯誤：{str(e)}\n\n💡 請檢查參數格式並重試"
        )]


async def handle_list_article_columns(
    endpoints: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[TextContent]:
    """Handle list_fhl_article_columns tool call"""
    
    columns = endpoints.list_article_columns()
    
    response_data = {
        "status": "success",
        "query_type": "list_article_columns",
        "column_count": len(columns),
        "columns": [
            {
                "code": col['code'],
                "name": col['name'],
                "description": col['description']
            }
            for col in columns
        ]
    }
    
    import json
    response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
    
    # Add usage examples
    notes = [
        "\n� **使用方式**：",
        "使用專欄代碼 (code) 進行搜尋，例如：",
        "",
        "📝 **範例**：",
        "• 搜尋「麻辣姊妹」專欄：`search_fhl_articles(column='women3')`",
        "• 搜尋「神學」專欄：`search_fhl_articles(column='theology')`",
        "• 搜尋「查經」專欄中標題含「約翰」：",
        "  `search_fhl_articles(column='bible_study', title='約翰')`"
    ]
    
    return [TextContent(type="text", text=response + "\n".join(notes))]
