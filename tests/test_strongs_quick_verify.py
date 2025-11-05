#!/usr/bin/env python3
"""
P1 Strong's 功能修復驗證腳本

快速驗證修復後的 Strong's 字典功能是否正常運作。
執行方式: python tests/test_strongs_quick_verify.py
"""

import asyncio
import sys
from pathlib import Path

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fhl_bible_mcp.tools.strongs import lookup_strongs, search_strongs_occurrences


def print_section(title: str):
    """打印章節標題"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_result(test_name: str, passed: bool, message: str = ""):
    """打印測試結果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {test_name}")
    if message:
        print(f"     └─ {message}")


async def test_lookup_strongs_g_prefix():
    """測試 G 前綴格式（新約）"""
    try:
        result = await lookup_strongs("G3056")
        
        # 驗證結果
        is_valid = (
            result["strongs_number"] != "00000" and
            result["testament"] == "NT" and
            len(result["original_word"]) > 0 and
            len(result["chinese_definition"]) > 0
        )
        
        print_result(
            "lookup_strongs('G3056')",
            is_valid,
            f"λόγος, 定義長度: {len(result['chinese_definition'])}"
        )
        return is_valid
    except Exception as e:
        print_result("lookup_strongs('G3056')", False, f"異常: {e}")
        return False


async def test_lookup_strongs_h_prefix():
    """測試 H 前綴格式（舊約）"""
    try:
        result = await lookup_strongs("H430")
        
        is_valid = (
            result["strongs_number"] != "00000" and
            result["testament"] == "OT" and
            len(result["original_word"]) > 0 and
            len(result["chinese_definition"]) > 0
        )
        
        print_result(
            "lookup_strongs('H430')",
            is_valid,
            f"אֱלֹהִים, 定義長度: {len(result['chinese_definition'])}"
        )
        return is_valid
    except Exception as e:
        print_result("lookup_strongs('H430')", False, f"異常: {e}")
        return False


async def test_lookup_strongs_integer():
    """測試整數格式（向後兼容）"""
    try:
        result = await lookup_strongs(3056, "NT")
        
        is_valid = (
            result["strongs_number"] != "00000" and
            result["testament"] == "NT" and
            len(result["original_word"]) > 0
        )
        
        print_result(
            "lookup_strongs(3056, 'NT')",
            is_valid,
            f"向後兼容驗證通過"
        )
        return is_valid
    except Exception as e:
        print_result("lookup_strongs(3056, 'NT')", False, f"異常: {e}")
        return False


async def test_search_strongs_g1344():
    """測試 G1344 搜尋（δικαιόω, 稱義）"""
    try:
        result = await search_strongs_occurrences("G1344", limit=5)
        
        is_valid = (
            result["occurrences"]["total_count"] > 0 and
            len(result["occurrences"]["results"]) > 0 and
            result["strongs_info"]["testament"] == "NT"
        )
        
        print_result(
            "search_strongs_occurrences('G1344')",
            is_valid,
            f"找到 {result['occurrences']['total_count']} 處出現"
        )
        return is_valid
    except Exception as e:
        print_result("search_strongs_occurrences('G1344')", False, f"異常: {e}")
        return False


async def test_search_strongs_h430():
    """測試 H430 搜尋（אֱלֹהִים, 神）"""
    try:
        result = await search_strongs_occurrences("H430", limit=5)
        
        is_valid = (
            result["occurrences"]["total_count"] > 0 and
            len(result["occurrences"]["results"]) > 0 and
            result["strongs_info"]["testament"] == "OT"
        )
        
        print_result(
            "search_strongs_occurrences('H430')",
            is_valid,
            f"找到 {result['occurrences']['total_count']} 處出現"
        )
        return is_valid
    except Exception as e:
        print_result("search_strongs_occurrences('H430')", False, f"異常: {e}")
        return False


async def test_format_consistency():
    """測試多格式一致性"""
    try:
        result1 = await lookup_strongs(3056, "NT")
        result2 = await lookup_strongs("3056", "NT")
        result3 = await lookup_strongs("G3056")
        result4 = await lookup_strongs("G03056")
        
        is_valid = (
            result1["strongs_number"] == result2["strongs_number"] ==
            result3["strongs_number"] == result4["strongs_number"] and
            result1["original_word"] == result2["original_word"] ==
            result3["original_word"] == result4["original_word"]
        )
        
        print_result(
            "多格式一致性驗證",
            is_valid,
            "4 種格式返回相同結果"
        )
        return is_valid
    except Exception as e:
        print_result("多格式一致性驗證", False, f"異常: {e}")
        return False


async def main():
    """主測試函數"""
    print_section("P1 Strong's 功能修復驗證")
    print("開始驗證修復後的功能...")
    
    results = []
    
    # 測試 lookup_strongs
    print_section("1️⃣  lookup_strongs 功能測試")
    results.append(await test_lookup_strongs_g_prefix())
    results.append(await test_lookup_strongs_h_prefix())
    results.append(await test_lookup_strongs_integer())
    
    # 測試 search_strongs_occurrences
    print_section("2️⃣  search_strongs_occurrences 功能測試")
    results.append(await test_search_strongs_g1344())
    results.append(await test_search_strongs_h430())
    
    # 測試一致性
    print_section("3️⃣  多格式一致性測試")
    results.append(await test_format_consistency())
    
    # 總結
    print_section("📊 測試總結")
    passed = sum(results)
    total = len(results)
    
    print(f"\n通過測試: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有測試通過！P1 Strong's 功能修復成功！")
        print("\n修復成效:")
        print("  ✅ lookup_strongs 支援 G/H 前綴")
        print("  ✅ search_strongs_occurrences 返回實際結果")
        print("  ✅ 向後兼容現有代碼")
        print("  ✅ 多格式輸入一致性")
        return 0
    else:
        print(f"\n❌ 有 {total - passed} 個測試失敗，需要進一步檢查。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
