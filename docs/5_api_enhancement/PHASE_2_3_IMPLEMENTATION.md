# Phase 2.3 Implementation Plan
## Footnotes Support (註腳支援) ✅ READY TO IMPLEMENT

**Status**: 🚀 實作中  
**Priority**: P1 (核心功能)  
**Estimated Time**: 3-4 hours  
**Date**: 2025-11-04  
**Updated**: 2025-11-04 (找到正確用法)

---

## Executive Summary

Phase 2.3 實作 `rt.php` 註腳 API。經過詳細測試後**成功找到正確用法**！

### 關鍵突破 🎉

✅ **API 完全可用！** 找到正確的參數組合
- **關鍵發現**: 需要 `bid` (書卷ID) + `id` (註腳ID)
- **版本限制**: 僅 `tcv` (現代中文譯本) 有註腳資料
- **回應格式**: JSON (非文檔所述的 XML)
- **測試範圍**: ID 1-20 全部有效，每個都返回註腳內容

### 測試結果對比

#### ❌ 初次測試（失敗）
```
參數: chineses=約&chap=3&sec=16
結果: record_count = 0
```

#### ✅ 詳細測試（成功）
```
參數: bid=43&id=1
結果: record_count = 1
回應: {
  "status": "success",
  "record_count": 1,
  "version": "tcv",
  "engs": "John",
  "record": [{
    "id": 1,
    "text": "「只有獨子」另有古卷作「只有與上帝相同的獨子」。"
  }]
}
```

---

## API 正確用法

### 必需參數

| 參數 | 類型 | 說明 | 範例 |
|------|------|------|------|
| `bid` | integer | 書卷編號 (1-66) | 1=創世記, 43=約翰福音 |
| `id` | integer | 註腳編號 | 1, 2, 3, ... |

### 可選參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `version` | string | `tcv` | 聖經版本（**僅 tcv 有註腳**） |
| `gb` | integer | 0 | 繁簡體選擇 (0=繁體, 1=簡體) |
| `chap` | integer | - | 章數（可選，不影響結果） |

### 成功範例

```python
# 範例 1: 創世記註腳 #1
GET /api/rt.php?bid=1&id=1&version=tcv&gb=0
→ "「太初，上帝創造天地。」或譯「太初，上帝創造天地的時候。」..."

# 範例 2: 約翰福音註腳 #10
GET /api/rt.php?bid=43&id=10&version=tcv&gb=0
→ "有些古卷沒有括弧內這一段；另有些古卷把這一段放在約翰福音21.24之後..."

# 範例 3: 羅馬書註腳 #1
GET /api/rt.php?bid=45&id=1&version=tcv&gb=0
→ "「因信而得以跟上帝有合宜關係的人將得生命」或譯..."
```

---

## 版本限制

### 測試結果

| 版本 | 是否有註腳 | record_count |
|------|-----------|--------------|
| `tcv` | ✅ 有 | > 0 |
| `unv` | ❌ 無 | 0 |
| `cunp` | ❌ 無 | 0 |
| `rcuv` | ❌ 無 | 0 |
| `ncv` | ❌ 無 | 0 |

**結論**: 註腳功能專門為 **TCV (台灣聖經公會現代中文譯本)** 設計

---

## 實作策略

### Phase 2.3 Implementation Steps

#### Step 1: API 端點層 (endpoints.py)

**新增方法**:
```python
async def get_footnote(
    self,
    book_id: int,
    footnote_id: int,
    version: str = "tcv",
    use_simplified: bool = False
) -> dict[str, Any]:
    """
    查詢聖經經文註腳（僅 TCV 版本）
    
    API: rt.php
    Version: tcv only
    
    Args:
        book_id: 書卷編號 (1-66)
        footnote_id: 註腳編號
        version: 聖經版本 (default: tcv, 僅 tcv 有註腳)
        use_simplified: 是否使用簡體中文
        
    Returns:
        註腳資料
        
    Example:
        >>> result = await api.get_footnote(book_id=1, footnote_id=1)
        >>> print(result["record"][0]["text"])
        「太初，上帝創造天地。」或譯...
    """
    params = {
        "bid": book_id,
        "id": footnote_id,
        "version": version,
        "gb": 1 if use_simplified else 0
    }
    
    return await self._cached_request(
        endpoint="rt.php",
        params=params,
        namespace="footnotes",
        strategy="verses"  # 7 day TTL
    )
```

**快取策略**: 
- Namespace: `footnotes`
- Strategy: `verses` (7 days TTL)
- 理由: 註腳內容不會變動

#### Step 2: 工具定義層 (tools/footnotes.py)

