# Prompts 使用指南 📖

**FHL Bible MCP Server - 完整對話範本使用說明**

---

## 📋 目錄

- [快速導覽](#快速導覽)
- [基礎類 Prompts](#基礎類-prompts-basic)
- [讀經類 Prompts](#讀經類-prompts-reading)
- [研經類 Prompts](#研經類-prompts-study)
- [特殊類 Prompts](#特殊類-prompts-special)
- [進階類 Prompts](#進階類-prompts-advanced)
- [使用技巧](#使用技巧)
- [常見問答](#常見問答)

---

## 快速導覽

### 🎯 我該用哪個 Prompt？

| 您的需求 | 推薦 Prompt | 難度 |
|---------|------------|------|
| 我是新手，不知道從哪開始 | `basic_help_guide` | ⭐ |
| 快速查一節經文 | `basic_quick_lookup` | ⭐ |
| 每天靈修讀經 | `reading_daily` | ⭐⭐ |
| 深入研讀一節經文 | `study_verse_deep` | ⭐⭐⭐ |
| 準備主日講道 | `special_sermon_prep` | ⭐⭐⭐⭐ |
| 研究聖經人物 | `advanced_character_study` | ⭐⭐⭐⭐⭐ |

### 📊 19 個 Prompts 總覽

```
FHL Bible MCP Server Prompts
├── 📘 基礎類 (Basic) - 4 個
│   ├── basic_help_guide           新手指南
│   ├── basic_uri_demo             URI 教學
│   ├── basic_quick_lookup         快速查經
│   └── basic_tool_reference       工具參考
│
├── 📖 讀經類 (Reading) - 3 個
│   ├── reading_daily              每日讀經
│   ├── reading_chapter            整章讀經
│   └── reading_passage            段落讀經
│
├── 🎓 研經類 (Study) - 4 個
│   ├── study_verse_deep           深入研讀
│   ├── study_topic_deep           主題研究
│   ├── study_translation_compare  版本比較
│   └── study_word_original        原文研究
│
├── 🎯 特殊類 (Special) - 5 個
│   ├── special_sermon_prep        講道準備
│   ├── special_devotional         靈修材料
│   ├── special_memory_verse       背經輔助
│   ├── special_topical_chain      主題串連
│   └── special_bible_trivia       聖經問答
│
└── 🚀 進階類 (Advanced) - 3 個
    ├── advanced_cross_reference   交叉引用
    ├── advanced_parallel_gospels  符類福音
    └── advanced_character_study   人物研究
```

---

## 基礎類 Prompts (Basic)

### 1. basic_help_guide - 使用指南

**用途**: 完整的系統使用說明，新手必讀

**適合對象**: 
- ⭐ 第一次使用的新手
- 想了解完整功能的使用者
- 需要查詢特定功能的使用者

**使用範例**:

```
👤 用戶: "我是新手，請教我如何使用這個聖經工具"
🤖 Claude: 使用 basic_help_guide prompt

👤 用戶: "有哪些可用的工具？"
🤖 Claude: 使用 basic_help_guide prompt，focus on tools

👤 用戶: "如何使用 URI 資源？"
🤖 Claude: 使用 basic_help_guide prompt，focus on resources
```

**功能內容**:
- ✅ 快速開始指南
- ✅ 工具 (Tools) 完整列表與說明
- ✅ 資源 (Resources) URI 使用方式
- ✅ 對話範本 (Prompts) 介紹
- ✅ 實用範例展示

---

### 2. basic_uri_demo - URI 使用示範

**用途**: 教導如何使用各種 Resource URI，互動式學習

**適合對象**:
- ⭐ 想學習 URI 語法的使用者
- 需要快速存取資源的進階使用者
- 開發者和整合者

**使用範例**:

```
👤 用戶: "教我如何使用 URI"
🤖 Claude: 使用 basic_uri_demo prompt

👤 用戶: "展示 bible:// URI 的用法"
🤖 Claude: 使用 basic_uri_demo prompt (uri_type="bible")

👤 用戶: "所有 URI 類型示範"
🤖 Claude: 使用 basic_uri_demo prompt (uri_type="all")
```

**功能內容**:
- ✅ **Bible URI**: `bible://verse/{version}/{book}/{chapter}/{verse}`
- ✅ **Strong's URI**: `strongs://{testament}/{number}`
- ✅ **Commentary URI**: `commentary://{book}/{chapter}/{verse}`
- ✅ **Info URI**: `info://{resource_type}`
- ✅ 互動練習與實例
- ✅ 進階應用技巧

**URI 範例**:
```
查詢經文: bible://verse/unv/John/3/16
查詢整章: bible://chapter/unv/Ps/23
希臘文字典: strongs://nt/25
查看版本: info://versions
```

---

### 3. basic_quick_lookup - 快速查經

**用途**: 簡單快速查詢經文，無複雜分析，立即取得結果

**適合對象**:
- ⭐ 需要快速查經文的所有使用者
- 日常靈修和讀經
- 查經班快速查詢

**使用範例**:

```
👤 用戶: "查約翰福音 3:16"
🤖 Claude: 使用 basic_quick_lookup prompt (query="John 3:16")

👤 用戶: "詩篇 23 篇"
🤖 Claude: 使用 basic_quick_lookup prompt (query="Psalm 23")

👤 用戶: "愛的經文"
🤖 Claude: 使用 basic_quick_lookup prompt (query="love")
```

**功能特點**:
- ✅ 智能解析查詢（經節/章節/書卷/關鍵字）
- ✅ 清晰呈現經文
- ✅ 提供相關經文建議
- ✅ 快速行動選項（深入研讀/聽音訊/查註釋）

**支援格式**:
```
經節格式: "John 3:16", "約翰福音 3:16"
章節格式: "Psalm 23", "詩篇 23 篇"
書卷格式: "Genesis", "創世記"
關鍵字: "love", "愛", "faith"
```

---

### 4. basic_tool_reference - 工具參考手冊

**用途**: 詳細的工具參考文檔，查詢特定工具的使用方法

**適合對象**:
- ⭐⭐ 想深入了解工具功能的使用者
- 開發者和進階使用者
- 需要精確控制查詢的使用者

**使用範例**:

```
👤 用戶: "列出所有工具"
🤖 Claude: 使用 basic_tool_reference prompt

👤 用戶: "search_bible 怎麼用？"
🤖 Claude: 使用 basic_tool_reference prompt (tool_name="search_bible")

👤 用戶: "顯示經文查詢相關的工具"
🤖 Claude: 使用 basic_tool_reference prompt (category="verse")
```

**工具分類**:
- 📖 **經文查詢類**: get_bible_verse, get_bible_chapter, get_bible_book
- 🔍 **搜尋類**: search_bible, search_commentary
- 📚 **原文研究類**: lookup_strongs, get_word_analysis
- 💬 **註釋類**: get_commentary
- ℹ️ **資訊類**: list_bible_versions, list_bible_books
- 🎧 **音訊類**: list_audio_versions, get_audio_chapter_with_text

**每個工具包含**:
- 功能說明
- 參數詳解（必填/選填）
- 返回格式
- 3-5 個使用範例
- 注意事項
- 相關工具推薦

---

## 讀經類 Prompts (Reading)

### 5. reading_daily - 每日讀經

**用途**: 結構化的每日靈修讀經體驗，培養讀經習慣

**適合對象**:
- ⭐⭐ 建立每日讀經習慣的信徒
- 靈修小組
- 家庭靈修

**使用範例**:

```
👤 用戶: "帶領我進行今天的讀經"
🤖 Claude: 使用 reading_daily prompt

👤 用戶: "我想讀詩篇"
🤖 Claude: 使用 reading_daily prompt (book="Psalm")

👤 用戶: "隨機選一章讓我讀"
🤖 Claude: 使用 reading_daily prompt (reading_plan="random")
```

**7 步驟完整流程**:

1. **選擇經文** 📖
   - 按計劃推薦 / 用戶指定 / 隨機選擇
   - 顯示今日金句

2. **閱讀經文** 👓
   - 完整章節內容
   - 音訊版本選項

3. **背景介紹** 🏛️
   - 書卷簡介
   - 歷史文化背景

4. **重點提示** 💡
   - 3-5 個關鍵要點
   - 重要字詞解釋

5. **默想問題** 🤔
   - 3 個引導思考的問題
   - 鼓勵寫下心得

6. **生活應用** 🎯
   - 如何應用到今天的生活
   - 具體行動建議

7. **禱告方向** 🙏
   - 根據經文的禱告提示

**參數說明**:
```python
reading_plan: "sequential" | "random" | "topic"  # 讀經計劃
book: Optional[str]                              # 指定書卷
chapter: Optional[int]                           # 指定章節
```

---

### 6. reading_chapter - 整章讀經

**用途**: 深入閱讀和理解整章聖經，包含結構分析和應用

**適合對象**:
- ⭐⭐⭐ 想深入理解一整章的信徒
- 查經班帶領者
- 講道準備初步研究

**使用範例**:

```
👤 用戶: "帶我讀詩篇 23 篇"
🤖 Claude: 使用 reading_chapter prompt (book="Psalm", chapter=23)

👤 用戶: "研讀羅馬書第 8 章"
🤖 Claude: 使用 reading_chapter prompt (book="Romans", chapter=8)

👤 用戶: "我想聽約翰福音第 1 章"
🤖 Claude: 使用 reading_chapter prompt 
           (book="John", chapter=1, include_audio=true)
```

**7 步驟深度分析**:

1. **章節概覽** 📊
   - 全文展示
   - 統計資訊（節數、字數、閱讀時間）

2. **文學結構分析** 🏗️
   - 段落劃分
   - 結構大綱
   - 文學體裁識別

3. **逐段講解** 📝
   - 3-5 個段落分析
   - 每段的中心思想、關鍵經節、重要字詞

4. **串珠經文** 🔗
   - 相關經文（3-5 處）
   - 交叉引用

5. **註釋摘要** 💬
   - 各節註釋
   - 綜合解經觀點

6. **音訊選項** 🎧（可選）
   - 可用版本列表
   - 提供朗讀連結

7. **應用與反思** 💭
   - 核心信息
   - 3 個思考問題
   - 實際應用建議
   - 背誦金句推薦

**參數說明**:
```python
book: str                    # 經卷名稱（必填）
chapter: int                 # 章數（必填）
version: str = "unv"        # 聖經版本
include_audio: bool = False # 是否包含音訊
```

---

### 7. reading_passage - 段落讀經

**用途**: 閱讀和分析跨章節的經文段落（如登山寶訓、屬靈軍裝）

**適合對象**:
- ⭐⭐⭐ 研讀重要段落的信徒
- 專題查經
- 深度靈修

**使用範例**:

```
👤 用戶: "讀創世記 1:1 到 2:3"
🤖 Claude: 使用 reading_passage prompt 
           (book="Genesis", start_chapter=1, start_verse=1, 
            end_chapter=2, end_verse=3)

👤 用戶: "馬太福音 5-7 章（登山寶訓）"
🤖 Claude: 使用 reading_passage prompt 
           (book="Matthew", start_chapter=5, end_chapter=7)

👤 用戶: "以弗所書 6:10-20（屬靈軍裝）"
🤖 Claude: 使用 reading_passage prompt 
           (book="Ephesians", start_chapter=6, start_verse=10, 
            end_chapter=6, end_verse=20)
```

**8 步驟段落研究**:

1. **段落獲取** 📖
   - 完整段落內容
   - 智能處理同章/跨章情況

2. **段落背景** 🎯
   - 在全書中的位置
   - 上下文連結
   - 歷史文化背景

3. **主題識別** 🔍
   - 主要主題
   - 相同主題的其他經文

4. **重點經節** ⭐
   - 3-5 個關鍵經節
   - 原文分析

5. **結構大綱** 📋
   - 邏輯結構
   - 論證流程或敘事發展

6. **解經要點** 💡
   - 註釋查詢
   - 難解經文解釋
   - 不同觀點比較

7. **神學反思** ⛪
   - 神學意義
   - 與核心教義的關聯
   - 救恩歷史位置

8. **實際應用** 🎯
   - 今日意義
   - 生活應用原則
   - 行動挑戰

**參數說明**:
```python
book: str                      # 經卷名稱（必填）
start_chapter: int             # 起始章（必填）
start_verse: Optional[int]     # 起始節
end_chapter: int               # 結束章（必填）
end_verse: Optional[int]       # 結束節
version: str = "unv"          # 聖經版本
```

---

## 研經類 Prompts (Study)

### 8. study_verse_deep - 深入研讀經文

**用途**: 專業級的經文深度研究，涵蓋原文、註釋、神學等

**適合對象**:
- ⭐⭐⭐⭐ 認真研經的信徒
- 神學生
- 傳道人和教師

**使用範例**:

```
👤 用戶: "深入研讀約翰福音 3:16"
🤖 Claude: 使用 study_verse_deep prompt (reference="John 3:16")

👤 用戶: "分析羅馬書 8:28"
🤖 Claude: 使用 study_verse_deep prompt (reference="Romans 8:28")
```

**研究內容**:
- ✅ 經文內容（多版本）
- ✅ 原文分析（Strong's Number）
- ✅ 字義解釋
- ✅ 文法結構
- ✅ 上下文分析
- ✅ 註釋參考
- ✅ 神學意義
- ✅ 實際應用

---

### 9. study_topic_deep - 主題研究

**用途**: 全面探討聖經中的特定主題

**適合對象**:
- ⭐⭐⭐⭐ 專題研究
- 講道準備
- 主題查經班

**使用範例**:

```
👤 用戶: "研究聖經中的「信心」主題"
🤖 Claude: 使用 study_topic_deep prompt (topic="faith")

👤 用戶: "探討「愛」的聖經教導"
🤖 Claude: 使用 study_topic_deep prompt (topic="love")
```

**研究內容**:
- ✅ 主題定義
- ✅ 原文字彙分析
- ✅ 舊約中的主題
- ✅ 新約中的發展
- ✅ 關鍵經文精選
- ✅ 神學綜合
- ✅ 實踐應用

---

### 10. study_translation_compare - 版本比較

**用途**: 比較不同聖經譯本的翻譯差異

**適合對象**:
- ⭐⭐⭐ 想了解翻譯差異的信徒
- 解經研究
- 翻譯研究

**使用範例**:

```
👤 用戶: "比較約翰福音 3:16 的不同譯本"
🤖 Claude: 使用 study_translation_compare prompt 
           (reference="John 3:16", 
            versions=["unv", "kjv", "niv"])

👤 用戶: "和合本與現代中文譯本的差異"
🤖 Claude: 使用 study_translation_compare prompt 
           (versions=["unv", "rcuv"])
```

**比較內容**:
- ✅ 並列顯示多個版本
- ✅ 關鍵差異標示
- ✅ 原文根據分析
- ✅ 翻譯選擇說明
- ✅ 解經影響討論

---

### 11. study_word_original - 原文字詞研究

**用途**: 深入研究希臘文/希伯來文原文字彙

**適合對象**:
- ⭐⭐⭐⭐ 原文研究愛好者
- 神學生
- 深度研經者

**使用範例**:

```
👤 用戶: "研究希臘文的『愛』字"
🤖 Claude: 使用 study_word_original prompt (word="love", language="greek")

👤 用戶: "希伯來文的『神』字研究"
🤖 Claude: 使用 study_word_original prompt (word="God", language="hebrew")
```

**研究內容**:
- ✅ Strong's Number
- ✅ 原文拼寫與發音
- ✅ 字義範圍
- ✅ 字根分析
- ✅ 聖經中的出現次數
- ✅ 典型經文
- ✅ 同義詞/反義詞
- ✅ 神學意義

---

## 特殊類 Prompts (Special)

### 12. special_sermon_prep - 講道準備

**用途**: 全面準備講道或查經，從解經到應用的完整資源

**適合對象**:
- ⭐⭐⭐⭐ 傳道人和牧師
- 查經班帶領者
- 主日學教師

**使用範例**:

```
👤 用戶: "準備約翰福音 3:16-21 的講道"
🤖 Claude: 使用 special_sermon_prep prompt 
           (passage="John 3:16-21", sermon_type="expository")

👤 用戶: "為青年團契準備詩篇 23 篇的查經"
🤖 Claude: 使用 special_sermon_prep prompt 
           (passage="Psalm 23", audience="youth")

👤 用戶: "主題式講道：信心"
🤖 Claude: 使用 special_sermon_prep prompt 
           (sermon_type="topical", topic="faith")
```

**6 大準備區塊**:

1. **經文準備** 📖
   - 主要經文（多版本比較）
   - 上下文經文
   - 平行經文

2. **解經研究** 🔍
   - 原文分析（關鍵字詞）
   - 註釋參考
   - 歷史文化背景
   - 文學結構

3. **大綱建議** 📝
   - 3-5 點主要大綱
   - 每點的經文支持
   - 邏輯流程

4. **例證建議** 💡
   - 相關聖經故事
   - 現代應用場景
   - 實例說明

5. **應用方向** 🎯
   - 針對不同聽眾的應用
   - 具體行動建議
   - 挑戰與鼓勵

6. **補充資源** 📚
   - 相關經文清單
   - 主題查經資料
   - 延伸閱讀建議

**參數說明**:
```python
passage: str                           # 經文範圍（必填）
sermon_type: "expository" | "topical" | "textual"  # 講道類型
audience: "general" | "youth" | "new_believers" | "mature"  # 聽眾對象
```

---

### 13. special_devotional - 靈修材料

**用途**: 生成個人或小組靈修材料，包含默想、禱告和應用

**適合對象**:
- ⭐⭐⭐ 個人靈修
- 小組查經
- 家庭靈修

**使用範例**:

```
👤 用戶: "為詩篇 23 準備靈修材料"
🤖 Claude: 使用 special_devotional prompt 
           (passage="Psalm 23", format="personal")

👤 用戶: "小組查經用的約翰福音 15 章材料"
🤖 Claude: 使用 special_devotional prompt 
           (passage="John 15", format="group")

👤 用戶: "家庭靈修 - 路加福音 15 章"
🤖 Claude: 使用 special_devotional prompt 
           (passage="Luke 15", format="family")
```

**8 步驟靈修指引**:

1. **開場禱告** 🙏
   - 開場禱詞建議

2. **經文閱讀** 📖
   - 今日經文
   - 建議閱讀方式（靜讀/朗讀/默想）

3. **背景簡介** 📚
   - 經文背景（1-2 段）
   - 與我們的關聯

4. **重點觀察** 👀
   - 3-5 個觀察要點
   - 關鍵字詞解釋

5. **默想問題** 💭
   - **個人版**: 3-4 個反思問題
   - **小組版**: 5-6 個討論問題
   - **家庭版**: 適齡的互動問題

6. **實際應用** 🎯
   - 今日行動
   - 本週挑戰
   - 生活實踐

7. **禱告方向** 🙏
   - 感恩事項
   - 認罪悔改
   - 代求事項
   - 奉獻立志

8. **金句卡片** ⭐
   - 可背誦的金句
   - 精美格式呈現

**參數說明**:
```python
passage: str                              # 經文（必填）
format: "personal" | "group" | "family"   # 格式
duration: "short" | "medium" | "long"     # 時長
```

---

### 14. special_memory_verse - 背經輔助

**用途**: 協助選擇、理解和背誦經文，提供記憶技巧

**適合對象**:
- ⭐⭐ 想背誦經文的信徒
- 兒童主日學
- 背經小組

**使用範例**:

```
👤 用戶: "推薦關於信心的背誦經文"
🤖 Claude: 使用 special_memory_verse prompt (topic="faith")

👤 用戶: "我想背詩篇中的經文"
🤖 Claude: 使用 special_memory_verse prompt (book="Psalm")

👤 用戶: "給初信者的簡單經文"
🤖 Claude: 使用 special_memory_verse prompt (difficulty="easy")
```

**5 大輔助功能**:

1. **經文推薦** 🎯
   - 根據主題搜尋
   - 篩選合適長度（短而精）
   - 按難度分級

2. **背誦計劃** 📅
   - 分段記憶法
   - 關鍵字提示
   - 重複練習建議

3. **理解輔助** 💡
   - 經文意義解釋
   - 原文字義
   - 應用場景

4. **記憶技巧** 🧠
   - 視覺化聯想
   - 韻律節奏
   - 串珠記憶（相關經文）

5. **複習系統** 🔄
   - 艾賓浩斯遺忘曲線
   - 複習時間表
   - 測驗題目

**參數說明**:
```python
topic: Optional[str]                      # 主題
book: Optional[str]                       # 特定書卷
difficulty: "easy" | "medium" | "hard"    # 難度
```

---

### 15. special_topical_chain - 主題串連

**用途**: 串連聖經中同一主題的所有重要經文，追蹤主題發展

**適合對象**:
- ⭐⭐⭐⭐ 主題研究
- 神學研究
- 系統查經

**使用範例**:

```
👤 用戶: "串連聖經中關於「愛」的教導"
🤖 Claude: 使用 special_topical_chain prompt (topic="love")

👤 用戶: "新約中的「恩典」主題"
🤖 Claude: 使用 special_topical_chain prompt 
           (topic="grace", testament="NT")

👤 用戶: "從創世記到啟示錄看「救贖」"
🤖 Claude: 使用 special_topical_chain prompt 
           (topic="redemption", depth="exhaustive")
```

**6 步驟主題追蹤**:

1. **主題定義** 📖
   - 聖經定義
   - 相關原文字詞
   - 同義詞和相關概念

2. **舊約追蹤** 📜
   - 首次出現（First Mention Principle）
   - 律法書中的教導
   - 歷史書中的實例
   - 詩歌智慧書中的反思
   - 先知書中的預言

3. **新約發展** ✝️
   - 福音書中耶穌的教導
   - 使徒行傳中的實踐
   - 書信中的神學闡述
   - 啟示錄中的完全

4. **神學發展線** 📈
   - 救恩歷史中的發展
   - 從舊約到新約的連貫性
   - 在基督裡的成全

5. **關鍵經文精選** ⭐
   - 最重要的 10-15 處經文
   - 按時間順序或邏輯順序
   - 每處經文的簡要註解

6. **實踐應用** 🎯
   - 今日意義
   - 如何活出該主題

**參數說明**:
```python
topic: str                                # 主題關鍵字（必填）
testament: "OT" | "NT" | "both"          # 約別
depth: "overview" | "detailed" | "exhaustive"  # 深度
```

---

### 16. special_bible_trivia - 聖經問答

**用途**: 互動式聖經知識問答，可用於學習或小組活動

**適合對象**:
- ⭐⭐ 所有信徒
- 主日學
- 小組遊戲
- 知識測驗

**使用範例**:

```
👤 用戶: "出 10 題關於舊約人物的問題"
🤖 Claude: 使用 special_bible_trivia prompt 
           (category="people", testament="OT", count=10)

👤 用戶: "簡單的新約問答題"
🤖 Claude: 使用 special_bible_trivia prompt 
           (testament="NT", difficulty="easy")

👤 用戶: "測試我對詩篇的了解"
🤖 Claude: 使用 special_bible_trivia prompt 
           (category="books", book="Psalm")
```

**5 種題型**:

1. **選擇題** ✅
   - 4 個選項
   - 提供經文出處

2. **填空題** ✏️
   - 經文填空
   - 人名/地名填空

3. **配對題** 🔗
   - 人物與事件配對
   - 經文與書卷配對

4. **簡答題** 📝
   - 解釋經文意義
   - 描述事件經過

5. **搶答題** ⚡（小組用）
   - 快速反應題
   - 計分規則

**每題包含**:
- 問題
- 選項/答案
- 正確答案
- 經文出處
- 詳細解釋
- 延伸知識

**參數說明**:
```python
category: "people" | "places" | "events" | "teachings" | "books"  # 類別
difficulty: "easy" | "medium" | "hard"    # 難度
count: int = 10                           # 題數
testament: Optional[str]                  # OT/NT/both
```

---

## 進階類 Prompts (Advanced)

### 17. advanced_cross_reference - 交叉引用分析

**用途**: 多層次的交叉引用分析，發現經文之間的關聯網絡

**適合對象**:
- ⭐⭐⭐⭐⭐ 深度研經者
- 解經研究
- 神學研究

**使用範例**:

```
👤 用戶: "約翰福音 3:16 的交叉引用"
🤖 Claude: 使用 advanced_cross_reference prompt 
           (reference="John 3:16", depth=2)

👤 用戶: "找出與羅馬書 8:28 相關的所有經文"
🤖 Claude: 使用 advanced_cross_reference prompt 
           (reference="Romans 8:28", depth=3, max_results=30)

👤 用戶: "詩篇 23:1 的直接引用"
🤖 Claude: 使用 advanced_cross_reference prompt 
           (reference="Psalm 23:1", depth=1)
```

**深度控制**:

- **Depth 1**: 直接引用（~4,450 字元）
  - 平行經文
  - 直接引用和被引用
  - 相同主題的經文

- **Depth 2**: 間接引用（~5,450 字元）
  - 包含 Depth 1 所有內容
  - 主題延伸的經文
  - 概念關聯的經文

- **Depth 3**: 主題連結（~6,340 字元）
  - 包含 Depth 1-2 所有內容
  - 廣泛主題相關經文
  - 應用性連結

**7 步驟分析流程**:

1. **目標經文解析** 🎯
   - 經文內容
   - Strong's Numbers
   - 關鍵主題識別

2. **第一層：直接引用** 🔗
   - 平行經文
   - 引用關係
   - 相同用語

3. **第二層：間接引用** 🔍（depth >= 2）
   - 主題延伸
   - 概念關聯
   - 教義連結

4. **第三層：主題連結** 🌐（depth >= 3）
   - 廣泛主題
   - 應用連結
   - 實踐相關

5. **關係網絡視覺化** 📊
   - ASCII 藝術展示引用關係樹

6. **連結分析報告** 📈
   - 主題分析
   - 神學意義
   - 實踐建議

7. **進階探索建議** 🚀
   - 延伸研究方向
   - 相關 prompts 推薦

**參數說明**:
```python
reference: str = "John 3:16"    # 目標經文
depth: int = 2                  # 深度層數（1-3）
max_results: int = 20           # 每層最大結果數（10-50）
version: str = "unv"           # 聖經譯本
```

---

### 18. advanced_parallel_gospels - 符類福音對照

**用途**: 四福音書平行事件比較，理解同一事件的不同記載

**適合對象**:
- ⭐⭐⭐⭐⭐ 福音書研究
- 神學生
- 解經研究

**使用範例**:

```
👤 用戶: "登山寶訓的符類福音對照"
🤖 Claude: 使用 advanced_parallel_gospels prompt 
           (event="Sermon on the Mount", include_john=false)

👤 用戶: "五餅二魚在四福音的記載"
🤖 Claude: 使用 advanced_parallel_gospels prompt 
           (event="Feeding of 5000", include_john=true)

👤 用戶: "耶穌受洗的對照"
🤖 Claude: 使用 advanced_parallel_gospels prompt 
           (event="Jesus' Baptism")
```

**9 步驟對照流程**:

1. **平行經文定位** 📍
   - 在四福音中找出相同事件的位置
   - 表格呈現

2. **經文全文檢索** 📖
   - 取得各福音書的完整經文

3. **逐字對照表** 📊
   - 四欄並列原文
   - 方便直接比較

4. **相同點分析** ✅
   - 共同核心事實
   - 相同用詞
   - 一致的神學主題

5. **差異點分析** 🔍
   - 各福音書的獨特細節
   - 作者的不同強調
   - 目標讀者的考量

6. **神學綜合** ⛪
   - 從四個角度看耶穌
   - 綜合神學信息
   - 互補性理解

7. **應用指引** 🎯
   - 講道應用
   - 小組查經
   - 個人靈修

8. **關係網絡圖** 🕸️
   - 福音書之間的關係
   - 資料來源假說

9. **總結與延伸** 📝
   - 核心發現
   - 延伸研究建議

**參數說明**:
```python
event: str = "Jesus' Baptism"    # 事件名稱（必填）
passage: Optional[str] = None    # 可選的特定段落
version: str = "unv"            # 聖經版本
include_john: bool = True       # 是否包含約翰福音
```

**長度控制**:
- `include_john=False`: ~6,029 字元（符類福音：馬太、馬可、路加）
- `include_john=True`: ~6,536 字元（完整四福音對照）

---

### 19. advanced_character_study - 聖經人物研究

**用途**: 全面的聖經人物研究，涵蓋生平、性格、教訓等 9 大維度

**適合對象**:
- ⭐⭐⭐⭐⭐ 人物專題研究
- 講道準備
- 神學研究
- 教學資源

**使用範例**:

```
👤 用戶: "研究保羅的生平"
🤖 Claude: 使用 advanced_character_study prompt 
           (character="Paul", focus="all")

👤 用戶: "大衛是怎樣的人？"
🤖 Claude: 使用 advanced_character_study prompt 
           (character="David", focus="character")

👤 用戶: "彼得的失敗與恢復"
🤖 Claude: 使用 advanced_character_study prompt 
           (character="Peter", focus="lessons")

👤 用戶: "亞伯拉罕生平時間線"
🤖 Claude: 使用 advanced_character_study prompt 
           (character="Abraham", focus="biography")
```

**9 大研究維度**:

1. **基本資料卡** 📋
   - 姓名意義
   - 時代背景
   - 家族關係
   - 身份職務
   - 經文統計

2. **生平時間線** 📅（focus="biography" 或 "all"）
   - **第一階段**: 早年生活
   - **第二階段**: 蒙召跟隨
   - **第三階段**: 使徒生涯/高峰
   - **第四階段**: 試煉與跌倒
   - **第五階段**: 恢復與事奉

3. **性格特質分析** 🎭（focus="character" 或 "all"）
   - **優點**: 3-5 項優點分析
   - **缺點**: 3-5 項弱點分析
   - **成長軌跡**: 性格發展歷程
   - **情感變化**: 情緒起伏

4. **屬靈教訓** 💡（focus="lessons" 或 "all"）
   - **正面榜樣**: 值得學習的地方
   - **負面警戒**: 需要避免的錯誤
   - **上帝的恩典**: 神在他身上的作為

5. **關係網絡圖** 🕸️
   - 與其他聖經人物的關係
   - 家族關係樹
   - 事奉夥伴

6. **聖經作者評價** 📖
   - 舊約/新約中對該人物的評價
   - 不同書卷的描述

7. **主題研究建議** 📚
   - 延伸研究方向
   - 相關主題探索

8. **應用與反思** 💭
   - **個人層面**: 個人生命的應用
   - **人際關係**: 關係處理的學習
   - **事奉層面**: 服事的借鏡

9. **教學講道資源** 🎓
   - 講道大綱建議
   - 教案設計
   - 小組討論問題

**焦點控制**:

- **focus="biography"**: 僅生平事蹟（~7,569 字元）
  - 基本資料 + 時間線 + 網絡圖 + 應用

- **focus="character"**: 僅性格分析（~6,895 字元）
  - 基本資料 + 性格分析 + 網絡圖 + 應用

- **focus="lessons"**: 僅屬靈教訓（~7,211 字元）
  - 基本資料 + 屬靈教訓 + 網絡圖 + 應用

- **focus="all"**: 完整研究（~10,127 字元）
  - 包含所有 9 大維度

**參數說明**:
```python
character: str = "Peter"                      # 人物名稱（必填）
focus: str = "all"                            # 焦點選項
    # "all": 完整研究
    # "biography": 僅生平事蹟
    # "character": 僅性格分析
    # "lessons": 僅屬靈教訓
testament: str = "both"                       # 約書範圍
    # "OT": 舊約人物
    # "NT": 新約人物
    # "both": 跨約人物
version: str = "unv"                         # 聖經譯本
```

---

## 使用技巧

### 💡 技巧 1: 組合使用 Prompts

不同 prompts 可以組合使用，形成完整的研經流程：

**範例：準備一篇講道**
```
1. basic_quick_lookup (快速了解經文)
   ↓
2. reading_chapter (閱讀整章背景)
   ↓
3. study_verse_deep (深入研讀關鍵經節)
   ↓
4. advanced_cross_reference (找相關經文)
   ↓
5. special_sermon_prep (整理講道大綱)
```

### 💡 技巧 2: 由淺入深

建議的學習路徑：

**新手路徑** (第 1-4 週)
```
Week 1: basic_help_guide → basic_quick_lookup
Week 2: reading_daily (建立讀經習慣)
Week 3: reading_chapter (深入一點)
Week 4: study_verse_deep (嘗試研經)
```

**進階路徑** (第 5-12 週)
```
Month 2: special_devotional, special_memory_verse
Month 3: study_topic_deep, special_topical_chain
```

**專業路徑** (3 個月後)
```
advanced_cross_reference
advanced_parallel_gospels
advanced_character_study
```

### 💡 技巧 3: 善用參數

每個 prompt 都有參數可以調整輸出：

**範例：控制長度**
```python
# 簡短版本
advanced_cross_reference(reference="John 3:16", depth=1)  # ~4,450 字元

# 完整版本
advanced_cross_reference(reference="John 3:16", depth=3)  # ~6,340 字元
```

**範例：調整焦點**
```python
# 只看生平
advanced_character_study(character="Peter", focus="biography")

# 完整研究
advanced_character_study(character="Peter", focus="all")
```

### 💡 技巧 4: 與 URI 資源結合

Prompts 產生的內容中會包含 URI 連結，點擊可直接訪問資源：

```
經文 URI: bible://verse/unv/John/3/16
註釋 URI: commentary://John/3/16
原文 URI: strongs://nt/25
```

### 💡 技巧 5: 針對不同場景

**個人靈修**
```
reading_daily → study_verse_deep → special_devotional
```

**小組查經**
```
reading_passage → special_devotional (format="group") → special_bible_trivia
```

**講道準備**
```
reading_chapter → advanced_cross_reference → special_sermon_prep
```

**主題研究**
```
study_topic_deep → special_topical_chain → advanced_cross_reference
```

---

## 常見問答

### ❓ Q1: 我該從哪個 Prompt 開始？

**A**: 從 `basic_help_guide` 開始！它會給您完整的系統介紹。

### ❓ Q2: Prompts 之間有什麼區別？

**A**: 主要區別在於：
- **深度**: basic < reading < study < advanced
- **用途**: 日常讀經 vs 專業研經 vs 講道準備
- **長度**: basic (簡短) < reading (中等) < advanced (詳盡)

### ❓ Q3: 如何選擇合適的 depth 或 focus 參數？

**A**: 
- **時間有限**: 選擇較小的值（depth=1, focus="character"）
- **深入研究**: 選擇較大的值（depth=3, focus="all"）
- **首次嘗試**: 使用默認值

### ❓ Q4: 可以同時使用多個 Prompts 嗎？

**A**: 可以！實際上我們鼓勵組合使用。例如：
```
1. basic_quick_lookup (快速查看)
2. study_verse_deep (深入研讀)
3. special_memory_verse (背誦)
```

### ❓ Q5: Advanced Prompts 和 Study Prompts 有什麼不同？

**A**: 
- **Study Prompts**: 專注於單一經文或主題的深度分析
- **Advanced Prompts**: 更廣泛的關聯性研究（交叉引用、平行對照、人物追蹤）

### ❓ Q6: 如何提供反饋或建議新的 Prompt？

**A**: 請在 GitHub 專案中開 Issue，我們會認真考慮每一個建議！

### ❓ Q7: Prompts 支援哪些語言？

**A**: 目前支援：
- **中文** (繁體/簡體)
- **英文**
- 其他語言正在規劃中

### ❓ Q8: 我可以自訂 Prompt 嗎？

**A**: 目前暫不支援自訂 Prompt，但您可以：
1. Fork 專案自行開發
2. 提交 Pull Request 貢獻新 Prompt
3. 開 Issue 建議新功能

---

## 結語

FHL Bible MCP Server 的 **19 個 Prompts** 提供了從入門到專業的完整聖經研讀體驗：

✅ **4 個基礎 Prompts** - 快速上手  
✅ **3 個讀經 Prompts** - 每日靈修  
✅ **4 個研經 Prompts** - 深度研讀  
✅ **5 個特殊 Prompts** - 專業應用  
✅ **3 個進階 Prompts** - 專家級研究  

無論您是：
- 👶 剛信主的新手
- 📖 每日讀經的信徒
- 🎓 認真研經的學生
- 🎤 準備講道的牧者
- 🔬 專業研究的學者

都能找到適合您的工具！

---

**開始使用**: 在 Claude Desktop 中說：
```
"使用 basic_help_guide 幫我了解這個聖經工具"
```

**需要幫助**: 參考 [README](../README.md) 或 [開發者指南](DEVELOPER_GUIDE.md)

**Made with ❤️ for Bible study | 願神的話語豐富您的生命！** 🙏
