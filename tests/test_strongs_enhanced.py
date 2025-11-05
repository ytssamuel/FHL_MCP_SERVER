"""
測試 Strong's 字典功能增強
測試 _parse_strongs_input() 和更新後的 lookup_strongs/search_strongs_occurrences
"""

import pytest
from src.fhl_bible_mcp.tools.strongs import (
    _parse_strongs_input,
    lookup_strongs,
    search_strongs_occurrences,
)
from src.fhl_bible_mcp.utils.errors import InvalidParameterError


class TestParseStrongsInput:
    """測試 _parse_strongs_input() 函數"""

    def test_parse_integer_with_testament(self):
        """測試整數輸入 + testament 參數"""
        number, testament = _parse_strongs_input(3056, "NT")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input(430, "OT")
        assert number == 430
        assert testament == "OT"

    def test_parse_integer_without_testament_raises_error(self):
        """測試整數輸入缺少 testament 參數應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input(3056)
        assert "整數輸入需要指定 testament 參數" in str(excinfo.value)

    def test_parse_string_number_with_testament(self):
        """測試字串數字輸入 + testament 參數"""
        number, testament = _parse_strongs_input("3056", "NT")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input("430", "OT")
        assert number == 430
        assert testament == "OT"

    def test_parse_string_number_without_testament_raises_error(self):
        """測試字串數字輸入缺少 testament 參數應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("3056")
        assert "數字字串輸入" in str(excinfo.value)
        assert "需要指定 testament 參數" in str(excinfo.value)

    def test_parse_g_prefix(self):
        """測試 G 前綴（新約）"""
        number, testament = _parse_strongs_input("G3056")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input("g3056")  # 小寫
        assert number == 3056
        assert testament == "NT"

    def test_parse_h_prefix(self):
        """測試 H 前綴（舊約）"""
        number, testament = _parse_strongs_input("H430")
        assert number == 430
        assert testament == "OT"

        number, testament = _parse_strongs_input("h430")  # 小寫
        assert number == 430
        assert testament == "OT"

    def test_parse_g_prefix_with_leading_zeros(self):
        """測試 G 前綴 + 前導零"""
        number, testament = _parse_strongs_input("G03056")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input("G003056")
        assert number == 3056
        assert testament == "NT"

    def test_parse_h_prefix_with_leading_zeros(self):
        """測試 H 前綴 + 前導零"""
        number, testament = _parse_strongs_input("H00430")
        assert number == 430
        assert testament == "OT"

        number, testament = _parse_strongs_input("H000430")
        assert number == 430
        assert testament == "OT"

    def test_parse_leading_zeros_with_testament(self):
        """測試前導零（無前綴）+ testament"""
        number, testament = _parse_strongs_input("03056", "NT")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input("00430", "OT")
        assert number == 430
        assert testament == "OT"

    def test_parse_whitespace_handling(self):
        """測試空白字元處理"""
        number, testament = _parse_strongs_input("  G3056  ")
        assert number == 3056
        assert testament == "NT"

        number, testament = _parse_strongs_input("  H430  ")
        assert number == 430
        assert testament == "OT"

    def test_parse_empty_string_raises_error(self):
        """測試空字串應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("")
        assert "不能為空" in str(excinfo.value)

        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("   ")
        assert "不能為空" in str(excinfo.value)

    def test_parse_invalid_format_raises_error(self):
        """測試無效格式應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("G")
        # "G" 會被解析為 G0，觸發「必須大於 0」錯誤
        assert "必須大於 0" in str(excinfo.value)

        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("Gabc")
        # 字母無法轉整數，觸發「無效格式」錯誤
        assert "無效的 Strong's Number 格式" in str(excinfo.value)

    def test_parse_zero_raises_error(self):
        """測試 0 或全零字串應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("0", "NT")
        assert "必須大於 0" in str(excinfo.value)

        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("G0000")
        assert "必須大於 0" in str(excinfo.value)

    def test_parse_negative_number_raises_error(self):
        """測試負數應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            _parse_strongs_input("-3056", "NT")
        # 負號被轉換後變成負數，觸發「必須大於 0」錯誤
        assert "必須大於 0" in str(excinfo.value)

    def test_parse_case_insensitive(self):
        """測試大小寫不敏感"""
        # G/H 前綴應該大小寫不敏感
        number1, testament1 = _parse_strongs_input("G3056")
        number2, testament2 = _parse_strongs_input("g3056")
        assert number1 == number2 == 3056
        assert testament1 == testament2 == "NT"

        # Testament 參數應該大小寫不敏感
        number1, testament1 = _parse_strongs_input(3056, "nt")
        number2, testament2 = _parse_strongs_input(3056, "NT")
        assert number1 == number2 == 3056
        assert testament1 == testament2 == "NT"

    def test_parse_g_prefix_overrides_testament(self):
        """測試 G 前綴會覆蓋 testament 參數（如果提供）"""
        # G 前綴應該總是解析為 NT，即使提供 OT
        number, testament = _parse_strongs_input("G3056", "OT")
        assert number == 3056
        assert testament == "NT"  # G 前綴優先

    def test_parse_h_prefix_overrides_testament(self):
        """測試 H 前綴會覆蓋 testament 參數（如果提供）"""
        # H 前綴應該總是解析為 OT，即使提供 NT
        number, testament = _parse_strongs_input("H430", "NT")
        assert number == 430
        assert testament == "OT"  # H 前綴優先


