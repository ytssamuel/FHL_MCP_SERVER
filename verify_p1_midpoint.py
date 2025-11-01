"""驗證所有已重構的 P1 prompts"""

import sys
sys.path.insert(0, '.')

# 測試已完成的6個 prompts
prompts_to_test = [
    ("basic_tool_reference", "src.fhl_bible_mcp.prompts.basic.basic_tool_reference", "BasicToolReferencePrompt", 500),
    ("reading_passage", "src.fhl_bible_mcp.prompts.reading.reading_passage", "ReadingPassagePrompt", 700),
    ("advanced_character_study", "src.fhl_bible_mcp.prompts.advanced.advanced_character_study", "AdvancedCharacterStudyPrompt", 1000),
    ("basic_uri_demo", "src.fhl_bible_mcp.prompts.basic.basic_uri_demo", "BasicURIDemoPrompt", 500),
    ("basic_help_guide", "src.fhl_bible_mcp.prompts.basic.basic_help_guide", "BasicHelpGuidePrompt", 500),
    ("reading_chapter", "src.fhl_bible_mcp.prompts.reading.reading_chapter", "ReadingChapterPrompt", 700),
]

print("=" * 80)
print("P1 重構驗證報告 - 中期檢查")
print("=" * 80)
print()

results = []
total_pass = 0
total_fail = 0

for name, module_path, class_name, target in prompts_to_test:
    try:
        # 動態導入
        module = __import__(module_path, fromlist=[class_name])
        PromptClass = getattr(module, class_name)
        
        # 實例化並渲染
        prompt = PromptClass()
        result = prompt.render()
        length = len(result)
        
        # 判斷是否達標
        is_pass = length <= target
        if is_pass:
            total_pass += 1
            status = "✅ PASS"
        else:
            total_fail += 1
            status = f"❌ FAIL (+{((length - target) / target * 100):.1f}%)"
        
        percentage = (length / target * 100)
        
        results.append({
            "name": name,
            "length": length,
            "target": target,
            "status": status,
            "percentage": percentage
        })
        
        print(f"[{status}] {name}")
        print(f"  長度: {length} 字 / {target} 字 ({percentage:.1f}%)")
        print()
        
    except Exception as e:
        print(f"[❌ ERROR] {name}")
        print(f"  錯誤: {str(e)}")
        print()
        total_fail += 1
        results.append({
            "name": name,
            "length": 0,
            "target": target,
            "status": f"❌ ERROR: {str(e)[:50]}",
            "percentage": 0
        })

print("=" * 80)
print("總結")
print("=" * 80)
print(f"測試總數: {len(prompts_to_test)}")
print(f"通過: {total_pass} ({total_pass/len(prompts_to_test)*100:.1f}%)")
print(f"失敗: {total_fail} ({total_fail/len(prompts_to_test)*100:.1f}%)")
print()

if total_pass == len(prompts_to_test):
    print("🎉 所有已重構的 prompts 都通過驗證！")
else:
    print("⚠️ 部分 prompts 需要調整")

print("=" * 80)
