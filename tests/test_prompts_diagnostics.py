"""
FHL Bible MCP Server - Prompts 診斷測試套件

完整的 Prompts 診斷測試，用於識別所有問題並生成診斷報告
"""

import pytest
import sys
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json

# 添加專案根目錄到 Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fhl_bible_mcp.prompts.manager import PromptManager
from src.fhl_bible_mcp.prompts.base import PromptTemplate


# ==================== 測試配置 ====================

# 長度標準（嚴格）
LENGTH_STANDARDS = {
    'basic': 500,      # 基礎類
    'reading': 700,    # 讀經類
    'study': 800,      # 研經類
    'special': 900,    # 特殊類
    'advanced': 1000   # 進階類
}

# 所有 Prompts 的完整清單（19 個）
ALL_PROMPTS = [
    # Basic (4)
    ('basic', 'basic_help_guide', 'BasicHelpGuidePrompt'),
    ('basic', 'basic_uri_demo', 'BasicURIDemoPrompt'),
    ('basic', 'basic_quick_lookup', 'BasicQuickLookupPrompt'),
    ('basic', 'basic_tool_reference', 'BasicToolReferencePrompt'),
    
    # Reading (3)
    ('reading', 'reading_daily', 'ReadingDailyPrompt'),
    ('reading', 'reading_chapter', 'ReadingChapterPrompt'),
    ('reading', 'reading_passage', 'ReadingPassagePrompt'),
    
    # Study (4)
    ('study', 'study_verse_deep', 'StudyVerseDeepPrompt'),
    ('study', 'study_topic_deep', 'StudyTopicDeepPrompt'),
    ('study', 'study_translation_compare', 'StudyTranslationComparePrompt'),
    ('study', 'study_word_original', 'StudyWordOriginalPrompt'),
    
    # Special (5)
    ('special', 'special_sermon_prep', 'SpecialSermonPrepPrompt'),
    ('special', 'special_devotional', 'SpecialDevotionalPrompt'),
    ('special', 'special_memory_verse', 'SpecialMemoryVersePrompt'),
    ('special', 'special_topical_chain', 'SpecialTopicalChainPrompt'),
    ('special', 'special_bible_trivia', 'SpecialBibleTriviaPrompt'),
    
    # Advanced (3)
    ('advanced', 'advanced_cross_reference', 'AdvancedCrossReferencePrompt'),
    ('advanced', 'advanced_parallel_gospels', 'AdvancedParallelGospelsPrompt'),
    ('advanced', 'advanced_character_study', 'AdvancedCharacterStudyPrompt'),
]


@dataclass
class PromptDiagnosticResult:
    """Prompt 診斷結果"""
    category: str
    name: str
    class_name: str
    import_success: bool
    import_error: str = ""
    instantiate_success: bool = False
    instantiate_error: str = ""
    render_success: bool = False
    render_error: str = ""
    rendered_length: int = 0
    length_standard: int = 0
    length_over: int = 0
    length_status: str = "UNKNOWN"  # PASS / FAIL / ERROR
    has_clear_steps: bool = False
    step_count: int = 0
    has_action_verbs: bool = False
    structure_score: int = 0  # 0-100
    structure_notes: str = ""


