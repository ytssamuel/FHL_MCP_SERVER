"""
API Validation Test for Footnotes (註腳) API

Tests rt.php endpoint before implementation to understand:
1. Response format (XML vs JSON)
2. Required parameters
3. Data structure
4. Book/chapter/verse support
"""

import asyncio
import httpx
import json
from typing import Any


async def test_footnotes_api():
    """Test rt.php API endpoint"""
    
    base_url = "https://bible.fhl.net/api/rt.php"
    
    print("=" * 70)
    print("註腳 API 測試 (rt.php)")
    print("=" * 70)
    
    # Test 1: Basic query with book/chapter/verse
    print("\n【測試 1】基本查詢 - 約翰福音 3:16")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type')}")
            print(f"  Content Length: {len(response.text)}")
            
            # Check if response is XML or JSON
            content_type = response.headers.get('content-type', '')
            if 'xml' in content_type.lower() or response.text.strip().startswith('<?xml'):
                print(f"  ⚠️  Response Format: XML")
                print(f"  Raw XML (前 500 字元):\n{response.text[:500]}")
            elif 'json' in content_type.lower():
                print(f"  ✅ Response Format: JSON")
                data = response.json()
                print(f"  JSON Data:\n{json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
            else:
                print(f"  ❓ Unknown Format")
                print(f"  Raw Content (前 300 字元):\n{response.text[:300]}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 2: Try with version parameter
    print("\n【測試 2】帶版本參數查詢")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "VERSION": "unv",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type')}")
            print(f"  Response Length: {len(response.text)}")
            print(f"  Response Preview (前 300 字元):\n{response.text[:300]}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 3: Try different book
    print("\n【測試 3】其他書卷 - 創世記 1:1")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "創",
                "chap": 1,
                "sec": 1,
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Has Content: {len(response.text) > 0}")
            print(f"  Content Length: {len(response.text)}")
            
            if len(response.text) > 0:
                print(f"  ✅ 有註腳資料")
                print(f"  Preview:\n{response.text[:400]}")
            else:
                print(f"  ⚠️  無註腳資料")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 4: Try without verse (chapter only)
    print("\n【測試 4】只指定章節（不指定節數）")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "chineses": "約",
                "chap": 3,
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Content Length: {len(response.text)}")
            
            if response.status_code == 200 and len(response.text) > 0:
                print(f"  ✅ 可以查詢整章註腳")
            else:
                print(f"  ⚠️  需要指定節數")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 5: Check for book ID support
    print("\n【測試 5】使用書卷 ID")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "book": 43,  # John
                "chap": 3,
                "sec": 16,
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Content Length: {len(response.text)}")
            
            if response.status_code == 200 and len(response.text) > 0:
                print(f"  ✅ 支援書卷 ID")
            else:
                print(f"  ⚠️  可能不支援書卷 ID")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 6: Test multiple verses that might have footnotes
    print("\n【測試 6】測試多個可能有註腳的經文")
    print("-" * 70)
    
    test_verses = [
        ("太", 1, 1, "馬太福音 1:1"),
        ("可", 1, 1, "馬可福音 1:1"),
        ("路", 1, 1, "路加福音 1:1"),
        ("約", 1, 1, "約翰福音 1:1"),
        ("羅", 1, 1, "羅馬書 1:1"),
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for book, chap, sec, name in test_verses:
            try:
                params = {
                    "chineses": book,
                    "chap": chap,
                    "sec": sec,
                    "gb": 0
                }
                response = await client.get(base_url, params=params)
                has_footnotes = len(response.text) > 100
                status = "✅" if has_footnotes else "⚠️ "
                print(f"  {status} {name}: {len(response.text)} bytes")
                
            except Exception as e:
                print(f"  ❌ {name}: Error - {e}")
    
    print("\n" + "=" * 70)
    print("測試完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_footnotes_api())
