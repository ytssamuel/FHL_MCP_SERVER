"""
Phase 3 Special Prompts 測試

測試特殊用途 prompts (special_*)：
- SpecialSermonPrepPrompt
- SpecialDevotionalPrompt
- SpecialMemoryVersePrompt
- SpecialTopicalChainPrompt
- SpecialBibleTriviaPrompt
"""

import sys
sys.path.insert(0, 'src')

from fhl_bible_mcp.prompts import (
    SpecialSermonPrepPrompt,
    SpecialDevotionalPrompt,
    SpecialMemoryVersePrompt,
    SpecialTopicalChainPrompt,
    SpecialBibleTriviaPrompt,
    PromptManager
)

def test_phase3_prompts():
    """測試 Phase 3 所有 special prompts"""
    print("=" * 80)
    print("Phase 3 Special Prompts 測試")
    print("=" * 80)
    
    # 測試 1: SpecialSermonPrepPrompt
    print("\n測試 1: SpecialSermonPrepPrompt")
    print("-" * 80)
    sermon_prompt = SpecialSermonPrepPrompt(
        passage="John 3:16-21",
        sermon_type="expository",
        audience="general",
        version="unv"
    )
    print(f"✓ 實例化成功")
    
    # 測試不同類型
    print("\n測試不同講道類型：")
    sermon_types = ["expository", "topical", "textual"]
    audiences = ["general", "youth", "new_believers", "mature"]
    
    for sermon_type in sermon_types:
        for audience in audiences[:2]:  # 只測試前兩種聽眾
            prompt = SpecialSermonPrepPrompt(
                passage="Psalm 23",
                sermon_type=sermon_type,
                audience=audience
            )
            rendered = prompt.render()
            print(f"  • {sermon_type} + {audience}: {len(rendered)} 字元")
    
    # 測試 2: SpecialDevotionalPrompt
    print("\n\n測試 2: SpecialDevotionalPrompt")
    print("-" * 80)
    devotional_prompt = SpecialDevotionalPrompt(
        passage="Psalm 23",
        format="personal",
        duration="medium",
        version="unv"
    )
    print(f"✓ 實例化成功")
    
    print("\n測試不同靈修格式：")
    formats = ["personal", "group", "family"]
    durations = ["short", "medium", "long"]
    
    for fmt in formats:
        for dur in durations:
            prompt = SpecialDevotionalPrompt(
                passage="John 15:1-8",
                format=fmt,
                duration=dur
            )
            rendered = prompt.render()
            print(f"  • {fmt} + {dur}: {len(rendered)} 字元")
    
    # 測試 3: SpecialMemoryVersePrompt
    print("\n\n測試 3: SpecialMemoryVersePrompt")
    print("-" * 80)
    memory_prompt = SpecialMemoryVersePrompt(
        topic="love",
        difficulty="medium",
        version="unv"
    )
    print(f"✓ 實例化成功")
    
    print("\n測試不同難度：")
    difficulties = ["easy", "medium", "hard"]
    
    # 測試指定主題
    for diff in difficulties:
        prompt = SpecialMemoryVersePrompt(
            topic="faith",
            difficulty=diff
        )
        rendered = prompt.render()
        print(f"  • topic=faith, difficulty={diff}: {len(rendered)} 字元")
    
    # 測試指定書卷
    prompt = SpecialMemoryVersePrompt(
        book="Psalm",
        difficulty="easy"
    )
    rendered = prompt.render()
    print(f"  • book=Psalm: {len(rendered)} 字元")
    
    # 測試無指定（推薦經典）
    prompt = SpecialMemoryVersePrompt(
        difficulty="medium"
    )
    rendered = prompt.render()
    print(f"  • 無指定（推薦經典）: {len(rendered)} 字元")
    
    # 測試 4: SpecialTopicalChainPrompt
    print("\n\n測試 4: SpecialTopicalChainPrompt")
    print("-" * 80)
    topical_prompt = SpecialTopicalChainPrompt(
        topic="grace",
        testament="both",
        depth="detailed",
        version="unv"
    )
    print(f"✓ 實例化成功")
    
    print("\n測試不同約別和深度：")
    testaments = ["OT", "NT", "both"]
    depths = ["overview", "detailed", "exhaustive"]
    
    for test in testaments:
        for depth in depths[:2]:  # 只測試前兩種深度
            prompt = SpecialTopicalChainPrompt(
                topic="love",
                testament=test,
                depth=depth
            )
            rendered = prompt.render()
            print(f"  • testament={test}, depth={depth}: {len(rendered)} 字元")
    
    # 測試 5: SpecialBibleTriviaPrompt
    print("\n\n測試 5: SpecialBibleTriviaPrompt")
    print("-" * 80)
    trivia_prompt = SpecialBibleTriviaPrompt(
        category="general",
        difficulty="medium",
        count=10,
        testament="both"
    )
    print(f"✓ 實例化成功")
    
    print("\n測試不同類別和難度：")
    categories = ["general", "people", "places", "events", "teachings", "books"]
    difficulties = ["easy", "medium", "hard"]
    
    for cat in categories:
        for diff in difficulties:
            prompt = SpecialBibleTriviaPrompt(
                category=cat,
                difficulty=diff,
                count=10
            )
            rendered = prompt.render()
            print(f"  • category={cat}, difficulty={diff}: {len(rendered)} 字元")
    
    # 測試不同題數
    print("\n測試不同題數：")
    for count in [5, 10, 20]:
        prompt = SpecialBibleTriviaPrompt(
            category="general",
            difficulty="medium",
            count=count
        )
        rendered = prompt.render()
        print(f"  • count={count}: {len(rendered)} 字元")
    
    print("\n" + "=" * 80)
    print("✅ 所有 Phase 3 prompts 測試通過！")
    print("=" * 80)


