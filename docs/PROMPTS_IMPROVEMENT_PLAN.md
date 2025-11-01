# Prompts 改善計畫 🔧

**FHL Bible MCP Server - Prompts 優化與重構專案**

---

## 📋 執行摘要

### 問題陳述

在測試過程中發現以下問題：

1. **部分 Prompts 無法載入** - 可能存在語法錯誤或導入問題
2. **Prompt 內容過於冗長** - 後期生成的 prompts 文字描述過長
3. **缺乏清晰的執行步驟** - AI 難以抓到執行重點，描述性文字過多

### 改善目標

1. ✅ **100% 載入成功率** - 所有 19 個 prompts 都能正常載入和渲染
2. ✅ **大幅縮短內容長度** - 基礎類 < 500 字，進階類 < 1000 字
3. ✅ **強化執行步驟** - 清晰、具體、可執行的步驟導向設計
4. ✅ **提升 AI 執行成功率** - AI 能準確理解並執行 prompt 指令

### 實施策略

- **策略**: 漸進優化（Strategy B）
- **方法**: 測試優先，診斷後逐步重構
- **處理詳細說明**: 移至 PROMPTS_USAGE_GUIDE.md

---

## 🎯 改善標準

### 長度標準（嚴格）

| Prompt 類別 | 原目標 | **新標準** | 說明 |
|------------|--------|-----------|------|
| 基礎類 (basic_*) | < 3000 字 | **< 500 字** | 快速、簡潔、即用 |
| 讀經類 (reading_*) | < 4000 字 | **< 700 字** | 清晰步驟 + 簡要說明 |
| 研經類 (study_*) | < 5000 字 | **< 800 字** | 專業但精簡 |
| 特殊類 (special_*) | < 6000 字 | **< 900 字** | 專業應用，重點步驟 |
| 進階類 (advanced_*) | < 8000 字 | **< 1000 字** | 複雜但條理清晰 |

### 設計原則

#### 1. 簡潔明確 (Concise & Clear)
```
❌ 避免：
"這個 prompt 將幫助您進行深入的聖經人物研究，
透過系統化的方法論，我們將從多個維度來分析..."

✅ 改為：
"## 步驟 1: 搜尋人物經文
使用 search_bible 查詢 '{character}'"
```

#### 2. 步驟導向 (Step-Oriented)
```markdown
## 步驟 N: [動作]
**工具**: tool_name
**執行**: 具體指令
**輸出**: 預期結果
```

#### 3. 動詞開頭 (Action-First)
- ✅ 使用：查詢、分析、比較、列出、搜尋
- ❌ 避免：可以、建議、嘗試、最好

#### 4. 最小化說明 (Minimal Explanation)
- 步驟說明：20-50 字
- 總體說明：0-100 字
- 詳細說明：移至文檔

---

## 📊 Phase 1: 診斷階段

### 目標

1. 找出所有有問題的 prompts
2. 分析每個 prompt 的當前狀態
3. 生成詳細診斷報告
4. 確定重構優先級

### 實施步驟

#### 1.1 創建診斷測試套件

**檔案**: `tests/test_prompts_diagnostics.py`

**測試項目**:

```python
class PromptsDiagnostics:
    """完整的 Prompts 診斷測試"""
    
    def test_import_all_prompts(self):
        """測試 1: 所有 prompts 能否正確導入"""
        # 測試從各模組導入
        # 檢查是否有 ImportError
        pass
    
    def test_instantiate_all_prompts(self):
        """測試 2: 所有 prompts 能否實例化"""
        # 測試無參數實例化
        # 測試有參數實例化
        pass
    
    def test_render_all_prompts(self):
        """測試 3: 所有 prompts 能否正常渲染"""
        # 測試默認參數渲染
        # 測試自定義參數渲染
        # 檢查是否有運行時錯誤
        pass
    
    def test_prompts_length_analysis(self):
        """測試 4: 長度分析"""
        # 統計每個 prompt 的輸出長度
        # 標記超過標準的 prompts
        # 生成長度分布圖表
        pass
    
    def test_prompts_structure_check(self):
        """測試 5: 結構檢查"""
        # 檢查是否包含明確步驟
        # 檢查是否有動詞開頭的指令
        # 評估步驟清晰度
        pass
    
    def test_prompt_manager_integration(self):
        """測試 6: PromptManager 整合"""
        # 測試通過 manager 獲取 prompts
        # 測試 list_prompts() 功能
        # 驗證註冊數量（應為 19）
        pass
```

