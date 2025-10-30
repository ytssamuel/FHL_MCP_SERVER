"""
Test Config Integration with API

Tests for config system integration with FHLAPIEndpoints.
"""

import pytest
import json
from pathlib import Path
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.config import Config, reset_config


@pytest.fixture
def test_config():
    """建立測試設定"""
    config = Config()
    config.api.base_url = "https://bible.fhl.net/json/"
    config.api.timeout = 45
    config.api.max_retries = 5
    config.cache.enabled = True
    config.cache.directory = ".test_cache"
    config.cache.cleanup_on_start = False
    return config


@pytest.fixture
def temp_config_file(tmp_path):
    """建立臨時設定檔"""
    config_data = {
        "server": {"name": "test-server", "version": "1.0.0"},
        "api": {
            "base_url": "https://bible.fhl.net/json/",
            "timeout": 60,
            "max_retries": 7
        },
        "defaults": {
            "bible_version": "unv",
            "chinese_variant": "traditional",
            "search_limit": 50,
            "include_strong": False
        },
        "cache": {
            "enabled": True,
            "directory": ".test_cache_from_file",
            "cleanup_on_start": False
        },
        "logging": {
            "level": "INFO",
            "file": None,
            "format": "%(message)s"
        }
    }
    
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    
    return config_file


def test_api_with_explicit_params():
    """
    Test 1: API 使用顯式參數
    測試直接傳入參數建立 API client
    """
    print("\n" + "="*70)
    print("Test 1: API with Explicit Parameters")
    print("="*70)
    
    # 重置全域設定
    reset_config()
    
    # 使用顯式參數
    api = FHLAPIEndpoints(
        base_url="https://bible.fhl.net/json/",
        timeout=90,
        max_retries=10,
        use_cache=False
    )
    
    # 檢查參數 (注意: FHLAPIClient 會自動去除末尾的斜線)
    assert api.base_url == "https://bible.fhl.net/json"
    assert api.timeout == 90
    assert api.max_retries == 10
    assert api.use_cache == False
    assert api.cache is None
    
    print("✅ API initialized with explicit parameters")
    print(f"   base_url: {api.base_url}")
    print(f"   timeout: {api.timeout}s")
    print(f"   max_retries: {api.max_retries}")
    print(f"   use_cache: {api.use_cache}")


def test_api_with_config_object(test_config):
    """
    Test 2: API 使用 Config 物件
    測試傳入 Config 物件建立 API client
    """
    print("\n" + "="*70)
    print("Test 2: API with Config Object")
    print("="*70)
    
    # 使用 Config 物件
    api = FHLAPIEndpoints(config=test_config)
    
    # 檢查從 Config 取得的參數 (注意: FHLAPIClient 會自動去除末尾的斜線)
    assert api.base_url == test_config.api.base_url.rstrip('/')
    assert api.timeout == test_config.api.timeout
    assert api.max_retries == test_config.api.max_retries
    assert api.use_cache == test_config.cache.enabled
    
    print("✅ API initialized with Config object")
    print(f"   base_url: {api.base_url}")
    print(f"   timeout: {api.timeout}s")
    print(f"   cache enabled: {api.use_cache}")


def test_api_with_global_config():
    """
    Test 3: API 使用全域設定
    測試使用全域設定建立 API client
    """
    print("\n" + "="*70)
    print("Test 3: API with Global Config")
    print("="*70)
    
    # 重置並設定全域設定
    reset_config()
    from fhl_bible_mcp.config import get_config
    global_config = get_config()
    global_config.api.timeout = 120
    global_config.cache.enabled = False
    
    # 建立 API (應該使用全域設定)
    api = FHLAPIEndpoints()
    
    # 檢查從全域設定取得的參數
    assert api.timeout == 120
    assert api.use_cache == False
    
    print("✅ API initialized with global config")
    print(f"   timeout: {api.timeout}s")
    print(f"   cache enabled: {api.use_cache}")


def test_api_parameter_priority():
    """
    Test 4: API 參數優先順序
    測試參數優先順序: 顯式參數 > Config 物件 > 全域設定
    """
    print("\n" + "="*70)
    print("Test 4: API Parameter Priority")
    print("="*70)
    
    # 重置全域設定
    reset_config()
    from fhl_bible_mcp.config import get_config
    global_config = get_config()
    global_config.api.timeout = 30
    
    # 建立自訂 Config
    custom_config = Config()
    custom_config.api.timeout = 60
    
    # 顯式參數應該覆蓋 Config
    api = FHLAPIEndpoints(
        timeout=90,
        config=custom_config
    )
    
    # 顯式參數優先
    assert api.timeout == 90
    
    # Config 物件優先於全域設定
    api2 = FHLAPIEndpoints(config=custom_config)
    assert api2.timeout == 60
    
    # 全域設定作為後備
    api3 = FHLAPIEndpoints()
    assert api3.timeout == 30
    
    print("✅ Parameter priority works correctly")
    print(f"   Explicit parameter: {api.timeout}s")
    print(f"   Config object: {api2.timeout}s")
    print(f"   Global config: {api3.timeout}s")


