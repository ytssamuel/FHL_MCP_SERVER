"""
原文研究 MCP Tools

提供希臘文、希伯來文字彙分析與 Strong's 字典查詢的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List, Union
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter
from ..utils.errors import InvalidParameterError


def _parse_strongs_input(
    input_value: Union[str, int],
    testament: Optional[str] = None,
) -> tuple[int, str]:
    """
    解析 Strong's Number 輸入，支援多種格式
    
    支援格式：
    - 整數: 3056 (需要 testament 參數)
    - 字串數字: "3056" (需要 testament 參數)
    - G 前綴: "G3056" → (3056, "NT")
    - H 前綴: "H430" → (430, "OT")
    - 前導零: "G03056" → (3056, "NT")
    
    Args:
        input_value: Strong's Number (整數、字串數字、或帶 G/H 前綴)
        testament: 約別 ("OT" 或 "NT")，當 input_value 無前綴時必填
        
    Returns:
        tuple[int, str]: (編號, 約別) 其中約別為 "OT" 或 "NT"
        
    Raises:
        InvalidParameterError: 輸入格式錯誤或缺少必要參數
        
    Examples:
        >>> _parse_strongs_input(3056, "NT")
        (3056, "NT")
        >>> _parse_strongs_input("G3056")
        (3056, "NT")
        >>> _parse_strongs_input("H430")
        (430, "OT")
        >>> _parse_strongs_input("03056", "NT")
        (3056, "NT")
    """
    # 處理整數輸入
    if isinstance(input_value, int):
        if testament is None:
            raise InvalidParameterError(
                parameter="testament",
                value=None,
                reason="整數輸入需要指定 testament 參數 ('OT' 或 'NT')"
            )
        return input_value, testament.upper()
    
    # 處理字串輸入
    input_str = str(input_value).strip().upper()
    
    if not input_str:
        raise InvalidParameterError(
            parameter="number",
            value=input_value,
            reason="Strong's Number 不能為空"
        )
    
    # 檢查是否有 G 或 H 前綴
    if input_str.startswith('G'):
        detected_testament = "NT"
        number_str = input_str[1:]
    elif input_str.startswith('H'):
        detected_testament = "OT"
        number_str = input_str[1:]
    else:
        # 純數字字串，需要 testament 參數
        if testament is None:
            raise InvalidParameterError(
                parameter="testament",
                value=None,
                reason=f"數字字串輸入 '{input_value}' 需要指定 testament 參數 ('OT' 或 'NT')"
            )
        detected_testament = testament.upper()
        number_str = input_str
    
    # 驗證約別
    if detected_testament not in ["OT", "NT"]:
        raise InvalidParameterError(
            parameter="testament",
            value=detected_testament,
            reason="應為 'OT' 或 'NT'"
        )
    
    # 移除前導零並轉換為整數
    try:
        number = int(number_str.lstrip('0') or '0')
    except ValueError:
        raise InvalidParameterError(
            parameter="number",
            value=input_value,
            reason="無效的 Strong's Number 格式"
        )
    
    if number <= 0:
        raise InvalidParameterError(
            parameter="number",
            value=input_value,
            reason="Strong's Number 必須大於 0"
        )
    
    return number, detected_testament


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
    number: Union[int, str],
    testament: Optional[str] = None,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    查詢 Strong's 原文字典
    
    支援多種輸入格式：
    - 整數 + testament: lookup_strongs(3056, "NT")
    - 字串數字 + testament: lookup_strongs("3056", "NT")
    - G 前綴（新約）: lookup_strongs("G3056")
    - H 前綴（舊約）: lookup_strongs("H430")

    Args:
        number: Strong's 編號（整數、字串數字、或帶 G/H 前綴）
        testament: 聖經約別 "OT" (舊約) 或 "NT" (新約)，當 number 無前綴時必填
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
        
    Examples:
        >>> await lookup_strongs(3056, "NT")  # 整數 + testament
        >>> await lookup_strongs("G3056")      # G 前綴（新約）
        >>> await lookup_strongs("H430")       # H 前綴（舊約）
    """
    # 解析輸入格式
    parsed_number, parsed_testament = _parse_strongs_input(number, testament)

    # 呼叫 API（API 只接受整數）
    async with FHLAPIEndpoints() as api:
        response = await api.get_strongs_dictionary(
            number=parsed_number,
            testament=parsed_testament.lower(),
        )

    if not response["record"] or len(response["record"]) == 0:
        raise InvalidParameterError(
            parameter="number",
            value=number,
            reason=f"找不到 Strong's #{parsed_number} ({parsed_testament})"
        )

    record = response["record"][0]

    result = {
        "strongs_number": record["sn"],
        "original_word": record.get("orig", ""),
        "chinese_definition": record.get("dic_text", ""),
        "english_definition": record.get("edic_text", ""),
        "testament": parsed_testament,
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
    number: Union[int, str],
    testament: Optional[str] = None,
    limit: int = 20,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    搜尋 Strong's 原文字在聖經中的所有出現位置
    
    支援多種輸入格式：
    - 整數 + testament: search_strongs_occurrences(1344, "NT")
    - 字串數字 + testament: search_strongs_occurrences("1344", "NT")
    - G 前綴（新約）: search_strongs_occurrences("G1344")
    - H 前綴（舊約）: search_strongs_occurrences("H430")

    Args:
        number: Strong's 編號（整數、字串數字、或帶 G/H 前綴）
        testament: "OT" 或 "NT"，當 number 無前綴時必填
        limit: 最多返回筆數
        use_simplified: 是否使用簡體中文

    Returns:
        包含字典定義和出現位置的字典
        
    Examples:
        >>> await search_strongs_occurrences(1344, "NT")  # 整數 + testament
        >>> await search_strongs_occurrences("G1344")     # G 前綴（新約）
        >>> await search_strongs_occurrences("H430")      # H 前綴（舊約）
    """
    # 解析輸入格式
    parsed_number, parsed_testament = _parse_strongs_input(number, testament)
    
    # 先取得字典定義（使用解析後的值）
    strongs_info = await lookup_strongs(number, testament, use_simplified)

    # 使用純數字（無前綴）搜尋聖經
    search_type = "hebrew_number" if parsed_testament == "OT" else "greek_number"

    from .search import search_bible

    search_results = await search_bible(
        query=str(parsed_number),  # 使用純數字，不含 G/H 前綴
        search_type=search_type,
        scope="ot" if parsed_testament == "OT" else "nt",
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
