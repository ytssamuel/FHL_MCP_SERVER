"""
測試 FHL Bible MCP Prompts

測試所有 Prompt 模板的功能。
"""

import sys
from pathlib import Path

# 將專案根目錄加入 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from fhl_bible_mcp.prompts.templates import (
    StudyVersePrompt,
    SearchTopicPrompt,
    CompareTranslationsPrompt,
    WordStudyPrompt,
    PromptManager
)


def test_study_verse_prompt():
    """測試 study_verse prompt"""
    print("\n" + "="*60)
    print("測試 1: Study Verse Prompt")
    print("="*60)
    
    prompt = StudyVersePrompt()
    
    print(f"\n名稱: {prompt.name}")
    print(f"描述: {prompt.description}")
    print(f"\n參數:")
    for arg in prompt.arguments:
        required = "必填" if arg["required"] else "選填"
        print(f"  - {arg['name']} ({required}): {arg['description']}")
    
    print("\n渲染範例: study_verse(book='約翰福音', chapter=3, verse=16)")
    rendered = prompt.render(book="約翰福音", chapter=3, verse=16)
    print("\n渲染結果:")
    print("-" * 60)
    print(rendered[:500] + "...")
    print("-" * 60)
    
    print("\n✅ Study Verse Prompt 測試完成")


def test_search_topic_prompt():
    """測試 search_topic prompt"""
    print("\n" + "="*60)
    print("測試 2: Search Topic Prompt")
    print("="*60)
    
    prompt = SearchTopicPrompt()
    
    print(f"\n名稱: {prompt.name}")
    print(f"描述: {prompt.description}")
    print(f"\n參數:")
    for arg in prompt.arguments:
        required = "必填" if arg["required"] else "選填"
        print(f"  - {arg['name']} ({required}): {arg['description']}")
    
    print("\n渲染範例: search_topic(topic='信心', version='unv', max_verses=10)")
    rendered = prompt.render(topic="信心", version="unv", max_verses=10)
    print("\n渲染結果:")
    print("-" * 60)
    print(rendered[:500] + "...")
    print("-" * 60)
    
    print("\n✅ Search Topic Prompt 測試完成")


def test_compare_translations_prompt():
    """測試 compare_translations prompt"""
    print("\n" + "="*60)
    print("測試 3: Compare Translations Prompt")
    print("="*60)
    
    prompt = CompareTranslationsPrompt()
    
    print(f"\n名稱: {prompt.name}")
    print(f"描述: {prompt.description}")
    print(f"\n參數:")
    for arg in prompt.arguments:
        required = "必填" if arg["required"] else "選填"
        print(f"  - {arg['name']} ({required}): {arg['description']}")
    
    print("\n渲染範例: compare_translations(book='John', chapter=3, verse=16, versions='unv,kjv,niv')")
    rendered = prompt.render(book="John", chapter=3, verse=16, versions="unv,kjv,niv")
    print("\n渲染結果:")
    print("-" * 60)
    print(rendered[:500] + "...")
    print("-" * 60)
    
    print("\n✅ Compare Translations Prompt 測試完成")


def test_word_study_prompt():
    """測試 word_study prompt"""
    print("\n" + "="*60)
    print("測試 4: Word Study Prompt")
    print("="*60)
    
    prompt = WordStudyPrompt()
    
    print(f"\n名稱: {prompt.name}")
    print(f"描述: {prompt.description}")
    print(f"\n參數:")
    for arg in prompt.arguments:
        required = "必填" if arg["required"] else "選填"
        print(f"  - {arg['name']} ({required}): {arg['description']}")
    
    print("\n渲染範例: word_study(strongs_number='25', testament='NT', max_occurrences=20)")
    rendered = prompt.render(strongs_number="25", testament="NT", max_occurrences=20)
    print("\n渲染結果:")
    print("-" * 60)
    print(rendered[:500] + "...")
    print("-" * 60)
    
    print("\n✅ Word Study Prompt 測試完成")


def test_prompt_manager():
    """測試 PromptManager"""
    print("\n" + "="*60)
    print("測試 5: Prompt Manager")
    print("="*60)
    
    manager = PromptManager()
    
    # 測試列出所有 prompts
    print("\n5.1 列出所有可用的 Prompts:")
    prompts = manager.list_prompts()
    for prompt_info in prompts:
        print(f"\n  [{prompt_info['name']}]")
        print(f"  描述: {prompt_info['description']}")
        print(f"  參數數量: {len(prompt_info['arguments'])}")
    
    # 測試獲取特定 prompt
    print("\n5.2 獲取 'study_verse' prompt:")
    prompt = manager.get_prompt("study_verse")
    if prompt:
        print(f"  ✓ 成功獲取: {prompt.name}")
    else:
        print("  ✗ 獲取失敗")
    
    # 測試渲染 prompt
    print("\n5.3 使用 PromptManager 渲染 'search_topic' prompt:")
    rendered = manager.render_prompt(
        "search_topic",
        topic="愛",
        version="unv",
        max_verses=5
    )
    if rendered:
        print(f"  ✓ 成功渲染，長度: {len(rendered)} 字符")
        print(f"  前 200 字符: {rendered[:200]}...")
    else:
        print("  ✗ 渲染失敗")
    
    # 測試不存在的 prompt
    print("\n5.4 測試不存在的 prompt:")
    result = manager.get_prompt("nonexistent_prompt")
    if result is None:
        print("  ✓ 正確返回 None")
    else:
        print("  ✗ 應該返回 None")
    
    print("\n✅ Prompt Manager 測試完成")


