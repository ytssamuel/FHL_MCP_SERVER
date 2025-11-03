# 手冊及說明文件 (Manuals & Documentation)

本資料夾包含 FHL Bible MCP Server 的使用手冊、API 文件和參考資料。

## 📚 文件列表

### API 文件

- **API.md** - 完整的 API 參考文件
  - 所有工具 (Tools) 的詳細說明
  - 資源 (Resources) URI 格式
  - 參數說明和使用範例
  - 錯誤處理說明

- **API_PARAMETER_FIX.md** - API 參數修復報告
  - `search_type` 參數一致性修復
  - 正確的參數值：`keyword`, `greek_number`, `hebrew_number`
  - 相關文件和測試的更新記錄

### 使用範例

- **EXAMPLES.md** - 實用範例集合
  - 常見使用場景
  - 工具組合使用方式
  - 與 Claude 對話的實際範例
  - 最佳實踐建議

### 快速參考

- **PROMPTS_QUICK_REFERENCE.md** - Prompts 快速參考
  - 所有 19 個 Prompts 的概覽
  - 快速查找表
  - 適用場景說明
  - 參數速查

### 測試報告

- **TESTING_REPORT.md** - 測試報告
  - 單元測試結果
  - 整合測試結果
  - 測試覆蓋率統計
  - 已知問題和限制

- **test_summary.txt** - 測試摘要
  - 最新測試運行結果
  - 簡要統計資料

---

## 🎯 文件用途

### 開發者參考

**API.md** 提供：
- 所有可用工具的技術規格
- 參數類型和驗證規則
- 返回值格式說明
- 錯誤碼和異常處理

**API_PARAMETER_FIX.md** 說明：
- 參數變更歷史
- Breaking changes 警告
- 遷移指南

### 使用者指南

**EXAMPLES.md** 包含：
- 實際使用情境範例
- 從簡單到複雜的漸進式教學
- 常見問題解決方案
- 工具組合使用技巧

**PROMPTS_QUICK_REFERENCE.md** 幫助：
- 快速找到適合的 Prompt
- 了解每個 Prompt 的用途
- 選擇正確的參數

### 質量保證

**TESTING_REPORT.md** 展示：
- 系統穩定性和可靠性
- 測試覆蓋範圍
- 性能指標
- 回歸測試結果

---

## 📖 使用建議

### 新手入門

1. 從 **EXAMPLES.md** 開始，看實際使用範例
2. 參考 **PROMPTS_QUICK_REFERENCE.md** 找到適合的 Prompt
3. 需要詳細資訊時查看 **API.md**

### 進階使用

1. 深入閱讀 **API.md** 了解所有工具
2. 參考 **EXAMPLES.md** 中的複雜範例
3. 查看 **TESTING_REPORT.md** 了解系統限制

### 開發整合

1. **API.md** 是主要技術參考
2. **API_PARAMETER_FIX.md** 了解變更歷史
3. **TESTING_REPORT.md** 確認測試覆蓋

---

## 🔧 API 重要資訊

### 工具分類

| 類別 | 工具數 | 主要用途 |
|------|--------|---------|
| **經文查詢** | 4 | 取得聖經經文 |
| **搜尋** | 3 | 全文搜尋和原文搜尋 |
| **原文研究** | 2 | Strong's 字典和字詞分析 |
| **註釋** | 2 | 經文註釋查詢 |
| **資訊** | 4 | 版本、書卷、註釋書列表 |
| **音訊** | 2 | 聖經朗讀音訊 |

### Resource URI 格式

```
bible://verse/{version}/{book}/{chapter}/{verse}
bible://chapter/{version}/{book}/{chapter}
strongs://{testament}/{number}
commentary://{book}/{chapter}/{verse}
info://{resource_type}
```

### 常用參數

- **version**: 聖經版本（如 `unv`, `niv`, `kjv`）
- **book**: 書卷名稱（支援中英文）
- **testament**: 約別（`OT` 舊約, `NT` 新約）
- **search_type**: 搜尋類型（`keyword`, `greek_number`, `hebrew_number`）

---

## ⚠️ 重要提醒

### Breaking Changes

**search_type 參數變更** (詳見 API_PARAMETER_FIX.md)：
- ❌ 舊值：`"greek"`, `"hebrew"`
- ✅ 新值：`"greek_number"`, `"hebrew_number"`

使用舊值會導致錯誤：
```
Invalid parameter 'search_type': greek - Must be 'keyword', 'greek_number', or 'hebrew_number'
```

---

## 📌 相關資料夾

- `../1_development/` - 開發文件和技術實作
- `../2_prompts_enhancement/` - Prompts 新增計劃
- `../3_prompts_improvement/` - Prompts 改進記錄
- `../deployment/` - 部署相關文件
- `../prompt_example/` - Prompt 範例文本

---

## 💡 獲取幫助

### 線上資源
- 使用 `basic_help_guide` Prompt 取得互動式幫助
- 使用 `basic_tool_reference` Prompt 查看工具說明
- 使用 `basic_uri_demo` Prompt 學習 URI 使用

### 文件導航
- 基礎使用 → EXAMPLES.md
- 快速查找 → PROMPTS_QUICK_REFERENCE.md
- 詳細規格 → API.md
- 測試狀態 → TESTING_REPORT.md

---

**最後更新**: 2025年11月3日
