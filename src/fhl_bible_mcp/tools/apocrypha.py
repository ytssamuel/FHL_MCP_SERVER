"""
Apocrypha (次經) Tools for MCP Server

Provides tools for querying and searching Apocrypha books (101-115).
"""

import logging
from typing import Any

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

logger = logging.getLogger(__name__)

# Apocrypha book mapping (Book ID 101-115)
APOCRYPHA_BOOKS = {
    # Chinese abbreviations
    "多": {"id": 101, "name_zh": "多俾亞傳", "name_en": "Tobit"},
    "友": {"id": 102, "name_zh": "友弟德傳", "name_en": "Judith"},
    "加上": {"id": 103, "name_zh": "瑪加伯上", "name_en": "1 Maccabees"},
    "加下": {"id": 104, "name_zh": "瑪加伯下", "name_en": "2 Maccabees"},
    "智": {"id": 105, "name_zh": "智慧篇", "name_en": "Wisdom"},
    "德": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},
    "巴": {"id": 107, "name_zh": "巴錄書", "name_en": "Baruch"},
    "耶信": {"id": 108, "name_zh": "耶利米書信", "name_en": "Letter of Jeremiah"},
    "但補": {"id": 109, "name_zh": "但以理補篇", "name_en": "Additions to Daniel"},
    # English abbreviations
    "Tob": {"id": 101, "name_zh": "多俾亞傳", "name_en": "Tobit"},
    "Jdt": {"id": 102, "name_zh": "友弟德傳", "name_en": "Judith"},
    "1Mac": {"id": 103, "name_zh": "瑪加伯上", "name_en": "1 Maccabees"},
    "2Mac": {"id": 104, "name_zh": "瑪加伯下", "name_en": "2 Maccabees"},
    "Wis": {"id": 105, "name_zh": "智慧篇", "name_en": "Wisdom"},
    "Sir": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},
    "Bar": {"id": 107, "name_zh": "巴錄書", "name_en": "Baruch"},
    "EpJer": {"id": 108, "name_zh": "耶利米書信", "name_en": "Letter of Jeremiah"},
}


def get_apocrypha_tool_definitions() -> list[dict[str, Any]]:
    """
    Get MCP tool definitions for Apocrypha operations.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "get_apocrypha_verse",
            "description": (
                "查詢次經 (Apocrypha) 經文內容。支援書卷 101-115。\n"
                "包含：多俾亞傳、友弟德傳、瑪加伯上下、智慧篇、德訓篇、巴錄書等。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "book": {
                        "type": "string",
                        "description": (
                            "次經書卷名稱（中文或英文縮寫）。"
                            "例如：'多'(多俾亞傳), '友'(友弟德傳), '加上'(瑪加伯上), "
                            "'智'(智慧篇), '德'(德訓篇), 'Tob', 'Wis', 'Sir' 等"
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
            "name": "search_apocrypha",
            "description": (
                "在次經 (Apocrypha) 中搜尋關鍵字。搜尋範圍為書卷 101-115。"
                "使用 1933年聖公會出版版本。"
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
            "name": "list_apocrypha_books",
            "description": "列出所有可用的次經書卷及其資訊",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
    ]


async def handle_get_apocrypha_verse(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle get_apocrypha_verse tool call.
    
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
        
        result = await api_client.get_apocrypha_verse(
            book=book,
            chapter=chapter,
            verse=verse,
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            v_name = result.get("v_name", "1933年聖公會出版")
            v_code = result.get("version", "c1933")
            bid = result.get("bid", "未知")
            
            # Format verses
            verses_text = []
            for verse_obj in result.get("record", []):
                verse_num = verse_obj.get("sec", "")
                text = verse_obj.get("bible_text", "")
                chineses = verse_obj.get("chineses", book)
                verses_text.append(f"{chineses} {chapter}:{verse_num} {text}")
            
            response = (
                f"**次經經文查詢結果**\n\n"
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
        logger.error(f"Error in get_apocrypha_verse: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]


async def handle_search_apocrypha(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle search_apocrypha tool call.
    
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
        
        result = await api_client.search_apocrypha(
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
                    f"{idx}. {chineses} {chap}:{sec} (Book {bid})\n   {text}"
                )
            
            response = (
                f"**次經搜尋結果**\n\n"
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
        logger.error(f"Error in search_apocrypha: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]


async def handle_list_apocrypha_books(
    api_client: FHLAPIEndpoints, arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle list_apocrypha_books tool call.
    
    Args:
        api_client: FHL API client (unused)
        arguments: Tool arguments (unused)
        
    Returns:
        List of MCP response messages
    """
    try:
        books_text = ["**次經 (Apocrypha) 書卷列表**\n"]
        books_text.append("Book ID 101-115\n")
        
        # Group by book ID
        books_by_id: dict[int, dict[str, Any]] = {}
        for abbr, info in APOCRYPHA_BOOKS.items():
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
        logger.error(f"Error in list_apocrypha_books: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]
