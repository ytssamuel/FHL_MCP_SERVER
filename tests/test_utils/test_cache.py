"""
Test Cache System

Tests for the cache system including FileCache, strategies, and cleanup.
"""

import pytest
import time
import json
from pathlib import Path
from fhl_bible_mcp.utils.cache import (
    FileCache,
    CacheStrategy,
    CacheEntry,
    get_cache,
    reset_cache
)


@pytest.fixture
def temp_cache_dir(tmp_path):
    """建立臨時快取目錄"""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def cache(temp_cache_dir):
    """建立測試用的快取實例"""
    reset_cache()  # 重置全域快取
    return FileCache(cache_dir=str(temp_cache_dir))


def test_cache_strategy_permanent():
    """
    Test 1: 永久快取策略
    測試永久快取永不過期
    """
    print("\n" + "="*70)
    print("Test 1: Permanent Cache Strategy")
    print("="*70)
    
    strategy = CacheStrategy(ttl_seconds=None)
    
    # 即使時間很久遠也不會過期
    old_time = time.time() - 365 * 24 * 3600  # 一年前
    assert not strategy.is_expired(old_time), "Permanent cache should never expire"
    
    # 過期時間應該是 None
    assert strategy.get_expiry_time(time.time()) is None
    
    print("✅ Permanent cache never expires")


def test_cache_strategy_ttl():
    """
    Test 2: TTL 快取策略
    測試帶有過期時間的快取
    """
    print("\n" + "="*70)
    print("Test 2: TTL Cache Strategy")
    print("="*70)
    
    # 建立 10 秒 TTL 的策略
    strategy = CacheStrategy(ttl_seconds=10)
    
    # 新快取不應過期
    now = time.time()
    assert not strategy.is_expired(now), "Fresh cache should not expire"
    
    # 舊快取應該過期
    old_time = now - 20  # 20 秒前
    assert strategy.is_expired(old_time), "Old cache should expire"
    
    # 檢查過期時間
    expiry = strategy.get_expiry_time(now)
    assert expiry is not None
    
    print(f"✅ TTL cache expires after {strategy.ttl_seconds} seconds")
    print(f"   Expiry time: {expiry}")


def test_cache_entry():
    """
    Test 3: CacheEntry 類別
    測試快取項目的建立與序列化
    """
    print("\n" + "="*70)
    print("Test 3: Cache Entry")
    print("="*70)
    
    strategy = CacheStrategy(ttl_seconds=60)
    now = time.time()
    
    # 建立快取項目
    entry = CacheEntry(
        key="test:key1",
        data={"message": "Hello, World!"},
        cached_at=now,
        strategy=strategy
    )
    
    # 檢查有效性
    assert entry.is_valid(), "Fresh entry should be valid"
    
    # 轉換為字典
    entry_dict = entry.to_dict()
    assert entry_dict["key"] == "test:key1"
    assert entry_dict["data"]["message"] == "Hello, World!"
    assert entry_dict["ttl_seconds"] == 60
    
    # 從字典重建
    restored = CacheEntry.from_dict(entry_dict)
    assert restored.key == entry.key
    assert restored.data == entry.data
    
    print("✅ Cache entry creation and serialization works")
    print(f"   Key: {entry.key}")
    print(f"   Valid: {entry.is_valid()}")


def test_file_cache_basic(cache):
    """
    Test 4: 基本快取操作
    測試 get, set, delete
    """
    print("\n" + "="*70)
    print("Test 4: Basic Cache Operations")
    print("="*70)
    
    # Set cache
    success = cache.set("test", "key1", {"value": 123}, strategy_name="permanent")
    assert success, "Cache set should succeed"
    
    # Get cache
    data = cache.get("test", "key1")
    assert data is not None, "Cache should exist"
    assert data["value"] == 123, "Cache data should match"
    
    # 檢查統計
    assert cache.stats["hits"] == 1
    assert cache.stats["writes"] == 1
    
    # Delete cache
    deleted = cache.delete("test", "key1")
    assert deleted, "Cache delete should succeed"
    
    # Get after delete
    data = cache.get("test", "key1")
    assert data is None, "Cache should not exist after delete"
    
    print("✅ Basic cache operations work")
    print(f"   Stats: {cache.stats}")


