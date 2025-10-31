# 多平台支援設計文檔

**文檔版本**: 1.0  
**制定日期**: 2025年11月1日  
**狀態**: 規劃階段

---

## 📋 目錄

- [支援平台總覽](#支援平台總覽)
- [配置文件格式](#配置文件格式)
- [平台檢測機制](#平台檢測機制)
- [統一配置抽象層](#統一配置抽象層)
- [安裝流程設計](#安裝流程設計)
- [測試策略](#測試策略)

---

## 支援平台總覽

### 平台優先級與時程

| 平台 | 優先級 | 實作階段 | 用戶基數 | API 穩定度 | 狀態 |
|------|--------|---------|---------|-----------|------|
| **Claude Desktop** | 🔴 高 | Phase 1 | 大 | 高 | ✅ 手動支援 |
| **VS Code** | 🔴 高 | Phase 1 | 極大 | 中 | ⏳ 計劃中 |
| **OpenAI Desktop** | 🟡 中 | Phase 2 | 大 | 待確認 | ⏳ 待驗證 |
| **Cursor IDE** | 🟡 中 | Phase 2 | 中 | 中 | ⏳ 計劃中 |
| **Continue.dev** | 🟢 低 | Phase 3 | 小 | 中 | ⏳ 未來 |
| **Zed Editor** | 🟢 低 | Phase 3 | 小 | 低 | ⏳ 未來 |

---

## 配置文件格式

### Claude Desktop

#### 配置文件位置

| 作業系統 | 配置文件路徑 |
|---------|-------------|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| | 完整路徑: `C:\Users\<Username>\AppData\Roaming\Claude\claude_desktop_config.json` |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

#### 配置格式

```json
{
  "mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": [
        "-m",
        "fhl_bible_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "/path/to/fhl-bible-mcp/src",
        "LOG_LEVEL": "INFO"
      }
    },
    "other-mcp-server": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
```

**關鍵欄位說明**:
- `mcpServers`: MCP server 配置對象
- `command`: 執行命令（python / python3 / 完整路徑）
- `args`: 命令參數陣列
- `env`: 環境變數（可選）
  - `PYTHONPATH`: Python 模組搜尋路徑
  - `LOG_LEVEL`: 日誌級別

#### 版本檢測

```python
# 檢測 Claude Desktop 版本
import json
from pathlib import Path

def get_claude_version() -> str:
    """獲取 Claude Desktop 版本"""
    # Windows
    if platform.system() == "Windows":
        # 檢查註冊表或安裝目錄
        pass
    # macOS
    elif platform.system() == "Darwin":
        # 檢查 Info.plist
        app_path = Path("/Applications/Claude.app")
        if app_path.exists():
            plist = app_path / "Contents/Info.plist"
            # 解析 plist 獲取版本
    # Linux
    else:
        # 檢查 .desktop 文件或安裝資訊
        pass
```

---

### VS Code + GitHub Copilot

#### 配置文件位置

| 作業系統 | User Settings | Workspace Settings |
|---------|--------------|-------------------|
| **Windows** | `%APPDATA%\Code\User\settings.json` | `<workspace>\.vscode\settings.json` |
| **macOS** | `~/Library/Application Support/Code/User/settings.json` | `<workspace>/.vscode/settings.json` |
| **Linux** | `~/.config/Code/User/settings.json` | `<workspace>/.vscode/settings.json` |

#### 配置格式 (預測)

```json
{
  "github.copilot.mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "env": {}
    }
  }
}
```

**或可能是**:

```json
{
  "mcp.servers": [
    {
      "name": "fhl-bible",
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "autoStart": true
    }
  ]
}
```

**注意**: ⚠️ VS Code MCP 支援格式需要在正式發布後確認

#### 安裝選項

**1. User Settings (全域)**:
- ✅ 所有專案自動生效
- ❌ 無法針對專案客製化

**2. Workspace Settings (專案)**:
- ✅ 針對特定專案配置
- ✅ 可版本控制（加入 git）
- ❌ 需要每個專案分別配置

**建議**: 預設使用 User Settings，提供 `--workspace` 選項給進階用戶

---

### OpenAI Desktop

#### 配置文件位置 (預測)

| 作業系統 | 配置文件路徑 (待驗證) |
|---------|---------------------|
| **Windows** | `%APPDATA%\OpenAI\config.json` |
| **macOS** | `~/Library/Application Support/OpenAI/config.json` |
| **Linux** | `~/.config/OpenAI/config.json` |

#### 配置格式 (預測)

```json
{
  "extensions": {
    "fhl-bible": {
      "type": "mcp",
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"],
      "enabled": true
    }
  }
}
```

**或可能是**:

```json
{
  "plugins": [
    {
      "name": "fhl-bible",
      "protocol": "mcp",
      "executable": "python",
      "arguments": ["-m", "fhl_bible_mcp.server"]
    }
  ]
}
```

**注意**: ⚠️ OpenAI Desktop 格式需在產品正式發布後驗證

---

### Cursor IDE

#### 配置文件位置

| 作業系統 | 配置文件路徑 |
|---------|-------------|
| **Windows** | `%APPDATA%\Cursor\User\settings.json` |
| **macOS** | `~/Library/Application Support/Cursor/User/settings.json` |
| **Linux** | `~/.config/Cursor/User/settings.json` |

#### 配置格式

Cursor 基於 VS Code，配置格式應類似：

```json
{
  "cursor.mcpServers": {
    "fhl-bible": {
      "command": "python",
      "args": ["-m", "fhl_bible_mcp.server"]
    }
  }
}
```

---

## 平台檢測機制

### 檢測策略

```python
# detector.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import platform
import json

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
        """檢測所有已安裝的平台"""
        platforms = []
        
        # Claude Desktop
        claude_info = self.detect_claude()
        if claude_info:
            platforms.append(claude_info)
        
        # VS Code
        vscode_info = self.detect_vscode()
        if vscode_info:
            platforms.append(vscode_info)
        
        # OpenAI Desktop
        openai_info = self.detect_openai()
        if openai_info:
            platforms.append(openai_info)
        
        # Cursor
        cursor_info = self.detect_cursor()
        if cursor_info:
            platforms.append(cursor_info)
        
        return platforms
    
    def detect_claude(self) -> Optional[PlatformInfo]:
        """檢測 Claude Desktop"""
        config_path = self._get_claude_config_path()
        
        if not config_path or not config_path.parent.exists():
            return None
        
        version = self._get_claude_version()
        executable = self._find_claude_executable()
        
        return PlatformInfo(
            name="claude",
            display_name="Claude Desktop",
            version=version,
            config_path=config_path,
            is_installed=True,
            executable_path=executable
        )
    
    def detect_vscode(self) -> Optional[PlatformInfo]:
        """檢測 VS Code"""
        config_path = self._get_vscode_config_path()
        
        if not config_path or not config_path.parent.exists():
            return None
        
        version = self._get_vscode_version()
        executable = self._find_vscode_executable()
        
        return PlatformInfo(
            name="vscode",
            display_name="Visual Studio Code",
            version=version,
            config_path=config_path,
            is_installed=True,
            executable_path=executable
        )
    
    def detect_openai(self) -> Optional[PlatformInfo]:
        """檢測 OpenAI Desktop"""
        config_path = self._get_openai_config_path()
        
        if not config_path or not config_path.parent.exists():
            return None
        
        version = self._get_openai_version()
        
        return PlatformInfo(
            name="openai",
            display_name="OpenAI Desktop",
            version=version,
            config_path=config_path,
            is_installed=True,
            executable_path=None
        )
    
    def _get_claude_config_path(self) -> Optional[Path]:
        """獲取 Claude 配置路徑"""
        system = platform.system()
        
        if system == "Windows":
            return Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json"
        elif system == "Darwin":  # macOS
            return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
        elif system == "Linux":
            return Path.home() / ".config/Claude/claude_desktop_config.json"
        
        return None
    
    def _get_vscode_config_path(self) -> Optional[Path]:
        """獲取 VS Code 配置路徑"""
        system = platform.system()
        
        if system == "Windows":
            return Path.home() / "AppData/Roaming/Code/User/settings.json"
        elif system == "Darwin":
            return Path.home() / "Library/Application Support/Code/User/settings.json"
        elif system == "Linux":
            return Path.home() / ".config/Code/User/settings.json"
        
        return None
    
    def _find_claude_executable(self) -> Optional[Path]:
        """查找 Claude 可執行文件"""
        system = platform.system()
        
        if system == "Windows":
            possible_paths = [
                Path.home() / "AppData/Local/Programs/Claude/Claude.exe",
                Path("C:/Program Files/Claude/Claude.exe"),
            ]
        elif system == "Darwin":
            possible_paths = [
                Path("/Applications/Claude.app"),
            ]
        else:  # Linux
            possible_paths = [
                Path("/usr/bin/claude"),
                Path("/usr/local/bin/claude"),
            ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _get_claude_version(self) -> Optional[str]:
        """獲取 Claude 版本"""
        # Windows: 檢查可執行文件版本資訊
        # macOS: 檢查 Info.plist
        # Linux: 檢查 --version 輸出
        pass
    
    def _get_vscode_version(self) -> Optional[str]:
        """獲取 VS Code 版本"""
        import subprocess
        try:
            result = subprocess.run(
                ["code", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return lines[0] if lines else None
        except:
            pass
        return None
```

### 檢測結果展示

```python
# CLI 輸出範例
from rich.table import Table
from rich.console import Console

def display_detection_results(platforms: List[PlatformInfo]):
    """展示檢測結果"""
    console = Console()
    table = Table(title="Detected MCP Clients")
    
    table.add_column("Platform", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Config Path", style="yellow")
    
    for platform in platforms:
        status = "✓ Installed" if platform.is_installed else "✗ Not found"
        version = platform.version or "Unknown"
        
        table.add_row(
            platform.display_name,
            version,
            status,
            str(platform.config_path)
        )
    
    console.print(table)
```

---

## 統一配置抽象層

### 配置管理器設計

```python
# config_manager.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import json
import shutil
from datetime import datetime

class ConfigManager(ABC):
    """配置管理器抽象基類"""
    
    def __init__(self, platform_name: str, config_path: Path):
        self.platform_name = platform_name
        self.config_path = config_path
        self.backup_dir = config_path.parent / ".fhl-backups"
    
    @abstractmethod
    def generate_config(self, install_path: Path) -> Dict[str, Any]:
        """生成平台特定配置"""
        pass
    
    @abstractmethod
    def merge_config(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """合併配置（保留現有配置）"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """驗證配置格式"""
        pass
    
    def backup_config(self) -> Optional[Path]:
        """備份現有配置"""
        if not self.config_path.exists():
            return None
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{self.platform_name}_{timestamp}.json"
        
        shutil.copy2(self.config_path, backup_path)
        return backup_path
    
    def restore_config(self, backup_path: Path) -> bool:
        """恢復配置"""
        if not backup_path.exists():
            return False
        
        shutil.copy2(backup_path, self.config_path)
        return True
    
    def read_config(self) -> Optional[Dict[str, Any]]:
        """讀取現有配置"""
        if not self.config_path.exists():
            return None
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    def write_config(self, config: Dict[str, Any]) -> bool:
        """寫入配置"""
        try:
            # 確保目錄存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 寫入配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error writing config: {e}")
            return False


class ClaudeConfigManager(ConfigManager):
    """Claude Desktop 配置管理器"""
    
    def generate_config(self, install_path: Path) -> Dict[str, Any]:
        """生成 Claude Desktop 配置"""
        python_cmd = self._get_python_command()
        
        return {
            "mcpServers": {
                "fhl-bible": {
                    "command": python_cmd,
                    "args": ["-m", "fhl_bible_mcp.server"],
                    "env": {
                        "PYTHONPATH": str(install_path / "src")
                    }
                }
            }
        }
    
    def merge_config(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """合併配置"""
        if not existing:
            return new
        
        # 保留現有的 mcpServers
        if "mcpServers" not in existing:
            existing["mcpServers"] = {}
        
        # 添加或更新 fhl-bible 配置
        existing["mcpServers"]["fhl-bible"] = new["mcpServers"]["fhl-bible"]
        
        return existing
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """驗證配置"""
        if not isinstance(config, dict):
            return False
        
        if "mcpServers" not in config:
            return False
        
        if "fhl-bible" not in config["mcpServers"]:
            return False
        
        fhl_config = config["mcpServers"]["fhl-bible"]
        required_fields = ["command", "args"]
        
        return all(field in fhl_config for field in required_fields)
    
    def _get_python_command(self) -> str:
        """獲取 Python 命令"""
        import sys
        import shutil
        
        # 如果在虛擬環境中，使用當前 Python
        if hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        ):
            return sys.executable
        
        # 否則使用 PATH 中的 python
        python3 = shutil.which('python3')
        if python3:
            return 'python3'
        
        python = shutil.which('python')
        if python:
            return 'python'
        
        # 最後使用當前 Python 完整路徑
        return sys.executable


class VSCodeConfigManager(ConfigManager):
    """VS Code 配置管理器"""
    
    def generate_config(self, install_path: Path) -> Dict[str, Any]:
        """生成 VS Code 配置"""
        python_cmd = self._get_python_command()
        
        # 假設的格式，需要在 VS Code 支援後確認
        return {
            "github.copilot.mcpServers": {
                "fhl-bible": {
                    "command": python_cmd,
                    "args": ["-m", "fhl_bible_mcp.server"],
                    "env": {}
                }
            }
        }
    
    def merge_config(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """合併配置"""
        if not existing:
            return new
        
        # 保留現有設置
        if "github.copilot.mcpServers" not in existing:
            existing["github.copilot.mcpServers"] = {}
        
        # 更新 fhl-bible
        existing["github.copilot.mcpServers"]["fhl-bible"] = \
            new["github.copilot.mcpServers"]["fhl-bible"]
        
        return existing
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """驗證配置"""
        # 實作驗證邏輯
        pass
    
    def _get_python_command(self) -> str:
        """獲取 Python 命令"""
        # 同 ClaudeConfigManager
        pass


class OpenAIConfigManager(ConfigManager):
    """OpenAI Desktop 配置管理器"""
    
    def generate_config(self, install_path: Path) -> Dict[str, Any]:
        """生成 OpenAI Desktop 配置"""
        # 待 OpenAI Desktop 正式發布後實作
        pass
    
    def merge_config(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """合併配置"""
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """驗證配置"""
        pass
```

### 配置管理器工廠

```python
# factory.py
from typing import Optional

class ConfigManagerFactory:
    """配置管理器工廠"""
    
    @staticmethod
    def create(platform_name: str, config_path: Path) -> Optional[ConfigManager]:
        """創建配置管理器"""
        managers = {
            "claude": ClaudeConfigManager,
            "vscode": VSCodeConfigManager,
            "openai": OpenAIConfigManager,
            "cursor": CursorConfigManager,
        }
        
        manager_class = managers.get(platform_name)
        if not manager_class:
            return None
        
        return manager_class(platform_name, config_path)
```

---

## 安裝流程設計

### 完整安裝流程

```python
# installer.py
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

class PlatformInstaller:
    """平台安裝器"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.console = Console()
        self.detector = PlatformDetector()
        self.config_manager = None
    
    def install(self, auto_detect: bool = False) -> bool:
        """執行安裝"""
        try:
            # 1. 檢測平台
            platform_info = self._detect_platform()
            if not platform_info:
                self.console.print(f"[red]✗ {self.platform_name} not detected[/red]")
                return False
            
            # 2. 初始化配置管理器
            self.config_manager = ConfigManagerFactory.create(
                self.platform_name,
                platform_info.config_path
            )
            
            # 3. 檢查 Python 環境
            if not self._check_python_environment():
                return False
            
            # 4. 獲取安裝路徑
            install_path = self._get_install_path()
            
            # 5. 生成配置
            new_config = self.config_manager.generate_config(install_path)
            
            # 6. 備份現有配置
            backup_path = self.config_manager.backup_config()
            if backup_path:
                self.console.print(f"[yellow]Backed up config to: {backup_path}[/yellow]")
            
            # 7. 合併配置
            existing_config = self.config_manager.read_config()
            merged_config = self.config_manager.merge_config(existing_config, new_config)
            
            # 8. 驗證配置
            if not self.config_manager.validate_config(merged_config):
                self.console.print("[red]✗ Generated config is invalid[/red]")
                return False
            
            # 9. 寫入配置
            if not self.config_manager.write_config(merged_config):
                self.console.print("[red]✗ Failed to write config[/red]")
                if backup_path:
                    self.config_manager.restore_config(backup_path)
                return False
            
            # 10. 驗證安裝
            if not self._verify_installation():
                self.console.print("[red]✗ Installation verification failed[/red]")
                if backup_path:
                    self.config_manager.restore_config(backup_path)
                return False
            
            self.console.print(f"[green]✓ Successfully installed to {self.platform_name}![/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]✗ Installation failed: {e}[/red]")
            return False
    
    def _detect_platform(self) -> Optional[PlatformInfo]:
        """檢測平台"""
        platforms = self.detector.detect_all()
        for platform in platforms:
            if platform.name == self.platform_name:
                return platform
        return None
    
    def _check_python_environment(self) -> bool:
        """檢查 Python 環境"""
        import sys
        
        # 檢查 Python 版本
        if sys.version_info < (3, 10):
            self.console.print("[red]✗ Python 3.10+ required[/red]")
            return False
        
        # 檢查套件是否安裝
        try:
            import fhl_bible_mcp
        except ImportError:
            self.console.print("[red]✗ fhl-bible-mcp not installed[/red]")
            self.console.print("[yellow]Run: pip install fhl-bible-mcp[/yellow]")
            return False
        
        return True
    
    def _get_install_path(self) -> Path:
        """獲取安裝路徑"""
        import fhl_bible_mcp
        module_path = Path(fhl_bible_mcp.__file__).parent.parent
        return module_path
    
    def _verify_installation(self) -> bool:
        """驗證安裝"""
        # 檢查配置文件存在
        if not self.config_manager.config_path.exists():
            return False
        
        # 檢查配置格式正確
        config = self.config_manager.read_config()
        if not config:
            return False
        
        return self.config_manager.validate_config(config)
```

---

## 測試策略

### 單元測試

```python
# tests/test_platform_detection.py
import pytest
from fhl_bible_mcp.cli.platform.detector import PlatformDetector

def test_detect_claude_desktop():
    """測試 Claude Desktop 檢測"""
    detector = PlatformDetector()
    result = detector.detect_claude()
    
    # 如果安裝了 Claude Desktop
    if result:
        assert result.name == "claude"
        assert result.config_path.exists()
        assert result.is_installed == True

def test_detect_vscode():
    """測試 VS Code 檢測"""
    detector = PlatformDetector()
    result = detector.detect_vscode()
    
    if result:
        assert result.name == "vscode"
        assert result.display_name == "Visual Studio Code"

# tests/test_config_manager.py
def test_claude_config_generation():
    """測試 Claude 配置生成"""
    manager = ClaudeConfigManager("claude", Path("/tmp/test.json"))
    config = manager.generate_config(Path("/install/path"))
    
    assert "mcpServers" in config
    assert "fhl-bible" in config["mcpServers"]
    assert config["mcpServers"]["fhl-bible"]["command"] == "python"

def test_config_merge():
    """測試配置合併"""
    manager = ClaudeConfigManager("claude", Path("/tmp/test.json"))
    
    existing = {
        "mcpServers": {
            "other-server": {"command": "node"}
        }
    }
    
    new = {
        "mcpServers": {
            "fhl-bible": {"command": "python"}
        }
    }
    
    merged = manager.merge_config(existing, new)
    
    assert "other-server" in merged["mcpServers"]
    assert "fhl-bible" in merged["mcpServers"]
```

### 整合測試

```python
# tests/test_installation.py
def test_full_installation_flow():
    """測試完整安裝流程"""
    installer = PlatformInstaller("claude")
    
    # 使用測試配置路徑
    with patch('PlatformDetector.detect_claude') as mock_detect:
        mock_detect.return_value = PlatformInfo(
            name="claude",
            display_name="Claude Desktop",
            version="1.0.0",
            config_path=Path("/tmp/test_config.json"),
            is_installed=True,
            executable_path=None
        )
        
        result = installer.install()
        assert result == True
```

### 跨平台測試

使用 GitHub Actions 在多個作業系統上測試：

```yaml
# .github/workflows/test.yml
name: Cross-platform Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest tests/test_platform/
```

---

## 相關文檔

- 📄 [部署策略總覽](DEPLOYMENT_STRATEGY.md)
- 📄 [CLI 實作計劃](CLI_IMPLEMENTATION_PLAN.md)
- 📄 [開發路線圖](DEPLOYMENT_ROADMAP.md)

---

**文檔維護**: 平台支援情況應隨各平台 MCP API 發布持續更新

**最後更新**: 2025年11月1日
