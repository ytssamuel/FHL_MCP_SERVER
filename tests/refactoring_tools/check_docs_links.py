"""
文件連結驗證腳本

檢查所有 .md 文件中的內部連結是否正確
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def find_broken_links() -> List[Tuple[str, str, str]]:
    """
    查找所有損壞的內部連結
    
    Returns:
        List[Tuple[str, str, str]]: (文件路徑, 損壞的連結, 行號)
    """
    broken_links = []
    project_root = Path(__file__).parent.parent.parent
    
    # 查找所有 .md 文件
    md_files = list(project_root.rglob("*.md"))
    
    # 正則表達式匹配 Markdown 連結
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    print("🔍 開始檢查文件連結...")
    print(f"找到 {len(md_files)} 個 Markdown 文件\n")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # 逐行檢查連結
            for line_num, line in enumerate(lines, 1):
                matches = link_pattern.findall(line)
                
                for link_text, link_url in matches:
                    # 跳過外部連結和錨點
                    if link_url.startswith(('http://', 'https://', '#', 'mailto:')):
                        continue
                    
                    # 移除錨點部分
                    link_path = link_url.split('#')[0]
                    if not link_path:
                        continue
                    
                    # 解析相對路徑
                    if link_path.startswith('/'):
                        # 絕對路徑
                        target_path = project_root / link_path[1:]
                    else:
                        # 相對路徑
                        target_path = (md_file.parent / link_path).resolve()
                    
                    # 檢查文件是否存在
                    if not target_path.exists():
                        rel_path = md_file.relative_to(project_root)
                        broken_links.append((
                            str(rel_path),
                            link_url,
                            line_num
                        ))
        
        except Exception as e:
            print(f"⚠️  處理文件時出錯 {md_file}: {e}")
    
    return broken_links


def print_results(broken_links: List[Tuple[str, str, str]]):
    """列印檢查結果"""
    print("=" * 70)
    
    if not broken_links:
        print("✅ 所有連結檢查通過！沒有發現損壞的連結。")
        print("\n📊 檢查統計:")
        print("  • 所有內部連結都正確指向目標文件")
        print("  • 文件路徑正確")
        print("  • 組織結構完整")
    else:
        print(f"⚠️  發現 {len(broken_links)} 個損壞的連結：\n")
        
        # 按文件分組顯示
        current_file = None
        for file_path, link, line_num in sorted(broken_links):
            if file_path != current_file:
                if current_file is not None:
                    print()
                print(f"📄 {file_path}:")
                current_file = file_path
            
            print(f"   ❌ Line {line_num}: {link}")
        
        print(f"\n總共發現 {len(broken_links)} 個損壞的連結")
    
    print("=" * 70)


def check_specific_docs_links():
    """檢查 docs/ 資料夾特定的舊路徑"""
    print("\n🔎 檢查 docs/ 舊路徑引用...")
    
    project_root = Path(__file__).parent.parent.parent
    docs_path = project_root / "docs"
    
    # 需要檢查的舊路徑模式
    old_patterns = [
        r'docs/PROMPTS_USAGE_GUIDE\.md',
        r'docs/PROMPTS_ENHANCEMENT_PLAN\.md',
        r'docs/DEVELOPER_GUIDE\.md',
        r'docs/INSTALLATION_GUIDE\.md',
        r'docs/API\.md',
        r'docs/EXAMPLES\.md',
        r'docs/PHASE_\d+',
        r'docs/PROMPTS_COMPLETE_REFACTORING',
        r'docs/PROMPTS_IMPROVEMENT',
        r'docs/PROMPTS_DIAGNOSTIC',
    ]
    
    issues = []
    
    for md_file in project_root.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in old_patterns:
                if re.search(pattern, content):
                    rel_path = md_file.relative_to(project_root)
                    issues.append((str(rel_path), pattern))
        
        except Exception as e:
            pass
    
    if issues:
        print("\n⚠️  發現使用舊路徑的引用：\n")
        for file_path, pattern in issues:
            print(f"  ❌ {file_path}: {pattern}")
    else:
        print("  ✅ 沒有發現舊路徑引用")


if __name__ == "__main__":
    print("🔍 開始驗證文件連結...")
    print("=" * 70)
    
    # 檢查損壞的連結
    broken_links = find_broken_links()
    print_results(broken_links)
    
    # 檢查舊路徑
    check_specific_docs_links()
    
    print("\n✨ 檢查完成！")
    
    # 返回狀態碼
    exit(0 if not broken_links else 1)
