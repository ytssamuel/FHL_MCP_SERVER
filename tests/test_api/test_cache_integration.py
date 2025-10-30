"""
Test Cache Integration with API Endpoints

Tests for cache integration in FHLAPIEndpoints.
"""

import pytest
import time
from pathlib import Path
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.utils.cache import reset_cache


@pytest.mark.asyncio
async def test_cache_integration_versions():
    """
    Test 1: 版本列表快取測試
    測試 get_bible_versions 的快取功能
    """
    print("\n" + "="*70)
    print("Test 1: Bible Versions Caching")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 第一次呼叫 - 應該從 API 取得
        start1 = time.time()
        result1 = await client.get_bible_versions()
        time1 = time.time() - start1
        
        assert result1["status"] == "success"
        count1 = result1["record_count"]
        print(f"   First call: {count1} versions, took {time1:.3f}s")
        
        # 第二次呼叫 - 應該從快取取得
        start2 = time.time()
        result2 = await client.get_bible_versions()
        time2 = time.time() - start2
        
        assert result2["status"] == "success"
        assert result2["record_count"] == count1
        print(f"   Second call: {count1} versions, took {time2:.3f}s")
        
        # 快取應該更快 (避免除以零)
        if time2 > 0:
            print(f"   Speedup: {time1/time2:.1f}x faster")
        else:
            print(f"   Speedup: Cache is extremely fast (< 0.001s)")
        
        # 檢查快取統計
        stats = client.cache.stats
        print(f"   Cache stats: hits={stats['hits']}, misses={stats['misses']}")
        assert stats['hits'] >= 1, "Should have cache hits"
    
    print("✅ Bible versions caching works")


@pytest.mark.asyncio
async def test_cache_integration_verses():
    """
    Test 2: 經文快取測試
    測試 get_verse 的快取功能
    """
    print("\n" + "="*70)
    print("Test 2: Verse Caching")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 第一次查詢 John 3:16
        start1 = time.time()
        result1 = await client.get_verse("約", 3, "16", version="unv")
        time1 = time.time() - start1
        
        assert result1["status"] == "success"
        assert len(result1["record"]) > 0, "Should have verse results"
        verse_text = result1["record"][0]["bible_text"]
        print(f"   First call: {time1:.3f}s")
        print(f"   Verse: {verse_text[:50]}...")
        
        # 第二次查詢相同經文 - 應該從快取取得
        start2 = time.time()
        result2 = await client.get_verse("約", 3, "16", version="unv")
        time2 = time.time() - start2
        
        assert result2["status"] == "success"
        assert len(result2["record"]) > 0
        assert result2["record"][0]["bible_text"] == verse_text
        print(f"   Second call: {time2:.3f}s")
        if time2 > 0:
            print(f"   Speedup: {time1/time2:.1f}x faster")
        else:
            print(f"   Speedup: Cache is extremely fast (< 0.001s)")
        
        # 檢查快取
        assert client.cache.stats['hits'] >= 1
    
    print("✅ Verse caching works")


@pytest.mark.asyncio
async def test_cache_integration_search():
    """
    Test 3: 搜尋快取測試
    測試 search_bible 的快取功能
    """
    print("\n" + "="*70)
    print("Test 3: Search Caching")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 搜尋「愛」
        start1 = time.time()
        result1 = await client.search_bible("愛", limit=5)
        time1 = time.time() - start1
        
        assert result1["status"] == "success"
        count = result1["record_count"]
        print(f"   First call: {count} results, took {time1:.3f}s")
        
        # 再次搜尋相同關鍵字
        start2 = time.time()
        result2 = await client.search_bible("愛", limit=5)
        time2 = time.time() - start2
        
        assert result2["record_count"] == count
        print(f"   Second call: {count} results, took {time2:.3f}s")
        print(f"   Speedup: {time1/time2:.1f}x faster")
        
        assert client.cache.stats['hits'] >= 1
    
    print("✅ Search caching works")


@pytest.mark.asyncio
async def test_cache_integration_strongs():
    """
    Test 4: Strong's 字典快取測試
    測試 get_strongs_dictionary 的永久快取
    """
    print("\n" + "="*70)
    print("Test 4: Strong's Dictionary Caching (Permanent)")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 查詢 Strong's #25 (agapao - 愛)
        result1 = await client.get_strongs_dictionary(25, "nt")
        assert result1["status"] == "success"
        orig_word = result1["record"][0]["orig"]
        print(f"   Original word: {orig_word}")
        
        # 再次查詢
        result2 = await client.get_strongs_dictionary(25, "nt")
        assert result2["record"][0]["orig"] == orig_word
        
        # 檢查快取資訊
        info = client.cache.get_info()
        print(f"   Cache info: {info['namespaces']}")
        assert "strongs" in info["namespaces"]
        
        # Strong's 是永久快取
        entries = client.cache.get_entries(namespace="strongs")
        for entry in entries:
            assert entry["expiry_time"] == "never", "Strong's should be permanent"
            print(f"   Entry: {entry['key'][:30]}... (expiry={entry['expiry_time']})")
    
    print("✅ Strong's dictionary permanent caching works")


