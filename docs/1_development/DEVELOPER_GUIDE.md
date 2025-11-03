# FHL Bible MCP Server - 開發者指南

本文檔面向希望理解、修改或貢獻 FHL Bible MCP Server 的開發者。

## 目錄

- [專案架構](#專案架構)
- [核心組件](#核心組件)
- [開發環境設置](#開發環境設置)
- [代碼風格指南](#代碼風格指南)
- [測試指南](#測試指南)
- [貢獻指南](#貢獻指南)
- [發布流程](#發布流程)

---

## 專案架構

### 整體架構圖

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Desktop                        │
│                     (MCP Client)                         │
└──────────────────┬──────────────────────────────────────┘
                   │ MCP Protocol (JSON-RPC over stdio)
┌──────────────────▼──────────────────────────────────────┐
│              FHL Bible MCP Server                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │         server.py (Main Server)                  │   │
│  │  • Tools Registration                            │   │
│  │  • Resources Registration                        │   │
│  │  • Prompts Registration                          │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Tools   │  │Resources │  │ Prompts  │              │
│  │  Layer   │  │  Layer   │  │  Layer   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │              │                     │
│  ┌────▼─────────────▼──────────────▼─────┐              │
│  │         API Client Layer                │             │
│  │  • FHLAPIEndpoints                      │             │
│  │  • HTTP Client (httpx)                  │             │
│  │  • Error Handling                       │             │
│  │  • Retry Logic                          │             │
│  └────────────────┬────────────────────────┘             │
└───────────────────┼──────────────────────────────────────┘
                    │ HTTPS
┌───────────────────▼──────────────────────────────────────┐
│         FHL Bible API (bible.fhl.net/json/)              │
│  • 聖經經文查詢                                            │
│  • 原文分析                                               │
│  • 註釋書                                                 │
│  • 主題查經                                               │
└──────────────────────────────────────────────────────────┘
```

### 目錄結構

```
FHL_MCP_SERVER/
├── src/fhl_bible_mcp/
│   ├── __init__.py           # 套件初始化
│   ├── server.py             # MCP Server 主程式
│   │
│   ├── api/                  # API 客戶端層
│   │   ├── __init__.py
│   │   ├── client.py         # HTTP 客戶端封裝
│   │   └── endpoints.py      # FHL API 端點封裝
│   │
│   ├── models/               # 資料模型
│   │   ├── __init__.py
│   │   ├── verse.py          # 經文模型
│   │   ├── search.py         # 搜尋結果模型
│   │   ├── strongs.py        # Strong's 字典模型
│   │   └── commentary.py     # 註釋模型
│   │
│   ├── tools/                # MCP Tools 實作
│   │   ├── __init__.py
│   │   ├── verse.py          # 經文查詢工具
│   │   ├── search.py         # 搜尋工具
│   │   ├── strongs.py        # 原文研究工具
│   │   ├── commentary.py     # 註釋工具
│   │   ├── info.py           # 資訊工具
│   │   └── audio.py          # 多媒體工具
│   │
│   ├── resources/            # MCP Resources 實作
│   │   ├── __init__.py
│   │   └── handlers.py       # Resource URI 處理器
│   │
│   ├── prompts/              # MCP Prompts 實作
│   │   ├── __init__.py
│   │   └── templates.py      # Prompt 範本
│   │
│   ├── utils/                # 工具函數
│   │   ├── __init__.py
│   │   ├── cache.py          # 快取系統
│   │   ├── booknames.py      # 書卷名稱轉換
│   │   └── errors.py         # 錯誤定義
│   │
│   └── config.py             # 配置管理
│
├── tests/                    # 測試套件
│   ├── __init__.py
│   ├── conftest.py           # 測試配置與 fixtures
│   │
│   ├── test_api/             # API 層測試
│   │   ├── test_client.py
│   │   └── test_endpoints.py
│   │
│   ├── test_tools/           # Tools 層測試
│   │   ├── test_verse.py
│   │   ├── test_search.py
│   │   ├── test_strongs.py
│   │   ├── test_commentary.py
│   │   ├── test_info.py
│   │   └── test_audio.py
│   │
│   ├── test_resources/       # Resources 層測試
│   │   └── test_handlers.py
│   │
│   ├── test_prompts/         # Prompts 層測試
│   │   └── test_templates.py
│   │
│   ├── test_utils/           # Utils 層測試
│   │   ├── test_cache.py
│   │   ├── test_booknames.py
│   │   └── test_errors.py
│   │
│   └── test_e2e/             # 端對端測試
│       ├── conftest.py
│       ├── test_e2e_final.py
│       └── test_e2e_extended.py
│
├── docs/                     # 文檔
│   ├── API.md
│   ├── DEVELOPER_GUIDE.md    # 本文件
│   ├── EXAMPLES.md
│   ├── FHL_BIBLE_MCP_PLANNING.md
│   ├── PHASE_4_2_FINAL_REPORT.md
│   └── TESTING_REPORT.md
│
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml            # 專案配置
└── config.example.json       # 配置範例
```

---

## 核心組件

### 1. Server 層 (`server.py`)

Server 是整個 MCP Server 的入口點，負責：

- 註冊所有 Tools
- 註冊所有 Resources
- 註冊所有 Prompts
- 處理 MCP 協議通信

**關鍵類別**:

```python
class FHLBibleServer:
    """FHL Bible MCP Server 主類"""
    
    def __init__(self):
        self.server = Server("fhl-bible-server")
        self.endpoints = FHLAPIEndpoints()
        self.resource_router = ResourceRouter(self.endpoints)
        self.prompt_manager = PromptManager()
        
    def _register_tools(self):
        """註冊所有 Tools"""
        
    def _register_resources(self):
        """註冊所有 Resources"""
        
    def _register_prompts(self):
        """註冊所有 Prompts"""
```

### 2. API 客戶端層

#### `client.py` - HTTP 客戶端

負責所有 HTTP 請求的底層處理：

- 使用 `httpx.AsyncClient` 進行異步請求
- 實作重試機制（3 次，指數退避）
- 錯誤處理與轉換
- 請求日誌記錄

**關鍵方法**:

```python
class FHLAPIClient:
    async def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """發送 API 請求並處理錯誤"""
```

#### `endpoints.py` - API 端點封裝

將 FHL API 的各個端點封裝成 Python 方法：

```python
class FHLAPIEndpoints:
    async def get_verse(self, book, chapter, verse, version, include_strong):
        """查詢經文 (qb.php)"""
        
    async def search_bible(self, keyword, version, scope, limit, offset):
        """搜尋聖經 (se.php)"""
        
    async def get_word_analysis(self, book, chapter, verse):
        """字彙分析 (qp.php)"""
```

### 3. Tools 層

每個 Tool 文件包含相關的工具函數：

- **verse.py**: 經文查詢工具
- **search.py**: 搜尋工具
- **strongs.py**: 原文研究工具
- **commentary.py**: 註釋工具
- **info.py**: 資訊查詢工具
- **audio.py**: 多媒體工具

**標準 Tool 函數結構**:

```python
async def tool_name(
    param1: str,
    param2: int,
    optional_param: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tool 說明
    
    Args:
        param1: 參數1說明
        param2: 參數2說明
        optional_param: 可選參數說明
        
    Returns:
        返回值說明
        
    Raises:
        ExceptionType: 異常說明
    """
    # 1. 參數驗證與轉換
    # 2. 呼叫 API
    # 3. 格式化結果
    # 4. 返回結果
```

### 4. Resources 層

Resource Handlers 處理不同類型的 Resource URI：

- **BibleResourceHandler**: 處理 `bible://` URI
- **StrongsResourceHandler**: 處理 `strongs://` URI
- **CommentaryResourceHandler**: 處理 `commentary://` URI
- **InfoResourceHandler**: 處理 `info://` URI

**Resource Handler 模式**:

```python
class ResourceHandler:
    def parse_uri(self, uri: str) -> Dict[str, Any]:
        """解析 URI"""
        
    async def handle(self, uri: str) -> Dict[str, Any]:
        """處理 Resource 請求"""
```

### 5. Prompts 層

Prompt Templates 提供預設對話範本：

```python
class PromptTemplate:
    name: str
    description: str
    arguments: List[Dict[str, Any]]
    
    def render(self, **kwargs) -> str:
        """渲染 prompt"""
```

### 6. Utils 層

#### `cache.py` - 快取系統

基於檔案的快取實作：

```python
class SimpleCache:
    def get(self, key: str) -> Optional[Any]:
        """獲取快取"""
        
    def set(self, key: str, value: Any, ttl: int = 3600):
        """設置快取"""
        
    def clear(self):
        """清空快取"""
```

#### `booknames.py` - 書卷名稱轉換

支援多種書卷名稱格式：

```python
class BookNameConverter:
    @staticmethod
    def get_chinese_short(name: str) -> Optional[str]:
        """轉換為中文縮寫"""
        
    @staticmethod
    def get_english_short(name: str) -> Optional[str]:
        """轉換為英文縮寫"""
```

#### `errors.py` - 錯誤定義

所有自定義異常：

```python
class FHLAPIError(Exception):
    """基礎錯誤"""

class BookNotFoundError(FHLAPIError):
    """找不到書卷"""
    
class InvalidParameterError(FHLAPIError):
    """參數錯誤"""
```

---

## 開發環境設置

### 1. Clone 專案

```bash
git clone https://github.com/yourusername/fhl-bible-mcp.git
cd fhl-bible-mcp
```

### 2. 建立虛擬環境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安裝開發依賴

```bash
pip install -e ".[dev]"
```

這會安裝：
- 生產依賴: mcp, httpx, pydantic, python-dotenv
- 開發依賴: pytest, pytest-asyncio, pytest-cov, ruff, black, mypy

### 4. 配置 IDE

#### VS Code

推薦安裝擴展：
- Python (Microsoft)
- Pylance (Microsoft)
- Ruff (Astral Software)
- Test Explorer UI

`.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

---

## 代碼風格指南

### 1. 通用規範

- **Python 版本**: 3.10+
- **編碼**: UTF-8
- **行寬**: 100 字元（Black 預設）
- **縮排**: 4 個空格
- **命名**:
  - 變數、函數: `snake_case`
  - 類別: `PascalCase`
  - 常數: `UPPER_SNAKE_CASE`

### 2. Import 順序

```python
# 1. 標準庫
import asyncio
import logging
from typing import Dict, Any, Optional

# 2. 第三方庫
from mcp.server import Server
import httpx

# 3. 本地模組
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.utils.errors import FHLAPIError
```

### 3. Docstring 格式

使用 Google 風格的 docstrings：

```python
def function_name(param1: str, param2: int) -> Dict[str, Any]:
    """
    簡短描述（一行）。
    
    詳細描述（如需要）。可以多行。
    
    Args:
        param1: 參數1的說明
        param2: 參數2的說明
        
    Returns:
        返回值的說明
        
    Raises:
        ValueError: 什麼情況下會拋出
        TypeError: 什麼情況下會拋出
        
    Examples:
        >>> function_name("test", 123)
        {'result': 'success'}
    """
```

### 4. 類型提示

所有函數都應使用類型提示：

```python
from typing import Optional, Dict, Any, List

async def get_verse(
    book: str,
    chapter: int,
    verse: Optional[str] = None
) -> Dict[str, Any]:
    ...
```

### 5. 錯誤處理

```python
try:
    result = await api_call()
except BookNotFoundError as e:
    logger.error(f"Book not found: {e}")
    raise
except APIResponseError as e:
    logger.error(f"API error: {e}")
    # 處理或重新拋出
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise FHLAPIError(f"Internal error: {e}") from e
```

---

## 測試指南

### 測試結構

```
tests/
├── test_api/           # API 層單元測試
├── test_tools/         # Tools 層單元測試
├── test_resources/     # Resources 層單元測試
├── test_prompts/       # Prompts 層單元測試
├── test_utils/         # Utils 層單元測試
└── test_e2e/           # 端對端整合測試
```

### 編寫單元測試

**Fixtures (conftest.py)**:

```python
@pytest.fixture
def mock_api_client():
    """Mock API Client"""
    client = AsyncMock(spec=FHLAPIClient)
    return client

@pytest.fixture
async def api_endpoints():
    """API Endpoints fixture"""
    endpoints = FHLAPIEndpoints()
    yield endpoints
    await endpoints.close()
```

**測試範例**:

```python
@pytest.mark.asyncio
async def test_get_bible_verse(mock_api_client):
    """測試查詢經文功能"""
    # Arrange
    mock_api_client._make_request.return_value = {
        "status": "success",
        "record": [{"bible_text": "test"}]
    }
    
    # Act
    result = await get_bible_verse("John", 3, "16")
    
    # Assert
    assert result["verses"][0]["text"] == "test"
```

### 執行測試

```bash
# 執行所有測試
pytest

# 執行特定測試文件
pytest tests/test_tools/test_verse.py

# 執行特定測試函數
pytest tests/test_tools/test_verse.py::test_get_bible_verse

# 顯示詳細輸出
pytest -v

# 顯示 print 輸出
pytest -s

# 只執行失敗的測試
pytest --lf

# 並行執行（需要 pytest-xdist）
pytest -n auto
```

### 覆蓋率報告

```bash
# 生成終端覆蓋率報告
pytest --cov=src/fhl_bible_mcp --cov-report=term

# 生成 HTML 覆蓋率報告
pytest --cov=src/fhl_bible_mcp --cov-report=html
# 報告位置: htmlcov/index.html

# 只顯示未覆蓋的行
pytest --cov=src/fhl_bible_mcp --cov-report=term-missing
```

### 測試覆蓋率目標

- **整體覆蓋率**: ≥ 80%
- **關鍵模組**: ≥ 90% (API, Tools)
- **E2E 測試**: 涵蓋所有主要使用場景

---

## 貢獻指南

### 1. Fork 與 Clone

```bash
# Fork 專案到您的 GitHub
# Clone 您的 Fork
git clone https://github.com/yourusername/fhl-bible-mcp.git
cd fhl-bible-mcp

# 添加上游倉庫
git remote add upstream https://github.com/originalowner/fhl-bible-mcp.git
```

### 2. 創建分支

```bash
# 從 main 創建特性分支
git checkout -b feature/your-feature-name

# 或修復分支
git checkout -b fix/bug-description
```

分支命名規範：
- `feature/` - 新功能
- `fix/` - Bug 修復
- `docs/` - 文檔更新
- `refactor/` - 重構
- `test/` - 測試相關

### 3. 開發

```bash
# 進行變更
# 編寫測試
# 執行測試
pytest

# 檢查代碼風格
ruff check src/
black --check src/

# 類型檢查
mypy src/
```

### 4. Commit

Commit 訊息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

類型 (type):
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文檔
- `style`: 格式（不影響代碼運行）
- `refactor`: 重構
- `test`: 測試
- `chore`: 建置或輔助工具變動

範例：

```
feat(tools): add support for apocrypha books

- Add qsub.php endpoint support
- Update BookNameConverter for apocrypha
- Add tests for apocrypha queries

Closes #123
```

### 5. Push 與 Pull Request

```bash
# Push 到您的 Fork
git push origin feature/your-feature-name

# 在 GitHub 上創建 Pull Request
```

Pull Request 應包含：
- 清晰的標題與描述
- 相關的 Issue 編號
- 測試證明
- 文檔更新（如需要）

### 6. Code Review

- 維護者會審查您的 PR
- 根據反饋進行修改
- 所有測試必須通過
- 至少一位維護者批准後才能合併

---

## 發布流程

### 版本號規範

使用語義化版本 (Semantic Versioning): `MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 變更
- **MINOR**: 向後兼容的新功能
- **PATCH**: 向後兼容的 Bug 修復

### 發布步驟

1. **更新版本號**

編輯 `pyproject.toml`:

```toml
[project]
version = "0.2.0"
```

2. **更新 CHANGELOG**

```markdown
## [0.2.0] - 2025-11-01

### Added
- Support for apocrypha books
- New search_strongs_occurrences tool

### Fixed
- Invalid parameter error in verse.py

### Changed
- Improved error messages
```

3. **創建 Tag**

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

4. **構建與發布**

```bash
# 構建
python -m build

# 上傳到 PyPI
python -m twine upload dist/*
```

---

## 常見問題

### Q: 如何添加新的 Tool？

1. 在 `src/fhl_bible_mcp/tools/` 創建或修改相應文件
2. 實作異步函數
3. 在 `server.py` 的 `_register_tools()` 中註冊
4. 添加測試到 `tests/test_tools/`
5. 更新 `docs/4_manuals/API.md`

### Q: 如何調試 MCP Server？

在 Claude Desktop 配置中添加日誌：

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

查看日誌：
- Windows: `%APPDATA%\Claude\logs\`
- macOS: `~/Library/Logs/Claude/`

### Q: 如何處理 API 變更？

1. 更新 `api/endpoints.py` 中的 API 調用
2. 更新相關的資料模型
3. 更新受影響的 Tools
4. 更新測試
5. 更新文檔

---

## 資源連結

- **MCP 官方文檔**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **FHL API**: https://bible.fhl.net/json/
- **信望愛站**: https://www.fhl.net/
- **專案 Issues**: https://github.com/yourusername/fhl-bible-mcp/issues

---

## 聯絡資訊

如有技術問題，請：

1. 查閱本指南與 API 文檔
2. 搜尋現有 Issues
3. 創建新 Issue（提供詳細資訊）

**Happy Coding! 🙏**
