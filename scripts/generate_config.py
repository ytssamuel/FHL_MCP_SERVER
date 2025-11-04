#!/usr/bin/env python3
"""
FHL Bible MCP Server - 配置生成器
自動生成 AI 助手的配置文件
"""

import sys
import os
import json
import platform
from pathlib import Path
from typing import Dict

def get_project_paths() -> Dict[str, str]:
    """獲取專案路徑"""
    script_dir = Path(__file__).parent.parent.resolve()
    src_dir = script_dir / 'src'
    cache_dir = script_dir / '.cache'
    
    system = platform.system()
    
    if system == "Windows":
        # Windows 使用雙反斜線
        # 使用 absolute() 而非 resolve() 來保留虛擬環境路徑
        venv_python = str((script_dir / 'venv' / 'Scripts' / 'python.exe').absolute()).replace('\\', '\\\\')
        src_path = str(src_dir.absolute()).replace('\\', '\\\\')
        cache_path = str(cache_dir.absolute()).replace('\\', '\\\\')
    else:
        # macOS/Linux
        # 使用 absolute() 而非 resolve() 來保留虛擬環境路徑（不解析 symlink）
        venv_python = str((script_dir / 'venv' / 'bin' / 'python').absolute())
        src_path = str(src_dir.absolute())
        cache_path = str(cache_dir.absolute())
    
    return {
        'venv_python': venv_python,
        'src_path': src_path,
        'cache_path': cache_path,
        'project_dir': str(script_dir)
    }

def generate_claude_config(paths: Dict[str, str]) -> Dict:
    """生成 Claude Desktop 配置"""
    # 使用虛擬環境的 Python 而不是系統 Python
    config = {
        "mcpServers": {
            "fhl-bible": {
                "command": paths['venv_python'],
                "args": [
                    "-m",
                    "fhl_bible_mcp"
                ],
                "env": {
                    "PYTHONPATH": paths['src_path'],
                    "LOG_LEVEL": "INFO",
                    "FHL_CACHE_DIR": paths['cache_path']
                }
            }
        }
    }
    
    return config

def generate_vscode_config(paths: Dict[str, str]) -> Dict:
    """生成 VS Code 配置"""
    config = {
        "github.copilot.chat.mcp.enabled": True,
        "github.copilot.chat.mcp.servers": {
            "fhl-bible": {
                "command": paths['venv_python'],
                "args": [
                    "-m",
                    "fhl_bible_mcp"
                ],
                "env": {
                    "PYTHONPATH": paths['src_path'],
                    "LOG_LEVEL": "INFO",
                    "FHL_CACHE_DIR": paths['cache_path']
                }
            }
        }
    }
    
    return config

def get_config_file_path(assistant: str) -> Path:
    """獲取配置文件路徑"""
    system = platform.system()
    
    if assistant == "claude":
        if system == "Windows":
            return Path(os.environ.get('APPDATA', '')) / 'Claude' / 'claude_desktop_config.json'
        elif system == "Darwin":
            return Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
        else:  # Linux
            return Path.home() / '.config' / 'Claude' / 'claude_desktop_config.json'
    
    elif assistant == "vscode":
        if system == "Windows":
            return Path(os.environ.get('APPDATA', '')) / 'Code' / 'User' / 'settings.json'
        elif system == "Darwin":
            return Path.home() / 'Library' / 'Application Support' / 'Code' / 'User' / 'settings.json'
        else:  # Linux
            return Path.home() / '.config' / 'Code' / 'User' / 'settings.json'
    
    return None

def print_config(config: Dict, title: str):
    """印出配置"""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}\n")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print()

def save_config_to_file(config: Dict, file_path: Path, merge: bool = True):
    """儲存配置到文件"""
    try:
        # 確保目錄存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果文件存在且需要合併
        if merge and file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = {}
            
            # 合併配置
            if 'mcpServers' in config:
                # Claude Desktop 配置
                if 'mcpServers' not in existing:
                    existing['mcpServers'] = {}
                existing['mcpServers'].update(config['mcpServers'])
            else:
                # VS Code 配置
                existing.update(config)
            
            config = existing
        
        # 寫入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"錯誤: {str(e)}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("FHL Bible MCP Server - 配置生成器")
    print("=" * 60)
    print()
    
    # 獲取專案路徑
    print("正在分析專案路徑...")
    paths = get_project_paths()
    print(f"專案目錄: {paths['project_dir']}")
    print(f"Python 路徑: {paths['venv_python']}")
    print(f"PYTHONPATH: {paths['src_path']}")
    print()
    
    # 選擇 AI 助手
    print("請選擇要配置的 AI 助手:")
    print("1. Claude Desktop (推薦)")
    print("2. VS Code / GitHub Copilot")
    print("3. 兩者都要")
    print("4. 只顯示配置（不寫入文件）")
    print()
    
    choice = input("請選擇 (1-4): ").strip()
    
    if choice not in ['1', '2', '3', '4']:
        print("無效的選擇")
        return 1
    
    # 生成配置
    claude_config = generate_claude_config(paths)
    vscode_config = generate_vscode_config(paths)
    
    # 根據選擇執行
    if choice in ['1', '3', '4']:
        print_config(claude_config, "Claude Desktop 配置")
        
        if choice != '4':
            config_path = get_config_file_path('claude')
            print(f"配置文件位置: {config_path}")
            
            if config_path.exists():
                merge = input("配置文件已存在，是否合併配置？(y/n): ").strip().lower() == 'y'
            else:
                merge = False
            
            confirm = input("確定要寫入配置文件嗎？(y/n): ").strip().lower()
            
            if confirm == 'y':
                if save_config_to_file(claude_config, config_path, merge):
                    print(f"✓ 配置已成功寫入: {config_path}")
                    print("\n請重啟 Claude Desktop 以應用配置")
                else:
                    print("✗ 配置寫入失敗")
    
    if choice in ['2', '3', '4']:
        print_config(vscode_config, "VS Code 配置")
        
        if choice != '4':
            config_path = get_config_file_path('vscode')
            print(f"配置文件位置: {config_path}")
            
            if config_path.exists():
                merge = True  # VS Code 配置總是合併
            else:
                merge = False
            
            confirm = input("確定要寫入配置文件嗎？(y/n): ").strip().lower()
            
            if confirm == 'y':
                if save_config_to_file(vscode_config, config_path, merge):
                    print(f"✓ 配置已成功寫入: {config_path}")
                    print("\n請在 VS Code 中執行 'Developer: Reload Window' 以應用配置")
                else:
                    print("✗ 配置寫入失敗")
    
    print("\n配置完成！")
    print("\n測試指令:")
    print("  查詢約翰福音 3:16")
    print("  使用 basic_help_guide 查看完整功能")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n錯誤: {str(e)}")
        sys.exit(1)