@pytest.mark.asyncio
async def test_cache_disabled():
    """
    Test 5: 停用快取測試
    測試當 use_cache=False 時不使用快取
    """
    print("\n" + "="*70)
    print("Test 5: Cache Disabled")
    print("="*70)
    
    async with FHLAPIEndpoints(use_cache=False) as client:
        # 應該沒有快取物件
        assert client.cache is None
        
        # 呼叫 API 應該正常運作
        result = await client.get_bible_versions()
        assert result["status"] == "success"
        print(f"   API call works without cache: {result['record_count']} versions")
    
    print("✅ Cache can be disabled")


@pytest.mark.asyncio
async def test_cache_cleanup_integration():
    """
    Test 6: 快取清理整合測試
    測試在實際使用中的快取清理
    """
    print("\n" + "="*70)
    print("Test 6: Cache Cleanup Integration")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 建立一些快取
        await client.get_bible_versions()  # permanent
        await client.get_verse("John", 3, "16")  # 7 days
        await client.search_bible("愛", limit=5)  # 1 day
        
        # 檢查快取資訊
        info = client.cache.get_info()
        total_before = info["total_files"]
        print(f"   Total cached items: {total_before}")
        print(f"   Namespaces: {info['namespaces']}")
        
        # 清理特定命名空間
        cleared = client.cache.clear(namespace="search")
        print(f"   Cleared 'search' namespace: {cleared} items")
        
        # 檢查剩餘
        info_after = client.cache.get_info()
        assert "search" not in info_after["namespaces"]
        print(f"   Remaining namespaces: {info_after['namespaces']}")
    
    print("✅ Cache cleanup integration works")


@pytest.mark.asyncio
async def test_cache_info_integration():
    """
    Test 7: 快取資訊整合測試
    測試取得完整的快取統計資訊
    """
    print("\n" + "="*70)
    print("Test 7: Cache Info Integration")
    print("="*70)
    
    reset_cache()
    
    async with FHLAPIEndpoints(use_cache=True, cache_dir=".cache/test") as client:
        # 建立多種類型的快取
        await client.get_bible_versions()
        await client.get_verse("John", 3, "16")
        await client.get_verse("John", 3, "17")
        await client.search_bible("神", limit=5)
        await client.get_strongs_dictionary(2316, "nt")
        
        # 重複呼叫以產生 cache hits
        await client.get_bible_versions()
        await client.get_verse("John", 3, "16")
        
        # 取得資訊
        info = client.cache.get_info()
        
        print(f"\n   Cache Statistics:")
        print(f"   ─────────────────")
        print(f"   Total files: {info['total_files']}")
        print(f"   Total size: {info['total_size_mb']} MB")
        print(f"   Expired: {info['expired_count']}")
        print(f"\n   Namespaces:")
        for ns, count in info['namespaces'].items():
            print(f"     • {ns}: {count} items")
        print(f"\n   Performance:")
        print(f"     • Hits: {info['stats']['hits']}")
        print(f"     • Misses: {info['stats']['misses']}")
        print(f"     • Hit rate: {info['stats']['hit_rate_percent']}%")
        print(f"     • Writes: {info['stats']['writes']}")
        
        assert info['stats']['hits'] >= 2, "Should have cache hits"
        assert info['stats']['hit_rate_percent'] > 0, "Should have positive hit rate"
    
    print("\n✅ Cache info integration works")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        """執行所有測試"""
        print("\n" + "="*70)
        print("FHL Bible MCP Server - Cache Integration Tests")
        print("="*70)
        
        tests = [
            ("Bible Versions Caching", test_cache_integration_versions),
            ("Verse Caching", test_cache_integration_verses),
            ("Search Caching", test_cache_integration_search),
            ("Strong's Permanent Cache", test_cache_integration_strongs),
            ("Cache Disabled", test_cache_disabled),
            ("Cache Cleanup", test_cache_cleanup_integration),
            ("Cache Info", test_cache_info_integration),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                await test_func()
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
        
        # 清理測試快取
        import shutil
        test_cache_dir = Path(".cache/test")
        if test_cache_dir.exists():
            shutil.rmtree(test_cache_dir)
        
        # 顯示總結
        print("\n" + "="*70)
        print("Test Summary")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
        print("="*70)
        
        if failed == 0:
            print("\n🎉 All cache integration tests passed!")
        else:
            print(f"\n⚠️  {failed} test(s) failed")
    
    # 執行測試
    asyncio.run(run_all_tests())
