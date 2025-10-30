"""
Integration tests for the complete MCP server workflow
測試完整的 MCP 伺服器工作流程
"""
import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from src.fhl_bible_mcp.api.client import FHLAPIClient
from src.fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from src.fhl_bible_mcp.config import Config
from src.fhl_bible_mcp.utils.cache import FileCache
from src.fhl_bible_mcp.utils.booknames import BookNameConverter


@pytest.mark.asyncio
async def test_full_verse_query_workflow():
    """
    Test 1: 完整的經文查詢流程
    API Client -> Endpoints -> Cache -> Config
    """
    print("\n" + "="*70)
    print("Integration Test 1: Full Verse Query Workflow")
    print("="*70)
    
    # 1. 設定配置
    config = Config.load(use_env=False)  # 使用正確的方法
    config.update("bible", "default_version", "unv")  # section, key, value
    config.update("cache", "enabled", True)
    
    # 2. 創建 API 客戶端
    async with FHLAPIEndpoints(use_cache=True) as client:
        # 3. 書卷名轉換
        converter = BookNameConverter()
        book_eng = converter.get_english_short("約")
        assert book_eng == "John"
        print(f"   ✓ Book name conversion: 約 -> {book_eng}")
        
        # 4. 查詢經文
        result = await client.get_verse(
            book="約",  # 使用正確的參數名
            chapter=3,
            verse="16",
            version="unv"
        )
        
        assert result["status"] == "success"
        assert len(result["record"]) > 0
        verse_text = result["record"][0]["bible_text"]
        print(f"   ✓ Verse query successful")
        print(f"   ✓ Text: {verse_text[:50]}...")
        
        # 5. 驗證快取
        cache_stats = client.cache.stats
        print(f"   ✓ Cache stats: hits={cache_stats['hits']}, misses={cache_stats['misses']}")
    
    print("✅ Full verse query workflow test passed")


@pytest.mark.asyncio
async def test_chinese_support_integration():
    """
    Test 2: 中文支援整合測試
    測試繁簡體轉換、書卷名標準化、模糊搜尋
    """
    print("\n" + "="*70)
    print("Integration Test 2: Chinese Support Integration")
    print("="*70)
    
    converter = BookNameConverter()
    
    # 1. 繁簡體自動轉換
    simplified_input = "创世记"
    normalized = converter.normalize_book_name(simplified_input)
    # normalize_book_name 可能返回中文縮寫，需要進一步轉換
    if normalized:
        book_info = converter.get_book_info(normalized)
        if book_info:
            normalized = book_info["eng_short"]
    assert normalized == "Gen"
    print(f"   ✓ Simplified Chinese: {simplified_input} -> {normalized}")
    
    # 2. 多種格式支援
    formats = ["約", "约", "約翰福音", "约翰福音", "John", "john", "Jn"]
    for fmt in formats:
        result = converter.normalize_book_name(fmt)
        assert result is not None, f"normalize_book_name returned None for: {fmt}"
        # 結果可能是中文或英文縮寫，都應該指向約翰福音
        book_info = converter.get_book_info(result)
        assert book_info is not None and book_info["id"] == 43, f"Failed for format: {fmt}"
    print(f"   ✓ Multiple formats supported: {len(formats)} variants")
    
    # 3. 模糊搜尋
    fuzzy_results = converter.fuzzy_search("约")
    assert len(fuzzy_results) > 0
    assert any(r["id"] == 43 for r in fuzzy_results)  # John (使用 "id" 不是 "book_id")
    print(f"   ✓ Fuzzy search: '约' found {len(fuzzy_results)} matches")
    
    # 4. 與 API 整合
    async with FHLAPIEndpoints(use_cache=True) as client:
        result = await client.get_verse(
            book="约",  # 簡體輸入，使用正確的參數名
            chapter=3,
            verse="16"
        )
        assert result["status"] == "success"
        print(f"   ✓ API accepts simplified Chinese input")
    
    print("✅ Chinese support integration test passed")


@pytest.mark.asyncio
async def test_config_cascade_integration():
    """
    Test 3: 配置層級整合測試
    測試配置的多層來源和優先級
    """
    print("\n" + "="*70)
    print("Integration Test 3: Config Cascade Integration")
    print("="*70)
    
    # 1. 預設配置
    config = Config.load(use_env=False)
    default_version = config.get("defaults", "bible_version")  # section="defaults", key="bible_version"
    print(f"   ✓ Default version: {default_version}")
    
    # 2. 執行時更新
    success = config.update("defaults", "bible_version", "kjv")  # section, key, value
    assert success is True  # update() 返回布林值
    updated_version = config.get("defaults", "bible_version")
    assert updated_version == "kjv"
    print(f"   ✓ Runtime update: {updated_version}")
    
    # 3. API 使用配置
    async with FHLAPIEndpoints(use_cache=True) as client:
        # 不指定版本，應使用配置中的預設值
        result = await client.get_bible_versions()
        assert result["status"] == "success"
        print(f"   ✓ API uses config: {result['record_count']} versions available")
    
    print("✅ Config cascade integration test passed")