def test_file_cache_expiry(cache):
    """
    Test 5: 快取過期
    測試 TTL 過期機制
    """
    print("\n" + "="*70)
    print("Test 5: Cache Expiry")
    print("="*70)
    
    # 建立一個 1 秒 TTL 的快取
    # 先手動建立快取項目（模擬已過期的快取）
    cache_key = cache._get_cache_key("test", "expiring_key")
    cache_file = cache._get_cache_file(cache_key)
    
    old_time = time.time() - 10  # 10 秒前
    entry = CacheEntry(
        key=cache_key,
        data={"value": "old"},
        cached_at=old_time,
        strategy=CacheStrategy(ttl_seconds=1)
    )
    
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(entry.to_dict(), f)
    
    # 嘗試讀取（應該過期）
    data = cache.get("test", "expiring_key", strategy_name="search")
    assert data is None, "Expired cache should return None"
    
    # 檔案應該被刪除
    assert not cache_file.exists(), "Expired cache file should be deleted"
    
    print("✅ Cache expiry works correctly")


def test_file_cache_strategies(cache):
    """
    Test 6: 預設快取策略
    測試不同類型的快取策略
    """
    print("\n" + "="*70)
    print("Test 6: Cache Strategies")
    print("="*70)
    
    # 測試各種策略
    strategies_to_test = [
        ("verses", "經文快取"),
        ("search", "搜尋快取"),
        ("strongs", "字典快取"),
        ("permanent", "永久快取"),
    ]
    
    for strategy_name, description in strategies_to_test:
        cache.set("test", f"key_{strategy_name}", {"test": True}, strategy_name=strategy_name)
        data = cache.get("test", f"key_{strategy_name}", strategy_name=strategy_name)
        assert data is not None, f"{description} should work"
        print(f"   ✓ {description}: {strategy_name}")
    
    print("✅ All cache strategies work")


def test_cache_clear(cache):
    """
    Test 7: 清除快取
    測試清除特定命名空間或全部快取
    """
    print("\n" + "="*70)
    print("Test 7: Cache Clear")
    print("="*70)
    
    # 建立多個命名空間的快取
    cache.set("verses", "john3:16", {"text": "..."}, "verses")
    cache.set("search", "love", {"results": []}, "search")
    cache.set("strongs", "25", {"definition": "..."}, "strongs")
    
    # 清除特定命名空間
    cleared = cache.clear(namespace="search")
    assert cleared == 1, "Should clear 1 item"
    
    # 檢查其他命名空間還在
    assert cache.get("verses", "john3:16") is not None
    assert cache.get("strongs", "25") is not None
    assert cache.get("search", "love") is None
    
    # 清除全部
    cleared = cache.clear()
    assert cleared >= 2, "Should clear at least 2 items"
    
    print(f"✅ Cache clear works")
    print(f"   Cleared items: {cleared}")


def test_cleanup_expired(cache):
    """
    Test 8: 清理過期快取
    測試自動清理過期項目
    """
    print("\n" + "="*70)
    print("Test 8: Cleanup Expired Cache")
    print("="*70)
    
    # 建立一些快取
    cache.set("test", "permanent", {"value": 1}, "permanent")
    
    # 手動建立過期的快取
    cache_key = cache._get_cache_key("test", "expired")
    cache_file = cache._get_cache_file(cache_key)
    
    old_entry = CacheEntry(
        key=cache_key,
        data={"value": "expired"},
        cached_at=time.time() - 100,
        strategy=CacheStrategy(ttl_seconds=1)
    )
    
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(old_entry.to_dict(), f)
    
    # 執行清理
    cleaned = cache.cleanup_expired()
    assert cleaned >= 1, "Should clean at least 1 expired item"
    
    # 永久快取應該還在
    assert cache.get("test", "permanent") is not None
    
    print(f"✅ Cleanup expired cache works")
    print(f"   Cleaned items: {cleaned}")


