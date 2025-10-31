# CLI 工具實作計劃

**文檔版本**: 1.0  
**制定日期**: 2025年11月1日  
**預計開發時間**: 2-3 週  
**狀態**: Phase 1 規劃階段

---

## 📋 目錄

- [專案目標](#專案目標)
- [命令架構](#命令架構)
- [技術棧選擇](#技術棧選擇)
- [代碼架構](#代碼架構)
- [功能實作](#功能實作)
- [互動設計](#互動設計)
- [測試策略](#測試策略)
- [打包與發布](#打包與發布)
- [開發時程](#開發時程)

---

## 專案目標

### 核心目標

1. **簡化安裝**: 一鍵安裝到支援的 MCP 客戶端
2. **自動檢測**: 自動發現已安裝的平台（Claude Desktop、VS Code等）
3. **互動式配置**: 友善的互動式安裝精靈
4. **診斷工具**: 檢查和修復常見問題
5. **跨平台支援**: Windows、macOS、Linux 三平台一致體驗

### 非功能性目標

- ⚡ 啟動時間 < 1 秒
- 📦 安裝包大小 < 10MB
- 🎨 美觀的 CLI 介面（使用 rich）
- 📚 完整的線上幫助文檔
- 🧪 測試覆蓋率 > 80%

---

## 命令架構

### 命令列表

```bash
# 主命令
fhl-bible <command> [options]

# 核心命令
fhl-bible setup         # 互動式安裝精靈
fhl-bible status        # 顯示安裝狀態
fhl-bible doctor        # 診斷問題
fhl-bible test          # 測試連接
fhl-bible update        # 更新配置
fhl-bible uninstall     # 卸載配置

# 輔助命令
fhl-bible list-platforms  # 列出支援的平台
fhl-bible version         # 顯示版本資訊
fhl-bible help            # 顯示幫助
```

### 命令詳細規格

#### 1. `fhl-bible setup`

**用途**: 互動式安裝精靈

**選項**:
```bash
fhl-bible setup [OPTIONS]

Options:
  -p, --platform TEXT     指定平台 (claude/vscode/openai/all)
  --auto                  自動檢測並安裝到所有平台
  --dry-run               模擬執行，不實際修改配置
  --force                 強制覆蓋現有配置
  --no-backup             不備份現有配置
  -v, --verbose           顯示詳細日誌
  -h, --help              顯示幫助

Examples:
  fhl-bible setup                    # 互動式安裝
  fhl-bible setup --auto             # 自動安裝到所有平台
  fhl-bible setup -p claude          # 僅安裝到 Claude Desktop
  fhl-bible setup --dry-run          # 預覽安裝操作
```

**執行流程**:
```
1. 環境檢查
   ├─ Python 版本檢查 (>= 3.10)
   ├─ fhl-bible-mcp 套件檢查
   └─ 權限檢查

2. 平台檢測
   ├─ 掃描已安裝的 MCP 客戶端
   ├─ 顯示檢測結果表格
   └─ 讓用戶選擇要安裝的平台

3. 配置生成
   ├─ 讀取現有配置
   ├─ 生成新配置
   ├─ 預覽配置差異
   └─ 確認安裝

4. 執行安裝
   ├─ 備份現有配置
   ├─ 寫入新配置
   ├─ 驗證安裝
   └─ 顯示安裝結果

5. 後續步驟
   └─ 提示用戶重啟應用
```

**輸出範例**:
```
╭──────────────────────────────────────────────╮
│   FHL Bible MCP Server - Setup Wizard       │
╰──────────────────────────────────────────────╯

✓ Python 3.11.5 detected
✓ fhl-bible-mcp v0.1.0 installed

Detecting MCP clients...

┌─────────────────────────────────────────────┐
│ Platform          │ Version │ Status        │
├───────────────────┼─────────┼───────────────┤
│ Claude Desktop    │ 1.2.0   │ ✓ Installed   │
│ VS Code           │ 1.85.0  │ ✓ Installed   │
│ OpenAI Desktop    │ -       │ ✗ Not found   │
└─────────────────────────────────────────────┘

? Select platforms to install:
  ◉ Claude Desktop
  ◉ Visual Studio Code
  ◯ All detected platforms

Generating configuration for Claude Desktop...

Preview:
┌─────────────────────────────────────────────┐
│ {                                           │
│   "mcpServers": {                           │
│     "fhl-bible": {                          │
│       "command": "python",                  │
│       "args": ["-m", "fhl_bible_mcp.server"]│
│     }                                       │
│   }                                         │
│ }                                           │
└─────────────────────────────────────────────┘

? Proceed with installation? (Y/n) 

✓ Backed up config to: ~/.config/Claude/.fhl-backups/
✓ Installed to Claude Desktop
✓ Configuration validated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Installation complete! 🎉

Next steps:
  1. Restart Claude Desktop
  2. Test connection: fhl-bible test
  3. View documentation: fhl-bible help
```

---

#### 2. `fhl-bible status`

**用途**: 顯示當前安裝狀態

**選項**:
```bash
fhl-bible status [OPTIONS]

Options:
  -p, --platform TEXT     檢查特定平台
  --verbose               顯示詳細配置
  --json                  JSON 格式輸出
  -h, --help              顯示幫助

Examples:
  fhl-bible status                # 檢查所有平台
  fhl-bible status -p claude      # 僅檢查 Claude Desktop
  fhl-bible status --json         # JSON 輸出
```

**輸出範例**:
```
FHL Bible MCP Server - Installation Status

┌──────────────────────────────────────────────────────────┐
│ Platform        │ Status      │ Config Path              │
├─────────────────┼─────────────┼──────────────────────────┤
│ Claude Desktop  │ ✓ Installed │ ~/.config/Claude/...json │
│ VS Code         │ ✗ Not found │ -                        │
│ OpenAI Desktop  │ ✗ N/A       │ Platform not detected    │
└──────────────────────────────────────────────────────────┘

Server Information:
  Version: 0.1.0
  Install Path: /usr/lib/python3.11/site-packages/fhl_bible_mcp
  Python: 3.11.5

Tools Available: 16
  ✓ search_verses
  ✓ get_verse
  ✓ get_chapter
  ...

Run 'fhl-bible doctor' to diagnose issues.
```

---

#### 3. `fhl-bible doctor`

**用途**: 診斷並修復問題

**選項**:
```bash
fhl-bible doctor [OPTIONS]

Options:
  -p, --platform TEXT     診斷特定平台
  --fix                   自動修復問題
  --verbose               顯示詳細診斷
  -h, --help              顯示幫助

Examples:
  fhl-bible doctor                # 診斷所有平台
  fhl-bible doctor --fix          # 自動修復問題
  fhl-bible doctor -p claude      # 僅診斷 Claude Desktop
```

**診斷項目**:
```python
CHECKS = [
    # 環境檢查
    "python_version",      # Python 版本 >= 3.10
    "package_installed",   # fhl-bible-mcp 已安裝
    "package_version",     # 版本是否最新
    
    # 配置檢查
    "config_exists",       # 配置文件存在
    "config_valid",        # 配置格式正確
    "config_complete",     # 必要欄位完整
    
    # 路徑檢查
    "python_path",         # Python 可執行文件路徑正確
    "module_path",         # 模組路徑可訪問
    "permissions",         # 文件權限正確
    
    # 連接檢查
    "server_start",        # 服務可啟動
    "tools_available",     # 工具可用
    "api_response",        # API 響應正常
]
```

**輸出範例**:
```
FHL Bible MCP Server - Diagnostic Report

Running diagnostics...

Environment Checks:
  ✓ Python version 3.11.5 (>= 3.10 required)
  ✓ fhl-bible-mcp v0.1.0 installed
  ⚠ Newer version available: v0.1.1

Configuration Checks (Claude Desktop):
  ✓ Config file exists
  ✗ Config format invalid
    └─ Missing 'command' field in mcpServers.fhl-bible
  ✓ Config permissions OK

Path Checks:
  ✓ Python executable found: /usr/bin/python3
  ✓ Module path accessible
  ✓ File permissions correct

Connection Checks:
  ✗ Server failed to start
    └─ Error: ModuleNotFoundError: No module named 'fhl_bible_mcp'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 2 issues:
  1. Config format invalid
  2. Server failed to start

Suggested fixes:
  • Run: fhl-bible setup --force
  • Or: fhl-bible doctor --fix

? Apply automatic fixes? (Y/n)
```

---

#### 4. `fhl-bible test`

**用途**: 測試 MCP 服務器連接

**選項**:
```bash
fhl-bible test [OPTIONS]

Options:
  -p, --platform TEXT     測試特定平台
  --tool TEXT             測試特定工具
  --timeout FLOAT         超時時間（秒，預設 10）
  -h, --help              顯示幫助

Examples:
  fhl-bible test                       # 測試所有平台
  fhl-bible test -p claude             # 測試 Claude Desktop
  fhl-bible test --tool search_verses  # 測試特定工具
```

**測試流程**:
```python
TEST_SEQUENCE = [
    # 基本測試
    ("Server Start", test_server_start),
    ("List Tools", test_list_tools),
    ("List Resources", test_list_resources),
    ("List Prompts", test_list_prompts),
    
    # 工具測試
    ("search_verses", lambda: test_tool("search_verses", {"query": "愛"})),
    ("get_verse", lambda: test_tool("get_verse", {"book": "約翰福音", "chapter": 3, "verse": 16})),
    ("get_chapter", lambda: test_tool("get_chapter", {"book": "詩篇", "chapter": 23})),
    
    # 資源測試
    ("book_list", test_resource_book_list),
    ("verse_of_day", test_resource_verse_of_day),
    
    # 提示測試
    ("bible_study", test_prompt_bible_study),
]
```

**輸出範例**:
```
FHL Bible MCP Server - Connection Test

Testing Claude Desktop...

Server Tests:
  ✓ Server start          [125ms]
  ✓ List tools            [45ms]
  ✓ List resources        [38ms]
  ✓ List prompts          [42ms]

Tool Tests:
  ✓ search_verses         [234ms] - Found 10 results
  ✓ get_verse             [156ms] - 約翰福音 3:16
  ✓ get_chapter           [298ms] - 詩篇 23 (6 verses)
  ✓ get_book              [523ms] - 創世記 (50 chapters)

Resource Tests:
  ✓ book_list             [89ms]  - 66 books
  ✓ verse_of_day          [67ms]  - 詩篇 119:105

Prompt Tests:
  ✓ bible_study           [112ms]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Summary:
  Total: 11 tests
  Passed: ✓ 11
  Failed: ✗ 0
  Duration: 1.734s

All tests passed! ✨
```

---

#### 5. `fhl-bible update`

**用途**: 更新配置或檢查更新

**選項**:
```bash
fhl-bible update [OPTIONS]

Options:
  -p, --platform TEXT     更新特定平台配置
  --check                 僅檢查更新
  --upgrade               升級到最新版本
  -h, --help              顯示幫助

Examples:
  fhl-bible update --check         # 檢查更新
  fhl-bible update --upgrade       # 升級到最新版本
  fhl-bible update -p claude       # 更新 Claude Desktop 配置
```

---

#### 6. `fhl-bible uninstall`

**用途**: 卸載配置

**選項**:
```bash
fhl-bible uninstall [OPTIONS]

Options:
  -p, --platform TEXT     卸載特定平台
  --all                   卸載所有平台
  --keep-backup           保留備份文件
  -h, --help              顯示幫助

Examples:
  fhl-bible uninstall -p claude    # 卸載 Claude Desktop 配置
  fhl-bible uninstall --all        # 卸載所有配置
```

**執行流程**:
```
1. 確認卸載
   └─ 顯示將被移除的配置

2. 備份配置
   └─ 創建最終備份

3. 移除配置
   ├─ 從配置文件中移除 fhl-bible 條目
   └─ 保留其他 MCP 服務器配置

4. 驗證卸載
   └─ 確認配置已移除

5. 清理（可選）
   ├─ 移除備份文件
   └─ 顯示如何完全移除套件
```

---

## 技術棧選擇

### 核心框架

#### Typer ⭐⭐⭐⭐⭐

**選擇理由**:
- 🎯 基於 Click，但使用 Python type hints
- 📝 自動生成幫助文檔
- ✨ 優雅的 API 設計
- 🔧 與 rich 完美整合

**範例**:
```python
import typer
from typing import Optional
from rich.console import Console

app = typer.Typer(
    name="fhl-bible",
    help="FHL Bible MCP Server CLI",
    add_completion=True,
)

console = Console()

@app.command()
def setup(
    platform: Optional[str] = typer.Option(
        None, "--platform", "-p",
        help="指定平台 (claude/vscode/openai/all)"
    ),
    auto: bool = typer.Option(
        False, "--auto",
        help="自動檢測並安裝到所有平台"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="模擬執行，不實際修改配置"
    ),
):
    """互動式安裝精靈"""
    if auto:
        console.print("[bold green]Auto-detecting platforms...[/bold green]")
        # 自動安裝邏輯
    else:
        # 互動式安裝邏輯
        pass

if __name__ == "__main__":
    app()
```

---

### 終端 UI

#### Rich ⭐⭐⭐⭐⭐

**用途**: 美觀的終端輸出

**功能**:
```python
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.tree import Tree
from rich.syntax import Syntax

console = Console()

# 表格
table = Table(title="Platforms")
table.add_column("Name", style="cyan")
table.add_column("Status", style="green")
table.add_row("Claude Desktop", "✓ Installed")
console.print(table)

# 進度條
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
) as progress:
    task = progress.add_task("Installing...", total=100)
    # 安裝邏輯
    progress.update(task, advance=10)

# 面板
console.print(Panel("Installation complete!", title="Success"))

# 語法高亮
config_json = '{"mcpServers": {...}}'
syntax = Syntax(config_json, "json", theme="monokai")
console.print(syntax)
```

---

#### Questionary ⭐⭐⭐⭐⭐

**用途**: 互動式輸入

**功能**:
```python
import questionary
from questionary import Style

# 自定義樣式
custom_style = Style([
    ('question', 'bold'),
    ('answer', 'fg:green bold'),
    ('pointer', 'fg:yellow bold'),
])

# 選擇
platform = questionary.select(
    "Select platform:",
    choices=[
        "Claude Desktop",
        "VS Code",
        "All detected platforms",
    ],
    style=custom_style
).ask()

# 確認
proceed = questionary.confirm(
    "Proceed with installation?",
    default=True
).ask()

# 多選
platforms = questionary.checkbox(
    "Select platforms to install:",
    choices=[
        questionary.Choice("Claude Desktop", checked=True),
        questionary.Choice("VS Code", checked=True),
        questionary.Choice("OpenAI Desktop", disabled=True),
    ]
).ask()

# 輸入
custom_path = questionary.path(
    "Enter installation path:",
    default=str(Path.home() / ".fhl-bible"),
).ask()
```

---

### 配置管理

#### Pydantic Settings ⭐⭐⭐⭐

**用途**: 配置驗證和管理

**範例**:
```python
from pydantic import BaseSettings, Field, validator
from pathlib import Path

class CLISettings(BaseSettings):
    """CLI 設置"""
    
    # 預設設置
    auto_backup: bool = Field(True, description="自動備份配置")
    backup_count: int = Field(5, description="保留備份數量")
    timeout: float = Field(10.0, description="連接超時（秒）")
    
    # 路徑設置
    config_dir: Path = Field(
        default_factory=lambda: Path.home() / ".fhl-bible",
        description="CLI 配置目錄"
    )
    
    @validator("timeout")
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError("Timeout must be positive")
        return v
    
    class Config:
        env_prefix = "FHL_BIBLE_"
        env_file = ".env"

settings = CLISettings()
```

---

## 代碼架構

### 專案結構

```
fhl_bible_mcp/
├── cli/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── app.py                # Typer app 定義
│   │
│   ├── commands/             # 命令實作
│   │   ├── __init__.py
│   │   ├── setup.py          # setup 命令
│   │   ├── status.py         # status 命令
│   │   ├── doctor.py         # doctor 命令
│   │   ├── test.py           # test 命令
│   │   ├── update.py         # update 命令
│   │   └── uninstall.py      # uninstall 命令
│   │
│   ├── platform/             # 平台相關
│   │   ├── __init__.py
│   │   ├── detector.py       # 平台檢測
│   │   ├── config_manager.py # 配置管理器
│   │   ├── installer.py      # 安裝器
│   │   └── platforms/        # 各平台實作
│   │       ├── __init__.py
│   │       ├── claude.py
│   │       ├── vscode.py
│   │       ├── openai.py
│   │       └── cursor.py
│   │
│   ├── utils/                # 工具函數
│   │   ├── __init__.py
│   │   ├── display.py        # 顯示工具（rich）
│   │   ├── prompts.py        # 互動提示（questionary）
│   │   ├── validators.py     # 驗證工具
│   │   └── backup.py         # 備份工具
│   │
│   ├── testing/              # 測試工具
│   │   ├── __init__.py
│   │   ├── runner.py         # 測試運行器
│   │   ├── checks.py         # 診斷檢查
│   │   └── fixtures.py       # 測試夾具
│   │
│   └── config/               # 配置
│       ├── __init__.py
│       ├── settings.py       # CLI 設置
│       └── constants.py      # 常量定義
│
├── pyproject.toml            # 專案配置
└── README.md
```

### 模組職責

#### `cli/app.py` - 主應用

```python
# cli/app.py
import typer
from rich.console import Console
from typing import Optional

from .commands import setup, status, doctor, test, update, uninstall
from .config import settings

app = typer.Typer(
    name="fhl-bible",
    help="FHL Bible MCP Server - Command Line Interface",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

console = Console()

# 註冊命令
app.command(name="setup")(setup.command)
app.command(name="status")(status.command)
app.command(name="doctor")(doctor.command)
app.command(name="test")(test.command)
app.command(name="update")(update.command)
app.command(name="uninstall")(uninstall.command)

@app.command()
def version():
    """顯示版本資訊"""
    from fhl_bible_mcp import __version__
    console.print(f"FHL Bible MCP Server v{__version__}")

@app.callback()
def main(
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="顯示詳細日誌"
    ),
):
    """FHL Bible MCP Server CLI"""
    if verbose:
        settings.log_level = "DEBUG"

if __name__ == "__main__":
    app()
```

---

#### `cli/commands/setup.py` - 安裝命令

```python
# cli/commands/setup.py
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from ..platform.detector import PlatformDetector
from ..platform.installer import PlatformInstaller
from ..utils.display import display_platforms, display_success
from ..utils.prompts import select_platforms, confirm_installation

console = Console()

def command(
    platform: Optional[str] = typer.Option(
        None, "--platform", "-p",
        help="指定平台 (claude/vscode/openai/all)"
    ),
    auto: bool = typer.Option(
        False, "--auto",
        help="自動安裝到所有平台"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="模擬執行"
    ),
    force: bool = typer.Option(
        False, "--force",
        help="強制覆蓋"
    ),
    no_backup: bool = typer.Option(
        False, "--no-backup",
        help="不備份配置"
    ),
):
    """互動式安裝精靈"""
    
    console.print(Panel(
        "[bold]FHL Bible MCP Server - Setup Wizard[/bold]",
        border_style="green"
    ))
    
    # 1. 環境檢查
    if not check_environment():
        return
    
    # 2. 平台檢測
    detector = PlatformDetector()
    platforms = detector.detect_all()
    
    if not platforms:
        console.print("[red]✗ No MCP clients detected[/red]")
        console.print("\nInstall Claude Desktop or VS Code first.")
        return
    
    display_platforms(platforms)
    
    # 3. 選擇平台
    if platform:
        selected = [p for p in platforms if p.name == platform]
    elif auto:
        selected = platforms
    else:
        selected = select_platforms(platforms)
    
    if not selected:
        console.print("[yellow]No platforms selected[/yellow]")
        return
    
    # 4. 確認安裝
    if not dry_run and not confirm_installation(selected):
        console.print("[yellow]Installation cancelled[/yellow]")
        return
    
    # 5. 執行安裝
    for platform_info in selected:
        installer = PlatformInstaller(
            platform_info,
            force=force,
            backup=not no_backup
        )
        
        if dry_run:
            console.print(f"[yellow]Would install to {platform_info.display_name}[/yellow]")
        else:
            success = installer.install()
            if success:
                display_success(platform_info)
            else:
                console.print(f"[red]✗ Failed to install to {platform_info.display_name}[/red]")

def check_environment() -> bool:
    """檢查環境"""
    import sys
    
    # Python 版本
    if sys.version_info < (3, 10):
        console.print("[red]✗ Python 3.10+ required[/red]")
        return False
    
    console.print(f"[green]✓[/green] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # 套件檢查
    try:
        import fhl_bible_mcp
        console.print(f"[green]✓[/green] fhl-bible-mcp v{fhl_bible_mcp.__version__}")
        return True
    except ImportError:
        console.print("[red]✗ fhl-bible-mcp not installed[/red]")
        console.print("\nRun: pip install fhl-bible-mcp")
        return False
```

---

#### `cli/platform/detector.py` - 平台檢測

```python
# cli/platform/detector.py
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import platform as sys_platform

@dataclass
class PlatformInfo:
    """平台資訊"""
    name: str
    display_name: str
    version: Optional[str]
    config_path: Path
    is_installed: bool
    executable_path: Optional[Path]

class PlatformDetector:
    """平台檢測器"""
    
    def detect_all(self) -> List[PlatformInfo]:
        """檢測所有平台"""
        platforms = []
        
        # Claude Desktop
        claude = self.detect_claude()
        if claude:
            platforms.append(claude)
        
        # VS Code
        vscode = self.detect_vscode()
        if vscode:
            platforms.append(vscode)
        
        # OpenAI Desktop
        openai = self.detect_openai()
        if openai:
            platforms.append(openai)
        
        # Cursor
        cursor = self.detect_cursor()
        if cursor:
            platforms.append(cursor)
        
        return platforms
    
    def detect_claude(self) -> Optional[PlatformInfo]:
        """檢測 Claude Desktop"""
        config_path = self._get_claude_config_path()
        
        if not config_path or not config_path.parent.exists():
            return None
        
        return PlatformInfo(
            name="claude",
            display_name="Claude Desktop",
            version=self._get_claude_version(),
            config_path=config_path,
            is_installed=True,
            executable_path=self._find_claude_executable()
        )
    
    def _get_claude_config_path(self) -> Optional[Path]:
        """獲取 Claude 配置路徑"""
        system = sys_platform.system()
        
        paths = {
            "Windows": Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json",
            "Darwin": Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
            "Linux": Path.home() / ".config/Claude/claude_desktop_config.json",
        }
        
        return paths.get(system)
    
    # ... 其他檢測方法
```

---

## 功能實作

### 關鍵功能實作細節

#### 1. 配置備份與恢復

```python
# cli/utils/backup.py
from pathlib import Path
from datetime import datetime
import shutil
import json

class BackupManager:
    """備份管理器"""
    
    def __init__(self, backup_dir: Path, max_backups: int = 5):
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, config_path: Path, platform: str) -> Path:
        """創建備份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{platform}_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(config_path, backup_path)
        self._cleanup_old_backups(platform)
        
        return backup_path
    
    def restore_backup(self, backup_path: Path, config_path: Path) -> bool:
        """恢復備份"""
        if not backup_path.exists():
            return False
        
        shutil.copy2(backup_path, config_path)
        return True
    
    def list_backups(self, platform: Optional[str] = None) -> List[Path]:
        """列出備份"""
        pattern = f"{platform}_*.json" if platform else "*.json"
        backups = sorted(
            self.backup_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        return backups
    
    def _cleanup_old_backups(self, platform: str):
        """清理舊備份"""
        backups = self.list_backups(platform)
        if len(backups) > self.max_backups:
            for old_backup in backups[self.max_backups:]:
                old_backup.unlink()
```

---

#### 2. 診斷檢查

```python
# cli/testing/checks.py
from dataclasses import dataclass
from typing import Callable, List, Optional
from enum import Enum

class CheckStatus(Enum):
    """檢查狀態"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"

@dataclass
class CheckResult:
    """檢查結果"""
    name: str
    status: CheckStatus
    message: str
    details: Optional[str] = None
    fix_command: Optional[str] = None

class DiagnosticChecker:
    """診斷檢查器"""
    
    def __init__(self, platform_info: PlatformInfo):
        self.platform = platform_info
        self.results: List[CheckResult] = []
    
    def run_all_checks(self) -> List[CheckResult]:
        """運行所有檢查"""
        checks = [
            self.check_python_version,
            self.check_package_installed,
            self.check_config_exists,
            self.check_config_valid,
            self.check_python_path,
            self.check_module_path,
            self.check_permissions,
            self.check_server_start,
        ]
        
        for check in checks:
            result = check()
            self.results.append(result)
        
        return self.results
    
    def check_python_version(self) -> CheckResult:
        """檢查 Python 版本"""
        import sys
        
        version = sys.version_info
        if version >= (3, 10):
            return CheckResult(
                name="Python Version",
                status=CheckStatus.PASSED,
                message=f"Python {version.major}.{version.minor}.{version.micro}"
            )
        else:
            return CheckResult(
                name="Python Version",
                status=CheckStatus.FAILED,
                message=f"Python {version.major}.{version.minor} detected",
                details="Python 3.10+ required",
                fix_command="Upgrade Python"
            )
    
    def check_config_valid(self) -> CheckResult:
        """檢查配置有效性"""
        try:
            with open(self.platform.config_path, 'r') as f:
                config = json.load(f)
            
            # 驗證配置結構
            if not self._validate_config_structure(config):
                return CheckResult(
                    name="Config Valid",
                    status=CheckStatus.FAILED,
                    message="Config structure invalid",
                    fix_command="fhl-bible setup --force"
                )
            
            return CheckResult(
                name="Config Valid",
                status=CheckStatus.PASSED,
                message="Config format OK"
            )
        except json.JSONDecodeError as e:
            return CheckResult(
                name="Config Valid",
                status=CheckStatus.FAILED,
                message="JSON parse error",
                details=str(e),
                fix_command="fhl-bible setup --force"
            )
    
    def check_server_start(self) -> CheckResult:
        """檢查服務器啟動"""
        import subprocess
        
        try:
            result = subprocess.run(
                ["python", "-m", "fhl_bible_mcp.server", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return CheckResult(
                    name="Server Start",
                    status=CheckStatus.PASSED,
                    message="Server can start"
                )
            else:
                return CheckResult(
                    name="Server Start",
                    status=CheckStatus.FAILED,
                    message="Server failed to start",
                    details=result.stderr,
                    fix_command="Check logs for details"
                )
        except Exception as e:
            return CheckResult(
                name="Server Start",
                status=CheckStatus.FAILED,
                message="Server test failed",
                details=str(e)
            )
```

---

## 互動設計

### 互動流程範例

#### Setup 命令互動流程

```python
# 完整互動式安裝流程
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import questionary

console = Console()

def interactive_setup():
    """互動式安裝流程"""
    
    # 1. 歡迎畫面
    console.print(Panel.fit(
        "[bold cyan]FHL Bible MCP Server[/bold cyan]\n"
        "Interactive Setup Wizard",
        border_style="cyan"
    ))
    
    # 2. 環境檢查
    console.print("\n[bold]Step 1: Environment Check[/bold]")
    with console.status("[yellow]Checking environment..."):
        python_ok, package_ok = check_environment_detailed()
    
    if not python_ok or not package_ok:
        console.print("[red]✗ Environment check failed[/red]")
        return
    
    # 3. 平台檢測
    console.print("\n[bold]Step 2: Platform Detection[/bold]")
    with console.status("[yellow]Detecting MCP clients..."):
        platforms = detect_platforms()
    
    # 顯示檢測結果
    table = Table(title="Detected Platforms")
    table.add_column("Platform", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Status", justify="center")
    
    for p in platforms:
        status = "✓" if p.is_installed else "✗"
        table.add_row(p.display_name, p.version or "Unknown", status)
    
    console.print(table)
    
    if not platforms:
        console.print("\n[red]No MCP clients detected[/red]")
        return
    
    # 4. 選擇平台
    console.print("\n[bold]Step 3: Select Platforms[/bold]")
    selected = questionary.checkbox(
        "Which platforms do you want to install to?",
        choices=[
            questionary.Choice(
                title=f"{p.display_name} ({p.version})",
                value=p,
                checked=True
            )
            for p in platforms
        ]
    ).ask()
    
    if not selected:
        console.print("[yellow]No platforms selected[/yellow]")
        return
    
    # 5. 預覽配置
    console.print("\n[bold]Step 4: Configuration Preview[/bold]")
    for platform_info in selected:
        config = generate_config_preview(platform_info)
        
        console.print(f"\n[cyan]{platform_info.display_name}:[/cyan]")
        console.print(Panel(
            Syntax(json.dumps(config, indent=2), "json"),
            title="Configuration",
            border_style="blue"
        ))
    
    # 6. 確認安裝
    proceed = questionary.confirm(
        "Proceed with installation?",
        default=True
    ).ask()
    
    if not proceed:
        console.print("[yellow]Installation cancelled[/yellow]")
        return
    
    # 7. 執行安裝
    console.print("\n[bold]Step 5: Installing...[/bold]")
    with Progress() as progress:
        task = progress.add_task("[green]Installing...", total=len(selected))
        
        for platform_info in selected:
            progress.update(task, description=f"Installing to {platform_info.display_name}...")
            success = install_platform(platform_info)
            
            if success:
                console.print(f"[green]✓[/green] {platform_info.display_name}")
            else:
                console.print(f"[red]✗[/red] {platform_info.display_name}")
            
            progress.advance(task)
    
    # 8. 完成
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]Installation Complete! 🎉[/bold green]\n\n"
        "Next steps:\n"
        "  1. Restart your MCP client\n"
        "  2. Test connection: [cyan]fhl-bible test[/cyan]\n"
        "  3. View status: [cyan]fhl-bible status[/cyan]",
        border_style="green"
    ))
```

---

## 測試策略

### 測試覆蓋

```python
# tests/cli/test_commands.py
import pytest
from typer.testing import CliRunner
from fhl_bible_mcp.cli.app import app

runner = CliRunner()

def test_setup_command():
    """測試 setup 命令"""
    result = runner.invoke(app, ["setup", "--help"])
    assert result.exit_code == 0
    assert "setup" in result.stdout

def test_status_command():
    """測試 status 命令"""
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0

def test_doctor_command():
    """測試 doctor 命令"""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0

# tests/cli/test_platform_detection.py
def test_detect_claude(tmp_path):
    """測試 Claude 檢測"""
    # 創建模擬配置
    config_dir = tmp_path / "Claude"
    config_dir.mkdir()
    config_file = config_dir / "claude_desktop_config.json"
    config_file.write_text('{"mcpServers": {}}')
    
    detector = PlatformDetector()
    # Mock 配置路徑
    with patch.object(detector, '_get_claude_config_path', return_value=config_file):
        result = detector.detect_claude()
        assert result is not None
        assert result.name == "claude"

# tests/cli/test_installer.py
def test_installation_flow(tmp_path):
    """測試安裝流程"""
    platform_info = PlatformInfo(
        name="claude",
        display_name="Claude Desktop",
        version="1.0.0",
        config_path=tmp_path / "config.json",
        is_installed=True,
        executable_path=None
    )
    
    installer = PlatformInstaller(platform_info)
    success = installer.install()
    
    assert success == True
    assert platform_info.config_path.exists()
```

---

## 打包與發布

### PyPI 發布

#### `pyproject.toml` 配置

```toml
[project]
name = "fhl-bible-mcp"
version = "0.1.0"
description = "FHL Bible MCP Server - Command Line Interface"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}

dependencies = [
    "mcp>=0.1.0",
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[project.scripts]
fhl-bible = "fhl_bible_mcp.cli:main"

[project.urls]
Homepage = "https://github.com/yourusername/fhl-bible-mcp"
Documentation = "https://github.com/yourusername/fhl-bible-mcp/blob/main/docs/"
Repository = "https://github.com/yourusername/fhl-bible-mcp"
"Bug Tracker" = "https://github.com/yourusername/fhl-bible-mcp/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/fhl_bible_mcp"]
```

#### 發布流程

```bash
# 1. 安裝構建工具
pip install build twine

# 2. 構建發行版
python -m build

# 3. 檢查發行版
twine check dist/*

# 4. 上傳到 TestPyPI（測試）
twine upload --repository testpypi dist/*

# 5. 測試安裝
pip install --index-url https://test.pypi.org/simple/ fhl-bible-mcp

# 6. 上傳到 PyPI（正式）
twine upload dist/*
```

---

## 開發時程

### Week 1: 核心架構

**目標**: 建立基礎架構和平台檢測

| 天 | 任務 | 產出 |
|----|------|------|
| Day 1-2 | 專案設置 | 目錄結構、pyproject.toml、基礎 CLI 框架 |
| Day 3-4 | 平台檢測 | PlatformDetector 類、所有平台檢測邏輯 |
| Day 5 | 配置管理 | ConfigManager 抽象類、Claude/VS Code 實作 |

**里程碑**: ✅ 能夠檢測已安裝的平台

---

### Week 2: 核心命令

**目標**: 實作主要命令（setup、status、doctor）

| 天 | 任務 | 產出 |
|----|------|------|
| Day 6-7 | Setup 命令 | 完整的互動式安裝流程 |
| Day 8 | Status 命令 | 狀態檢查和顯示 |
| Day 9-10 | Doctor 命令 | 診斷檢查、問題修復 |

**里程碑**: ✅ 可以安裝和診斷配置

---

### Week 3: 測試與發布

**目標**: 測試、文檔、打包發布

| 天 | 任務 | 產出 |
|----|------|------|
| Day 11 | Test 命令 | 連接測試、工具測試 |
| Day 12 | Update/Uninstall 命令 | 更新和卸載邏輯 |
| Day 13 | 單元測試 | 80%+ 測試覆蓋率 |
| Day 14 | 整合測試 | 跨平台測試 |
| Day 15 | 文檔與發布 | README、PyPI 發布 |

**里程碑**: ✅ Phase 1 完成，PyPI 發布

---

## 成功標準

### Phase 1 完成標準

- ✅ 支援 Claude Desktop 和 VS Code
- ✅ 所有核心命令實作完成
- ✅ 測試覆蓋率 > 80%
- ✅ 文檔完整（README + CLI help）
- ✅ 發布到 PyPI
- ✅ 三平台（Windows/macOS/Linux）測試通過

---

## 相關文檔

- 📄 [部署策略總覽](DEPLOYMENT_STRATEGY.md)
- 📄 [多平台支援設計](MULTI_PLATFORM_SUPPORT.md)
- 📄 [GUI 開發計劃](GUI_DEVELOPMENT_PLAN.md)
- 📄 [開發路線圖](DEPLOYMENT_ROADMAP.md)

---

**最後更新**: 2025年11月1日