**工具列表**:
1. `get_bible_footnote` - 查詢特定註腳
2. `list_footnotes_for_book` - 列出書卷的所有註腳（可選）

**範例代碼**:
```python
"""
Footnotes (註腳) Tools for MCP Server

Provides tools for querying Bible footnotes (TCV version only).
"""

import logging
from typing import Any

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

logger = logging.getLogger(__name__)


def get_footnotes_tool_definitions() -> list[dict[str, Any]]:
    """Get MCP tool definitions for footnotes operations."""
    return [
        {
            "name": "get_bible_footnote",
            "description": (
                "查詢聖經經文註腳（僅限 TCV 現代中文譯本）。\n"
                "註腳提供原文翻譯的不同選擇、古卷差異、或其他重要說明。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "書卷編號 (1-66)",
                        "minimum": 1,
                        "maximum": 66
                    },
                    "footnote_id": {
                        "type": "integer",
                        "description": "註腳編號（每個書卷有自己的編號系統）",
                        "minimum": 1
                    },
                    "use_simplified": {
                        "type": "boolean",
                        "description": "是否使用簡體中文"
                    }
                },
                "required": ["book_id", "footnote_id"]
            }
        }
    ]


async def handle_get_bible_footnote(
    api_client: FHLAPIEndpoints,
    arguments: dict[str, Any]
) -> list[dict[str, Any]]:
    """Handle get_bible_footnote tool call."""
    try:
        book_id = arguments["book_id"]
        footnote_id = arguments["footnote_id"]
        use_simplified = arguments.get("use_simplified", False)
        
        result = await api_client.get_footnote(
            book_id=book_id,
            footnote_id=footnote_id,
            use_simplified=use_simplified
        )
        
        if result.get("status") == "success":
            record_count = result.get("record_count", 0)
            version = result.get("version", "tcv")
            engs = result.get("engs", "")
            
            if record_count > 0:
                record = result["record"][0]
                footnote_text = record.get("text", "")
                
                response = (
                    f"**聖經註腳**\n\n"
                    f"版本: {version} (現代中文譯本)\n"
                    f"書卷: {engs}\n"
                    f"註腳 #{footnote_id}:\n\n"
                    f"{footnote_text}"
                )
            else:
                response = f"❌ 找不到註腳 #{footnote_id}（書卷 ID: {book_id}）"
            
            return [{"type": "text", "text": response}]
        else:
            error_msg = result.get("error", "未知錯誤")
            return [{"type": "text", "text": f"❌ 查詢失敗: {error_msg}"}]
            
    except Exception as e:
        logger.error(f"Error in get_bible_footnote: {e}", exc_info=True)
        return [{"type": "text", "text": f"❌ 錯誤: {str(e)}"}]
```

#### Step 3: 伺服器註冊 (server.py)

**更新項目**:
1. Import footnotes tools
2. Add to `list_tools()` dynamic loading
3. Add handler in `call_tool()`
4. Update tool count logging

```python
# In server.py

from fhl_bible_mcp.tools.footnotes import (
    get_footnotes_tool_definitions,
    handle_get_bible_footnote,
)

# In list_tools()
] + [
    # Dynamically add Footnotes tools
    Tool(
        name=tool["name"],
        description=tool["description"],
        inputSchema=tool["inputSchema"]
    )
    for tool in get_footnotes_tool_definitions()
]

# In call_tool()
elif name == "get_bible_footnote":
    result = await handle_get_bible_footnote(self.endpoints, arguments)
    return result
```

#### Step 4: 單元測試 (test_footnotes.py)

**測試項目**:
```python
"""
Tests for Footnotes APIs

Tests the footnote query functionality (rt.php).
"""

import pytest
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


@pytest.fixture
def api_client():
    """Create API client fixture"""
    return FHLAPIEndpoints()


@pytest.mark.asyncio
class TestFootnotesAPI:
    """Test Footnotes API endpoints"""
    
    async def test_get_footnote_success(self, api_client):
        """Test querying a valid footnote"""
        result = await api_client.get_footnote(
            book_id=1,  # Genesis
            footnote_id=1
        )
        
        assert result["status"] == "success"
        assert result["record_count"] == 1
        assert result["version"] == "tcv"
        assert "record" in result
        assert len(result["record"]) == 1
        assert "text" in result["record"][0]
        assert "id" in result["record"][0]
    
    async def test_get_footnote_multiple_books(self, api_client):
        """Test footnotes from different books"""
        test_cases = [
            (1, 1, "Gen"),    # Genesis
            (43, 1, "John"),  # John
            (45, 1, "Rom"),   # Romans
        ]
        
        for book_id, footnote_id, expected_engs in test_cases:
            result = await api_client.get_footnote(
                book_id=book_id,
                footnote_id=footnote_id
            )
            
            assert result["status"] == "success"
            assert result["record_count"] == 1
            assert result["engs"] == expected_engs
    
    async def test_get_footnote_simplified(self, api_client):
        """Test footnote with simplified Chinese"""
        result = await api_client.get_footnote(
            book_id=1,
            footnote_id=1,
            use_simplified=True
        )
        
        assert result["status"] == "success"
        assert result["record_count"] == 1
    
    async def test_get_footnote_invalid_id(self, api_client):
        """Test querying a non-existent footnote"""
        result = await api_client.get_footnote(
            book_id=1,
            footnote_id=999999
        )
        
        # Should still return success but with 0 records
        assert result["status"] == "success"
        assert result["record_count"] == 0
```

