"""
Phase 4 Advanced Prompts 測試套件

測試 Phase 4 進階功能 prompts：
- advanced_cross_reference: 交叉引用分析
- advanced_parallel_gospels: 符類福音對照
- advanced_character_study: 聖經人物研究
"""

import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from fhl_bible_mcp.prompts import (
    PromptManager,
    AdvancedCrossReferencePrompt,
    AdvancedParallelGospelsPrompt,
    AdvancedCharacterStudyPrompt
)


def test_phase4_prompts():
    """測試 Phase 4 的 3 個 advanced prompts"""
    print("\n" + "=" * 80)
    print("Phase 4 Advanced Prompts 測試")
    print("=" * 80)
    
    # 測試 1: AdvancedCrossReferencePrompt
    print("\n測試 1: AdvancedCrossReferencePrompt")
    print("-" * 80)
    
    # 測試默認參數
    prompt1 = AdvancedCrossReferencePrompt()
    print("✓ 實例化成功（默認參數）")
    
    # 測試不同深度
    print("\n測試不同深度和經文：")
    test_cases_cross_ref = [
        {"reference": "John 3:16", "depth": 1, "max_results": 10},
        {"reference": "Romans 8:28", "depth": 2, "max_results": 20},
        {"reference": "Psalm 23:1", "depth": 3, "max_results": 30},
        {"reference": "Matthew 5:3", "depth": 2, "max_results": 15},
    ]
    
    for params in test_cases_cross_ref:
        prompt = AdvancedCrossReferencePrompt(**params)
        rendered = prompt.render()
        print(f"  • reference={params['reference']}, depth={params['depth']}, max_results={params['max_results']}: {len(rendered)} 字元")
        
        # 驗證內容包含關鍵元素
        assert params['reference'] in rendered, f"經文位置 {params['reference']} 未在輸出中"
        assert f"第 {params['depth']} 層" in rendered, f"深度資訊未在輸出中"
        assert "交叉引用分析" in rendered, "標題未在輸出中"
        
        # 驗證深度相關內容
        if params['depth'] >= 2:
            assert "第二層" in rendered or "間接引用" in rendered, "第二層內容缺失"
        if params['depth'] >= 3:
            assert "第三層" in rendered or "主題連結" in rendered, "第三層內容缺失"
    
    print("\n✅ AdvancedCrossReferencePrompt 測試通過")
    
    # 測試 2: AdvancedParallelGospelsPrompt
    print("\n" + "=" * 80)
    print("測試 2: AdvancedParallelGospelsPrompt")
    print("-" * 80)
    
    # 測試默認參數
    prompt2 = AdvancedParallelGospelsPrompt()
    print("✓ 實例化成功（默認參數）")
    
    # 測試不同事件和配置
    print("\n測試不同事件和配置：")
    test_cases_gospels = [
        {"event": "Jesus' Baptism", "include_john": True},
        {"event": "Feeding 5000", "include_john": True},
        {"event": "Transfiguration", "include_john": False},
        {"event": "Sermon on the Mount", "passage": "Matthew 5-7", "include_john": False},
        {"event": "Last Supper", "include_john": True},
    ]
    
    for params in test_cases_gospels:
        prompt = AdvancedParallelGospelsPrompt(**params)
        rendered = prompt.render()
        print(f"  • event='{params['event']}', include_john={params.get('include_john', True)}: {len(rendered)} 字元")
        
        # 驗證內容包含關鍵元素
        assert params['event'] in rendered, f"事件名稱 {params['event']} 未在輸出中"
        assert "符類福音對照" in rendered, "標題未在輸出中"
        assert "馬太福音" in rendered, "馬太福音未提及"
        assert "馬可福音" in rendered, "馬可福音未提及"
        assert "路加福音" in rendered, "路加福音未提及"
        
        # 驗證約翰福音包含邏輯
        if params.get('include_john', True):
            assert "約翰福音" in rendered, "應包含約翰福音但未找到"
        else:
            # 可能仍會提到約翰福音（在說明中），但不會詳細對照
            pass
    
    print("\n✅ AdvancedParallelGospelsPrompt 測試通過")
    
    # 測試 3: AdvancedCharacterStudyPrompt
    print("\n" + "=" * 80)
    print("測試 3: AdvancedCharacterStudyPrompt")
    print("-" * 80)
    
    # 測試默認參數
    prompt3 = AdvancedCharacterStudyPrompt()
    print("✓ 實例化成功（默認參數）")
    
    # 測試不同人物和焦點
    print("\n測試不同人物和焦點：")
    test_cases_character = [
        {"character": "Peter", "focus": "all", "testament": "NT"},
        {"character": "David", "focus": "biography", "testament": "OT"},
        {"character": "Paul", "focus": "character", "testament": "NT"},
        {"character": "Moses", "focus": "lessons", "testament": "OT"},
        {"character": "Abraham", "focus": "all", "testament": "both"},
    ]
    
    for params in test_cases_character:
        prompt = AdvancedCharacterStudyPrompt(**params)
        rendered = prompt.render()
        print(f"  • character='{params['character']}', focus={params['focus']}, testament={params['testament']}: {len(rendered)} 字元")
        
        # 驗證內容包含關鍵元素
        assert params['character'] in rendered, f"人物名稱 {params['character']} 未在輸出中"
        assert "聖經人物研究" in rendered, "標題未在輸出中"
        assert "基本資料" in rendered, "基本資料部分缺失"
        
        # 驗證焦點相關內容
        if params['focus'] in ['all', 'biography']:
            assert "生平事蹟" in rendered or "時間線" in rendered, "生平事蹟部分缺失"
        else:
            assert "焦點不包含" in rendered or "調整 focus" in rendered, "應該顯示焦點不包含提示"
        
        if params['focus'] in ['all', 'character']:
            assert "性格特質" in rendered or "性格分析" in rendered, "性格分析部分缺失"
        
        if params['focus'] in ['all', 'lessons']:
            assert "屬靈教訓" in rendered or "屬靈功課" in rendered, "屬靈教訓部分缺失"
    
    print("\n✅ AdvancedCharacterStudyPrompt 測試通過")
    
    print("\n" + "=" * 80)
    print("✅ 所有 Phase 4 prompts 測試通過！")
    print("=" * 80)


