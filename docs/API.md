# FHL Bible MCP Server - API 完整文檔

本文檔詳細說明 FHL Bible MCP Server 提供的所有 **Tools**、**Resources** 和 **Prompts**。

## 目錄

- [Tools (工具)](#tools-工具)
  - [經文查詢工具](#經文查詢工具)
  - [搜尋工具](#搜尋工具)
  - [原文研究工具](#原文研究工具)
  - [註釋研經工具](#註釋研經工具)
  - [資訊查詢工具](#資訊查詢工具)
  - [多媒體工具](#多媒體工具)
- [Resources (資源)](#resources-資源)
  - [Bible Resources](#bible-resources)
  - [Strong's Resources](#strongs-resources)
  - [Commentary Resources](#commentary-resources)
  - [Info Resources](#info-resources)
- [Prompts (提示範本)](#prompts-提示範本)

---

## Tools (工具)

Tools 是可執行的動作，允許 AI 主動呼叫 API 完成各種聖經研究任務。

### 經文查詢工具

#### `get_bible_verse`

查詢指定章節的聖經經文。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷名稱（中文或英文，如 "約" 或 "John"） |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | string | ❌ | null | 節數（支援 "1", "1-5", "1,3,5" 等格式） |
| `version` | string | ❌ | "unv" | 聖經版本代碼 |
| `include_strong` | boolean | ❌ | false | 是否包含 Strong's Number |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**返回結果**:

```json
{
  "version": "unv",
  "version_name": "FHL和合本",
  "record_count": 1,
  "verses": [
    {
      "book": "約",
      "book_eng": "John",
      "chapter": 3,
      "verse": 16,
      "text": "「　神愛世人，甚至將他的獨生子賜給他們..."
    }
  ],
  "navigation": {
    "prev": {"book": "約", "chapter": 3, "verse": 15},
    "next": {"book": "約", "chapter": 3, "verse": 17}
  }
}
```

**使用範例**:

```
請查詢約翰福音 3:16
請查詢羅馬書 8:28-30，包含 Strong's Number
```

---

#### `get_bible_chapter`

查詢整章聖經經文。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷名稱 |
| `chapter` | integer | ✅ | - | 章數 |
| `version` | string | ❌ | "unv" | 聖經版本代碼 |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**返回結果**:

```json
{
  "version": "unv",
  "version_name": "FHL和合本",
  "book": "約",
  "book_eng": "John",
  "chapter": 3,
  "verse_count": 36,
  "verses": [
    {"verse": 1, "text": "有一個法利賽人..."},
    {"verse": 2, "text": "這人夜裡來見耶穌..."}
  ]
}
```

**使用範例**:

```
請給我約翰福音第 3 章的完整內容
查詢創世記第 1 章
```

---

#### `query_verse_citation`

使用經文引用格式查詢（支援複雜引用）。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `citation` | string | ✅ | - | 經文引用（如 "太 10:1-3", "約 3:16"） |
| `version` | string | ❌ | "unv" | 聖經版本代碼 |
| `include_strong` | boolean | ❌ | false | 是否包含 Strong's Number |

**返回結果**:

```json
{
  "citation": "太 10:1-3",
  "version": "unv",
  "verses": [...]
}
```

**使用範例**:

```
請查詢 "太 5:1-12"
查詢 "創 1:1-5; 約 1:1"
```

---

### 搜尋工具

#### `search_bible`

在聖經中搜尋關鍵字。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜尋關鍵字 |
| `version` | string | ❌ | "unv" | 聖經版本代碼 |
| `scope` | string | ❌ | "all" | 搜尋範圍：all/ot/nt |
| `limit` | integer | ❌ | 50 | 最多返回筆數 |
| `offset` | integer | ❌ | 0 | 跳過筆數（分頁） |

**返回結果**:

```json
{
  "keyword": "愛",
  "total_count": 523,
  "returned_count": 50,
  "results": [
    {
      "book": "創",
      "book_eng": "Gen",
      "chapter": 22,
      "verse": 2,
      "text": "神說：「你帶著你的兒子，就是你獨生的兒子，你所愛的以撒...",
      "id": 559
    }
  ]
}
```

**使用範例**:

```
搜尋聖經中所有提到「愛」的經文
在新約中搜尋「信心」
```

---

#### `search_bible_advanced`

進階聖經搜尋（支援原文編號搜尋）。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜尋內容 |
| `search_type` | string | ✅ | - | 搜尋類型：keyword/greek_number/hebrew_number |
| `version` | string | ❌ | "unv" | 聖經版本代碼 |
| `scope` | string | ❌ | "all" | 搜尋範圍：all/ot/nt/range |
| `range_start` | integer | ❌ | null | 範圍起始經卷編號 (1-66) |
| `range_end` | integer | ❌ | null | 範圍結束經卷編號 (1-66) |
| `limit` | integer | ❌ | 50 | 最多返回筆數 |

**使用範例**:

```
使用希臘文編號 G25 (agapao) 搜尋所有相關經文
搜尋希伯來文編號 H3068 (YHWH) 在舊約中的出現
```

---

### 原文研究工具

#### `get_word_analysis`

取得經文的原文字彙分析。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷英文縮寫（如 "John"） |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | integer | ✅ | - | 節數 |

**返回結果**:

```json
{
  "testament": "NT",
  "book": "John",
  "chapter": 3,
  "verse": 16,
  "original_text": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...",
  "literal_translation": "如此 因為 愛了 這 神 這 世界...",
  "words": [
    {
      "position": 3,
      "word": "ἠγάπησεν",
      "strongs_number": "00025",
      "part_of_speech": "動詞",
      "morphology": "第一簡單過去 主動 直說語氣 第三人稱 單數",
      "lemma": "ἀγαπάω",
      "gloss": "愛",
      "remark": ""
    }
  ]
}
```

**使用範例**:

```
請分析約翰福音 3:16 的希臘文原文
分析創世記 1:1 的希伯來文
```

---

#### `lookup_strongs`

查詢 Strong's 原文字典。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `strongs_number` | string | ✅ | - | Strong's 編號（如 "25" 或 "G25"） |
| `testament` | string | ✅ | - | 新舊約：NT/OT |

**返回結果**:

```json
{
  "strongs_number": "00025",
  "original_word": "ἀγαπάω",
  "chinese_definition": "25 agapao {ag-ap-ah'-o}\n\n可能源自 agan (多)...",
  "english_definition": "25 agapao {ag-ap-ah'-o}\n\nperhaps from agan...",
  "related_words": [
    {
      "word": "ἀγαπάω",
      "number": "00025",
      "occurrences": 143,
      "gloss": "愛；表明或證明一個人的愛；渴望"
    },
    {
      "word": "ἀγάπη",
      "number": "00026",
      "occurrences": 116,
      "gloss": "愛；早期教會信徒一同分享的愛餐"
    }
  ]
}
```

**使用範例**:

```
查詢 Strong's G25 (agapao)
查詢希伯來文編號 H3068
```

---

#### `search_strongs_occurrences`

搜尋 Strong's 編號在聖經中的所有出現位置。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `strongs_number` | string | ✅ | - | Strong's 編號 |
| `testament` | string | ✅ | - | 新舊約：NT/OT |
| `limit` | integer | ❌ | 50 | 最多返回筆數 |

**返回結果**:

```json
{
  "strongs_number": "00025",
  "testament": "NT",
  "total_occurrences": 143,
  "results": [
    {
      "book": "太",
      "chapter": 5,
      "verse": 43,
      "text": "你們聽見有話說：「當愛你的鄰舍，恨你的仇敵。」"
    }
  ]
}
```

---

### 註釋研經工具

#### `get_commentary`

取得聖經註釋。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷英文縮寫 |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | integer | ✅ | - | 節數 |
| `commentary_ids` | array | ❌ | null | 註釋書 ID 陣列（不指定則返回所有） |

**返回結果**:

```json
{
  "book": "John",
  "chapter": 3,
  "verse": 16,
  "commentaries": [
    {
      "id": 1,
      "name": "CBOL加插註釋",
      "title": "約翰福音 3:16",
      "content": "神愛世人的愛是犧牲的愛..."
    }
  ]
}
```

**使用範例**:

```
查詢約翰福音 3:16 的註釋
查詢羅馬書 8:28 的 CBOL 註釋
```

---

#### `list_commentaries`

列出所有可用的註釋書。

**輸入參數**: 無

**返回結果**:

```json
{
  "commentaries": [
    {"id": 1, "name": "CBOL加插註釋"},
    {"id": 2, "name": "parsing 註釋"},
    {"id": 3, "name": "信望愛站註釋"},
    {"id": 4, "name": "串珠"},
    {"id": 8, "name": "蔡茂堂牧師講道"},
    {"id": 9, "name": "盧俊義牧師講道"},
    {"id": 10, "name": "康來昌牧師講道"}
  ]
}
```

---

#### `search_commentary`

在註釋書中搜尋關鍵字。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜尋關鍵字 |
| `commentary_ids` | array | ❌ | null | 註釋書 ID 陣列 |

**返回結果**:

```json
{
  "keyword": "救恩",
  "results": [
    {
      "commentary_id": 1,
      "commentary_name": "CBOL加插註釋",
      "title": "約翰福音 3:16-21",
      "book": "約",
      "chapter_start": 3,
      "verse_start": 16
    }
  ]
}
```

---

#### `get_topic_study`

查詢主題查經資料。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 主題關鍵字 |
| `source` | string | ❌ | "all" | 資料來源：torrey_en/naves_en/torrey_zh/naves_zh/all |
| `limit` | integer | ❌ | 20 | 最多返回筆數 |

**返回結果**:

```json
{
  "keyword": "love",
  "total_count": 15,
  "results": [
    {
      "source": "torrey_zh",
      "topic": "愛 - 神的愛",
      "content": "是永恆的 耶31:3\n是豐盛的 弗2:4\n..."
    }
  ]
}
```

**使用範例**:

```
查詢主題：愛
搜尋 Torrey 主題查經中關於「信心」的資料
```

---

### 資訊查詢工具

#### `list_bible_versions`

列出所有可用的聖經版本。

**輸入參數**: 無

**返回結果**:

```json
{
  "total_count": 84,
  "versions": [
    {
      "code": "unv",
      "name": "FHL和合本",
      "has_strongs": true,
      "testament": "both",
      "special_font": "none",
      "can_download": true,
      "last_updated": "2024-01-15"
    }
  ]
}
```

---

#### `get_book_list`

取得聖經書卷列表。

**輸入參數**: 無

**返回結果**:

```json
{
  "total_books": 66,
  "old_testament": [
    {
      "id": 1,
      "english_short": "Gen",
      "english_full": "Genesis",
      "chinese_short": "創",
      "chinese_full": "創世記"
    }
  ],
  "new_testament": [
    {
      "id": 40,
      "english_short": "Matt",
      "english_full": "Matthew",
      "chinese_short": "太",
      "chinese_full": "馬太福音"
    }
  ]
}
```

---

#### `get_book_info`

取得特定書卷的詳細資訊。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷名稱（中英文皆可） |

**返回結果**:

```json
{
  "id": 43,
  "english_short": "John",
  "english_full": "John",
  "chinese_short": "約",
  "chinese_full": "約翰福音",
  "testament": "NT",
  "category": "Gospel",
  "chapters": 21
}
```

---

#### `search_available_versions`

搜尋可用的聖經版本。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜尋關鍵字 |
| `has_strongs` | boolean | ❌ | null | 篩選有 Strong's Number 的版本 |
| `testament` | string | ❌ | null | 篩選新舊約：ot/nt/both |

**使用範例**:

```
搜尋所有包含 Strong's Number 的英文版本
找出所有台語聖經版本
```

---

### 多媒體工具

#### `get_audio_bible`

取得有聲聖經連結。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book_id` | integer | ✅ | - | 經卷編號 (1-66) |
| `chapter` | integer | ✅ | - | 章數 |
| `audio_version` | integer | ❌ | 0 | 音訊版本（0=和合本，1=台語，等） |

**返回結果**:

```json
{
  "version_name": "和合本",
  "book": "約",
  "book_eng": "John",
  "chapter": 3,
  "audio_files": {
    "mp3": "https://bible.fhl.net/audio/...",
    "ogg": "https://bible.fhl.net/audio/..."
  },
  "navigation": {
    "prev": {"book_id": 43, "chapter": 2},
    "next": {"book_id": 43, "chapter": 4}
  }
}
```

**音訊版本代碼**:

| 代碼 | 名稱 |
|------|------|
| 0 | 和合本 |
| 1 | 台語 |
| 2 | 客家話 |
| 3 | 廣東話 |
| 4 | 現代中文譯本 |
| 7 | 希伯來文 |
| 9 | 希臘文 |

---

## Resources (資源)

Resources 提供靜態或動態資料供 AI 讀取，使用 URI 格式存取。

### Bible Resources

#### `bible://verse/{version}/{book}/{chapter}/{verse}`

取得特定經文。

**範例**:
- `bible://verse/unv/John/3/16`
- `bible://verse/kjv/Gen/1/1-5`

**返回格式**: 與 `get_bible_verse` 工具相同

---

#### `bible://chapter/{version}/{book}/{chapter}`

取得整章經文。

**範例**:
- `bible://chapter/unv/John/3`
- `bible://chapter/niv/Rom/8`

**返回格式**: 與 `get_bible_chapter` 工具相同

---

### Strong's Resources

#### `strongs://{testament}/{number}`

Strong's 字典資源。

**範例**:
- `strongs://nt/25` (希臘文 agapao)
- `strongs://ot/3068` (希伯來文 YHWH)

**返回格式**: 與 `lookup_strongs` 工具相同

---

### Commentary Resources

#### `commentary://{book}/{chapter}/{verse}`

經文註釋資源。

**範例**:
- `commentary://John/3/16`
- `commentary://Rom/8/28`

**返回格式**: 與 `get_commentary` 工具相同

---

### Info Resources

#### `info://versions`

聖經版本列表。

**返回格式**: 與 `list_bible_versions` 工具相同

---

#### `info://books`

書卷列表。

**返回格式**: 與 `get_book_list` 工具相同

---

#### `info://commentaries`

註釋書列表。

**返回格式**: 與 `list_commentaries` 工具相同

---

## Prompts (提示範本)

Prompts 提供預設的對話範本，幫助使用者快速開始聖經研讀。

### `study_verse`

深入研讀經文。

**描述**: 深入研讀一節經文，包含經文內容、原文分析、註釋等。

**參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `book` | string | ✅ | 經卷名稱（中英文皆可） |
| `chapter` | integer | ✅ | 章數 |
| `verse` | integer | ✅ | 節數 |
| `version` | string | ❌ | 聖經版本代碼（預設 unv） |

**範本內容**:

```
請幫我深入研讀 {book} {chapter}:{verse}。

請按照以下步驟進行研讀：

1. **經文內容**
   - 查詢經文內容（{version} 版本）
   - 同時獲取包含 Strong's Number 的版本

2. **原文字彙分析**
   - 取得該節經文的希臘文/希伯來文分析
   - 列出每個重要字詞的原文、詞性、字型變化

3. **關鍵字詞研究**
   - 針對經文中的關鍵字，查詢 Strong's 字典
   - 解釋重要字詞的原文意義、用法、神學含義

4. **註釋研經**
   - 查詢相關註釋書的解經
   - 綜合各家註釋的觀點

5. **相關經文**
   - 使用串珠或搜尋功能找出相關經文
   - 比較相關經文的上下文

6. **總結應用**
   - 總結該節經文的核心信息
   - 提供實際生活應用建議
```

**使用範例**:

```
請幫我研讀約翰福音 3:16
使用 study_verse prompt 研讀羅馬書 8:28
```

---

### `search_topic`

主題研究。

**描述**: 研究聖經中的特定主題，包含經文搜尋、主題查經、註釋等。

**參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `topic` | string | ✅ | 主題關鍵字 |
| `version` | string | ❌ | 聖經版本代碼（預設 unv） |

**範本內容**:

```
請幫我研究聖經中關於「{topic}」的教導。

請按照以下步驟進行研究：

1. **經文搜尋**
   - 在聖經中搜尋包含「{topic}」的經文
   - 列出最重要的 10-15 節經文

2. **主題查經**
   - 查詢 Torrey 和 Naves 主題查經中關於「{topic}」的資料
   - 整理主題的分類與架構

3. **原文研究**（如適用）
   - 查找與「{topic}」相關的希臘文/希伯來文字詞
   - 分析原文字義的豐富內涵

4. **註釋整理**
   - 搜尋註釋書中關於「{topic}」的討論
   - 綜合不同註釋的觀點

5. **綜合分析**
   - 總結聖經對「{topic}」的整體教導
   - 分析舊約與新約的連貫性
   - 提煉核心原則

6. **實際應用**
   - 提供實際生活應用建議
   - 給出具體的行動步驟
```

**使用範例**:

```
請研究聖經中關於「愛」的教導
使用 search_topic prompt 研究「信心」
```

---

### `compare_translations`

版本比較。

**描述**: 比較不同聖經譯本的翻譯差異。

**參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `book` | string | ✅ | 經卷名稱 |
| `chapter` | integer | ✅ | 章數 |
| `verse` | integer | ✅ | 節數 |
| `versions` | string | ❌ | 版本代碼列表（逗號分隔，預設 "unv,kjv,niv"） |

**範本內容**:

```
請幫我比較 {book} {chapter}:{verse} 在不同譯本中的翻譯。

請比較以下版本：{versions}

請按照以下步驟進行比較：

1. **列出各譯本經文**
   - 查詢並列出各譯本的經文內容
   - 標明版本名稱與特色

2. **翻譯差異分析**
   - 指出主要的翻譯差異
   - 分析造成差異的可能原因（原文、神學、語境等）

3. **原文分析**
   - 查看希臘文/希伯來文原文
   - 分析原文字詞的多重意義
   - 說明各譯本選擇的依據

4. **上下文考量**
   - 分析經文的上下文
   - 說明不同翻譯如何影響理解

5. **推薦翻譯**
   - 根據原文與上下文，推薦最貼切的翻譯
   - 說明推薦理由
```

**使用範例**:

```
比較約翰福音 3:16 在和合本、KJV 和 NIV 中的翻譯
使用 compare_translations prompt 比較羅馬書 8:28
```

---

### `word_study`

原文字詞研究。

**描述**: 深入研究希臘文或希伯來文單字。

**參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `strongs_number` | string | ✅ | Strong's 編號 |
| `testament` | string | ✅ | 新舊約：NT/OT |
| `example_verses` | integer | ❌ | 範例經文數量（預設 10） |

**範本內容**:

```
請幫我研究 Strong's #{strongs_number} ({testament}) 這個原文字。

請按照以下步驟進行研究：

1. **字典定義**
   - 查詢 Strong's 字典的中英文定義
   - 列出原文拼寫與發音
   - 說明字根與構詞

2. **字義範圍**
   - 分析該字的基本意義
   - 列出延伸意義與比喻用法
   - 說明在不同語境中的變化

3. **聖經出現位置**
   - 搜尋該字在聖經中的所有出現（前 {example_verses} 處）
   - 為每處出現提供經文與簡短說明
   - 分析使用頻率與分布

4. **語境分析**
   - 選擇 3-5 個代表性經文深入分析
   - 說明該字在不同語境中的具體意義
   - 比較新舊約用法的異同（如適用）

5. **同源字研究**
   - 列出相關的同源字
   - 說明字義之間的關聯與差異
   - 分析同源字的使用模式

6. **神學意義**
   - 總結該字的神學重要性
   - 說明對理解聖經神學的貢獻
   - 提供解經應用建議
```

**使用範例**:

```
請研究 Strong's G25 (agapao - 愛)
使用 word_study prompt 研究希伯來文 H3068 (YHWH)
```

---

## 常用聖經版本代碼

| 代碼 | 名稱 | Strong's | 語言 |
|------|------|----------|------|
| `unv` | FHL和合本 | ✅ | 繁體中文 |
| `nstrunv` | 新標點和合本 | ✅ | 繁體中文 |
| `kjv` | King James Version | ✅ | 英文 |
| `niv` | New International Version | ❌ | 英文 |
| `tcv` | 現代中文譯本 | ❌ | 繁體中文 |
| `spring` | 呂振中譯本 | ❌ | 繁體中文 |
| `tclv` | 台語白話字聖經 | ❌ | 台語 |

完整版本列表請使用 `list_bible_versions` 工具查詢。

---

## 錯誤處理

所有 Tools 在遇到錯誤時會返回標準錯誤格式：

```json
{
  "error": "BookNotFoundError",
  "message": "找不到書卷: XYZ",
  "details": {
    "book": "XYZ",
    "suggestions": ["約", "John", "約翰福音"]
  }
}
```

常見錯誤類型：

- `BookNotFoundError`: 找不到指定的書卷
- `InvalidParameterError`: 參數格式錯誤
- `APIResponseError`: API 返回錯誤
- `NetworkError`: 網路連接錯誤
- `RateLimitError`: 請求頻率超過限制

---

## 使用建議

1. **書卷名稱**: 支援中文（創、太）、英文縮寫（Gen、Matt）、英文全名（Genesis、Matthew）
2. **經文範圍**: 使用 `verse` 參數支援多種格式：
   - 單節: `"16"`
   - 範圍: `"16-18"`
   - 多節: `"16,18,20"`
   - 混合: `"16-18,20,22-24"`
3. **分頁查詢**: 使用 `limit` 和 `offset` 參數進行分頁
4. **快取機制**: 常用資料（版本列表、書卷列表）會自動快取
5. **錯誤重試**: 網路錯誤會自動重試 3 次

---

## 版權聲明

本 MCP Server 使用信望愛站（FHL）提供的聖經 API。請注意：

- 聖經譯本版權歸屬於各譯本的版權方
- 本 Server 僅作為 API 介面層，不儲存或重新分發經文內容
- 使用者應遵守各譯本的版權規定
- 詳見 [信望愛站版權說明](https://www.fhl.net/main/fhl/fhl8.html)

---

**完整範例請參考 [EXAMPLES.md](EXAMPLES.md)**