#### 1.2 執行診斷測試

**命令**:
```bash
# 執行診斷測試
pytest tests/test_prompts_diagnostics.py -v --tb=short

# 生成詳細報告
pytest tests/test_prompts_diagnostics.py --html=diagnostics_report.html
```

#### 1.3 生成診斷報告

**檔案**: `docs/PROMPTS_DIAGNOSTIC_REPORT.md`

**報告內容**:

```markdown
# Prompts 診斷報告

## 執行時間
2025-XX-XX

## 測試結果總覽

### 載入測試
- 成功: X/19
- 失敗: Y/19
- 成功率: Z%

### 長度分析

| Prompt | 當前長度 | 標準 | 狀態 |
|--------|---------|------|------|
| basic_help_guide | 3200 | 500 | ❌ 超標 |
| reading_daily | 2100 | 700 | ❌ 超標 |
| ... | ... | ... | ... |

### 問題分類

#### P0: 載入失敗（必須修復）
- [ ] prompt_name_1: ImportError ...
- [ ] prompt_name_2: AttributeError ...

#### P1: 嚴重超長（高優先）
- [ ] prompt_name_3: 3200 字（標準 500）
- [ ] prompt_name_4: 2100 字（標準 700）

#### P2: 中度超長（中優先）
- [ ] prompt_name_5: 1200 字（標準 1000）

#### P3: 結構待優化（低優先）
- [ ] prompt_name_6: 步驟不清晰
```

---

## 🛠️ Phase 2: 重構準備階段

### 2.1 建立 Prompt 重構模板

**檔案**: `docs/PROMPT_REFACTORING_TEMPLATE.md`

**模板結構**:

```python
"""
Prompt 重構模板

用於統一所有 prompts 的結構和風格
"""

@dataclass
class OptimizedPromptTemplate(PromptTemplate):
    """優化的 Prompt 模板"""
    
    # 參數定義（保持原有參數，確保向後兼容）
    param1: str = "default_value"
    param2: int = 1
    
    def __post_init__(self):
        """初始化"""
        super().__init__(
            name="prompt_name",
            description="一句話簡述功能（20-30 字）",
            arguments=[
                {
                    "name": "param1",
                    "description": "簡短說明（10-20 字）",
                    "required": False
                }
            ]
        )
    
    def render(self, **kwargs) -> str:
        """渲染 prompt
        
        核心原則：
        1. 總長度 < 標準（500/700/800/900/1000 字）
        2. 步驟清晰（3-7 個步驟）
        3. 動詞開頭
        4. 最小化說明
        """
        # 使用參數或默認值
        param1 = kwargs.get('param1') or self.param1
        
        # 構建輸出（使用輔助方法）
        return f"""# {self._get_title()}

{self._render_steps()}

{self._render_output_format()}
"""
    
    def _get_title(self) -> str:
        """標題（5-10 字）"""
        return "功能名稱"
    
    def _render_steps(self) -> str:
        """渲染執行步驟（核心內容）
        
        每個步驟：
        - 標題：## 步驟 N: [動作]（5-10 字）
        - 內容：20-50 字
        - 格式：**工具**、**執行**、**輸出**
        """
        steps = []
        
        # 步驟 1
        steps.append("""
## 步驟 1: [動作]
**工具**: tool_name
**執行**: 具體指令
**輸出**: 預期結果
""")
        
        # 步驟 2-N...
        
        return "\n".join(steps)
    
    def _render_output_format(self) -> str:
        """預期輸出格式（可選，50-100 字）"""
        return """
## 預期輸出
簡要說明輸出格式
"""
```

