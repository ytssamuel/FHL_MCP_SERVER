"""
更深入的次經 API 測試 - 嘗試不同的參數組合
"""
import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test_apocrypha_detailed():
    client = FHLAPIEndpoints()
    
    print("=" * 70)
    print("次經 API 深入測試")
    print("=" * 70)
    
    # Test 1: 不指定 version
    print("\n【測試 1】不指定 version 參數")
    print("-" * 70)
    result1 = await client._make_request('qsub.php', {
        'chineses': '多',
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result1}")
    
    # Test 2: 使用 book ID 而非中文名稱
    print("\n【測試 2】使用 book ID (bid=101)")
    print("-" * 70)
    result2 = await client._make_request('qsub.php', {
        'bid': 101,
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result2}")
    
    # Test 3: 嘗試英文書名
    print("\n【測試 3】使用英文書名 (engs=Tobit)")
    print("-" * 70)
    result3 = await client._make_request('qsub.php', {
        'engs': 'Tobit',
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result3}")
    
    # Test 4: 嘗試不同的次經書卷
    print("\n【測試 4】測試不同的次經書卷")
    print("-" * 70)
    apocrypha_books = [
        ('多', 'Tobit', 101),
        ('友', 'Judith', 102),
        ('加上', '1Mac', 103),
        ('智', 'Wisdom', 105),
        ('德', 'Sirach', 106),
    ]
    
    for chinese, english, book_id in apocrypha_books:
        print(f"\n  測試: {chinese} ({english}, ID={book_id})")
        result = await client._make_request('qsub.php', {
            'chineses': chinese,
            'chap': 1,
            'sec': 1,
            'gb': 0
        })
        print(f"    record_count: {result.get('record_count', 0)}")
        if result.get('record_count', 0) > 0:
            print(f"    ✅ 有資料!")
            print(f"    第一節: {result['record'][0].get('bible_text', '')[:50]}...")
    
    # Test 5: 嘗試 sesub.php 搜尋
    print("\n【測試 5】測試 sesub.php 搜尋端點")
    print("-" * 70)
    
    # 5a: 無 version
    print("  5a. 不指定 version")
    result5a = await client._make_request('sesub.php', {
        'q': '智慧',
        'gb': 0
    })
    print(f"      結果: {result5a}")
    
    # 5b: 使用 VERSION 參數
    print("\n  5b. 使用 VERSION 參數")
    result5b = await client._make_request('sesub.php', {
        'VERSION': 'unv',
        'q': '智慧',
        'gb': 0
    })
    print(f"      結果: {result5b}")
    
    # Test 6: 檢查 API 是否回傳錯誤訊息
    print("\n【測試 6】檢查可能的錯誤訊息")
    print("-" * 70)
    result6 = await client._make_request('qsub.php', {
        'chineses': '多',
        'chap': 1,
        'sec': 1,
        'version': 'unv',
        'gb': 0
    })
    
    print(f"完整回應: {result6}")
    if 'error' in result6:
        print(f"  ⚠️  錯誤訊息: {result6['error']}")
    if 'message' in result6:
        print(f"  ℹ️  訊息: {result6['message']}")
    
    # Test 7: 直接訪問原始回應
    print("\n【測試 7】檢查原始 HTTP 回應")
    print("-" * 70)
    import httpx
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(
            'https://bible.fhl.net/api/qsub.php',
            params={'chineses': '多', 'chap': 1, 'sec': 1, 'gb': 0}
        )
        print(f"  HTTP Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type')}")
        print(f"  Content Length: {len(response.content)}")
        print(f"  Raw Content (前 200 字元):")
        print(f"  {response.text[:200]}")
    
    await client.close()

asyncio.run(test_apocrypha_detailed())
