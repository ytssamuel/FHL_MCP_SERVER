#!/usr/bin/env python3
"""
FHL Bible MCP Server - 環境驗證腳本
驗證安裝環境是否正確配置
"""

import sys
import os
import json
import platform
from pathlib import Path
from typing import Tuple, List, Dict

# ANSI 顏色碼
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def colored(text: str, color: str) -> str:
    """返回帶顏色的文字"""
    return f"{color}{text}{Colors.RESET}"

def print_header(text: str):
    """印出標題"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")

def print_result(check_name: str, passed: bool, message: str = ""):
    """印出檢查結果"""
    status = colored("✓ PASS", Colors.GREEN) if passed else colored("✗ FAIL", Colors.RED)
    print(f"{status} - {check_name}")
    if message:
        print(f"      {message}")

def check_python_version() -> Tuple[bool, str]:
    """檢查 Python 版本"""
    version = sys.version_info
    required = (3, 10)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (需要 >= 3.10)"

def check_virtual_env() -> Tuple[bool, str]:
    """檢查是否在虛擬環境中"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        return True, f"虛擬環境: {sys.prefix}"
    else:
        return False, "未在虛擬環境中執行"

def check_project_structure() -> Tuple[bool, str]:
    """檢查專案結構"""
    script_dir = Path(__file__).parent.parent
    required_paths = [
        'src/fhl_bible_mcp',
        'src/fhl_bible_mcp/server.py',
        'src/fhl_bible_mcp/api',
        'src/fhl_bible_mcp/tools',
        'pyproject.toml'
    ]
    
    missing = []
    for path in required_paths:
        if not (script_dir / path).exists():
            missing.append(path)
    
    if not missing:
        return True, "專案結構完整"
    else:
        return False, f"缺少文件/目錄: {', '.join(missing)}"

def check_package_installed() -> Tuple[bool, str]:
    """檢查套件是否已安裝"""
    try:
        import fhl_bible_mcp
        version = getattr(fhl_bible_mcp, '__version__', 'unknown')
        return True, f"fhl-bible-mcp {version} 已安裝"
    except ImportError:
        return False, "fhl-bible-mcp 未安裝"

def check_dependencies() -> Tuple[bool, str, List[str]]:
    """檢查必要依賴"""
    required_packages = {
        'httpx': 'httpx',
        'mcp': 'mcp',
    }
    
    missing = []
    installed = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            installed.append(package_name)
        except ImportError:
            missing.append(package_name)
    
    if not missing:
        return True, f"所有依賴已安裝 ({len(installed)} 個)", installed
    else:
        return False, f"缺少依賴: {', '.join(missing)}", installed

def check_server_import() -> Tuple[bool, str]:
    """檢查 server 模組是否可以導入"""
    try:
        from fhl_bible_mcp import server
        return True, "server 模組可正常導入"
    except ImportError as e:
        return False, f"無法導入 server 模組: {str(e)}"

def check_pythonpath() -> Tuple[bool, str]:
    """檢查 PYTHONPATH 是否正確設置"""
    script_dir = Path(__file__).parent.parent
    src_dir = script_dir / 'src'
    
    # 檢查 src 是否在 sys.path 中
    src_in_path = str(src_dir.resolve()) in [str(Path(p).resolve()) for p in sys.path]
    
    if src_in_path:
        return True, f"PYTHONPATH 包含 src 目錄"
    else:
        return False, f"PYTHONPATH 未包含 {src_dir}"

def check_cache_dir() -> Tuple[bool, str]:
    """檢查快取目錄"""
    cache_dir = os.environ.get('FHL_CACHE_DIR')
    
    if cache_dir:
        cache_path = Path(cache_dir)
        if cache_path.exists():
            return True, f"快取目錄: {cache_dir}"
        else:
            return False, f"快取目錄不存在: {cache_dir}"
    else:
        # 檢查預設位置
        default_cache = Path.home() / '.cache' / 'fhl_bible_mcp'
        if default_cache.exists():
            return True, f"使用預設快取目錄: {default_cache}"
        else:
            return True, "快取目錄未設定（將使用預設位置）"

def check_config_files() -> Tuple[bool, str, Dict]:
    """檢查 AI 助手配置文件"""
    system = platform.system()
    configs = {}
    
    # Claude Desktop 配置
    if system == "Windows":
        claude_config = Path(os.environ.get('APPDATA', '')) / 'Claude' / 'claude_desktop_config.json'
    elif system == "Darwin":  # macOS
        claude_config = Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
    else:  # Linux
        claude_config = Path.home() / '.config' / 'Claude' / 'claude_desktop_config.json'
    
    configs['Claude Desktop'] = {
        'path': claude_config,
        'exists': claude_config.exists(),
        'configured': False
    }
    
    if claude_config.exists():
        try:
            with open(claude_config, 'r', encoding='utf-8') as f:
                data = json.load(f)
                configs['Claude Desktop']['configured'] = 'fhl-bible' in data.get('mcpServers', {})
        except:
            pass
    
    # VS Code 配置
    if system == "Windows":
        vscode_config = Path(os.environ.get('APPDATA', '')) / 'Code' / 'User' / 'settings.json'
    elif system == "Darwin":
        vscode_config = Path.home() / 'Library' / 'Application Support' / 'Code' / 'User' / 'settings.json'
    else:
        vscode_config = Path.home() / '.config' / 'Code' / 'User' / 'settings.json'
    
    configs['VS Code'] = {
        'path': vscode_config,
        'exists': vscode_config.exists(),
        'configured': False
    }
    
    if vscode_config.exists():
        try:
            with open(vscode_config, 'r', encoding='utf-8') as f:
                data = json.load(f)
                servers = data.get('github.copilot.chat.mcp.servers', {})
                configs['VS Code']['configured'] = 'fhl-bible' in servers
        except:
            pass
    
    # 總結
    configured_count = sum(1 for c in configs.values() if c['configured'])
    
    if configured_count > 0:
        return True, f"找到 {configured_count} 個已配置的 AI 助手", configs
    else:
        return False, "未找到已配置的 AI 助手", configs