### 2.2 定義重構檢查清單

**每個 Prompt 重構時必須檢查**:

- [ ] **總長度**: 符合標準（500/700/800/900/1000 字）
- [ ] **步驟數量**: 3-7 個步驟
- [ ] **步驟標題**: 動詞開頭（查詢、分析、比較等）
- [ ] **步驟內容**: 每步 20-50 字
- [ ] **說明文字**: 最小化，移至文檔
- [ ] **參數相容**: 保持原有參數，確保向後兼容
- [ ] **載入測試**: 能正常導入和實例化
- [ ] **渲染測試**: 能正常渲染，無錯誤
- [ ] **文檔更新**: 詳細說明已移至 PROMPTS_USAGE_GUIDE.md

---

## 🔨 Phase 3: 重構實施階段

### 3.1 重構優先級

根據診斷報告結果，按以下優先級重構：

#### P0: 載入失敗（立即修復）
**時程**: Day 1-2

待診斷結果確認具體 prompts

**修復步驟**:
1. 檢查 Python 語法
2. 檢查 dataclass 定義
3. 檢查 `__post_init__` 和 `super().__init__`
4. 檢查循環導入
5. 測試驗證

#### P1: 嚴重超長（高優先）
**時程**: Day 3-7

預期需要重構的 prompts（待診斷確認）:
- `advanced_character_study` (~10,000 字 → 1000 字)
- `advanced_cross_reference` (~6,000 字 → 1000 字)
- `advanced_parallel_gospels` (~6,000 字 → 1000 字)
- `special_sermon_prep` (~5,000 字 → 900 字)
- `special_devotional` (~4,000 字 → 900 字)
- `reading_chapter` (~3,000 字 → 700 字)

**重構方法**:
1. 保留核心功能和參數
2. 精簡為 3-7 個清晰步驟
3. 移除冗長說明
4. 移除範例和詳細解釋
5. 將詳細內容移至 PROMPTS_USAGE_GUIDE.md

#### P2: 中度超長（中優先）
**時程**: Day 8-10

預期需要優化的 prompts:
- 其他超過標準但不嚴重的 prompts

#### P3: 結構優化（低優先）
**時程**: Day 11-12

- 結構不清晰但長度可接受的 prompts

### 3.2 重構範例

#### 範例 1: advanced_character_study

**當前問題**:
- 長度: ~10,000 字
- 標準: < 1000 字
- 問題: 大量說明文字、過多範例、冗長描述

**重構後**:

```python
def render(self, character=None, focus=None, testament=None, version=None):
    character = character or self.character
    focus = focus or self.focus
    testament = testament or self.testament
    version = version or self.version
    
    return f"""# 人物研究: {character}

## 步驟 1: 搜尋經文
**工具**: search_bible
**執行**: 查詢所有提及 "{character}" 的經文
**輸出**: 經文列表（書卷、章節、節數）

## 步驟 2: 建立時間線
**工具**: get_bible_verse
**執行**: 按時間順序列出 5-10 個關鍵事件
**輸出**: 時間線（早年→呼召→高峰→試煉→晚年）

## 步驟 3: 性格分析
**執行**: 從事件中歸納性格特質
**輸出**: 優點 3-5 項、缺點 3-5 項，各附經文依據

## 步驟 4: 屬靈教訓
**執行**: 提煉可學習的功課
**輸出**: 正面榜樣、負面警戒、神的恩典

## 步驟 5: 關係網絡
**執行**: 列出與其他人物的關係
**輸出**: 家人、師徒、同工、對手

## 預期輸出
簡要報告格式：基本資料 → 時間線 → 性格 → 教訓 → 關係

💡 參數 focus 可控制輸出範圍：biography/character/lessons/all
"""
    # 總長度: ~400 字 ✅
```

**說明移至文檔**:
- 詳細的 9 大研究維度說明 → PROMPTS_USAGE_GUIDE.md
- 使用範例和技巧 → PROMPTS_USAGE_GUIDE.md
- 輸出格式範例 → PROMPTS_USAGE_GUIDE.md

