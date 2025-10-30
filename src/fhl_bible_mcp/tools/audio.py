"""
多媒體 MCP Tools

提供有聲聖經查詢的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import InvalidParameterError


# 有聲聖經版本對照
AUDIO_VERSIONS = {
    "unv": {"id": 0, "name": "和合本"},
    "taiwanese": {"id": 1, "name": "台語"},
    "hakka": {"id": 2, "name": "客家話"},
    "cantonese": {"id": 3, "name": "廣東話"},
    "tcv": {"id": 4, "name": "現代中文譯本"},
    "taiwanese_nt": {"id": 5, "name": "台語新約"},
    "red_bible": {"id": 6, "name": "紅皮聖經"},
    "hebrew": {"id": 7, "name": "希伯來文"},
    "fuzhou": {"id": 8, "name": "福州話"},
    "greek": {"id": 9, "name": "希臘文"},
    "spring_taiwanese": {"id": 10, "name": "Spring台語"},
    "spring_unv": {"id": 11, "name": "Spring和合本"},
    "netbible_chinese": {"id": 12, "name": "NetBible中文版"},
    "pct": {"id": 13, "name": "全民台語聖經"},
    "tsou": {"id": 14, "name": "鄒語"},
    "taiwanese_south": {"id": 15, "name": "台語南部腔"},
    "modern_taiwanese": {"id": 17, "name": "現代台語譯本"},
    "modern_hakka": {"id": 18, "name": "現代客語譯本"},
    "tao": {"id": 19, "name": "達悟語"},
}


async def get_audio_bible(
    book: str,
    chapter: int,
    audio_version: str = "unv",
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    取得有聲聖經音檔連結

    Args:
        book: 經卷名稱（支援中文或英文）
        chapter: 章數
        audio_version: 有聲聖經版本代碼（預設 "unv" 和合本）
            可用版本：unv, taiwanese, hakka, cantonese, tcv, taiwanese_nt,
                     red_bible, hebrew, fuzhou, greek, spring_taiwanese,
                     spring_unv, netbible_chinese, pct, tsou, taiwanese_south,
                     modern_taiwanese, modern_hakka, tao
        use_simplified: 是否使用簡體中文

    Returns:
        包含音檔連結的字典

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 驗證音檔版本
    if audio_version not in AUDIO_VERSIONS:
        raise InvalidParameterError(
            f"無效的有聲聖經版本: {audio_version}，"
            f"可用版本: {', '.join(AUDIO_VERSIONS.keys())}"
        )

    # 取得書卷編號
    book_id = BookNameConverter.get_book_id(book)
    if not book_id:
        raise InvalidParameterError(f"找不到書卷: {book}")

    version_id = AUDIO_VERSIONS[audio_version]["id"]

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_audio_bible(
            book_id=book_id,
            chapter=chapter,
            audio_version=version_id,
        )

    # 格式化回應
    result = {
        "version": audio_version,
        "version_name": response["name"],
        "book": response["chinesef"],
        "book_eng": response["engf"],
        "chapter": response["chap"],
        "audio_files": {},
    }

    # 添加音檔連結
    if response.get("mp3"):
        result["audio_files"]["mp3"] = response.get("mp3")
    if response.get("ogg"):
        result["audio_files"]["ogg"] = response.get("ogg")

    # 添加導航資訊
    navigation = {}
    if response.get("pbid") and response.get("pchap"):
        navigation["prev"] = {
            "book_id": response.get("pbid"),
            "book": response.get("pchinesef"),
            "chapter": response.get("pchap"),
        }
    if response.get("nbid") and response.get("nchap"):
        navigation["next"] = {
            "book_id": response.get("nbid"),
            "book": response.get("nchinesef"),
            "chapter": response.get("nchap"),
        }

    if navigation:
        result["navigation"] = navigation

    return result


async def list_audio_versions() -> Dict[str, Any]:
    """
    列出所有可用的有聲聖經版本

    Returns:
        有聲聖經版本列表
    """
    versions = []
    for code, info in AUDIO_VERSIONS.items():
        versions.append(
            {
                "code": code,
                "id": info["id"],
                "name": info["name"],
            }
        )

    # 按 ID 排序
    versions.sort(key=lambda x: x["id"])

    return {
        "total_count": len(versions),
        "versions": versions,
    }


async def get_audio_chapter_with_text(
    book: str,
    chapter: int,
    audio_version: str = "unv",
    text_version: str = "unv",
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    同時取得有聲聖經與經文內容

    Args:
        book: 經卷名稱
        chapter: 章數
        audio_version: 有聲聖經版本
        text_version: 經文版本
        use_simplified: 是否使用簡體中文

    Returns:
        包含音檔與經文的字典
    """
    # 取得音檔資訊
    audio_info = await get_audio_bible(
        book=book,
        chapter=chapter,
        audio_version=audio_version,
        use_simplified=use_simplified,
    )

    # 取得經文內容
    from .verse import get_bible_chapter

    verse_info = await get_bible_chapter(
        book=book,
        chapter=chapter,
        version=text_version,
        use_simplified=use_simplified,
    )

    return {
        "audio": audio_info,
        "text": verse_info,
    }
