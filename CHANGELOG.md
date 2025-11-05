# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-11-05

### ✨ Enhanced

#### P1 Strong's 字典功能增強

- **[P1-4] lookup_strongs 多格式支援**: 支援多種 Strong's Number 輸入格式
  - **新增功能**:
    - 支援 G 前綴（新約）: `lookup_strongs("G3056")` 自動識別為新約
    - 支援 H 前綴（舊約）: `lookup_strongs("H430")` 自動識別為舊約
    - 支援前導零: `"G03056"` 正確解析為 3056
    - 大小寫不敏感: `"g3056"` 和 `"G3056"` 等效
    - 向後兼容: 原有格式 `lookup_strongs(3056, "NT")` 仍然有效
  - **實現方式**:
    - 新增 `_parse_strongs_input()` 輔助函數解析多種格式
    - 更新函數簽名: `number: Union[int, str]`, `testament: Optional[str]`
    - API 調用使用純整數（移除 G/H 前綴）
  - **測試覆蓋**: 17 個單元測試驗證所有格式
  - [實施報告](docs/6_bug_fix/P1_STRONGS_FIX_IMPLEMENTATION.md)

- **[P1-5] search_strongs_occurrences 修復**: 修復搜尋功能返回 0 結果問題
  - **問題**: `search_strongs_occurrences("G1344")` 返回 0 筆結果
  - **根本原因**: 
    - Greek search API 不接受 "G1344" 格式（返回 0 結果）
    - 只接受純數字 "1344" 格式
  - **解決方案**:
    - 使用 `_parse_strongs_input()` 提取純數字
    - 傳遞純數字給 search_bible API
    - 支援所有 lookup_strongs 的輸入格式
  - **驗證**: G1344 (稱義) 和 H430 (神) 搜尋均返回實際結果
  - [實施報告](docs/6_bug_fix/P1_STRONGS_FIX_IMPLEMENTATION.md)

### 🔧 Changed

- **MCP 工具定義更新**: 
  - `lookup_strongs` 和 `search_strongs_occurrences` 參數類型改為 `["string", "integer"]`
  - `testament` 參數改為可選（當使用 G/H 前綴時）
  - 更新工具描述說明多格式支援

### � Fixed

- **[P1-6] search_bible 參數驗證**: 修復 greek_number/hebrew_number 參數驗證失敗
  - **問題**: `search_type="greek_number"` 被 MCP 工具拒絕（"must be equal to one of the allowed values"）
  - **根本原因**: server.py 的工具定義使用 `["keyword", "greek", "hebrew"]`，但實現使用 `["keyword", "greek_number", "hebrew_number"]`
  - **解決方案**: 統一 MCP 工具定義為 `["keyword", "greek_number", "hebrew_number"]`
  - **測試驗證**: 
    - G1344 搜尋返回 35 處出現 ✅
    - H430 搜尋返回 20 處出現（含創 1:1） ✅
  - [修復報告](docs/6_bug_fix/P1_SEARCH_BIBLE_PARAM_FIX.md)

### �📊 Testing

- **新增測試檔案**: `tests/test_strongs_enhanced.py`
  - 31 個測試用例全部通過 ✅
- **新增測試檔案**: `tests/test_search_bible_numbers.py`
  - 5 個測試用例全部通過 ✅
  - 驗證 greek_number/hebrew_number 搜尋功能
  - 涵蓋單元測試、整合測試、端到端測試
  - 測試覆蓋率: strongs.py 從 30% → 65%

- **快速驗證腳本**: `tests/test_strongs_quick_verify.py`
  - 6 個核心功能驗證測試
  - 可快速驗證修復成效

### 📈 Impact

**P1 問題修復完成度**:
- v0.1.1-bugfix: P0 100% (2/2), P1 60% (3/5), 總計 71% (5/7)
- **v0.1.2**: P0 100% (2/2), **P1 100% (6/6)**, **總計 100% (8/8)** ✅