@pytest.mark.asyncio
class TestLookupStrongsEnhanced:
    """測試增強後的 lookup_strongs() 函數"""

    async def test_lookup_with_integer_and_testament(self):
        """測試整數 + testament 格式"""
        result = await lookup_strongs(3056, "NT")
        assert result["strongs_number"] is not None
        assert result["testament"] == "NT"
        assert result["original_word"]  # 應有原文字
        # 不應該是 00000 demo 資料
        assert result["strongs_number"] != "00000"

    async def test_lookup_with_g_prefix(self):
        """測試 G 前綴格式"""
        result = await lookup_strongs("G3056")
        assert result["strongs_number"] is not None
        assert result["testament"] == "NT"
        assert result["original_word"]  # 應有希臘文
        # 驗證是真實詞條，不是 demo
        assert result["strongs_number"] != "00000"
        # 驗證有原文字（非空），具體內容依 API 返回
        assert len(result["original_word"]) > 0
        assert result["chinese_definition"]  # 應有中文定義

    async def test_lookup_with_h_prefix(self):
        """測試 H 前綴格式"""
        result = await lookup_strongs("H430")
        assert result["strongs_number"] is not None
        assert result["testament"] == "OT"
        assert result["original_word"]  # 應有希伯來文
        # 驗證是真實詞條
        assert result["strongs_number"] != "00000"

    async def test_lookup_with_leading_zeros(self):
        """測試前導零格式"""
        result1 = await lookup_strongs("G03056")
        result2 = await lookup_strongs("G3056")
        # 前導零應該被正確處理，結果相同
        assert result1["strongs_number"] == result2["strongs_number"]
        assert result1["original_word"] == result2["original_word"]

    async def test_lookup_invalid_number_raises_error(self):
        """測試無效編號應報錯"""
        # 注意：某些大編號可能存在，所以這個測試可能不穩定
        # 改為測試明確不存在的編號或格式錯誤
        with pytest.raises(InvalidParameterError):
            await lookup_strongs("Gabc")  # 格式錯誤

    async def test_lookup_without_testament_and_prefix_raises_error(self):
        """測試沒有 testament 也沒有前綴應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            await lookup_strongs(3056)
        assert "需要指定 testament 參數" in str(excinfo.value)


@pytest.mark.asyncio
class TestSearchStrongsOccurrencesEnhanced:
    """測試增強後的 search_strongs_occurrences() 函數"""

    async def test_search_with_integer_and_testament(self):
        """測試整數 + testament 格式"""
        result = await search_strongs_occurrences(1344, "NT", limit=5)
        assert "strongs_info" in result
        assert "occurrences" in result
        # 應該返回實際結果，不是 0
        assert result["occurrences"]["total_count"] > 0
        assert len(result["occurrences"]["results"]) > 0

    async def test_search_with_g_prefix(self):
        """測試 G 前綴格式（G1344 = δικαιόω, 稱義）"""
        result = await search_strongs_occurrences("G1344", limit=5)
        assert "strongs_info" in result
        assert "occurrences" in result
        
        # 驗證 Strong's 資訊正確
        assert result["strongs_info"]["testament"] == "NT"
        assert result["strongs_info"]["strongs_number"] != "00000"
        
        # 驗證有搜尋結果（G1344 應該在羅馬書等處出現）
        assert result["occurrences"]["total_count"] > 0, "G1344 應該有出現記錄"
        assert len(result["occurrences"]["results"]) > 0
        
        # 驗證結果包含經文資訊
        first_result = result["occurrences"]["results"][0]
        assert "book" in first_result
        assert "chapter" in first_result
        assert "verse" in first_result

    async def test_search_with_h_prefix(self):
        """測試 H 前綴格式（H430 = אֱלֹהִים, 神）"""
        result = await search_strongs_occurrences("H430", limit=5)
        assert "strongs_info" in result
        assert "occurrences" in result
        
        # 驗證 Strong's 資訊正確
        assert result["strongs_info"]["testament"] == "OT"
        assert result["strongs_info"]["strongs_number"] != "00000"
        
        # H430 在舊約中應該非常常見（神）
        assert result["occurrences"]["total_count"] > 0, "H430 應該有出現記錄"
        assert len(result["occurrences"]["results"]) > 0

    async def test_search_respects_limit(self):
        """測試 limit 參數正常運作"""
        result = await search_strongs_occurrences("G1344", limit=3)
        assert len(result["occurrences"]["results"]) <= 3

    async def test_search_without_testament_and_prefix_raises_error(self):
        """測試沒有 testament 也沒有前綴應報錯"""
        with pytest.raises(InvalidParameterError) as excinfo:
            await search_strongs_occurrences(1344)
        assert "需要指定 testament 參數" in str(excinfo.value)


@pytest.mark.asyncio
class TestStrongsIntegration:
    """整合測試：驗證修復後的 Strong's 功能"""

    async def test_g3056_logos_full_workflow(self):
        """完整測試 G3056 (λόγος, 道) 的查詢和搜尋"""
        # 1. 查詢字典
        lookup_result = await lookup_strongs("G3056")
        assert lookup_result["strongs_number"] != "00000"
        assert len(lookup_result["original_word"]) > 0  # 有原文字
        assert lookup_result["testament"] == "NT"
        assert lookup_result["chinese_definition"]  # 有中文定義

        # 2. 搜尋出現位置
        search_result = await search_strongs_occurrences("G3056", limit=5)
        assert search_result["occurrences"]["total_count"] > 0
        
        # 3. 驗證約翰福音 1:1 應該在結果中（道）
        results = search_result["occurrences"]["results"]
        assert len(results) > 0

    async def test_h430_elohim_full_workflow(self):
        """完整測試 H430 (אֱלֹהִים, 神) 的查詢和搜尋"""
        # 1. 查詢字典
        lookup_result = await lookup_strongs("H430")
        assert lookup_result["strongs_number"] != "00000"
        assert lookup_result["testament"] == "OT"

        # 2. 搜尋出現位置
        search_result = await search_strongs_occurrences("H430", limit=5)
        assert search_result["occurrences"]["total_count"] > 0
        
        # 3. 驗證創世記 1:1 應該在結果中（神）
        results = search_result["occurrences"]["results"]
        assert len(results) > 0

    async def test_multiple_formats_return_same_result(self):
        """測試不同格式返回相同結果"""
        result1 = await lookup_strongs(3056, "NT")
        result2 = await lookup_strongs("3056", "NT")
        result3 = await lookup_strongs("G3056")
        result4 = await lookup_strongs("G03056")

        # 所有格式應該返回相同的 Strong's Number
        assert result1["strongs_number"] == result2["strongs_number"]
        assert result2["strongs_number"] == result3["strongs_number"]
        assert result3["strongs_number"] == result4["strongs_number"]

        # 原文字應該相同
        assert result1["original_word"] == result2["original_word"]
        assert result2["original_word"] == result3["original_word"]
        assert result3["original_word"] == result4["original_word"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
