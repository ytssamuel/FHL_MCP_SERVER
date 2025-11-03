# FHL Bible MCP Server - 使用說明

## Phase 2.4 完成: MCP Server 整合

### ✅ 完成項目

#### 1. Server 架構
- **FHLBibleServer 類別**: 主要 server 類別
- **初始化**: 自動載入 API Client, ResourceRouter, PromptManager
- **Handler 註冊**: 自動註冊 Tools, Resources, Prompts

#### 2. 整合元件

##### Tools (19 個工具函數)
- **Verse Tools** (3): get_bible_verse, get_bible_chapter, query_verse_citation
- **Search Tools** (2): search_bible, search_bible_advanced  
- **Strong's Tools** (3): get_word_analysis, lookup_strongs, search_strongs_occurrences
- **Commentary Tools** (4): get_commentary, list_commentaries, search_commentary, get_topic_study
- **Info Tools** (4): list_bible_versions, get_book_list, get_book_info, search_available_versions
- **Audio Tools** (3): get_audio_bible, list_audio_versions, get_audio_chapter_with_text

##### Resources (7 種 URI 類型)
- **bible://verse/{version}/{book}/{chapter}/{verse}** - 查詢經文
- **bible://chapter/{version}/{book}/{chapter}** - 查詢整章
- **strongs://{testament}/{number}** - Strong's 字典
- **commentary://{book}/{chapter}/{verse}** - 經文註釋
- **info://versions** - 聖經版本列表
- **info://books** - 書卷列表
- **info://commentaries** - 註釋書列表

##### Prompts (4 個範本)
- **study_verse** - 深入研讀經文 (6 步驟)
- **search_topic** - 主題研究 (6 步驟)
- **compare_translations** - 譯本比較 (6 步驟)
- **word_study** - 原文字彙研究 (7 步驟)

#### 3. 測試驗證
- ✅ Server 初始化測試
- ✅ Tools 註冊測試  
- ✅ Resources 註冊測試
- ✅ Prompts 註冊測試
- ✅ Handler 機制測試
- ✅ 元件整合測試

所有 6 個測試類別 100% 通過!

## 執行 Server

### 1. 直接執行
```powershell
python -m fhl_bible_mcp.server
```

### 2. 使用 stdio (標準輸入/輸出)
Server 使用 MCP stdio 協議,適合與 AI 助手整合:
```powershell
python -m fhl_bible_mcp.server | your_mcp_client
```

### 3. 測試 Server 初始化
```powershell
python tests/test_server/test_server_init.py
```

## Server 能力

### Tools API
Server 提供 19 個工具函數,支援:
- 經文查詢 (單節、多節、整章)
- 聖經搜尋 (關鍵字、原文編號)
- 原文字彙分析 (希臘文/希伯來文)
- 註釋解經
- 版本資訊
- 有聲聖經

### Resources API  
Server 支援 7 種 URI 資源:
- 直接透過 URI 存取經文和資料
- 支援 RESTful 風格的資源查詢
- 統一的錯誤處理

### Prompts API
Server 提供 4 個研經範本:
- 引導式聖經研讀
- 結構化研經步驟
- 整合工具函數呼叫

## Server 架構

```
FHLBibleServer
├── server: mcp.server.Server
├── endpoints: FHLAPIEndpoints (API 客戶端)
├── resource_router: ResourceRouter (資源路由)
└── prompt_manager: PromptManager (提示範本)

註冊的 Handlers:
├── @server.list_tools() → list[Tool]
├── @server.call_tool() → Sequence[TextContent]
├── @server.list_resources() → list[Resource]
├── @server.read_resource() → str
├── @server.list_prompts() → list[Prompt]
└── @server.get_prompt() → GetPromptResult
```

## 使用範例

### 在 AI 助手中使用

當 AI 助手連接到此 MCP Server 時,可以:

1. **查詢經文**:
   ```
   使用 get_bible_verse 工具查詢約翰福音 3:16
   ```

2. **存取資源**:
   ```
   讀取資源 bible://verse/unv/John/3/16
   ```

3. **使用提示範本**:
   ```
   使用 study_verse 提示研讀創世記 1:1
   ```

### 與 Claude Desktop 整合

在 Claude Desktop 配置文件中添加:
```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "cwd": "C:\\Users\\USER\\Desktop\\develope\\FHL_MCP_SERVER"
    }
  }
}
```

## 日誌記錄

Server 使用 Python logging 模組:
- Level: INFO
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- 記錄所有工具呼叫和資源存取

## 錯誤處理

Server 提供完整的錯誤處理:
- API 錯誤 (FHLAPIError 層次結構)
- Resource 錯誤 (ResourceError)
- Tool 呼叫錯誤 (返回錯誤訊息)
- 所有錯誤都會記錄到日誌

## 下一步

✅ **Phase 2.4 完成!**

接下來的開發方向:
- Phase 3: 功能增強 (快取、配置管理)
- Phase 4: 測試與文件
- Phase 5: 進階功能

## 技術細節

- Python: 3.10+
- MCP SDK: 1.19.0
- Protocol: stdio (標準輸入/輸出)
- API Base: https://bible.fhl.net/json/
- 非同步支援: 完整的 async/await

## 專案結構

```
src/fhl_bible_mcp/
├── server.py           # MCP Server 主程式 ⭐
├── api/
│   ├── client.py       # HTTP 客戶端
│   ├── endpoints.py    # API 端點
│   └── exceptions.py   # 異常定義
├── tools/              # 19 個工具函數
│   ├── verse.py
│   ├── search.py
│   ├── strongs.py
│   ├── commentary.py
│   ├── info.py
│   └── audio.py
├── resources/          # 資源處理器
│   └── handlers.py
└── prompts/            # 提示範本
    └── templates.py

tests/
└── test_server/
    └── test_server_init.py  # Server 測試 ⭐
```

## 授權

MIT License
