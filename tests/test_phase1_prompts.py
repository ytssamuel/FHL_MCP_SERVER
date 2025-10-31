"""
測試 Phase 1 新增的 Prompts

測試 quick_lookup 和 tool_reference prompts
"""

import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_phase1_prompts():
    """測試 Phase 1 的兩個新 prompts"""
    print("=" * 70)
    print("測試 Phase 1 新增的 Prompts")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import (
            BasicQuickLookupPrompt,
            BasicToolReferencePrompt,
            PromptManager
        )
        print("✓ 成功導入 Phase 1 prompts")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        return False
    
    print("\n" + "=" * 70)
    print("測試 1：BasicQuickLookupPrompt")
    print("=" * 70)
    
    try:
        quick_lookup = BasicQuickLookupPrompt()
        print(f"✓ 實例化成功")
        print(f"  名稱：{quick_lookup.name}")
        print(f"  描述：{quick_lookup.description}")
        print(f"  參數數量：{len(quick_lookup.arguments)}")
        
        # 測試渲染
        prompt_text = quick_lookup.render(query="約翰福音 3:16")
        print(f"✓ 渲染成功（長度：{len(prompt_text)} 字元）")
        
        # 測試不同查詢類型
        test_queries = [
            "約翰福音 3:16",
            "詩篇 23",
            "愛",
            "腓利門書"
        ]
        
        print("\n  測試不同查詢類型：")
        for query in test_queries:
            text = quick_lookup.render(query=query, version="unv")
            print(f"    • {query}: {len(text)} 字元")
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("測試 2：BasicToolReferencePrompt")
    print("=" * 70)
    
    try:
        tool_ref = BasicToolReferencePrompt()
        print(f"✓ 實例化成功")
        print(f"  名稱：{tool_ref.name}")
        print(f"  描述：{tool_ref.description}")
        print(f"  參數數量：{len(tool_ref.arguments)}")
        
        # 測試全部工具
        all_tools_text = tool_ref.render()
        print(f"✓ 渲染所有工具成功（長度：{len(all_tools_text)} 字元）")
        
        # 測試特定工具
        single_tool_text = tool_ref.render(tool_name="get_bible_verse")
        print(f"✓ 渲染單一工具成功（長度：{len(single_tool_text)} 字元）")
        
        # 測試類別
        categories = ["verse", "search", "strongs", "commentary", "info", "audio"]
        print("\n  測試不同類別：")
        for category in categories:
            text = tool_ref.render(category=category)
            print(f"    • {category}: {len(text)} 字元")
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("測試 3：PromptManager 註冊")
    print("=" * 70)
    
    try:
        manager = PromptManager()
        prompts = manager.list_prompts()
        
        print(f"✓ 總共註冊 {len(prompts)} 個 prompts")
        
        # 檢查 Phase 1 prompts
        phase1_prompts = ["basic_help_guide", "basic_uri_demo", "basic_quick_lookup", "basic_tool_reference"]
        print("\n  Phase 1 Prompts 檢查：")
        for name in phase1_prompts:
            if manager.has_prompt(name):
                prompt = manager.get_prompt(name)
                print(f"    ✓ {name}: {prompt.description}")
            else:
                print(f"    ✗ {name}: 未找到")
                return False
        
        # 測試渲染
        print("\n  測試通過 Manager 渲染：")
        quick_text = manager.render_prompt("basic_quick_lookup", query="約翰福音 3:16")
        if quick_text:
            print(f"    ✓ basic_quick_lookup 渲染成功（{len(quick_text)} 字元）")
        else:
            print(f"    ✗ basic_quick_lookup 渲染失敗")
            return False
        
        tool_text = manager.render_prompt("basic_tool_reference")
        if tool_text:
            print(f"    ✓ basic_tool_reference 渲染成功（{len(tool_text)} 字元）")
        else:
            print(f"    ✗ basic_tool_reference 渲染失敗")
            return False
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_backward_compatibility():
    """測試向後兼容性"""
    print("\n" + "=" * 70)
    print("測試 4：向後兼容性")
    print("=" * 70)
    
    try:
        # 從 templates 導入
        from fhl_bible_mcp.prompts.templates import (
            QuickLookupPrompt,
            ToolReferencePrompt
        )
        print("✓ 從 templates.py 導入成功（向後兼容）")
        
        # 測試實例化
        quick = QuickLookupPrompt()
        tool = ToolReferencePrompt()
        print("✓ 實例化成功")
        
        return True
    except Exception as e:
        print(f"✗ 向後兼容性測試失敗：{e}")
        return False


def main():
    """執行所有測試"""
    print("\n" + "═" * 70)
    print(" Phase 1 Prompts 測試")
    print("═" * 70 + "\n")
    
    results = []
    
    # 測試 Phase 1 prompts
    results.append(("Phase 1 Prompts", test_phase1_prompts()))
    
    # 測試向後兼容
    results.append(("向後兼容性", test_backward_compatibility()))
    
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
        print("\n🎉 Phase 1 完成！所有測試通過！")
        print("\n已完成的 Prompts（新命名規則）：")
        print("  ✅ 1. basic_help_guide - 基礎｜使用指南")
        print("  ✅ 2. basic_uri_demo - 基礎｜URI 使用示範")
        print("  ✅ 3. basic_quick_lookup - 基礎｜快速查經")
        print("  ✅ 4. basic_tool_reference - 基礎｜工具參考")
        print("\n原有 Prompts（已重命名）：")
        print("  ✅ study_verse_deep - 研經｜深入研讀經文")
        print("  ✅ study_topic_deep - 研經｜主題研究")
        print("  ✅ study_translation_compare - 研經｜版本比較")
        print("  ✅ study_word_original - 研經｜原文字詞研究")
        print("\n下一步：Phase 2 - 讀經輔助系列")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 個測試失敗")
        return 1


if __name__ == "__main__":
    exit(main())
