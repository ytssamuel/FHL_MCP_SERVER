# Phase 2.3 Implementation Plan
## Footnotes Support (註腳支援) - READY TO IMPLEMENT ✅

**Status**: � 實作中  
**Priority**: P1 (核心功能)  
**Estimated Time**: 3-4 hours  
**Date**: 2025-11-04

---

## Executive Summary

Phase 2.3 實作 `rt.php` 註腳 API。經過詳細測試後成功找到正確用法！

### 測試結果 (更新)

✅ **API 完全可用！找到正確的參數組合**
- **關鍵發現**: 需要 `bid` (書卷ID) + `id` (註腳ID)
- **版本限制**: 僅 `tcv` (現代中文譯本) 有註腳資料
- **回應格式**: JSON (非文檔所述的 XML)
- **測試範圍**: ID 1-20 全部有效，每個都返回註腳內容

### API Response Format (Successful)

```json
{
  "status": "success",
  "record_count": 1,
  "version": "tcv",
  "engs": "Gen",
  "record": [{
    "id": 1,
    "text": "「太初，上帝創造天地。」或譯「太初，上帝創造天地的時候。」..."
  }]
}
```

### 成功範例

- 創世記註腳 #1: "「太初，上帝創造天地。」或譯..."
- 約翰福音註腳 #1: "「只有獨子」另有古卷作..."
- 羅馬書註腳 #1: "「因信而得以跟上帝有合宜關係的人將得生命」或譯..."

---

## 正確用法發現

### 1. 註腳資料確實不存在

**可能性**: ⭐⭐⭐⭐ (高)

**解釋**: 
- FHL API 可能沒有提供註腳資料
- 或註腳功能尚未完全實作
- 或僅特定版本/經文才有註腳

**證據**:
- 所有版本、所有書卷都返回 0 筆資料
- API 回應格式正常，但內容為空

### 2. 需要特殊參數或權限

**可能性**: ⭐⭐⭐ (中)

**解釋**:
- 可能需要特殊的 API key 或 token
- 可能需要未知的參數組合
- 可能需要登入或授權

**證據**:
- 測試了多種參數組合皆無效

### 3. API 端點不正確

**可能性**: ⭐ (低)

**解釋**:
- 註腳 API 可能不是 rt.php
- 可能有其他端點提供註腳功能

**證據**:
- API 文檔明確提到 rt.php
- HTTP 200 回應表示端點存在

---

## 調整後的策略

### 選項 A: 暫緩實作（推薦）

**理由**:
1. 沒有可用的測試資料
2. 無法驗證實作正確性
3. 可能浪費開發時間

**建議行動**:
1. ✅ 完成 API 測試腳本（已完成）
2. ✅ 記錄測試結果
3. ⏸️ 暫緩功能實作
4. 📧 聯繫 FHL 確認註腳 API 狀態
5. 📝 在文檔中標註「待確認」

**如果未來有資料**:
- 可以快速恢復實作
- 測試腳本已準備好

### 選項 B: 實作骨架（備用方案）

**理由**:
1. 為未來做準備
2. 保持 API 完整性
3. 便於測試和除錯

**實作內容**:
- 實作基本的 API 呼叫方法
- 處理空結果情況
- 新增相應的 MCP 工具
- **不包含**詳細的資料處理邏輯

**範例代碼**:
```python
async def get_footnote(
    self,
    book: str,
    chapter: int,
    verse: int,
    version: str = "unv"
) -> dict[str, Any]:
    """
    查詢經文註腳（實驗性功能）
    
    ⚠️ 注意: 此 API 目前可能返回空結果
    測試顯示大部分經文沒有註腳資料。
    
    API: rt.php
    Status: Experimental
    
    Args:
        book: 書卷名稱
        chapter: 章數
        verse: 節數
        version: 聖經版本
        
    Returns:
        註腳資料（可能為空）
    """
    params = {
        "chineses": book,
        "chap": chapter,
        "sec": verse,
        "VERSION": version,
        "gb": 0
    }
    
    return await self._cached_request(
        endpoint="rt.php",
        params=params,
        namespace="footnotes",
        strategy="verses"  # 7 day TTL
    )
```

