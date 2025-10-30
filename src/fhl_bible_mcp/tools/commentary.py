"""
註釋與研經 MCP Tools

提供聖經註釋查詢、註釋搜尋、主題查經的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import InvalidParameterError


async def get_commentary(
    book: str,
    chapter: int,
    verse: int,
    commentary_id: Optional[int] = None,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    取得聖經註釋

    Args:
        book: 經卷名稱（支援中文或英文）
        chapter: 章數
        verse: 節數
        commentary_id: 註釋書編號（可選，不指定則返回所有可用的註釋）
        use_simplified: 是否使用簡體中文

    Returns:
        註釋內容字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 轉換書卷名稱為英文縮寫
    eng_short = BookNameConverter.get_english_short(book)
    if not eng_short:
        raise InvalidParameterError(f"找不到書卷: {book}")

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_commentary(
            book=eng_short,
            chapter=chapter,
            verse=verse,
            commentary_id=commentary_id,
        )

    # 格式化結果
    commentaries = []
    
    # 檢查是否有 record 鍵且不為空
    if "record" in response and response["record"]:
        for record in response["record"]:
            commentary_entry = {
                "commentary_name": record["book_name"],
                "title": record.get("title", "") or "",
                "content": record.get("com_text", "") or "",
            }

            # 添加導航資訊
            if record.get("prev"):
                commentary_entry["navigation"] = {
                    "prev": {
                        "book": record.get("prev").engs,
                        "chapter": record.get("prev").chap,
                        "verse": record.get("prev").sec,
                    }
                }
                if record.get("next"):
                    commentary_entry["navigation"]["next"] = {
                        "book": record.get("next").engs,
                        "chapter": record.get("next").chap,
                        "verse": record.get("next").sec,
                    }

            commentaries.append(commentary_entry)

    result = {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "commentary_count": len(commentaries),
        "commentaries": commentaries,
    }

    return result


async def list_commentaries(
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    列出所有可用的註釋書

    Args:
        use_simplified: 是否使用簡體中文

    Returns:
        註釋書列表
    """
    async with FHLAPIEndpoints() as api:
        response = await api.list_commentaries()

    commentaries = []
    for record in response["record"]:
        commentaries.append(
            {
                "id": record["id"],
                "name": record["name"],
            }
        )

    return {
        "total_count": response["record_count"],
        "commentaries": commentaries,
    }


async def search_commentary(
    keyword: str,
    commentary_id: Optional[int] = None,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    在註釋書中搜尋關鍵字

    Args:
        keyword: 搜尋關鍵字
        commentary_id: 註釋書編號（可選，不指定則搜尋所有註釋書）
        use_simplified: 是否使用簡體中文

    Returns:
        搜尋結果字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    if not keyword or not keyword.strip():
        raise InvalidParameterError("搜尋關鍵字不能為空")

    async with FHLAPIEndpoints() as api:
        response = await api.search_commentary(
            keyword=keyword,
            commentary_id=commentary_id,
        )

    # 格式化結果
    results = []
    if "record" in response and response["record"]:
        for record in response["record"]:
            results.append(
                {
                    "commentary_id": record["tag"],
                    "commentary_name": record["book_name"],
                    "title": record.get("title", "") or "",
                    "book": record["chinesef"],
                    "book_eng": record["engs"],
                    "chapter_start": record["bchap"],
                    "verse_start": record["bsec"],
                    "chapter_end": record["echap"],
                    "verse_end": record["esec"],
                }
            )

    return {
        "keyword": keyword,
        "total_count": len(results),
        "results": results,
    }


async def get_topic_study(
    keyword: str,
    source: str = "all",
    use_simplified: bool = False,
    count_only: bool = False,
) -> Dict[str, Any]:
    """
    查詢主題查經資料

    Args:
        keyword: 主題關鍵字
        source: 資料來源
            - "all": 全部查詢
            - "torrey_en": Torrey 英文
            - "naves_en": Naves 英文
            - "torrey_zh": Torrey 中文
            - "naves_zh": Naves 中文
        use_simplified: 是否使用簡體中文
        count_only: 是否只返回筆數

    Returns:
        主題查經結果字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    if not keyword or not keyword.strip():
        raise InvalidParameterError("關鍵字不能為空")

    # 驗證資料來源
    valid_sources = ["torrey_en", "naves_en", "torrey_zh", "naves_zh", "all"]

    if source not in valid_sources:
        raise InvalidParameterError(
            f"無效的資料來源: {source}，應為 'all', 'torrey_en', 'naves_en', 'torrey_zh', 或 'naves_zh'"
        )

    async with FHLAPIEndpoints() as api:
        response = await api.get_topic_study(
            keyword=keyword,
            source=source,
            count_only=count_only,
        )

    if count_only:
        return {
            "keyword": keyword,
            "source": source,
            "total_count": response["record_count"],
        }

    # 格式化結果
    results = []
    if "record" in response and response["record"]:
        for record in response["record"]:
            source_name = ""
            if record["book"] == 0:
                source_name = "Torrey (English)"
            elif record["book"] == 1:
                source_name = "Naves (English)"
            elif record["book"] == 2:
                source_name = "Torrey (中文)"
            elif record["book"] == 3:
                source_name = "Naves (中文)"

            results.append(
                {
                    "id": record["id"],
                    "source": source_name,
                    "topic": record.get("topic", "") or "",
                    "content": record.get("text", "") or "",
                }
            )

    return {
        "keyword": keyword,
        "source": source,
        "total_count": response.get("record_count", len(results)),
        "results": results,
    }
