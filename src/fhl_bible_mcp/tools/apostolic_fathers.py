"""
Apostolic Fathers (使徒教父) Tools for MCP Server

Provides tools for querying and searching Apostolic Fathers books (201-217).
"""

import logging
from typing import Any

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

logger = logging.getLogger(__name__)

# Apostolic Fathers book mapping (Book ID 201-217)
APOSTOLIC_FATHERS_BOOKS = {
    # Chinese abbreviations
    "革": {"id": 201, "name_zh": "革利免前書", "name_en": "1 Clement"},
    "革二": {"id": 202, "name_zh": "革利免後書", "name_en": "2 Clement"},
    "伊": {"id": 203, "name_zh": "伊格那丟書信", "name_en": "Ignatius"},
    "坡": {"id": 204, "name_zh": "坡旅甲書信", "name_en": "Polycarp"},
    "黑": {"id": 205, "name_zh": "黑馬牧人書", "name_en": "Shepherd of Hermas"},
    "巴": {"id": 206, "name_zh": "巴拿巴書", "name_en": "Barnabas"},
    "訓": {"id": 207, "name_zh": "十二使徒遺訓", "name_en": "Didache"},
    "帕": {"id": 216, "name_zh": "帕皮亞殘篇", "name_en": "Papias Fragments"},
    # English abbreviations
    "1Clem": {"id": 201, "name_zh": "革利免前書", "name_en": "1 Clement"},
    "2Clem": {"id": 202, "name_zh": "革利免後書", "name_en": "2 Clement"},
    "Ign": {"id": 203, "name_zh": "伊格那丟書信", "name_en": "Ignatius"},
    "Pol": {"id": 204, "name_zh": "坡旅甲書信", "name_en": "Polycarp"},
    "Herm": {"id": 205, "name_zh": "黑馬牧人書", "name_en": "Shepherd of Hermas"},
    "Barn": {"id": 206, "name_zh": "巴拿巴書", "name_en": "Barnabas"},
    "Did": {"id": 207, "name_zh": "十二使徒遺訓", "name_en": "Didache"},
    "Pap": {"id": 216, "name_zh": "帕皮亞殘篇", "name_en": "Papias Fragments"},
}


