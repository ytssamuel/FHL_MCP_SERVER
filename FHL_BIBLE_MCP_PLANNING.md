# FHL 聖經 API MCP Server 規劃文件

**專案名稱**: FHL Bible MCP Server  
**API 來源**: https://bible.fhl.net/json/  
**開發語言**: Python  
**日期**: 2025年10月31日  
**版本**: 1.0

---

## 目錄

1. [專案概述](#專案概述)
2. [API 分析](#api-分析)
3. [API 測試結果](#api-測試結果)
4. [MCP Server 架構設計](#mcp-server-架構設計)
5. [實作計劃](#實作計劃)
6. [版權注意事項](#版權注意事項)

---

## 專案概述

### 目標
開發一個基於 Model Context Protocol (MCP) 的 Server，整合信望愛站（Faith, Hope, Love, FHL）提供的聖經 JSON API，讓 AI 助手能夠查詢聖經經文、註釋、字彙分析等豐富的聖經資源。

### 特色
- 支援多種聖經譯本（和合本、KJV、現代中文譯本等）
- 提供原文字彙分析（希臘文、希伯來文）
- 支援經文搜尋、主題查經
- 提供註釋書與研經資源
- 支援次經和使徒教父文獻
- 多語言支援（繁體/簡體中文切換）

---

## API 分析

### API 基本資訊

**Base URL**: `https://bible.fhl.net/json/`  
**回應格式**: JSON  
**編碼**: UTF-8  
**通用參數**: 
- `gb`: 繁簡體選擇 (0=繁體, 1=簡體)

### API 端點分類

#### 1. 基礎資訊類 API

##### 1.1 ab.php - 聖經版本列表
- **用途**: 列出所有可用的聖經版本
- **參數**: 無
- **回應欄位**:
  - `book`: 版本縮寫
  - `cname`: 版本名稱
  - `proc`: 特殊字型需求 (0=無, 1=希臘文, 2=希伯來文, 3=羅馬拼音, 4=Open Han)
  - `strong`: 是否有 Strong's Number
  - `ntonly/otonly`: 是否僅限新約/舊約
  - `candownload`: 是否可下載離線資料
  - `version`: 資料庫更新時間

##### 1.2 abv.php - 離線資料狀況
- **用途**: 列出可供下載的離線聖經資料
- **參數**: `gb`

##### 1.3 listall.html - 書卷列表
- **用途**: 列出聖經書卷基本資料
- **格式**: CSV
- **輸出**: 編號,英文簡寫,英文全名,中文簡寫,英文短簡寫

#### 2. 經文查詢類 API

##### 2.1 qb.php - 查詢聖經經文（正典）
- **用途**: 查詢指定章節的聖經經文
- **參數**:
  - `chineses`: 中文經卷縮寫 (default: 羅)
  - `chap`: 章 (default: 1)
  - `sec`: 節，支援格式: "1", "1-5", "1,5,6", "1-2,5,8-10"
  - `version`: 聖經版本 (default: nstrunv)
  - `strong`: 是否包含 Strong's Number (0/1)
  - `gb`: 繁簡體選擇
- **回應**:
  - `status`: 成功與否
  - `record_count`: 資料筆數
  - `proc`: 特殊字型需求
  - `version`: 版本簡寫
  - `v_name`: 版本名稱
  - `prev/next`: 前後節資訊
  - `record[]`: 經文陣列
    - `engs`: 英文縮寫
    - `chineses`: 中文縮寫
    - `chap`: 章
    - `sec`: 節
    - `bible_text`: 經文內容

##### 2.2 qsub.php - 查詢次經
- **用途**: 查詢次經經文
- **參數**: 同 qb.php
- **經卷範圍**: 101-115

##### 2.3 qaf.php - 查詢使徒教父文獻
- **用途**: 查詢使徒教父著作
- **參數**: 同 qb.php
- **經卷範圍**: 201-217

##### 2.4 qsb.php - 經文引用查詢
- **用途**: 支援複雜的經文引用格式查詢
- **參數**:
  - `version`: 聖經版本
  - `engs`: 書卷簡寫
  - `qstr`: 引用字串 (如: "太 10:1-3")
  - `strong`: Strong's Number
  - `gb`: 繁簡體

##### 2.5 rt.php - 經文註腳
- **用途**: 查詢聖經經文的註腳
- **參數**:
  - `engs`: 英文經卷縮寫
  - `id`: 註腳編號
  - `chap`: 章
  - `version`: 版本
  - `gb`: 繁簡體
- **回應**: XML 格式
  - `id`: 註腳編號
  - `text`: 註腳內容

#### 3. 搜尋類 API

##### 3.1 se.php - 經文關鍵字搜尋（正典）
- **用途**: 在聖經中搜尋關鍵字或原文編號
- **參數**:
  - `VERSION`: 聖經版本 (default: unv)
  - `orig`: 查詢形式 (0=關鍵字, 1=希臘文編號, 2=希伯來文編號)
  - `q`: 查詢內容
  - `RANGE`: 查詢範圍 (0=全部, 1=新約, 2=舊約, 3=指定範圍)
  - `range_bid/range_eid`: 範圍起始/結束經卷編號 (1-66)
  - `limit`: 最多顯示筆數
  - `offset`: 跳過筆數
  - `gb`: 繁簡體
  - `count_only`: 是否只輸出筆數 (0/1)
  - `index_only`: 是否只輸出經卷不含內容 (0/1)
- **回應**:
  - `record_count`: 結果筆數
  - `orig`: 查詢形式
  - `key`: 查詢字串
  - `record[]`: 搜尋結果

##### 3.2 sesub.php - 次經搜尋
- **用途**: 在次經中搜尋
- **參數**: 同 se.php
- **經卷範圍**: 101-115

##### 3.3 seaf.php - 使徒教父搜尋
- **用途**: 在使徒教父文獻中搜尋
- **參數**: 同 se.php
- **經卷範圍**: 201-217

#### 4. 字彙分析類 API

##### 4.1 qp.php - 字彙分析
- **用途**: 查詢經文的原文字彙分析
- **參數**:
  - `engs`: 英文經卷縮寫
  - `chap`: 章
  - `sec`: 節
  - `gb`: 繁簡體
- **回應**:
  - `N`: 新舊約 (0=新約, 1=舊約)
  - `record[]`:
    - `wid=0`: 整節原文經文與直譯
      - `word`: 原文經文
      - `exp`: 原文直譯
      - `remark`: 註釋
    - `wid>0`: 個別字彙分析
      - `word`: 原文
      - `sn`: 原文編號 (Strong's Number)
      - `pro`: 詞性
      - `wform`: 字彙分析（格變資訊）
      - `orig`: 原型
      - `exp`: 中文解釋
      - `remark`: 註釋

##### 4.2 sd.php - 原文字典
- **用途**: 查詢 Strong's Dictionary 原文字典
- **參數**:
  - `N`: 範圍 (0=新約希臘文, 1=舊約希伯來文)
  - `k`: 原文編號
  - `gb`: 繁簡體
- **回應**:
  - `sn`: 原文編號
  - `dic_text`: 中文字典內容
  - `edic_text`: 英文字典內容
  - `dic_type`: 字典類型
  - `orig`: 原文
  - `same[]`: 同源字（僅新約）
    - `word`: 原文
    - `csn`: 編號
    - `ccnt`: 出現次數
    - `cexp`: 中文解釋

##### 4.3 sbdag.php - 浸宣中文希臘文字典
- **用途**: 查詢浸宣希臘文字典（僅授權信望愛站）
- **參數**: `k`, `gb`
- **注意**: 版權限制，僅授權信望愛站使用

##### 4.4 stwcbhdic.php - 浸宣中文希伯來文字典
- **用途**: 查詢浸宣希伯來文字典（僅授權信望愛站）
- **參數**: `k`, `gb`
- **注意**: 版權限制，僅授權信望愛站使用

#### 5. 註釋類 API

##### 5.1 sc.php - 聖經註釋
- **用途**: 查詢聖經註釋書內容
- **參數**:
  - `validbook=1`: 列出可用的註釋書
  - `book`: 註釋書編號（可用逗號分隔查詢多本）
  - `engs`: 英文經卷縮寫
  - `chap`: 章
  - `sec`: 節
  - `gb`: 繁簡體
- **回應**:
  - validbook=1 時:
    - `id`: 註釋書編號
    - `name`: 註釋書名稱
  - 一般查詢:
    - `title`: 標題
    - `book_name`: 註釋書名稱
    - `com_text`: 註釋內容
    - `prev/next`: 前後段資訊

##### 5.2 ssc.php - 搜尋註釋
- **用途**: 在註釋書中搜尋關鍵字
- **參數**:
  - `book`: 註釋書編號
  - `key`: 關鍵字
  - `gb`: 繁簡體
- **回應**:
  - `title`: 標題
  - `tag`: 註釋書編號
  - `book_name`: 註釋書名稱
  - `chinesef`: 中文經卷
  - `engs`: 英文經卷
  - `bchap/bsec`: 開始章節
  - `echap/esec`: 結束章節

#### 6. 主題查經類 API

##### 6.1 st.php - 主題查經
- **用途**: 查詢主題查經資料
- **參數**:
  - `N`: 書籍選擇
    - 0: torrey 英文
    - 1: naves 英文
    - 2: torrey 中譯
    - 3: naves 中譯
    - 4: 全部查詢
  - `k`: 編號
  - `keyword`: 關鍵字
  - `gb`: 繁簡體
  - `count_only`: 只輸出筆數
- **回應**:
  - `book`: 書籍類型
  - `id`: 編號
  - `topic`: 主題
  - `text`: 內容

#### 7. 多媒體類 API

##### 7.1 au.php - 有聲聖經
- **用途**: 取得有聲聖經音檔連結
- **參數**:
  - `version`: 有聲聖經版本
    - 0: 和合本
    - 1: 台語
    - 2: 客家話
    - 3: 廣東話
    - 4: 現代中文譯本
    - 5: 台語新約
    - 6: 紅皮聖經
    - 7: 希伯來文
    - 8: 福州話
    - 9: 希臘文
    - 10: spring台語
    - 11: spring和合本
    - 12: NetBible中文版
    - 13: 全民台語聖經
    - 14: 鄒語
    - 15: 台語南部腔
    - 17: 現代台語譯本
    - 18: 現代客語譯本
    - 19: 達悟語
  - `bid`: 經卷編號 (1-66)
  - `chap`: 章
  - `gb`: 繁簡體
- **回應**:
  - `name`: 有聲聖經名稱
  - `chinesef`: 經卷名
  - `engf`: 英文經卷名
  - `chap`: 章
  - `pbid/pchinesef/pchap`: 前一章資訊
  - `nbid/nchinesef/nchap`: 後一章資訊
  - `ogg`: OGG 格式 URL
  - `mp3`: MP3 格式 URL

##### 7.2 aump4.php - 投影片有聲聖經
- **用途**: 提供投影片格式的有聲聖經
- **參數**: 同 au.php
- **回應**: 額外包含 `mp4` 欄位

#### 8. 其他資源類 API

##### 8.1 ob.php - 珍本聖經書籍列表
- **用途**: 列出珍本聖經書籍
- **參數**:
  - `id`: 書籍編號（不輸入顯示全部）
  - `gb`: 繁簡體
- **回應**:
  - `id`: 書籍編號
  - `div`: 分類
  - `age/agec`: 著作年代（西元/中文）
  - `title`: 書名
  - `author`: 作者
  - `lang`: 語文
  - `style`: 文體格式
  - `intro`: 簡介
  - `copyright`: 著作權資訊
  - `provider`: 提供者
  - `remark`: 備註

##### 8.2 sob.php - 珍本聖經內容查詢
- **用途**: 查詢珍本聖經內容
- **參數**:
  - `book`: 書籍編號 (all=查詢模式)
  - `bid`: 經卷編號 (1-66)
  - `engs`: 經卷英文縮寫
  - `chap`: 章
  - `sec`: 節
  - `page`: 頁數
  - `gb`: 繁簡體
- **回應**:
  - mode=1 (查詢模式): 返回符合的經卷列表
  - mode=0 (檢視模式): 返回圖片與頁面資訊

##### 8.3 sobj.php - 地點與照片查詢
- **用途**: 查詢聖經地點與相關照片
- **參數**:
  - `engs`: 英文經卷縮寫
  - `chap`: 章
  - `sec`: 節
  - `gb`: 繁簡體
- **回應**:
  - `id`: 物件編號
  - `ename`: 英文名字
  - `mname`: 現代名字
  - `cname`: 和合本名字
  - `c1name`: 新標點和合本名字
  - `c2name`: 現代中文譯本名字
  - `hsname`: 舊約原文編號
  - `gsname`: 新約原文編號
  - `otype`: 座標型態 (0=點, 1=polyline, 2=polygon)
  - `objpath`: 物件座標
  - `other`: 別名
  - `remark`: 備註
  - `exp5`: 說明
  - `is_site`: 是否為地點
  - `has_collect`: 是否有照片或影音
  - `related`: 相關資料

---

## API 測試結果

### 測試 1: ab.php - 聖經版本列表

**請求**:
```bash
curl "https://bible.fhl.net/json/ab.php"
```

**結果**: ✅ 成功
- 返回 84 個聖經譯本
- 包含版本縮寫、名稱、特殊字型需求等資訊
- 主要版本: unv (和合本), kjv (KJV), nstrunv (新標點和合本) 等

### 測試 2: qb.php - 查詢約翰福音 3:16

**請求**:
```bash
curl "https://bible.fhl.net/json/qb.php?chineses=約&chap=3&sec=16&version=unv&gb=0"
```

**結果**: ✅ 成功
```json
{
  "status": "success",
  "record_count": 1,
  "v_name": "FHL和合本",
  "version": "unv",
  "record": [{
    "engs": "John",
    "chineses": "約",
    "chap": 3,
    "sec": 16,
    "bible_text": "「　神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不致滅亡，反得永生。"
  }],
  "prev": {"chineses": "約", "engs": "John", "chap": 3, "sec": 15},
  "next": {"chineses": "約", "engs": "John", "chap": 3, "sec": 17}
}
```

**觀察**:
- API 正常運作
- 提供前後節導航資訊
- 經文內容完整

### 測試 3: se.php - 關鍵字搜尋「愛」

**請求**:
```bash
curl "https://bible.fhl.net/json/se.php?VERSION=unv&orig=0&q=愛&RANGE=0&limit=5&gb=0"
```

**結果**: ✅ 成功
- 返回 5 筆搜尋結果
- 涵蓋創世記多處包含「愛」字的經文
- 每筆記錄包含經卷、章、節、經文內容

**觀察**:
- 支援中文關鍵字搜尋
- 可限制返回筆數
- 提供經文絕對編號（id）

### 測試 4: sd.php - 原文字典查詢（希臘文 #25 - agapao 愛）

**請求**:
```bash
curl "https://bible.fhl.net/json/sd.php?N=0&k=25&gb=0"
```

**結果**: ✅ 成功
```json
{
  "status": "success",
  "record_count": 1,
  "record": [{
    "sn": "00025",
    "dic_text": "25 agapao {ag-ap-ah'-o}\r\n\r\n可能源自 agan (多)...",
    "edic_text": "25 agapao {ag-ap-ah'-o}\n\nperhaps from agan...",
    "dic_type": 0,
    "orig": "ἀγαπάω",
    "same": [
      {"word": "ἀγαπάω", "csn": "00025", "ccnt": "143", "cexp": "愛；表明或證明一個人的愛；渴望"},
      {"word": "ἀγάπη, ης, ἡ", "csn": "00026", "ccnt": "116", "cexp": "愛；早期教會信徒一同分享的愛餐"},
      {"word": "ἀγαπητός, ή, όν", "csn": "00027", "ccnt": "61", "cexp": "親愛的，至愛的"}
    ]
  }]
}
```

**觀察**:
- 提供詳細的中英文字典解釋
- 包含原文拼寫
- 列出同源字及其出現次數
- 適合深度研經使用

### 測試 5: sc.php - 查詢註釋書列表

**請求**:
```bash
curl "https://bible.fhl.net/json/sc.php?validbook=1&gb=0"
```

**結果**: ✅ 成功
```json
{
  "status": "success",
  "record_count": 7,
  "record": [
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

**觀察**:
- 提供多種註釋書
- 包含學術註釋與牧師講道
- 可用於註釋查詢的 book 參數

### 測試 6: qp.php - 字彙分析（約翰福音 3:16）

**請求**:
```bash
curl "https://bible.fhl.net/json/qp.php?engs=John&chap=3&sec=16&gb=0"
```

**結果**: ✅ 成功
- 返回 26 筆記錄（1 筆整節 + 25 個字詞）
- wid=0: 整句原文與直譯
- wid=1-25: 每個希臘字的詳細分析
  - 原文拼寫
  - Strong's Number
  - 詞性
  - 字彙分析（時態、語態、人稱等）
  - 原型
  - 中文解釋

**範例記錄**:
```json
{
  "wid": 3,
  "word": "ἠγάπησεν",
  "sn": "00025",
  "pro": "動詞",
  "wform": "第一簡單過去 主動 直說語氣 第三人稱 單數",
  "orig": "ἀγαπάω",
  "exp": "愛"
}
```

**觀察**:
- 提供完整的希臘文文法分析
- 對神學研究和語言學習極有價值
- 可串接 sd.php 查詢更深入的字典資料

### 測試總結

| API | 狀態 | 回應速度 | 資料品質 | 適用場景 |
|-----|------|---------|---------|---------|
| ab.php | ✅ | 快 | 優 | 版本列表 |
| qb.php | ✅ | 快 | 優 | 經文查詢 |
| se.php | ✅ | 中等 | 優 | 關鍵字搜尋 |
| sd.php | ✅ | 快 | 優 | 原文研究 |
| sc.php | ✅ | 快 | 優 | 註釋研經 |
| qp.php | ✅ | 中等 | 優 | 深度字彙分析 |

**結論**: 所有測試的 API 均正常運作，回應結構清晰，資料完整且豐富，非常適合開發 MCP Server。

---

## MCP Server 架構設計

### 整體架構

```
FHL Bible MCP Server
├── Tools (工具) - 執行動作
├── Resources (資源) - 提供資料
└── Prompts (提示) - 預設對話範本
```

### 技術棧

- **語言**: Python 3.10+
- **MCP SDK**: `mcp` Python package
- **HTTP 客戶端**: `httpx` (異步支援)
- **JSON 處理**: 內建 `json`
- **錯誤處理**: 完整的異常捕獲與日誌記錄

### 1. Tools (工具) 設計

Tools 是可執行的動作，允許 AI 主動呼叫 API 完成任務。

#### 1.1 經文查詢工具

##### `get_bible_verse`
查詢指定章節的聖經經文

**輸入參數**:
```python
{
  "book": str,           # 經卷（中文或英文縮寫）
  "chapter": int,        # 章
  "verse": str,          # 節（可選，支援 "1", "1-5", "1,3,5" 等格式）
  "version": str,        # 版本代碼（可選，預設 "unv"）
  "include_strong": bool # 是否包含 Strong's Number（可選，預設 False）
}
```

**輸出**:
```python
{
  "version_name": str,
  "verses": [
    {
      "book": str,
      "chapter": int,
      "verse": int,
      "text": str
    }
  ],
  "navigation": {
    "prev": {...},
    "next": {...}
  }
}
```

**對應 API**: qb.php

##### `search_bible`
在聖經中搜尋關鍵字或原文編號

**輸入參數**:
```python
{
  "query": str,          # 搜尋內容
  "search_type": str,    # "keyword" | "greek_number" | "hebrew_number"
  "scope": str,          # "all" | "ot" | "nt" | "range"
  "version": str,        # 版本代碼（可選）
  "limit": int,          # 最多返回筆數（可選，預設 50）
  "offset": int          # 跳過筆數（可選，預設 0）
}
```

**輸出**:
```python
{
  "total_count": int,
  "results": [
    {
      "book": str,
      "chapter": int,
      "verse": int,
      "text": str,
      "highlight": str   # 標記關鍵字的經文
    }
  ]
}
```

**對應 API**: se.php

#### 1.2 原文研究工具

##### `get_word_analysis`
取得經文的字彙分析

**輸入參數**:
```python
{
  "book": str,       # 經卷英文縮寫
  "chapter": int,    # 章
  "verse": int       # 節
}
```

**輸出**:
```python
{
  "testament": str,  # "OT" | "NT"
  "original_text": str,
  "translation": str,
  "words": [
    {
      "position": int,
      "word": str,
      "strongs_number": str,
      "part_of_speech": str,
      "morphology": str,
      "lemma": str,
      "gloss": str
    }
  ]
}
```

**對應 API**: qp.php

##### `lookup_strongs`
查詢 Strong's 原文字典

**輸入參數**:
```python
{
  "number": int,         # Strong's Number
  "testament": str       # "OT" | "NT"
}
```

**輸出**:
```python
{
  "strongs_number": str,
  "original_word": str,
  "chinese_definition": str,
  "english_definition": str,
  "related_words": [
    {
      "word": str,
      "number": str,
      "occurrences": int,
      "gloss": str
    }
  ]
}
```

**對應 API**: sd.php

#### 1.3 註釋與研經工具

##### `get_commentary`
取得聖經註釋

**輸入參數**:
```python
{
  "book": str,           # 經卷英文縮寫
  "chapter": int,        # 章
  "verse": int,          # 節
  "commentary_id": int   # 註釋書編號（可選，不指定則返回所有）
}
```

**輸出**:
```python
{
  "results": [
    {
      "commentary_name": str,
      "title": str,
      "content": str
    }
  ]
}
```

**對應 API**: sc.php

##### `search_commentary`
搜尋註釋內容

**輸入參數**:
```python
{
  "keyword": str,        # 關鍵字
  "commentary_id": int   # 註釋書編號（可選）
}
```

**對應 API**: ssc.php

##### `get_topic_study`
查詢主題查經

**輸入參數**:
```python
{
  "keyword": str,        # 主題關鍵字
  "source": str          # "torrey_en" | "naves_en" | "torrey_zh" | "naves_zh" | "all"
}
```

**輸出**:
```python
{
  "results": [
    {
      "source": str,
      "topic": str,
      "content": str
    }
  ]
}
```

**對應 API**: st.php

#### 1.4 版本與資訊工具

##### `list_bible_versions`
列出所有可用的聖經版本

**輸入參數**: 無

**輸出**:
```python
{
  "versions": [
    {
      "code": str,
      "name": str,
      "has_strongs": bool,
      "testament": str,  # "both" | "ot_only" | "nt_only"
      "special_font": str
    }
  ]
}
```

**對應 API**: ab.php

##### `list_commentaries`
列出所有可用的註釋書

**輸入參數**: 無

**對應 API**: sc.php?validbook=1

##### `get_book_list`
取得聖經書卷列表

**輸入參數**: 無

**對應 API**: listall.html

#### 1.5 多媒體工具

##### `get_audio_bible`
取得有聲聖經連結

**輸入參數**:
```python
{
  "book_id": int,        # 經卷編號 (1-66)
  "chapter": int,        # 章
  "audio_version": str   # 音訊版本代碼
}
```

**輸出**:
```python
{
  "version_name": str,
  "book": str,
  "chapter": int,
  "audio_files": {
    "mp3": str,
    "ogg": str
  },
  "navigation": {
    "prev": {...},
    "next": {...}
  }
}
```

**對應 API**: au.php

### 2. Resources (資源) 設計

Resources 提供靜態或動態資料供 AI 讀取。

#### 2.1 經文資源

##### `bible://verse/{version}/{book}/{chapter}/{verse}`
取得特定經文

**範例**: `bible://verse/unv/John/3/16`

##### `bible://chapter/{version}/{book}/{chapter}`
取得整章經文

**範例**: `bible://chapter/unv/Gen/1`

#### 2.2 研經資源

##### `strongs://{testament}/{number}`
Strong's 字典資源

**範例**: `strongs://nt/25`

##### `commentary://{book}/{chapter}/{verse}`
註釋資源

**範例**: `commentary://John/3/16`

#### 2.3 資訊資源

##### `info://versions`
版本列表

##### `info://books`
書卷列表

##### `info://commentaries`
註釋書列表

### 3. Prompts (提示) 設計

Prompts 提供預設的對話範本，幫助使用者快速開始。

#### 3.1 `study_verse`
研讀經文

**描述**: 深入研讀一節經文，包含經文內容、原文分析、註釋等

**參數**:
```python
{
  "book": str,
  "chapter": int,
  "verse": int,
  "version": str  # 可選
}
```

**範本**:
```
請幫我深入研讀 {book} {chapter}:{verse}。

請提供：
1. 經文內容（{version} 版本）
2. 原文字彙分析
3. 相關的 Strong's 字典解釋
4. 註釋書的解經
5. 相關經文連結
```

#### 3.2 `search_topic`
主題研究

**描述**: 研究聖經中的特定主題

**參數**:
```python
{
  "topic": str
}
```

**範本**:
```
請幫我研究聖經中關於「{topic}」的教導。

請提供：
1. 相關經文搜尋結果
2. 主題查經資料
3. 註釋書中的相關討論
4. 綜合分析與應用
```

#### 3.3 `compare_translations`
版本比較

**描述**: 比較不同聖經譯本的翻譯

**參數**:
```python
{
  "book": str,
  "chapter": int,
  "verse": int,
  "versions": list  # 版本代碼列表
}
```

**範本**:
```
請幫我比較 {book} {chapter}:{verse} 在不同譯本中的翻譯。

請比較以下版本：{versions}

並分析翻譯差異與原文意義。
```

#### 3.4 `word_study`
原文字詞研究

**描述**: 深入研究希臘文或希伯來文單字

**參數**:
```python
{
  "strongs_number": int,
  "testament": str
}
```

**範本**:
```
請幫我研究 Strong's #{strongs_number} ({testament}) 這個原文字。

請提供：
1. 字典定義
2. 在聖經中的所有出現位置（前 20 處）
3. 字義在不同語境中的變化
4. 同源字分析
5. 神學意義
```

### 4. 錯誤處理

#### 錯誤類型

```python
class FHLAPIError(Exception):
    """FHL API 基礎錯誤"""
    pass

class NetworkError(FHLAPIError):
    """網路連接錯誤"""
    pass

class InvalidParameterError(FHLAPIError):
    """參數錯誤"""
    pass

class APIResponseError(FHLAPIError):
    """API 回應錯誤"""
    pass

class RateLimitError(FHLAPIError):
    """請求頻率限制"""
    pass
```

#### 錯誤處理策略

1. **網路重試**: 自動重試 3 次，指數退避
2. **參數驗證**: 在發送請求前驗證所有參數
3. **友善錯誤訊息**: 將 API 錯誤轉換為使用者友善的訊息
4. **日誌記錄**: 記錄所有錯誤以便除錯

### 5. 快取策略

為提升效能，實作快取機制：

```python
{
  "bible_versions": "永久快取",
  "book_list": "永久快取",
  "commentaries_list": "永久快取",
  "verses": "7天快取",
  "search_results": "1天快取",
  "strongs_dict": "永久快取",
  "word_analysis": "7天快取",
  "commentary_content": "7天快取"
}
```

### 6. 設定檔

```json
{
  "server": {
    "name": "fhl-bible-server",
    "version": "1.0.0"
  },
  "api": {
    "base_url": "https://bible.fhl.net/json/",
    "timeout": 30,
    "max_retries": 3
  },
  "defaults": {
    "bible_version": "unv",
    "chinese_variant": "traditional",
    "search_limit": 50,
    "include_strong": false
  },
  "cache": {
    "enabled": true,
    "directory": ".cache"
  },
  "logging": {
    "level": "INFO",
    "file": "fhl_bible_mcp.log"
  }
}
```

---

## 實作計劃

### Phase 1: 基礎架構（第 1 週）

#### 1.1 專案初始化
- [ ] 建立專案目錄結構
- [ ] 初始化 Python 虛擬環境
- [ ] 安裝依賴套件
  - mcp
  - httpx
  - pydantic (資料驗證)
  - python-dotenv (環境變數)
- [ ] 設定開發工具
  - ruff (linter)
  - black (formatter)
  - pytest (測試框架)

#### 1.2 API 客戶端層
- [ ] 實作 `FHLAPIClient` 基礎類
  - HTTP 請求封裝
  - 錯誤處理
  - 重試機制
  - 日誌記錄
- [ ] 實作個別 API 方法
  - `get_bible_versions()`
  - `get_verse()`
  - `search_bible()`
  - `get_word_analysis()`
  - `get_strongs_dict()`
  - `get_commentary()`
  - 等等...
- [ ] 單元測試

#### 1.3 資料模型
- [ ] 使用 Pydantic 定義所有資料模型
  - BibleVerse
  - SearchResult
  - WordAnalysis
  - StrongsEntry
  - Commentary
  - 等等...

### Phase 2: MCP 伺服器實作（第 2-3 週）

#### 2.1 Tools 實作
- [ ] 經文查詢工具
  - get_bible_verse
  - search_bible
- [ ] 原文研究工具
  - get_word_analysis
  - lookup_strongs
- [ ] 註釋與研經工具
  - get_commentary
  - search_commentary
  - get_topic_study
- [ ] 版本與資訊工具
  - list_bible_versions
  - list_commentaries
  - get_book_list
- [ ] 多媒體工具
  - get_audio_bible

#### 2.2 Resources 實作
- [ ] 經文資源
  - bible://verse/...
  - bible://chapter/...
- [ ] 研經資源
  - strongs://...
  - commentary://...
- [ ] 資訊資源
  - info://versions
  - info://books
  - info://commentaries

#### 2.3 Prompts 實作
- [ ] study_verse
- [ ] search_topic
- [ ] compare_translations
- [ ] word_study

### Phase 3: 功能增強（第 4 週）

#### 3.1 快取系統
- [ ] 實作檔案快取
- [ ] 快取過期策略
- [ ] 快取清理功能

#### 3.2 設定管理
- [ ] 載入設定檔
- [ ] 環境變數支援
- [ ] 執行時設定修改

#### 3.3 中文支援優化
- [ ] 中英文書卷名轉換
- [ ] 繁簡體自動處理
- [ ] 輸入容錯（接受多種書卷名格式）

### Phase 4: 測試與文件（第 5 週）

#### 4.1 測試
- [ ] 單元測試覆蓋率 > 80%
- [ ] 整合測試
- [ ] 端對端測試
- [ ] 負載測試

#### 4.2 文件
- [ ] README.md
  - 專案介紹
  - 安裝指南
  - 快速開始
- [ ] API 文件
  - 所有 Tools 說明
  - 所有 Resources 說明
  - 所有 Prompts 說明
- [ ] 開發者指南
  - 架構說明
  - 貢獻指南
- [ ] 使用範例
  - Claude Desktop 整合
  - 實際使用案例

#### 4.3 部署準備
- [ ] Docker 支援
- [ ] CI/CD 設定
- [ ] 發布到 PyPI

### Phase 5: 進階功能（未來擴充）

#### 5.1 更多資源
- [ ] 次經支援 (qsub.php)
- [ ] 使徒教父文獻 (qaf.php)
- [ ] 珍本聖經 (ob.php, sob.php)
- [ ] 地點與照片 (sobj.php)

#### 5.2 智能功能
- [ ] 經文語意搜尋
- [ ] 自動主題分類
- [ ] 經文推薦系統

#### 5.3 使用者介面
- [ ] Web UI（可選）
- [ ] VS Code 擴充套件

### 目錄結構

```
FHL_MCP_SERVER/
├── src/
│   └── fhl_bible_mcp/
│       ├── __init__.py
│       ├── server.py              # MCP Server 主程式
│       ├── api/
│       │   ├── __init__.py
│       │   ├── client.py          # API 客戶端
│       │   └── endpoints.py       # API 端點封裝
│       ├── models/
│       │   ├── __init__.py
│       │   ├── verse.py           # 經文模型
│       │   ├── search.py          # 搜尋模型
│       │   ├── strongs.py         # 原文字典模型
│       │   └── commentary.py      # 註釋模型
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── verse.py           # 經文工具
│       │   ├── search.py          # 搜尋工具
│       │   ├── strongs.py         # 原文工具
│       │   └── commentary.py      # 註釋工具
│       ├── resources/
│       │   ├── __init__.py
│       │   └── handlers.py        # Resource handlers
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── templates.py       # Prompt 範本
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── cache.py           # 快取系統
│       │   ├── booknames.py       # 書卷名轉換
│       │   └── errors.py          # 錯誤定義
│       └── config.py              # 設定管理
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   ├── test_tools/
│   ├── test_resources/
│   └── test_integration/
├── docs/
│   ├── API.md
│   ├── TOOLS.md
│   ├── RESOURCES.md
│   ├── PROMPTS.md
│   └── EXAMPLES.md
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE
└── FHL_BIBLE_MCP_PLANNING.md  # 本文件
```

### 開發時程

| 階段 | 時間 | 主要任務 |
|------|------|---------|
| Phase 1 | 第 1 週 | 基礎架構、API 客戶端 |
| Phase 2 | 第 2-3 週 | MCP Server 實作 |
| Phase 3 | 第 4 週 | 功能增強 |
| Phase 4 | 第 5 週 | 測試與文件 |
| Phase 5 | 未來 | 進階功能 |

---

## 版權注意事項

### ⚠️ 重要聲明

根據信望愛站的版權說明（https://www.fhl.net/main/fhl/fhl8.html）：

1. **聖經譯本版權**
   - 信望愛站上各個聖經譯本，有些僅授權給信望愛站使用
   - 使用者必須查閱版權說明，不得任意使用，以免違法
   - 本 MCP Server 僅作為 API 的介面層，不儲存或重新分發任何經文內容
   - 所有經文內容均即時從 FHL API 取得

2. **特殊授權內容**
   - 浸宣中文希臘文字典（sbdag.php）- 僅授權信望愛站使用
   - 浸宣中文希伯來文字典（stwcbhdic.php）- 僅授權信望愛站使用
   - 本 MCP Server 將不實作這兩個 API 的直接調用

3. **合理使用原則**
   - 本專案為非商業性質的研經工具
   - 使用者應遵守相關版權規定
   - 建議使用者在使用特定譯本前先確認版權狀態

4. **開發者責任**
   - 本 MCP Server 開發者不對使用者違反版權的行為負責
   - 使用者應自行確保其使用方式符合版權規定
   - 建議在文件中明確告知使用者版權限制

### 建議使用流程

1. 使用前先調用 `list_bible_versions` 查看可用版本
2. 選擇符合自己需求且版權允許的譯本
3. 進行合理範圍的研經活動
4. 不要大量下載或重新分發經文內容

---

## 附錄

### A. 書卷代碼對照表

#### 舊約（1-39）
| 編號 | 英文縮寫 | 中文縮寫 | 中文全名 |
|------|---------|---------|---------|
| 1 | Gen | 創 | 創世記 |
| 2 | Ex | 出 | 出埃及記 |
| 3 | Lev | 利 | 利未記 |
| ... | ... | ... | ... |

#### 新約（40-66）
| 編號 | 英文縮寫 | 中文縮寫 | 中文全名 |
|------|---------|---------|---------|
| 40 | Matt | 太 | 馬太福音 |
| 41 | Mark | 可 | 馬可福音 |
| 42 | Luke | 路 | 路加福音 |
| 43 | John | 約 | 約翰福音 |
| ... | ... | ... | ... |

### B. 常用聖經版本代碼

| 代碼 | 名稱 | 說明 |
|------|------|------|
| unv | FHL和合本 | 包含 Strong's Number |
| nstrunv | 新標點和合本 | 包含 Strong's Number |
| kjv | KJV | King James Version |
| niv | NIV | New International Version |
| tcv | 現代中文譯本 | 繁體版 |
| tclv | 台語白話字聖經 | 台語 |
| spring | 呂振中譯本 | 繁體 |

### C. 參考資源

- **信望愛站首頁**: https://www.fhl.net/
- **API 文件**: https://bible.fhl.net/json/
- **版權說明**: https://www.fhl.net/main/fhl/fhl8.html
- **MCP 官方文件**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk

---

## 版本歷史

- **v1.0** (2025-10-31): 初始規劃文件
  - 完成 API 分析
  - 完成 API 測試
  - 完成 MCP Server 架構設計
  - 完成實作計劃

---

## 結語

本規劃文件詳細分析了信望愛站聖經 API 的各項功能，並設計了完整的 MCP Server 架構。透過 MCP 協議，我們可以讓 AI 助手（如 Claude）直接存取豐富的聖經資源，提供專業的研經輔助功能。

開發過程中需要特別注意：
1. **版權尊重**: 嚴格遵守信望愛站的版權規定
2. **API 禮儀**: 實作請求限速，避免對伺服器造成負擔
3. **錯誤處理**: 提供友善的錯誤訊息
4. **使用者體驗**: 設計直觀的工具與提示
5. **文件完整**: 提供清晰的使用說明

期待這個專案能成為研讀聖經的有力工具！
