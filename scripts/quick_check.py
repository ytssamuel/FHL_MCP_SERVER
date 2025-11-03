#!/usr/bin/env python3
"""
FHL Bible MCP Server - 快速驗證腳本
在安裝前檢查基本環境
"""

import sys
import platform
from pathlib import Path

def check_python_version():
    """檢查 Python 版本"""
    version = sys.version_info
    required = (3, 10)
    
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version >= required:
        print("✓ Python 版本符合要求 (>= 3.10)")
        return True
    else:
        print(f"✗ Python 版本過低 (需要 >= 3.10)")
        return False

def check_system():
    """檢查作業系統"""
    system = platform.system()
    print(f"作業系統: {system} {platform.release()}")
    
    if system in ['Windows', 'Darwin', 'Linux']:
        print(f"✓ 支援的作業系統")
        return True
    else:
        print(f"⚠ 未測試的作業系統")
        return False

def check_project_files():
    """檢查必要的專案文件"""
    script_dir = Path(__file__).parent.parent
    required_files = [
        'pyproject.toml',
        'src/fhl_bible_mcp/server.py',
        'README.md'
    ]
    
    print("\n檢查專案文件:")
    all_exist = True
    for file in required_files:
        path = script_dir / file
        exists = path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def main():
    """主函數"""
    print("=" * 50)
    print("FHL Bible MCP Server - 環境快速檢查")
    print("=" * 50)
    print()
    
    results = []
    
    # 檢查 Python 版本
    results.append(check_python_version())
    print()
    
    # 檢查作業系統
    results.append(check_system())
    print()
    
    # 檢查專案文件
    results.append(check_project_files())
    print()
    
    # 總結
    print("=" * 50)
    if all(results):
        print("✓ 所有基本檢查通過！")
        print("\n您可以執行安裝腳本：")
        if platform.system() == 'Windows':
            print("  .\\scripts\\install.bat")
        else:
            print("  bash scripts/install.sh")
    else:
        print("✗ 有些檢查未通過")
        print("\n請先修正上述問題再進行安裝")
    print("=" * 50)
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n錯誤: {str(e)}")
        sys.exit(1)
