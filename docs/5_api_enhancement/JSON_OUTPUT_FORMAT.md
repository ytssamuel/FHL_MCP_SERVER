# 次經與使徒教父 API 輸出格式說明

## 📅 更新日期
2025年1月4日

## 📋 概述

次經 (Apocrypha) 和使徒教父 (Apostolic Fathers) 的所有 API 工具現在都使用 **結構化 JSON 格式** 輸出，取代原本的純文字格式。

## 🎯 為什麼使用 JSON 格式？

### 優點
✅ **結構化**: 資料有明確的欄位和階層  
✅ **易於解析**: 程式可以直接處理 JSON 資料  
✅ **類型安全**: 欄位類型明確（字串、數字、陣列等）  
✅ **可擴展**: 未來可以輕鬆新增欄位而不破壞相容性  
✅ **國際化**: 完美支援中文等 Unicode 字元  

## 📚 API 輸出格式

### 1. 查詢次經經文 (`get_apocrypha_verse`)

#### 輸入範例
```
請給我瑪加伯上第 1 章第 1-3 節
```

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "apocrypha_verse",
  "book": "瑪加伯上",
  "book_id": "103",
  "chapter": 1,
  "verse": "1-3",
  "version": {
    "code": "c1933",
    "name": "1933年聖公會出版"
  },
  "verse_count": 3,
  "verses": [
    {
      "book": "瑪加伯上",
      "book_id": "103",
      "chapter": 1,
      "verse": "1",
      "text": "腓力的兒子亞力山大是馬其頓人。他出離基庭境以後、戰勝了波斯和米太兩國的王大利烏、遂繼承了他的王位。"
    },
    {
      "book": "瑪加伯上",
      "book_id": "103",
      "chapter": 1,
      "verse": "2",
      "text": "他經歷了多次的戰爭、得了許多的堅壘、並殺了世上的許多君王。"
    },
    {
      "book": "瑪加伯上",
      "book_id": "103",
      "chapter": 1,
      "verse": "3",
      "text": "他到了世界邊疆、擄掠了許多國民、以致全地都在他面前無聲、他的心就驕傲自高了。"
    }
  ]
}
```

#### 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 查詢狀態：`"success"` 或 `"error"` |
| `query_type` | string | 查詢類型：`"apocrypha_verse"` |
| `book` | string | 書卷中文名稱（如「瑪加伯上」） |
| `book_id` | string | 書卷 ID（101-115） |
| `chapter` | integer | 章數 |
| `verse` | string\|null | 節數範圍（如 "1-3"），若查詢整章則為 null |
| `version` | object | 版本資訊 |
| `version.code` | string | 版本代碼（`"c1933"`） |
| `version.name` | string | 版本名稱 |
| `verse_count` | integer | 返回的經文數量 |
| `verses` | array | 經文陣列 |
| `verses[].book` | string | 書卷名稱 |
| `verses[].book_id` | string | 書卷 ID |
| `verses[].chapter` | integer | 章數 |
| `verses[].verse` | string | 節數 |
| `verses[].text` | string | 經文內容 |

---

### 2. 搜尋次經 (`search_apocrypha`)

#### 輸入範例
```
在次經中搜尋「信心」
```

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "apocrypha_search",
  "keyword": "信心",
  "total_count": 15,
  "returned_count": 10,
  "offset": 0,
  "results": [
    {
      "book": "瑪加伯上",
      "book_id": "103",
      "chapter": "2",
      "verse": "50",
      "text": "我的兒子們、你們要發出信心和熱誠、為律法爭戰、願意為他捨命。"
    },
    {
      "book": "德訓篇",
      "book_id": "106",
      "chapter": "32",
      "verse": "24",
      "text": "凡事依靠信心的人、必得幫助。遵守律法的、必得智慧。"
    }
  ]
}
```

#### 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 查詢狀態 |
| `query_type` | string | 查詢類型：`"apocrypha_search"` |
| `keyword` | string | 搜尋關鍵字 |
| `total_count` | integer | 總結果數 |
| `returned_count` | integer | 本次返回的結果數 |
| `offset` | integer | 分頁偏移量 |
| `results` | array | 搜尋結果陣列 |
| `results[].book` | string | 書卷名稱 |
| `results[].book_id` | string | 書卷 ID |
| `results[].chapter` | string | 章數 |
| `results[].verse` | string | 節數 |
| `results[].text` | string | 經文內容 |

---

### 3. 列出次經書卷 (`list_apocrypha_books`)

