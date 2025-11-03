"""
Extended Footnotes API Testing

Test different parameter combinations to find working footnotes.
"""

import asyncio
import httpx
import json


async def test_footnotes_extended():
    """Test rt.php with different parameters"""
    
    base_url = "https://bible.fhl.net/api/rt.php"
    
    print("=" * 70)
    print("註腳 API 擴展測試")
    print("=" * 70)
    
    # Test different versions
    print("\n【測試 1】測試不同版本")
    print("-" * 70)
    
    versions = ["unv", "cunp", "rcuv", "tcv", "ncv", "niv", "kjv"]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for version in versions:
            try:
                params = {
                    "chineses": "約",
                    "chap": 1,
                    "sec": 1,
                    "VERSION": version,
                    "gb": 0
                }
                response = await client.get(base_url, params=params)
                data = response.json()
                count = data.get("record_count", 0)
                has_notes = count > 0
                status = "✅" if has_notes else "⚠️ "
                print(f"  {status} Version '{version}': record_count={count}")
                
                if has_notes:
                    print(f"      Data: {json.dumps(data, ensure_ascii=False, indent=6)[:300]}")
                    
            except Exception as e:
                print(f"  ❌ Version '{version}': Error - {e}")
    
    # Test 2: Try without gb parameter
    print("\n【測試 2】不使用 gb 參數")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "約",
                "chap": 1,
                "sec": 1
            }
            response = await client.get(base_url, params=params)
            data = response.json()
            print(f"  Record Count: {data.get('record_count', 0)}")
            print(f"  Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 3: Try with different parameter names
    print("\n【測試 3】測試不同的參數名稱")
    print("-" * 70)
    
    param_combinations = [
        {"book": "約", "chapter": 1, "verse": 1},
        {"chineses": "約", "chapter": 1, "verse": 1},
        {"chineses": "約", "chap": 1, "verse": 1},
        {"chineses": "約", "chap": 1, "sec": 1, "gb": 0},
        {"engs": "John", "chap": 1, "sec": 1},
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, params in enumerate(param_combinations, 1):
            try:
                response = await client.get(base_url, params=params)
                data = response.json()
                count = data.get("record_count", 0)
                print(f"  Test {idx}: {params}")
                print(f"    → record_count={count}")
                
            except Exception as e:
                print(f"  Test {idx}: Error - {e}")
    
    # Test 4: Check actual FHL website usage
    print("\n【測試 4】檢查 FHL 網站實際用法")
    print("-" * 70)
    print("  提示：註腳功能可能需要特定的版本或參數組合")
    print("  建議：查看 FHL 網站原始碼以了解正確的 API 調用方式")
    
    # Test 5: Try with estudy parameter (some APIs use this)
    print("\n【測試 5】測試 estudy 參數")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "約",
                "chap": 1,
                "sec": 1,
                "estudy": "rt",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            data = response.json()
            print(f"  Record Count: {data.get('record_count', 0)}")
            print(f"  Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("擴展測試完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_footnotes_extended())
