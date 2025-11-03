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

回傳文章列表，包含：
- 標題 (title)
- 作者 (author)
- 發表日期 (pubtime)
- 專欄 (column)
- 摘要 (abst)
- 完整內容 (txt, HTML 格式)

範例：
- 搜尋標題包含「愛」的文章：search_fhl_articles(title="愛")
- 搜尋作者「陳鳳翔」的文章：search_fhl_articles(author="陳鳳翔")
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
        
        # Format output
        if result.get("status") == 1 and result.get("record_count", 0) > 0:
            articles = result.get("record", [])
            
            if not articles:
                return [TextContent(
                    type="text",
                    text="⚠️ 未找到符合條件的文章"
                )]
            
            output = [f"📚 找到 {result['record_count']} 篇文章"]
            
            if result.get("limited"):
                output.append(f"（顯示前 {arguments.get('limit', 50)} 篇）")
            
            output.append("\n" + "="*60 + "\n")
            
            for i, article in enumerate(articles, 1):
                output.append(f"📄 文章 {i}")
                output.append(f"標題：{article.get('title', 'N/A')}")
                output.append(f"作者：{article.get('author', 'N/A')}")
                output.append(f"專欄：{article.get('column', 'N/A')} ({article.get('ptab', 'N/A')})")
                output.append(f"日期：{article.get('pubtime', 'N/A')}")
                
                # Abstract
                abstract = article.get('abst', '')
                if abstract:
                    output.append(f"\n📝 摘要：")
                    output.append(abstract)
                
                # Content preview (remove HTML tags)
                content = article.get('txt', '')
                if content:
                    # Simple HTML tag removal
                    clean_content = re.sub(r'<[^>]+>', '', content)
                    # Remove extra whitespace
                    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
                    
                    preview_length = 300
                    if len(clean_content) > preview_length:
                        preview = clean_content[:preview_length] + "..."
                    else:
                        preview = clean_content
                    
                    output.append(f"\n📖 內容預覽：")
                    output.append(preview)
                
                output.append("\n" + "-"*60 + "\n")
            
            output.append("\n💡 提示：")
            output.append("- 文章內容為 HTML 格式，包含圖片、連結等")
            output.append("- 可使用 title、author、content 等參數進一步篩選")
            output.append("- 使用 list_fhl_article_columns 查看可用專欄")
            
            return [TextContent(type="text", text="\n".join(output))]
        
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
            return [TextContent(
                type="text",
                text="⚠️ 未找到符合條件的文章"
            )]
    
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
    
    output = ["📋 信望愛站文章專欄列表\n"]
    output.append("=" * 60 + "\n")
    
    for col in columns:
        output.append(f"📌 {col['name']} ({col['code']})")
        output.append(f"   {col['description']}\n")
    
    output.append("=" * 60)
    output.append(f"\n💡 共 {len(columns)} 個專欄")
    output.append("\n📖 使用方式：")
    output.append("   使用專欄代碼 (code) 進行搜尋，例如：")
    output.append("   search_fhl_articles(column='women3')")
    output.append("\n📝 範例：")
    output.append("   • 搜尋「麻辣姊妹」專欄：search_fhl_articles(column='women3')")
    output.append("   • 搜尋「神學」專欄：search_fhl_articles(column='theology')")
    output.append("   • 搜尋「查經」專欄中標題含「約翰」：")
    output.append("     search_fhl_articles(column='bible_study', title='約翰')")
    
    return [TextContent(type="text", text="\n".join(output))]