#### 範例 2: special_sermon_prep

**當前問題**:
- 長度: ~5,000 字
- 標準: < 900 字
- 問題: 過多的準備建議、例證說明

**重構後**:

```python
def render(self, passage=None, sermon_type=None, audience=None):
    passage = passage or self.passage
    sermon_type = sermon_type or self.sermon_type
    audience = audience or self.audience
    
    return f"""# 講道準備: {passage}

## 步驟 1: 經文研讀
**工具**: get_bible_verse, get_word_analysis
**執行**: 查詢 {passage} 原文，分析關鍵字詞
**輸出**: 經文內容、原文分析、上下文

## 步驟 2: 查閱註釋
**工具**: get_commentary
**執行**: 查詢 {passage} 的註釋書
**輸出**: 解經要點、神學意義

## 步驟 3: 交叉引用
**工具**: search_bible
**執行**: 找出相關經文（3-5 處）
**輸出**: 平行經文、主題連結

## 步驟 4: 建立大綱
**執行**: 根據經文結構設計 3-5 點大綱
**輸出**: 主要大綱，每點附經文支持

## 步驟 5: 應用方向
**執行**: 針對 {audience} 聽眾設計應用
**輸出**: 實際應用、行動建議

## 預期輸出
講道大綱：引言 → 3-5 要點 → 應用 → 結論

💡 sermon_type: expository/topical/textual
💡 audience: general/youth/new_believers/mature
"""
    # 總長度: ~500 字 ✅
```

### 3.3 重構工作流程

**每個 Prompt 的重構流程**:

```
1. 閱讀當前 prompt 代碼
   ↓
2. 識別核心功能和參數
   ↓
3. 提取主要執行步驟（3-7 個）
   ↓
4. 精簡每個步驟為 20-50 字
   ↓
5. 移除冗長說明、範例、詳細解釋
   ↓
6. 將詳細內容移至 PROMPTS_USAGE_GUIDE.md
   ↓
7. 測試：載入、渲染、長度檢查
   ↓
8. Code Review：符合標準檢查清單
   ↓
9. 提交代碼
```

---

## ✅ Phase 4: 測試與驗證階段

### 4.1 重構後測試

**執行完整測試套件**:

```bash
# 1. 載入測試
pytest tests/test_prompts_diagnostics.py::test_import_all_prompts -v

# 2. 渲染測試
pytest tests/test_prompts_diagnostics.py::test_render_all_prompts -v

# 3. 長度測試
pytest tests/test_prompts_diagnostics.py::test_prompts_length_analysis -v

# 4. 完整測試
pytest tests/test_prompts_diagnostics.py -v

# 5. 生成報告
pytest tests/test_prompts_diagnostics.py --html=refactoring_report.html
```

**驗證標準**:
- ✅ 所有 prompts 載入成功（19/19）
- ✅ 所有 prompts 渲染成功（19/19）
- ✅ 所有 prompts 長度符合標準
- ✅ 所有步驟清晰明確

### 4.2 實際使用測試

**在 AI 助手中測試每個 prompt**:

#### 測試矩陣

| Prompt | Claude Desktop | GitHub Copilot | 執行成功 | 備註 |
|--------|---------------|----------------|----------|------|
| basic_help_guide | ✅ | ✅ | ✅ | - |
| basic_uri_demo | ✅ | ✅ | ✅ | - |
| ... | ... | ... | ... | ... |

#### 測試項目
1. **AI 理解度**: AI 是否理解 prompt 意圖
2. **執行完整度**: AI 是否完成所有步驟
3. **輸出品質**: 輸出是否符合預期
4. **錯誤率**: 是否有執行錯誤或遺漏

### 4.3 性能測試

**長度對比**:

```markdown
# 重構前後對比

| Prompt | 重構前 | 重構後 | 縮減率 |
|--------|--------|--------|--------|
| basic_help_guide | 3200 | 450 | 86% |
| advanced_character_study | 10127 | 950 | 91% |
| ... | ... | ... | ... |
| **平均** | **~6500** | **~700** | **89%** |
```

