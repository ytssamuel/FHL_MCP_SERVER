# FHL Bible MCP Server 安裝指南 🚀

**完整的跨平台安裝與配置教學**

---

## 📋 目錄

- [系統需求](#系統需求)
- [安裝步驟](#安裝步驟)
- [AI 助手配置](#ai-助手配置)
  - [Claude Desktop (推薦)](#選項-1-claude-desktop-推薦-)
  - [GitHub Copilot (VS Code)](#選項-2-github-copilot-vs-code)
  - [OpenAI Desktop (ChatGPT)](#選項-3-openai-desktop-chatgpt)
- [驗證安裝](#驗證安裝)
- [疑難排解](#疑難排解)
- [進階配置](#進階配置)

---

## 系統需求

### 必要條件

- **Python**: 3.10 或更高版本
  - Windows: [Python 官網下載](https://www.python.org/downloads/)
  - macOS: `brew install python@3.10` 或從官網下載
  - Linux: `sudo apt install python3.10` (Ubuntu/Debian) 或使用發行版的套件管理器

- **pip**: Python 套件管理器（通常隨 Python 一起安裝）

- **Git** (可選，建議安裝):
  - Windows: [Git for Windows](https://git-scm.com/download/win)
  - macOS: `brew install git` 或使用 Xcode Command Line Tools
  - Linux: `sudo apt install git`

### AI 助手（至少選擇一個）

- ✅ [Claude Desktop](https://claude.ai/download) - **推薦**，MCP 支援最完整
- ✅ [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) - VS Code 擴充功能
- ✅ [OpenAI Desktop](https://openai.com/chatgpt/desktop/) - ChatGPT 桌面版 (Beta)

---

## 安裝步驟

### Step 1: 下載專案

#### 方法 A: 使用 Git Clone（推薦）

**所有平台**:
```bash
git clone https://github.com/ytssamuel/FHL_MCP_SERVER.git
cd FHL_MCP_SERVER
```

#### 方法 B: 下載 ZIP 檔案

1. 前往 [GitHub Repository](https://github.com/ytssamuel/FHL_MCP_SERVER)
2. 點擊綠色的 "Code" 按鈕
3. 選擇 "Download ZIP"
4. 解壓縮到您想要的位置
5. 在終端機/命令提示字元中進入該目錄

---

### Step 2: 建立 Python 虛擬環境

虛擬環境可以隔離專案依賴，避免與系統 Python 套件衝突。

#### Windows (PowerShell)

```powershell
# 確認 Python 版本
python --version

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1
```

> 💡 **提示**: 如果遇到執行政策錯誤，請以管理員身份執行 PowerShell 並執行：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### macOS / Linux (Bash/Zsh)

```bash
# 確認 Python 版本
python3 --version

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate
```

**確認虛擬環境已啟動**:
- Windows: 提示字元前會顯示 `(venv)`
- macOS/Linux: 終端機前會顯示 `(venv)`

---

### Step 3: 安裝 Python 套件

確認虛擬環境已啟動後，安裝專案依賴：

```bash
# 標準安裝（使用者）
pip install -e .

# 開發版本（包含測試工具，開發者使用）
pip install -e ".[dev]"
```

**等待安裝完成**，應該會看到類似以下訊息：
```
Successfully installed fhl-bible-mcp-0.1.0 ...
```

---

### Step 4: 驗證安裝

測試 MCP Server 是否可以正常啟動：

```bash
python -m fhl_bible_mcp.server
```

**預期輸出**:
```
MCP Server initialized successfully
Server running on stdio...
```

看到這些訊息表示安裝成功！按 `Ctrl+C` 停止 server。

---

## AI 助手配置

現在您需要配置至少一個 AI 助手來使用 FHL Bible MCP Server。

---

## 選項 1: Claude Desktop (推薦) 🌟

Claude Desktop 是目前對 MCP 支援最完整、最穩定的選擇。

### 1.1 安裝 Claude Desktop

- **下載**: [claude.ai/download](https://claude.ai/download)
- **平台**: Windows 10+, macOS 10.15+, Linux (AppImage)
- **需求**: Anthropic 帳號（免費註冊）

### 1.2 找到配置文件位置

Claude Desktop 使用 JSON 配置文件來管理 MCP Servers。

| 平台 | 配置文件路徑 |
|------|-------------|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

**快速打開配置文件**:

**Windows (PowerShell)**:
```powershell
# 查看配置文件
notepad "$env:APPDATA\Claude\claude_desktop_config.json"

# 如果文件不存在，創建它
if (!(Test-Path "$env:APPDATA\Claude\claude_desktop_config.json")) {
    New-Item -Path "$env:APPDATA\Claude\claude_desktop_config.json" -ItemType File -Force
}
```

**macOS (Terminal)**:
```bash
# 查看配置文件
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 如果文件不存在，創建它
mkdir -p ~/Library/Application\ Support/Claude
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux**:
```bash
# 查看配置文件
nano ~/.config/Claude/claude_desktop_config.json

# 如果文件不存在，創建它
mkdir -p ~/.config/Claude
touch ~/.config/Claude/claude_desktop_config.json
```

### 1.3 獲取 Python 可執行文件的完整路徑

**重要**: 必須使用虛擬環境中 Python 的**完整絕對路徑**。

#### Windows (PowerShell)

```powershell
# 進入專案目錄
cd C:\path\to\FHL_MCP_SERVER

# 獲取 Python 路徑
(Get-Item .\venv\Scripts\python.exe).FullName
```

**範例輸出**:
```
C:\Users\YourName\Desktop\FHL_MCP_SERVER\venv\Scripts\python.exe
```

#### macOS / Linux (Terminal)

```bash
# 進入專案目錄
cd /path/to/FHL_MCP_SERVER

# 獲取 Python 路徑
realpath venv/bin/python
```

**範例輸出**:
```
/Users/YourName/Desktop/FHL_MCP_SERVER/venv/bin/python
```

**複製這個路徑**，下一步會用到。

### 1.4 編輯配置文件

打開配置文件，添加或修改為以下內容：

#### Windows 配置範例

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "C:\\Users\\YourName\\Desktop\\FHL_MCP_SERVER\\venv\\Scripts\\python.exe",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

> ⚠️ **Windows 路徑注意事項**:
> - 必須使用雙反斜線 `\\` 或單斜線 `/`
> - 路徑中的每個 `\` 都要寫成 `\\`
> - 或者全部改用 `/`: `C:/Users/YourName/Desktop/...`

#### macOS / Linux 配置範例

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "/Users/YourName/Desktop/FHL_MCP_SERVER/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

**如果您已有其他 MCP Servers**，添加到現有配置中：

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "fhl-bible": {
      "command": "/path/to/FHL_MCP_SERVER/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

### 1.5 重啟 Claude Desktop

1. **完全關閉** Claude Desktop（確保不在背景執行）
   - Windows: 工作管理員中確認沒有 Claude 程序
   - macOS: `Cmd+Q` 完全退出
   - Linux: `killall claude` 確保完全關閉

2. **重新啟動** Claude Desktop

3. 等待幾秒鐘讓 MCP Server 初始化

### 1.6 驗證連接

在 Claude 對話框中輸入以下任一指令：

```
請列出所有可用的聖經版本
```

或

```
查詢約翰福音 3:16
```

或

```
使用 basic_help_guide 查看完整功能
```

**成功指標**:
- ✅ Claude 回應聖經相關內容
- ✅ 能看到經文、版本列表等資訊
- ✅ 沒有錯誤訊息

**如果成功，恭喜！您已完成 Claude Desktop 的配置！** 🎉

### 1.7 疑難排解 (Claude Desktop)

#### 問題 1: Server 未連接或找不到

**檢查 Claude 日誌**:

- **Windows**: `%APPDATA%\Claude\logs\`
- **macOS**: `~/Library/Logs/Claude/`
- **Linux**: `~/.config/Claude/logs/`

找到最新的日誌文件，查看錯誤訊息。

**常見錯誤**:

**錯誤**: `Command not found` 或 `python: command not found`

**解決**: 使用完整絕對路徑，不要使用 `python` 或 `python3`

```json
{
  "command": "C:\\full\\path\\to\\venv\\Scripts\\python.exe"  // Windows
  "command": "/full/path/to/venv/bin/python"  // macOS/Linux
}
```

**錯誤**: `Module not found: fhl_bible_mcp`

**解決**: 
1. 確認虛擬環境中已安裝套件：
   ```bash
   # 啟動虛擬環境
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   
   # 檢查安裝
   pip list | grep fhl-bible-mcp
   ```

2. 如果沒有，重新安裝：
   ```bash
   pip install -e .
   ```

**錯誤**: `Permission denied`

**解決** (macOS/Linux):
```bash
chmod +x venv/bin/python
```

#### 問題 2: JSON 格式錯誤

**症狀**: Claude Desktop 啟動失敗或沒有反應

**解決**: 
1. 使用 [JSONLint](https://jsonlint.com/) 驗證 JSON 格式
2. 確認所有引號、逗號、括號都正確
3. 使用線上工具或 VS Code 的 JSON 驗證

#### 問題 3: 路徑包含空格或特殊字元

**Windows 範例**:
```json
{
  "command": "C:\\Program Files\\FHL_MCP_SERVER\\venv\\Scripts\\python.exe"
}
```

確保路徑用引號包圍，雙反斜線正確。

**macOS/Linux 範例**:
```json
{
  "command": "/Users/Your Name/Documents/FHL_MCP_SERVER/venv/bin/python"
}
```

空格不需要跳脫，但整個路徑必須在引號內。

---

## 選項 2: GitHub Copilot (VS Code)

GitHub Copilot Chat 現在支援 MCP，讓您在編碼時也能查詢聖經！

### 2.1 前置要求

1. **安裝 VS Code**: [code.visualstudio.com](https://code.visualstudio.com/)

2. **安裝 GitHub Copilot 擴充功能**:
   - 打開 VS Code
   - 按 `Ctrl+Shift+X` (macOS: `Cmd+Shift+X`) 打開擴充功能面板
   - 搜尋 "GitHub Copilot"
   - 安裝以下兩個擴充功能：
     - **GitHub Copilot** (必須)
     - **GitHub Copilot Chat** (必須)

3. **GitHub Copilot 訂閱**:
   - 需要 GitHub Copilot 個人版、商業版或企業版訂閱
   - 學生和開源貢獻者可能有免費方案
   - 前往 [GitHub Copilot](https://github.com/features/copilot) 了解更多

4. **登入 GitHub 帳號**:
   - 在 VS Code 中，點擊左下角的帳號圖示
   - 選擇 "Sign in to Sync Settings"
   - 使用 GitHub 帳號登入

### 2.2 獲取 Python 路徑

與 Claude Desktop 相同，獲取虛擬環境中 Python 的完整路徑：

**Windows**:
```powershell
cd C:\path\to\FHL_MCP_SERVER
(Get-Item .\venv\Scripts\python.exe).FullName
```

**macOS/Linux**:
```bash
cd /path/to/FHL_MCP_SERVER
realpath venv/bin/python
```

### 2.3 配置 VS Code 設定

#### 方法 A: 使用設定介面（推薦）

1. 打開 VS Code 設定:
   - Windows/Linux: `Ctrl+,`
   - macOS: `Cmd+,`

2. 點擊右上角的 **Open Settings (JSON)** 圖示 (文件圖示)

3. 這會打開 `settings.json` 文件

#### 方法 B: 直接編輯 settings.json

**快速打開**:
- Windows/Linux: `Ctrl+Shift+P` → 輸入 "Preferences: Open User Settings (JSON)"
- macOS: `Cmd+Shift+P` → 輸入 "Preferences: Open User Settings (JSON)"

**設定文件位置**:
- Windows: `%APPDATA%\Code\User\settings.json`
- macOS: `~/Library/Application Support/Code/User/settings.json`
- Linux: `~/.config/Code/User/settings.json`

### 2.4 添加 MCP Server 配置

在 `settings.json` 中添加以下內容：

#### Windows 配置

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "fhl-bible": {
      "command": "C:\\Users\\YourName\\Desktop\\FHL_MCP_SERVER\\venv\\Scripts\\python.exe",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

#### macOS / Linux 配置

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "fhl-bible": {
      "command": "/Users/YourName/Desktop/FHL_MCP_SERVER/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

**如果您已有其他設定**，將 MCP 相關配置合併進去：

```json
{
  "editor.fontSize": 14,
  "workbench.colorTheme": "Dark+",
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "fhl-bible": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

### 2.5 重新載入 VS Code

1. 按 `F1` 或 `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`)
2. 輸入 "Developer: Reload Window"
3. 按 Enter

或者完全關閉並重新啟動 VS Code。

### 2.6 驗證連接

1. **打開 Copilot Chat**:
   - 按 `Ctrl+Shift+I` (macOS: `Cmd+Shift+I`)
   - 或點擊側邊欄的 Chat 圖示

2. **測試 MCP Server**:

在 Copilot Chat 中輸入：

```
@fhl-bible 查詢約翰福音 3:16
```

或

```
@fhl-bible 列出所有可用的聖經版本
```

或

```
@fhl-bible 使用 basic_help_guide 查看功能
```

**成功指標**:
- ✅ Copilot 識別 `@fhl-bible` 標籤
- ✅ 返回聖經相關內容
- ✅ 沒有錯誤訊息

**如果成功，恭喜！您已完成 GitHub Copilot 的配置！** 🎉

### 2.7 使用技巧

**在 Copilot Chat 中使用 MCP**:

```
# 基礎查詢
@fhl-bible 搜尋聖經中關於「愛」的經文

# 深度研究
@fhl-bible 分析約翰福音 1:1 的希臘文原文

# 使用 Prompts
@fhl-bible 使用 study_verse_deep 研讀羅馬書 8:28

# 進階功能
@fhl-bible 使用 advanced_character_study 研究彼得
```

**在編輯器中使用**:

在任何檔案中，選取文字後右鍵 → "Copilot" → "Ask Copilot"，然後引用 `@fhl-bible`。

### 2.8 疑難排解 (GitHub Copilot)

#### 問題 1: 找不到 @fhl-bible

**症狀**: 輸入 `@fhl-bible` 時沒有自動完成建議

**解決**:
1. 確認 `github.copilot.chat.mcp.enabled` 設為 `true`
2. 檢查 `settings.json` 的 JSON 格式是否正確
3. 重新載入視窗或重啟 VS Code
4. 檢查 Copilot 是否已登入且訂閱有效

#### 問題 2: MCP Server 連接失敗

**查看錯誤訊息**:
1. 按 `Ctrl+Shift+U` (macOS: `Cmd+Shift+U`) 打開輸出面板
2. 在下拉選單選擇 "GitHub Copilot Chat"
3. 查看錯誤訊息

**常見解決方法**:
- 確認 Python 路徑正確
- 確認虛擬環境中已安裝套件
- 檢查路徑中的特殊字元和空格

#### 問題 3: Copilot 不識別 MCP 命令

**確認 MCP 功能已啟用**:

```json
{
  "github.copilot.chat.mcp.enabled": true
}
```

如果仍有問題，可能是 Copilot 版本太舊：
1. 更新 GitHub Copilot 擴充功能到最新版本
2. 檢查 VS Code 版本（建議 1.80+）

---

## 選項 3: OpenAI Desktop (ChatGPT)

OpenAI Desktop 的 MCP 支援目前處於 Beta 階段。

> ⚠️ **重要提示**: 
> - OpenAI Desktop 的 MCP 功能仍在開發中
> - 配置方式可能會頻繁變更
> - 建議優先使用 Claude Desktop 或 GitHub Copilot
> - 以下內容基於目前（2025 年 1 月）的 Beta 版本

### 3.1 前置要求

1. **安裝 OpenAI Desktop**:
   - 下載: [openai.com/chatgpt/desktop](https://openai.com/chatgpt/desktop/)
   - 平台: Windows 10+, macOS 11+

2. **ChatGPT 訂閱** (可能需要):
   - ChatGPT Plus ($20/月) 或
   - ChatGPT Pro ($200/月)
   - 免費版可能不支援 MCP 功能

3. **啟用 Beta 功能**:
   - 在 ChatGPT 設定中啟用實驗性功能

### 3.2 配置文件位置

| 平台 | 配置文件路徑 |
|------|-------------|
| **Windows** | `%APPDATA%\OpenAI\ChatGPT\mcp_config.json` |
| **macOS** | `~/Library/Application Support/OpenAI/ChatGPT/mcp_config.json` |

> 📝 **注意**: 配置文件路徑和格式可能會隨版本更新而變更。請查看 [OpenAI 官方文檔](https://platform.openai.com/docs/) 獲取最新資訊。

### 3.3 創建配置文件

配置文件可能不會自動創建，需要手動建立。

#### Windows (PowerShell)

```powershell
# 創建目錄
New-Item -Path "$env:APPDATA\OpenAI\ChatGPT" -ItemType Directory -Force

# 創建配置文件
New-Item -Path "$env:APPDATA\OpenAI\ChatGPT\mcp_config.json" -ItemType File -Force

# 打開配置文件
notepad "$env:APPDATA\OpenAI\ChatGPT\mcp_config.json"
```

#### macOS (Terminal)

```bash
# 創建目錄
mkdir -p ~/Library/Application\ Support/OpenAI/ChatGPT

# 創建配置文件
touch ~/Library/Application\ Support/OpenAI/ChatGPT/mcp_config.json

# 打開配置文件
open -e ~/Library/Application\ Support/OpenAI/ChatGPT/mcp_config.json
```

### 3.4 獲取 Python 路徑

與前面相同，獲取虛擬環境中 Python 的完整路徑：

**Windows**:
```powershell
cd C:\path\to\FHL_MCP_SERVER
(Get-Item .\venv\Scripts\python.exe).FullName
```

**macOS**:
```bash
cd /path/to/FHL_MCP_SERVER
realpath venv/bin/python
```

### 3.5 編輯配置文件

將以下內容添加到配置文件：

#### Windows 配置

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "C:\\Users\\YourName\\Desktop\\FHL_MCP_SERVER\\venv\\Scripts\\python.exe",
      "args": ["-m", "fhl_bible_mcp.server"],
      "enabled": true,
      "autoStart": true
    }
  }
}
```

#### macOS 配置

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "/Users/YourName/Desktop/FHL_MCP_SERVER/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "enabled": true,
      "autoStart": true
    }
  }
}
```

### 3.6 啟用 MCP 功能

1. 打開 OpenAI Desktop
2. 點擊左下角的 **設定** 圖示 (齒輪)
3. 找到 **Beta Features** 或 **實驗性功能**
4. 啟用 **Model Context Protocol** 選項
5. 如果找不到此選項，可能您的帳號或版本不支援 MCP

### 3.7 重啟 OpenAI Desktop

完全關閉並重新啟動應用程式：

**Windows**:
- 右鍵工作列的 ChatGPT 圖示
- 選擇 "退出"
- 重新啟動

**macOS**:
- `Cmd+Q` 完全退出
- 重新啟動

### 3.8 驗證連接

在 ChatGPT 對話框中輸入：

```
查詢約翰福音 3:16（使用 FHL Bible MCP）
```

或

```
使用 FHL Bible MCP Server 搜尋聖經中關於「愛」的經文
```

> 📝 **注意**: OpenAI Desktop 的 MCP 調用方式可能與 Claude 不同，可能需要明確指定使用 MCP Server。

### 3.9 疑難排解 (OpenAI Desktop)

#### 問題 1: 找不到配置選項

**可能原因**:
- 您的帳號類型不支援 MCP（需要 Plus 或 Pro）
- OpenAI Desktop 版本太舊
- MCP 功能尚未對您的地區開放

**解決**:
1. 確認您的訂閱計劃
2. 更新 OpenAI Desktop 到最新版本
3. 查看 [OpenAI Status](https://status.openai.com/) 確認功能可用性

#### 問題 2: MCP Server 無法啟動

**查看日誌** (如果有):
- Windows: `%APPDATA%\OpenAI\ChatGPT\logs\`
- macOS: `~/Library/Logs/OpenAI/ChatGPT/`

**常見解決方法**:
- 確認配置文件格式正確（JSON 驗證）
- 確認 Python 路徑正確
- 嘗試手動啟動 server 測試：
  ```bash
  python -m fhl_bible_mcp.server
  ```

#### 問題 3: 功能限制

由於 MCP 支援仍在 Beta 階段，可能會有以下限制：
- 某些 MCP 功能不可用
- 回應速度較慢
- 偶爾連接不穩定

**建議**: 如果 OpenAI Desktop 的 MCP 功能不穩定，請考慮使用 Claude Desktop 或 GitHub Copilot 作為主要選擇。

---

## 驗證安裝

無論您選擇哪個 AI 助手，都可以使用以下測試來驗證安裝是否成功。

### 基礎測試

```
查詢約翰福音 3:16
```

**預期結果**: 應該顯示約翰福音 3:16 的經文內容。

### 功能測試

```
列出所有可用的聖經版本
```

**預期結果**: 應該列出多個聖經版本（和合本、KJV、NIV 等）。

### Prompt 測試

```
使用 basic_help_guide 查看完整功能
```

**預期結果**: 應該顯示完整的功能介紹和使用說明。

### 進階測試

```
使用 study_verse_deep 深入研讀羅馬書 8:28
```

**預期結果**: 應該提供詳細的經文分析，包括原文、註釋、應用等。

---

## 疑難排解

### 常見問題彙整

#### Q1: Python 版本太舊

**錯誤訊息**: `Python 3.10 or higher is required`

**解決**:
1. 下載並安裝 Python 3.10+
2. 重新建立虛擬環境
3. 重新安裝套件

#### Q2: 找不到模組

**錯誤訊息**: `ModuleNotFoundError: No module named 'fhl_bible_mcp'`

**解決**:
```bash
# 確認虛擬環境已啟動
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 重新安裝
pip install -e .

# 驗證安裝
pip list | grep fhl-bible-mcp
```

#### Q3: 權限錯誤

**Windows**: 以管理員身份執行 PowerShell

**macOS/Linux**:
```bash
# 給予執行權限
chmod +x venv/bin/python
chmod +x venv/bin/pip
```

#### Q4: 虛擬環境無法啟動

**Windows PowerShell 執行政策錯誤**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux PATH 問題**:
```bash
# 確認 python3 在 PATH 中
which python3

# 如果找不到，安裝 Python 3
```

#### Q5: AI 助手無法連接 MCP Server

**檢查清單**:
- [ ] 配置文件 JSON 格式正確
- [ ] Python 路徑是完整絕對路徑
- [ ] 虛擬環境中已安裝套件
- [ ] AI 助手已完全重啟
- [ ] 沒有防火牆阻擋

**調試步驟**:
1. 手動啟動 server 測試：
   ```bash
   python -m fhl_bible_mcp.server
   ```
2. 查看 AI 助手的日誌文件
3. 嘗試使用絕對路徑的另一種寫法（`\\` vs `/`）

#### Q6: 路徑包含非 ASCII 字元

**症狀**: 路徑中有中文或其他非 ASCII 字元導致錯誤

**解決**:
1. 將專案移動到只包含英文和數字的路徑
2. 或在配置文件中使用 UTF-8 編碼
3. Windows: 考慮使用短路徑 `dir /x` 查看

---

## 進階配置

### 環境變數

您可以在配置文件中添加環境變數：

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "/path/to/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {
        "FHL_API_TIMEOUT": "30",
        "FHL_CACHE_ENABLED": "true",
        "PYTHONPATH": "/path/to/FHL_MCP_SERVER/src"
      }
    }
  }
}
```

### 多個 AI 助手同時使用

您可以在多個 AI 助手中同時配置 FHL Bible MCP Server：

1. 在 Claude Desktop 配置
2. 在 VS Code (Copilot) 配置
3. 在 OpenAI Desktop 配置

它們會各自獨立運行，互不干擾。

### 更新 MCP Server

當有新版本時：

```bash
# 進入專案目錄
cd /path/to/FHL_MCP_SERVER

# 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# 拉取最新代碼
git pull

# 重新安裝
pip install -e . --upgrade

# 重啟 AI 助手
```

### 開發模式

如果您想修改代碼並即時測試：

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 格式化代碼
black src/

# 類型檢查
mypy src/
```

---

## 獲取幫助

### 文檔資源

- **使用指南**: [PROMPTS_USAGE_GUIDE.md](../2_prompts_enhancement/PROMPTS_USAGE_GUIDE.md)
- **快速參考**: [PROMPTS_QUICK_REFERENCE.md](../4_manuals/PROMPTS_QUICK_REFERENCE.md)
- **使用範例**: [EXAMPLES.md](../4_manuals/EXAMPLES.md)
- **API 文檔**: [API.md](../4_manuals/API.md)

### 社群支援

- **GitHub Issues**: [提交問題](https://github.com/ytssamuel/FHL_MCP_SERVER/issues)
- **GitHub Discussions**: [參與討論](https://github.com/ytssamuel/FHL_MCP_SERVER/discussions)

### 聯絡方式

如有任何問題，歡迎：
1. 在 GitHub 上開 Issue
2. 查看現有的 Issues 和 Discussions
3. 參考 [疑難排解](#疑難排解) 區塊

---

## 下一步

安裝完成後，建議您：

1. 📖 閱讀 [Prompts 使用指南](../2_prompts_enhancement/PROMPTS_USAGE_GUIDE.md) 了解 19 個 prompts
2. ⚡ 查看 [快速參考卡](../4_manuals/PROMPTS_QUICK_REFERENCE.md) 快速上手
3. 💡 瀏覽 [使用範例](../4_manuals/EXAMPLES.md) 看實際應用場景
4. 🎯 嘗試使用 `basic_help_guide` prompt 獲取完整功能介紹

---

**安裝指南結束 | Made with ❤️ for Bible study** 🙏

**最後更新**: 2025 年 1 月 | **版本**: 1.0
