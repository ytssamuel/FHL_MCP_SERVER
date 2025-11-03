# 📁 Docs 資料夾組織說明

**組織日期**: 2025年11月3日  
**版本**: 1.0

本文件說明 `docs/` 資料夾的組織結構和使用指南。

---

## 📂 資料夾結構

```
docs/
├── 1_development/          # 開發文件（起始專案）
├── 2_prompts_enhancement/  # Prompts 新增計劃
├── 3_prompts_improvement/  # Prompts 改進計劃
├── 4_manuals/              # 手冊及說明文件
├── deployment/             # 部署相關文件
└── prompt_example/         # Prompt 範例文本
```

---

## 🗂️ 各資料夾說明

### 1️⃣ 開發文件 (1_development/)

**用途**: 專案開發相關的核心文件

**包含內容**:
- 起始專案文件（開發指南、安裝指南、專案規劃）
- 技術實作說明（Server、Cache）
- Phase 3 & 4 開發階段報告

**適合對象**: 開發者、專案管理者、技術架構師

**重點文件**:
- `DEVELOPER_GUIDE.md` - 開發者指南
- `INSTALLATION_GUIDE.md` - 安裝指南
- `FHL_BIBLE_MCP_PLANNING.md` - 專案規劃

📖 [查看完整 README](1_development/README.md)

---

### 2️⃣ Prompts 新增計劃 (2_prompts_enhancement/)

**用途**: 新增 15 個 Prompts 的計劃和實作記錄

**包含內容**:
- 完整的新增計劃（15 個新 Prompts 設計）
- Phase 1-4 完成報告（Basic → Reading → Special → Advanced）
- Prompts 使用指南

**適合對象**: 產品設計者、使用者體驗設計師、文檔撰寫者

**重點文件**:
- `PROMPTS_ENHANCEMENT_PLAN.md` - 新增計劃
- `PROMPTS_USAGE_GUIDE.md` - 使用指南
- `PROMPTS_PHASE1-4_COMPLETION_REPORT.md` - 各階段報告

**成果**: 19 個 Prompts（4 個原有 + 15 個新增）

📖 [查看完整 README](2_prompts_enhancement/README.md)

---

### 3️⃣ Prompts 改進計劃 (3_prompts_improvement/)

**用途**: 現有 Prompts 的重構和優化記錄

**包含內容**:
- 改進計劃和診斷報告
- P0/P1/P2/P3 重構記錄
- 完整重構報告（-93.4% 長度優化）
- 重構工具組織

**適合對象**: 代碼優化者、質量保證工程師、維護人員

**重點文件**:
- `PROMPTS_IMPROVEMENT_PLAN.md` - 改進計劃
- `PROMPTS_COMPLETE_REFACTORING_REPORT.md` - 完整重構報告
- `PROMPTS_DIAGNOSTIC_REPORT.md` - 診斷報告

**成果**: 131,460 → 8,621 字元（-93.4%），100% 測試通過

📖 [查看完整 README](3_prompts_improvement/README.md)

---

### 4️⃣ 手冊及說明文件 (4_manuals/)

**用途**: 使用者手冊、API 參考、測試報告

**包含內容**:
- API 完整文件
- 使用範例集合
- Prompts 快速參考
- 測試報告

**適合對象**: 終端用戶、API 整合開發者、測試人員

**重點文件**:
- `API.md` - API 完整參考
- `EXAMPLES.md` - 實用範例
- `PROMPTS_QUICK_REFERENCE.md` - Prompts 速查
- `TESTING_REPORT.md` - 測試報告

📖 [查看完整 README](4_manuals/README.md)

---

### 📦 部署文件 (deployment/)

**用途**: 部署策略和多平台支援計劃

**包含內容**:
- CLI 實作計劃
- GUI 開發計劃
- 部署路線圖
- 多平台支援策略

**適合對象**: DevOps 工程師、系統管理員

**重點文件**:
- `DEPLOYMENT_STRATEGY.md`
- `CLI_IMPLEMENTATION_PLAN.md`
- `GUI_DEVELOPMENT_PLAN.md`

---

### 📝 Prompt 範例 (prompt_example/)

**用途**: 所有 Prompts 的原始範例文本

**包含內容**:
- 19 個 Prompt 的完整文本
- 中文研經範例

**適合對象**: Prompt 開發者、內容撰寫者

**檔案格式**: `.txt` 文本檔

---

## 🎯 快速導航

### 我想...