def get_apostolic_fathers_tool_definitions() -> list[dict[str, Any]]:
    """
    Get MCP tool definitions for Apostolic Fathers operations.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "get_apostolic_fathers_verse",
            "description": (
                "查詢使徒教父 (Apostolic Fathers) 文獻內容。支援書卷 201-217。\n"
                "包含：革利免前後書、伊格那丟書信、坡旅甲書信、黑馬牧人書、"
                "巴拿巴書、十二使徒遺訓、帕皮亞殘篇等。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "book": {
                        "type": "string",
                        "description": (
                            "使徒教父書卷名稱（中文或英文縮寫）。"
                            "例如：'革'(革利免前書), '革二'(革利免後書), '伊'(伊格那丟), "
                            "'黑'(黑馬牧人書), '訓'(十二使徒遺訓), '1Clem', 'Did' 等"
                        ),
                    },
                    "chapter": {
                        "type": "integer",
                        "description": "章數",
                    },
                    "verse": {
                        "type": "string",
                        "description": (
                            "節數（可選）。支援多種格式：\n"
                            "- 單節：'1'\n"
                            "- 範圍：'1-5'\n"
                            "- 多節：'1,3,5'\n"
                            "- 混合：'1-2,5,8-10'\n"
                            "若不提供則返回整章"
                        ),
                    },
                },
                "required": ["book", "chapter"],
            },
        },
        {
            "name": "search_apostolic_fathers",
            "description": (
                "在使徒教父 (Apostolic Fathers) 文獻中搜尋關鍵字。搜尋範圍為書卷 201-217。"
                "使用黃錫木主編《使徒教父著作》版本。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜尋關鍵字",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回結果數量上限",
                    },
                    "offset": {
                        "type": "integer",
                        "description": "跳過的結果數量（用於分頁）",
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "list_apostolic_fathers_books",
            "description": "列出所有可用的使徒教父書卷及其資訊",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
    ]


async def handle_get_apostolic_fathers_verse(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle get_apostolic_fathers_verse tool call.
    
    Args:
        api_client: FHL API client
        arguments: Tool arguments
        
    Returns:
        List of MCP response messages
    """
    try:
        book = arguments["book"]
        chapter = arguments["chapter"]
        verse = arguments.get("verse")
        
        result = await api_client.get_apostolic_fathers_verse(
            book=book,
            chapter=chapter,
            verse=verse,
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            v_name = result.get("v_name", "黃錫木主編《使徒教父著作》")
            v_code = result.get("version", "afhuang")
            bid = result.get("bid", "未知")
            
            # Format verses
            verses_text = []
            for verse_obj in result.get("record", []):
                verse_num = verse_obj.get("sec", "")
                text = verse_obj.get("bible_text", "")
                chineses = verse_obj.get("chineses", book)
                verses_text.append(f"{chineses} {chapter}:{verse_num} {text}")
            
            response = (
                f"**使徒教父文獻查詢結果**\n\n"
                f"版本: {v_name} ({v_code})\n"
                f"書卷 ID: {bid}\n"
                f"經文數量: {record_count}\n\n"
                f"{chr(10).join(verses_text)}"
            )
            
            return [{"type": "text", "text": response}]
        else:
            error_msg = result.get("error", "未知錯誤")
            return [{"type": "text", "text": f"❌ 查詢失敗: {error_msg}"}]
            
    except Exception as e:
        logger.error(f"Error in get_apostolic_fathers_verse: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]


async def handle_search_apostolic_fathers(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle search_apostolic_fathers tool call.
    
    Args:
        api_client: FHL API client
        arguments: Tool arguments
        
    Returns:
        List of MCP response messages
    """
    try:
        query = arguments["query"]
        limit = arguments.get("limit")
        offset = arguments.get("offset", 0)
        
        result = await api_client.search_apostolic_fathers(
            query=query,
            limit=limit,
            offset=offset,
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            key = result.get("key", query)
            
            # Format search results
            results_text = []
            for idx, verse_obj in enumerate(result.get("record", []), 1):
                chineses = verse_obj.get("chineses", "")
                bid = verse_obj.get("bid", "")
                chap = verse_obj.get("chap", "")
                sec = verse_obj.get("sec", "")
                text = verse_obj.get("bible_text", "")
                
                results_text.append(
                    f"{idx}. {chineses} {chap}:{sec} (Book {bid})\n   {text[:100]}..."
                )
            
            response = (
                f"**使徒教父文獻搜尋結果**\n\n"
                f"關鍵字: {key}\n"
                f"總結果數: {record_count}\n"
                f"顯示: {len(results_text)} 筆\n\n"
                f"{chr(10).join(results_text)}"
            )
            
            return [{"type": "text", "text": response}]
        else:
            error_msg = result.get("error", "未知錯誤")
            return [{"type": "text", "text": f"❌ 搜尋失敗: {error_msg}"}]
            
    except Exception as e:
        logger.error(f"Error in search_apostolic_fathers: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]


async def handle_list_apostolic_fathers_books(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle list_apostolic_fathers_books tool call.
    
    Args:
        api_client: FHL API client (unused)
        arguments: Tool arguments (unused)
        
    Returns:
        List of MCP response messages
    """
    try:
        books_text = ["**使徒教父 (Apostolic Fathers) 書卷列表**\n"]
        books_text.append("Book ID 201-217\n")
        
        # Group by book ID
        books_by_id: dict[int, dict[str, Any]] = {}
        for abbr, info in APOSTOLIC_FATHERS_BOOKS.items():
            book_id = info["id"]
            if book_id not in books_by_id:
                books_by_id[book_id] = info.copy()
                books_by_id[book_id]["abbrs"] = []
            books_by_id[book_id]["abbrs"].append(abbr)
        
        # Format output
        for book_id in sorted(books_by_id.keys()):
            info = books_by_id[book_id]
            abbrs = ", ".join(info["abbrs"])
            books_text.append(
                f"{book_id}. **{info['name_zh']}** ({info['name_en']})\n"
                f"    縮寫: {abbrs}"
            )
        
        response = "\n".join(books_text)
        return [{"type": "text", "text": response}]
        
    except Exception as e:
        logger.error(f"Error in list_apostolic_fathers_books: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]
