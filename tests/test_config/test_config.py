"""
Test Configuration Management

Tests for the config system including file loading, environment variables, and runtime updates.
"""

import pytest
import json
import os
from pathlib import Path
from fhl_bible_mcp.config import (
    Config,
    ServerConfig,
    APIConfig,
    DefaultsConfig,
    CacheConfig,
    LoggingConfig,
    get_config,
    reset_config
)


@pytest.fixture
def temp_config_file(tmp_path):
    """建立臨時設定檔"""
    config_data = {
        "server": {
            "name": "test-server",
            "version": "2.0.0"
        },
        "api": {
            "base_url": "https://test.api.com/",
            "timeout": 60,
            "max_retries": 5
        },
        "defaults": {
            "bible_version": "kjv",
            "chinese_variant": "simplified",
            "search_limit": 100,
            "include_strong": True
        },
        "cache": {
            "enabled": False,
            "directory": ".test_cache",
            "cleanup_on_start": True
        },
        "logging": {
            "level": "DEBUG",
            "file": "test.log",
            "format": "%(levelname)s - %(message)s"
        }
    }
    
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    
    return config_file


def test_default_config():
    """
    Test 1: 預設設定
    測試創建預設設定物件
    """
    print("\n" + "="*70)
    print("Test 1: Default Configuration")
    print("="*70)
    
    config = Config()
    
    # 檢查預設值
    assert config.server.name == "fhl-bible-server"
    assert config.server.version == "1.0.0"
    assert config.api.base_url == "https://bible.fhl.net/json/"
    assert config.api.timeout == 30
    assert config.api.max_retries == 3
    assert config.defaults.bible_version == "unv"
    assert config.defaults.chinese_variant == "traditional"
    assert config.defaults.search_limit == 50
    assert config.defaults.include_strong == False
    assert config.cache.enabled == True
    assert config.cache.directory == ".cache"
    assert config.logging.level == "INFO"
    
    print("✅ Default configuration values are correct")
    print(f"   Server: {config.server.name} v{config.server.version}")
    print(f"   API: {config.api.base_url}")
    print(f"   Cache: {config.cache.enabled}")


def test_load_from_file(temp_config_file):
    """
    Test 2: 從檔案載入設定
    測試從 JSON 檔案載入設定
    """
    print("\n" + "="*70)
    print("Test 2: Load Configuration from File")
    print("="*70)
    
    config = Config.load(config_file=str(temp_config_file), use_env=False)
    
    # 檢查載入的值
    assert config.server.name == "test-server"
    assert config.server.version == "2.0.0"
    assert config.api.base_url == "https://test.api.com/"
    assert config.api.timeout == 60
    assert config.api.max_retries == 5
    assert config.defaults.bible_version == "kjv"
    assert config.defaults.chinese_variant == "simplified"
    assert config.defaults.search_limit == 100
    assert config.defaults.include_strong == True
    assert config.cache.enabled == False
    assert config.cache.directory == ".test_cache"
    assert config.cache.cleanup_on_start == True
    assert config.logging.level == "DEBUG"
    assert config.logging.file == "test.log"
    
    print("✅ Configuration loaded from file")
    print(f"   Server: {config.server.name} v{config.server.version}")
    print(f"   API timeout: {config.api.timeout}s")
    print(f"   Cache enabled: {config.cache.enabled}")


