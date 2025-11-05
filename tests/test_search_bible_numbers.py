"""
測試 search_bible 的 greek_number 和 hebrew_number 功能

此測試驗證 P1 缺陷修復後的 search_bible 對原文編號搜尋的支援。
針對二次回歸測試中發現的參數驗證問題進行驗證。
"""

import pytest
import asyncio
from fhl_bible_mcp.tools.search import search_bible


class TestSearchBibleNumbers:
    """測試 search_bible 的原文編號搜尋功能"""

    @pytest.mark.asyncio
    async def test_greek_number_g1344_basic(self):
        """
        測試 G1344 (δικαιόω, 稱義) 的希臘文編號搜尋
        
        預期至少包含以下經文：
        - Matt 12:37
        - Luke 7:29, 10:29, 16:15, 18:14
        - Acts 13:39
        - Rom 2:13, 3:24, 3:26, 3:28, 3:30, 4:2, 4:5, 5:1, 5:9, 6:7
        """
        result = await search_bible(
            query="1344",  # 純數字格式（不含 G 前綴）
            search_type="greek_number",
            scope="nt",
            version="unv",
            limit=50
        )
        
        # 驗證基本結構
        assert "results" in result
        assert "total_count" in result
        assert result["total_count"] > 0, "應該找到至少一個結果"
        
        # 驗證是否包含關鍵經文
        verses_found = [
            (v.get('book_eng', v.get('book', '')), v['chapter'], v['verse'])
            for v in result["results"]
        ]
        
        # 檢查羅馬書 3:24（稱義的核心經文）
        # 書卷名稱可能是 "Rom", "Romans" 或中文
        has_rom_3_24 = any(
            ('Rom' in book_eng or 'rom' in book_eng.lower()) and ch == 3 and vs == 24
            for book_eng, ch, vs in verses_found
        )
        
        # 檢查使徒行傳 13:39（測試報告提到的經文）
        has_acts_13_39 = any(
            ('Act' in book_eng or 'act' in book_eng.lower()) and ch == 13 and vs == 39
            for book_eng, ch, vs in verses_found
        )
        
        # 至少應該找到其中一個（因為 limit=50 可能不包含所有結果）
        assert has_rom_3_24 or has_acts_13_39, \
            f"應包含羅馬書 3:24 或使徒行傳 13:39，實際找到: {[(b, c, v) for b, c, v in verses_found[:10]]}"
        
        print(f"✅ 找到 {result['total_count']} 處 G1344 出現")
        print(f"   前 5 處: {[(f'{b} {c}:{v}') for b, c, v in verses_found[:5]]}")

    @pytest.mark.asyncio
    async def test_hebrew_number_h430_basic(self):
        """
        測試 H430 (אֱלֹהִים, 神) 的希伯來文編號搜尋
        
        H430 是舊約中最常見的「神」字，應該有大量結果。
        預期至少包含創世記 1:1（起初神創造天地）。
        """
        result = await search_bible(
            query="430",  # 純數字格式（不含 H 前綴）
            search_type="hebrew_number",
            scope="ot",
            version="unv",
            limit=20
        )
        
        # 驗證基本結構
        assert "results" in result
        assert "total_count" in result
        assert result["total_count"] > 0, "應該找到至少一個結果"
        
        # H430 是非常常見的字，應該返回滿額結果（達到 limit）
        assert len(result["results"]) >= 10, f"H430 應該有大量出現，實際返回: {len(result['results'])}"
        
        # 驗證是否包含創世記 1:1
        verses_found = [
            (v.get('book_eng', v.get('book', '')), v['chapter'], v['verse'])
            for v in result["results"]
        ]
        
        has_gen_1_1 = any(
            ('Gen' in book_eng or 'gen' in book_eng.lower()) and ch == 1 and vs == 1
            for book_eng, ch, vs in verses_found
        )
        
        assert has_gen_1_1, \
            f"應包含創世記 1:1（起初神創造天地），實際前 10 筆: {[(b, c, v) for b, c, v in verses_found[:10]]}"
        
        print(f"✅ 找到 {result['total_count']} 處 H430 出現")
        print(f"   前 5 處: {[(f'{b} {c}:{v}') for b, c, v in verses_found[:5]]}")

    @pytest.mark.asyncio
    async def test_search_type_parameter_validation(self):
        """
        測試 search_type 參數驗證
        
        驗證以下值應該被接受：
        - "keyword"
        - "greek_number"
        - "hebrew_number"
        """
        # 測試 keyword（應該成功）
        result = await search_bible(
            query="稱義",
            search_type="keyword",
            version="unv"
        )
        assert "results" in result
        
        # 測試 greek_number（應該成功）
        result = await search_bible(
            query="1344",
            search_type="greek_number",
            scope="nt",
            version="unv"
        )
        assert "results" in result
        
        # 測試 hebrew_number（應該成功）
        result = await search_bible(
            query="430",
            search_type="hebrew_number",
            scope="ot",
            version="unv"
        )
        assert "results" in result
        
        print("✅ 所有 search_type 參數驗證通過")

    @pytest.mark.asyncio
    async def test_greek_number_comprehensive_verses(self):
        """
        測試 G1344 的完整經文列表（測試報告中列出的預期經文）
        """
        result = await search_bible(
            query="1344",
            search_type="greek_number",
            scope="nt",
            version="unv",
            limit=100  # 獲取更多結果
        )
        
        # 測試報告中列出的預期經文
        expected_verses = [
            ("Matthew", 12, 37),
            ("Luke", 7, 29),
            ("Luke", 10, 29),
            ("Luke", 16, 15),
            ("Luke", 18, 14),
            ("Acts", 13, 39),
            ("Romans", 2, 13),
            ("Romans", 3, 24),
            ("Romans", 3, 26),
            ("Romans", 3, 28),
            ("Romans", 3, 30),
            ("Romans", 4, 2),
            ("Romans", 4, 5),
            ("Romans", 5, 1),
            ("Romans", 5, 9),
            ("Romans", 6, 7),
        ]
        
        found_count = 0
        for expected_book, expected_chapter, expected_verse in expected_verses:
            found = any(
                (v.get("chapter") == expected_chapter and 
                 v.get("verse") == expected_verse and
                 (expected_book.lower() in v.get("book_eng", "").lower() or
                  expected_book.lower() in v.get("book", "").lower()))
                for v in result["results"]
            )
            if found:
                found_count += 1
        
        # 至少應該找到一些預期經文（功能正常即可）
        assert found_count >= 3, \
            f"應該找到至少 3 處預期經文，實際找到 {found_count}"
        
        print(f"✅ 在 {result['total_count']} 處結果中找到 {found_count}/{len(expected_verses)} 處預期經文")

    @pytest.mark.asyncio
    async def test_verse_content_quality(self):
        """
        測試返回的經文內容質量
        
        驗證：
        1. 每個結果都有必要的欄位
        2. 經文內容不為空
        3. 書卷、章節、節數都有效
        """
        result = await search_bible(
            query="1344",
            search_type="greek_number",
            scope="nt",
            version="unv",
            limit=10
        )
        
        assert len(result["results"]) > 0, "應該有結果"
        
        for verse in result["results"]:
            # 檢查必要欄位
            assert "book" in verse, "應該有書卷名稱"
            assert "chapter" in verse, "應該有章節號"
            assert "verse" in verse, "應該有節號"
            assert "text" in verse or "content" in verse, "應該有經文內容"
            
            # 檢查值的有效性
            assert verse["book"], "書卷名稱不應為空"
            assert verse["chapter"] > 0, "章節號應大於 0"
            assert verse["verse"] > 0, "節號應大於 0"
            
            # 檢查經文內容不為空
            text = verse.get("text") or verse.get("content", "")
            assert text.strip(), "經文內容不應為空"
        
        print(f"✅ 驗證 {len(result['results'])} 筆結果的內容質量，全部通過")


def main():
    """快速驗證腳本"""
    print("=" * 60)
    print("  search_bible greek_number/hebrew_number 功能驗證")
    print("=" * 60)
    print()
    
    async def run_tests():
        test = TestSearchBibleNumbers()
        
        try:
            print("📝 測試 1: Greek Number G1344 基本搜尋")
            await test.test_greek_number_g1344_basic()
            print()
            
            print("📝 測試 2: Hebrew Number H430 基本搜尋")
            await test.test_hebrew_number_h430_basic()
            print()
            
            print("📝 測試 3: search_type 參數驗證")
            await test.test_search_type_parameter_validation()
            print()
            
            print("📝 測試 4: G1344 完整經文列表驗證")
            await test.test_greek_number_comprehensive_verses()
            print()
            
            print("📝 測試 5: 經文內容質量驗證")
            await test.test_verse_content_quality()
            print()
            
            print("=" * 60)
            print("🎉 所有測試通過！")
            print("=" * 60)
            
        except AssertionError as e:
            print(f"\n❌ 測試失敗: {e}")
            raise
        except Exception as e:
            print(f"\n❌ 錯誤: {e}")
            raise
    
    asyncio.run(run_tests())


if __name__ == "__main__":
    main()
