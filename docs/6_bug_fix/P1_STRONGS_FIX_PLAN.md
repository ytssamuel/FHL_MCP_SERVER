# P1 Strong's 功能修復計劃

**創建日期**: 2025-11-05  
**優先級**: P1（體驗改善，不影響核心功能）  
**預計版本**: v0.1.2

---

## 📋 問題概述

### 待修復項目

1. **lookup_strongs**: 返回 Strong's Number 00000 範例
2. **search_strongs_occurrences**: 返回 0 筆結果
3. **search_bible (greek_number模式)**: 參數驗證錯誤

---

## 🔍 問題詳細分析

### 問題 1: lookup_strongs 返回 00000 範例

**現象**:
```
lookup_strongs(G3056) 或 lookup_strongs(H430)
→ 返回 Strong's Number: 00000 的範例說明文字
```

**根因分析**:
1. **參數格式誤解**: 
   - 用戶傳入 `"G3056"` 或 `"H430"` (帶前綴的字串)
   - 實際 API 期望: `number=3056` (整數) + `testament="NT"` (約別)
   - G/H 前綴是文檔標記，不是 API 參數

2. **FHL API 行為**:
   - 當傳入無效參數時，API 返回 demo 資料 (Strong's 00000)
   - 這是 API 的預設行為，不是 bug

3. **當前實現問題**:
```python
async def lookup_strongs(
    number: int,
    testament: str = "NT",
    use_simplified: bool = False,
) -> Dict[str, Any]:
    # 參數類型已正確（整數），但缺少輸入驗證和轉換
```

**影響範圍**:
- MCP 工具 `lookup_strongs` 
- Resource `strongs://` URI
- Prompts 中的 Strong's 查詢

### 問題 2: search_strongs_occurrences 返回 0 筆

**現象**:
```
search_strongs_occurrences("G1344")
→ total_count: 0, results: []
```

**根因分析**:
1. **依賴問題 1**: 如果 `lookup_strongs` 獲取錯誤資料，後續搜尋也會失敗
2. **search_bible 整合問題**: 
```python
async def search_strongs_occurrences(number, testament, ...):
    strongs_info = await lookup_strongs(number, testament, ...)
    search_type = "hebrew_number" if testament == "OT" else "greek_number"
    
    search_results = await search_bible(
        query=str(number),  # 只傳入數字，沒有 G/H 前綴
        search_type=search_type,
        ...
    )
```

3. **FHL API 查詢格式**:
   - API 可能期望: `query="1344"` 或 `query="G1344"`
   - 需要測試確認正確格式

**影響範圍**:
- MCP 工具 `search_strongs_occurrences`
- Prompts 中的出現位置統計

### 問題 3: search_bible (greek_number) 參數驗證

**現象**:
```
search_bible(query="1344", search_type="greek_number")
→ 參數驗證錯誤或結果不符預期
```

**根因分析**:
1. **枚舉值已修正**: 之前的 `'greek'`/`'hebrew'` 已改為 `'greek_number'`/`'hebrew_number'`
2. **參數格式問題**: 
   - 是否需要 G/H 前綴？
   - FHL API 實際接受的格式是什麼？

---

## 🎯 修復策略

### 階段 1: 參數處理增強（核心修復）

#### 1.1 增強 lookup_strongs 的輸入處理

**目標**: 接受多種輸入格式，自動解析和轉換

**修改文件**: `src/fhl_bible_mcp/tools/strongs.py`

**新增功能**:
```python
def _parse_strongs_input(input_value: str | int, testament: str = None) -> tuple[int, str]:
    """
    解析 Strong's Number 輸入，支持多種格式
    
    支持格式:
    - 整數: 3056
    - 字串數字: "3056"
    - 帶前綴: "G3056", "H430"
    - 帶零: "03056", "G03056"
    
    Returns:
        (number: int, testament: str)
    """
    # 如果是整數，直接使用
    if isinstance(input_value, int):
        if testament is None:
            raise ValueError("整數輸入需要指定 testament 參數")
        return input_value, testament.upper()
    
    # 字串處理
    input_str = str(input_value).strip().upper()
    
    # 檢查前綴
    if input_str.startswith('G'):
        detected_testament = "NT"
        number_str = input_str[1:]
    elif input_str.startswith('H'):
        detected_testament = "OT"
        number_str = input_str[1:]
    else:
        # 純數字，使用提供的 testament
        if testament is None:
            raise ValueError("數字字串輸入需要指定 testament 參數")
        detected_testament = testament.upper()
        number_str = input_str
    
    # 移除前導零並轉換為整數
    try:
        number = int(number_str.lstrip('0') or '0')
    except ValueError:
        raise ValueError(f"無效的 Strong's Number: {input_value}")
    
    # 如果同時提供了 testament，確保一致
    if testament and testament.upper() != detected_testament:
        raise ValueError(
            f"前綴({detected_testament})與指定的 testament({testament})不一致"
        )
    
    return number, detected_testament
```

**修改 lookup_strongs**:
```python
async def lookup_strongs(
    number: int | str,  # 改為支持 str
    testament: str | None = None,  # 改為可選
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    查詢 Strong's 原文字典
    
    Args:
        number: Strong's 編號
            - 整數: 3056 (需要指定 testament)
            - 字串: "3056", "G3056", "H430"
        testament: 聖經約別 "OT" 或 "NT" (可選，如果 number 包含前綴)
        use_simplified: 是否使用簡體中文
    
    Examples:
        lookup_strongs(3056, "NT")          # 整數 + testament
        lookup_strongs("3056", "NT")        # 字串數字 + testament  
        lookup_strongs("G3056")             # 帶前綴，自動檢測
        lookup_strongs("H430")              # 帶前綴，自動檢測
    """
    # 解析輸入
    parsed_number, parsed_testament = _parse_strongs_input(number, testament)
    
    # 呼叫 API
    async with FHLAPIEndpoints() as api:
        response = await api.get_strongs_dictionary(
            number=parsed_number,
            testament=parsed_testament.lower(),
        )
    
    # ... 其餘邏輯不變 ...
```

#### 1.2 測試 FHL API 的 Strong's 搜尋格式

**目標**: 確定 search_bible 使用 greek_number/hebrew_number 時的正確查詢格式

**測試腳本** (`scripts/test_strongs_api.py`):
```python
#!/usr/bin/env python3
"""
測試 FHL API 的 Strong's Number 搜尋格式
"""
import asyncio
from src.fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test_strongs_search_formats():
    """測試不同的查詢格式"""
    async with FHLAPIEndpoints() as api:
        test_cases = [
            # Greek Strong's 1344 (δικαιόω - 稱義)
            ("1344", "greek_number", "nt"),
            ("G1344", "greek_number", "nt"),
            ("01344", "greek_number", "nt"),
            
            # Hebrew Strong's 430 (אֱלֹהִים - 神)
            ("430", "hebrew_number", "ot"),
            ("H430", "hebrew_number", "ot"),
            ("00430", "hebrew_number", "ot"),
        ]
        
        for query, search_type, scope in test_cases:
            print(f"\n測試: query='{query}', type={search_type}, scope={scope}")
            try:
                result = await api.search_bible(
                    query=query,
                    search_type=search_type,
                    scope=scope,
                    limit=5
                )
                print(f"✓ 結果數: {result.get('record_count', 0)}")
                if result.get('record_count', 0) > 0:
                    print(f"  首筆: {result['record'][0].get('bible_text', '')[:50]}")
            except Exception as e:
                print(f"✗ 錯誤: {e}")

if __name__ == "__main__":
    asyncio.run(test_strongs_search_formats())
```

#### 1.3 修復 search_strongs_occurrences

**根據測試結果修改**:
```python
async def search_strongs_occurrences(
    number: int | str,  # 支持多種格式
    testament: str | None = None,
    limit: int = 20,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    搜尋 Strong's 原文字在聖經中的所有出現位置
    
    Args:
        number: Strong's 編號 (3056, "3056", "G3056", "H430")
        testament: "OT" 或 "NT" (可選)
        limit: 最多返回筆數
        use_simplified: 是否使用簡體中文
    """
    # 解析輸入
    parsed_number, parsed_testament = _parse_strongs_input(number, testament)
    
    # 先取得字典定義
    strongs_info = await lookup_strongs(parsed_number, parsed_testament, use_simplified)
    
    # 使用原文編號搜尋聖經
    search_type = "hebrew_number" if parsed_testament == "OT" else "greek_number"
    
    # 根據 API 測試結果，決定查詢格式
    # 選項 1: 純數字
    query_str = str(parsed_number)
    # 選項 2: 帶前綴 (如果 API 需要)
    # query_str = f"{'H' if parsed_testament == 'OT' else 'G'}{parsed_number}"
    
    from .search import search_bible
    
    search_results = await search_bible(
        query=query_str,
        search_type=search_type,
        scope="ot" if parsed_testament == "OT" else "nt",
        limit=limit,
        use_simplified=use_simplified,
    )
    
    return {
        "strongs_info": strongs_info,
        "occurrences": {
            "total_count": search_results["total_count"],
            "showing": len(search_results["results"]),
            "results": search_results["results"],
        },
    }
```

### 階段 2: 文檔更新

#### 2.1 更新 API 文檔

**文件**: `docs/4_manuals/API.md`

**添加清晰的參數說明**:
```markdown
#### `lookup_strongs`

查詢 Strong's 原文字典。

**輸入參數**:

| 參數             | 類型       | 必填 | 預設值 | 說明                               |
| ---------------- | ---------- | ---- | ------ | ---------------------------------- |
| `number`         | int \| str | ✅    | -      | Strong's 編號（多種格式）          |
| `testament`      | string     | ❌    | -      | 約別：NT/OT（number 為整數時必填） |
| `use_simplified` | boolean    | ❌    | false  | 是否使用簡體中文                   |

**參數格式支持**:
- 整數: `3056` (必須指定 testament="NT")
- 字串數字: `"3056"` (必須指定 testament)
- 帶前綴（推薦）: `"G3056"`, `"H430"` (自動檢測 testament)
- 帶前導零: `"G03056"` (自動移除)

**使用範例**:
```
# 方式 1: 整數 + testament (推薦用於程式化調用)
lookup_strongs(3056, "NT")

# 方式 2: 帶前綴字串（推薦用於用戶輸入）
lookup_strongs("G3056")
lookup_strongs("H430")

# 方式 3: 字串數字 + testament
lookup_strongs("3056", "NT")
```
```

#### 2.2 更新 Prompts 文檔

**文件**: `docs/prompt_example/study_word_original.txt`

**更新使用說明**:
```
Strong's Number 格式說明：
- 推薦使用帶前綴格式：G3056（新約/希臘文），H430（舊約/希伯來文）
- 也支持：3056 + testament="NT"
- 前綴會自動判斷約別，更方便使用
```

### 階段 3: 測試驗證

#### 3.1 單元測試

**文件**: `tests/test_tools/test_strongs_enhanced.py`

```python
"""Strong's 工具增強功能測試"""
import pytest
from src.fhl_bible_mcp.tools.strongs import (
    _parse_strongs_input,
    lookup_strongs,
    search_strongs_occurrences
)

class TestStrongsInputParsing:
    """測試輸入解析功能"""
    
    def test_parse_integer_with_testament(self):
        """測試整數 + testament"""
        number, testament = _parse_strongs_input(3056, "NT")
        assert number == 3056
        assert testament == "NT"
    
    def test_parse_string_number_with_testament(self):
        """測試字串數字 + testament"""
        number, testament = _parse_strongs_input("3056", "NT")
        assert number == 3056
        assert testament == "NT"
    
    def test_parse_g_prefix(self):
        """測試 G 前綴"""
        number, testament = _parse_strongs_input("G3056")
        assert number == 3056
        assert testament == "NT"
    
    def test_parse_h_prefix(self):
        """測試 H 前綴"""
        number, testament = _parse_strongs_input("H430")
        assert number == 430
        assert testament == "OT"
    
    def test_parse_with_leading_zeros(self):
        """測試前導零"""
        number, testament = _parse_strongs_input("G03056")
        assert number == 3056
        assert testament == "NT"
    
    def test_parse_lowercase_prefix(self):
        """測試小寫前綴"""
        number, testament = _parse_strongs_input("g3056")
        assert number == 3056
        assert testament == "NT"
    
    def test_parse_conflict_testament(self):
        """測試前綴與 testament 衝突"""
        with pytest.raises(ValueError, match="不一致"):
            _parse_strongs_input("G3056", "OT")
    
    def test_parse_integer_without_testament(self):
        """測試整數缺少 testament"""
        with pytest.raises(ValueError, match="需要指定 testament"):
            _parse_strongs_input(3056)

@pytest.mark.asyncio
class TestLookupStrongsEnhanced:
    """測試 lookup_strongs 增強功能"""
    
    async def test_lookup_with_integer(self):
        """測試整數格式"""
        result = await lookup_strongs(25, "NT")
        assert result["strongs_number"] == "00025"
        assert "ἀγαπάω" in result["original_word"]
    
    async def test_lookup_with_g_prefix(self):
        """測試 G 前綴格式"""
        result = await lookup_strongs("G25")
        assert result["strongs_number"] == "00025"
        assert result["testament"] == "NT"
    
    async def test_lookup_with_h_prefix(self):
        """測試 H 前綴格式"""
        result = await lookup_strongs("H430")
        assert result["strongs_number"] == "00430"
        assert result["testament"] == "OT"

@pytest.mark.asyncio
class TestSearchStrongsOccurrencesEnhanced:
    """測試 search_strongs_occurrences 增強功能"""
    
    async def test_search_with_g_prefix(self):
        """測試 G 前綴搜尋"""
        result = await search_strongs_occurrences("G1344", limit=5)
        assert result["strongs_info"]["strongs_number"] == "01344"
        assert result["occurrences"]["total_count"] > 0
    
    async def test_search_with_integer(self):
        """測試整數格式搜尋"""
        result = await search_strongs_occurrences(1344, "NT", limit=5)
        assert result["occurrences"]["total_count"] > 0
```

#### 3.2 整合測試

**測試用例**:
1. ✅ lookup_strongs("G3056") → λόγος 完整詞條
2. ✅ lookup_strongs(3056, "NT") → 相同結果
3. ✅ lookup_strongs("H430") → אֱלֹהִים 完整詞條
4. ✅ search_strongs_occurrences("G1344") → 至少 30+ 筆（羅馬書等）
5. ✅ search_strongs_occurrences("H430") → 至少 2000+ 筆（創世記等）

---

## 📊 實施計劃

### 階段 1: 研究和測試（1-2 小時）

- [ ] 運行 `scripts/test_strongs_api.py` 測試 FHL API
- [ ] 確定正確的查詢格式（純數字 vs 帶前綴）
- [ ] 記錄測試結果

### 階段 2: 代碼實現（2-3 小時）

- [ ] 實現 `_parse_strongs_input()` 輔助函數
- [ ] 修改 `lookup_strongs()` 支持多格式輸入
- [ ] 修改 `search_strongs_occurrences()` 使用正確查詢格式
- [ ] 更新 MCP server 的工具定義
- [ ] 更新 Resource handler

### 階段 3: 測試（1-2 小時）

- [ ] 編寫單元測試 (`test_strongs_enhanced.py`)
- [ ] 運行所有測試確保無回歸
- [ ] 手動測試關鍵用例

### 階段 4: 文檔更新（1 小時）

- [ ] 更新 API.md
- [ ] 更新 Prompt 範例
- [ ] 更新 QUICK_REFERENCE.md
- [ ] 創建使用指南

### 階段 5: 發布（30 分鐘）

- [ ] 更新 CHANGELOG.md
- [ ] 更新版本號到 v0.1.2
- [ ] 創建 Git tag
- [ ] 更新 README.md

**預計總時間**: 5-8 小時

---

## 🎯 成功標準

### 功能目標

✅ **lookup_strongs** 支持所有格式:
- `lookup_strongs(3056, "NT")`  → 成功
- `lookup_strongs("3056", "NT")` → 成功
- `lookup_strongs("G3056")` → 成功
- `lookup_strongs("H430")` → 成功

✅ **search_strongs_occurrences** 返回正確結果:
- G1344 → 至少 30+ 筆
- H430 → 至少 2000+ 筆

✅ **錯誤處理**:
- 無效輸入 → 清晰錯誤訊息
- 衝突參數 → 明確指出問題

### 質量目標

- ✅ 100% 單元測試覆蓋
- ✅ 所有回歸測試通過
- ✅ 文檔完整更新
- ✅ 向後兼容（現有整數格式調用不受影響）

---

## 📝 技術決策

### 決策 1: 參數接受 Union[int, str]

**選擇**: 同時支持整數和字串

**理由**:
- 向後兼容現有代碼
- 方便用戶直接輸入 G/H 格式
- 靈活性更高

**實現**:
```python
number: int | str  # Python 3.10+ union syntax
```

### 決策 2: testament 參數改為可選

**選擇**: 當 number 包含前綴時，testament 可選

**理由**:
- 減少冗餘參數
- 更符合用戶直覺
- 前綴已明確指示約別

**實現**:
```python
testament: str | None = None
```

### 決策 3: 保留現有整數介面

**選擇**: 不破壞現有 API

**理由**:
- 向後兼容
- 測試代碼不需修改
- 程式化調用更高效

---

## 🔄 後續優化（v0.1.3+）

### 可選增強

1. **快取優化**:
   - Strong's 字典條目永久快取
   - 出現位置結果短期快取

2. **批量查詢**:
   - `lookup_strongs_batch([G25, G26, G27])`
   - 減少 API 調用次數

3. **搜尋結果分組**:
   - 按書卷分組統計
   - 顯示使用頻率分布

4. **語義搜尋**:
   - 根據詞義找相關 Strong's Number
   - 同義詞推薦

---

**修復負責人**: GitHub Copilot  
**審核狀態**: 待開始  
**追蹤連結**: [測試報告](./testing_report.md#待修復項目p1-優先級)
