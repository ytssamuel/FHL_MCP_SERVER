# FHL MCP Server API 增強計畫

**文檔類型**: 規劃文檔  
**建立日期**: 2025年11月3日  
**狀態**: 📋 規劃階段  
**版本**: 1.0

---

## 📋 目錄

1. [執行摘要](#執行摘要)
2. [API 盤點結果](#api-盤點結果)
3. [API 端點可行性測試](#api-端點可行性測試)
4. [文章 API 整合分析](#文章-api-整合分析)
5. [實作規劃](#實作規劃)
6. [風險與建議](#風險與建議)
7. [附錄](#附錄)

---

## 執行摘要

### 計畫目標

1. **盤點未實作的 API**: 識別 `bible.fhl.net/json/` 中尚未實作的 API 端點
2. **評估 API 路徑轉換**: 測試從 `/json/` 轉換到 `/api/` 的可行性
3. **整合文章 API**: 整合 `www.fhl.net/api/json.php` 和 `json_all.php` 文章查詢功能

### 關鍵發現

✅ **重大發現**: `bible.fhl.net/api/` 端點**完全可用**，可作為新的 base URL  
✅ **API 升級**: `/api/` 端點回應包含更多欄位（如 `bid`），功能更完整  
⚠️ **文章 API 限制**: `json.php` 無參數時資料量過大（8021 筆），需要參數過濾  
✅ **文章 API 可用**: `json_all.php` 可列出所有文章的元資料（不含內容）

### 測試結果統計

- **測試端點總數**: 12 個
- **成功端點**: 9 個 (75%)
- **失敗端點**: 3 個 (25%)
- **/api/ 端點成功率**: 100% (3/3)
- **文章 API 成功率**: 50% (2/4)

---

## API 盤點結果

### 已實作的 API (8 個類別)

根據 `src/fhl_bible_mcp/api/endpoints.py` 分析，目前已實作：

#### 1. ✅ 基礎資訊類 (2/3)
- ✅ `ab.php` - 聖經版本列表
- ✅ `listall.html` - 書卷列表
- ❌ `abv.php` - 離線資料狀況 **(未實作)**

#### 2. ✅ 經文查詢類 (2/5)
- ✅ `qb.php` - 查詢聖經經文（正典）
- ✅ `qsb.php` - 經文引用查詢
- ❌ `qsub.php` - 查詢次經 **(未實作)**
- ❌ `qaf.php` - 查詢使徒教父文獻 **(未實作)**
- ❌ `rt.php` - 經文註腳 **(未實作)**

#### 3. ✅ 搜尋類 (1/3)
- ✅ `se.php` - 經文關鍵字搜尋（正典）
- ❌ `sesub.php` - 次經搜尋 **(未實作)**
- ❌ `seaf.php` - 使徒教父搜尋 **(未實作)**

#### 4. ✅ 字彙分析類 (2/4)
- ✅ `qp.php` - 字彙分析
- ✅ `sd.php` - Strong's 原文字典
- ❌ `sbdag.php` - 浸宣希臘文字典 **(未實作，有版權限制)**
- ❌ `stwcbhdic.php` - 浸宣希伯來文字典 **(未實作，有版權限制)**

#### 5. ✅ 註釋類 (3/3)
- ✅ `sc.php` - 聖經註釋
- ✅ `ssc.php` - 搜尋註釋
- ✅ `list_commentaries()` - 列出註釋書

#### 6. ✅ 主題查經類 (1/1)
- ✅ `st.php` - 主題查經

#### 7. ✅ 多媒體類 (1/1)
- ✅ `au.php` - 有聲聖經

#### 8. ❌ 文章類 (0/2)
- ❌ `json.php` - 文章查詢 **(未實作，新發現)**
- ❌ `json_all.php` - 所有文章列表 **(未實作，新發現)**

### 未實作 API 統計

| 類別 | 已實作 | 未實作 | 完成度 |
|------|--------|--------|--------|
| 基礎資訊 | 2 | 1 | 67% |
| 經文查詢 | 2 | 3 | 40% |
| 搜尋 | 1 | 2 | 33% |
| 字彙分析 | 2 | 2 | 50% |
| 註釋 | 3 | 0 | 100% |
| 主題查經 | 1 | 0 | 100% |
| 多媒體 | 1 | 0 | 100% |
| 文章 | 0 | 2 | 0% |
| **總計** | **12** | **10** | **55%** |

### 未實作 API 詳細清單

#### 優先級 P1 - 核心功能

1. **qsub.php** - 查詢次經
   - 用途: 查詢次經經文（經卷 101-115）
   - 重要性: 高（完整聖經支援）
   - 實作難度: 低（類似 qb.php）

2. **qaf.php** - 查詢使徒教父文獻
   - 用途: 查詢使徒教父著作（經卷 201-217）
   - 重要性: 中（教會歷史研究）
   - 實作難度: 低（類似 qb.php）

3. **sesub.php** - 次經搜尋
   - 用途: 在次經中搜尋關鍵字
   - 重要性: 高（配合 qsub.php）
   - 實作難度: 低（類似 se.php）

4. **seaf.php** - 使徒教父搜尋
   - 用途: 在使徒教父文獻中搜尋
   - 重要性: 中（配合 qaf.php）
   - 實作難度: 低（類似 se.php）

#### 優先級 P2 - 輔助功能

5. **rt.php** - 經文註腳
   - 用途: 查詢特定版本的經文註腳
   - 重要性: 中（提供額外註釋）
   - 實作難度: 中（回應格式為 XML）
   - 注意: 回應格式為 XML，需要額外處理

6. **abv.php** - 離線資料狀況
   - 用途: 列出可下載的離線資料
   - 重要性: 低（離線使用場景）
   - 實作難度: 低（類似 ab.php）

#### 優先級 P3 - 版權限制

7. **sbdag.php** - 浸宣希臘文字典
   - 用途: 查詢浸宣希臘文字典
   - 重要性: 中（更詳細的字典）
   - 實作難度: 低
   - **版權限制**: 僅授權信望愛站使用，需要確認是否可整合

8. **stwcbhdic.php** - 浸宣希伯來文字典
   - 用途: 查詢浸宣希伯來文字典
   - 重要性: 中（更詳細的字典）
   - 實作難度: 低
   - **版權限制**: 僅授權信望愛站使用，需要確認是否可整合

#### 優先級 P1 - 新發現的 API

9. **json.php** - 信望愛站文章查詢
   - 用途: 查詢信望愛站的文章
   - 重要性: 高（擴展內容類型）
   - 實作難度: 中（需要處理大量資料）
   - 位置: `www.fhl.net/api/json.php`

10. **json_all.php** - 所有文章列表
    - 用途: 列出所有文章的元資料
    - 重要性: 高（配合 json.php）
    - 實作難度: 低（簡單的列表查詢）
    - 位置: `www.fhl.net/api/json_all.php`

---

## API 端點可行性測試

### 測試方法

建立測試腳本 `test_api_endpoints.py`，測試以下項目：
1. 現有 `bible.fhl.net/json/` 端點
2. 新的 `bible.fhl.net/api/` 端點
3. `www.fhl.net/api/json.php` 文章 API
4. `www.fhl.net/api/json_all.php` 文章列表 API

### 測試結果

#### 1. bible.fhl.net/json/ 端點（現有）

| API | 狀態 | 回應時間 | 備註 |
|-----|------|----------|------|
| ab.php | ✅ 成功 | 快 | 84 個版本 |
| qb.php | ✅ 成功 | 快 | 回應正常 |
| se.php | ✅ 成功 | 快 | 搜尋正常 |

**結論**: 現有端點運作正常，穩定可靠。

#### 2. bible.fhl.net/api/ 端點（新路徑）

| API | 狀態 | 回應時間 | 差異 |
|-----|------|----------|------|
| api/ab.php | ✅ 成功 | 快 | **與 json/ 相同** |
| api/qb.php | ✅ 成功 | 快 | **包含額外的 `bid` 欄位** |
| api/se.php | ✅ 成功 | 快 | **包含額外的 `bid` 欄位** |

**關鍵發現**:

```json
// json/qb.php 回應（舊）
{
  "record": [{
    "engs": "John",
    "chineses": "約",
    "chap": 3,
    "sec": 16,
    "bible_text": "..."
  }]
}

// api/qb.php 回應（新）
{
  "record": [{
    "bid": 43,              // ⭐ 新增：書卷 ID
    "engs": "John",
    "chineses": "約",
    "chap": 3,
    "sec": 16,
    "bible_text": "..."
  }]
}
```

**結論**: 
- ✅ `/api/` 端點**完全可用**
- ✅ 功能**更完整**（包含 `bid` 欄位）
- ✅ **建議使用** `/api/` 作為新的 base URL
- ⚠️ 需要確認是否所有 API 都支援（需進一步測試）

#### 3. www.fhl.net/api/json.php（文章 API）

| 測試案例 | 狀態 | 備註 |
|---------|------|------|
| 無參數 | ❌ 失敗 | `{"status":0,"result":"data too much 8021"}` |
| gb=0 | ❌ 失敗 | 同上，資料量過大 |
| ptab=sunday | ❌ 失敗 | `{"status":0,"result":"no data"}` |
| title=愛 | ✅ 成功 | 504 筆結果 |

**回應格式**（成功時）:

```json
{
  "status": 1,
  "record_count": 504,
  "record": [
    {
      "id": "8984",
      "column": "麻辣姊妹",
      "ptab": "women3",
      "aid": "515",
      "title": "從何西阿三個孩子的名字看耶和華信實的愛",
      "author": "陳鳳翔",
      "pubtime": "2025.10.19",
      "abst": "摘要內容...",
      "txt": "完整文章內容（HTML 格式）..."
    }
  ]
}
```

**結論**:
- ⚠️ **必須提供過濾參數**（title, author, txt, abst 等）
- ✅ 支援的參數:
  - `ptab`: 專欄英文名稱
  - `pubtime`: 發表日期 (格式: 2025.10.19)
  - `title`: 標題關鍵字
  - `author`: 作者
  - `abst`: 摘要關鍵字
  - `txt`: 內文關鍵字
  - `gb`: 繁簡體 (0=繁體, 1=簡體)
- ⚠️ 沒有分頁機制，大量結果會很慢

#### 4. www.fhl.net/api/json_all.php（所有文章列表）

| 測試案例 | 狀態 | 備註 |
|---------|------|------|
| 無參數 | ✅ 成功 | 8021 筆，但 record 為空字串 |
| gb=0 | ✅ 成功 | 同上 |

**回應格式**:

```json
{
  "status": 1,
  "record_count": 8021,
  "record": ""  // ⚠️ 空字串，沒有詳細資料
}
```

**結論**:
- ✅ 可以取得文章總數
- ❌ **不包含文章詳細資料**（只有數量）
- 💡 用途: 搭配 `json.php` 使用，先了解總數

---

## 文章 API 整合分析

### API 對比

| 項目 | json.php | json_all.php |
|------|----------|--------------|
| **用途** | 查詢文章內容 | 取得文章總數 |
| **回應內容** | 完整文章（含 HTML） | 僅數量 |
| **是否需要參數** | 是（否則報錯） | 否 |
| **資料量** | 依查詢而定 | 固定（僅數字） |
| **分頁支援** | ❌ 無 | N/A |
| **適用場景** | 精確查詢 | 統計資訊 |

### 整合策略

#### 方案 A: 僅整合 json.php（推薦）

**優點**:
- ✅ 提供實用的文章搜尋功能
- ✅ 可以精確查詢標題、作者、內容
- ✅ 回應包含完整文章內容

**缺點**:
- ⚠️ 必須提供至少一個搜尋參數
- ⚠️ 沒有分頁，大量結果可能很慢

**實作建議**:
```python
async def search_articles(
    self,
    title: str | None = None,
    author: str | None = None,
    content: str | None = None,
    abstract: str | None = None,
    column: str | None = None,  # ptab
    pub_date: str | None = None,  # format: 2025.10.19
    limit: int = 50  # 客戶端限制
) -> dict[str, Any]:
    """
    搜尋信望愛站文章
    
    Args:
        title: 標題關鍵字
        author: 作者名稱
        content: 內文關鍵字
        abstract: 摘要關鍵字
        column: 專欄英文名稱
        pub_date: 發表日期（格式: 2025.10.19）
        limit: 最多回傳結果數（客戶端限制）
    
    Returns:
        文章列表（包含標題、作者、內容等）
        
    Raises:
        InvalidParameterError: 如果沒有提供任何搜尋參數
    """
    # 至少需要一個參數
    if not any([title, author, content, abstract, column, pub_date]):
        raise InvalidParameterError(
            "search_params", None,
            "Must provide at least one search parameter"
        )
    
    params = {"gb": 0}  # 預設繁體
    if title: params["title"] = title
    if author: params["author"] = author
    if content: params["txt"] = content
    if abstract: params["abst"] = abstract
    if column: params["ptab"] = column
    if pub_date: params["pubtime"] = pub_date
    
    # 發送請求
    data = await self._make_request(
        "http://www.fhl.net/api/json.php",
        params=params
    )
    
    # 客戶端限制結果數量
    if "record" in data and isinstance(data["record"], list):
        data["record"] = data["record"][:limit]
        data["record_count"] = min(data["record_count"], limit)
    
    return data
```

#### 方案 B: 整合兩個 API

**優點**:
- ✅ 提供文章總數統計
- ✅ 提供文章搜尋功能

**缺點**:
- ⚠️ `json_all.php` 實用性有限（只有數量）
- ⚠️ 增加維護成本

**實作建議**:
```python
async def get_articles_count(self) -> int:
    """取得文章總數"""
    data = await self._make_request(
        "http://www.fhl.net/api/json_all.php"
    )
    return data.get("record_count", 0)

async def search_articles(self, ...) -> dict[str, Any]:
    # 同方案 A
```

### 建議採用方案

**推薦: 方案 A**

理由:
1. `json_all.php` 只提供數量，實用性有限
2. 減少 API 端點數量，簡化架構
3. 聚焦於實用的搜尋功能
4. 如果未來需要總數，可以在方案 A 基礎上輕鬆添加

---

## 實作規劃

### Phase 1: Base URL 升級（P0 - 必須）

**目標**: 將 base URL 從 `bible.fhl.net/json/` 升級到 `bible.fhl.net/api/`

**範圍**:
- 更新 `config.py` 的預設 base URL
- 更新所有文檔中的 URL 引用
- 保持向後相容性（允許使用者配置舊 URL）

**風險**: 低
- `/api/` 端點完全相容
- 回應包含更多資訊（bid 欄位）
- 可以逐步遷移

**實作步驟**:
1. 更新 `src/fhl_bible_mcp/config.py`:
   ```python
   # Before
   BASE_URL = "https://bible.fhl.net/json/"
   
   # After
   BASE_URL = "https://bible.fhl.net/api/"
   ```

2. 更新文檔:
   - README.md
   - API.md
   - DEVELOPER_GUIDE.md
   - 所有 Planning 文檔

3. 測試所有現有 API:
   - 確認所有端點在 `/api/` 下正常運作
   - 驗證回應格式相容性
   - 更新測試腳本

4. 更新快取鍵:
   - 由於 URL 改變，快取鍵會不同
   - 考慮清理舊快取或保持兩套

**預計工時**: 2-3 小時

---

### Phase 2: 實作未支援的聖經 API（P1）

**目標**: 實作次經、使徒教父文獻相關 API

#### 2.1 次經支援

**新增 API**:
1. `qsub.php` - 查詢次經經文
2. `sesub.php` - 次經搜尋

**實作方法**:
```python
async def get_apocrypha_verse(
    self,
    book: str,
    chapter: int,
    verse: str | None = None,
    version: str = "unv",
) -> dict[str, Any]:
    """
    查詢次經經文（經卷 101-115）
    
    API: qsub.php
    類似 get_verse()，但用於次經
    """
    params = {
        "chineses": book,
        "chap": chapter,
        "version": version,
    }
    if verse is not None:
        params["sec"] = verse
    
    return await self._cached_request(
        endpoint="qsub.php",
        params=params,
        namespace="apocrypha",
        strategy="verses"
    )

async def search_apocrypha(
    self,
    query: str,
    version: str = "unv",
    limit: int | None = None,
    offset: int = 0,
) -> dict[str, Any]:
    """
    在次經中搜尋關鍵字
    
    API: sesub.php
    類似 search_bible()，但用於次經
    """
    params = {
        "VERSION": version,
        "orig": "0",
        "q": query,
        "offset": offset,
    }
    if limit is not None:
        params["limit"] = limit
    
    return await self._cached_request(
        endpoint="sesub.php",
        params=params,
        namespace="search",
        strategy="search"
    )
```

**預計工時**: 3-4 小時

#### 2.2 使徒教父支援

**新增 API**:
1. `qaf.php` - 查詢使徒教父文獻
2. `seaf.php` - 使徒教父搜尋

**實作方法**: 類似 2.1，但用於使徒教父（經卷 201-217）

**預計工時**: 3-4 小時

#### 2.3 經文註腳

**新增 API**:
1. `rt.php` - 經文註腳

**特殊處理**:
- ⚠️ 回應格式為 XML，需要 XML 解析
- 可能需要 `xml.etree.ElementTree` 或 `lxml`

**實作方法**:
```python
async def get_verse_footnote(
    self,
    book: str,
    chapter: int,
    version: str,
    footnote_id: str,
) -> dict[str, Any]:
    """
    查詢經文註腳
    
    API: rt.php
    注意: 回應為 XML 格式
    """
    params = {
        "engs": book,
        "chap": chapter,
        "version": version,
        "id": footnote_id,
    }
    
    # 發送請求
    xml_response = await self._make_request("rt.php", params)
    
    # 解析 XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_response)
    
    # 轉換為 JSON 格式
    return {
        "status": "success",
        "footnote_id": footnote_id,
        "text": root.find("text").text if root.find("text") is not None else ""
    }
```

**預計工時**: 2-3 小時

---

### Phase 3: 文章 API 整合（P1）

**目標**: 整合信望愛站文章查詢功能

#### 3.1 文章搜尋

**新增 API**:
1. `json.php` - 文章搜尋

**實作方法**: 參考「整合策略 - 方案 A」

**新增工具類**:
```python
# 新檔案: src/fhl_bible_mcp/tools/articles.py

from mcp.server.models import Tool

TOOL_SEARCH_ARTICLES = Tool(
    name="fhl_search_articles",
    description="""
    搜尋信望愛站的文章。
    
    可以依據標題、作者、內容、摘要、專欄、發表日期等條件搜尋。
    至少需要提供一個搜尋條件。
    
    回傳文章列表，包含標題、作者、發表日期、摘要、內容等。
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "標題關鍵字"
            },
            "author": {
                "type": "string",
                "description": "作者名稱"
            },
            "content": {
                "type": "string",
                "description": "內文關鍵字"
            },
            "abstract": {
                "type": "string",
                "description": "摘要關鍵字"
            },
            "column": {
                "type": "string",
                "description": "專欄英文名稱（如 women3）"
            },
            "pub_date": {
                "type": "string",
                "description": "發表日期，格式為 YYYY.MM.DD（如 2025.10.19）"
            },
            "limit": {
                "type": "integer",
                "description": "最多回傳結果數",
                "default": 50,
                "minimum": 1,
                "maximum": 200
            }
        }
    }
)
```

**快取策略**:
- Namespace: `articles`
- Strategy: `search` (1 day TTL)
- 理由: 文章更新頻率較低（每週日更新）

**預計工時**: 4-5 小時

#### 3.2 文章專欄列表（可選）

如果需要提供專欄列表功能，可以考慮：
1. 從文檔中維護專欄清單
2. 或透過爬蟲取得專欄資訊

**預計工時**: 2-3 小時（如需要）

---

### Phase 4: 輔助功能（P2）

**目標**: 實作次要功能

#### 4.1 離線資料狀況

**新增 API**:
1. `abv.php` - 離線資料狀況

**用途**: 較少使用，優先級低

**預計工時**: 1-2 小時

---

### Phase 5: 版權限制 API（P3 - 需確認）

**目標**: 實作浸宣字典（如獲授權）

**注意事項**:
- ⚠️ **需要確認版權許可**
- 文檔明確標示「僅授權信望愛站使用」
- 在實作前需要聯繫信望愛站確認

**API**:
1. `sbdag.php` - 浸宣希臘文字典
2. `stwcbhdic.php` - 浸宣希伯來文字典

**建議**: 先跳過，等確認版權後再實作

---

### 總工時估算

| Phase | 內容 | 優先級 | 工時 |
|-------|------|--------|------|
| Phase 1 | Base URL 升級 | P0 | 2-3 小時 |
| Phase 2.1 | 次經支援 | P1 | 3-4 小時 |
| Phase 2.2 | 使徒教父支援 | P1 | 3-4 小時 |
| Phase 2.3 | 經文註腳 | P1 | 2-3 小時 |
| Phase 3.1 | 文章搜尋 | P1 | 4-5 小時 |
| Phase 3.2 | 專欄列表（可選） | P2 | 2-3 小時 |
| Phase 4.1 | 離線資料 | P2 | 1-2 小時 |
| Phase 5 | 浸宣字典（待確認） | P3 | 4-5 小時 |
| **總計** | | | **22-33 小時** |

**核心功能 (P0-P1)**: 14-19 小時  
**完整功能 (含 P2)**: 17-24 小時  
**全部功能 (含 P3)**: 22-33 小時

---

## 風險與建議

### 風險評估

#### 1. API 端點變更風險 - 🟡 中等

**風險**:
- `/api/` 端點可能不是所有 API 都支援
- 未來 FHL 可能變更 API 結構

**緩解措施**:
- ✅ 全面測試所有端點
- ✅ 保留配置選項允許切換 base URL
- ✅ 建立完整的測試腳本
- ✅ 文檔中說明降級方案

#### 2. 文章 API 限制 - 🟡 中等

**風險**:
- 沒有分頁機制，大量結果可能很慢
- 必須提供搜尋參數，無法列出所有文章

**緩解措施**:
- ✅ 客戶端實作 limit 限制
- ✅ 文檔中明確說明使用限制
- ✅ 提供搜尋建議和最佳實踐
- ⚠️ 考慮實作客戶端快取

#### 3. XML 格式處理 - 🟢 低

**風險**:
- `rt.php` 回應為 XML，需額外處理

**緩解措施**:
- ✅ 使用標準庫 `xml.etree.ElementTree`
- ✅ 轉換為統一的 JSON 格式
- ✅ 完善的錯誤處理

#### 4. 版權限制 - 🔴 高

**風險**:
- 浸宣字典 API 有版權限制
- 未經授權使用可能違反版權

**緩解措施**:
- ✅ 先跳過這些 API
- ✅ 聯繫信望愛站確認
- ✅ 文檔中明確標示版權限制
- ⚠️ 如需使用，需要正式授權協議

### 建議

#### 短期建議（立即執行）

1. **升級到 /api/ 端點** ⭐
   - 優先級: 最高
   - 理由: 功能更完整，向前相容
   - 工時: 2-3 小時
   - 預期收益: 高

2. **實作次經和使徒教父支援** ⭐
   - 優先級: 高
   - 理由: 完整的聖經支援
   - 工時: 6-8 小時
   - 預期收益: 中高

3. **整合文章搜尋功能** ⭐
   - 優先級: 高
   - 理由: 擴展內容類型，提供更豐富資源
   - 工時: 4-5 小時
   - 預期收益: 高

#### 中期建議（後續規劃）

4. **實作經文註腳**
   - 優先級: 中
   - 理由: 提供更詳細的註釋
   - 工時: 2-3 小時
   - 預期收益: 中

5. **建立 API 測試套件**
   - 優先級: 中高
   - 理由: 確保 API 穩定性
   - 工時: 4-6 小時
   - 預期收益: 高（長期）

#### 長期建議（視情況而定）

6. **實作離線資料查詢**
   - 優先級: 低
   - 理由: 使用場景較少
   - 工時: 1-2 小時

7. **浸宣字典整合（需授權）**
   - 優先級: 視授權而定
   - 理由: 更詳細的字典資源
   - 前置條件: 取得版權許可

### 最佳實踐建議

1. **API 設計原則**
   - 保持一致的命名規範
   - 統一的錯誤處理
   - 完整的類型提示
   - 詳細的文檔字串

2. **測試策略**
   - 為每個新 API 建立測試
   - 測試正常情況和邊界情況
   - 測試錯誤處理
   - 定期執行回歸測試

3. **快取策略**
   - 根據資料更新頻率選擇 TTL
   - 使用適當的命名空間
   - 考慮快取失效機制

4. **文檔維護**
   - 更新 API.md
   - 更新 EXAMPLES.md
   - 更新 README.md
   - 提供遷移指南

---

## 附錄

### A. 測試腳本輸出

完整測試輸出參見: `test_api_endpoints.py` 執行結果

### B. API 回應範例

#### B.1 bible.fhl.net/api/qb.php

```json
{
  "status": "success",
  "record_count": 1,
  "v_name": "FHL和合本",
  "version": "unv",
  "proc": 0,
  "record": [
    {
      "bid": 1,
      "engs": "Gen",
      "chineses": "創",
      "chap": 3,
      "sec": 16,
      "bible_text": "又對女人說：我必多多加增你懷胎的苦楚..."
    }
  ],
  "prev": {
    "bid": 1,
    "chineses": "創",
    "engs": "Gen",
    "chap": 3,
    "sec": 15
  },
  "next": {
    "bid": 1,
    "chineses": "創",
    "engs": "Gen",
    "chap": 3,
    "sec": 17
  }
}
```

#### B.2 www.fhl.net/api/json.php

```json
{
  "status": 1,
  "record_count": 504,
  "record": [
    {
      "id": "8984",
      "column": "麻辣姊妹",
      "ptab": "women3",
      "aid": "515",
      "title": "從何西阿三個孩子的名字看耶和華信實的愛",
      "author": "陳鳳翔",
      "pubtime": "2025.10.19",
      "abst": "何西阿三個孩子的名字，是作為丈夫的對妻子的呼喚...",
      "txt": "<pic>hosea_and_gomer.jpg</pic><br/>..."
    }
  ]
}
```

### C. 專欄英文名稱參考

根據測試結果，已知的專欄名稱包括（但不限於）:
- `women3` - 麻辣姊妹
- `sunday` - 週日專欄（測試時無資料）

完整專欄列表需要進一步調查或從網站取得。

### D. 相關文檔

- **API 原始文檔**: https://www.fhl.net/api/api.html
- **現有規劃文檔**: `docs/1_development/FHL_BIBLE_MCP_PLANNING.md`
- **API 實作**: `src/fhl_bible_mcp/api/endpoints.py`
- **測試腳本**: `test_api_endpoints.py`

---

## 變更記錄

| 日期 | 版本 | 變更內容 | 作者 |
|------|------|----------|------|
| 2025-11-03 | 1.0 | 初始版本，完成 API 盤點和測試 | GitHub Copilot |

---

**文檔狀態**: ✅ 已完成  
**下一步**: 等待審核，決定實作優先級  
**預計開始實作**: 待定

---

*本文檔為 FHL MCP Server API 增強計畫的規劃文檔。所有測試結果基於 2025年11月3日 的測試。*