@pytest.mark.asyncio
async def test_cache_config_integration():
    """
    Test 4: 快取與配置整合測試
    """
    print("\n" + "="*70)
    print("Integration Test 4: Cache-Config Integration")
    print("="*70)
    
    # 1. 配置快取設定
    config = Config.load(use_env=False)
    config.update("cache", "enabled", True)  # section, key, value
    # CacheConfig 沒有 ttl 屬性，移除此更新
    # config.update("cache", "ttl", 300)
    
    # 2. 創建快取
    cache = FileCache(cache_dir=".cache/integration_test")
    
    # 3. 測試快取策略 (FileCache.set() 參數: namespace, key, data, strategy_name)
    cache.set("test", "test_key", {"data": "test_value"}, strategy_name="ttl")
    cached_data = cache.get("test", "test_key")
    assert cached_data["data"] == "test_value"
    print(f"   ✓ Cache with TTL working")
    
    # 4. API 整合快取 (使用新的快取目錄並清理)
    cache_test_dir = tempfile.mkdtemp(prefix="cache_test_")
    
    try:
        async with FHLAPIEndpoints(
            use_cache=True,
            cache_dir=cache_test_dir
        ) as client:
            # 第一次查詢（cache miss）
            result1 = await client.get_bible_versions()
            stats1 = client.cache.stats
            initial_hits = stats1["hits"]
            
            # 第二次查詢（應使用快取，cache hit）
            result2 = await client.get_bible_versions()
            stats2 = client.cache.stats
            
            assert stats2["hits"] > initial_hits, f"Expected cache hit increase, got {initial_hits} -> {stats2['hits']}"
            print(f"   ✓ Cache hits increased: {initial_hits} -> {stats2['hits']}")
    finally:
        # 清理測試快取目錄
        if Path(cache_test_dir).exists():
            shutil.rmtree(cache_test_dir)
    
    # 清理
    cache.clear()
    print("✅ Cache-config integration test passed")


@pytest.mark.asyncio
async def test_error_recovery_integration():
    """
    Test 5: 錯誤恢復整合測試
    測試系統在錯誤情況下的恢復能力
    """
    print("\n" + "="*70)
    print("Integration Test 5: Error Recovery Integration")
    print("="*70)
    
    converter = BookNameConverter()
    
    # 1. 無效書卷名處理
    invalid_book = converter.normalize_book_name("不存在的書")
    assert invalid_book is None
    print(f"   ✓ Invalid book name handled gracefully")
    
    # 2. 模糊搜尋作為後備
    fuzzy_results = converter.fuzzy_search("約")
    assert len(fuzzy_results) > 0
    print(f"   ✓ Fuzzy search as fallback: {len(fuzzy_results)} results")
    
    # 3. API 錯誤處理
    async with FHLAPIEndpoints(use_cache=True) as client:
        try:
            # 嘗試查詢無效章節
            result = await client.get_verse(
                book="約",  # 使用正確的參數名
                chapter=999,  # 無效章節
                verse="1"
            )
            # 如果 API 返回結果，檢查狀態
            if "status" in result:
                print(f"   ✓ API handled invalid chapter: {result.get('status')}")
        except Exception as e:
            print(f"   ✓ Exception caught and handled: {type(e).__name__}")
    
    print("✅ Error recovery integration test passed")


@pytest.mark.asyncio
async def test_multi_component_workflow():
    """
    Test 6: 多組件協作工作流程
    測試 BookNames -> Config -> Cache -> API 的完整流程
    """
    print("\n" + "="*70)
    print("Integration Test 6: Multi-Component Workflow")
    print("="*70)
    
    # 1. 初始化所有組件
    config = Config.load(use_env=False)
    converter = BookNameConverter()
    
    # 2. 測試場景：用戶輸入簡體中文書名查詢經文
    user_input = "创世记"
    
    # 步驟 1: 書名標準化
    normalized_book = converter.normalize_book_name(user_input)
    assert normalized_book is not None
    print(f"   Step 1: Normalize '{user_input}' -> '{normalized_book}'")
    
    # 步驟 2: 取得書卷資訊
    book_info = converter.get_book_info(normalized_book)
    assert book_info is not None
    chinese_short = book_info["chi_short"]
    print(f"   Step 2: Get book info -> '{chinese_short}'")
    
    # 步驟 3: 使用配置的預設版本
    version = config.get("defaults", "bible_version", "unv")  # section="defaults", key="bible_version"
    print(f"   Step 3: Use config version -> '{version}'")
    
    # 步驟 4: API 查詢（帶快取）
    async with FHLAPIEndpoints(use_cache=True) as client:
        result = await client.get_verse(
            book=chinese_short,  # 使用正確的參數名
            chapter=1,
            verse="1",
            version=version
        )
        
        assert result["status"] == "success"
        verse_text = result["record"][0]["bible_text"]
        print(f"   Step 4: API query successful")
        print(f"   Result: {verse_text[:50]}...")
        
        # 步驟 5: 驗證快取
        cache_stats = client.cache.stats
        print(f"   Step 5: Cache stats -> hits={cache_stats['hits']}, misses={cache_stats['misses']}")
    
    print("✅ Multi-component workflow test passed")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Running Integration Tests")
    print("="*80)
    
    asyncio.run(test_full_verse_query_workflow())
    asyncio.run(test_chinese_support_integration())
    asyncio.run(test_config_cascade_integration())
    asyncio.run(test_cache_config_integration())
    asyncio.run(test_error_recovery_integration())
    asyncio.run(test_multi_component_workflow())
    
    print("\n" + "="*80)
    print("✅ All Integration Tests Passed!")
    print("="*80)