class PromptsDiagnostics:
    """Prompts 診斷測試類"""
    
    def __init__(self):
        self.results: List[PromptDiagnosticResult] = []
        self.manager = None
    
    # ==================== 測試 1: 導入測試 ====================
    
    def test_import_all_prompts(self) -> Tuple[int, int, List[PromptDiagnosticResult]]:
        """
        測試 1: 所有 prompts 能否正確導入
        
        Returns:
            (成功數, 失敗數, 結果列表)
        """
        print("\n" + "="*80)
        print("測試 1: Prompts 導入測試")
        print("="*80)
        
        success_count = 0
        fail_count = 0
        results = []
        
        for category, name, class_name in ALL_PROMPTS:
            result = PromptDiagnosticResult(
                category=category,
                name=name,
                class_name=class_name,
                import_success=False,
                length_standard=LENGTH_STANDARDS[category]
            )
            
            try:
                # 嘗試導入
                module_path = f"src.fhl_bible_mcp.prompts.{category}"
                module = __import__(module_path, fromlist=[class_name])
                prompt_class = getattr(module, class_name)
                
                result.import_success = True
                success_count += 1
                print(f"✅ {name}: 導入成功")
                
            except Exception as e:
                result.import_success = False
                result.import_error = str(e)
                fail_count += 1
                print(f"❌ {name}: 導入失敗 - {e}")
            
            results.append(result)
        
        print(f"\n📊 導入測試結果: {success_count}/{len(ALL_PROMPTS)} 成功")
        self.results = results
        return success_count, fail_count, results
    
    # ==================== 測試 2: 實例化測試 ====================
    
    def test_instantiate_all_prompts(self) -> Tuple[int, int]:
        """
        測試 2: 所有 prompts 能否實例化
        
        Returns:
            (成功數, 失敗數)
        """
        print("\n" + "="*80)
        print("測試 2: Prompts 實例化測試")
        print("="*80)
        
        success_count = 0
        fail_count = 0
        
        for result in self.results:
            if not result.import_success:
                print(f"⏭️  {result.name}: 跳過（導入失敗）")
                continue
            
            try:
                # 嘗試實例化
                module_path = f"src.fhl_bible_mcp.prompts.{result.category}"
                module = __import__(module_path, fromlist=[result.class_name])
                prompt_class = getattr(module, result.class_name)
                
                # 無參數實例化
                instance = prompt_class()
                
                result.instantiate_success = True
                success_count += 1
                print(f"✅ {result.name}: 實例化成功")
                
            except Exception as e:
                result.instantiate_success = False
                result.instantiate_error = str(e)
                fail_count += 1
                print(f"❌ {result.name}: 實例化失敗 - {e}")
        
        print(f"\n📊 實例化測試結果: {success_count}/{len([r for r in self.results if r.import_success])} 成功")
        return success_count, fail_count
    
    # ==================== 測試 3: 渲染測試 ====================
    
    def test_render_all_prompts(self) -> Tuple[int, int]:
        """
        測試 3: 所有 prompts 能否正常渲染
        
        Returns:
            (成功數, 失敗數)
        """
        print("\n" + "="*80)
        print("測試 3: Prompts 渲染測試")
        print("="*80)
        
        success_count = 0
        fail_count = 0
        
        for result in self.results:
            if not result.import_success or not result.instantiate_success:
                print(f"⏭️  {result.name}: 跳過（導入或實例化失敗）")
                continue
            
            try:
                # 嘗試渲染
                module_path = f"src.fhl_bible_mcp.prompts.{result.category}"
                module = __import__(module_path, fromlist=[result.class_name])
                prompt_class = getattr(module, result.class_name)
                instance = prompt_class()
                
                # 使用默認參數渲染
                rendered = instance.render()
                
                if rendered and isinstance(rendered, str):
                    result.render_success = True
                    result.rendered_length = len(rendered)
                    success_count += 1
                    print(f"✅ {result.name}: 渲染成功 ({result.rendered_length} 字)")
                else:
                    result.render_success = False
                    result.render_error = "渲染返回空或非字符串"
                    fail_count += 1
                    print(f"❌ {result.name}: 渲染失敗 - 返回空或非字符串")
                
            except Exception as e:
                result.render_success = False
                result.render_error = str(e)
                fail_count += 1
                print(f"❌ {result.name}: 渲染失敗 - {e}")
        
        print(f"\n📊 渲染測試結果: {success_count}/{len([r for r in self.results if r.import_success and r.instantiate_success])} 成功")
        return success_count, fail_count
    
    # ==================== 測試 4: 長度分析 ====================
    
    def test_prompts_length_analysis(self) -> Dict[str, Any]:
        """
        測試 4: 長度分析
        
        Returns:
            統計數據字典
        """
        print("\n" + "="*80)
        print("測試 4: Prompts 長度分析")
        print("="*80)
        
        pass_count = 0
        fail_count = 0
        total_length = 0
        max_length = 0
        max_length_prompt = ""
        
        # 按類別統計
        category_stats = {
            'basic': {'count': 0, 'total': 0, 'pass': 0, 'fail': 0},
            'reading': {'count': 0, 'total': 0, 'pass': 0, 'fail': 0},
            'study': {'count': 0, 'total': 0, 'pass': 0, 'fail': 0},
            'special': {'count': 0, 'total': 0, 'pass': 0, 'fail': 0},
            'advanced': {'count': 0, 'total': 0, 'pass': 0, 'fail': 0},
        }
        
        print(f"\n{'Prompt':<35} {'長度':<8} {'標準':<8} {'超標':<8} {'狀態':<8}")
        print("-" * 75)
        
        for result in self.results:
            if not result.render_success:
                result.length_status = "ERROR"
                print(f"{result.name:<35} {'N/A':<8} {result.length_standard:<8} {'N/A':<8} ❌ ERROR")
                continue
            
            # 計算超標量
            result.length_over = result.rendered_length - result.length_standard
            
            # 判斷狀態
            if result.rendered_length <= result.length_standard:
                result.length_status = "PASS"
                pass_count += 1
                category_stats[result.category]['pass'] += 1
                status_icon = "✅ PASS"
            else:
                result.length_status = "FAIL"
                fail_count += 1
                category_stats[result.category]['fail'] += 1
                status_icon = "❌ FAIL"
            
            # 統計
            total_length += result.rendered_length
            category_stats[result.category]['count'] += 1
            category_stats[result.category]['total'] += result.rendered_length
            
            if result.rendered_length > max_length:
                max_length = result.rendered_length
                max_length_prompt = result.name
            
            # 打印結果
            print(f"{result.name:<35} {result.rendered_length:<8} {result.length_standard:<8} {result.length_over if result.length_over > 0 else '-':<8} {status_icon}")
        
        # 計算平均值
        render_success_count = len([r for r in self.results if r.render_success])
        avg_length = total_length / render_success_count if render_success_count > 0 else 0
        
        # 打印統計
        print("\n" + "="*80)
        print("📊 長度統計")
        print("="*80)
        print(f"總計: {render_success_count} 個 prompts")
        print(f"通過: {pass_count} 個 ({pass_count/render_success_count*100:.1f}%)")
        print(f"未通過: {fail_count} 個 ({fail_count/render_success_count*100:.1f}%)")
        print(f"平均長度: {avg_length:.0f} 字")
        print(f"最長 Prompt: {max_length_prompt} ({max_length} 字)")
        
        print("\n按類別統計:")
        print("-" * 75)
        print(f"{'類別':<12} {'數量':<8} {'平均長度':<12} {'通過':<8} {'未通過':<8}")
        print("-" * 75)
        for category, stats in category_stats.items():
            if stats['count'] > 0:
                avg = stats['total'] / stats['count']
                print(f"{category:<12} {stats['count']:<8} {avg:<12.0f} {stats['pass']:<8} {stats['fail']:<8}")
        
        return {
            'total': render_success_count,
            'pass': pass_count,
            'fail': fail_count,
            'avg_length': avg_length,
            'max_length': max_length,
            'max_length_prompt': max_length_prompt,
            'category_stats': category_stats
        }
    
    # ==================== 測試 5: 結構檢查 ====================
    
    def test_prompts_structure_check(self) -> Dict[str, Any]:
        """
        測試 5: 結構檢查
        
        檢查 prompt 是否包含清晰的步驟、動詞開頭的指令等
        
        Returns:
            統計數據字典
        """
        print("\n" + "="*80)
        print("測試 5: Prompts 結構檢查")
        print("="*80)
        
        action_verbs = [
            '查詢', '搜尋', '分析', '比較', '列出', '提取', '總結', '歸納',
            '檢查', '驗證', '計算', '統計', '排序', '篩選', '組織', '建立',
            '創建', '生成', '輸出', '顯示', '展示', '使用', '執行', '調用'
        ]
        
        good_structure = 0
        poor_structure = 0
        
        print(f"\n{'Prompt':<35} {'步驟':<8} {'動詞':<8} {'評分':<8} {'狀態':<10}")
        print("-" * 75)
        
        for result in self.results:
            if not result.render_success:
                print(f"{result.name:<35} {'N/A':<8} {'N/A':<8} {'N/A':<8} ⏭️  ERROR")
                continue
            
            # 獲取渲染內容
            try:
                module_path = f"src.fhl_bible_mcp.prompts.{result.category}"
                module = __import__(module_path, fromlist=[result.class_name])
                prompt_class = getattr(module, result.class_name)
                instance = prompt_class()
                rendered = instance.render()
                
                # 檢查步驟標記
                step_markers = ['## 步驟', '步驟 1', '步驟 2', '步驟 3', 'Step 1', 'Step 2']
                result.has_clear_steps = any(marker in rendered for marker in step_markers)
                
                # 計算步驟數
                result.step_count = sum(rendered.count(f'步驟 {i}') for i in range(1, 20))
                if result.step_count == 0:
                    result.step_count = sum(rendered.count(f'Step {i}') for i in range(1, 20))
                
                # 檢查動詞使用
                verb_count = sum(rendered.count(verb) for verb in action_verbs)
                result.has_action_verbs = verb_count >= 3
                
                # 計算結構評分 (0-100)
                score = 0
                notes = []
                
                # 有清晰步驟 +40
                if result.has_clear_steps:
                    score += 40
                    notes.append("有步驟標記")
                else:
                    notes.append("缺步驟標記")
                
                # 步驟數量 3-7 個 +30
                if 3 <= result.step_count <= 7:
                    score += 30
                    notes.append(f"步驟數適中({result.step_count})")
                elif result.step_count > 0:
                    score += 15
                    notes.append(f"步驟數欠佳({result.step_count})")
                else:
                    notes.append("無明確步驟")
                
                # 有動詞 +30
                if result.has_action_verbs:
                    score += 30
                    notes.append("有動作動詞")
                else:
                    notes.append("缺動作動詞")
                
                result.structure_score = score
                result.structure_notes = "; ".join(notes)
                
                # 判斷結構品質
                if score >= 70:
                    status = "✅ 良好"
                    good_structure += 1
                else:
                    status = "⚠️  待改善"
                    poor_structure += 1
                
                # 打印結果
                step_str = str(result.step_count) if result.step_count > 0 else '-'
                verb_str = '✓' if result.has_action_verbs else '✗'
                print(f"{result.name:<35} {step_str:<8} {verb_str:<8} {score:<8} {status}")
                
            except Exception as e:
                result.structure_notes = f"檢查失敗: {e}"
                print(f"{result.name:<35} {'N/A':<8} {'N/A':<8} {'N/A':<8} ❌ ERROR")
        
        # 統計
        render_success_count = len([r for r in self.results if r.render_success])
        
        print("\n" + "="*80)
        print("📊 結構統計")
        print("="*80)
        print(f"良好結構: {good_structure}/{render_success_count} ({good_structure/render_success_count*100:.1f}%)")
        print(f"待改善: {poor_structure}/{render_success_count} ({poor_structure/render_success_count*100:.1f}%)")
        
        return {
            'good_structure': good_structure,
            'poor_structure': poor_structure,
            'total': render_success_count
        }
    
    # ==================== 測試 6: PromptManager 整合 ====================
    
    def test_prompt_manager_integration(self) -> Tuple[bool, str]:
        """
        測試 6: PromptManager 整合
        
        Returns:
            (成功與否, 訊息)
        """
        print("\n" + "="*80)
        print("測試 6: PromptManager 整合測試")
        print("="*80)
        
        try:
            # 創建 PromptManager
            manager = PromptManager()
            self.manager = manager
            
            # 檢查註冊數量
            registered_count = len(manager.get_prompt_names())
            expected_count = 19
            
            print(f"\n註冊 Prompts 數量: {registered_count}")
            print(f"預期數量: {expected_count}")
            
            if registered_count == expected_count:
                print(f"✅ PromptManager 整合成功")
                
                # 測試 list_prompts
                prompts_list = manager.list_prompts()
                print(f"\nlist_prompts() 返回: {len(prompts_list)} 個 prompts")
                
                # 測試 get_prompt
                sample_prompt = manager.get_prompt('basic_help_guide')
                if sample_prompt:
                    print(f"✅ get_prompt() 成功獲取 prompt")
                else:
                    print(f"⚠️  get_prompt() 無法獲取 prompt")
                
                return True, "PromptManager 整合測試通過"
            else:
                msg = f"❌ 註冊數量不符: 預期 {expected_count}, 實際 {registered_count}"
                print(msg)
                return False, msg
                
        except Exception as e:
            msg = f"❌ PromptManager 整合失敗: {e}"
            print(msg)
            return False, msg
    
    # ==================== 生成報告 ====================
    
    def generate_report(self, output_path: str = None) -> str:
        """
        生成診斷報告
        
        Args:
            output_path: 報告輸出路徑，默認為 docs/PROMPTS_DIAGNOSTIC_REPORT.md
            
        Returns:
            報告內容
        """
        if output_path is None:
            output_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'docs', 
                'PROMPTS_DIAGNOSTIC_REPORT.md'
            )
        
        # 統計數據
        total = len(self.results)
        import_success = len([r for r in self.results if r.import_success])
        instantiate_success = len([r for r in self.results if r.instantiate_success])
        render_success = len([r for r in self.results if r.render_success])
        length_pass = len([r for r in self.results if r.length_status == "PASS"])
        length_fail = len([r for r in self.results if r.length_status == "FAIL"])
        
        # 分類問題
        p0_issues = [r for r in self.results if not r.import_success or not r.instantiate_success or not r.render_success]
        p1_issues = [r for r in self.results if r.render_success and r.length_over > r.length_standard * 0.5]
        p2_issues = [r for r in self.results if r.render_success and 0 < r.length_over <= r.length_standard * 0.5]
        p3_issues = [r for r in self.results if r.render_success and r.structure_score < 70]
        
        # 生成報告
        report = f"""# Prompts 診斷報告 🔍

**FHL Bible MCP Server - Prompts 優化診斷**

---

## 執行資訊

- **執行時間**: {self._get_current_time()}
- **測試版本**: 1.0
- **測試 Prompts 數量**: {total}
- **測試項目**: 6 項（導入、實例化、渲染、長度、結構、整合）

---

## 📊 測試結果總覽

### 基本測試

| 測試項目 | 成功 | 失敗 | 成功率 |
|---------|------|------|--------|
| **導入測試** | {import_success}/{total} | {total - import_success}/{total} | {import_success/total*100:.1f}% |
| **實例化測試** | {instantiate_success}/{total} | {total - instantiate_success}/{total} | {instantiate_success/total*100:.1f}% |
| **渲染測試** | {render_success}/{total} | {total - render_success}/{total} | {render_success/total*100:.1f}% |

### 長度分析

| 測試項目 | 通過 | 未通過 | 通過率 |
|---------|------|--------|--------|
| **長度標準** | {length_pass}/{render_success} | {length_fail}/{render_success} | {length_pass/render_success*100 if render_success > 0 else 0:.1f}% |

**標準**: 基礎 < 500 字，讀經 < 700 字，研經 < 800 字，特殊 < 900 字，進階 < 1000 字

---

## 📋 詳細分析

### 長度分析表

| Prompt | 類別 | 當前長度 | 標準 | 超標 | 狀態 |
|--------|------|----------|------|------|------|
"""
        
        # 添加每個 prompt 的詳細資料
        for result in sorted(self.results, key=lambda r: r.length_over if r.render_success else 0, reverse=True):
            if result.render_success:
                status_icon = "✅" if result.length_status == "PASS" else "❌"
                over_str = f"+{result.length_over}" if result.length_over > 0 else "-"
                report += f"| `{result.name}` | {result.category} | {result.rendered_length} | {result.length_standard} | {over_str} | {status_icon} {result.length_status} |\n"
            else:
                report += f"| `{result.name}` | {result.category} | N/A | {result.length_standard} | N/A | ❌ ERROR |\n"
        
        report += f"""
### 結構分析表

| Prompt | 步驟數 | 結構評分 | 狀態 | 備註 |
|--------|--------|----------|------|------|
"""
        
        for result in sorted(self.results, key=lambda r: r.structure_score if r.render_success else 0):
            if result.render_success:
                status_icon = "✅" if result.structure_score >= 70 else "⚠️"
                step_str = str(result.step_count) if result.step_count > 0 else "-"
                report += f"| `{result.name}` | {step_str} | {result.structure_score}/100 | {status_icon} | {result.structure_notes} |\n"
            else:
                report += f"| `{result.name}` | - | - | ❌ | 渲染失敗 |\n"
        
        report += f"""
---

## 🚨 問題分類

### P0: 載入/渲染失敗（必須立即修復）

**數量**: {len(p0_issues)} 個

"""
        
        if p0_issues:
            for result in p0_issues:
                report += f"""#### `{result.name}`

- **類別**: {result.category}
- **問題**:
"""
                if not result.import_success:
                    report += f"  - ❌ 導入失敗: `{result.import_error}`\n"
                if not result.instantiate_success:
                    report += f"  - ❌ 實例化失敗: `{result.instantiate_error}`\n"
                if not result.render_success:
                    report += f"  - ❌ 渲染失敗: `{result.render_error}`\n"
                report += "\n"
        else:
            report += "✅ 無 P0 問題\n\n"
        
        report += f"""### P1: 嚴重超長（高優先級）

**數量**: {len(p1_issues)} 個

**標準**: 超過標準 50% 以上

"""
        
        if p1_issues:
            for result in sorted(p1_issues, key=lambda r: r.length_over, reverse=True):
                over_pct = (result.length_over / result.length_standard) * 100
                report += f"- [ ] **`{result.name}`**: {result.rendered_length} 字（標準 {result.length_standard}，超標 {result.length_over} 字，+{over_pct:.0f}%）\n"
            report += "\n"
        else:
            report += "✅ 無 P1 問題\n\n"
        
        report += f"""### P2: 中度超長（中優先級）

**數量**: {len(p2_issues)} 個

**標準**: 超過標準 0-50%

"""
        
        if p2_issues:
            for result in sorted(p2_issues, key=lambda r: r.length_over, reverse=True):
                over_pct = (result.length_over / result.length_standard) * 100
                report += f"- [ ] **`{result.name}`**: {result.rendered_length} 字（標準 {result.length_standard}，超標 {result.length_over} 字，+{over_pct:.0f}%）\n"
            report += "\n"
        else:
            report += "✅ 無 P2 問題\n\n"
        
        report += f"""### P3: 結構待優化（低優先級）

**數量**: {len(p3_issues)} 個

**標準**: 結構評分 < 70

"""
        
        if p3_issues:
            for result in sorted(p3_issues, key=lambda r: r.structure_score):
                report += f"- [ ] **`{result.name}`**: 評分 {result.structure_score}/100（{result.structure_notes}）\n"
            report += "\n"
        else:
            report += "✅ 無 P3 問題\n\n"
        
        report += f"""---

## 📈 統計數據

### 按類別統計

"""
        
        # 按類別統計
        category_summary = {}
        for result in self.results:
            if result.category not in category_summary:
                category_summary[result.category] = {
                    'total': 0,
                    'render_success': 0,
                    'length_pass': 0,
                    'length_fail': 0,
                    'total_length': 0,
                    'avg_length': 0,
                    'standard': result.length_standard
                }
            
            category_summary[result.category]['total'] += 1
            if result.render_success:
                category_summary[result.category]['render_success'] += 1
                category_summary[result.category]['total_length'] += result.rendered_length
                if result.length_status == "PASS":
                    category_summary[result.category]['length_pass'] += 1
                elif result.length_status == "FAIL":
                    category_summary[result.category]['length_fail'] += 1
        
        # 計算平均值
        for cat, stats in category_summary.items():
            if stats['render_success'] > 0:
                stats['avg_length'] = stats['total_length'] / stats['render_success']
        
        report += "| 類別 | 數量 | 標準 | 平均長度 | 通過 | 未通過 | 通過率 |\n"
        report += "|------|------|------|----------|------|--------|--------|\n"
        
        for cat in ['basic', 'reading', 'study', 'special', 'advanced']:
            if cat in category_summary:
                stats = category_summary[cat]
                pass_rate = (stats['length_pass'] / stats['render_success'] * 100) if stats['render_success'] > 0 else 0
                report += f"| {cat} | {stats['total']} | {stats['standard']} | {stats['avg_length']:.0f} | {stats['length_pass']} | {stats['length_fail']} | {pass_rate:.1f}% |\n"
        
        report += f"""
### 總體統計

- **總 Prompts**: {total}
- **渲染成功**: {render_success}
- **長度通過**: {length_pass}
- **長度未通過**: {length_fail}
- **平均長度**: {sum(r.rendered_length for r in self.results if r.render_success) / render_success if render_success > 0 else 0:.0f} 字
- **最長 Prompt**: {max((r for r in self.results if r.render_success), key=lambda r: r.rendered_length).name if render_success > 0 else 'N/A'} ({max((r.rendered_length for r in self.results if r.render_success), default=0)} 字)

---

## 🎯 重構建議

### 優先級排序

1. **立即修復 P0** ({len(p0_issues)} 個)
   - 修復導入/實例化/渲染錯誤
   - 確保所有 prompts 都能正常載入

2. **高優先級 P1** ({len(p1_issues)} 個)
   - 嚴重超長的 prompts
   - 需要大幅縮減內容（50%+ 超標）

3. **中優先級 P2** ({len(p2_issues)} 個)
   - 中度超長的 prompts
   - 需要適度縮減內容（0-50% 超標）

4. **低優先級 P3** ({len(p3_issues)} 個)
   - 結構待優化的 prompts
   - 改善步驟清晰度和動詞使用

### 重構策略

**漸進優化（Strategy B）**:
1. Phase 1: 修復 P0 問題（Day 1-2）
2. Phase 2: 重構 P1 問題（Day 3-7）
3. Phase 3: 優化 P2 問題（Day 8-10）
4. Phase 4: 改善 P3 問題（Day 11-12）

### 目標

- ✅ **100% 載入成功率**
- ✅ **100% 長度合規**
- ✅ **90%+ 結構良好**
- ✅ **平均長度 < 700 字**

---

## 📝 下一步行動

1. **審閱報告**: 確認問題分類和優先級
2. **準備重構**: 創建重構模板和檢查清單
3. **開始修復**: 從 P0 問題開始，逐步解決
4. **測試驗證**: 每次重構後運行診斷測試
5. **更新文檔**: 將詳細說明移至使用指南

---

**報告生成時間**: {self._get_current_time()}  
**報告版本**: 1.0  
**狀態**: 診斷完成，待重構

---

Made with ❤️ for better Prompts 🚀
"""
        
        # 寫入檔案
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 診斷報告已生成: {output_path}")
        
        return report
    
    def _get_current_time(self) -> str:
        """獲取當前時間字串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==================== Pytest 測試函數 ====================

@pytest.fixture(scope="module")
def diagnostics():
    """創建診斷測試實例"""
    return PromptsDiagnostics()


def test_1_import_all_prompts(diagnostics):
    """測試 1: 導入測試"""
    success, fail, results = diagnostics.test_import_all_prompts()
    assert success > 0, "至少應該有一個 prompt 導入成功"


def test_2_instantiate_all_prompts(diagnostics):
    """測試 2: 實例化測試"""
    success, fail = diagnostics.test_instantiate_all_prompts()
    assert success > 0, "至少應該有一個 prompt 實例化成功"


def test_3_render_all_prompts(diagnostics):
    """測試 3: 渲染測試"""
    success, fail = diagnostics.test_render_all_prompts()
    assert success > 0, "至少應該有一個 prompt 渲染成功"


def test_4_prompts_length_analysis(diagnostics):
    """測試 4: 長度分析"""
    stats = diagnostics.test_prompts_length_analysis()
    assert stats['total'] > 0, "應該有可分析的 prompts"


def test_5_prompts_structure_check(diagnostics):
    """測試 5: 結構檢查"""
    stats = diagnostics.test_prompts_structure_check()
    assert stats['total'] > 0, "應該有可檢查的 prompts"


def test_6_prompt_manager_integration(diagnostics):
    """測試 6: PromptManager 整合"""
    success, msg = diagnostics.test_prompt_manager_integration()
    assert success, f"PromptManager 整合失敗: {msg}"


def test_7_generate_report(diagnostics):
    """測試 7: 生成診斷報告"""
    report = diagnostics.generate_report()
    assert report and len(report) > 0, "報告應該有內容"
    assert "# Prompts 診斷報告" in report, "報告應該包含標題"


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("🔍 FHL Bible MCP Server - Prompts 診斷測試")
    print("=" * 80)
    
    diagnostics = PromptsDiagnostics()
    
    # 執行所有測試
    diagnostics.test_import_all_prompts()
    diagnostics.test_instantiate_all_prompts()
    diagnostics.test_render_all_prompts()
    diagnostics.test_prompts_length_analysis()
    diagnostics.test_prompts_structure_check()
    diagnostics.test_prompt_manager_integration()
    
    # 生成報告
    print("\n" + "="*80)
    print("生成診斷報告...")
    print("="*80)
    diagnostics.generate_report()
    
    print("\n✅ 診斷測試完成！")
    print("\n請查看 docs/PROMPTS_DIAGNOSTIC_REPORT.md 獲取詳細報告")
