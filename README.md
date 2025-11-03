# FHL Bible MCP Server 📖

> A Model Context Protocol (MCP) server for accessing the Faith, Hope, Love (信望愛站) Bible API.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io/)
[![Test Coverage](https://img.shields.io/badge/coverage-83%25-brightgreen.svg)](docs/1_development/PHASE_4_2_FINAL_REPORT.md)
[![Tests](https://img.shields.io/badge/tests-160%20passed-success.svg)](docs/1_development/PHASE_4_2_FINAL_REPORT.md)

## 📖 Overview

FHL Bible MCP Server 是一個基於 Model Context Protocol 的伺服器，整合了信望愛站提供的豐富聖經資源 API。透過此 MCP Server，AI 助手（如 Claude）可以直接查詢聖經經文、原文字彙分析、註釋書、主題查經等專業研經資源。

### ✨ 主要功能

- 🔍 **經文查詢**: 支援多種聖經譯本（和合本、KJV、現代中文譯本等）
- 📚 **原文研究**: 提供希臘文、希伯來文字彙分析與 Strong's 字典
- 💡 **註釋研經**: 查詢多種註釋書與牧師講道內容
- 🔎 **經文搜尋**: 關鍵字搜尋與進階原文編號搜尋
- 🎯 **主題查經**: 查詢主題相關的聖經教導
- 🎵 **有聲聖經**: 取得多語言有聲聖經連結
- 🌏 **繁簡支援**: 完整支援繁體/簡體中文切換

## 🚀 Quick Start

### 🎯 方法一：一鍵安裝（推薦）

使用自動化安裝腳本，快速完成環境配置：

```bash
# 1. 下載專案
git clone https://github.com/ytssamuel/FHL_MCP_SERVER.git
cd FHL_MCP_SERVER

# 2. 執行一鍵安裝
# Windows:
.\scripts\install.bat

# macOS/Linux:
chmod +x scripts/install.sh
bash scripts/install.sh

# 3. 生成配置（互動式）
python scripts/generate_config.py
```

**腳本功能**:
- ✅ 自動檢查 Python 版本
- ✅ 建立虛擬環境
- ✅ 安裝所有依賴
- ✅ 驗證安裝結果
- ✅ 生成 AI 助手配置

### 📝 方法二：手動安裝

1. **下載專案**
   ```bash
   git clone https://github.com/ytssamuel/FHL_MCP_SERVER.git
   cd FHL_MCP_SERVER
   ```

2. **安裝依賴**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   pip install -e .

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. **配置 AI 助手**
   
   使用自動生成腳本（推薦）：
   ```bash
   python scripts/generate_config.py
   ```
   
   或選擇您偏好的 AI 助手手動添加配置：

   <details>
   <summary><b>Claude Desktop 配置</b> (推薦) ⭐</summary>

   編輯配置文件（`%APPDATA%\Claude\claude_desktop_config.json` on Windows 或 `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS）：

   **Windows:**
   ```json
   {
     "mcpServers": {
       "fhl-bible": {
         "command": "python",
         "args": ["-m", "fhl_bible_mcp.server"],
         "env": {
           "PYTHONPATH": "C:\\path\\to\\FHL_MCP_SERVER\\src",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

   **macOS/Linux:**
   ```json
   {
     "mcpServers": {
       "fhl-bible": {
         "command": "python3",
         "args": ["-m", "fhl_bible_mcp.server"],
         "env": {
           "PYTHONPATH": "/path/to/FHL_MCP_SERVER/src",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```
   </details>

   <details>
   <summary><b>GitHub Copilot (VS Code) 配置</b> 💻</summary>

   編輯 VS Code 設定（`settings.json`）：

   **Windows:**
   ```json
   {
     "github.copilot.chat.mcp.enabled": true,
     "github.copilot.chat.mcp.servers": {
       "fhl-bible": {
         "command": "C:\\path\\to\\FHL_MCP_SERVER\\venv\\Scripts\\python.exe",
         "args": ["-m", "fhl_bible_mcp.server"],
         "env": {
           "PYTHONPATH": "C:\\path\\to\\FHL_MCP_SERVER\\src",
           "LOG_LEVEL": "INFO",
           "FHL_CACHE_DIR": "C:\\path\\to\\FHL_MCP_SERVER\\.cache"
         }
       }
     }
   }
   ```

   **macOS/Linux:**
   ```json
   {
     "github.copilot.chat.mcp.enabled": true,
     "github.copilot.chat.mcp.servers": {
       "fhl-bible": {
         "command": "/path/to/FHL_MCP_SERVER/venv/bin/python",
         "args": ["-m", "fhl_bible_mcp.server"],
         "env": {
           "PYTHONPATH": "/path/to/FHL_MCP_SERVER/src",
           "LOG_LEVEL": "INFO",
           "FHL_CACHE_DIR": "/path/to/FHL_MCP_SERVER/.cache"
         }
       }
     }
   }
   ```
   </details>

   > ⚠️ **重要**: 
   > - 將 `/path/to/FHL_MCP_SERVER` 替換為您的實際專案路徑
   > - Windows 路徑使用雙反斜線 `\\` 或單斜線 `/`
   > - `PYTHONPATH` 必須指向專案的 `src` 目錄

4. **開始使用**
   ```
   查詢約翰福音 3:16
   使用 basic_help_guide 查看完整功能
   ```

> 📖 **詳細安裝步驟**: 請參閱 **[完整安裝指南](docs/1_development/INSTALLATION_GUIDE.md)** 
> 
> 包含：
> - ✅ 跨平台詳細步驟 (Windows/macOS/Linux)
> - ✅ 三種 AI 助手完整配置教學
> - ✅ 常見問題疑難排解
> - ✅ 進階配置選項

---

## 🛠️ 安裝輔助工具

專案提供完整的自動化腳本，簡化安裝配置流程：

| 腳本 | 功能 | 使用時機 |
|------|------|----------|
| `quick_check.py` | 環境預檢 | 安裝前檢查 Python 版本和專案結構 |
| `install.bat/sh` | 一鍵安裝 | 自動建立環境、安裝依賴、驗證結果 |
| `verify_setup.py` | 環境驗證 | 安裝後全面檢查配置（9 項檢查）|
| `generate_config.py` | 配置生成 | 互動式生成 AI 助手配置檔 |

**快速使用**:
```bash
# 1. 安裝前檢查
python scripts/quick_check.py

# 2. 一鍵安裝
# Windows: .\scripts\install.bat
# Unix:    bash scripts/install.sh

# 3. 環境驗證
python scripts/verify_setup.py

# 4. 生成配置
python scripts/generate_config.py
```

詳細說明請參考 [scripts/README.md](scripts/README.md)

---

## 📚 Available Tools

### 經文查詢
- `get_bible_verse` - 查詢指定章節的聖經經文
- `get_bible_chapter` - 查詢整章聖經經文
- `search_bible` - 在聖經中搜尋關鍵字

### 原文研究
- `get_word_analysis` - 取得經文的字彙分析
- `lookup_strongs` - 查詢 Strong's 原文字典
- `search_by_strongs` - 以 Strong's Number 搜尋經文

### 註釋研經
- `get_commentary` - 取得聖經註釋
- `search_commentary` - 搜尋註釋內容
- `get_topic_study` - 查詢主題查經

### 次經與使徒教父 ⭐ NEW
- `get_apocrypha_verse` - 查詢次經經文（舊約次經 101-115）
- `get_apocrypha_chapter` - 查詢次經整章
- `search_apocrypha` - 搜尋次經內容
- `get_apostolic_fathers_verse` - 查詢使徒教父經文（201-217）
- `get_apostolic_fathers_chapter` - 查詢使徒教父整章
- `search_apostolic_fathers` - 搜尋使徒教父內容

### 註腳查詢 ⭐ NEW
- `get_footnote` - 查詢聖經註腳（目前支援 TCV 版本）

### 文章搜尋 ⭐ NEW
- `search_fhl_articles` - 搜尋信望愛站文章（8000+ 篇文章）
- `list_fhl_article_columns` - 列出可用的文章專欄

### 資訊工具
- `list_bible_versions` - 列出所有可用的聖經版本
- `list_commentaries` - 列出所有可用的註釋書
- `get_book_list` - 取得聖經書卷列表

### 多媒體
- `get_audio_bible` - 取得有聲聖經連結

**總計**: 27 個工具函數 | 更多詳細說明請參閱 [完整 API 文件](docs/4_manuals/API.md)。

## 🏗️ Architecture

```
FHL Bible MCP Server
├── Tools (工具) - 執行動作和查詢
├── Resources (資源) - 提供靜態/動態資料
└── Prompts (提示) - 預設對話範本
```

## 📖 Resources

本伺服器提供以下 URI schemes：

- `bible://verse/{version}/{book}/{chapter}/{verse}` - 查詢特定經文
- `bible://chapter/{version}/{book}/{chapter}` - 查詢整章經文
- `strongs://{testament}/{number}` - Strong's 字典資源
- `commentary://{book}/{chapter}/{verse}` - 註釋資源
- `info://versions` - 版本列表
- `info://books` - 書卷列表
- `info://commentaries` - 註釋書列表

## 🎯 Prompts

內建 **19 個**專業對話範本，涵蓋從入門到進階的完整研經需求：

### 📘 基礎類 (Basic) - 快速上手
- `basic_help_guide` - 完整使用指南，新手必讀
- `basic_uri_demo` - URI 使用示範，教您直接存取資源
- `basic_quick_lookup` - 快速查經，簡單方便
- `basic_tool_reference` - 工具參考手冊，詳細說明所有功能

### 📖 讀經類 (Reading) - 每日靈修
- `reading_daily` - 每日讀經計劃，結構化的靈修體驗
- `reading_chapter` - 整章讀經，深入理解一整章
- `reading_passage` - 段落讀經，跨章節經文研讀

### 🎓 研經類 (Study) - 深度研讀
- `study_verse_deep` - 深入研讀經文，專業解經分析
- `study_topic_deep` - 主題研究，全面探討聖經主題
- `study_translation_compare` - 版本比較，多譯本對照
- `study_word_original` - 原文字詞研究，希伯來文/希臘文分析

### 🎯 特殊類 (Special) - 專業應用
- `special_sermon_prep` - 講道準備，全方位備課資源
- `special_devotional` - 靈修材料，個人/小組/家庭適用
- `special_memory_verse` - 背經輔助，記憶技巧與計劃
- `special_topical_chain` - 主題串連，貫穿聖經的主題追蹤
- `special_bible_trivia` - 聖經問答，互動式知識測驗

### 🚀 進階類 (Advanced) - 專業研究
- `advanced_cross_reference` - 交叉引用分析，多層次引用網絡 (1-3 層深度)
- `advanced_parallel_gospels` - 符類福音對照，四福音平行比較
- `advanced_character_study` - 聖經人物研究，9 大維度全面分析

> 💡 **提示**: 使用 `basic_help_guide` prompt 查看完整功能介紹和使用教學！  
> 📚 詳細說明請參閱 [Prompts 使用指南](docs/2_prompts_enhancement/PROMPTS_USAGE_GUIDE.md)

## 🔧 Development

### Setup Development Environment

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 執行 linting
ruff check .

# 格式化程式碼
black .

# 型別檢查
mypy src/
```

### Project Structure

```
FHL_MCP_SERVER/
├── src/fhl_bible_mcp/
│   ├── api/          # API 客戶端
│   ├── models/       # 資料模型
│   ├── tools/        # MCP Tools
│   ├── resources/    # MCP Resources
│   ├── prompts/      # MCP Prompts
│   └── utils/        # 工具函式
├── tests/            # 測試
├── docs/             # 文件
└── pyproject.toml    # 專案設定
```

## ⚖️ Copyright Notice

### 重要聲明

本專案使用信望愛站（FHL）提供的聖經 API。請注意：

1. **聖經譯本版權**: 信望愛站上各個聖經譯本，有些僅授權給信望愛站使用。使用者必須查閱[版權說明](https://www.fhl.net/main/fhl/fhl8.html)，不得任意使用，以免違法。

2. **本專案角色**: 本 MCP Server 僅作為 API 的介面層，不儲存或重新分發任何經文內容。所有經文內容均即時從 FHL API 取得。

3. **合理使用**: 本專案為非商業性質的研經工具。使用者應遵守相關版權規定，在合理範圍內進行研經活動。

4. **開發者責任**: 本 MCP Server 開發者不對使用者違反版權的行為負責。使用者應自行確保其使用方式符合版權規定。

### 參考資源

- **信望愛站首頁**: https://www.fhl.net/
- **API 文件**: https://bible.fhl.net/api/ (升級版，包含 bid 欄位)
- **舊版 API**: https://bible.fhl.net/json/ (仍可使用)
- **版權說明**: https://www.fhl.net/main/fhl/fhl8.html

## 📝 License

本專案採用 MIT License - 詳見 [LICENSE](LICENSE) 檔案。

注意：此授權僅適用於本專案的程式碼，不包含透過 API 取得的聖經內容及文章。內容的版權歸屬於各譯本的版權方及信望愛站。

## 🤝 Contributing

歡迎貢獻！如有問題或建議，請開 Issue 討論。

## 📮 Contact

如有問題或建議，請開 [Issue](https://github.com/yourusername/fhl-bible-mcp/issues)。

## 🙏 Acknowledgments

- 感謝信望愛站（Faith, Hope, Love）提供豐富的聖經資源 API
- 感謝 Anthropic 開發 Model Context Protocol
- 感謝所有貢獻者

---

## 🎊 專案狀態

### 📈 開發進度

- ✅ **Phase 1**: API 客戶端實作 - 完成
- ✅ **Phase 2**: MCP Server 核心功能 - 完成
- ✅ **Phase 3**: 進階功能與優化 - 完成
- ✅ **Phase 4.1**: 全面測試套件 - 完成 (138 測試)
- ✅ **Phase 4.2**: E2E 測試與文檔 - 完成 (160 測試, 83% 覆蓋率)
- ✅ **Phase 5**: Prompts 增強計劃 - 完成 (19 個 Prompts)
- ✅ **Phase 6**: API 增強計劃 - 完成 (次經、使徒教父、註腳、文章) 🎊

### 🎯 功能統計

| 類別 | 數量 | 說明 |
|------|------|------|
| **工具函數** | 27 | 涵蓋經文查詢、原文研究、註釋、次經、使徒教父、註腳、文章搜尋 |
| **Prompts** | 19 | 基礎、讀經、研經、特殊、進階五大類 |
| **聖經版本** | 20+ | 中文、英文、多語言譯本 |
| **註釋書** | 10+ | 多種權威註釋資源 |
| **單元測試** | 160 | 100% 通過率 |
| **覆蓋率** | 83% | 高品質程式碼保證 |

### 📊 測試統計

```
總測試數:    160 個
通過率:      100% ✅
程式碼覆蓋率: 83% 🚀
100% 覆蓋模組: 12 個
```

詳細測試報告請參考 [PHASE_4_2_FINAL_REPORT.md](docs/1_development/PHASE_4_2_FINAL_REPORT.md)

## 📚 Documentation

### 📖 使用手冊
- **[API 完整文件](docs/4_manuals/API.md)** - 所有 Tools、Resources、Prompts 的詳細說明
- **[使用範例](docs/4_manuals/EXAMPLES.md)** - Claude Desktop 整合與實際案例
- **[Prompts 快速參考](docs/4_manuals/PROMPTS_QUICK_REFERENCE.md)** - 19 個 Prompts 速查表

### 👨‍💻 開發文件
- **[開發者指南](docs/1_development/DEVELOPER_GUIDE.md)** - 架構說明與貢獻指南
- **[安裝指南](docs/1_development/INSTALLATION_GUIDE.md)** - 詳細安裝步驟
- **[專案規劃](docs/1_development/FHL_BIBLE_MCP_PLANNING.md)** - 專案規劃與 API 分析
- **[測試報告](docs/1_development/PHASE_4_2_FINAL_REPORT.md)** - 完整測試覆蓋率報告

### 🎯 Prompts 相關
- **[Prompts 使用指南](docs/2_prompts_enhancement/PROMPTS_USAGE_GUIDE.md)** - 19 個 Prompts 完整教學
- **[Prompts 增強計劃](docs/2_prompts_enhancement/PROMPTS_ENHANCEMENT_PLAN.md)** - 15 個新 Prompts 設計文件
- **[Prompts 改進報告](docs/3_prompts_improvement/PROMPTS_COMPLETE_REFACTORING_REPORT.md)** - 重構優化記錄

### 📂 文件導航
- **[文件總覽](docs/README.md)** - 完整的文件結構導航

---

**Made with ❤️ for Bible study and research | 讓 AI 成為您的聖經研究助手！** 🙏