def test_prompt_manager():
    """測試 PromptManager 是否正確註冊所有 prompts"""
    print("\n\n" + "=" * 80)
    print("測試 4: PromptManager 註冊")
    print("=" * 80)
    
    manager = PromptManager()
    prompts = manager.get_prompt_names()
    
    print(f"\n✓ 總共註冊 {len(prompts)} 個 prompts")
    print(f"\n所有 prompts 列表：")
    for i, name in enumerate(sorted(prompts), 1):
        print(f"  {i:2d}. {name}")
    
    # 檢查 Phase 3 prompts 是否都存在
    print("\nPhase 3 Prompts 檢查：")
    phase3_prompts = [
        "special_sermon_prep",
        "special_devotional",
        "special_memory_verse",
        "special_topical_chain",
        "special_bible_trivia"
    ]
    
    all_found = True
    for name in phase3_prompts:
        found = manager.has_prompt(name)
        status = "✓" if found else "✗"
        print(f"  {status} {name}")
        if not found:
            all_found = False
    
    if not all_found:
        print("\n❌ 有些 Phase 3 prompts 沒有被正確註冊！")
        return False
    
    # 測試通過 Manager 渲染
    print("\n測試通過 Manager 渲染：")
    
    # 測試 special_sermon_prep
    rendered = manager.render_prompt(
        "special_sermon_prep",
        passage="John 3:16",
        sermon_type="expository",
        audience="general"
    )
    print(f"  ✓ special_sermon_prep 渲染成功（{len(rendered)} 字元）")
    
    # 測試 special_devotional
    rendered = manager.render_prompt(
        "special_devotional",
        passage="Psalm 23",
        format="personal",
        duration="medium"
    )
    print(f"  ✓ special_devotional 渲染成功（{len(rendered)} 字元）")
    
    # 測試 special_memory_verse
    rendered = manager.render_prompt(
        "special_memory_verse",
        topic="love",
        difficulty="medium"
    )
    print(f"  ✓ special_memory_verse 渲染成功（{len(rendered)} 字元）")
    
    # 測試 special_topical_chain
    rendered = manager.render_prompt(
        "special_topical_chain",
        topic="grace",
        testament="both",
        depth="detailed"
    )
    print(f"  ✓ special_topical_chain 渲染成功（{len(rendered)} 字元）")
    
    # 測試 special_bible_trivia
    rendered = manager.render_prompt(
        "special_bible_trivia",
        category="general",
        difficulty="medium",
        count=10
    )
    print(f"  ✓ special_bible_trivia 渲染成功（{len(rendered)} 字元）")
    
    # 驗證總數
    print(f"\n✓ Prompt 總數正確：{len(prompts)} 個")
    
    # 按類別統計
    print("\n分類統計：")
    basic_count = len([p for p in prompts if p.startswith("basic_")])
    reading_count = len([p for p in prompts if p.startswith("reading_")])
    study_count = len([p for p in prompts if p.startswith("study_")])
    special_count = len([p for p in prompts if p.startswith("special_")])
    
    print(f"  • 基礎類 (basic_*): {basic_count} 個")
    print(f"  • 讀經類 (reading_*): {reading_count} 個")
    print(f"  • 研經類 (study_*): {study_count} 個")
    print(f"  • 特殊類 (special_*): {special_count} 個")
    print(f"  • 總計: {basic_count + reading_count + study_count + special_count} 個")
    
    # 驗證預期數量
    expected = 4 + 3 + 4 + 5  # basic + reading + study + special
    if len(prompts) == expected:
        print(f"\n✅ 數量正確：{len(prompts)} = 4 (basic) + 3 (reading) + 4 (study) + 5 (special)")
    else:
        print(f"\n❌ 數量不符：預期 {expected}，實際 {len(prompts)}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ PromptManager 測試通過！")
    print("=" * 80)
    return True


