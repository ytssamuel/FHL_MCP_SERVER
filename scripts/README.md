# Scripts 資料夾

本資料夾包含 FHL Bible MCP Server 的安裝和驗證腳本。

## 📁 腳本清單

### 1. 一鍵安裝腳本

#### Windows
```bash
.\scripts\install.bat
```

#### macOS / Linux
```bash
chmod +x scripts/install.sh
bash scripts/install.sh
```

**功能**:
- ✅ 自動檢查 Python 版本
- ✅ 建立 Python 虛擬環境
- ✅ 安裝所有依賴套件
- ✅ 執行安裝驗證
- ✅ 顯示配置指引

---

### 2. 快速環境檢查

```bash
# 在安裝前執行，檢查基本環境
python scripts/quick_check.py
```

**檢查項目**:
- Python 版本 (>= 3.10)
- 作業系統相容性
- 必要專案文件

---

### 3. 完整環境驗證

```bash
# 在安裝後執行，全面驗證配置
python scripts/verify_setup.py
```

**驗證項目**:
- ✓ Python 版本
- ✓ 虛擬環境
- ✓ 專案結構
- ✓ 套件安裝
- ✓ 依賴檢查
- ✓ PYTHONPATH 設定
- ✓ Server 模組導入
- ✓ 快取目錄
- ✓ AI 助手配置

**輸出範例**:
```
========================================
FHL Bible MCP Server - 環境驗證
========================================

系統資訊:
  作業系統: Windows 10
  Python: 3.10.11
  專案目錄: C:\...\FHL_MCP_SERVER

開始驗證...

✓ PASS - Python 版本
      Python 3.10.11
✓ PASS - 虛擬環境
      虛擬環境: C:\...\venv
✓ PASS - 專案結構
      專案結構完整
...

總計: 9/9 項檢查通過

🎉 恭喜！所有檢查都通過！
```

---

### 4. 配置生成器

```bash
# 互動式生成 AI 助手配置
python scripts/generate_config.py
```

**功能**:
- 🎯 自動偵測專案路徑
- 📝 生成正確的配置文件
- 💾 選擇性寫入配置
- 🔄 支援配置合併

**支援的 AI 助手**:
1. Claude Desktop
2. VS Code / GitHub Copilot
3. 兩者都配置
4. 只顯示配置（不寫入）

**使用流程**:
```
請選擇要配置的 AI 助手:
1. Claude Desktop (推薦)
2. VS Code / GitHub Copilot
3. 兩者都要
4. 只顯示配置（不寫入文件）

請選擇 (1-4): 1

正在分析專案路徑...
專案目錄: /path/to/FHL_MCP_SERVER
Python 路徑: /path/to/venv/bin/python
PYTHONPATH: /path/to/FHL_MCP_SERVER/src

Claude Desktop 配置:
{
  "mcpServers": {
    "fhl-bible": {
      "command": "/path/to/FHL_MCP_SERVER/venv/bin/python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/FHL_MCP_SERVER/src",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}

⚠️ 重要: 使用虛擬環境的 Python (venv/bin/python)

確定要寫入配置文件嗎？(y/n): y
✓ 配置已成功寫入
```

---

## 🚀 快速開始流程

### 完整安裝流程

```bash
# 1. 下載專案
git clone https://github.com/ytssamuel/FHL_MCP_SERVER.git
cd FHL_MCP_SERVER

# 2. (可選) 快速檢查環境
python scripts/quick_check.py

# 3. 一鍵安裝
# Windows:
.\scripts\install.bat

# macOS/Linux:
chmod +x scripts/install.sh
bash scripts/install.sh

# 4. 生成配置
python scripts/generate_config.py

# 5. 重啟 AI 助手
# Claude Desktop: 完全關閉後重新啟動
# VS Code: Developer: Reload Window
```

---

## 💡 使用技巧

### 重新驗證環境

安裝後如果遇到問題，可以隨時重新驗證：

```bash
# 啟動虛擬環境
# Windows:
.\venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 執行驗證
python scripts/verify_setup.py
```

### 查看配置不寫入

如果只想查看配置範例而不實際修改配置文件：

```bash
python scripts/generate_config.py
# 選擇選項 4: 只顯示配置（不寫入文件）
```

### 手動配置

如果自動配置不適用，可以手動編輯配置文件：

**Claude Desktop**:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**VS Code**:
- Windows: `%APPDATA%\Code\User\settings.json`
- macOS: `~/Library/Application Support/Code/User/settings.json`
- Linux: `~/.config/Code/User/settings.json`

---

## 🔧 疑難排解

### 腳本執行權限問題 (macOS/Linux)

```bash
# 添加執行權限
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### PowerShell 執行政策錯誤 (Windows)

```powershell
# 以管理員身份執行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python 指令找不到

**Windows**:
- 確認 Python 已安裝並添加到 PATH
- 試試 `python` 或 `py`

**macOS/Linux**:
- 確認已安裝 Python 3.10+
- 試試 `python3` 或 `python3.10`

### 虛擬環境啟動失敗

**確保在專案根目錄**:
```bash
cd /path/to/FHL_MCP_SERVER
```

**重新建立虛擬環境**:
```bash
# 刪除舊的虛擬環境
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# 重新建立
python3 -m venv venv  # macOS/Linux
python -m venv venv   # Windows
```

---

## 📚 相關文檔

- **完整安裝指南**: [docs/1_development/INSTALLATION_GUIDE.md](../docs/1_development/INSTALLATION_GUIDE.md)
- **開發者指南**: [docs/1_development/DEVELOPER_GUIDE.md](../docs/1_development/DEVELOPER_GUIDE.md)
- **主 README**: [README.md](../README.md)

---

## 🤝 貢獻

如果您發現腳本有問題或有改進建議，歡迎提交 Issue 或 Pull Request！

---

**Made with ❤️ for FHL Bible MCP Server**
