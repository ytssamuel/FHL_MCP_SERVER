"""
測試新的模組化 Prompts 結構

用途：驗證重構後的 prompts 模組是否正常工作
"""

import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """測試所有導入是否正常"""
    print("=" * 70)
    print("測試 1：基礎導入")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import PromptTemplate, PromptManager
        print("✓ 成功導入 PromptTemplate 和 PromptManager")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        return False
    
    print("\n" + "=" * 70)
    print("測試 2：基礎 Prompts 導入")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import HelpGuidePrompt, URIDemoPrompt
        print("✓ 成功導入 HelpGuidePrompt")
        print("✓ 成功導入 URIDemoPrompt")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        return False
    
    print("\n" + "=" * 70)
    print("測試 3：研經 Prompts 導入")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import (
            StudyVersePrompt,
            SearchTopicPrompt,
            CompareTranslationsPrompt,
            WordStudyPrompt
        )
        print("✓ 成功導入 StudyVersePrompt")
        print("✓ 成功導入 SearchTopicPrompt")
        print("✓ 成功導入 CompareTranslationsPrompt")
        print("✓ 成功導入 WordStudyPrompt")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        return False
    
    print("\n" + "=" * 70)
    print("測試 4：向後兼容性（從 templates 導入）")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts.templates import (
            PromptTemplate,
            PromptManager,
            StudyVersePrompt,
            HelpGuidePrompt
        )
        print("✓ 成功從 templates.py 導入所有類別")
        print("✓ 向後兼容性正常")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        return False
    
    return True


def test_prompt_manager():
    """測試 PromptManager 功能"""
    print("\n" + "=" * 70)
    print("測試 5：PromptManager 功能")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import PromptManager
        
        # 創建管理器實例
        manager = PromptManager()
        print("✓ 成功創建 PromptManager 實例")
        
        # 列出所有 prompts
        prompts = manager.list_prompts()
        print(f"✓ 註冊的 Prompts 數量：{len(prompts)}")
        
        print("\n註冊的 Prompts：")
        for prompt in prompts:
            print(f"  • {prompt['name']}: {prompt['description']}")
        
        # 測試取得特定 prompt
        help_prompt = manager.get_prompt("help_guide")
        if help_prompt:
            print("\n✓ 成功取得 help_guide prompt")
            print(f"  名稱：{help_prompt.name}")
            print(f"  描述：{help_prompt.description}")
        else:
            print("\n✗ 無法取得 help_guide prompt")
            return False
        
        # 測試渲染 prompt
        uri_demo_text = manager.render_prompt("uri_demo", uri_type="all")
        if uri_demo_text:
            print("\n✓ 成功渲染 uri_demo prompt")
            print(f"  渲染結果長度：{len(uri_demo_text)} 字元")
        else:
            print("\n✗ 無法渲染 uri_demo prompt")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_prompt_instances():
    """測試 Prompt 實例化和渲染"""
    print("\n" + "=" * 70)
    print("測試 6：Prompt 實例化和渲染")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import (
            HelpGuidePrompt,
            URIDemoPrompt,
            StudyVersePrompt
        )
        
        # 測試 HelpGuidePrompt
        help_guide = HelpGuidePrompt()
        print(f"✓ HelpGuidePrompt 實例化成功")
        print(f"  名稱：{help_guide.name}")
        print(f"  參數：{len(help_guide.arguments)} 個")
        
        # 渲染測試
        help_text = help_guide.render(section="all")
        print(f"✓ 渲染成功（長度：{len(help_text)} 字元）")
        
        # 測試 URIDemoPrompt
        uri_demo = URIDemoPrompt()
        print(f"\n✓ URIDemoPrompt 實例化成功")
        print(f"  名稱：{uri_demo.name}")
        
        # 測試不同類型
        for uri_type in ["all", "bible", "strongs", "commentary", "info"]:
            text = uri_demo.render(uri_type=uri_type)
            print(f"  • {uri_type}: {len(text)} 字元")
        
        # 測試 StudyVersePrompt
        study_verse = StudyVersePrompt()
        print(f"\n✓ StudyVersePrompt 實例化成功")
        verse_text = study_verse.render(book="John", chapter=3, verse=16)
        print(f"✓ 渲染成功（長度：{len(verse_text)} 字元）")
        
        return True
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """執行所有測試"""
    print("\n" + "═" * 70)
    print(" FHL Bible MCP Server - Prompts 模組化重構測試")
    print("═" * 70 + "\n")
    
    results = []
    
    # 測試導入
    results.append(("導入測試", test_imports()))
    
    # 測試 PromptManager
    results.append(("PromptManager 測試", test_prompt_manager()))
    
    # 測試 Prompt 實例
    results.append(("Prompt 實例測試", test_prompt_instances()))
    
    # 總結
    print("\n" + "═" * 70)
    print(" 測試總結")
    print("═" * 70)
    
    for name, success in results:
        status = "✓ 通過" if success else "✗ 失敗"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\n總計：{passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！重構成功！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 個測試失敗")
        return 1


if __name__ == "__main__":
    exit(main())
