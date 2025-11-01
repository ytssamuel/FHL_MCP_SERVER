# Refactoring Tools

本目錄包含 FHL Bible MCP Server Prompts 重構專案中使用的工具腳本。

## 📁 目錄結構

### 驗證腳本 (Verification Scripts)

這些腳本用於驗證 prompts 是否符合長度標準和功能要求。

- **verify_all_19_prompts.py** - 驗證所有19個prompts（完整版本）
- **verify_all_p1.py** - 驗證P1階段的15個prompts
- **verify_p1_midpoint.py** - 驗證P1中期的6個prompts
- **verify_basic_tool_reference.py** - 驗證單個prompt（basic_tool_reference）
- **verify_character_study.py** - 驗證單個prompt（advanced_character_study）
- **verify_reading_passage.py** - 驗證單個prompt（reading_passage）
- **verify_uri_demo.py** - 驗證單個prompt（basic_uri_demo）

### 批次處理腳本 (Batch Processing Scripts)

這些腳本用於批次重構多個 prompts。

- **quick_refactor_batch1.py** - 第一批批次重構（prompt #7）
- **quick_refactor_batch2.py** - 第二批批次重構（prompts #8-15）
- **batch_refactor.py** - 通用批次重構腳本
- **batch_prompts_templates.py** - 批次重構的模板定義

## 🚀 使用方式

### 驗證所有 Prompts

```bash
# 驗證所有19個prompts
python tests/refactoring_tools/verify_all_19_prompts.py

# 驗證P1的15個prompts
python tests/refactoring_tools/verify_all_p1.py

# 驗證P1中期的6個prompts
python tests/refactoring_tools/verify_p1_midpoint.py
```

### 批次重構 Prompts

```bash
# 執行第一批重構
python tests/refactoring_tools/quick_refactor_batch1.py

# 執行第二批重構
python tests/refactoring_tools/quick_refactor_batch2.py
```

## 📊 重構成果

本次重構專案的完整成果：

- **重構數量**: 19個prompts
- **總縮減**: 131,460字 → 8,621字 (-93.4%)
- **驗證通過率**: 100% (19/19)
- **結構優化**: 100%採用步驟導向格式

詳細報告請參閱：
- `docs/PROMPTS_COMPLETE_REFACTORING_REPORT.md` - 完整重構報告
- `docs/PROMPT_P1_REFACTORING_REPORT.md` - P1階段報告
- `docs/PROMPT_P1_MIDPOINT_REPORT.md` - P1中期報告

## 🎯 腳本說明

### 驗證腳本功能

所有驗證腳本都會：
1. 動態導入 prompt 類別
2. 實例化並渲染 prompt
3. 檢查渲染後的長度是否符合標準
4. 輸出詳細的驗證報告

### 批次處理腳本功能

批次處理腳本會：
1. 自動備份原始檔案（.bak）
2. 寫入重構後的內容
3. 使用UTF-8編碼確保正確性
4. 輸出執行結果

## 📝 注意事項

1. 這些腳本主要用於專案重構過程，現在作為歷史記錄保存
2. 未來如需類似的重構工作，可以參考這些腳本
3. 驗證腳本仍可用於日常檢查 prompts 品質
4. 不建議直接執行批次處理腳本，除非明確需要重新重構

## 🔗 相關文件

- [完整重構報告](../../docs/PROMPTS_COMPLETE_REFACTORING_REPORT.md)
- [P1重構報告](../../docs/PROMPT_P1_REFACTORING_REPORT.md)
- [P1中期報告](../../docs/PROMPT_P1_MIDPOINT_REPORT.md)
- [診斷報告](../../docs/PROMPTS_DIAGNOSTIC_REPORT.md)

---

**創建日期**: 2025年11月1日  
**專案**: FHL Bible MCP Server Prompts Refactoring  
**狀態**: ✅ 已完成