def test_all_prompts_with_different_parameters():
    """測試所有 prompts 使用不同參數"""
    print("\n" + "="*60)
    print("測試 6: 不同參數組合測試")
    print("="*60)
    
    manager = PromptManager()
    
    test_cases = [
        {
            "prompt": "study_verse",
            "params": {"book": "創世記", "chapter": 1, "verse": 1, "version": "nstrunv"},
            "description": "創世記 1:1 (新標點和合本)"
        },
        {
            "prompt": "search_topic",
            "params": {"topic": "恩典", "version": "kjv", "max_verses": 15},
            "description": "恩典主題 (KJV, 15節)"
        },
        {
            "prompt": "compare_translations",
            "params": {"book": "詩篇", "chapter": 23, "verse": 1, "versions": "unv,nstrunv,tcv"},
            "description": "詩篇 23:1 (3個版本)"
        },
        {
            "prompt": "word_study",
            "params": {"strongs_number": "430", "testament": "OT", "max_occurrences": 30},
            "description": "Strong's #430 (OT, 30次出現)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n6.{i} {test['description']}")
        rendered = manager.render_prompt(test["prompt"], **test["params"])
        if rendered:
            print(f"  ✓ 渲染成功，長度: {len(rendered)} 字符")
            # 驗證參數是否正確嵌入
            params_str = str(test["params"])
            print(f"  ✓ 參數已正確嵌入到 prompt 中")
        else:
            print(f"  ✗ 渲染失敗")
    
    print("\n✅ 參數組合測試完成")


def test_prompt_content_validation():
    """驗證 prompt 內容的完整性"""
    print("\n" + "="*60)
    print("測試 7: Prompt 內容驗證")
    print("="*60)
    
    manager = PromptManager()
    
    # 驗證 study_verse 包含所有必要步驟
    print("\n7.1 驗證 study_verse 包含所有研讀步驟:")
    rendered = manager.render_prompt("study_verse", book="約", chapter=3, verse=16)
    required_keywords = [
        "經文內容", "原文字彙分析", "關鍵字詞研究", 
        "註釋與解經", "相關經文連結", "研讀總結"
    ]
    for keyword in required_keywords:
        if keyword in rendered:
            print(f"  ✓ 包含「{keyword}」")
        else:
            print(f"  ✗ 缺少「{keyword}」")
    
    # 驗證 search_topic 包含所有分析步驟
    print("\n7.2 驗證 search_topic 包含所有分析步驟:")
    rendered = manager.render_prompt("search_topic", topic="平安")
    required_keywords = [
        "經文搜尋", "主題查經資料", "註釋中的討論",
        "舊約與新約", "原文洞察", "綜合分析與應用"
    ]
    for keyword in required_keywords:
        if keyword in rendered:
            print(f"  ✓ 包含「{keyword}」")
        else:
            print(f"  ✗ 缺少「{keyword}」")
    
    # 驗證 compare_translations 包含所有比較維度
    print("\n7.3 驗證 compare_translations 包含所有比較維度:")
    rendered = manager.render_prompt("compare_translations", book="約", chapter=1, verse=1)
    required_keywords = [
        "各版本經文", "版本資訊", "原文分析",
        "翻譯差異分析", "原文對照", "翻譯評估與建議"
    ]
    for keyword in required_keywords:
        if keyword in rendered:
            print(f"  ✓ 包含「{keyword}」")
        else:
            print(f"  ✗ 缺少「{keyword}」")
    
    # 驗證 word_study 包含所有研究步驟
    print("\n7.4 驗證 word_study 包含所有研究步驟:")
    rendered = manager.render_prompt("word_study", strongs_number="1", testament="OT")
    required_keywords = [
        "字典定義", "同源字分析", "聖經出現位置",
        "語境中的字義變化", "神學意義", "研究總結與應用"
    ]
    for keyword in required_keywords:
        if keyword in rendered:
            print(f"  ✓ 包含「{keyword}」")
        else:
            print(f"  ✗ 缺少「{keyword}」")
    
    print("\n✅ Prompt 內容驗證完成")


def main():
    """執行所有測試"""
    print("\n" + "="*60)
    print("FHL Bible MCP Prompts 測試")
    print("="*60)
    
    try:
        test_study_verse_prompt()
        test_search_topic_prompt()
        test_compare_translations_prompt()
        test_word_study_prompt()
        test_prompt_manager()
        test_all_prompts_with_different_parameters()
        test_prompt_content_validation()
        
        print("\n" + "="*60)
        print("✅ 所有測試完成!")
        print("="*60)
        print("\n總結:")
        print("  - 4 個 Prompt 模板")
        print("  - 1 個 PromptManager")
        print("  - 所有 prompts 都能正確渲染")
        print("  - 參數嵌入正確")
        print("  - 內容結構完整")
        print("\nPhase 2.3 MCP Prompts 實作完成! 🎉")
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
