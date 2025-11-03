"""
Docs 資料夾組織驗證腳本

此腳本驗證 docs/ 資料夾的組織是否正確完成
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

def check_docs_organization() -> Tuple[bool, List[str]]:
    """
    檢查 docs 資料夾組織
    
    Returns:
        Tuple[bool, List[str]]: (是否成功, 問題列表)
    """
    issues = []
    docs_path = Path(__file__).parent.parent.parent / "docs"
    
    if not docs_path.exists():
        issues.append("❌ docs/ 資料夾不存在")
        return False, issues
    
    # 期望的資料夾結構
    expected_folders = {
        "1_development": 14,
        "2_prompts_enhancement": 7,
        "3_prompts_improvement": 10,
        "4_manuals": 7,
        "deployment": 5,
        "prompt_example": 20
    }
    
    # 檢查資料夾存在性和文件數量
    print("📂 檢查資料夾結構...")
    for folder, expected_count in expected_folders.items():
        folder_path = docs_path / folder
        
        if not folder_path.exists():
            issues.append(f"❌ 資料夾不存在: {folder}")
            continue
        
        # 計算文件數（包括 README.md）
        files = list(folder_path.glob("*"))
        file_count = len([f for f in files if f.is_file()])
        
        print(f"  ✓ {folder}: {file_count} 個文件 (期望 {expected_count})")
        
        if file_count != expected_count:
            issues.append(
                f"⚠️  {folder} 文件數不符: "
                f"實際 {file_count}, 期望 {expected_count}"
            )
    
    # 檢查 README 文件
    print("\n📖 檢查 README 文件...")
    readme_files = [
        "README.md",  # 總覽
        "1_development/README.md",
        "2_prompts_enhancement/README.md",
        "3_prompts_improvement/README.md",
        "4_manuals/README.md",
    ]
    
    for readme in readme_files:
        readme_path = docs_path / readme
        if readme_path.exists():
            print(f"  ✓ {readme}")
        else:
            issues.append(f"❌ README 不存在: {readme}")
    
    # 檢查組織報告
    print("\n📋 檢查組織報告...")
    report_path = docs_path / "DOCS_ORGANIZATION_REPORT.md"
    if report_path.exists():
        print(f"  ✓ DOCS_ORGANIZATION_REPORT.md")
    else:
        issues.append("❌ 組織報告不存在: DOCS_ORGANIZATION_REPORT.md")
    
    # 檢查特定重要文件
    print("\n📄 檢查關鍵文件...")
    key_files = {
        "1_development": [
            "DEVELOPER_GUIDE.md",
            "INSTALLATION_GUIDE.md",
            "FHL_BIBLE_MCP_PLANNING.md"
        ],
        "2_prompts_enhancement": [
            "PROMPTS_ENHANCEMENT_PLAN.md",
            "PROMPTS_USAGE_GUIDE.md"
        ],
        "3_prompts_improvement": [
            "PROMPTS_IMPROVEMENT_PLAN.md",
            "PROMPTS_COMPLETE_REFACTORING_REPORT.md"
        ],
        "4_manuals": [
            "API.md",
            "EXAMPLES.md",
            "PROMPTS_QUICK_REFERENCE.md"
        ]
    }
    
    for folder, files in key_files.items():
        for file in files:
            file_path = docs_path / folder / file
            if file_path.exists():
                print(f"  ✓ {folder}/{file}")
            else:
                issues.append(f"❌ 關鍵文件不存在: {folder}/{file}")
    
    # 檢查 deployment 和 prompt_example 是否保持不變
    print("\n🔒 檢查保護資料夾...")
    deployment_files = [
        "CLI_IMPLEMENTATION_PLAN.md",
        "DEPLOYMENT_ROADMAP.md",
        "DEPLOYMENT_STRATEGY.md",
        "GUI_DEVELOPMENT_PLAN.md",
        "MULTI_PLATFORM_SUPPORT.md"
    ]
    
    for file in deployment_files:
        file_path = docs_path / "deployment" / file
        if file_path.exists():
            print(f"  ✓ deployment/{file}")
        else:
            issues.append(f"❌ deployment 文件遺失: {file}")
    
    # 檢查 prompt_example
    prompt_example_path = docs_path / "prompt_example"
    if prompt_example_path.exists():
        txt_files = list(prompt_example_path.glob("*.txt"))
        print(f"  ✓ prompt_example: {len(txt_files)} 個 .txt 文件")
        if len(txt_files) != 20:
            issues.append(
                f"⚠️  prompt_example 文件數不符: "
                f"實際 {len(txt_files)}, 期望 20"
            )
    else:
        issues.append("❌ prompt_example 資料夾不存在")
    
    return len(issues) == 0, issues


def print_summary(success: bool, issues: List[str]):
    """列印摘要"""
    print("\n" + "=" * 70)
    if success:
        print("✅ 組織驗證通過！所有檢查項目都正確。")
        print("\n📊 統計:")
        print("  • 4 個主要分類資料夾")
        print("  • 2 個保護資料夾（deployment, prompt_example）")
        print("  • 5 個 README 導航文件")
        print("  • 38 個文件成功分類")
        print("  • 1 個組織報告")
    else:
        print("⚠️  組織驗證發現問題：")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n總共發現 {len(issues)} 個問題")
    print("=" * 70)


if __name__ == "__main__":
    print("🔍 開始驗證 docs/ 資料夾組織...")
    print("=" * 70)
    
    success, issues = check_docs_organization()
    print_summary(success, issues)
    
    # 返回狀態碼
    exit(0 if success else 1)