def test_load_from_env(monkeypatch):
    """
    Test 3: 從環境變數載入設定
    測試從環境變數覆蓋設定
    """
    print("\n" + "="*70)
    print("Test 3: Load Configuration from Environment")
    print("="*70)
    
    # 設定環境變數
    env_vars = {
        "FHL_SERVER_NAME": "env-server",
        "FHL_API_TIMEOUT": "45",
        "FHL_API_MAX_RETRIES": "7",
        "FHL_DEFAULT_VERSION": "niv",
        "FHL_DEFAULT_CHINESE": "simplified",
        "FHL_DEFAULT_SEARCH_LIMIT": "200",
        "FHL_DEFAULT_INCLUDE_STRONG": "true",
        "FHL_CACHE_ENABLED": "false",
        "FHL_CACHE_DIR": "/tmp/cache",
        "FHL_LOG_LEVEL": "WARNING",
        "FHL_LOG_FILE": "app.log",
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    # 載入設定
    config = Config.load(use_env=True)
    
    # 檢查環境變數是否生效
    assert config.server.name == "env-server"
    assert config.api.timeout == 45
    assert config.api.max_retries == 7
    assert config.defaults.bible_version == "niv"
    assert config.defaults.chinese_variant == "simplified"
    assert config.defaults.search_limit == 200
    assert config.defaults.include_strong == True
    assert config.cache.enabled == False
    assert config.cache.directory == "/tmp/cache"
    assert config.logging.level == "WARNING"
    assert config.logging.file == "app.log"
    
    print("✅ Configuration loaded from environment variables")
    print(f"   Loaded {len(env_vars)} environment variables")
    print(f"   Server: {config.server.name}")
    print(f"   API timeout: {config.api.timeout}s")


def test_env_override_file(temp_config_file, monkeypatch):
    """
    Test 4: 環境變數覆蓋檔案設定
    測試環境變數優先於檔案設定
    """
    print("\n" + "="*70)
    print("Test 4: Environment Variables Override File")
    print("="*70)
    
    # 設定環境變數
    monkeypatch.setenv("FHL_SERVER_NAME", "override-server")
    monkeypatch.setenv("FHL_API_TIMEOUT", "99")
    
    # 先載入檔案,再套用環境變數
    config = Config.load(config_file=str(temp_config_file), use_env=True)
    
    # 環境變數應該覆蓋檔案設定
    assert config.server.name == "override-server"  # From env
    assert config.api.timeout == 99  # From env
    assert config.server.version == "2.0.0"  # From file
    assert config.api.max_retries == 5  # From file
    
    print("✅ Environment variables override file settings")
    print(f"   server.name: override-server (from env)")
    print(f"   api.timeout: 99 (from env)")
    print(f"   server.version: 2.0.0 (from file)")


def test_runtime_update():
    """
    Test 5: 執行時更新設定
    測試在執行時修改設定
    """
    print("\n" + "="*70)
    print("Test 5: Runtime Configuration Update")
    print("="*70)
    
    config = Config()
    
    # 更新設定
    success = config.update("api", "timeout", 120)
    assert success == True
    assert config.api.timeout == 120
    
    success = config.update("cache", "enabled", False)
    assert success == True
    assert config.cache.enabled == False
    
    success = config.update("defaults", "bible_version", "kjv")
    assert success == True
    assert config.defaults.bible_version == "kjv"
    
    # 測試無效的更新
    success = config.update("invalid_section", "key", "value")
    assert success == False
    
    success = config.update("api", "invalid_key", "value")
    assert success == False
    
    print("✅ Runtime configuration updates work")
    print(f"   Updated api.timeout: {config.api.timeout}")
    print(f"   Updated cache.enabled: {config.cache.enabled}")
    print(f"   Invalid updates rejected")


def test_get_value():
    """
    Test 6: 取得設定值
    測試 get() 方法
    """
    print("\n" + "="*70)
    print("Test 6: Get Configuration Value")
    print("="*70)
    
    config = Config()
    
    # 取得有效的值
    assert config.get("api", "timeout") == 30
    assert config.get("server", "name") == "fhl-bible-server"
    assert config.get("cache", "enabled") == True
    
    # 取得不存在的值(使用預設值)
    assert config.get("invalid", "key", default="default_value") == "default_value"
    assert config.get("api", "invalid_key", default=100) == 100
    
    print("✅ Get configuration value works")
    print(f"   api.timeout: {config.get('api', 'timeout')}")
    print(f"   invalid.key: {config.get('invalid', 'key', 'default')}")


def test_to_dict():
    """
    Test 7: 轉換為字典
    測試 to_dict() 方法
    """
    print("\n" + "="*70)
    print("Test 7: Convert Configuration to Dictionary")
    print("="*70)
    
    config = Config()
    config_dict = config.to_dict()
    
    # 檢查結構
    assert "server" in config_dict
    assert "api" in config_dict
    assert "defaults" in config_dict
    assert "cache" in config_dict
    assert "logging" in config_dict
    
    # 檢查內容
    assert config_dict["server"]["name"] == "fhl-bible-server"
    assert config_dict["api"]["timeout"] == 30
    assert config_dict["cache"]["enabled"] == True
    
    print("✅ Configuration to dictionary conversion works")
    print(f"   Keys: {list(config_dict.keys())}")


def test_save_and_load(tmp_path):
    """
    Test 8: 儲存與載入設定
    測試 save() 和 load() 方法
    """
    print("\n" + "="*70)
    print("Test 8: Save and Load Configuration")
    print("="*70)
    
    # 建立設定並修改
    config1 = Config()
    config1.update("server", "name", "saved-server")
    config1.update("api", "timeout", 99)
    
    # 儲存
    save_path = tmp_path / "saved_config.json"
    success = config1.save(str(save_path))
    assert success == True
    assert save_path.exists()
    
    # 載入
    config2 = Config.load(config_file=str(save_path), use_env=False)
    assert config2.server.name == "saved-server"
    assert config2.api.timeout == 99
    
    print("✅ Save and load configuration works")
    print(f"   Saved to: {save_path}")
    print(f"   Loaded server.name: {config2.server.name}")


def test_config_sources(temp_config_file, monkeypatch):
    """
    Test 9: 設定來源追蹤
    測試 _sources 追蹤設定值的來源
    """
    print("\n" + "="*70)
    print("Test 9: Configuration Sources Tracking")
    print("="*70)
    
    # 設定環境變數
    monkeypatch.setenv("FHL_SERVER_NAME", "env-name")
    
    # 從檔案和環境變數載入
    config = Config.load(config_file=str(temp_config_file), use_env=True)
    
    # 執行時更新
    config.update("cache", "enabled", True)
    
    # 取得來源
    sources = config.get_sources()
    
    # 檢查來源追蹤
    assert len(sources) > 0
    assert "server.name" in sources
    
    # 列出所有來源
    print("✅ Configuration sources tracking works")
    print(f"\n   Configuration sources ({len(sources)} settings):")
    for key, source in list(sources.items())[:10]:
        print(f"     • {key}: {source}")


def test_global_config():
    """
    Test 10: 全域設定實例
    測試 get_config() 全域設定函數
    """
    print("\n" + "="*70)
    print("Test 10: Global Configuration Instance")
    print("="*70)
    
    reset_config()
    
    config1 = get_config()
    config2 = get_config()
    
    # 應該是相同實例
    assert config1 is config2
    
    # 測試 reload
    config3 = get_config(reload=True)
    assert config3 is not None
    
    print("✅ Global configuration instance works")
    print(f"   Same instance: {config1 is config2}")


def test_type_validation():
    """
    Test 11: 型別驗證
    測試 update() 時的型別檢查
    """
    print("\n" + "="*70)
    print("Test 11: Type Validation")
    print("="*70)
    
    config = Config()
    
    # 正確的型別
    assert config.update("api", "timeout", 60, validate=True) == True
    assert config.api.timeout == 60
    
    # 錯誤的型別(應該失敗)
    assert config.update("api", "timeout", "invalid", validate=True) == False
    assert config.api.timeout == 60  # 應該保持原值
    
    # 關閉驗證(應該成功但可能有問題)
    assert config.update("api", "timeout", "120", validate=False) == True
    
    print("✅ Type validation works")
    print(f"   Correct type update: success")
    print(f"   Incorrect type update: rejected")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    import asyncio
    import tempfile
    
    async def run_all_tests():
        """執行所有測試"""
        print("\n" + "="*70)
        print("FHL Bible MCP Server - Configuration Management Tests")
        print("="*70)
        
        # 建立臨時目錄
        temp_dir = Path(tempfile.mkdtemp())
        
        # 建立臨時設定檔
        config_data = {
            "server": {"name": "test-server", "version": "2.0.0"},
            "api": {"base_url": "https://test.api.com/", "timeout": 60, "max_retries": 5},
            "defaults": {"bible_version": "kjv", "chinese_variant": "simplified", "search_limit": 100, "include_strong": True},
            "cache": {"enabled": False, "directory": ".test_cache", "cleanup_on_start": True},
            "logging": {"level": "DEBUG", "file": "test.log", "format": "%(levelname)s - %(message)s"}
        }
        temp_config_file = temp_dir / "test_config.json"
        with open(temp_config_file, "w") as f:
            json.dump(config_data, f)
        
        # Mock monkeypatch for environment variables
        class MockMonkeypatch:
            def __init__(self):
                self.original_env = os.environ.copy()
            
            def setenv(self, key, value):
                os.environ[key] = value
            
            def cleanup(self):
                os.environ.clear()
                os.environ.update(self.original_env)
        
        monkeypatch = MockMonkeypatch()
        
        tests = [
            ("Default Configuration", test_default_config),
            ("Load from File", lambda: test_load_from_file(temp_config_file)),
            ("Load from Environment", lambda: test_load_from_env(monkeypatch)),
            ("Environment Override File", lambda: test_env_override_file(temp_config_file, monkeypatch)),
            ("Runtime Update", test_runtime_update),
            ("Get Value", test_get_value),
            ("To Dictionary", test_to_dict),
            ("Save and Load", lambda: test_save_and_load(temp_dir)),
            ("Sources Tracking", lambda: test_config_sources(temp_config_file, monkeypatch)),
            ("Global Instance", test_global_config),
            ("Type Validation", test_type_validation),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                monkeypatch.cleanup()  # Reset env for each test
                monkeypatch = MockMonkeypatch()
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
        monkeypatch.cleanup()
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
            print("\n🎉 All configuration tests passed!")
        else:
            print(f"\n⚠️  {failed} test(s) failed")
    
    # 執行測試
    asyncio.run(run_all_tests())
