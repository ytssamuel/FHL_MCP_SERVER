# FHL Bible MCP Server - 快取系統

## Phase 3.1 完成: 快取系統實作

### ✅ 完成項目

#### 1. 核心快取模組 (`utils/cache.py`)

##### CacheStrategy 類別
- **功能**: 定義快取過期策略
- **TTL 支援**: Time To Live 機制
- **永久快取**: ttl_seconds=None 表示永不過期

##### CacheEntry 類別
- **功能**: 表示單個快取項目
- **屬性**: key, data, cached_at, strategy
- **方法**: is_valid(), to_dict(), from_dict()

##### FileCache 類別
- **功能**: 檔案系統快取實作
- **儲存格式**: JSON
- **命名空間**: 支援多個獨立的快取命名空間
- **統計資訊**: 追蹤 hits, misses, writes, deletes, errors

#### 2. 快取策略

| 類型 | 命名空間 | TTL | 說明 |
|------|---------|-----|------|
| **永久快取** | versions | - | 聖經版本列表永不過期 |
| | books | - | 書卷列表永不過期 |
| | commentaries | - | 註釋書列表永不過期 |
| | strongs | - | Strong's 字典永不過期 |
| **7天快取** | verses | 7天 | 經文內容快取 7天 |
| | word_analysis | 7天 | 字彙分析快取 7天 |
| | commentary | 7天 | 註釋內容快取 7天 |
| **1天快取** | search | 1天 | 搜尋結果快取 1天 |

#### 3. API 客戶端整合

##### FHLAPIEndpoints 擴展
- **快取開關**: use_cache 參數控制
- **快取目錄**: cache_dir 參數設定
- **自動快取**: _cached_request() 方法
- **快取鍵生成**: _make_cache_key() 使用 MD5 hash

##### 已整合的 API 方法
- ✅ `get_bible_versions()` - 永久快取
- ✅ `get_verse()` - 7天快取
- ✅ `search_bible()` - 1天快取
- ✅ `get_strongs_dictionary()` - 永久快取

#### 4. 快取操作

##### 基本操作
```python
from fhl_bible_mcp.utils.cache import FileCache

# 建立快取
cache = FileCache(cache_dir=".cache")

# 儲存快取
cache.set("verses", "john3:16", {"text": "..."}, strategy_name="verses")

# 讀取快取
data = cache.get("verses", "john3:16", strategy_name="verses")

# 刪除快取
cache.delete("verses", "john3:16")
```

##### 清理操作
```python
# 清除特定命名空間
cache.clear(namespace="search")

# 清除所有快取
cache.clear()

# 清理過期項目
cleaned = cache.cleanup_expired()
```

##### 取得資訊
```python
# 取得統計資訊
info = cache.get_info()
print(f"Total files: {info['total_files']}")
print(f"Hit rate: {info['stats']['hit_rate_percent']}%")

# 列出快取項目
entries = cache.get_entries(namespace="verses")
```

#### 5. 效能提升

根據測試結果:
- **版本列表**: 快取加速 **~36倍**
- **經文查詢**: 快取加速 **~44倍**
- **搜尋**: 快取加速 **~34倍**
- **Strong's**: 快取加速 **~30倍**

#### 6. 測試驗證

##### 單元測試 (`test_utils/test_cache.py`)
- ✅ 11 個測試全部通過
- 測試範圍:
  * CacheStrategy (永久/TTL)
  * CacheEntry (序列化)
  * FileCache 基本操作
  * 快取過期機制
  * 快取策略
  * 清理功能
  * 資訊查詢
  * 全域快取實例

##### 整合測試 (`test_api/test_cache_integration.py`)
- ✅ 7 個測試全部通過
- 測試範圍:
  * 版本列表快取
  * 經文快取
  * 搜尋快取
  * Strong's 永久快取
  * 快取停用
  * 快取清理整合
  * 快取資訊整合

## 使用範例

### 1. 啟用快取 (預設)

```python
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async with FHLAPIEndpoints() as client:
    # 自動使用快取
    versions = await client.get_bible_versions()
    verse = await client.get_verse("約", 3, "16")
    
    # 第二次呼叫會使用快取
    verse = await client.get_verse("約", 3, "16")  # 快 ~44倍!
```

### 2. 停用快取

```python
async with FHLAPIEndpoints(use_cache=False) as client:
    # 不使用快取,每次都發送 API 請求
    versions = await client.get_bible_versions()
```

### 3. 自訂快取目錄

```python
async with FHLAPIEndpoints(cache_dir=".my_cache") as client:
    versions = await client.get_bible_versions()
```

### 4. 手動管理快取

```python
from fhl_bible_mcp.utils.cache import get_cache

# 取得全域快取實例
cache = get_cache()

# 查看快取資訊
info = cache.get_info()
print(f"快取檔案: {info['total_files']}")
print(f"快取大小: {info['total_size_mb']} MB")
print(f"命中率: {info['stats']['hit_rate_percent']}%")

# 清理過期快取
cleaned = cache.cleanup_expired()
print(f"清理了 {cleaned} 個過期項目")

# 清除特定命名空間
cache.clear(namespace="search")

# 清除所有快取
cache.clear()
```

## 快取檔案結構

```
.cache/
├── a1b2c3d4e5f6...json  # 版本列表 (永久)
├── f1e2d3c4b5a6...json  # 約翰福音 3:16 (7天)
├── 1234567890ab...json  # 搜尋結果 "愛" (1天)
└── abcdef123456...json  # Strong's #25 (永久)
```