#### 開始開發
→ 前往 `1_development/`  
→ 閱讀 `DEVELOPER_GUIDE.md` 和 `INSTALLATION_GUIDE.md`

#### 了解 Prompts 功能
→ 前往 `2_prompts_enhancement/`  
→ 閱讀 `PROMPTS_ENHANCEMENT_PLAN.md` 和 `PROMPTS_USAGE_GUIDE.md`

#### 學習如何使用
→ 前往 `4_manuals/`  
→ 閱讀 `EXAMPLES.md` 和 `PROMPTS_QUICK_REFERENCE.md`

#### 查看 API 文件
→ 前往 `4_manuals/`  
→ 閱讀 `API.md`

#### 了解重構過程
→ 前往 `3_prompts_improvement/`  
→ 閱讀 `PROMPTS_COMPLETE_REFACTORING_REPORT.md`

#### 準備部署
→ 前往 `deployment/`  
→ 閱讀 `DEPLOYMENT_STRATEGY.md`

---

## 📊 專案統計

### 文件數量

| 資料夾 | 文件數 |
|--------|--------|
| 1_development | 14 個 |
| 2_prompts_enhancement | 7 個 |
| 3_prompts_improvement | 10 個 |
| 4_manuals | 7 個 |
| deployment | 5 個 |
| prompt_example | 20 個 |
| **總計** | **63 個** |

### Prompts 成果

- **總 Prompts**: 19 個
- **新增**: 15 個（Phase 1-4）
- **重構**: 19 個（P0-P3）
- **長度優化**: -93.4%
- **測試通過率**: 100%

---

## 🔍 文件索引

### 核心規劃文件
- 專案規劃: `1_development/FHL_BIBLE_MCP_PLANNING.md`
- Prompts 新增: `2_prompts_enhancement/PROMPTS_ENHANCEMENT_PLAN.md`
- Prompts 改進: `3_prompts_improvement/PROMPTS_IMPROVEMENT_PLAN.md`
- 部署策略: `deployment/DEPLOYMENT_STRATEGY.md`

### 使用指南
- 開發指南: `1_development/DEVELOPER_GUIDE.md`
- 安裝指南: `1_development/INSTALLATION_GUIDE.md`
- Prompts 使用: `2_prompts_enhancement/PROMPTS_USAGE_GUIDE.md`
- API 參考: `4_manuals/API.md`
- 使用範例: `4_manuals/EXAMPLES.md`

### 完成報告
- Phase 3 總結: `1_development/PHASE_3_SUMMARY.md`
- Phase 4 最終: `1_development/PHASE_4_2_FINAL_REPORT.md`
- Prompts 新增: `2_prompts_enhancement/PROMPTS_PHASE1-4_COMPLETION_REPORT.md`
- Prompts 重構: `3_prompts_improvement/PROMPTS_COMPLETE_REFACTORING_REPORT.md`

### 快速參考
- Prompts 速查: `4_manuals/PROMPTS_QUICK_REFERENCE.md`
- API 參數修復: `4_manuals/API_PARAMETER_FIX.md`
- 測試報告: `4_manuals/TESTING_REPORT.md`

---

## 🛠️ 維護指南

### 新增文件時

1. **確定文件類型**:
   - 開發相關 → `1_development/`
   - Prompts 新功能 → `2_prompts_enhancement/`
   - Prompts 優化 → `3_prompts_improvement/`
   - 使用手冊/API → `4_manuals/`
   - 部署相關 → `deployment/`
   - Prompt 文本 → `prompt_example/`

2. **更新對應的 README.md**

3. **更新本文件的索引**

### 重組文件時

1. 維持 4 大分類的邏輯
2. 更新所有交叉引用
3. 更新各資料夾的 README.md
4. 記錄變更歷史

---

## 📌 注意事項

### ⚠️ 請勿修改

- `deployment/` - 部署文件，保持獨立
- `prompt_example/` - Prompt 原始文本，由系統使用

### ✅ 建議做法

- 每個資料夾的 README.md 提供詳細說明
- 使用清晰的文件命名規範
- 相關文件集中存放
- 定期更新索引和交叉引用

---

## 📞 聯絡資訊

如有文件組織建議或發現問題，請：
1. 查看對應資料夾的 README.md
2. 參考本文件的快速導航
3. 提交 Issue 或 Pull Request

---

**維護者**: FHL Bible MCP Server 開發團隊  
**最後更新**: 2025年11月3日  
**版本**: 1.0