---

## Implementation Checklist

### API Layer
- [ ] Add `get_footnote()` method to `endpoints.py`
- [ ] Add proper docstring with examples
- [ ] Use correct cache strategy (7-day TTL)
- [ ] Handle TCV-only limitation

### Tools Layer
- [ ] Create `tools/footnotes.py`
- [ ] Define `get_bible_footnote` tool
- [ ] Implement handler function
- [ ] Add comprehensive error handling

### Server Integration
- [ ] Import footnotes tools in `server.py`
- [ ] Add to dynamic tool list
- [ ] Add handler routing in `call_tool()`
- [ ] Update tool count (24 → 25 functions)

### Testing
- [ ] Create `tests/test_footnotes.py`
- [ ] Test successful queries
- [ ] Test multiple books
- [ ] Test simplified Chinese
- [ ] Test invalid footnote IDs
- [ ] Achieve 100% test pass rate

### Documentation
- [ ] Update `PHASE_2_3_PLANNING.md` with success
- [ ] Create `PHASE_2_3_COMPLETION_REPORT.md`
- [ ] Document TCV-only limitation
- [ ] Provide usage examples

---

## Known Limitations

### 1. Version Limitation ⚠️

**Issue**: Only TCV version has footnotes  
**Impact**: Users of other versions cannot use this feature  
**Workaround**: Document clearly in tool description  
**Example**:
```
✅ TCV (tcv): 有註腳
❌ UNV (unv): 無註腳
❌ CUNP (cunp): 無註腳
```

### 2. Footnote ID Discovery

**Issue**: No API to list available footnote IDs for a book  
**Impact**: Users need to know footnote IDs in advance  
**Workaround**: 
- Start from ID 1 and increment
- Handle `record_count: 0` gracefully
- Provide guidance in documentation

### 3. No Chapter/Verse Mapping

**Issue**: API doesn't return which verse the footnote belongs to  
**Impact**: Cannot automatically show footnotes when displaying verses  
**Workaround**: Footnotes are accessed separately, not inline

---

## Expected Outcomes

### Features Delivered
1. ✅ Query footnotes by book ID and footnote ID
2. ✅ Support simplified/traditional Chinese
3. ✅ Caching with 7-day TTL
4. ✅ Comprehensive error handling
5. ✅ MCP tool integration

### Test Coverage
- Target: 100% pass rate
- Tests: 4-5 comprehensive tests
- Coverage: Success cases, edge cases, error handling

### Performance
- API response: ~300-500ms
- Cache hit rate: Expected 80-90% (rarely changing content)

---

## Timeline

| Task | Estimated Time | Status |
|------|----------------|--------|
| Update planning doc | 15 min | ✅ Done |
| Implement API layer | 30 min | 📋 Next |
| Create tools layer | 45 min | Pending |
| Server integration | 20 min | Pending |
| Unit tests | 30 min | Pending |
| Documentation | 30 min | Pending |
| **Total** | **~3 hours** | **In Progress** |

---

## Next Steps

1. ✅ Update `PHASE_2_3_PLANNING.md` (Done)
2. 📋 Implement `get_footnote()` in `endpoints.py` (Next)
3. Create `tools/footnotes.py`
4. Register tools in `server.py`
5. Create unit tests
6. Generate completion report

---

## Success Criteria

- [x] API tests show successful responses
- [ ] API method implemented with proper types
- [ ] MCP tool registered and functional
- [ ] Unit tests pass at 100%
- [ ] Documentation complete
- [ ] No breaking changes to existing code

---

*Document Status*: ✅ Updated with successful test results  
*Ready to Implement*: YES  
*Date*: 2025-11-04
