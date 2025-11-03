# API 參數修正報告

**修正日期**: 2025年11月2日  
**問題**: `search_type` 參數值不一致導致 API 呼叫錯誤

---

## 🐛 問題描述

在測試時發現部分 API 呼叫出現錯誤：

```
錯誤: Invalid parameter 'search_type': greek - Must be 'keyword', 'greek_number', or 'hebrew_number'
```

**根本原因**：專案中對 `search_type` 參數的值定義不一致：
- MCP Server 定義使用：`["keyword", "greek", "hebrew"]`
- API Endpoints 期望：`["keyword", "greek_number", "hebrew_number"]`
- Tools 層混用：`"greek"` 和 `"hebrew"`

---

## 🔍 問題分析

### 受影響的檔案

1. **src/fhl_bible_mcp/server.py** (Line 194)
   - MCP 工具 `search_bible` 的 inputSchema 定義錯誤
   - 使用了 `["keyword", "greek", "hebrew"]`

2. **src/fhl_bible_mcp/tools/search.py** (Lines 52-60)
   - 驗證邏輯使用錯誤的值
   - `search_type_map` 定義為 `{"keyword": 0, "greek": 1, "hebrew": 2}`

3. **src/fhl_bible_mcp/tools/strongs.py** (Line 191)
   - `search_strongs_occurrences` 函數使用錯誤的值
   - 使用了 `"hebrew"` 和 `"greek"`

4. **tests/test_tools/test_search_tools.py** (Lines 95, 97, 124, 126)
   - 測試案例使用錯誤的值

### 正確的值

根據 API 文檔和 `endpoints.py` 的實作，正確的值應該是：
- ✅ `"keyword"` - 關鍵字搜尋
- ✅ `"greek_number"` - 希臘文編號搜尋（Strong's Number）
- ✅ `"hebrew_number"` - 希伯來文編號搜尋（Strong's Number）

---

## ✅ 修正內容

### 1. server.py

**修正前**：
```python
"search_type": {"type": "string", "enum": ["keyword", "greek", "hebrew"]}
```

**修正後**：
```python
"search_type": {
    "type": "string", 
    "enum": ["keyword", "greek_number", "hebrew_number"],
    "description": "搜尋類型：keyword(關鍵字)/greek_number(希臘文編號)/hebrew_number(希伯來文編號)"
}
```

### 2. tools/search.py

**修正前**：
```python
search_type_map = {
    "keyword": 0,
    "greek": 1,
    "hebrew": 2,
}
# 錯誤訊息：應為 'keyword', 'greek', 或 'hebrew'
```

**修正後**：
```python
search_type_map = {
    "keyword": 0,
    "greek_number": 1,
    "hebrew_number": 2,
}
# 錯誤訊息：應為 'keyword', 'greek_number', 或 'hebrew_number'
```

同時更新了文檔註釋：
```python
search_type: 搜尋類型
    - "keyword": 關鍵字搜尋
    - "greek_number": 希臘文編號搜尋
    - "hebrew_number": 希伯來文編號搜尋
```

### 3. tools/strongs.py

**修正前**：
```python
search_type = "hebrew" if testament.upper() == "OT" else "greek"
```

**修正後**：
```python
search_type = "hebrew_number" if testament.upper() == "OT" else "greek_number"
```

### 4. tests/test_tools/test_search_tools.py

**修正前**：
```python
# test_search_bible_greek_strong
result = await search_bible(query="G3056", search_type="greek", scope="nt")
assert result["search_type"] == "greek"

# test_search_bible_hebrew_strong
result = await search_bible(query="H1254", search_type="hebrew", scope="ot")
assert result["search_type"] == "hebrew"
```

**修正後**：
```python
# test_search_bible_greek_strong
result = await search_bible(query="G3056", search_type="greek_number", scope="nt")
assert result["search_type"] == "greek_number"

# test_search_bible_hebrew_strong
result = await search_bible(query="H1254", search_type="hebrew_number", scope="ot")
assert result["search_type"] == "hebrew_number"
```

---

## 🧪 測試驗證

### 測試結果

```bash
$ python -m pytest tests/test_tools/test_search_tools.py::test_search_bible_greek_strong \
    tests/test_tools/test_search_tools.py::test_search_bible_hebrew_strong -v

========================== test session starts ==========================
tests/test_tools/test_search_tools.py::test_search_bible_greek_strong PASSED [ 50%]
tests/test_tools/test_search_tools.py::test_search_bible_hebrew_strong PASSED [100%]

=========================== 2 passed in 2.50s ===========================
```

✅ **測試通過！**

---

## 📊 影響範圍

### 修正的檔案
- ✅ `src/fhl_bible_mcp/server.py` - MCP 工具定義
- ✅ `src/fhl_bible_mcp/tools/search.py` - 搜尋工具邏輯
- ✅ `src/fhl_bible_mcp/tools/strongs.py` - Strong's 工具邏輯
- ✅ `tests/test_tools/test_search_tools.py` - 測試案例

### 影響的功能
1. **search_bible** - 聖經搜尋工具（MCP）
2. **search_strongs_occurrences** - Strong's 編號出現位置查詢

### 向後相容性
⚠️ **Breaking Change** - 這是一個不相容的變更

如果有外部工具或腳本使用以下參數值，需要更新：
- `"greek"` → `"greek_number"`
- `"hebrew"` → `"hebrew_number"`

---

## 🎯 根本原因分析

### 為什麼會發生？

1. **定義來源不一致**
   - API 層（endpoints.py）從一開始就定義為 `_number` 後綴
   - MCP 層（server.py）簡化為不帶後綴
   - Tools 層同時存在兩種用法

2. **缺乏統一的常數定義**
   - 沒有集中定義這些列舉值
   - 各層各自定義導致不一致

3. **測試覆蓋不足**
   - 雖有測試但使用了錯誤的 mock 值
   - 沒有端到端測試驗證完整流程

---

## 💡 預防措施

### 建議改進

1. **集中定義常數**
   ```python
   # 建議在 utils/constants.py 中定義
   class SearchType:
       KEYWORD = "keyword"
       GREEK_NUMBER = "greek_number"
       HEBREW_NUMBER = "hebrew_number"
   ```

2. **類型檢查**
   - 使用 Literal 類型提示
   ```python
   from typing import Literal
   
   SearchTypeValue = Literal["keyword", "greek_number", "hebrew_number"]
   ```

3. **更完整的測試**
   - 添加端到端測試
   - 測試實際的 API 呼叫流程

4. **文檔同步**
   - 確保 API.md 文檔與代碼一致
   - 在 CHANGELOG 中記錄此變更

---

## 📝 後續行動

### 已完成
- ✅ 修正所有相關代碼
- ✅ 更新測試案例
- ✅ 驗證測試通過

### 待辦事項
- [ ] 運行完整測試套件確保無其他破壞
- [ ] 更新 API 文檔（如有需要）
- [ ] 更新 CHANGELOG
- [ ] 考慮是否需要提供遷移指南

---

## 🔗 相關文件

- API 文檔：`docs/4_manuals/API.md`
- 測試檔案：`tests/test_tools/test_search_tools.py`
- API 實作：`src/fhl_bible_mcp/api/endpoints.py`

---

**修正狀態**: ✅ **已完成**  
**測試狀態**: ✅ **通過**  
**文檔狀態**: 📝 **待更新**

---

*感謝回報此問題！這個修正確保了 API 參數的一致性，提升了系統的穩定性。*