def test_cache_info(cache):
    """
    Test 9: 快取資訊
    測試取得快取統計資訊
    """
    print("\n" + "="*70)
    print("Test 9: Cache Info")
    print("="*70)
    
    # 建立一些快取
    cache.set("verses", "key1", {"data": "test1"}, "verses")
    cache.set("verses", "key2", {"data": "test2"}, "verses")
    cache.set("search", "key3", {"data": "test3"}, "search")
    
    # 取得資訊
    info = cache.get_info()
    
    assert info["total_files"] >= 3
    assert "verses" in info["namespaces"]
    assert "search" in info["namespaces"]
    assert info["namespaces"]["verses"] == 2
    assert info["namespaces"]["search"] == 1
    
    print("✅ Cache info works")
    print(f"   Total files: {info['total_files']}")
    print(f"   Total size: {info['total_size_mb']} MB")
    print(f"   Namespaces: {info['namespaces']}")
    print(f"   Hit rate: {info['stats']['hit_rate_percent']}%")


def test_cache_entries(cache):
    """
    Test 10: 快取項目列表
    測試列出快取項目
    """
    print("\n" + "="*70)
    print("Test 10: Cache Entries List")
    print("="*70)
    
    # 建立快取
    cache.set("test", "key1", {"value": 1}, "permanent")
    cache.set("test", "key2", {"value": 2}, "verses")
    
    # 取得所有項目
    entries = cache.get_entries()
    assert len(entries) >= 2
    
    # 取得特定命名空間
    test_entries = cache.get_entries(namespace="test")
    assert len(test_entries) >= 2
    
    # 檢查項目資訊
    for entry in test_entries:
        assert "key" in entry
        assert "cached_at" in entry
        assert "is_valid" in entry
        assert "expiry_time" in entry
        print(f"   • {entry['key']}: valid={entry['is_valid']}, expiry={entry['expiry_time']}")
    
    print(f"✅ Cache entries list works")


def test_global_cache():
    """
    Test 11: 全域快取實例
    測試全域快取取得函數
    """
    print("\n" + "="*70)
    print("Test 11: Global Cache Instance")
    print("="*70)
    
    reset_cache()
    
    cache1 = get_cache()
    cache2 = get_cache()
    
    assert cache1 is cache2, "Should return same instance"
    
    print("✅ Global cache instance works")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        """執行所有測試"""
        print("\n" + "="*70)
        print("FHL Bible MCP Server - Cache System Tests")
        print("="*70)
        
        # 建立臨時目錄
        import tempfile
        temp_dir = Path(tempfile.mkdtemp())
        cache_dir = temp_dir / "test_cache"
        cache_dir.mkdir()
        
        cache = FileCache(cache_dir=str(cache_dir))
        
        tests = [
            ("Cache Strategy - Permanent", test_cache_strategy_permanent),
            ("Cache Strategy - TTL", test_cache_strategy_ttl),
            ("Cache Entry", test_cache_entry),
            ("Basic Operations", lambda: test_file_cache_basic(cache)),
            ("Cache Expiry", lambda: test_file_cache_expiry(cache)),
            ("Cache Strategies", lambda: test_file_cache_strategies(cache)),
            ("Cache Clear", lambda: test_cache_clear(cache)),
            ("Cleanup Expired", lambda: test_cleanup_expired(cache)),
            ("Cache Info", lambda: test_cache_info(cache)),
            ("Cache Entries", lambda: test_cache_entries(cache)),
            ("Global Cache", test_global_cache),
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
                failed += 1
        
        # 清理
        import shutil
        shutil.rmtree(temp_dir)
        
        # 顯示總結
        print("\n" + "="*70)
        print("Test Summary")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
        print("="*70)
        
        if failed == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {failed} test(s) failed")
    
    # 執行測試
    asyncio.run(run_all_tests())