def print_config_details(configs: Dict):
    """印出配置詳情"""
    print(f"\n{Colors.BOLD}配置文件狀態:{Colors.RESET}")
    for name, info in configs.items():
        exists_status = colored("存在", Colors.GREEN) if info['exists'] else colored("不存在", Colors.YELLOW)
        config_status = colored("已配置", Colors.GREEN) if info['configured'] else colored("未配置", Colors.YELLOW)
        print(f"  {name}:")
        print(f"    文件: {exists_status}")
        print(f"    MCP: {config_status}")
        print(f"    路徑: {info['path']}")

def print_recommendations(results: Dict):
    """印出建議"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}建議事項:{Colors.RESET}")
    
    recommendations = []
    
    if not results['venv'][0]:
        recommendations.append("• 請在虛擬環境中運行：source venv/bin/activate (macOS/Linux) 或 .\\venv\\Scripts\\activate (Windows)")
    
    if not results['package'][0]:
        recommendations.append("• 請安裝套件：pip install -e .")
    
    if not results['dependencies'][0]:
        recommendations.append("• 請安裝依賴：pip install -e .")
    
    if not results['config'][0]:
        recommendations.append(f"• 請配置 AI 助手，參考文檔：docs/1_development/INSTALLATION_GUIDE.md")
    
    if not recommendations:
        print(f"{colored('✓', Colors.GREEN)} 所有檢查都通過！您的環境已正確配置。")
    else:
        for rec in recommendations:
            print(rec)

def main():
    """主函數"""
    print_header("FHL Bible MCP Server - 環境驗證")
    
    print(f"{Colors.BOLD}系統資訊:{Colors.RESET}")
    print(f"  作業系統: {platform.system()} {platform.release()}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  專案目錄: {Path(__file__).parent.parent}")
    
    print(f"\n{Colors.BOLD}開始驗證...{Colors.RESET}\n")
    
    results = {}
    
    # 1. Python 版本
    passed, msg = check_python_version()
    results['python'] = (passed, msg)
    print_result("Python 版本", passed, msg)
    
    # 2. 虛擬環境
    passed, msg = check_virtual_env()
    results['venv'] = (passed, msg)
    print_result("虛擬環境", passed, msg)
    
    # 3. 專案結構
    passed, msg = check_project_structure()
    results['structure'] = (passed, msg)
    print_result("專案結構", passed, msg)
    
    # 4. 套件安裝
    passed, msg = check_package_installed()
    results['package'] = (passed, msg)
    print_result("套件安裝", passed, msg)
    
    # 5. 依賴檢查
    passed, msg, installed = check_dependencies()
    results['dependencies'] = (passed, msg)
    print_result("必要依賴", passed, msg)
    
    # 6. PYTHONPATH
    passed, msg = check_pythonpath()
    results['pythonpath'] = (passed, msg)
    print_result("PYTHONPATH", passed, msg)
    
    # 7. Server 導入
    passed, msg = check_server_import()
    results['server'] = (passed, msg)
    print_result("Server 模組", passed, msg)
    
    # 8. 快取目錄
    passed, msg = check_cache_dir()
    results['cache'] = (passed, msg)
    print_result("快取目錄", passed, msg)
    
    # 9. 配置文件
    passed, msg, configs = check_config_files()
    results['config'] = (passed, msg)
    print_result("AI 助手配置", passed, msg)
    print_config_details(configs)
    
    # 總結
    print_header("驗證結果")
    
    total = len(results)
    passed_count = sum(1 for p, _ in results.values() if p)
    
    print(f"{Colors.BOLD}總計:{Colors.RESET} {passed_count}/{total} 項檢查通過")
    
    if passed_count == total:
        print(f"\n{colored('🎉 恭喜！所有檢查都通過！', Colors.GREEN)}")
        print(f"\n您可以開始使用 FHL Bible MCP Server 了。")
        print(f"試試在 AI 助手中輸入：{colored('查詢約翰福音 3:16', Colors.BLUE)}")
    else:
        print(f"\n{colored('⚠️  有些檢查未通過', Colors.YELLOW)}")
        print_recommendations(results)
    
    print(f"\n如需幫助，請參閱：{colored('docs/1_development/INSTALLATION_GUIDE.md', Colors.BLUE)}\n")
    
    # 返回狀態碼
    return 0 if passed_count == total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{colored('已取消', Colors.YELLOW)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{colored(f'錯誤: {str(e)}', Colors.RED)}")
        sys.exit(1)
