# API 增強計畫文檔

**資料夾**: `docs/5_api_enhancement/`  
**目的**: FHL MCP Server API 功能擴展規劃與測試

---

## 📁 文檔清單

### 1. API_ENHANCEMENT_PLAN.md ⭐
**完整的 API 增強計畫**

包含內容:
- 📊 API 盤點結果（已實作 vs 未實作）
- 🧪 API 端點可行性測試報告
- 📝 文章 API 整合分析
- 🗺️ 分階段實作規劃
- ⚠️ 風險評估與建議

### 2. API_TEST_RESULTS.md
**詳細測試結果記錄**

測試項目:
- ✅ bible.fhl.net/json/ 端點測試
- ✅ bible.fhl.net/api/ 端點測試
- ✅ www.fhl.net/api/json.php 測試
- ✅ www.fhl.net/api/json_all.php 測試

---

## 🎯 關鍵發現

### 1. API 路徑升級 ⭐

**重大發現**: `bible.fhl.net/api/` 完全可用且功能更強！

| 項目 | /json/ 端點 | /api/ 端點 |
|------|------------|-----------|
| 可用性 | ✅ | ✅ |
| 欄位 | 基本 | **包含 `bid`** |
| 建議 | 保持相容 | **推薦使用** |

**結論**: 建議升級 base URL 到 `/api/`

### 2. API 完成度

| 類別 | 已實作 | 未實作 | 完成度 |
|------|--------|--------|--------|
| 基礎資訊 | 2 | 1 | 67% |
| 經文查詢 | 2 | 3 | 40% |
| 搜尋 | 1 | 2 | 33% |
| 字彙分析 | 2 | 2 | 50% |
| 註釋 | 3 | 0 | 100% ✅ |
| 主題查經 | 1 | 0 | 100% ✅ |
| 多媒體 | 1 | 0 | 100% ✅ |
| **文章** | **0** | **2** | **0%** ⚠️ |
| **總計** | **12** | **10** | **55%** |

### 3. 文章 API

**新發現**: 信望愛站提供文章查詢 API

- ✅ `json.php` - 可搜尋文章（需參數）
- ✅ `json_all.php` - 取得文章總數
- ⚠️ 無分頁機制
- ⚠️ 無參數時資料過大（8021 筆）

---

## 📋 未實作 API 清單

### 優先級 P1（核心功能）

1. ⭐ **qsub.php** - 查詢次經
2. ⭐ **qaf.php** - 查詢使徒教父文獻
3. ⭐ **sesub.php** - 次經搜尋
4. ⭐ **seaf.php** - 使徒教父搜尋
5. ⭐ **json.php** - 文章搜尋（新發現）
6. ⭐ **json_all.php** - 文章列表（新發現）

### 優先級 P2（輔助功能）

7. **rt.php** - 經文註腳（XML 格式）
8. **abv.php** - 離線資料狀況

### 優先級 P3（版權限制）

9. ⚠️ **sbdag.php** - 浸宣希臘文字典（需授權）
10. ⚠️ **stwcbhdic.php** - 浸宣希伯來文字典（需授權）

---

## 🗓️ 實作計畫

### Phase 1: Base URL 升級（P0）
- **工時**: 2-3 小時
- **內容**: 升級到 `/api/` 端點
- **優先級**: 最高 ⭐⭐⭐

### Phase 2: 次經與使徒教父（P1）
- **工時**: 8-11 小時
- **內容**: qsub.php, qaf.php, sesub.php, seaf.php
- **優先級**: 高 ⭐⭐

### Phase 3: 文章 API（P1）
- **工時**: 4-5 小時
- **內容**: json.php 整合
- **優先級**: 高 ⭐⭐

### Phase 4: 輔助功能（P2）
- **工時**: 3-5 小時
- **內容**: rt.php, abv.php
- **優先級**: 中 ⭐

### Phase 5: 版權 API（P3）
- **工時**: 4-5 小時
- **內容**: 浸宣字典（待授權）
- **優先級**: 待定 ⚠️

**總工時**: 22-33 小時  
**核心功能 (P0-P1)**: 14-19 小時

---

## 📝 快速開始

### 1. 閱讀完整計畫

```bash
# 開啟完整規劃文檔
code docs/5_api_enhancement/API_ENHANCEMENT_PLAN.md
```

### 2. 查看測試結果

```bash
# 執行 API 測試
python test_api_endpoints.py

# 查看測試結果文檔
code docs/5_api_enhancement/API_TEST_RESULTS.md
```

### 3. 開始實作

依照 Phase 順序實作:
1. Phase 1: Base URL 升級
2. Phase 2: 次經與使徒教父
3. Phase 3: 文章 API

---

## 🔗 相關資源

### 外部資源
- [FHL API 文檔](https://www.fhl.net/api/api.html)
- [聖經 API 端點](https://bible.fhl.net/json/)

### 內部文檔
- [原始規劃](../1_development/FHL_BIBLE_MCP_PLANNING.md)
- [API 實作](../../src/fhl_bible_mcp/api/endpoints.py)
- [開發指南](../1_development/DEVELOPER_GUIDE.md)

### 測試工具
- [API 測試腳本](../../test_api_endpoints.py)
- [單元測試](../../tests/)

---

## 📊 統計資訊

- **文檔數**: 2 個
- **測試端點**: 12 個
- **成功率**: 75%
- **未實作 API**: 10 個
- **預計工時**: 22-33 小時

---

## 🤝 貢獻指南

### 實作新 API

1. 在 `endpoints.py` 中添加方法
2. 在對應的 `tools/*.py` 中添加工具定義
3. 在 `server.py` 中註冊工具
4. 撰寫單元測試
5. 更新文檔

### 更新文檔

- 完成實作後更新本 README
- 在 API_ENHANCEMENT_PLAN.md 標記完成狀態
- 更新主要的 API.md 文檔

---

## ✅ 檢查清單

實作前檢查:
- [ ] 閱讀完整規劃文檔
- [ ] 執行測試腳本確認環境
- [ ] 了解 Phase 1 的重要性
- [ ] 確認開發環境設定

實作後檢查:
- [ ] 通過所有單元測試
- [ ] 更新 API.md 文檔
- [ ] 更新 EXAMPLES.md 範例
- [ ] 更新本 README 標記完成
- [ ] 提交 commit 並推送

---

**最後更新**: 2025年11月3日  
**文檔狀態**: ✅ 規劃完成  
**實作狀態**: ⏳ 等待開始

---

*此資料夾包含 FHL MCP Server API 功能擴展的完整規劃與測試文檔。*