#### 輸入範例
```
列出所有次經書卷
```

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "list_apocrypha_books",
  "id_range": "101-115",
  "book_count": 9,
  "books": [
    {
      "id": 101,
      "name_zh": "多俾亞傳",
      "name_en": "Tobit",
      "abbreviations": ["多", "多俾亞傳", "Tob", "Tobit"]
    },
    {
      "id": 103,
      "name_zh": "瑪加伯上",
      "name_en": "1 Maccabees",
      "abbreviations": ["加上", "瑪加伯上", "1Mac", "1 Maccabees"]
    },
    {
      "id": 106,
      "name_zh": "德訓篇",
      "name_en": "Sirach",
      "abbreviations": ["德", "德訓篇", "便西拉智訓", "Sir", "Sirach"]
    }
  ]
}
```

#### 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 查詢狀態 |
| `query_type` | string | 查詢類型：`"list_apocrypha_books"` |
| `id_range` | string | 書卷 ID 範圍 |
| `book_count` | integer | 書卷總數 |
| `books` | array | 書卷列表 |
| `books[].id` | integer | 書卷 ID |
| `books[].name_zh` | string | 中文名稱 |
| `books[].name_en` | string | 英文名稱 |
| `books[].abbreviations` | array | 所有支援的縮寫和別名 |

---

### 4. 查詢使徒教父文獻 (`get_apostolic_fathers_verse`)

#### 輸入範例
```
查詢革利免前書第 1 章
```

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "apostolic_fathers_verse",
  "book": "革利免前書",
  "book_id": "201",
  "chapter": 1,
  "verse": null,
  "version": {
    "code": "afhuang",
    "name": "黃錫木主編《使徒教父著作》"
  },
  "verse_count": 58,
  "verses": [
    {
      "book": "革利免前書",
      "book_id": "201",
      "chapter": 1,
      "verse": "1",
      "text": "基督的教會，寄居在羅馬，寫信給基督的教會..."
    }
  ]
}
```

#### 欄位說明
同次經經文查詢，但 `query_type` 為 `"apostolic_fathers_verse"`。

---

### 5. 搜尋使徒教父文獻 (`search_apostolic_fathers`)

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "apostolic_fathers_search",
  "keyword": "愛心",
  "total_count": 25,
  "returned_count": 10,
  "offset": 0,
  "results": [...]
}
```

#### 欄位說明
同次經搜尋，但 `query_type` 為 `"apostolic_fathers_search"`。

---

### 6. 列出使徒教父書卷 (`list_apostolic_fathers_books`)

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "list_apostolic_fathers_books",
  "id_range": "201-217",
  "book_count": 8,
  "books": [
    {
      "id": 201,
      "name_zh": "革利免前書",
      "name_en": "1 Clement",
      "abbreviations": ["革", "革利免前書", "1Clem", "1 Clement"]
    }
  ]
}
```

#### 欄位說明
同次經書卷列表，但 `query_type` 為 `"list_apostolic_fathers_books"`。

---

## 🔄 與其他 API 的一致性

### 相同點
- 所有新的次經/使徒教父 API 都使用 JSON 格式
- 錯誤訊息仍然使用簡單文字格式（以 ❌ 開頭）

### 不同點
- **原有的聖經查詢 API** 仍使用原本的文字格式
- **次經/使徒教父 API** 使用新的 JSON 格式

這種設計是漸進式的，未來可以考慮將所有 API 統一為 JSON 格式。

---

## 💡 程式處理範例

### Python 範例

```python
import json

# 假設 response 是從 API 獲得的字串
# 移除 markdown code block 標記
json_str = response.strip().removeprefix("```json\n").removesuffix("\n```")

# 解析 JSON
data = json.loads(json_str)

# 存取資料
if data["status"] == "success":
    print(f"書卷: {data['book']}")
    print(f"經文數量: {data['verse_count']}")
    
    for verse in data["verses"]:
        print(f"{verse['book']} {verse['chapter']}:{verse['verse']}")
        print(f"  {verse['text']}")
```

### JavaScript 範例

