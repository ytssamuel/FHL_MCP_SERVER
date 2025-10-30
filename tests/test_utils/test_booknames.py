"""
Test Book Name Conversion

Tests for Chinese-English book name conversion, traditional-simplified conversion, and fuzzy matching.
"""

import pytest
from fhl_bible_mcp.utils.booknames import BookNameConverter


def test_basic_conversion():
    """
    Test 1: 基本中英文轉換
    測試基礎的書卷名稱轉換功能
    """
    print("\n" + "="*70)
    print("Test 1: Basic Book Name Conversion")
    print("="*70)
    
    # 中文簡寫 -> 英文
    assert BookNameConverter.get_english_short("創") == "Gen"
    assert BookNameConverter.get_english_full("創") == "Genesis"
    
    # 中文全名 -> 英文
    assert BookNameConverter.get_english_short("創世記") == "Gen"
    assert BookNameConverter.get_english_full("創世記") == "Genesis"
    
    # 英文 -> 中文
    assert BookNameConverter.get_chinese_short("Gen") == "創"
    assert BookNameConverter.get_chinese_full("Genesis") == "創世記"
    
    # 約翰福音
    assert BookNameConverter.get_chinese_short("John") == "約"
    assert BookNameConverter.get_chinese_full("John") == "約翰福音"
    assert BookNameConverter.get_english_short("約") == "John"
    
    print("✅ Basic conversion works")
    print(f"   創 -> {BookNameConverter.get_english_full('創')}")
    print(f"   John -> {BookNameConverter.get_chinese_full('John')}")


def test_simplified_to_traditional():
    """
    Test 2: 簡體轉繁體
    測試簡體中文轉繁體中文
    """
    print("\n" + "="*70)
    print("Test 2: Simplified to Traditional Chinese")
    print("="*70)
    
    # 單字轉換
    assert BookNameConverter.simplified_to_traditional("创") == "創"
    assert BookNameConverter.simplified_to_traditional("约") == "約"
    assert BookNameConverter.simplified_to_traditional("启") == "啟"
    
    # 詞組轉換
    assert BookNameConverter.simplified_to_traditional("创世记") == "創世記"
    assert BookNameConverter.simplified_to_traditional("约翰福音") == "約翰福音"
    assert BookNameConverter.simplified_to_traditional("启示录") == "啟示錄"
    
    print("✅ Simplified to traditional conversion works")
    print(f"   创世记 -> {BookNameConverter.simplified_to_traditional('创世记')}")
    print(f"   约翰福音 -> {BookNameConverter.simplified_to_traditional('约翰福音')}")


def test_traditional_to_simplified():
    """
    Test 3: 繁體轉簡體
    測試繁體中文轉簡體中文
    """
    print("\n" + "="*70)
    print("Test 3: Traditional to Simplified Chinese")
    print("="*70)
    
    # 單字轉換
    assert BookNameConverter.traditional_to_simplified("創") == "创"
    assert BookNameConverter.traditional_to_simplified("約") == "约"
    assert BookNameConverter.traditional_to_simplified("啟") == "启"
    
    # 詞組轉換
    assert BookNameConverter.traditional_to_simplified("創世記") == "创世记"
    assert BookNameConverter.traditional_to_simplified("約翰福音") == "约翰福音"
    assert BookNameConverter.traditional_to_simplified("啟示錄") == "启示录"
    
    print("✅ Traditional to simplified conversion works")
    print(f"   創世記 -> {BookNameConverter.traditional_to_simplified('創世記')}")
    print(f"   約翰福音 -> {BookNameConverter.traditional_to_simplified('約翰福音')}")


