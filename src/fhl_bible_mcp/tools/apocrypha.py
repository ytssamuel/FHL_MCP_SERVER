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
    # Chinese full names (常用別名)
    "多俾亞傳": {"id": 101, "name_zh": "多俾亞傳", "name_en": "Tobit"},
    "友弟德傳": {"id": 102, "name_zh": "友弟德傳", "name_en": "Judith"},
    "瑪加伯上": {"id": 103, "name_zh": "瑪加伯上", "name_en": "1 Maccabees"},
    "瑪加伯下": {"id": 104, "name_zh": "瑪加伯下", "name_en": "2 Maccabees"},
    "智慧篇": {"id": 105, "name_zh": "智慧篇", "name_en": "Wisdom"},
    "德訓篇": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},
    "便西拉智訓": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},  # 別名
    "巴錄書": {"id": 107, "name_zh": "巴錄書", "name_en": "Baruch"},
    "耶利米書信": {"id": 108, "name_zh": "耶利米書信", "name_en": "Letter of Jeremiah"},
    "但以理補篇": {"id": 109, "name_zh": "但以理補篇", "name_en": "Additions to Daniel"},
    # English abbreviations
    "Tob": {"id": 101, "name_zh": "多俾亞傳", "name_en": "Tobit"},
    "Jdt": {"id": 102, "name_zh": "友弟德傳", "name_en": "Judith"},
    "1Mac": {"id": 103, "name_zh": "瑪加伯上", "name_en": "1 Maccabees"},
    "2Mac": {"id": 104, "name_zh": "瑪加伯下", "name_en": "2 Maccabees"},
    "Wis": {"id": 105, "name_zh": "智慧篇", "name_en": "Wisdom"},
    "Sir": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},
    "Bar": {"id": 107, "name_zh": "巴錄書", "name_en": "Baruch"},
    "EpJer": {"id": 108, "name_zh": "耶利米書信", "name_en": "Letter of Jeremiah"},
    # English full names
    "Tobit": {"id": 101, "name_zh": "多俾亞傳", "name_en": "Tobit"},
    "Judith": {"id": 102, "name_zh": "友弟德傳", "name_en": "Judith"},
    "1 Maccabees": {"id": 103, "name_zh": "瑪加伯上", "name_en": "1 Maccabees"},
    "2 Maccabees": {"id": 104, "name_zh": "瑪加伯下", "name_en": "2 Maccabees"},
    "Wisdom": {"id": 105, "name_zh": "智慧篇", "name_en": "Wisdom"},
    "Sirach": {"id": 106, "name_zh": "德訓篇", "name_en": "Sirach"},
    "Baruch": {"id": 107, "name_zh": "巴錄書", "name_en": "Baruch"},
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
                "包含：多俾亞傳、友弟德傳、瑪加伯上下、智慧篇、德訓篇(便西拉智訓)、巴錄書等。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "book": {
                        "type": "string",
                        "description": (
                            "次經書卷名稱（支援多種格式）。\n"
                            "中文縮寫：'多', '友', '加上', '加下', '智', '德', '巴', '耶信', '但補'\n"
                            "中文全名：'多俾亞傳', '友弟德傳', '瑪加伯上', '瑪加伯下', '智慧篇', '德訓篇', '便西拉智訓', '巴錄書' 等\n"
                            "英文：'Tob', 'Jdt', '1Mac', '2Mac', 'Wis', 'Sir', 'Bar', 'Tobit', 'Judith', 'Sirach' 等"
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
        
        # Get book info for display name
        book_info = APOCRYPHA_BOOKS.get(book)
        display_name = book_info["name_zh"] if book_info else book
        
        result = await api_client.get_apocrypha_verse(
            book=book,
            chapter=chapter,
            verse=verse,
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            v_name = result.get("v_name", "1933年聖公會出版")
            v_code = result.get("version", "c1933")
            
            # Get bid from first record (if available)
            records = result.get("record", [])
            bid = records[0].get("bid", "未知") if records else "未知"
            
            # Format verses with proper book name
            verses = []
            for verse_obj in records:
                verses.append({
                    "book": display_name,
                    "book_id": verse_obj.get("bid", bid),
                    "chapter": chapter,
                    "verse": verse_obj.get("sec", ""),
                    "text": verse_obj.get("bible_text", "")
                })
            
            # Return structured JSON format
            response_data = {
                "status": "success",
                "query_type": "apocrypha_verse",
                "book": display_name,
                "book_id": bid,
                "chapter": chapter,
                "verse": verse,
                "version": {
                    "code": v_code,
                    "name": v_name
                },
                "verse_count": record_count,
                "verses": verses
            }
            
            import json
            response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
            
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
        
        # Create reverse lookup: bid -> book name
        bid_to_name = {}
        for book_key, book_info in APOCRYPHA_BOOKS.items():
            bid = book_info["id"]
            if bid not in bid_to_name:
                bid_to_name[bid] = book_info["name_zh"]
        
        result = await api_client.search_apocrypha(
            query=query,
            limit=limit,
            offset=offset,
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            key = result.get("key", query)
            
            # Format search results with proper book names
            results = []
            for verse_obj in result.get("record", []):
                bid = verse_obj.get("bid", "")
                chap = verse_obj.get("chap", "")
                sec = verse_obj.get("sec", "")
                text = verse_obj.get("bible_text", "")
                
                # Use our book name mapping instead of API's chineses
                book_name = bid_to_name.get(int(bid), verse_obj.get("chineses", ""))
                
                results.append({
                    "book": book_name,
                    "book_id": bid,
                    "chapter": chap,
                    "verse": sec,
                    "text": text
                })
            
            # Return structured JSON format
            response_data = {
                "status": "success",
                "query_type": "apocrypha_search",
                "keyword": key,
                "total_count": record_count,
                "returned_count": len(results),
                "offset": offset,
                "results": results
            }
            
            import json
            response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
            
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
        # Group by book ID
        books_by_id: dict[int, dict[str, Any]] = {}
        for abbr, info in APOCRYPHA_BOOKS.items():
            book_id = info["id"]
            if book_id not in books_by_id:
                books_by_id[book_id] = info.copy()
                books_by_id[book_id]["abbrs"] = []
            books_by_id[book_id]["abbrs"].append(abbr)
        
        # Build books list
        books_list = []
        for book_id in sorted(books_by_id.keys()):
            info = books_by_id[book_id]
            books_list.append({
                "id": book_id,
                "name_zh": info["name_zh"],
                "name_en": info["name_en"],
                "abbreviations": info["abbrs"]
            })
        
        # Return structured JSON format
        response_data = {
            "status": "success",
            "query_type": "list_apocrypha_books",
            "id_range": "101-115",
            "book_count": len(books_list),
            "books": books_list
        }
        
        import json
        response = f"```json\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n```"
        return [{"type": "text", "text": response}]
        
    except Exception as e:
        logger.error(f"Error in list_apocrypha_books: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]
