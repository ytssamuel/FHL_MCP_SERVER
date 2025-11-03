"""
測試使徒教父 (Apostolic Fathers) API 端點
測試 qaf.php 和 seaf.php
"""
import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test_apostolic_fathers():
    client = FHLAPIEndpoints()
    
    print("=" * 70)
    print("使徒教父 (Apostolic Fathers) API 測試")
    print("書卷範圍: 201-217")
    print("=" * 70)
    
    # Test 1: qaf.php - 不指定 version
    print("\n【測試 1】qaf.php - 不指定 version")
    print("-" * 70)
    result1 = await client._make_request('qaf.php', {
        'chineses': '革',  # 革利免前書
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result1}")
    
    # Test 2: 使用 book ID
    print("\n【測試 2】qaf.php - 使用 book ID (bid=201)")
    print("-" * 70)
    result2 = await client._make_request('qaf.php', {
        'bid': 201,
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result2}")
    
    # Test 3: 使用英文書名
    print("\n【測試 3】qaf.php - 使用英文書名")
    print("-" * 70)
    result3 = await client._make_request('qaf.php', {
        'engs': '1Clem',
        'chap': 1,
        'sec': 1,
        'gb': 0
    })
    print(f"結果: {result3}")
    
    # Test 4: 測試不同的使徒教父書卷
    print("\n【測試 4】測試不同的使徒教父書卷")
    print("-" * 70)
    apostolic_fathers_books = [
        ('革', '1Clement', 201, '革利免前書'),
        ('革二', '2Clement', 202, '革利免後書'),
        ('伊', 'Ignatius', 203, '伊格那丟書信'),
        ('坡', 'Polycarp', 204, '坡旅甲書信'),
    ]
    
    for chinese, english, book_id, full_name in apostolic_fathers_books:
        print(f"\n  測試: {chinese} ({english}, ID={book_id}) - {full_name}")
        result = await client._make_request('qaf.php', {
            'chineses': chinese,
            'chap': 1,
            'sec': 1,
            'gb': 0
        })
        print(f"    status: {result.get('status')}")
        print(f"    record_count: {result.get('record_count', 0)}")
        if result.get('record_count', 0) > 0:
            print(f"    ✅ 有資料!")
            verse = result['record'][0]
            print(f"    bid: {verse.get('bid', 'N/A')}")
            print(f"    經文: {verse.get('bible_text', '')[:50]}...")
    
    # Test 5: seaf.php 搜尋
    print("\n【測試 5】seaf.php - 搜尋端點")
    print("-" * 70)
    
    # 5a: 不指定 version
    print("  5a. 不指定 version，搜尋「教會」")
    result5a = await client._make_request('seaf.php', {
        'q': '教會',
        'gb': 0
    })
    print(f"      status: {result5a.get('status')}")
    print(f"      record_count: {result5a.get('record_count', 0)}")
    if result5a.get('record_count', 0) > 0:
        print(f"      ✅ 找到結果!")
        print(f"      第一筆: {result5a['record'][0].get('bible_text', '')[:50]}...")
    
    # 5b: 使用 VERSION 參數（測試是否會失敗）
    print("\n  5b. 使用 VERSION 參數（預期可能失敗）")
    try:
        result5b = await client._make_request('seaf.php', {
            'VERSION': 'unv',
            'q': '教會',
            'gb': 0
        })
        print(f"      結果: {result5b}")
    except Exception as e:
        print(f"      ❌ 錯誤: {e}")
    
    # Test 6: 檢查原始 HTTP 回應
    print("\n【測試 6】檢查原始 HTTP 回應")
    print("-" * 70)
    import httpx
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(
            'https://bible.fhl.net/api/qaf.php',
            params={'chineses': '革', 'chap': 1, 'sec': 1, 'gb': 0}
        )
        print(f"  HTTP Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type')}")
        print(f"  Content Length: {len(response.content)}")
        print(f"  Raw Content (前 300 字元):")
        print(f"  {response.text[:300]}")
    
    await client.close()

asyncio.run(test_apostolic_fathers())
