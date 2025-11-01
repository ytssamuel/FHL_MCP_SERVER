"""
驗證所有19個prompts（包含P1完成的15個 + P2/P3的4個）
"""
import sys
import importlib
from pathlib import Path

# 所有19個 prompts
ALL_PROMPTS = [
    # P1 完成的 15 個
    ("basic.basic_tool_reference", "BasicToolReferencePrompt", {}, 500),
    ("reading.reading_passage", "ReadingPassagePrompt", {"book": "約翰福音", "start_chapter": 3, "start_verse": 1, "end_chapter": 3, "end_verse": 16}, 700),
    ("advanced.advanced_character_study", "AdvancedCharacterStudyPrompt", {"character": "彼得"}, 1000),
    ("basic.basic_uri_demo", "BasicURIDemoPrompt", {}, 500),
    ("basic.basic_help_guide", "BasicHelpGuidePrompt", {}, 500),
    ("reading.reading_chapter", "ReadingChapterPrompt", {"book": "創世記", "chapter": 1}, 700),
    ("special.special_topical_chain", "SpecialTopicalChainPrompt", {"topic": "信心"}, 900),
    ("advanced.advanced_parallel_gospels", "AdvancedParallelGospelsPrompt", {"event": "登山寶訓"}, 1000),
    ("special.special_sermon_prep", "SpecialSermonPrepPrompt", {"passage": "約翰福音3:16"}, 900),
    ("advanced.advanced_cross_reference", "AdvancedCrossReferencePrompt", {"reference": "約翰福音3:16"}, 1000),
    ("reading.reading_daily", "ReadingDailyPrompt", {"passage": "約翰福音3:16"}, 700),
    ("special.special_bible_trivia", "SpecialBibleTriviaPrompt", {"category": "all"}, 900),
    ("special.special_memory_verse", "SpecialMemoryVersePrompt", {"verse": "約翰福音3:16"}, 900),
    ("special.special_devotional", "SpecialDevotionalPrompt", {"passage": "約翰福音3:16"}, 900),
    ("basic.basic_quick_lookup", "BasicQuickLookupPrompt", {"query": "約翰福音3:16"}, 500),
    
    # P2/P3 完成的 4 個
    ("study.study_word_original", "StudyWordOriginalPrompt", {"strongs_number": "G26", "testament": "NT"}, 800),
    ("study.study_verse_deep", "StudyVerseDeepPrompt", {"book": "約翰福音", "chapter": 3, "verse": 16}, 800),
    ("study.study_topic_deep", "StudyTopicDeepPrompt", {"topic": "愛"}, 800),
    ("study.study_translation_compare", "StudyTranslationComparePrompt", {"book": "約翰福音", "chapter": 3, "verse": 16}, 800),
]

print("=" * 80)
print("🔍 驗證所有19個prompts")
print("=" * 80)

results = []
pass_count = 0
fail_count = 0
p1_pass = 0
p1_fail = 0
p2p3_pass = 0
p2p3_fail = 0

for idx, (module_name, class_name, params, max_length) in enumerate(ALL_PROMPTS, 1):
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
            if idx <= 15:
                p1_pass += 1
            else:
                p2p3_pass += 1
        else:
            fail_count += 1
            if idx <= 15:
                p1_fail += 1
            else:
                p2p3_fail += 1
        
        results.append({
            "num": idx,
            "name": class_name,
            "length": length,
            "max": max_length,
            "status": status,
            "percentage": percentage
        })
        
        category = "P1" if idx <= 15 else "P2/P3"
        print(f"{idx:2}. [{category:5}] {class_name:35} {length:4}字/{max_length:4}字 ({percentage:6}) {status}")
        
    except Exception as e:
        fail_count += 1
        if idx <= 15:
            p1_fail += 1
        else:
            p2p3_fail += 1
        category = "P1" if idx <= 15 else "P2/P3"
        results.append({
            "num": idx,
            "name": class_name,
            "length": 0,
            "max": max_length,
            "status": "❌ ERROR",
            "percentage": "N/A"
        })
        print(f"{idx:2}. [{category:5}] {class_name:35} ERROR: {str(e)}")

print("=" * 80)
print(f"📊 總計: {len(ALL_PROMPTS)}個")
print(f"   ✅ 通過: {pass_count}個 ({pass_count/len(ALL_PROMPTS)*100:.1f}%)")
print(f"   ❌ 失敗: {fail_count}個 ({fail_count/len(ALL_PROMPTS)*100:.1f}%)")
print("-" * 80)
print(f"   P1 (前15個): 通過 {p1_pass}/15 | 失敗 {p1_fail}/15")
print(f"   P2/P3 (後4個): 通過 {p2p3_pass}/4 | 失敗 {p2p3_fail}/4")
print("=" * 80)

if fail_count == 0:
    print("🎉 所有prompts驗證通過！")
    sys.exit(0)
else:
    print(f"⚠️  有 {fail_count} 個prompts未通過驗證")
    sys.exit(1)
