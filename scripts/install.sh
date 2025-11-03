#!/bin/bash
# FHL Bible MCP Server - macOS/Linux 一鍵安裝腳本
# 自動完成環境設定和套件安裝

set -e  # 遇到錯誤立即退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 印出標題
print_header() {
    echo -e "${BOLD}${BLUE}========================================${NC}"
    echo -e "${BOLD}${BLUE}$1${NC}"
    echo -e "${BOLD}${BLUE}========================================${NC}"
    echo ""
}

# 印出步驟
print_step() {
    echo -e "${BOLD}[$1] $2${NC}"
}

# 印出成功訊息
print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

# 印出警告訊息
print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# 印出錯誤訊息
print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# 印出跳過訊息
print_skip() {
    echo -e "${YELLOW}[SKIP] $1${NC}"
}

# 開始
print_header "FHL Bible MCP Server - 一鍵安裝"

# 檢測作業系統
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    PYTHON_CMD="python3"
else
    print_error "不支援的作業系統: $OSTYPE"
    exit 1
fi

echo "作業系統: $OS"
echo ""

# 1. 檢查 Python
print_step "1/6" "檢查 Python..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    print_error "未找到 Python！"
    echo "請先安裝 Python 3.10 或更高版本"
    if [[ "$OS" == "macOS" ]]; then
        echo "安裝方式："
        echo "  brew install python@3.10"
        echo "  或下載：https://www.python.org/downloads/"
    else
        echo "安裝方式："
        echo "  sudo apt install python3.10  # Ubuntu/Debian"
        echo "  或參考您的發行版文檔"
    fi
    exit 1
fi

$PYTHON_CMD --version
print_success "Python 已安裝"
echo ""

# 檢查 Python 版本
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.10"

if ! $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    print_error "Python 版本過低: $PYTHON_VERSION (需要 >= $REQUIRED_VERSION)"
    exit 1
fi

# 2. 檢查專案目錄
if [ ! -f "pyproject.toml" ]; then
    print_error "請在專案根目錄執行此腳本"
    echo "當前目錄: $(pwd)"
    exit 1
fi

print_success "專案目錄確認"
echo ""

# 3. 建立虛擬環境
print_step "2/6" "建立虛擬環境..."
if [ -d "venv" ]; then
    print_skip "虛擬環境已存在"
else
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        print_error "建立虛擬環境失敗"
        exit 1
    fi
    print_success "虛擬環境建立完成"
fi
echo ""

# 4. 啟動虛擬環境
print_step "3/6" "啟動虛擬環境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "啟動虛擬環境失敗"
    exit 1
fi
print_success "虛擬環境已啟動"
echo ""

# 5. 升級 pip
print_step "4/6" "升級 pip..."
python -m pip install --upgrade pip --quiet
print_success "pip 已升級"
echo ""

# 6. 安裝套件
print_step "5/6" "安裝 FHL Bible MCP Server..."
pip install -e . --quiet
if [ $? -ne 0 ]; then
    print_error "套件安裝失敗"
    exit 1
fi
print_success "套件安裝完成"
echo ""

# 7. 驗證安裝
print_step "6/6" "驗證安裝..."
python scripts/verify_setup.py
VERIFY_RESULT=$?
echo ""

if [ $VERIFY_RESULT -ne 0 ]; then
    print_warning "部分檢查未通過，請查看上方訊息"
    echo ""
else
    print_header "安裝完成！"
fi

# 顯示下一步
echo "下一步："
echo "1. 配置 AI 助手（Claude Desktop 或 VS Code）"
echo "2. 參考文檔：docs/1_development/INSTALLATION_GUIDE.md"
echo ""

# 根據作業系統顯示配置路徑
if [[ "$OS" == "macOS" ]]; then
    echo "快速配置 Claude Desktop："
    echo "  文件位置：~/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OS" == "Linux" ]]; then
    echo "快速配置 Claude Desktop："
    echo "  文件位置：~/.config/Claude/claude_desktop_config.json"
fi

echo "  專案路徑：$(pwd)"
echo "  PYTHONPATH：$(pwd)/src"
echo ""

echo "啟動虛擬環境："
echo "  source venv/bin/activate"
echo ""
