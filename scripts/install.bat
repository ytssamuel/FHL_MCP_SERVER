@echo off
REM FHL Bible MCP Server - Windows 一鍵安裝腳本
REM 自動完成環境設定和套件安裝

echo ========================================
echo FHL Bible MCP Server - 一鍵安裝
echo ========================================
echo.

REM 檢查 Python
echo [1/6] 檢查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python！
    echo 請先安裝 Python 3.10 或更高版本
    echo 下載地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo [OK] Python 已安裝
echo.

REM 檢查是否在專案目錄
if not exist "pyproject.toml" (
    echo [ERROR] 請在專案根目錄執行此腳本
    echo 當前目錄: %CD%
    pause
    exit /b 1
)

echo [OK] 專案目錄確認
echo.

REM 建立虛擬環境
echo [2/6] 建立虛擬環境...
if exist "venv\" (
    echo [SKIP] 虛擬環境已存在
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] 建立虛擬環境失敗
        pause
        exit /b 1
    )
    echo [OK] 虛擬環境建立完成
)
echo.

REM 啟動虛擬環境
echo [3/6] 啟動虛擬環境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 啟動虛擬環境失敗
    pause
    exit /b 1
)
echo [OK] 虛擬環境已啟動
echo.

REM 升級 pip
echo [4/6] 升級 pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip 已升級
echo.

REM 安裝套件
echo [5/6] 安裝 FHL Bible MCP Server...
pip install -e . --quiet
if errorlevel 1 (
    echo [ERROR] 套件安裝失敗
    pause
    exit /b 1
)
echo [OK] 套件安裝完成
echo.

REM 驗證安裝
echo [6/6] 驗證安裝...
python scripts\verify_setup.py
if errorlevel 1 (
    echo.
    echo [WARNING] 部分檢查未通過，請查看上方訊息
    echo.
) else (
    echo.
    echo ========================================
    echo 安裝完成！
    echo ========================================
    echo.
)

echo 下一步：
echo 1. 配置 AI 助手（Claude Desktop 或 VS Code）
echo 2. 參考文檔：docs\1_development\INSTALLATION_GUIDE.md
echo.
echo 快速配置 Claude Desktop：
echo.
echo   配置文件：%%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo   配置內容（複製使用，記得替換路徑）：
echo   {
echo     "mcpServers": {
echo       "fhl-bible": {
echo         "command": "%CD%\\venv\\Scripts\\python.exe",
echo         "args": ["-m", "fhl_bible_mcp"],
echo         "env": {
echo           "PYTHONPATH": "%CD%\\src",
echo           "LOG_LEVEL": "INFO",
echo           "FHL_CACHE_DIR": "%CD%\\.cache"
echo         }
echo       }
echo     }
echo   }
echo.
echo   ⚠️  重要：必須使用虛擬環境的 Python（venv\Scripts\python.exe）
echo.
echo 或使用自動配置工具：
echo   python scripts\generate_config.py
echo.
echo.

pause
