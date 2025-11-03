"""
Footnotes (註腳) Tools for MCP Server

Provides tools for querying Bible footnotes (TCV version only).
"""

import logging
from typing import Any

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

logger = logging.getLogger(__name__)


def get_footnotes_tool_definitions() -> list[dict[str, Any]]:
    """
    Get MCP tool definitions for footnotes operations.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "get_bible_footnote",
            "description": (
                "查詢聖經經文註腳（僅限 TCV 現代中文譯本）。\n"
                "註腳提供原文翻譯的不同選擇、古卷差異說明、或其他重要補充資訊。\n\n"
                "**重要提示**: 僅台灣聖經公會現代中文譯本 (TCV) 有註腳功能。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": (
                            "書卷編號 (1-66)。"
                            "例如：1=創世記, 19=詩篇, 43=約翰福音, 45=羅馬書"
                        ),
                        "minimum": 1,
                        "maximum": 66
                    },
                    "footnote_id": {
                        "type": "integer",
                        "description": (
                            "註腳編號（每個書卷有自己的編號系統）。"
                            "從 1 開始遞增。若編號不存在，會返回空結果。"
                        ),
                        "minimum": 1
                    },
                    "use_simplified": {
                        "type": "boolean",
                        "description": "是否使用簡體中文（預設：否）"
                    }
                },
                "required": ["book_id", "footnote_id"]
            }
        }
    ]


async def handle_get_bible_footnote(
    api_client: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Handle get_bible_footnote tool call.
    
    Args:
        api_client: FHL API client
        arguments: Tool arguments
        
    Returns:
        List of MCP response messages
    """
    try:
        book_id = arguments["book_id"]
        footnote_id = arguments["footnote_id"]
        use_simplified = arguments.get("use_simplified", False)
        
        result = await api_client.get_footnote(
            book_id=book_id,
            footnote_id=footnote_id,
            use_simplified=use_simplified
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            version = result.get("version", "tcv")
            engs = result.get("engs", "")
            
            if record_count > 0:
                record = result["record"][0]
                footnote_text = record.get("text", "")
                returned_id = record.get("id", footnote_id)
                
                response = (
                    f"**聖經註腳**\n\n"
                    f"📖 版本: TCV (現代中文譯本)\n"
                    f"📚 書卷: {engs} (ID: {book_id})\n"
                    f"🔖 註腳 #{returned_id}:\n\n"
                    f"{footnote_text}"
                )
            else:
                response = (
                    f"❌ 找不到註腳\n\n"
                    f"書卷 ID: {book_id}\n"
                    f"註腳 ID: {footnote_id}\n\n"
                    f"可能原因：\n"
                    f"1. 此註腳編號不存在\n"
                    f"2. 書卷 ID 不正確（應為 1-66）\n"
                    f"3. 建議從註腳 #1 開始嘗試"
                )
            
            return [{"type": "text", "text": response}]
        else:
            error_msg = result.get("error", "未知錯誤")
            return [{"type": "text", "text": f"❌ 查詢失敗: {error_msg}"}]
            
    except Exception as e:
        logger.error(f"Error in get_bible_footnote: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]
