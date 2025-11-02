"""
搜尋 MCP Tools

提供聖經搜尋功能的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import InvalidParameterError


async def search_bible(
    query: str,
    search_type: str = "keyword",
    scope: str = "all",
    version: str = "unv",
    limit: int = 50,
    offset: int = 0,
    use_simplified: bool = False,
    count_only: bool = False,
) -> Dict[str, Any]:
    """
    在聖經中搜尋關鍵字或原文編號

    Args:
        query: 搜尋內容（關鍵字或原文編號）
        search_type: 搜尋類型
            - "keyword": 關鍵字搜尋
            - "greek_number": 希臘文編號搜尋
            - "hebrew_number": 希伯來文編號搜尋
        scope: 搜尋範圍
            - "all": 全部聖經
            - "ot": 舊約
            - "nt": 新約
            - "range": 指定範圍（需配合 range_start, range_end）
        version: 聖經版本代碼
        limit: 最多返回筆數
        offset: 跳過筆數（用於分頁）
        use_simplified: 是否使用簡體中文
        count_only: 是否只返回結果筆數

    Returns:
        搜尋結果字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 驗證搜尋類型
    search_type_map = {
        "keyword": 0,
        "greek_number": 1,
        "hebrew_number": 2,
    }

    if search_type not in search_type_map:
        raise InvalidParameterError(
            parameter="search_type",
            value=search_type,
            reason="無效的搜尋類型，應為 'keyword', 'greek_number', 或 'hebrew_number'"
        )

    # 驗證範圍
    scope_map = {
        "all": 0,
        "nt": 1,
        "ot": 2,
    }

    if scope not in scope_map:
        raise InvalidParameterError(
            parameter="scope",
            value=scope,
            reason="無效的搜尋範圍，應為 'all', 'ot', 或 'nt'"
        )

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.search_bible(
            query=query,
            search_type=search_type,
            scope=scope,
            version=version,
            limit=limit,
            offset=offset,
            count_only=count_only,
        )

    # 如果只要筆數
    if count_only:
        return {
            "total_count": response["record_count"],
            "query": query,
            "search_type": search_type,
            "scope": scope,
        }

    # 格式化搜尋結果
    results = []
    for record in response["record"]:
        results.append(
            {
                "book": record["chineses"],
                "book_eng": record["engs"],
                "chapter": record["chap"],
                "verse": record["sec"],
                "text": record["bible_text"],
            }
        )

    return {
        "total_count": response["record_count"],
        "query": query,
        "search_type": search_type,
        "scope": scope,
        "limit": limit,
        "offset": offset,
        "results": results,
    }


async def search_bible_advanced(
    query: str,
    search_type: str = "keyword",
    range_start: Optional[str] = None,
    range_end: Optional[str] = None,
    version: str = "unv",
    limit: int = 50,
    offset: int = 0,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    進階聖經搜尋（支援指定書卷範圍）

    Args:
        query: 搜尋內容
        search_type: 搜尋類型
        range_start: 起始書卷（如 "創" 或 "Gen"）
        range_end: 結束書卷（如 "啟" 或 "Rev"）
        version: 聖經版本代碼
        limit: 最多返回筆數
        offset: 跳過筆數
        use_simplified: 是否使用簡體中文

    Returns:
        搜尋結果字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 如果沒有指定範圍，使用一般搜尋
    if not range_start or not range_end:
        return await search_bible(
            query=query,
            search_type=search_type,
            scope="all",
            version=version,
            limit=limit,
            offset=offset,
            use_simplified=use_simplified,
        )

    # 取得書卷編號
    start_id = BookNameConverter.get_book_id(range_start)
    end_id = BookNameConverter.get_book_id(range_end)

    if not start_id or not end_id:
        raise InvalidParameterError(
            parameter="range",
            value=f"{range_start} - {range_end}",
            reason="無效的書卷範圍"
        )

    if start_id > end_id:
        raise InvalidParameterError(
            parameter="range",
            value=f"{range_start} > {range_end}",
            reason="起始書卷不能大於結束書卷"
        )

    # 驗證搜尋類型
    search_type_map = {
        "keyword": 0,
        "greek": 1,
        "hebrew": 2,
    }

    if search_type not in search_type_map:
        raise InvalidParameterError(
            parameter="search_type",
            value=search_type,
            reason="無效的搜尋類型"
        )

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.search_bible(
            query=query,
            search_type=search_type,
            scope="range",
            version=version,
            limit=limit,
            offset=offset,
            range_start=start_id,
            range_end=end_id,
        )

    # 格式化結果
    results = []
    for record in response["record"]:
        results.append(
            {
                "book": record["chineses"],
                "book_eng": record["engs"],
                "chapter": record["chap"],
                "verse": record["sec"],
                "text": record["bible_text"],
            }
        )

    return {
        "total_count": response["record_count"],
        "query": query,
        "search_type": search_type,
        "range": {
            "start": range_start,
            "end": range_end,
        },
        "limit": limit,
        "offset": offset,
        "results": results,
    }
