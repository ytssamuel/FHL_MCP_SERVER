"""
原文研究 MCP Tools

提供希臘文、希伯來文字彙分析與 Strong's 字典查詢的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import InvalidParameterError


async def get_word_analysis(
    book: str,
    chapter: int,
    verse: int,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    取得經文的原文字彙分析

    Args:
        book: 經卷名稱（支援中文或英文）
        chapter: 章數
        verse: 節數
        use_simplified: 是否使用簡體中文

    Returns:
        包含原文分析的字典，包括：
        - testament: "OT" (舊約) 或 "NT" (新約)
        - original_text: 原文經文
        - translation: 原文直譯
        - words: 字詞分析列表

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 轉換書卷名稱為英文縮寫（API 需要）
    eng_short = BookNameConverter.get_english_short(book)
    if not eng_short:
        raise InvalidParameterError(f"找不到書卷: {book}")

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_word_analysis(
            book=eng_short,
            chapter=chapter,
            verse=verse,
        )

    # 判斷新舊約
    testament = "OT" if response["N"] == 1 else "NT"

    # 提取整節資訊（wid=0）
    original_text = ""
    translation = ""
    remark = ""

    if response["record"] and len(response["record"]) > 0:
        first_record = response["record"][0]
        if first_record.get("wid") == 0:
            original_text = first_record.get("word", "")
            translation = first_record.get("exp", "")
            remark = first_record.get("remark", "")

    # 提取個別字詞分析（wid>0）
    words = []
    for record in response["record"]:
        if record.get("wid") and record["wid"] > 0:
            word_info = {
                "position": record["wid"],
                "word": record.get("word", ""),
                "strongs_number": record.get("sn", ""),
                "part_of_speech": record.get("pro", ""),
                "morphology": record.get("wform", ""),
                "lemma": record.get("orig", ""),
                "gloss": record.get("exp", ""),
            }
            if record.get("remark"):
                word_info["remark"] = record["remark"]
            words.append(word_info)

    result = {
        "testament": testament,
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "original_text": original_text,
        "translation": translation,
        "word_count": len(words),
        "words": words,
    }

    if remark:
        result["remark"] = remark

    return result


async def lookup_strongs(
    number: int,
    testament: str = "NT",
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    查詢 Strong's 原文字典

    Args:
        number: Strong's 編號（如 25）
        testament: 聖經約別 "OT" (舊約) 或 "NT" (新約)
        use_simplified: 是否使用簡體中文

    Returns:
        字典條目，包括：
        - strongs_number: Strong's 編號
        - original_word: 原文字
        - chinese_definition: 中文定義
        - english_definition: 英文定義
        - related_words: 同源字列表（僅新約）

    Raises:
        InvalidParameterError: 參數錯誤
    """
    # 驗證約別
    if testament.upper() not in ["OT", "NT"]:
        raise InvalidParameterError(
            f"無效的約別: {testament}，應為 'OT' 或 'NT'"
        )

    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_strongs_dictionary(
            number=number,
            testament=testament.lower(),
        )

    if not response["record"] or len(response["record"]) == 0:
        raise InvalidParameterError(
            f"找不到 Strong's #{number} ({testament})"
        )

    record = response["record"][0]

    result = {
        "strongs_number": record["sn"],
        "original_word": record.get("orig", ""),
        "chinese_definition": record.get("dic_text", ""),
        "english_definition": record.get("edic_text", ""),
        "testament": testament.upper(),
    }

    # 添加同源字（僅新約有此資訊）
    if record.get("same") and len(record["same"]) > 0:
        related_words = []
        for same_word in record["same"]:
            related_words.append(
                {
                    "word": same_word["word"],
                    "number": same_word["csn"],
                    "occurrences": int(same_word["ccnt"]) if same_word.get("ccnt") else 0,
                    "gloss": same_word.get("cexp", ""),
                }
            )
        result["related_words"] = related_words

    return result


async def search_strongs_occurrences(
    number: int,
    testament: str = "NT",
    limit: int = 20,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    搜尋 Strong's 原文字在聖經中的所有出現位置

    Args:
        number: Strong's 編號
        testament: "OT" 或 "NT"
        limit: 最多返回筆數
        use_simplified: 是否使用簡體中文

    Returns:
        包含字典定義和出現位置的字典
    """
    # 先取得字典定義
    strongs_info = await lookup_strongs(number, testament, use_simplified)

    # 使用原文編號搜尋聖經
    search_type = "hebrew" if testament.upper() == "OT" else "greek"

    from .search import search_bible

    search_results = await search_bible(
        query=str(number),
        search_type=search_type,
        scope="ot" if testament.upper() == "OT" else "nt",
        limit=limit,
        use_simplified=use_simplified,
    )

    return {
        "strongs_info": strongs_info,
        "occurrences": {
            "total_count": search_results["total_count"],
            "showing": len(search_results["results"]),
            "results": search_results["results"],
        },
    }