---

## 📚 Phase 5: 文檔更新階段

### 5.1 更新 PROMPTS_USAGE_GUIDE.md

**新增內容**:

```markdown
# Prompts 使用指南

## 設計哲學

FHL Bible MCP Server 的 prompts 採用**精簡步驟導向**設計：
- ✅ 簡潔明確（基礎類 < 500 字，進階類 < 1000 字）
- ✅ 步驟清晰（3-7 個可執行步驟）
- ✅ 動詞開頭（查詢、分析、比較）
- ✅ 最小化說明（重點在執行）

## 詳細說明

### [Prompt Name]

**快速使用**:
```
使用 [prompt_name] [簡單範例]
```

**詳細說明**:
[從原 prompt 中移過來的詳細說明]
- 完整功能介紹
- 使用場景
- 參數詳解
- 輸出範例
- 使用技巧

...（對每個 prompt 重複）
```

### 5.2 更新 PROMPTS_QUICK_REFERENCE.md

**更新統計數據**:
- 平均長度從 ~6500 字縮減至 ~700 字
- 縮減率: 89%
- 步驟清晰度提升

### 5.3 創建重構報告

**檔案**: `docs/PROMPTS_REFACTORING_REPORT.md`

**內容**:
```markdown
# Prompts 重構報告

## 執行摘要
- 重構日期: 2025-XX-XX
- 重構 Prompts: 19 個
- 成功率: 100%

## 改善成果

### 長度優化
- 重構前平均: ~6500 字
- 重構後平均: ~700 字
- 縮減率: 89%

### 載入成功率
- 重構前: XX%
- 重構後: 100%

### AI 執行成功率
- 重構前: XX%
- 重構後: XX%

## 詳細對比

[每個 prompt 的前後對比]

## 經驗總結

[重構過程中的經驗和教訓]
```

---

## 📅 實施時程

### 第 1 週：診斷與準備（5 天）

**Day 1-2: 創建診斷測試**
- [ ] 創建 `tests/test_prompts_diagnostics.py`
- [ ] 實現 6 個診斷測試函數
- [ ] 設置測試環境

**Day 3: 執行診斷**
- [ ] 執行完整診斷測試
- [ ] 收集測試結果
- [ ] 識別問題 prompts

**Day 4: 生成報告**
- [ ] 生成 `PROMPTS_DIAGNOSTIC_REPORT.md`
- [ ] 分析問題並分類（P0/P1/P2/P3）
- [ ] 確定重構優先級

**Day 5: 準備重構**
- [ ] 創建 `PROMPT_REFACTORING_TEMPLATE.md`
- [ ] 定義重構檢查清單
- [ ] 準備重構工具和環境

---

### 第 2 週：P0 和 P1 重構（5 天）

**Day 1-2: 修復 P0（載入失敗）**
- [ ] 修復所有載入失敗的 prompts
- [ ] 測試驗證載入成功
- [ ] 提交代碼

**Day 3-5: 重構 P1（嚴重超長）**
- [ ] 重構 advanced_character_study
- [ ] 重構 advanced_cross_reference
- [ ] 重構 advanced_parallel_gospels
- [ ] 重構 special_sermon_prep
- [ ] 重構 special_devotional
- [ ] 重構 reading_chapter
- [ ] 每個 prompt 重構後立即測試

---

### 第 3 週：P2/P3 重構與測試（5 天）

**Day 1-2: 重構 P2（中度超長）**
- [ ] 重構剩餘超長 prompts
- [ ] 測試驗證

**Day 3: 重構 P3（結構優化）**
- [ ] 優化結構不清晰的 prompts
- [ ] 測試驗證

**Day 4-5: 全面測試**
- [ ] 執行完整測試套件
- [ ] 在 Claude Desktop 測試所有 prompts
- [ ] 在 GitHub Copilot 測試所有 prompts
- [ ] 收集測試結果

---

### 第 4 週：文檔與收尾（5 天）

