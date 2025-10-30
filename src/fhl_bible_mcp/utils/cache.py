"""
Cache System for FHL Bible MCP Server

提供檔案快取功能，支援 TTL (Time To Live) 過期策略。
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CacheStrategy:
    """快取策略基類"""
    
    def __init__(self, ttl_seconds: Optional[int] = None):
        """
        初始化快取策略
        
        Args:
            ttl_seconds: 快取存活時間（秒），None 表示永久快取
        """
        self.ttl_seconds = ttl_seconds
    
    def is_expired(self, cached_time: float) -> bool:
        """
        檢查快取是否過期
        
        Args:
            cached_time: 快取建立時間（Unix timestamp）
            
        Returns:
            True 如果已過期，False 如果仍有效
        """
        if self.ttl_seconds is None:
            return False  # 永久快取永不過期
        
        elapsed = time.time() - cached_time
        return elapsed > self.ttl_seconds
    
    def get_expiry_time(self, cached_time: float) -> Optional[datetime]:
        """
        取得快取過期時間
        
        Args:
            cached_time: 快取建立時間（Unix timestamp）
            
        Returns:
            過期時間，None 表示永不過期
        """
        if self.ttl_seconds is None:
            return None
        
        return datetime.fromtimestamp(cached_time + self.ttl_seconds)


class CacheEntry:
    """快取項目"""
    
    def __init__(
        self,
        key: str,
        data: Any,
        cached_at: float,
        strategy: CacheStrategy
    ):
        """
        初始化快取項目
        
        Args:
            key: 快取鍵
            data: 快取資料
            cached_at: 快取時間
            strategy: 快取策略
        """
        self.key = key
        self.data = data
        self.cached_at = cached_at
        self.strategy = strategy
    
    def is_valid(self) -> bool:
        """檢查快取是否仍然有效"""
        return not self.strategy.is_expired(self.cached_at)
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return {
            "key": self.key,
            "data": self.data,
            "cached_at": self.cached_at,
            "ttl_seconds": self.strategy.ttl_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheEntry":
        """從字典建立快取項目"""
        strategy = CacheStrategy(ttl_seconds=data.get("ttl_seconds"))
        return cls(
            key=data["key"],
            data=data["data"],
            cached_at=data["cached_at"],
            strategy=strategy
        )


class FileCache:
    """
    檔案快取系統
    
    使用 JSON 格式儲存快取資料到檔案系統。
    """
    
    # 預設的快取策略（單位：秒）
    STRATEGIES = {
        "permanent": None,              # 永久快取
        "verses": 7 * 24 * 3600,        # 經文：7天
        "search": 1 * 24 * 3600,        # 搜尋：1天
        "word_analysis": 7 * 24 * 3600, # 字彙分析：7天
        "commentary": 7 * 24 * 3600,    # 註釋：7天
        "strongs": None,                # Strong's 字典：永久
        "versions": None,               # 版本列表：永久
        "books": None,                  # 書卷列表：永久
        "commentaries": None,           # 註釋書列表：永久
    }
    
    def __init__(self, cache_dir: str = ".cache"):
        """
        初始化檔案快取
        
        Args:
            cache_dir: 快取目錄路徑
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 快取統計
        self.stats = {
            "hits": 0,
            "misses": 0,
            "writes": 0,
            "deletes": 0,
            "errors": 0
        }
        
        logger.info(f"FileCache initialized: cache_dir={self.cache_dir.absolute()}")
    
    def _get_cache_key(self, namespace: str, key: str) -> str:
        """
        生成快取鍵
        
        Args:
            namespace: 命名空間（如 "verses", "search" 等）
            key: 鍵值
            
        Returns:
            組合後的快取鍵
        """
        return f"{namespace}:{key}"
    
    def _get_cache_file(self, cache_key: str) -> Path:
        """
        取得快取檔案路徑
        
        Args:
            cache_key: 快取鍵
            
        Returns:
            快取檔案路徑
        """
        # 使用 hash 避免檔名過長或包含非法字元
        key_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
    
    def get(
        self,
        namespace: str,
        key: str,
        strategy_name: str = "permanent"
    ) -> Optional[Any]:
        """
        取得快取資料
        
        Args:
            namespace: 命名空間
            key: 鍵值
            strategy_name: 快取策略名稱
            
        Returns:
            快取的資料，如果不存在或已過期則返回 None
        """
        cache_key = self._get_cache_key(namespace, key)
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            self.stats["misses"] += 1
            logger.debug(f"Cache miss: {cache_key}")
            return None
        
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            
            entry = CacheEntry.from_dict(cached_data)
            
            # 檢查是否過期
            if not entry.is_valid():
                self.stats["misses"] += 1
                logger.debug(f"Cache expired: {cache_key}")
                # 刪除過期的快取
                cache_file.unlink()
                return None
            
            self.stats["hits"] += 1
            logger.debug(f"Cache hit: {cache_key}")
            return entry.data
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error reading cache {cache_key}: {e}")
            return None
    
    def set(
        self,
        namespace: str,
        key: str,
        data: Any,
        strategy_name: str = "permanent"
    ) -> bool:
        """
        設定快取資料
        
        Args:
            namespace: 命名空間
            key: 鍵值
            data: 要快取的資料
            strategy_name: 快取策略名稱
            
        Returns:
            True 如果成功，False 如果失敗
        """
        cache_key = self._get_cache_key(namespace, key)
        cache_file = self._get_cache_file(cache_key)
        
        try:
            # 取得快取策略
            ttl_seconds = self.STRATEGIES.get(strategy_name)
            strategy = CacheStrategy(ttl_seconds=ttl_seconds)
            
            # 建立快取項目
            entry = CacheEntry(
                key=cache_key,
                data=data,
                cached_at=time.time(),
                strategy=strategy
            )
            
            # 寫入檔案
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
            
            self.stats["writes"] += 1
            logger.debug(f"Cache written: {cache_key} (strategy={strategy_name})")
            return True
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error writing cache {cache_key}: {e}")
            return False
    
    def delete(self, namespace: str, key: str) -> bool:
        """
        刪除快取項目
        
        Args:
            namespace: 命名空間
            key: 鍵值
            
        Returns:
            True 如果成功刪除，False 如果不存在或刪除失敗
        """
        cache_key = self._get_cache_key(namespace, key)
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            return False
        
        try:
            cache_file.unlink()
            self.stats["deletes"] += 1
            logger.debug(f"Cache deleted: {cache_key}")
            return True
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error deleting cache {cache_key}: {e}")
            return False
    
    def clear(self, namespace: Optional[str] = None) -> int:
        """
        清除快取
        
        Args:
            namespace: 命名空間（如果指定則只清除該命名空間的快取）
            
        Returns:
            清除的快取項目數量
        """
        cleared = 0
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    # 讀取快取檔案以取得命名空間
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cached_data = json.load(f)
                    
                    cache_key = cached_data.get("key", "")
                    
                    # 如果指定了命名空間，檢查是否匹配
                    if namespace is not None:
                        if not cache_key.startswith(f"{namespace}:"):
                            continue
                    
                    # 刪除快取檔案
                    cache_file.unlink()
                    cleared += 1
                    
                except Exception as e:
                    logger.error(f"Error clearing cache file {cache_file}: {e}")
                    self.stats["errors"] += 1
            
            logger.info(f"Cache cleared: {cleared} items (namespace={namespace})")
            return cleared
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            self.stats["errors"] += 1
            return cleared
    
    def cleanup_expired(self) -> int:
        """
        清理所有過期的快取項目
        
        Returns:
            清理的項目數量
        """
        cleaned = 0
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cached_data = json.load(f)
                    
                    entry = CacheEntry.from_dict(cached_data)
                    
                    # 如果過期則刪除
                    if not entry.is_valid():
                        cache_file.unlink()
                        cleaned += 1
                        logger.debug(f"Cleaned expired cache: {entry.key}")
                    
                except Exception as e:
                    logger.error(f"Error cleaning cache file {cache_file}: {e}")
                    self.stats["errors"] += 1
            
            logger.info(f"Cleanup completed: {cleaned} expired items removed")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            self.stats["errors"] += 1
            return cleaned
    
    def get_info(self) -> Dict[str, Any]:
        """
        取得快取資訊
        
        Returns:
            快取統計資訊
        """
        total_files = len(list(self.cache_dir.glob("*.json")))
        total_size = sum(
            f.stat().st_size for f in self.cache_dir.glob("*.json")
        )
        
        # 統計各命名空間的快取數量
        namespaces: Dict[str, int] = {}
        expired_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                
                cache_key = cached_data.get("key", "")
                namespace = cache_key.split(":", 1)[0] if ":" in cache_key else "unknown"
                namespaces[namespace] = namespaces.get(namespace, 0) + 1
                
                # 檢查是否過期
                entry = CacheEntry.from_dict(cached_data)
                if not entry.is_valid():
                    expired_count += 1
                    
            except Exception:
                pass
        
        hit_rate = 0.0
        total_requests = self.stats["hits"] + self.stats["misses"]
        if total_requests > 0:
            hit_rate = self.stats["hits"] / total_requests * 100
        
        return {
            "cache_dir": str(self.cache_dir.absolute()),
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "expired_count": expired_count,
            "namespaces": namespaces,
            "stats": {
                **self.stats,
                "hit_rate_percent": round(hit_rate, 2)
            }
        }
    
    def get_entries(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        取得快取項目列表
        
        Args:
            namespace: 命名空間篩選（可選）
            
        Returns:
            快取項目資訊列表
        """
        entries = []
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                
                cache_key = cached_data.get("key", "")
                
                # 命名空間篩選
                if namespace is not None:
                    if not cache_key.startswith(f"{namespace}:"):
                        continue
                
                entry = CacheEntry.from_dict(cached_data)
                
                entries.append({
                    "key": entry.key,
                    "cached_at": datetime.fromtimestamp(entry.cached_at).isoformat(),
                    "is_valid": entry.is_valid(),
                    "expiry_time": (
                        entry.strategy.get_expiry_time(entry.cached_at).isoformat()
                        if entry.strategy.get_expiry_time(entry.cached_at)
                        else "never"
                    ),
                    "file_size": cache_file.stat().st_size
                })
                
            except Exception as e:
                logger.error(f"Error reading cache entry {cache_file}: {e}")
        
        return entries


# 全域快取實例
_global_cache: Optional[FileCache] = None


def get_cache(cache_dir: str = ".cache") -> FileCache:
    """
    取得全域快取實例
    
    Args:
        cache_dir: 快取目錄
        
    Returns:
        FileCache 實例
    """
    global _global_cache
    
    if _global_cache is None:
        _global_cache = FileCache(cache_dir=cache_dir)
    
    return _global_cache


def reset_cache() -> None:
    """重置全域快取實例（主要用於測試）"""
    global _global_cache
    _global_cache = None
