"""
測試 Phase 2 新增的 Reading Prompts

測試 reading_daily, reading_chapter, reading_passage prompts
"""

import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_phase2_prompts():
    """測試 Phase 2 的三個新 prompts"""
    print("=" * 70)
    print("測試 Phase 2 新增的 Reading Prompts")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import (
            ReadingDailyPrompt,
            ReadingChapterPrompt,
            ReadingPassagePrompt,
            PromptManager
        )
        print("✓ 成功導入 Phase 2 prompts")
    except ImportError as e:
        print(f"✗ 導入失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("測試 1：ReadingDailyPrompt")
    print("=" * 70)
    
    try:
        daily_reading = ReadingDailyPrompt()
        print(f"✓ 實例化成功")
        print(f"  名稱：{daily_reading.name}")
        print(f"  描述：{daily_reading.description}")
        print(f"  參數數量：{len(daily_reading.arguments)}")
        
        # 測試不同的讀經計劃
        plans = [
            ("verse_of_day", None, None),
            ("sequential", "約翰福音", 1),
            ("random", None, None),
            ("topic", "愛", None)
        ]
        
        print("\n  測試不同讀經計劃：")
        for plan, book, chapter in plans:
            kwargs = {"reading_plan": plan, "version": "unv"}
            if book:
                kwargs["book"] = book
            if chapter:
                kwargs["chapter"] = chapter
            
            text = daily_reading.render(**kwargs)
            print(f"    • {plan}: {len(text)} 字元")
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("測試 2：ReadingChapterPrompt")
    print("=" * 70)
    
    try:
        chapter_reading = ReadingChapterPrompt()
        print(f"✓ 實例化成功")
        print(f"  名稱：{chapter_reading.name}")
        print(f"  描述：{chapter_reading.description}")
        print(f"  參數數量：{len(chapter_reading.arguments)}")
        
        # 測試不同章節
        chapters = [
            ("約翰福音", 3, False),
            ("詩篇", 23, True),
            ("羅馬書", 8, False)
        ]
        
        print("\n  測試不同章節：")
        for book, chapter, include_audio in chapters:
            text = chapter_reading.render(
                book=book,
                chapter=chapter,
                version="unv",
                include_audio=include_audio
            )
            audio_tag = " (含音訊)" if include_audio else ""
            print(f"    • {book} {chapter}{audio_tag}: {len(text)} 字元")
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("測試 3：ReadingPassagePrompt")
    print("=" * 70)
    
    try:
        passage_reading = ReadingPassagePrompt()
        print(f"✓ 實例化成功")
        print(f"  名稱：{passage_reading.name}")
        print(f"  描述：{passage_reading.description}")
        print(f"  參數數量：{len(passage_reading.arguments)}")
        
        # 測試不同段落
        passages = [
            ("約翰福音", 3, 16, 3, 21),  # 同章內
            ("創世記", 1, 1, 2, 3),      # 跨章
            ("詩篇", 23, 1, 23, 6),      # 同章內
            ("馬太福音", 5, 1, 7, 29)    # 跨多章
        ]
        
        print("\n  測試不同段落：")
        for book, sc, sv, ec, ev in passages:
            text = passage_reading.render(
                book=book,
                start_chapter=sc,
                start_verse=sv,
                end_chapter=ec,
                end_verse=ev,
                version="unv"
            )
            ref = f"{sc}:{sv}-{ec}:{ev}" if sc != ec else f"{sc}:{sv}-{ev}"
            print(f"    • {book} {ref}: {len(text)} 字元")
        
    except Exception as e:
        print(f"✗ 測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_prompt_manager():
    """測試 PromptManager 註冊"""
    print("\n" + "=" * 70)
    print("測試 4：PromptManager 註冊")
    print("=" * 70)
    
    try:
        from fhl_bible_mcp.prompts import PromptManager
        
        manager = PromptManager()
        prompts = manager.list_prompts()
        
        print(f"✓ 總共註冊 {len(prompts)} 個 prompts")
        
        # 檢查 Phase 2 prompts
        phase2_prompts = ["reading_daily", "reading_chapter", "reading_passage"]
        print("\n  Phase 2 Prompts 檢查：")
        for name in phase2_prompts:
            if manager.has_prompt(name):
                prompt = manager.get_prompt(name)
                print(f"    ✓ {name}: {prompt.description[:50]}...")
            else:
                print(f"    ✗ {name}: 未找到")
                return False
        
        # 測試渲染
        print("\n  測試通過 Manager 渲染：")
        
        # 測試 reading_daily
        daily_text = manager.render_prompt(
            "reading_daily",
            reading_plan="verse_of_day",
            version="unv"
        )
        if daily_text:
            print(f"    ✓ reading_daily 渲染成功（{len(daily_text)} 字元）")
        else:
            print(f"    ✗ reading_daily 渲染失敗")
            return False
        
        # 測試 reading_chapter
        chapter_text = manager.render_prompt(
            "reading_chapter",
            book="約翰福音",
            chapter=3,
            version="unv"
        )
        if chapter_text:
            print(f"    ✓ reading_chapter 渲染成功（{len(chapter_text)} 字元）")
        else:
            print(f"    ✗ reading_chapter 渲染失敗")
            return False
        
        # 測試 reading_passage
        passage_text = manager.render_prompt(
            "reading_passage",
            book="約翰福音",
            start_chapter=3,
            start_verse=16,
            end_chapter=3,
            end_verse=21,
            version="unv"
        )
        if passage_text:
            print(f"    ✓ reading_passage 渲染成功（{len(passage_text)} 字元）")
        else:
            print(f"    ✗ reading_passage 渲染失敗")
            return False
        
        # 檢查總數應該是 11 個（4 basic + 3 reading + 4 study）
        if len(prompts) == 11:
            print(f"\n  ✓ Prompt 總數正確：11 個")
            print("\n  分類統計：")
            
            basic_count = sum(1 for p in prompts if p['name'].startswith('basic_'))
            reading_count = sum(1 for p in prompts if p['name'].startswith('reading_'))
            study_count = sum(1 for p in prompts if p['name'].startswith('study_'))
            
            print(f"    • 基礎類 (basic_*): {basic_count} 個")
            print(f"    • 讀經類 (reading_*): {reading_count} 個")
            print(f"    • 研經類 (study_*): {study_count} 個")
        else:
            print(f"\n  ✗ Prompt 總數錯誤：預期 11 個，實際 {len(prompts)} 個")
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
    print("測試 5：向後兼容性")
    print("=" * 70)
    
    try:
        # 從 templates 導入 Phase 2 prompts
        from fhl_bible_mcp.prompts.templates import (
            ReadingDailyPrompt,
            ReadingChapterPrompt,
            ReadingPassagePrompt
        )
        print("✓ 從 templates.py 導入成功（向後兼容）")
        
        # 測試實例化
        daily = ReadingDailyPrompt()
        chapter = ReadingChapterPrompt()
        passage = ReadingPassagePrompt()
        print("✓ 實例化成功")
        
        # 測試渲染
        text = daily.render(reading_plan="verse_of_day")
        if len(text) > 0:
            print("✓ 渲染成功")
        
        return True
    except Exception as e:
        print(f"✗ 向後兼容性測試失敗：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """執行所有測試"""
    print("\n" + "═" * 70)
    print(" Phase 2 Reading Prompts 測試")
    print("═" * 70 + "\n")
    
    results = []
    
    # 測試 Phase 2 prompts
    results.append(("Phase 2 Prompts", test_phase2_prompts()))
    
    # 測試 PromptManager
    results.append(("PromptManager 註冊", test_prompt_manager()))
    
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
        print("\n🎉 Phase 2 完成！所有測試通過！")
        print("\n已完成的 Prompts（新命名規則）：")
        print("\n📖 基礎類 (basic_*)：")
        print("  ✅ 1. basic_help_guide - 基礎｜使用指南")
        print("  ✅ 2. basic_uri_demo - 基礎｜URI 使用示範")
        print("  ✅ 3. basic_quick_lookup - 基礎｜快速查經")
        print("  ✅ 4. basic_tool_reference - 基礎｜工具參考")
        print("\n📚 讀經類 (reading_*)：")
        print("  ✅ 5. reading_daily - 讀經｜每日讀經計劃")
        print("  ✅ 6. reading_chapter - 讀經｜整章讀經輔助")
        print("  ✅ 7. reading_passage - 讀經｜段落讀經分析")
        print("\n🔍 研經類 (study_*)：")
        print("  ✅ 8. study_verse_deep - 研經｜深入研讀經文")
        print("  ✅ 9. study_topic_deep - 研經｜主題研究")
        print("  ✅ 10. study_translation_compare - 研經｜版本比較")
        print("  ✅ 11. study_word_original - 研經｜原文字詞研究")
        print("\n總計：11 個 Prompts 全部就緒！")
        print("\n下一步：Phase 3 - 特殊用途系列（sermon_prep, devotional 等）")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 個測試失敗")
        return 1


if __name__ == "__main__":
    exit(main())

