"""
Detailed Footnotes API Testing based on official documentation

According to FHL API docs:
- rt.php lists Bible verse footnotes
- Required: bid (book ID) + id (footnote ID)
- Optional: chap (chapter), version, gb
- Response format: XML
"""

import asyncio
import httpx
import xml.etree.ElementTree as ET
from typing import Any


async def test_footnotes_detailed():
    """Test rt.php with correct parameters based on documentation"""
    
    base_url = "https://bible.fhl.net/api/rt.php"
    
    print("=" * 70)
    print("註腳 API 詳細測試 (基於官方文檔)")
    print("=" * 70)
    print("\n根據文檔，rt.php 需要:")
    print("  - bid: 書卷編號")
    print("  - id: 註腳編號 ⭐ (關鍵參數)")
    print("  - version: 版本 (default: tcv)")
    print("  - gb: 繁簡體 (default: 0)")
    print("  - chap: 章 (可選)")
    print()
    
    # Test 1: Try with book ID and footnote ID
    print("【測試 1】使用書卷 ID + 註腳 ID")
    print("-" * 70)
    
    # Try different footnote IDs
    test_cases = [
        (1, 1, "創世記, 註腳 #1"),
        (1, 2, "創世記, 註腳 #2"),
        (1, 100, "創世記, 註腳 #100"),
        (43, 1, "約翰福音, 註腳 #1"),
        (43, 10, "約翰福音, 註腳 #10"),
        (45, 1, "羅馬書, 註腳 #1"),
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for bid, footnote_id, desc in test_cases:
            try:
                params = {
                    "bid": bid,
                    "id": footnote_id,
                    "version": "tcv",
                    "gb": 0
                }
                response = await client.get(base_url, params=params)
                
                # Check if response is XML
                content_type = response.headers.get('content-type', '')
                is_xml = 'xml' in content_type.lower() or response.text.strip().startswith('<?xml')
                
                if is_xml:
                    # Try to parse XML
                    try:
                        root = ET.fromstring(response.text)
                        record_count = root.find('.//record_count')
                        count = int(record_count.text) if record_count is not None else 0
                        
                        if count > 0:
                            print(f"  ✅ {desc}: 找到 {count} 筆註腳")
                            # Show footnote details
                            for record in root.findall('.//record'):
                                footnote_id = record.find('id')
                                text = record.find('text')
                                if footnote_id is not None and text is not None:
                                    print(f"      註腳 #{footnote_id.text}: {text.text[:100]}...")
                        else:
                            print(f"  ⚠️  {desc}: record_count = {count}")
                    except ET.ParseError as e:
                        print(f"  ❌ {desc}: XML 解析失敗 - {e}")
                        print(f"      Response: {response.text[:200]}")
                else:
                    # Try JSON
                    try:
                        data = response.json()
                        count = data.get('record_count', 0)
                        if count > 0:
                            print(f"  ✅ {desc}: 找到 {count} 筆註腳")
                            print(f"      Data: {data}")
                        else:
                            print(f"  ⚠️  {desc}: record_count = {count}")
                    except:
                        print(f"  ❓ {desc}: Unknown format")
                        print(f"      Response: {response.text[:200]}")
                        
            except Exception as e:
                print(f"  ❌ {desc}: Error - {e}")
    
    # Test 2: Try with version parameter
    print("\n【測試 2】測試不同版本的註腳")
    print("-" * 70)
    
    versions = ["tcv", "unv", "cunp", "rcuv", "ncv"]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for version in versions:
            try:
                params = {
                    "bid": 43,  # 約翰福音
                    "id": 1,
                    "version": version,
                    "gb": 0
                }
                response = await client.get(base_url, params=params)
                
                # Try to get record_count
                if 'xml' in response.headers.get('content-type', '').lower() or response.text.strip().startswith('<?xml'):
                    try:
                        root = ET.fromstring(response.text)
                        record_count = root.find('.//record_count')
                        count = int(record_count.text) if record_count is not None else 0
                        status = "✅" if count > 0 else "⚠️ "
                        print(f"  {status} Version '{version}': record_count = {count}")
                    except:
                        print(f"  ❌ Version '{version}': XML 解析失敗")
                else:
                    try:
                        data = response.json()
                        count = data.get('record_count', 0)
                        status = "✅" if count > 0 else "⚠️ "
                        print(f"  {status} Version '{version}': record_count = {count}")
                    except:
                        print(f"  ❓ Version '{version}': Unknown format")
                        
            except Exception as e:
                print(f"  ❌ Version '{version}': Error - {e}")
    
    # Test 3: Try with chapter parameter
    print("\n【測試 3】加入章節參數")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "bid": 43,  # 約翰福音
                "id": 1,
                "chap": 3,
                "version": "tcv",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            
            if 'xml' in response.headers.get('content-type', '').lower() or response.text.strip().startswith('<?xml'):
                try:
                    root = ET.fromstring(response.text)
                    record_count = root.find('.//record_count')
                    count = int(record_count.text) if record_count is not None else 0
                    print(f"  Record Count: {count}")
                    if count > 0:
                        print(f"  ✅ 找到註腳資料")
                        print(f"  XML Response:\n{response.text[:500]}")
                    else:
                        print(f"  ⚠️  無註腳資料")
                except ET.ParseError:
                    print(f"  Response: {response.text[:300]}")
            else:
                try:
                    data = response.json()
                    print(f"  Record Count: {data.get('record_count', 0)}")
                    print(f"  Response: {data}")
                except:
                    print(f"  Response: {response.text[:300]}")
                    
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 4: Try a range of footnote IDs
    print("\n【測試 4】測試註腳 ID 範圍 (1-20)")
    print("-" * 70)
    
    found_count = 0
    async with httpx.AsyncClient(timeout=30.0) as client:
        for footnote_id in range(1, 21):
            try:
                params = {
                    "bid": 43,  # 約翰福音
                    "id": footnote_id,
                    "version": "tcv",
                    "gb": 0
                }
                response = await client.get(base_url, params=params)
                
                count = 0
                if 'xml' in response.headers.get('content-type', '').lower() or response.text.strip().startswith('<?xml'):
                    try:
                        root = ET.fromstring(response.text)
                        record_count = root.find('.//record_count')
                        count = int(record_count.text) if record_count is not None else 0
                    except:
                        pass
                else:
                    try:
                        data = response.json()
                        count = data.get('record_count', 0)
                    except:
                        pass
                
                if count > 0:
                    found_count += 1
                    print(f"  ✅ 註腳 ID #{footnote_id}: 找到 {count} 筆")
            except Exception as e:
                print(f"  ❌ 註腳 ID #{footnote_id}: Error - {e}")
        
        print(f"\n  總結: 在 1-20 範圍內找到 {found_count} 個有效的註腳 ID")
    
    # Test 5: Check response format
    print("\n【測試 5】檢查回應格式")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "bid": 1,
                "id": 1,
                "version": "tcv",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            
            print(f"  HTTP Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type')}")
            print(f"  Content Length: {len(response.text)}")
            
            # Determine format
            if 'xml' in response.headers.get('content-type', '').lower():
                print(f"  ✅ Response Format: XML (as documented)")
            elif response.text.strip().startswith('<?xml'):
                print(f"  ✅ Response Format: XML (detected from content)")
            elif response.text.strip().startswith('{'):
                print(f"  ⚠️  Response Format: JSON (unexpected)")
            else:
                print(f"  ❓ Response Format: Unknown")
            
            print(f"\n  Raw Response (前 500 字元):")
            print(f"  {response.text[:500]}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 6: Try without footnote ID (test if it's really required)
    print("\n【測試 6】測試是否必須提供註腳 ID")
    print("-" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 6a: Only bid
        try:
            params = {
                "bid": 43,
                "version": "tcv",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  只提供 bid: Status={response.status_code}, Length={len(response.text)}")
            
            if response.status_code == 200 and len(response.text) > 100:
                print(f"    → ✅ 可以不提供註腳 ID")
                print(f"    Response: {response.text[:200]}")
            else:
                print(f"    → ⚠️  回應很短，可能需要註腳 ID")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Test 6b: bid + chap
        try:
            params = {
                "bid": 43,
                "chap": 3,
                "version": "tcv",
                "gb": 0
            }
            response = await client.get(base_url, params=params)
            print(f"  提供 bid + chap: Status={response.status_code}, Length={len(response.text)}")
            
            if response.status_code == 200 and len(response.text) > 100:
                print(f"    → ✅ bid + chap 可能足夠")
                print(f"    Response: {response.text[:200]}")
            else:
                print(f"    → ⚠️  回應很短")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("詳細測試完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_footnotes_detailed())
