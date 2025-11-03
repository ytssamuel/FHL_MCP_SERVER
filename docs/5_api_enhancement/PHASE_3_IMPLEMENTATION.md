# Phase 3 實施計劃：文章 API 整合

**階段**: Phase 3 - Article API Integration  
**日期**: 2025年11月4日  
**狀態**: 🔄 進行中

---

## 📋 目錄

1. [階段概述](#階段概述)
2. [Phase 3.1: 文章搜尋](#phase-31-文章搜尋)
3. [Phase 3.2: 專欄列表](#phase-32-專欄列表)
4. [實施檢查清單](#實施檢查清單)

---

## 階段概述

### 目標

整合信望愛站的文章查詢功能，讓使用者能夠：
1. 搜尋文章（依標題、作者、內容、摘要等）
2. 查詢可用的專欄列表

### API 端點

- **文章搜尋**: `www.fhl.net/api/json.php`
- **專欄資訊**: 從維護的清單提供

### 範圍

- ✅ Phase 3.1: 文章搜尋功能 (P1)
- ✅ Phase 3.2: 專欄列表功能 (P2)

---

## Phase 3.1: 文章搜尋

### API 規格

**端點**: `http://www.fhl.net/api/json.php`

**必要條件**: 至少提供一個搜尋參數（否則返回 "data too much"）

**參數**:
- `title`: 標題關鍵字
- `author`: 作者名稱
- `txt`: 內文關鍵字
- `abst`: 摘要關鍵字
- `ptab`: 專欄英文名稱
- `pubtime`: 發表日期 (格式: YYYY.MM.DD)
- `gb`: 繁簡體 (0=繁體, 1=簡體)

**響應範例**:
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
      "abst": "何西阿三個孩子的名字...",
      "txt": "<pic>hosea_and_gomer.jpg</pic><br/>..."
    }
  ]
}
```

### 實施方法

#### 1. API 端點層 (endpoints.py)

```python
async def search_articles(
    self,
    title: str | None = None,
    author: str | None = None,
    content: str | None = None,
    abstract: str | None = None,
    column: str | None = None,
    pub_date: str | None = None,
    use_simplified: bool = False,
    limit: int = 50
) -> dict[str, Any]:
    """
    搜尋信望愛站文章
    
    API: www.fhl.net/api/json.php
    
    Args:
        title: 標題關鍵字
        author: 作者名稱
        content: 內文關鍵字
        abstract: 摘要關鍵字
        column: 專欄英文名稱 (ptab)
        pub_date: 發表日期，格式 YYYY.MM.DD (如 2025.10.19)
        use_simplified: 是否使用簡體中文
        limit: 最多回傳結果數（客戶端限制）
    
    Returns:
        文章列表，包含標題、作者、內容等
    
    Raises:
        InvalidParameterError: 如果沒有提供任何搜尋參數
    
    Examples:
        >>> # 搜尋標題包含「愛」的文章
        >>> await api.search_articles(title="愛")
        
        >>> # 搜尋作者「陳鳳翔」的文章
        >>> await api.search_articles(author="陳鳳翔")
        
        >>> # 搜尋「麻辣姊妹」專欄
        >>> await api.search_articles(column="women3")
    """
    # 至少需要一個搜尋參數
    if not any([title, author, content, abstract, column, pub_date]):
        from fhl_bible_mcp.utils.errors import InvalidParameterError
        raise InvalidParameterError(
            "search_params",
            None,
            "Must provide at least one search parameter (title, author, content, abstract, column, or pub_date)"
        )
    
    # 構建參數
    params: dict[str, str | int] = {
        "gb": 1 if use_simplified else 0
    }
    
    if title:
        params["title"] = title
    if author:
        params["author"] = author
    if content:
        params["txt"] = content
    if abstract:
        params["abst"] = abstract
    if column:
        params["ptab"] = column
    if pub_date:
        params["pubtime"] = pub_date
    
    # 發送請求（使用完整 URL）
    data = await self._cached_request(
        endpoint="json.php",
        params=params,
        namespace="articles",
        strategy="search",
        base_url="http://www.fhl.net/api/"
    )
    
    # 客戶端限制結果數量
    if data.get("status") == 1 and "record" in data:
        if isinstance(data["record"], list) and len(data["record"]) > limit:
            data["record"] = data["record"][:limit]
            data["record_count"] = limit
            data["limited"] = True  # 標記為已限制
    
    return data
```

#### 2. 工具層 (tools/articles.py)

```python
"""
Article Search Tools

Tools for searching and browsing Faith Hope Love (信望愛) articles.
"""

from typing import Any
from mcp.types import Tool, TextContent

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


def get_articles_tool_definitions() -> list[dict[str, Any]]:
    """Get article search tool definitions"""
    return [
        {
            "name": "search_fhl_articles",
            "description": """搜尋信望愛站的文章。
            
可以依據標題、作者、內容、摘要、專欄、發表日期等條件搜尋。
至少需要提供一個搜尋條件。

回傳文章列表，包含：
- 標題 (title)
- 作者 (author)
- 發表日期 (pubtime)
- 專欄 (column)
- 摘要 (abst)
- 完整內容 (txt, HTML 格式)

範例：
- 搜尋標題包含「愛」的文章
- 搜尋作者「陳鳳翔」的文章
- 搜尋「麻辣姊妹」專欄的文章
""",
            "inputSchema": {
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
                        "description": "專欄英文代碼（如 women3）。使用 list_fhl_article_columns 工具查看可用專欄"
                    },
                    "pub_date": {
                        "type": "string",
                        "description": "發表日期，格式為 YYYY.MM.DD（如 2025.10.19）"
                    },
                    "use_simplified": {
                        "type": "boolean",
                        "description": "是否使用簡體中文（預設：false，使用繁體）",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多回傳結果數（預設：50，範圍：1-200）",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 200
                    }
                }
            }
        }
    ]