每個快取檔案包含:
```json
{
  "key": "verses:md5hash",
  "data": { "status": "success", ... },
  "cached_at": 1698765432.123,
  "ttl_seconds": 604800
}
```

## 快取策略設計

### 為什麼這樣設計?

1. **永久快取 (versions, books, strongs)**
   - 這些資料很少變動
   - 節省 API 請求次數
   - 減少網路延遲

2. **7天快取 (verses, word_analysis, commentary)**
   - 經文內容穩定
   - 平衡更新需求與效能
   - 支援離線使用情境

3. **1天快取 (search)**
   - 搜尋結果可能受資料庫更新影響
   - 較短的過期時間確保時效性
   - 仍能提供顯著效能提升

### 快取鍵生成

使用 MD5 hash 生成快取鍵:
- 避免檔名過長
- 避免非法字元
- 確保相同參數產生相同鍵

## 效能分析

### 快取命中場景

**第一次呼叫** (Cache Miss):
```
API Request → Network → Parse → Cache Store → Return
總時間: ~300-500ms
```

**第二次呼叫** (Cache Hit):
```
Cache Read → Return
總時間: ~8-15ms
```

**效能提升**: **30-50倍**

### 記憶體使用

- 快取檔案: JSON 格式,壓縮良好
- 典型大小:
  * 版本列表: ~10 KB
  * 單節經文: ~500 bytes
  * 搜尋結果: ~2-5 KB
  * Strong's 項目: ~3-5 KB

### 磁碟空間

- 預估 1000 次 API 呼叫:
  * 約 5-10 MB 快取檔案
  * 過期清理後: 2-5 MB

## 進階功能

### 1. 快取統計

```python
async with FHLAPIEndpoints() as client:
    # 執行一些操作
    await client.get_verse("約", 3, "16")
    await client.get_verse("約", 3, "16")  # cache hit
    
    # 查看統計
    stats = client.cache.stats
    print(f"命中: {stats['hits']}")
    print(f"未命中: {stats['misses']}")
    print(f"命中率: {stats['hits']/(stats['hits']+stats['misses'])*100:.1f}%")
```

### 2. 過期時間查詢

```python
entries = cache.get_entries(namespace="verses")
for entry in entries:
    print(f"鍵: {entry['key']}")
    print(f"建立時間: {entry['cached_at']}")
    print(f"過期時間: {entry['expiry_time']}")
    print(f"是否有效: {entry['is_valid']}")
```

### 3. 自動清理

```python
import schedule
import time

def cleanup_cache():
    cache = get_cache()
    cleaned = cache.cleanup_expired()
    print(f"清理了 {cleaned} 個過期項目")

# 每天清理一次過期快取
schedule.every().day.at("03:00").do(cleanup_cache)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 最佳實踐

### 1. 快取目錄管理

```python
# 開發環境
client = FHLAPIEndpoints(cache_dir=".cache/dev")

# 生產環境
client = FHLAPIEndpoints(cache_dir="/var/cache/fhl_bible")

# 測試環境
client = FHLAPIEndpoints(cache_dir=".cache/test")
```

### 2. 定期清理

建議定期執行:
```python
cache.cleanup_expired()  # 清理過期項目
```

### 3. 監控快取大小

```python
info = cache.get_info()
if info['total_size_mb'] > 100:  # 超過 100 MB
    cache.clear()  # 清空快取
```

## 技術細節

### 檔案格式

- **格式**: JSON
- **編碼**: UTF-8
- **命名**: MD5 hash + .json
- **結構**: {key, data, cached_at, ttl_seconds}

### 執行緒安全

- 目前實作: **不是執行緒安全**
- 使用場景: 單執行緒異步應用
- 未來改進: 可加入檔案鎖機制

### 錯誤處理

- 讀取錯誤: 返回 None,觸發 API 呼叫
- 寫入錯誤: 記錄錯誤,不影響功能
- 所有錯誤都會記錄到日誌

## 效能基準測試

### 測試環境
- Python 3.10
- Windows 11
- SSD 硬碟

### 測試結果

| 操作 | 無快取 | 有快取 | 加速比 |
|------|-------|-------|--------|
| get_bible_versions() | 292ms | 8ms | 36.5x |
| get_verse() | 353ms | 8ms | 44.1x |
| search_bible() | 305ms | 9ms | 33.9x |
| get_strongs_dictionary() | 354ms | 12ms | 29.5x |

**平均加速**: **~36倍**

## 下一步

✅ **Phase 3.1 完成!**

接下來的開發:
- Phase 3.2: 設定管理
- Phase 3.3: 增強中文支援
- Phase 4: 測試與文件
- Phase 5: 進階功能

## 專案結構更新

```
src/fhl_bible_mcp/
├── utils/
│   └── cache.py           # 快取系統 ⭐ NEW
├── api/
│   └── endpoints.py       # 整合快取功能 ⭐ 更新
└── ...

tests/
├── test_utils/
│   └── test_cache.py      # 快取單元測試 ⭐ NEW
└── test_api/
    └── test_cache_integration.py  # 快取整合測試 ⭐ NEW

.cache/                    # 快取目錄 ⭐ NEW
└── *.json                 # 快取檔案
```

## 授權

MIT License