### 選項 C: 跳過此 Phase

**理由**:
1. 節省開發時間
2. 聚焦於有實際資料的 API
3. 避免維護無用功能

**建議**:
- 直接進入 Phase 3 (文章 API)
- 或進入其他有價值的功能開發

---

## 建議決策

### 推薦方案: **選項 A (暫緩實作)**

**原因**:
1. ✅ 已完成 API 測試，了解當前狀況
2. ✅ 不浪費開發時間在無資料的功能上
3. ✅ 保持未來實作的可能性
4. ✅ 文檔記錄清楚，便於後續追蹤

**下一步行動**:
1. 📝 更新 API_ENHANCEMENT_PLAN.md，標註 rt.php 狀態
2. 📝 建立此規劃文檔，記錄測試結果
3. 🚀 **直接進入 Phase 3: 文章 API 整合**
4. 📧 （可選）發郵件給 FHL 詢問註腳 API 狀態

---

## 如果選擇實作（選項 B）

### Implementation Checklist

#### API Layer
- [ ] Add `get_footnote()` method to `endpoints.py`
- [ ] Handle empty responses gracefully
- [ ] Add appropriate cache strategy
- [ ] Include warning in docstring

#### Tools Layer
- [ ] Create `tools/footnotes.py`
- [ ] Define `get_footnote` tool
- [ ] Handle empty result display
- [ ] Add "experimental" label

#### Server Integration
- [ ] Register footnote tools
- [ ] Add to tool list
- [ ] Add to handler routing

#### Testing
- [ ] Create `tests/test_footnotes.py`
- [ ] Test empty response handling
- [ ] Test error scenarios
- [ ] Document expected behavior

#### Documentation
- [ ] Update API.md
- [ ] Mark as "Experimental"
- [ ] Document known limitations
- [ ] Provide examples

---

## Alternative: Skip to Phase 3

如果決定跳過 Phase 2.3，建議：

### Next Phase: Phase 3 - Article API Integration

**Why Phase 3 is better**:
1. ✅ **有實際資料**: 測試證實文章 API 有 8000+ 筆資料
2. ✅ **功能完整**: 可以查詢標題、作者、內容
3. ✅ **用戶價值高**: 提供豐富的神學文章資源
4. ✅ **實作難度適中**: 標準 JSON API，無特殊處理

**Phase 3 Features**:
- Article search by title, author, content
- Column (專欄) filtering
- Date filtering
- Result limiting (client-side)
- HTML content rendering

**Estimated Time**: 4-5 hours

---

## Test Results Summary

### Test Script Location
- `tests/api_validation/test_footnotes_api.py`
- `tests/api_validation/test_footnotes_api_extended.py`

### Test Coverage
- ✅ Basic query (book/chapter/verse)
- ✅ With/without VERSION parameter
- ✅ Different books (創, 太, 可, 路, 約, 羅)
- ✅ Different versions (unv, cunp, rcuv, tcv, ncv, niv, kjv)
- ✅ Chapter-only query
- ✅ Book ID support
- ✅ Different parameter names

### Results
- **All tests**: HTTP 200 OK
- **All tests**: `record_count: 0`
- **No errors**: API is working, just no data

---

## Conclusion

**建議**: ⏸️ **暫緩 Phase 2.3，直接進入 Phase 3**

**理由總結**:
1. rt.php API 運作正常，但無可用資料
2. 無法驗證實作正確性
3. 文章 API (Phase 3) 有實際資料且價值更高
4. 保持未來實作的可能性

**下一步**:
→ **開始 Phase 3: Article API Integration**

---

## Phase Progress Update

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1 | ✅ 完成 | Base URL upgraded to /api/ |
| Phase 2.1 | ✅ 完成 | Apocrypha support (qsub.php, sesub.php) |
| Phase 2.2 | ✅ 完成 | Apostolic Fathers support (qaf.php, seaf.php) |
| **Phase 2.3** | **⏸️ 暫緩** | **Footnotes (rt.php) - No data available** |
| Phase 3 | 📋 待開始 | Article API (json.php) - Ready to start |

---

*Document Status*: ✅ Complete  
*Decision Required*: User approval to skip to Phase 3  
*Date*: 2025-11-04
