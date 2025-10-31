# FHL Bible MCP Server 📖

> A Model Context Protocol (MCP) server for accessing the Faith, Hope, Love (信望愛站) Bible API.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io/)
[![Test Coverage](https://img.shields.io/badge/coverage-83%25-brightgreen.svg)](docs/PHASE_4_2_FINAL_REPORT.md)
[![Tests](https://img.shields.io/badge/tests-160%20passed-success.svg)](docs/PHASE_4_2_FINAL_REPORT.md)

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

### Prerequisites

- Python 3.10 或更高版本
- pip 或 poetry

### Installation

1. **Clone 專案**

```bash
git clone https://github.com/yourusername/fhl-bible-mcp.git
cd fhl-bible-mcp
```

2. **建立虛擬環境**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows PowerShell
```

3. **安裝套件**

```bash
pip install -e .
# 或安裝開發版本
pip install -e ".[dev]"
```

### Usage with Claude Desktop

1. 在 Claude Desktop 的設定檔中加入此 MCP Server：

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": ["-m", "fhl_bible_mcp"],
      "env": {}
    }
  }
}
```

2. 重啟 Claude Desktop

3. 開始使用！例如：
   - "請幫我查詢約翰福音 3:16"
   - "搜尋聖經中所有提到『愛』的經文"
   - "分析約翰福音 3:16 的希臘文原文"

## 📚 Available Tools

### 經文查詢
- `get_bible_verse` - 查詢指定章節的聖經經文
- `search_bible` - 在聖經中搜尋關鍵字

### 原文研究
- `get_word_analysis` - 取得經文的字彙分析
- `lookup_strongs` - 查詢 Strong's 原文字典

### 註釋研經
- `get_commentary` - 取得聖經註釋
- `search_commentary` - 搜尋註釋內容
- `get_topic_study` - 查詢主題查經

### 資訊工具
- `list_bible_versions` - 列出所有可用的聖經版本
- `list_commentaries` - 列出所有可用的註釋書
- `get_book_list` - 取得聖經書卷列表

### 多媒體
- `get_audio_bible` - 取得有聲聖經連結

更多詳細說明請參閱 [完整文件](docs/TOOLS.md)。

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
> 📚 詳細說明請參閱 [Prompts 使用指南](docs/PROMPTS_USAGE_GUIDE.md)

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
- **API 文件**: https://bible.fhl.net/json/
- **版權說明**: https://www.fhl.net/main/fhl/fhl8.html

## 📝 License

本專案採用 MIT License - 詳見 [LICENSE](LICENSE) 檔案。

注意：此授權僅適用於本專案的程式碼，不包含透過 API 取得的聖經內容。聖經內容的版權歸屬於各譯本的版權方。

## 🤝 Contributing

歡迎貢獻！請參閱 [貢獻指南](CONTRIBUTING.md)。

## 📮 Contact

如有問題或建議，請開 [Issue](https://github.com/yourusername/fhl-bible-mcp/issues)。

## 🙏 Acknowledgments

- 感謝信望愛站（Faith, Hope, Love）提供豐富的聖經資源 API
- 感謝 Anthropic 開發 Model Context Protocol
- 感謝所有貢獻者

## � 專案狀態

- ✅ **Phase 1**: API 客戶端實作 - 完成
- ✅ **Phase 2**: MCP Server 核心功能 - 完成
- ✅ **Phase 3**: 進階功能與優化 - 完成
- ✅ **Phase 4.1**: 全面測試套件 - 完成 (138 測試)
- ✅ **Phase 4.2**: E2E 測試與文檔 - 完成 (160 測試, 83% 覆蓋率)
- ✅ **Phase 5**: Prompts 增強計劃 - 完成 (19 個 Prompts) 🎊

### 🎯 測試統計

```
總測試數:    160 個
通過率:      100% ✅
程式碼覆蓋率: 83% 🚀
100% 覆蓋模組: 12 個
```

詳細測試報告請參考 [PHASE_4_2_FINAL_REPORT.md](docs/PHASE_4_2_FINAL_REPORT.md)

## �📚 Documentation

- **[API 完整文件](docs/API.md)** - 所有 Tools、Resources、Prompts 的詳細說明
- **[開發者指南](docs/DEVELOPER_GUIDE.md)** - 架構說明與貢獻指南
- **[使用範例](docs/EXAMPLES.md)** - Claude Desktop 整合與實際案例
- **[測試報告](docs/PHASE_4_2_FINAL_REPORT.md)** - 完整測試覆蓋率報告
- **[規劃文件](docs/FHL_BIBLE_MCP_PLANNING.md)** - 專案規劃與 API 分析

---

**Made with ❤️ for Bible study and research | 讓 AI 成為您的聖經研究助手！** 🙏