def test_prompt_manager():
    """測試 PromptManager 是否正確註冊了所有 prompts"""
    print("\n" + "=" * 80)
    print("測試 4: PromptManager 註冊")
    print("=" * 80)
    
    manager = PromptManager()
    
    # 檢查總數
    all_prompts = manager.list_prompts()
    print(f"\n✓ 總共註冊 {len(all_prompts)} 個 prompts")
    
    # 列出所有 prompts
    print("\n所有 prompts 列表：")
    for i, prompt_info in enumerate(all_prompts, 1):
        print(f"  {i:2d}. {prompt_info['name']}")
    
    # 檢查 Phase 4 prompts 是否存在
    print("\nPhase 4 Prompts 檢查：")
    phase4_prompts = [
        "advanced_cross_reference",
        "advanced_parallel_gospels",
        "advanced_character_study"
    ]
    
    for prompt_name in phase4_prompts:
        prompt = manager.get_prompt(prompt_name)
        assert prompt is not None, f"Prompt {prompt_name} 未註冊"
        print(f"  ✓ {prompt_name}")
    
    # 測試通過 Manager 渲染
    print("\n測試通過 Manager 渲染：")
    
    # 測試 advanced_cross_reference
    prompt = manager.get_prompt("advanced_cross_reference")
    rendered = prompt.render(reference="John 3:16", depth=2)
    print(f"  ✓ advanced_cross_reference 渲染成功（{len(rendered)} 字元）")
    
    # 測試 advanced_parallel_gospels
    prompt = manager.get_prompt("advanced_parallel_gospels")
    rendered = prompt.render(event="Last Supper")
    print(f"  ✓ advanced_parallel_gospels 渲染成功（{len(rendered)} 字元）")
    
    # 測試 advanced_character_study
    prompt = manager.get_prompt("advanced_character_study")
    rendered = prompt.render(character="Peter", focus="lessons")
    print(f"  ✓ advanced_character_study 渲染成功（{len(rendered)} 字元）")
    
    # 驗證總數
    expected_count = 19  # 4 basic + 3 reading + 4 study + 5 special + 3 advanced
    assert len(all_prompts) == expected_count, f"Prompt 總數錯誤：期望 {expected_count}，實際 {len(all_prompts)}"
    print(f"\n✓ Prompt 總數正確：{expected_count} 個")
    
    # 分類統計
    print("\n分類統計：")
    basic_count = sum(1 for p in all_prompts if p['name'].startswith('basic_'))
    reading_count = sum(1 for p in all_prompts if p['name'].startswith('reading_'))
    study_count = sum(1 for p in all_prompts if p['name'].startswith('study_'))
    special_count = sum(1 for p in all_prompts if p['name'].startswith('special_'))
    advanced_count = sum(1 for p in all_prompts if p['name'].startswith('advanced_'))
    
    print(f"  • 基礎類 (basic_*): {basic_count} 個")
    print(f"  • 讀經類 (reading_*): {reading_count} 個")
    print(f"  • 研經類 (study_*): {study_count} 個")
    print(f"  • 特殊類 (special_*): {special_count} 個")
    print(f"  • 進階類 (advanced_*): {advanced_count} 個")
    print(f"  • 總計: {len(all_prompts)} 個")
    
    # 驗證數量
    assert basic_count == 4, f"基礎類數量錯誤：期望 4，實際 {basic_count}"
    assert reading_count == 3, f"讀經類數量錯誤：期望 3，實際 {reading_count}"
    assert study_count == 4, f"研經類數量錯誤：期望 4，實際 {study_count}"
    assert special_count == 5, f"特殊類數量錯誤：期望 5，實際 {special_count}"
    assert advanced_count == 3, f"進階類數量錯誤：期望 3，實際 {advanced_count}"
    
    print(f"\n✅ 數量正確：{expected_count} = {basic_count} (basic) + {reading_count} (reading) + {study_count} (study) + {special_count} (special) + {advanced_count} (advanced)")
    
    print("\n" + "=" * 80)
    print("✅ PromptManager 測試通過！")
    print("=" * 80)