def test_normalize_book_name():
    """
    Test 4: 標準化書卷名稱
    測試各種格式的書卷名稱標準化
    """
    print("\n" + "="*70)
    print("Test 4: Normalize Book Names")
    print("="*70)
    
    # 中文全名
    assert BookNameConverter.normalize_book_name("創世記") == "創"
    assert BookNameConverter.normalize_book_name("約翰福音") == "約"
    
    # 簡體中文
    assert BookNameConverter.normalize_book_name("创世记") == "創"
    assert BookNameConverter.normalize_book_name("约翰福音") == "約"
    
    # 英文
    assert BookNameConverter.normalize_book_name("Genesis") == "創"
    assert BookNameConverter.normalize_book_name("John") == "約"
    
    # 英文縮寫
    assert BookNameConverter.normalize_book_name("Gen") == "創"
    assert BookNameConverter.normalize_book_name("Matt") == "太"
    
    # 別名
    assert BookNameConverter.normalize_book_name("创") == "創"
    assert BookNameConverter.normalize_book_name("太福音") == "太"
    assert BookNameConverter.normalize_book_name("撒上") == "撒上"
    assert BookNameConverter.normalize_book_name("林前") == "林前"
    
    # 英文別名
    assert BookNameConverter.normalize_book_name("1sam") == "撒上"
    assert BookNameConverter.normalize_book_name("1 cor") == "林前"
    assert BookNameConverter.normalize_book_name("mt") == "太"
    
    print("✅ Book name normalization works")
    print(f"   创世记 -> {BookNameConverter.normalize_book_name('创世记')}")
    print(f"   1sam -> {BookNameConverter.normalize_book_name('1sam')}")
    print(f"   太福音 -> {BookNameConverter.normalize_book_name('太福音')}")


def test_fuzzy_search():
    """
    Test 5: 模糊搜尋
    測試書卷名稱模糊搜尋功能
    """
    print("\n" + "="*70)
    print("Test 5: Fuzzy Search")
    print("="*70)
    
    # 搜尋 "约"
    results = BookNameConverter.fuzzy_search("约")
    assert len(results) > 0
    # 應該包含約書亞、約伯、約珥、約拿、約翰等
    book_names = [r["chi_short"] for r in results]
    print(f"   搜尋 '约': {book_names}")
    
    # 搜尋 "john"
    results = BookNameConverter.fuzzy_search("john")
    assert len(results) > 0
    # 應該包含 John, 1 John, 2 John, 3 John
    book_names = [r["eng_short"] for r in results]
    print(f"   搜尋 'john': {book_names}")
    
    # 搜尋 "太"
    results = BookNameConverter.fuzzy_search("太")
    assert len(results) > 0
    assert results[0]["chi_short"] == "太"
    print(f"   搜尋 '太': {results[0]['chi_full']}")
    
    # 搜尋 "gen"
    results = BookNameConverter.fuzzy_search("gen")
    assert len(results) > 0
    assert results[0]["eng_short"] == "Gen"
    print(f"   搜尋 'gen': {results[0]['eng_full']}")
    
    print("✅ Fuzzy search works")


def test_get_book_info():
    """
    Test 6: 取得書卷完整資訊
    測試取得書卷詳細資訊
    """
    print("\n" + "="*70)
    print("Test 6: Get Book Information")
    print("="*70)
    
    # 用中文簡寫查詢
    info = BookNameConverter.get_book_info("創")
    assert info is not None
    assert info["id"] == 1
    assert info["eng_short"] == "Gen"
    assert info["eng_full"] == "Genesis"
    assert info["chi_short"] == "創"
    assert info["chi_full"] == "創世記"
    assert info["testament"] == "OT"
    assert info["testament_name"] == "舊約"
    
    # 用英文查詢
    info = BookNameConverter.get_book_info("John")
    assert info is not None
    assert info["id"] == 43
    assert info["testament"] == "NT"
    assert info["testament_name"] == "新約"
    
    # 用編號查詢
    info = BookNameConverter.get_book_info(1)
    assert info is not None
    assert info["chi_full"] == "創世記"
    
    # 用簡體中文查詢
    info = BookNameConverter.get_book_info("创世记")
    assert info is not None
    assert info["chi_full"] == "創世記"
    
    print("✅ Get book info works")
    print(f"   創 -> {info['eng_full']} ({info['testament_name']})")