**向後兼容性**: 100% - 所有現有代碼無需修改

**新修復問題**:
- P1-4: lookup_strongs 多格式支援
- P1-5: search_strongs_occurrences 返回結果
- P1-6: search_bible 參數驗證

### 📚 Documentation

- 新增 `docs/6_bug_fix/P1_STRONGS_FIX_IMPLEMENTATION.md` - Strong's 字典修復實施報告
- 新增 `docs/6_bug_fix/P1_SEARCH_BIBLE_PARAM_FIX.md` - search_bible 參數修復報告
- 新增 `docs/6_bug_fix/v0.1.2_RELEASE_NOTES.md` - 完整發布說明
- 更新 `docs/6_bug_fix/testing_report.md` - 添加最終驗證結果
- 更新 `docs/6_bug_fix/BUG_FIX_SUMMARY.md` - 完整修復總結
- 更新 `docs/4_manuals/API.md` - Strong's 和 search_bible 功能文檔
- 更新 `docs/4_manuals/PROMPTS_QUICK_REFERENCE.md` - 快速參考指南

---

## [0.1.1-bugfix] - 2025-11-05

### 🐛 Fixed

#### P0 優先級（核心功能）

- **[P0-1] 書卷映射錯置**: 修復了所有經文查詢返回錯誤書卷的嚴重問題
  - 問題: Acts/John/Psalms 查詢錯誤返回 Genesis
  - 原因: FHL API 的 `chineses` 和 `engs` 參數不可靠
  - 解決: 改用 `bid` (Book ID) 參數進行書卷識別
  - 影響方法: 
    - `get_verse()`
    - `get_apocrypha_verse()`
    - `get_apostolic_fathers_verse()`
    - `get_word_analysis()`
    - `get_commentary()`
  - [詳細報告](docs/6_bug_fix/BUG_FIX_SUMMARY.md#p0-1)

- **[P0-2] Strong's 字典功能**: 驗證並澄清 API 正確使用方式
  - 問題: 報告稱返回 "Strong's Number: 00000" 範例
  - 診斷: API 實際正常運作，參數格式理解有誤
  - 解決: 更新文檔說明，明確參數格式要求
  - [詳細報告](docs/6_bug_fix/BUG_FIX_SUMMARY.md#p0-2)

#### P1 優先級（體驗改善）

- **[P1-1] 參數型別驗證不足**: 增強參數處理靈活性
  - 問題: 傳入整數參數導致 `AttributeError: 'int' object has no attribute 'isascii'`
  - 解決: 
    - 修改 `BookNameConverter.get_book_id()` 支持整數、數字字串、書卷名稱
    - 在 `search_bible_advanced()` 添加自動型別轉換
  - 改進: 用戶可以使用 `40`, `"40"`, `"太"` 等多種格式
  - [詳細報告](docs/6_bug_fix/BUG_FIX_SUMMARY.md#p1-1)

- **[P1-2] 註釋查詢返回空**: 修復註釋 API 查詢失敗
  - 問題: `get_commentary()` 總是返回 0 筆結果
  - 原因: 使用 `engs` 參數導致 API 失敗
  - 解決: 改用 `bid` 參數，與經文查詢保持一致
  - 測試: 約 3:16, 羅 3:24 等經文註釋查詢成功
  - [詳細報告](docs/6_bug_fix/BUG_FIX_SUMMARY.md#p1-2)

- **[P1-3] get_word_analysis 錯誤**: 修復原文分析功能
  - 問題: 返回 `KeyError: 'N'` 和 "Fail:engs error!"
  - 原因: 使用 `engs` 參數導致 API 響應異常
  - 解決: 改用 `bid` 參數
  - 測試: 約 3:16 (25 個希臘文), 創 1:1 (7 個希伯來文) 成功
  - [詳細報告](docs/6_bug_fix/BUG_FIX_SUMMARY.md#p1-3)

### ✨ Enhanced

- **書卷支援擴展**: 
  - 添加次經書卷定義 (bid 101-115, 15 卷)
  - 添加使徒教父書卷定義 (bid 201-217, 8 卷)
  - 更新 `booknames.py` 包含完整書卷列表

- **參數處理改進**:
  - `get_book_id()` 現在支持整數、字串、書卷名稱
  - 自動型別轉換提升用戶體驗

### 📝 Documentation

- 新增 `docs/6_bug_fix/` 目錄
  - `BUG_FIX_SUMMARY.md` - 完整修復總結報告
  - `BUG_FIX_PLAN.md` - 詳細修復計劃
  - `BUG_FIX_PROGRESS.md` - 實時進度追蹤
  - `README.md` - Bug 修復文檔索引
- 更新主要 README.md 添加版本徽章和修復通知
- 更新 `docs/README.md` 添加 6_bug_fix 目錄說明

### 🧪 Testing

#### 初步驗證（修復時）
- 所有 5 個 bug 已驗證修復 (100%)
- 測試涵蓋:
  - 經文查詢 (聖經、次經、使徒教父)
  - Strong's 字典查詢
  - 原文分析 (希臘文、希伯來文)
  - 註釋查詢
  - 參數型別驗證 (整數、字串、書卷名)

#### 回歸壓力測試（修復後）
**測試日期**: 2025-11-05  
**測試版本**: v0.1.1-bugfix

**測試結果**:
- ✅ P0 核心功能: 10/10 通過 (100%)
- 🟡 P1 體驗改善: 3/5 通過 (60%)
- 📊 總體通過率: 13/15 (87%)

**通過項目**:
- ✅ Acts 12/13, John 3, Psalms 23 書卷映射正確
- ✅ 約 3:16, 徒 13:39 Strong's 標記正確
- ✅ get_word_analysis (約 1:1) 原文分析成功
- ✅ get_commentary (約 3:16, 羅 3:24) 註釋查詢成功
- ✅ search_bible_advanced 參數型別驗證通過
- ✅ 詩 23 audio+text 文字對齊正確
- ✅ 智 1:1-5 次經書卷映射正確
- ✅ citation 引用解析正確

**待修項目** (P1, 不影響核心功能):
- ⚠️ lookup_strongs: 仍返回 00000 範例
- ⚠️ search_strongs_occurrences: 返回 0 筆
- ⚠️ search_bible (greek_number): 參數驗證需統一

**結論**: P0 級別問題完全解決，核心功能穩定，可立即發布。剩餘 P1 項目規劃在 v0.1.2 修復。

詳細測試報告: [testing_report.md](docs/6_bug_fix/testing_report.md#13-回歸壓力測試結果修復後)

### 🔧 Changed Files

- `src/fhl_bible_mcp/api/endpoints.py` (5 個方法修改)
- `src/fhl_bible_mcp/utils/booknames.py` (書卷定義擴展)
- `src/fhl_bible_mcp/tools/search.py` (參數型別處理)

---

## [0.1.0] - 2025-11-03

### Added

- 初始版本發布
- 27 個工具函數
  - 經文查詢 (聖經、次經、使徒教父)
  - 原文研究 (Strong's 字典、字彙分析)
  - 註釋研經
  - 文章搜尋
  - 多媒體 (有聲聖經)
- 19 個專業對話範本 (Basic/Reading/Study/Special/Advanced)
- MCP Server 基礎架構
- 完整的安裝腳本和配置工具
- 83% 測試覆蓋率 (160 個測試通過)

### Documentation

- 完整的開發指南
- API 參考文檔
- Prompts 使用指南
- 安裝指南
- 5 個主題文檔目錄 (1_development 到 5_api_enhancement)

---

## Links

- [完整文檔](docs/README.md)
- [Bug 修復報告](docs/6_bug_fix/README.md)
- [開發指南](docs/1_development/DEVELOPER_GUIDE.md)
- [API 文檔](docs/4_manuals/API.md)