def test_backward_compatibility():
    """測試向後兼容性"""
    print("\n" + "=" * 80)
    print("測試 5: 向後兼容性")
    print("=" * 80)
    
    # 測試從 templates.py 導入
    try:
        from fhl_bible_mcp.prompts.templates import (
            AdvancedCrossReferencePrompt,
            AdvancedParallelGospelsPrompt,
            AdvancedCharacterStudyPrompt
        )
        print("\n✓ 從 templates.py 導入成功（向後兼容）")
        
        # 測試實例化
        prompt1 = AdvancedCrossReferencePrompt()
        prompt2 = AdvancedParallelGospelsPrompt()
        prompt3 = AdvancedCharacterStudyPrompt()
        print("✓ 所有 Phase 4 prompts 都可以從 templates.py 導入並實例化")
        
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        raise
    
    print("\n" + "=" * 80)
    print("✅ 向後兼容性測試通過！")
    print("=" * 80)


def main():
    """主測試函數"""
    print("\n" + "=" * 80)
    print(" " * 20 + "Phase 4 Advanced Prompts 完整測試套件")
    print("=" * 80)
    
    try:
        # 執行所有測試
        test_phase4_prompts()
        test_prompt_manager()
        test_backward_compatibility()
        
        # 最終總結
        print("\n" + "=" * 80)
        print("🎉 Phase 4 完成！所有測試通過！")
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
        
        print("\n【Phase 3: Special - 特殊用途】✅")
        print(" 12. special_sermon_prep - 講道準備")
        print(" 13. special_devotional - 靈修材料")
        print(" 14. special_memory_verse - 背經輔助")
        print(" 15. special_topical_chain - 主題串連")
        print(" 16. special_bible_trivia - 聖經問答")
        
        print("\n【Phase 4: Advanced - 進階功能】✅ NEW!")
        print(" 17. advanced_cross_reference - 交叉引用分析")
        print(" 18. advanced_parallel_gospels - 符類福音對照")
        print(" 19. advanced_character_study - 聖經人物研究")
        
        print("\n總計：19 個 Prompts 全部就緒！")
        print("完成度：19/15 = 126.7% 🎊")
        
        print("\n" + "=" * 80)
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ 測試失敗：{e}")
        return 1
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