def test_parse_reference():
    """
    Test 7: 解析經文引用
    測試經文引用格式解析
    """
    print("\n" + "="*70)
    print("Test 7: Parse Scripture Reference")
    print("="*70)
    
    # 中文格式
    ref = BookNameConverter.parse_reference("約3:16")
    assert ref is not None
    assert ref["book"] == "約"
    assert ref["chapter"] == 3
    assert ref["verse_start"] == 16
    assert ref["verse_end"] == 16
    print(f"   約3:16 -> {ref['book_full']} {ref['chapter']}:{ref['verse_start']}")
    
    # 英文格式
    ref = BookNameConverter.parse_reference("John 3:16")
    assert ref is not None
    assert ref["book"] == "約"
    assert ref["chapter"] == 3
    assert ref["verse_start"] == 16
    
    # 範圍格式
    ref = BookNameConverter.parse_reference("創 1:1-5")
    assert ref is not None
    assert ref["book"] == "創"
    assert ref["chapter"] == 1
    assert ref["verse_start"] == 1
    assert ref["verse_end"] == 5
    print(f"   創 1:1-5 -> {ref['book_full']} {ref['chapter']}:{ref['verse_start']}-{ref['verse_end']}")
    
    # 簡體中文
    ref = BookNameConverter.parse_reference("创世记 1:1")
    assert ref is not None
    assert ref["book"] == "創"
    assert ref["chapter"] == 1
    
    # 全名格式
    ref = BookNameConverter.parse_reference("馬太福音 5:3")
    assert ref is not None
    assert ref["book"] == "太"
    assert ref["chapter"] == 5
    assert ref["verse_start"] == 3
    
    print("✅ Parse reference works")


def test_book_id_conversion():
    """
    Test 8: 書卷編號轉換
    測試書卷編號與名稱的互轉
    """
    print("\n" + "="*70)
    print("Test 8: Book ID Conversion")
    print("="*70)
    
    # 編號 -> 名稱
    assert BookNameConverter.get_chinese_short("1") == "創"
    assert BookNameConverter.get_chinese_full("1") == "創世記"
    assert BookNameConverter.get_english_short("1") == "Gen"
    assert BookNameConverter.get_english_full("1") == "Genesis"
    
    # 名稱 -> 編號
    assert BookNameConverter.get_book_id("創") == 1
    assert BookNameConverter.get_book_id("約") == 43
    assert BookNameConverter.get_book_id("啟") == 66
    
    # 邊界測試
    assert BookNameConverter.get_chinese_short("39") == "瑪"  # 舊約最後一卷
    assert BookNameConverter.get_chinese_short("40") == "太"  # 新約第一卷
    assert BookNameConverter.get_chinese_short("66") == "啟"  # 最後一卷
    
    print("✅ Book ID conversion works")
    print(f"   1 -> {BookNameConverter.get_chinese_full('1')}")
    print(f"   43 -> {BookNameConverter.get_chinese_full('43')}")
    print(f"   66 -> {BookNameConverter.get_chinese_full('66')}")


def test_testament_check():
    """
    Test 9: 新舊約判斷
    測試書卷所屬新舊約判斷
    """
    print("\n" + "="*70)
    print("Test 9: Testament Check")
    print("="*70)
    
    # 舊約
    assert BookNameConverter.is_old_testament("創") == True
    assert BookNameConverter.is_new_testament("創") == False
    assert BookNameConverter.is_old_testament("瑪") == True
    
    # 新約
    assert BookNameConverter.is_old_testament("太") == False
    assert BookNameConverter.is_new_testament("太") == True
    assert BookNameConverter.is_new_testament("啟") == True
    
    # 邊界
    assert BookNameConverter.is_old_testament("39") == True
    assert BookNameConverter.is_new_testament("40") == True
    
    print("✅ Testament check works")
    print(f"   創 is OT: {BookNameConverter.is_old_testament('創')}")
    print(f"   太 is NT: {BookNameConverter.is_new_testament('太')}")