async def handle_search_articles(
    endpoints: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[TextContent]:
    """Handle search_fhl_articles tool call"""
    
    result = await endpoints.search_articles(
        title=arguments.get("title"),
        author=arguments.get("author"),
        content=arguments.get("content"),
        abstract=arguments.get("abstract"),
        column=arguments.get("column"),
        pub_date=arguments.get("pub_date"),
        use_simplified=arguments.get("use_simplified", False),
        limit=arguments.get("limit", 50)
    )
    
    # 格式化輸出
    if result.get("status") == 1 and result.get("record_count", 0) > 0:
        articles = result.get("record", [])
        
        if not articles:
            return [TextContent(
                type="text",
                text="⚠️ 未找到符合條件的文章"
            )]
        
        output = [f"📚 找到 {result['record_count']} 篇文章"]
        
        if result.get("limited"):
            output.append(f"（顯示前 {arguments.get('limit', 50)} 篇）")
        
        output.append("\n" + "="*60 + "\n")
        
        for i, article in enumerate(articles, 1):
            output.append(f"📄 文章 {i}")
            output.append(f"標題：{article.get('title', 'N/A')}")
            output.append(f"作者：{article.get('author', 'N/A')}")
            output.append(f"專欄：{article.get('column', 'N/A')} ({article.get('ptab', 'N/A')})")
            output.append(f"日期：{article.get('pubtime', 'N/A')}")
            output.append(f"\n摘要：\n{article.get('abst', 'N/A')}")
            
            # 內容預覽（去除 HTML 標籤）
            content = article.get('txt', '')
            if content:
                # 簡單去除 HTML 標籤
                import re
                clean_content = re.sub(r'<[^>]+>', '', content)
                preview = clean_content[:200] + "..." if len(clean_content) > 200 else clean_content
                output.append(f"\n內容預覽：\n{preview}")
            
            output.append("\n" + "-"*60 + "\n")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif result.get("status") == 0:
        error_msg = result.get("result", "Unknown error")
        return [TextContent(
            type="text",
            text=f"❌ 搜尋失敗：{error_msg}\n\n💡 提示：請確認至少提供一個搜尋條件"
        )]
    
    else:
        return [TextContent(
            type="text",
            text="⚠️ 未找到符合條件的文章"
        )]
```

---

## Phase 3.2: 專欄列表

### 資料來源

由於 API 沒有提供專欄列表端點，我們維護一個專欄清單。

### 專欄資料

根據信望愛站網站和測試，已知專欄包括：

| 專欄代碼 | 專欄名稱 | 說明 |
|---------|---------|------|
| women3 | 麻辣姊妹 | 女性信仰生活 |
| sunday | 主日學 | 主日學教材 |
| youth | 青少年 | 青少年信仰 |
| family | 家庭 | 家庭生活 |
| theology | 神學 | 神學探討 |
| bible_study | 查經 | 聖經研究 |
| devotion | 靈修 | 靈修分享 |

### 實施方法

#### 1. API 端點層 (endpoints.py)

```python
def list_article_columns(self) -> list[dict[str, str]]:
    """
    列出可用的文章專欄
    
    Returns:
        專欄列表，包含專欄代碼、名稱、說明
    
    Note:
        此資料由系統維護，非從 API 查詢
    
    Examples:
        >>> columns = api.list_article_columns()
        >>> for col in columns:
        ...     print(f"{col['code']}: {col['name']}")
    """
    return [
        {
            "code": "women3",
            "name": "麻辣姊妹",
            "description": "女性信仰生活分享"
        },
        {
            "code": "sunday",
            "name": "主日學",
            "description": "主日學教材與資源"
        },
        {
            "code": "youth",
            "name": "青少年",
            "description": "青少年信仰與生活"
        },
        {
            "code": "family",
            "name": "家庭",
            "description": "家庭生活與信仰"
        },
        {
            "code": "theology",
            "name": "神學",
            "description": "神學探討與研究"
        },
        {
            "code": "bible_study",
            "name": "查經",
            "description": "聖經研究與分享"
        },
        {
            "code": "devotion",
            "name": "靈修",
            "description": "靈修心得與見證"
        },
        {
            "code": "mission",
            "name": "宣教",
            "description": "宣教事工與分享"
        },
        {
            "code": "church",
            "name": "教會",
            "description": "教會生活與事奉"
        },
        {
            "code": "culture",
            "name": "文化",
            "description": "信仰與文化對話"
        }
    ]
```

#### 2. 工具層 (tools/articles.py - 擴展)

```python
def get_articles_tool_definitions() -> list[dict[str, Any]]:
    """Get article search tool definitions"""
    return [
        # ... search_fhl_articles (前面已定義) ...
        
        {
            "name": "list_fhl_article_columns",
            "description": """列出信望愛站可用的文章專欄。
            
回傳所有可搜尋的專欄，包含：
- 專欄代碼 (code): 用於 search_fhl_articles 的 column 參數
- 專欄名稱 (name): 中文名稱
- 專欄說明 (description): 專欄內容簡介

使用專欄代碼可以精確搜尋特定專欄的文章。
""",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]


async def handle_list_article_columns(
    endpoints: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[TextContent]:
    """Handle list_fhl_article_columns tool call"""
    
    columns = endpoints.list_article_columns()
    
    output = ["📋 信望愛站文章專欄列表\n"]
    output.append("=" * 60 + "\n")
    
    for col in columns:
        output.append(f"📌 {col['name']} ({col['code']})")
        output.append(f"   {col['description']}\n")
    
    output.append("=" * 60)
    output.append(f"\n💡 共 {len(columns)} 個專欄")
    output.append("\n💡 使用專欄代碼 (code) 進行搜尋，例如：")
    output.append("   search_fhl_articles(column='women3')")
    
    return [TextContent(type="text", text="\n".join(output))]
```

---

## 實施檢查清單

### Phase 3.1: 文章搜尋

- [ ] **API 端點層**
  - [ ] 在 `endpoints.py` 中添加 `search_articles()` 方法
  - [ ] 實現參數驗證（至少一個搜尋參數）
  - [ ] 實現客戶端結果限制
  - [ ] 添加快取支援（namespace: articles, strategy: search, 1 day TTL）
  - [ ] 添加完整的 docstring 和範例

- [ ] **工具層**
  - [ ] 創建 `tools/articles.py` 文件
  - [ ] 實現 `get_articles_tool_definitions()`
  - [ ] 實現 `handle_search_articles()` handler
  - [ ] 格式化輸出（標題、作者、摘要、內容預覽）
  - [ ] 添加友好的錯誤訊息

- [ ] **伺服器整合**
  - [ ] 在 `server.py` 中 import articles tools
  - [ ] 註冊 `search_fhl_articles` 工具
  - [ ] 添加 handler 路由
  - [ ] 更新工具計數日誌

### Phase 3.2: 專欄列表

- [ ] **API 端點層**
  - [ ] 在 `endpoints.py` 中添加 `list_article_columns()` 方法
  - [ ] 維護專欄資料清單
  - [ ] 添加 docstring

- [ ] **工具層**
  - [ ] 在 `get_articles_tool_definitions()` 中添加專欄列表工具
  - [ ] 實現 `handle_list_article_columns()` handler
  - [ ] 格式化專欄列表輸出

- [ ] **伺服器整合**
  - [ ] 註冊 `list_fhl_article_columns` 工具
  - [ ] 添加 handler 路由

### 測試

- [ ] **單元測試** (`tests/test_articles.py`)
  - [ ] 測試文章搜尋（標題、作者、內容）
  - [ ] 測試參數驗證（無參數時拋出錯誤）
  - [ ] 測試結果限制
  - [ ] 測試專欄列表查詢
  - [ ] 測試繁簡體切換

- [ ] **API 驗證測試** (`tests/api_validation/test_articles_api.py`)
  - [ ] 測試各種搜尋參數組合
  - [ ] 測試專欄過濾
  - [ ] 測試日期過濾
  - [ ] 測試大量結果處理

### 文檔

- [ ] **完成報告**
  - [ ] 創建 `PHASE_3_COMPLETION_REPORT.md`
  - [ ] 記錄實施過程
  - [ ] 記錄測試結果
  - [ ] 記錄已知限制

---

## 技術細節

### 快取策略

```python
# 文章搜尋
namespace = "articles"
strategy = "search"  # 1 day TTL
```

**理由**：
- 文章更新頻率：每週日更新
- 1 天 TTL 足夠，避免過期資料
- 不同搜尋條件有不同快取

### 錯誤處理

**無參數錯誤**：
```python
raise InvalidParameterError(
    "search_params",
    None,
    "Must provide at least one search parameter"
)
```

**API 錯誤**：
```json
{
  "status": 0,
  "result": "data too much 8021"
}
```

**沒有結果**：
```json
{
  "status": 0,
  "result": "no data"
}
```

### 結果限制

由於 API 沒有分頁機制，我們在客戶端實現結果限制：

```python
if len(data["record"]) > limit:
    data["record"] = data["record"][:limit]
    data["record_count"] = limit
    data["limited"] = True  # 標記為已限制
```

### HTML 內容處理

文章內容 (`txt` 欄位) 為 HTML 格式，包含：
- 圖片標籤：`<pic>filename.jpg</pic>`
- 換行：`<br/>`
- 其他 HTML 標籤

在預覽時簡單去除標籤：
```python
import re
clean_content = re.sub(r'<[^>]+>', '', content)
```

---

## 已知限制

### API 限制

1. **必須提供搜尋參數**
   - 無參數時返回 "data too much"
   - 必須至少提供一個條件

2. **無分頁機制**
   - 所有結果一次返回
   - 大量結果可能很慢
   - 使用客戶端限制緩解

3. **專欄清單無 API**
   - 需要手動維護專欄列表
   - 可能不完整或過期

### 功能限制

1. **內容為 HTML 格式**
   - 包含 HTML 標籤
   - 需要額外處理才能純文字顯示

2. **圖片僅文件名**
   - `<pic>` 標籤只有文件名
   - 需要拼接完整 URL

3. **無全文搜尋排序**
   - API 返回順序不明
   - 無法控制排序方式

---

## 預期成果

### 工具數量

實施完成後：
- 總工具數：25 → **27 functions**
- 新增：2 個文章相關工具
  - `search_fhl_articles`: 文章搜尋
  - `list_fhl_article_columns`: 專欄列表

### 使用場景

1. **主題研究**
   - 搜尋特定主題的文章
   - 找到相關作者和專欄

2. **作者追蹤**
   - 查找特定作者的所有文章
   - 了解作者的神學觀點

3. **專欄瀏覽**
   - 探索特定專欄的內容
   - 發現感興趣的主題

4. **時間查詢**
   - 查找特定日期的文章
   - 追蹤最新發表

---

**Phase 3 Status: 🔄 IN PROGRESS**

*文檔建立日期: 2025年11月4日*  
*預計完成時間: 6-8 小時*
