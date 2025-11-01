"""
驗證所有15個P1重構prompts
"""
import sys
import importlib
from pathlib import Path

# 所有15個P1 prompts
P1_PROMPTS = [
    # 已完成的前6個
    ("basic.basic_tool_reference", "BasicToolReferencePrompt", {}, 500),
    ("reading.reading_passage", "ReadingPassagePrompt", {"book": "約翰福音", "start_chapter": 3, "start_verse": 1, "end_chapter": 3, "end_verse": 16}, 700),
    ("advanced.advanced_character_study", "AdvancedCharacterStudyPrompt", {"character": "彼得"}, 1000),
    ("basic.basic_uri_demo", "BasicURIDemoPrompt", {}, 500),
    ("basic.basic_help_guide", "BasicHelpGuidePrompt", {}, 500),
    ("reading.reading_chapter", "ReadingChapterPrompt", {"book": "創世記", "chapter": 1}, 700),
    # 新完成的9個
    ("special.special_topical_chain", "SpecialTopicalChainPrompt", {"topic": "信心"}, 900),
    ("advanced.advanced_parallel_gospels", "AdvancedParallelGospelsPrompt", {"event": "登山寶訓"}, 1000),
    ("special.special_sermon_prep", "SpecialSermonPrepPrompt", {"passage": "約翰福音3:16"}, 900),
    ("advanced.advanced_cross_reference", "AdvancedCrossReferencePrompt", {"reference": "約翰福音3:16"}, 1000),
    ("reading.reading_daily", "ReadingDailyPrompt", {"passage": "約翰福音3:16"}, 700),
    ("special.special_bible_trivia", "SpecialBibleTriviaPrompt", {"category": "all"}, 900),
    ("special.special_memory_verse", "SpecialMemoryVersePrompt", {"verse": "約翰福音3:16"}, 900),
    ("special.special_devotional", "SpecialDevotionalPrompt", {"passage": "約翰福音3:16"}, 900),
    ("basic.basic_quick_lookup", "BasicQuickLookupPrompt", {"query": "約翰福音3:16"}, 500),
]

print("=" * 70)
print("驗證所有15個P1重構prompts")
print("=" * 70)

results = []
pass_count = 0
fail_count = 0

for idx, (module_name, class_name, params, max_length) in enumerate(P1_PROMPTS, 1):
    try:
        # 動態導入
        module = importlib.import_module(f"src.fhl_bible_mcp.prompts.{module_name}")
        cls = getattr(module, class_name)
        
        # 實例化並渲染
        prompt = cls()
        rendered = prompt.render(**params)
        length = len(rendered)
        
        # 判斷結果
        status = "✅ PASS" if length <= max_length else "❌ FAIL"
        percentage = f"{length/max_length*100:.1f}%"
        
        if length <= max_length:
            pass_count += 1
        else:
            fail_count += 1
        
        results.append({
            "num": idx,
            "name": class_name,
            "length": length,
            "max": max_length,
            "status": status,
            "percentage": percentage
        })
        
        print(f"{idx:2}. {class_name:35} {length:4}字/{max_length:4}字 ({percentage:6}) {status}")
        
    except Exception as e:
        fail_count += 1
        results.append({
            "num": idx,
            "name": class_name,
            "length": 0,
            "max": max_length,
            "status": "❌ ERROR",
            "percentage": "N/A"
        })
        print(f"{idx:2}. {class_name:35} ERROR: {str(e)}")

print("=" * 70)
print(f"總計: {len(P1_PROMPTS)}個 | 通過: {pass_count}個 ({pass_count/len(P1_PROMPTS)*100:.1f}%) | 失敗: {fail_count}個")
print("=" * 70)

if fail_count == 0:
    print("🎉 所有prompts驗證通過！")
    sys.exit(0)
else:
    print("⚠️ 有prompts未通過驗證")
    sys.exit(1)