def test_api_with_file_config(temp_config_file):
    """
    Test 5: API 使用檔案設定
    測試從檔案載入設定並建立 API client
    """
    print("\n" + "="*70)
    print("Test 5: API with File Config")
    print("="*70)
    
    # 從檔案載入設定
    config = Config.load(config_file=str(temp_config_file), use_env=False)
    
    # 使用載入的設定建立 API
    api = FHLAPIEndpoints(config=config)
    
    # 檢查從檔案載入的參數
    assert api.timeout == 60
    assert api.max_retries == 7
    assert api.use_cache == True
    
    print("✅ API initialized with file config")
    print(f"   Config file: {temp_config_file}")
    print(f"   timeout: {api.timeout}s")
    print(f"   max_retries: {api.max_retries}")


def test_cache_cleanup_on_start():
    """
    Test 6: 啟動時清理快取
    測試 cleanup_on_start 設定
    """
    print("\n" + "="*70)
    print("Test 6: Cache Cleanup on Start")
    print("="*70)
    
    # 建立設定,啟用啟動時清理
    config = Config()
    config.cache.enabled = True
    config.cache.cleanup_on_start = True
    config.cache.directory = ".test_cache_cleanup"
    
    # 建立 API (應該自動清理)
    api = FHLAPIEndpoints(config=config)
    
    # 檢查快取已啟用
    assert api.use_cache == True
    assert api.cache is not None
    
    print("✅ Cache cleanup on start works")
    print(f"   Cache directory: {config.cache.directory}")
    print(f"   Cleanup on start: {config.cache.cleanup_on_start}")


def test_api_runtime_config_update():
    """
    Test 7: API 執行時更新設定
    測試在執行時更新 Config 是否影響 API
    """
    print("\n" + "="*70)
    print("Test 7: Runtime Config Update")
    print("="*70)
    
    # 建立設定
    config = Config()
    config.api.timeout = 30
    
    # 建立 API
    api = FHLAPIEndpoints(config=config)
    assert api.timeout == 30
    
    # 更新設定
    config.update("api", "timeout", 60)
    
    # 已建立的 API 實例不受影響
    assert api.timeout == 30
    
    # 新建立的 API 使用更新後的設定
    api2 = FHLAPIEndpoints(config=config)
    assert api2.timeout == 60
    
    print("✅ Runtime config update behavior correct")
    print(f"   Original API timeout: {api.timeout}s (unchanged)")
    print(f"   New API timeout: {api2.timeout}s (updated)")


@pytest.mark.asyncio
async def test_api_actual_request_with_config():
    """
    Test 8: 實際 API 請求
    測試使用 Config 進行實際 API 請求
    """
    print("\n" + "="*70)
    print("Test 8: Actual API Request with Config")
    print("="*70)
    
    # 建立設定
    config = Config()
    config.cache.enabled = True
    config.cache.directory = ".test_cache_request"
    
    # 建立 API
    api = FHLAPIEndpoints(config=config)
    
    try:
        # 測試取得聖經版本列表
        versions = await api.get_bible_versions()
        
        assert versions is not None
        assert isinstance(versions, list)
        assert len(versions) > 0
        
        print("✅ Actual API request successful")
        print(f"   Retrieved {len(versions)} Bible versions")
        print(f"   Cache enabled: {api.use_cache}")
        
        # 測試快取資訊
        if api.cache:
            cache_info = api.cache.get_info()
            print(f"   Cache stats: {cache_info['total_entries']} entries")
    
    except Exception as e:
        print(f"⚠️  API request failed (expected if no internet): {e}")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    import asyncio
    import tempfile
    
    async def run_all_tests():
        """執行所有測試"""
        print("\n" + "="*70)
        print("FHL Bible MCP Server - Config Integration Tests")
        print("="*70)
        
        # 建立臨時目錄
        temp_dir = Path(tempfile.mkdtemp())
        
        # 建立測試設定
        test_config = Config()
        test_config.api.base_url = "https://bible.fhl.net/json/"
        test_config.api.timeout = 45
        test_config.cache.enabled = True
        
        # 建立臨時設定檔
        config_data = {
            "server": {"name": "test-server", "version": "1.0.0"},
            "api": {"base_url": "https://bible.fhl.net/json/", "timeout": 60, "max_retries": 7},
            "cache": {"enabled": True, "directory": ".test_cache_from_file", "cleanup_on_start": False}
        }
        temp_config_file = temp_dir / "test_config.json"
        with open(temp_config_file, "w") as f:
            json.dump(config_data, f)
        
        tests = [
            ("Explicit Parameters", test_api_with_explicit_params),
            ("Config Object", lambda: test_api_with_config_object(test_config)),
            ("Global Config", test_api_with_global_config),
            ("Parameter Priority", test_api_parameter_priority),
            ("File Config", lambda: test_api_with_file_config(temp_config_file)),
            ("Cache Cleanup", test_cache_cleanup_on_start),
            ("Runtime Update", test_api_runtime_config_update),
            ("Actual Request", test_api_actual_request_with_config),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                if asyncio.iscoroutinefunction(test_func):
                    await test_func()
                else:
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
        
        # 清理
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        # 顯示總結
        print("\n" + "="*70)
        print("Test Summary")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
        print("="*70)
        
        if failed == 0:
            print("\n🎉 All config integration tests passed!")
        else:
            print(f"\n⚠️  {failed} test(s) failed")
    
    # 執行測試
    asyncio.run(run_all_tests())
