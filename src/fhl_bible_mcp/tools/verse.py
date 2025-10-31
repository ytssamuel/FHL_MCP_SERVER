"""
經文查詢 MCP Tools

提供查詢聖經經文的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import BookNotFoundError, InvalidParameterError


async def get_bible_verse(
    book: str,
    chapter: int,
    verse: Optional[str] = None,
    version: str = "unv",
    include_strong: bool = False,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    查詢指定章節的聖經經文

    Args:
        book: 經卷名稱（支援中文或英文，如 "約" 或 "John"）
        chapter: 章數
        verse: 節數（可選，支援 "1", "1-5", "1,3,5" 等格式）
        version: 聖經版本代碼（預設 "unv" 和合本）
        include_strong: 是否包含 Strong's Number
        use_simplified: 是否使用簡體中文

    Returns:
        包含經文內容、版本資訊、導航資訊的字典

    Raises:
        InvalidParameterError: 參數錯誤（如找不到書卷）
    """
    # 轉換書卷名稱為中文縮寫（API 需要）
    chi_short = BookNameConverter.get_chinese_short(book)
    if not chi_short:
        raise BookNotFoundError(book)

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_verse(
            book=chi_short,
            chapter=chapter,
            verse=verse,
            version=version,
            include_strong=include_strong,
        )

    # 格式化回應
    verses = []
    for record in response["record"]:
        verses.append(
            {
                "book": record["chineses"],
                "book_eng": record["engs"],
                "chapter": record["chap"],
                "verse": record["sec"],
                "text": record["bible_text"],
            }
        )

    result = {
        "version": response["version"],
        "version_name": response["v_name"],
        "record_count": response["record_count"],
        "verses": verses,
    }

    # 添加導航資訊
    if "prev" in response and response["prev"]:
        result["navigation"] = {
            "prev": {
                "book": response["prev"]["chineses"],
                "book_eng": response["prev"]["engs"],
                "chapter": response["prev"]["chap"],
                "verse": response["prev"]["sec"],
            }
        }
        if "next" in response and response["next"]:
            result["navigation"]["next"] = {
                "book": response["next"]["chineses"],
                "book_eng": response["next"]["engs"],
                "chapter": response["next"]["chap"],
                "verse": response["next"]["sec"],
            }

    return result


async def get_bible_chapter(
    book: str,
    chapter: int,
    version: str = "unv",
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    查詢整章聖經經文

    Args:
        book: 經卷名稱（支援中文或英文）
        chapter: 章數
        version: 聖經版本代碼
        use_simplified: 是否使用簡體中文

    Returns:
        包含整章經文的字典
    """
    # 不指定 verse 參數會返回整章
    return await get_bible_verse(
        book=book,
        chapter=chapter,
        verse=None,
        version=version,
        include_strong=False,
        use_simplified=use_simplified,
    )


async def query_verse_citation(
    citation: str,
    version: str = "unv",
    include_strong: bool = False,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    根據經文引用字串查詢經文（如 "約 3:16" 或 "John 3:16"）

    Args:
        citation: 經文引用字串（如 "約 3:16", "太 5:3-10"）
        version: 聖經版本代碼
        include_strong: 是否包含 Strong's Number
        use_simplified: 是否使用簡體中文

    Returns:
        包含經文內容的字典

    Raises:
        InvalidParameterError: 引用格式錯誤
    """
    # 解析引用字串（簡單實作，可以後續增強）
    import re

    # 匹配格式：書卷 章:節 或 書卷 章:節-節
    pattern = r"^(.+?)\s+(\d+):(\d+(?:-\d+|,\d+)*)$"
    match = re.match(pattern, citation.strip())

    if not match:
        raise InvalidParameterError("citation", citation, "無效的經文引用格式")

    book_name, chapter, verses = match.groups()

    return await get_bible_verse(
        book=book_name,
        chapter=int(chapter),
        verse=verses,
        version=version,
        include_strong=include_strong,
        use_simplified=use_simplified,
    )