```javascript
// 假設 response 是從 API 獲得的字串
const jsonStr = response
  .trim()
  .replace(/^```json\n/, '')
  .replace(/\n```$/, '');

// 解析 JSON
const data = JSON.parse(jsonStr);

// 存取資料
if (data.status === "success") {
  console.log(`書卷: ${data.book}`);
  console.log(`經文數量: ${data.verse_count}`);
  
  data.verses.forEach(verse => {
    console.log(`${verse.book} ${verse.chapter}:${verse.verse}`);
    console.log(`  ${verse.text}`);
  });
}
```

---

## 📝 注意事項

1. **Markdown Code Block**: JSON 輸出會包在 ` ```json ... ``` ` 標記中，方便在 Markdown 環境中顯示
2. **Unicode 支援**: 使用 `ensure_ascii=False` 確保中文正確顯示
3. **Pretty Print**: 使用 `indent=2` 讓 JSON 格式化，方便閱讀
4. **錯誤處理**: 查詢失敗時仍返回簡單的文字訊息（以 ❌ 開頭）

---

## 📰 文章 API (Articles)

### 1. 搜尋文章 (`search_fhl_articles`)

**⚠️ API 限制說明**：
FHL API **不支援**通過 ID 直接獲取文章。搜尋結果已包含完整內容，因此：
- 預設模式：返回內容預覽（約 200 字）
- 完整模式：設定 `include_content=true` 返回完整 HTML 內容

#### 輸入範例（預覽模式）
```
搜尋標題包含「愛」的文章
```

#### 輸出格式（預覽模式，`include_content=false`）
```json
{
  "status": "success",
  "query_type": "article_search",
  "total_count": 15,
  "returned_count": 10,
  "limited": false,
  "content_included": false,
  "articles": [
    {
      "id": "8984",
      "aid": "515",
      "title": "愛的真諦",
      "author": "張三",
      "column": {
        "name": "靈修",
        "code": "devotion"
      },
      "pub_date": "2025.01.01",
      "abstract": "探討哥林多前書13章中愛的本質...",
      "content_preview": "愛是恆久忍耐，又有恩慈；愛是不嫉妒..."
    }
  ]
}
```

#### 輸出格式（完整模式，`include_content=true`）
```json
{
  "status": "success",
  "query_type": "article_search",
  "total_count": 15,
  "returned_count": 10,
  "limited": false,
  "content_included": true,
  "articles": [
    {
      "id": "8984",
      "aid": "515",
      "title": "愛的真諦",
      "author": "張三",
      "column": {
        "name": "靈修",
        "code": "devotion"
      },
      "pub_date": "2025.01.01",
      "abstract": "探討哥林多前書13章中愛的本質...",
      "content": "<p>愛是恆久忍耐，又有恩慈...<br/>完整的 HTML 內容...</p><pic>image.jpg</pic>",
      "content_format": "HTML"
    }
  ]
}
```

#### 欄位說明
| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 狀態：`success` 或 `no_results` |
| `query_type` | string | 查詢類型：`article_search` |
| `total_count` | integer | 找到的文章總數 |
| `returned_count` | integer | 實際返回的文章數 |
| `limited` | boolean | 是否因 limit 限制而截斷結果 |
| `content_included` | boolean | 是否包含完整內容 |
| `articles` | array | 文章列表 |
| `articles[].id` | string | 文章 ID |
| `articles[].aid` | string | 文章 AID |
| `articles[].title` | string | 文章標題 |
| `articles[].author` | string | 作者名稱 |
| `articles[].column.name` | string | 專欄名稱（中文） |
| `articles[].column.code` | string | 專欄代碼（英文） |
| `articles[].pub_date` | string | 發表日期（格式：YYYY.MM.DD） |
| `articles[].abstract` | string | 文章摘要 |
| `articles[].content_preview` | string | 內容預覽（約 200 字，當 `content_included=false`） |
| `articles[].content` | string | 完整 HTML 內容（當 `content_included=true`） |
| `articles[].content_format` | string | 內容格式：`HTML`（當 `content_included=true`） |

**使用建議**：
1. **快速瀏覽**：使用預設模式（`include_content=false`）快速查看文章列表
2. **詳細閱讀**：設定 `include_content=true` 獲取完整內容
3. **節省頻寬**：僅在需要完整內容時才設定 `include_content=true`

**HTML 標籤說明**（完整模式）：
- `<pic>filename.jpg</pic>` - 圖片檔案名稱
- `<br/>` - 換行
- `<a href='...'>` - 超連結
- 其他標準 HTML 標籤

---

### 2. 列出文章專欄 (`list_fhl_article_columns`)

#### 輸入範例
```
列出所有可用的文章專欄
```

#### 輸出格式
```json
{
  "status": "success",
  "query_type": "list_article_columns",
  "column_count": 12,
  "columns": [
    {
      "code": "women3",
      "name": "麻辣姊妹",
      "description": "女性信仰生活分享"
    },
    {
      "code": "theology",
      "name": "神學",
      "description": "神學探討與研究"
    }
  ]
}
```

#### 欄位說明
| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 狀態：`success` |
| `query_type` | string | 查詢類型：`list_article_columns` |
| `column_count` | integer | 專欄總數 |
| `columns` | array | 專欄列表 |
| `columns[].code` | string | 專欄代碼（用於搜尋） |
| `columns[].name` | string | 專欄名稱（中文） |
| `columns[].description` | string | 專欄說明 |

---

## 🎯 未來改進方向

1. **統一所有 API 格式**: 將所有聖經查詢 API 也改為 JSON 格式
2. **版本控制**: 在 JSON 中加入 `api_version` 欄位
3. **分頁資訊**: 在搜尋結果中加入 `has_more`, `next_offset` 等分頁資訊
4. **元數據**: 加入查詢時間戳、快取狀態等元數據
5. **文章內容解析**: 提供純文字版本選項（自動移除 HTML 標籤）
6. **API 增強**: 如 FHL API 未來支援通過 ID 直接獲取文章，則恢復 `get_fhl_article_content` 工具

---

## 📌 已知 API 限制

### 文章 API
- **不支援通過 ID 獲取**：FHL API 無法通過文章 ID/AID 直接獲取單篇文章
- **解決方案**：`search_articles` API 返回的結果已包含完整內容（`txt` 欄位）
- **建議做法**：使用 `include_content` 參數控制是否返回完整內容

---

**更新者**: GitHub Copilot  
**審核者**: 用戶確認  
**狀態**: ✅ 已實施（2025年1月4日更新：文章 API 改為可選完整內容）
