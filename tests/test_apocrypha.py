"""
Unit tests for Apocrypha (次經) API endpoints

Tests qsub.php and sesub.php endpoints for books 101-115.
"""

import pytest
import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


class TestApocryphaEndpoints:
    """Test Apocrypha API endpoints"""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for tests"""
        return FHLAPIEndpoints()
    
    @pytest.mark.asyncio
    async def test_get_apocrypha_verse_single(self, api_client):
        """Test querying a single Apocrypha verse"""
        result = await api_client.get_apocrypha_verse(
            book="多",  # Tobit
            chapter=1,
            verse="1"
        )
        
        assert result["status"] == "success"
        assert result["record_count"] >= 1
        assert "record" in result
        assert len(result["record"]) >= 1
        
        # Check verse structure
        verse = result["record"][0]
        assert "bid" in verse  # Apocrypha should have bid field
        assert "bible_text" in verse
        assert verse["chap"] == 1
        
        print(f"\n✅ 次經單節查詢成功")
        print(f"   書卷 ID: {verse.get('bid')}")
        print(f"   經文: {verse['bible_text'][:50]}...")
    
    @pytest.mark.asyncio
    async def test_get_apocrypha_verse_range(self, api_client):
        """Test querying Apocrypha verse range"""
        result = await api_client.get_apocrypha_verse(
            book="智",  # Wisdom  
            chapter=1,
            verse="1-3"
        )
        
        assert result["status"] == "success"
        assert result["record_count"] >= 3
        assert len(result["record"]) >= 3
        
        # Check bid field is present
        for verse in result["record"]:
            assert "bid" in verse
            assert verse["bid"] in range(101, 116)  # Apocrypha range
        
        print(f"\n✅ 次經範圍查詢成功 (1-3 節)")
        print(f"   返回 {result['record_count']} 節")
    
    @pytest.mark.asyncio
    async def test_get_apocrypha_chapter(self, api_client):
        """Test querying entire Apocrypha chapter"""
        result = await api_client.get_apocrypha_verse(
            book="德",  # Sirach
            chapter=1,
            verse=None  # No verse = entire chapter
        )
        
        assert result["status"] == "success"
        assert result["record_count"] > 0
        assert "record" in result
        
        print(f"\n✅ 次經整章查詢成功")
        print(f"   共 {result['record_count']} 節")
    
    @pytest.mark.asyncio
    async def test_search_apocrypha(self, api_client):
        """Test searching in Apocrypha"""
        result = await api_client.search_apocrypha(
            query="智慧",
            limit=5
        )
        
        assert result["status"] == "success"
        assert "record_count" in result
        assert "record" in result
        
        # Check results have bid field
        if result["record_count"] > 0:
            for verse in result["record"]:
                assert "bid" in verse
                assert verse["bid"] in range(101, 116)
                assert "bible_text" in verse
        
        print(f"\n✅ 次經搜尋成功")
        print(f"   關鍵字: 智慧")
        print(f"   找到 {result['record_count']} 筆結果")
        if result["record_count"] > 0:
            print(f"   第一筆: {result['record'][0]['bible_text'][:50]}...")
    
    @pytest.mark.asyncio
    async def test_search_apocrypha_with_offset(self, api_client):
        """Test Apocrypha search with pagination"""
        # First batch
        result1 = await api_client.search_apocrypha(
            query="愛",
            limit=3,
            offset=0
        )
        
        # Second batch
        result2 = await api_client.search_apocrypha(
            query="愛",
            limit=3,
            offset=3
        )
        
        assert result1["status"] == "success"
        assert result2["status"] == "success"
        
        # Results should be different (if total > 3)
        if result1["record_count"] > 3:
            assert result1["record"][0]["id"] != result2["record"][0]["id"]
        
        print(f"\n✅ 次經分頁搜尋成功")
        print(f"   總結果數: {result1['record_count']}")
        print(f"   第一批 (0-2): {len(result1['record'])} 筆")
        print(f"   第二批 (3-5): {len(result2['record'])} 筆")
    
    @pytest.mark.asyncio
    async def test_apocrypha_books(self, api_client):
        """Test different Apocrypha books"""
        books = [
            ("多", "Tobit"),
            ("友", "Judith"),
            ("智", "Wisdom"),
            ("德", "Sirach"),
        ]
        
        print(f"\n✅ 測試不同次經書卷:")
        
        for chinese, english in books:
            result = await api_client.get_apocrypha_verse(
                book=chinese,
                chapter=1,
                verse="1"
            )
            
            assert result["status"] == "success"
            assert result["record_count"] >= 1
            
            verse = result["record"][0]
            bid = verse.get("bid", "N/A")
            print(f"   {chinese} ({english}): Book ID {bid} ✓")


# Run tests if executed directly
if __name__ == "__main__":
    async def run_tests():
        """Run all tests"""
        client = FHLAPIEndpoints()
        test_instance = TestApocryphaEndpoints()
        
        print("=" * 70)
        print("次經 (Apocrypha) API 端點測試")
        print("=" * 70)
        
        try:
            # Test 1: Single verse
            await test_instance.test_get_apocrypha_verse_single(client)
            
            # Test 2: Verse range
            await test_instance.test_get_apocrypha_verse_range(client)
            
            # Test 3: Entire chapter
            await test_instance.test_get_apocrypha_chapter(client)
            
            # Test 4: Search
            await test_instance.test_search_apocrypha(client)
            
            # Test 5: Search with pagination
            await test_instance.test_search_apocrypha_with_offset(client)
            
            # Test 6: Different books
            await test_instance.test_apocrypha_books(client)
            
            print("\n" + "=" * 70)
            print("✅ 所有測試通過！")
            print("=" * 70)
            
        except Exception as e:
            print(f"\n❌ 測試失敗: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await client.close()
    
    asyncio.run(run_tests())
