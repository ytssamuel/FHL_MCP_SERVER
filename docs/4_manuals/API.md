# FHL Bible MCP Server - API 完整文檔

本文檔詳細說明 FHL Bible MCP Server 提供的所有 **Tools**、**Resources** 和 **Prompts**。

## 目錄

- [Tools (工具)](#tools-工具)
  - [經文查詢工具](#經文查詢工具)
  - [搜尋工具](#搜尋工具)
  - [原文研究工具](#原文研究工具)
  - [註釋研經工具](#註釋研經工具)
  - [次經查詢工具](#次經查詢工具) ⭐ NEW
  - [使徒教父查詢工具](#使徒教父查詢工具) ⭐ NEW
  - [註腳查詢工具](#註腳查詢工具) ⭐ NEW
  - [文章搜尋工具](#文章搜尋工具) ⭐ NEW
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

> ✨ **v0.1.2 增強**: 支援多種輸入格式，包括 G/H 前綴、前導零、大小寫不敏感等。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `number` | string/integer | ✅ | - | Strong's 編號（支援多種格式，見下方說明） |
| `testament` | string | ❌ | - | 新舊約：NT/OT（使用 G/H 前綴時可省略） |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**支援的輸入格式**:

| 格式 | 範例 | 說明 | Testament 參數 |
|------|------|------|----------------|
| 整數 + testament | `3056, "NT"` | 傳統格式 | 必填 |
| 字串數字 + testament | `"3056", "NT"` | 字串格式 | 必填 |
| G 前綴（新約） | `"G3056"` | 自動識別新約 | 可省略 |
| H 前綴（舊約） | `"H430"` | 自動識別舊約 | 可省略 |
| 前導零 | `"G03056"` | 正確解析為 3056 | 依前綴 |
| 大小寫不敏感 | `"g3056"` | 等同 "G3056" | 依前綴 |

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
# 傳統格式（向後兼容）
查詢 Strong's 3056, 新約
lookup_strongs(3056, "NT")

# 新格式（推薦）
查詢 Strong's G3056 (λόγος, 道)
lookup_strongs("G3056")

查詢希伯來文 H430 (אֱלֹהִים, 神)
lookup_strongs("H430")

# 前導零格式
lookup_strongs("G03056")

# 大小寫不敏感
lookup_strongs("g3056")
```

---

#### `search_strongs_occurrences`

搜尋 Strong's 編號在聖經中的所有出現位置。

> ✨ **v0.1.2 增強**: 支援與 `lookup_strongs` 相同的多種輸入格式。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `number` | string/integer | ✅ | - | Strong's 編號（支援多種格式） |
| `testament` | string | ❌ | - | 新舊約：NT/OT（使用 G/H 前綴時可省略） |
| `limit` | integer | ❌ | 20 | 最多返回筆數 |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**返回結果**:

```json
{
  "strongs_info": {
    "strongs_number": "01344",
    "original_word": "δικαιόω",
    "chinese_definition": "稱義...",
    "testament": "NT"
  },
  "occurrences": {
    "total_count": 39,
    "showing": 5,
    "results": [
      {
        "book": "羅",
        "chapter": 3,
        "verse": 24,
        "text": "如今卻蒙神的恩典，因基督耶穌的救贖，就白白地稱義。"
      },
      {
        "book": "羅",
        "chapter": 5,
        "verse": 1,
        "text": "我們既因信稱義，就藉著我們的主耶穌基督得與神相和。"
      }
    ]
  }
}
```

**使用範例**:

```
# 傳統格式
搜尋 Strong's 1344 在新約中的出現位置
search_strongs_occurrences(1344, "NT", limit=5)

# 新格式（推薦）
搜尋 G1344 (δικαιόω, 稱義) 的所有出現
search_strongs_occurrences("G1344", limit=10)

搜尋 H430 (אֱלֹהִים, 神) 在舊約的出現
search_strongs_occurrences("H430", limit=20)
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

### 次經查詢工具

⭐ **NEW**: Phase 2.1 新增功能

次經（Apocrypha）是新舊約聖經之間的文獻，編號 101-115。

#### `get_apocrypha_verse`

查詢次經經文。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 書卷名稱（支援中文全名、縮寫、英文等多種格式） |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | string | ❌ | null | 節數（支援 "1", "1-5", "1,3,5" 等格式，若不提供則返回整章） |

**版本**: 使用 1933年聖公會出版 (c1933) 版本

**次經書卷列表**:

| ID | 英文名稱 | 中文名稱 | 別名 | 支援的縮寫/全名 |
|----|---------|---------|------|----------------|
| 101 | Tobit | 多俾亞傳 | - | '多', '多俾亞傳', 'Tob', 'Tobit' |
| 102 | Judith | 友弟德傳 | - | '友', '友弟德傳', 'Jdt', 'Judith' |
| 103 | 1 Maccabees | 瑪加伯上 | - | '加上', '瑪加伯上', '1Mac', '1 Maccabees' |
| 104 | 2 Maccabees | 瑪加伯下 | - | '加下', '瑪加伯下', '2Mac', '2 Maccabees' |
| 105 | Wisdom | 智慧篇 | - | '智', '智慧篇', 'Wis', 'Wisdom' |
| 106 | Sirach | 德訓篇 | 便西拉智訓 | '德', '德訓篇', '便西拉智訓', 'Sir', 'Sirach' |
| 107 | Baruch | 巴錄書 | - | '巴', '巴錄書', 'Bar', 'Baruch' |
| 108 | Letter of Jeremiah | 耶利米書信 | - | '耶信', '耶利米書信', 'EpJer' |
| 109 | Additions to Daniel | 但以理補篇 | - | '但補', '但以理補篇' |

**返回結果**:

```json
{
  "book_id": 103,
  "book_name": "Tobit",
  "book_name_chinese": "多俾亞傳",
  "chapter": 1,
  "verse": "1",
  "version": "unv",
  "verses": [
    {
      "verse": 1,
      "text": "多俾亞的事蹟..."
    }
  ]
}
```

**使用範例**:

```
查詢次經多俾亞傳 1:1
請給我所羅門智訓第 2 章
```

---

#### `get_apocrypha_chapter`

查詢次經整章。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book_id` | integer | ✅ | - | 次經書卷 ID (101-115) |
| `chapter` | integer | ✅ | - | 章數 |
| `version` | string | ❌ | "unv" | 版本代碼 |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**使用範例**:

```
請給我瑪加伯上第 1 章的完整內容
查詢便西拉智訓第 3 章
```

---

#### `search_apocrypha`

在次經中搜尋關鍵字。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜尋關鍵字 |
| `version` | string | ❌ | "unv" | 版本代碼 |
| `book_ids` | array | ❌ | null | 限制搜尋的書卷 ID |
| `limit` | integer | ❌ | 50 | 最多返回筆數 |

**返回結果**:

```json
{
  "keyword": "智慧",
  "total_count": 145,
  "results": [
    {
      "book_id": 106,
      "book_name": "Wisdom of Solomon",
      "chapter": 1,
      "verse": 4,
      "text": "智慧不會進入懷詐之心..."
    }
  ]
}
```

**使用範例**:

```
在次經中搜尋「智慧」
在瑪加伯書中搜尋「勇氣」
```

---

### 使徒教父查詢工具

⭐ **NEW**: Phase 2.2 新增功能

使徒教父（Apostolic Fathers）是早期基督教文獻，編號 201-217。

#### `get_apostolic_fathers_verse`

查詢使徒教父經文。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book_id` | integer | ✅ | - | 書卷 ID (201-217) |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | string | ❌ | null | 節數（支援範圍格式） |
| `version` | string | ❌ | "unv" | 版本代碼 |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**使徒教父書卷列表**:

| ID | 英文名稱 | 中文名稱 |
|----|---------|---------|
| 201 | 1 Clement | 革利免一書 |
| 202 | 2 Clement | 革利免二書 |
| 203 | Ignatius to the Ephesians | 伊格那丟致以弗所書 |
| 204 | Ignatius to the Magnesians | 伊格那丟致馬格尼西亞書 |
| 205 | Ignatius to the Trallians | 伊格那丟致特拉勒斯書 |
| 206 | Ignatius to the Romans | 伊格那丟致羅馬書 |
| 207 | Ignatius to the Philadelphians | 伊格那丟致非拉鐵非書 |
| 208 | Ignatius to the Smyrnaeans | 伊格那丟致士每拿書 |
| 209 | Ignatius to Polycarp | 伊格那丟致坡旅甲書 |
| 210 | Polycarp to the Philippians | 坡旅甲致腓立比書 |
| 211 | Martyrdom of Polycarp | 坡旅甲殉道記 |
| 212 | Didache | 十二使徒遺訓 |
| 213 | Barnabas | 巴拿巴書 |
| 214 | Shepherd of Hermas (Visions) | 黑馬牧人書（異象篇） |
| 215 | Shepherd of Hermas (Commands) | 黑馬牧人書（誡命篇） |
| 216 | Shepherd of Hermas (Similitudes) | 黑馬牧人書（比喻篇） |
| 217 | Diognetus | 致丟格那妥書 |

**使用範例**:

```
查詢革利免一書 1:1
請給我十二使徒遺訓第 1 章
```

---

#### `get_apostolic_fathers_chapter`

查詢使徒教父整章。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book_id` | integer | ✅ | - | 書卷 ID (201-217) |
| `chapter` | integer | ✅ | - | 章數 |
| `version` | string | ❌ | "unv" | 版本代碼 |
| `use_simplified` | boolean | ❌ | false | 是否使用簡體中文 |

**使用範例**:

```
請給我巴拿巴書第 1 章的完整內容
查詢坡旅甲殉道記第 1 章
```

---

#### `search_apostolic_fathers`

在使徒教父文獻中搜尋關鍵字。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜尋關鍵字 |
| `version` | string | ❌ | "unv" | 版本代碼 |
| `book_ids` | array | ❌ | null | 限制搜尋的書卷 ID |
| `limit` | integer | ❌ | 50 | 最多返回筆數 |

**使用範例**:

```
在使徒教父文獻中搜尋「信心」
在伊格那丟書信中搜尋「殉道」
```

---

### 註腳查詢工具

⭐ **NEW**: Phase 2.3 新增功能

查詢聖經經文的註腳資訊（目前僅支援 TCV 版本）。

#### `get_footnote`

查詢聖經註腳。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `book` | string | ✅ | - | 經卷名稱（中文或英文） |
| `chapter` | integer | ✅ | - | 章數 |
| `verse` | integer | ✅ | - | 節數 |
| `version` | string | ❌ | "tcv" | 版本代碼（目前僅支援 "tcv"） |

**返回結果**:

```json
{
  "book": "約",
  "chapter": 3,
  "verse": 16,
  "version": "tcv",
  "footnotes": [
    {
      "position": "a",
      "text": "「獨生子」或譯「獨一的兒子」。",
      "type": "translation_note"
    }
  ]
}
```

**使用範例**:

```
查詢約翰福音 3:16 的註腳
請給我馬太福音 5:1 的 TCV 註腳
```

**注意事項**:
- 目前僅支援 TCV（現代中文譯本）
- 不是所有經文都有註腳
- 註腳類型包括：翻譯說明、文本註解、背景資訊等

---

### 文章搜尋工具

⭐ **NEW**: Phase 3 新增功能

搜尋信望愛站的文章資源（8000+ 篇文章）。

#### `search_fhl_articles`

搜尋信望愛站文章。

**輸入參數**:

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `title` | string | ❌ | null | 標題關鍵字 |
| `author` | string | ❌ | null | 作者名稱 |
| `content` | string | ❌ | null | 內文關鍵字 |
| `abstract` | string | ❌ | null | 摘要關鍵字 |
| `column` | string | ❌ | null | 專欄代碼（見下表） |
| `pub_date` | string | ❌ | null | 發表日期 (YYYY.MM.DD) |
| `use_simplified` | boolean | ❌ | false | 使用簡體中文 |
| `limit` | integer | ❌ | 50 | 最多返回筆數 (上限 200) |

**專欄代碼**:

| 代碼 | 名稱 | 說明 |
|------|------|------|
| women3 | 麻辣姊妹 | 女性視角的信仰反思 |
| sunday | 主日學 | 主日學教材與教學資源 |
| youth | 青少年 | 青少年團契與輔導 |
| family | 家庭 | 家庭與婚姻議題 |
| theology | 神學 | 神學思考與討論 |
| bible_study | 查經 | 查經方法與材料 |
| devotion | 靈修 | 靈修分享與默想 |
| mission | 宣教 | 宣教與福音工作 |
| church | 教會 | 教會事工與牧養 |
| culture | 文化 | 文化與信仰對話 |
| history | 歷史 | 教會歷史與人物 |
| counseling | 輔導 | 心理輔導與關懷 |

**返回結果**:

```json
{
  "search_params": {
    "title": "愛",
    "column": "theology"
  },
  "total_count": 156,
  "returned_count": 50,
  "limited": false,
  "articles": [
    {
      "id": "8984",
      "title": "從何西阿三個孩子的名字看耶和華信實的愛",
      "author": "陳鳳翔",
      "column": "麻辣姊妹",
      "column_code": "women3",
      "pub_date": "2025.10.19",
      "abstract": "何西阿書是一卷充滿愛的書...",
      "content_preview": "何西阿書描述神對以色列的愛..."
    }
  ]
}
```

**使用範例**:

```
搜尋標題包含「愛」的文章
搜尋陳鳳翔寫的神學文章
查詢麻辣姊妹專欄中關於家庭的文章
搜尋 2025 年發表的靈修文章
```

**注意事項**:
- 至少需要提供一個搜尋參數
- 結果預設限制 50 筆，最多 200 筆
- 內容包含 HTML 標籤，預覽時會自動清理
- 搜尋採用關鍵字匹配（非全文搜尋）

---

#### `list_fhl_article_columns`

列出所有可用的文章專欄。

**輸入參數**: 無

**返回結果**:

```json
{
  "total_columns": 12,
  "columns": [
    {
      "code": "women3",
      "name": "麻辣姊妹",
      "description": "女性視角的信仰反思與生活應用"
    },
    {
      "code": "theology",
      "name": "神學",
      "description": "神學思考、教義探討與信仰反思"
    }
  ]
}
```

**使用範例**:

```
請列出所有文章專欄
有哪些文章類別可以搜尋？
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