**Day 1-2: 更新文檔**
- [ ] 更新 PROMPTS_USAGE_GUIDE.md（移入詳細說明）
- [ ] 更新 PROMPTS_QUICK_REFERENCE.md
- [ ] 更新 README.md（如需要）

**Day 3: 創建重構報告**
- [ ] 創建 PROMPTS_REFACTORING_REPORT.md
- [ ] 記錄前後對比數據
- [ ] 總結經驗教訓

**Day 4: 最終驗證**
- [ ] 完整測試所有功能
- [ ] 驗證文檔完整性
- [ ] 確認向後兼容性

**Day 5: 發布準備**
- [ ] 更新版本號
- [ ] 準備 Release Notes
- [ ] 代碼審查
- [ ] 合併到主分支

---

## 📊 成功指標

### 量化指標

| 指標 | 當前值 | 目標值 | 測量方式 |
|------|--------|--------|----------|
| **載入成功率** | TBD | 100% | 自動化測試 |
| **渲染成功率** | TBD | 100% | 自動化測試 |
| **平均長度** | ~6500 字 | ~700 字 | 字數統計 |
| **最大長度** | ~10000 字 | < 1000 字 | 字數統計 |
| **步驟清晰度** | 低 | 高 | 人工審查 + 測試 |
| **AI 執行成功率** | TBD | > 90% | 實際使用測試 |

### 質化指標

- ✅ **可讀性**: Prompts 簡潔易懂
- ✅ **可執行性**: AI 能準確執行步驟
- ✅ **可維護性**: 代碼結構清晰，易於維護
- ✅ **向後兼容**: 不破壞現有功能
- ✅ **用戶體驗**: 使用者反饋正面

---

## 🔄 持續改進

### 重構後的維護

1. **新增 Prompt 規範**
   - 所有新 prompts 必須符合新標準
   - 使用重構模板
   - Code Review 檢查長度和結構

2. **定期檢查**
   - 每月執行診斷測試
   - 監控 prompts 長度變化
   - 收集用戶反饋

3. **版本控制**
   - 記錄每次 prompt 修改
   - 維護變更日誌
   - 追蹤性能指標

---

## 📝 附錄

### A. 詳細說明移動清單

**需要從 Prompts 移至 PROMPTS_USAGE_GUIDE.md 的內容**:

1. **功能介紹** - 完整的功能說明（100-300 字）
2. **使用場景** - 詳細的使用場景描述
3. **參數詳解** - 每個參數的詳細說明和範例
4. **輸出範例** - 完整的輸出格式範例
5. **使用技巧** - 進階使用技巧和建議
6. **範例說明** - 具體的使用範例展示
7. **注意事項** - 詳細的注意事項和限制
8. **相關 Prompts** - 相關 prompts 的推薦和說明

### B. 重構前後範例對比

**詳見重構實施階段的範例 1 和範例 2**

### C. 測試命令速查

```bash
# 診斷測試
pytest tests/test_prompts_diagnostics.py -v

# 單個測試
pytest tests/test_prompts_diagnostics.py::test_import_all_prompts -v

# 生成 HTML 報告
pytest tests/test_prompts_diagnostics.py --html=report.html

# 長度分析
pytest tests/test_prompts_diagnostics.py::test_prompts_length_analysis -v

# 所有 prompts 測試
pytest tests/ -k prompt -v
```

---

## ✅ 審批與執行

### 決策確認

- ✅ **策略**: 漸進優化（Strategy B）
- ✅ **長度標準**: 基礎類 < 500 字，進階類 < 1000 字
- ✅ **詳細說明**: 移至 PROMPTS_USAGE_GUIDE.md
- ✅ **優先順序**: 測試優先

### 下一步行動

1. **立即執行**: Phase 1 診斷階段
2. **等待確認**: 診斷報告完成後再開始重構
3. **持續溝通**: 每個階段完成後報告進度

---

**文檔版本**: 1.0  
**創建日期**: 2025-01-XX  
**作者**: FHL Bible MCP Server Team  
**狀態**: 待執行

---

**Made with ❤️ for better Prompts** 🚀