def test_backward_compatibility():
    """測試向後兼容性"""
    print("\n\n" + "=" * 80)
    print("測試 5: 向後兼容性")
    print("=" * 80)
    
    try:
        # Phase 3 的 prompts 沒有舊名稱，直接測試從 templates 導入
        from fhl_bible_mcp.prompts.templates import (
            SpecialSermonPrepPrompt,
            SpecialDevotionalPrompt,
            SpecialMemoryVersePrompt,
            SpecialTopicalChainPrompt,
            SpecialBibleTriviaPrompt
        )
        
        print("\n✓ 從 templates.py 導入成功（向後兼容）")
        
        # 測試實例化
        sermon = SpecialSermonPrepPrompt(passage="John 3:16")
        devotional = SpecialDevotionalPrompt(passage="Psalm 23")
        memory = SpecialMemoryVersePrompt(topic="love")
        topical = SpecialTopicalChainPrompt(topic="grace")
        trivia = SpecialBibleTriviaPrompt()
        
        print("✓ 所有 Phase 3 prompts 都可以從 templates.py 導入並實例化")
        
        print("\n" + "=" * 80)
        print("✅ 向後兼容性測試通過！")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ 向後兼容性測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主測試函數"""
    print("\n" + "=" * 80)
    print(" Phase 3 Special Prompts 完整測試套件")
    print("=" * 80)
    
    all_passed = True
    
    try:
        # 測試 1: Phase 3 prompts
        test_phase3_prompts()
    except Exception as e:
        print(f"\n❌ Phase 3 prompts 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        # 測試 2: PromptManager
        if not test_prompt_manager():
            all_passed = False
    except Exception as e:
        print(f"\n❌ PromptManager 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        # 測試 3: 向後兼容性
        if not test_backward_compatibility():
            all_passed = False
    except Exception as e:
        print(f"\n❌ 向後兼容性測試失敗：{e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    # 總結
    print("\n\n" + "=" * 80)
    if all_passed:
        print("🎉 Phase 3 完成！所有測試通過！")
        print("=" * 80)
        print("\n已完成的 Prompts（新命名規則）：")
        print("\n【Phase 1: Basic - 基礎類】✅")
        print("  1. basic_help_guide - 使用指南")
        print("  2. basic_uri_demo - URI 使用示範")
        print("  3. basic_quick_lookup - 快速查經")
        print("  4. basic_tool_reference - 工具參考")
        print("\n【Phase 2: Reading - 讀經類】✅")
        print("  5. reading_daily - 每日讀經")
        print("  6. reading_chapter - 整章讀經")
        print("  7. reading_passage - 段落讀經")
        print("\n【原有: Study - 研經類】✅")
        print("  8. study_verse_deep - 深入研讀經文")
        print("  9. study_topic_deep - 主題研究")
        print(" 10. study_translation_compare - 版本比較")
        print(" 11. study_word_original - 原文字詞研究")
        print("\n【Phase 3: Special - 特殊用途】✅ NEW!")
        print(" 12. special_sermon_prep - 講道準備")
        print(" 13. special_devotional - 靈修材料")
        print(" 14. special_memory_verse - 背經輔助")
        print(" 15. special_topical_chain - 主題串連")
        print(" 16. special_bible_trivia - 聖經問答")
        print("\n總計：16 個 Prompts 全部就緒！")
        print("\n下一步：Phase 4 - 進階功能系列（cross_reference, parallel_gospels, character_study）")
        print("=" * 80)
        return 0
    else:
        print("❌ 部分測試失敗，請檢查錯誤訊息")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit(main())
