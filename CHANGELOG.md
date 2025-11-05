# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- 所有 5 個 bug 已驗證修復 (100%)
- 測試涵蓋:
  - 經文查詢 (聖經、次經、使徒教父)
  - Strong's 字典查詢
  - 原文分析 (希臘文、希伯來文)
  - 註釋查詢
  - 參數型別驗證 (整數、字串、書卷名)

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