def test_all_books_list():
    """
    Test 10: 取得所有書卷列表
    測試取得完整書卷列表功能
    """
    print("\n" + "="*70)
    print("Test 10: Get All Books List")
    print("="*70)
    
    books = BookNameConverter.get_all_books()
    
    # 應該有 66 卷
    assert len(books) == 66
    
    # 檢查第一卷
    assert books[0]["id"] == 1
    assert books[0]["chi_full"] == "創世記"
    
    # 檢查最後一卷
    assert books[-1]["id"] == 66
    assert books[-1]["chi_full"] == "啟示錄"
    
    # 檢查結構
    first_book = books[0]
    assert "id" in first_book
    assert "eng_short" in first_book
    assert "eng_full" in first_book
    assert "chi_short" in first_book
    assert "chi_full" in first_book
    
    print("✅ Get all books list works")
    print(f"   Total books: {len(books)}")
    print(f"   First: {books[0]['chi_full']}")
    print(f"   Last: {books[-1]['chi_full']}")


def test_edge_cases():
    """
    Test 11: 邊界情況測試
    測試各種邊界情況和錯誤處理
    """
    print("\n" + "="*70)
    print("Test 11: Edge Cases")
    print("="*70)
    
    # 空字串
    assert BookNameConverter.get_book_id("") is None
    assert BookNameConverter.normalize_book_name("") is None
    assert BookNameConverter.parse_reference("") is None
    
    # 不存在的書卷
    assert BookNameConverter.get_book_id("不存在的書卷") is None
    assert BookNameConverter.normalize_book_name("xyz123") is None
    
    # 無效的編號
    assert BookNameConverter.get_chinese_short("0") is None
    assert BookNameConverter.get_chinese_short("67") is None
    assert BookNameConverter.get_chinese_short("999") is None
    
    # 無效的引用格式
    assert BookNameConverter.parse_reference("約翰") is None
    assert BookNameConverter.parse_reference("3:16") is None
    assert BookNameConverter.parse_reference("Book 3:16") is None
    
    print("✅ Edge cases handled correctly")


def test_case_insensitive_english():
    """
    Test 12: 英文大小寫不敏感
    測試英文書卷名大小寫不影響查詢
    """
    print("\n" + "="*70)
    print("Test 12: Case Insensitive English")
    print("="*70)
    
    # 大寫
    assert BookNameConverter.get_chinese_short("JOHN") == "約"
    assert BookNameConverter.get_chinese_short("GENESIS") == "創"
    
    # 小寫
    assert BookNameConverter.get_chinese_short("john") == "約"
    assert BookNameConverter.get_chinese_short("genesis") == "創"
    
    # 混合
    assert BookNameConverter.get_chinese_short("JoHn") == "約"
    assert BookNameConverter.get_chinese_short("GeNeSiS") == "創"
    
    print("✅ Case insensitive English works")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    """執行所有測試"""
    print("\n" + "="*70)
    print("FHL Bible MCP Server - Book Name Conversion Tests")
    print("="*70)
    
    tests = [
        ("Basic Conversion", test_basic_conversion),
        ("Simplified to Traditional", test_simplified_to_traditional),
        ("Traditional to Simplified", test_traditional_to_simplified),
        ("Normalize Book Name", test_normalize_book_name),
        ("Fuzzy Search", test_fuzzy_search),
        ("Get Book Info", test_get_book_info),
        ("Parse Reference", test_parse_reference),
        ("Book ID Conversion", test_book_id_conversion),
        ("Testament Check", test_testament_check),
        ("All Books List", test_all_books_list),
        ("Edge Cases", test_edge_cases),
        ("Case Insensitive", test_case_insensitive_english),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ Test Failed: {name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ Test Error: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # 顯示總結
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 All book name conversion tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
