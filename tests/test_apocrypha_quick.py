"""Quick test for Apocrypha API"""
import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test():
    client = FHLAPIEndpoints()
    
    print("Testing qsub.php endpoint...")
    print("-" * 70)
    
    # Test 1: Tobit 1:1
    print("\n1. Testing 多俾亞傳 (Tobit) 1:1")
    result = await client._make_request('qsub.php', {
        'chineses': '多',
        'chap': 1,
        'sec': 1,
        'version': 'unv',
        'gb': 0
    })
    print(f"Result: {result}")
    
    # Test 2: Try with book ID
    print("\n2. Testing with book ID 101")
    result2 = await client._make_request('qsub.php', {
        'bid': 101,
        'chap': 1,
        'sec': 1,
        'version': 'unv',
        'gb': 0
    })
    print(f"Result: {result2}")
    
    # Test 3: Try sesub.php
    print("\n3. Testing sesub.php search")
    result3 = await client._make_request('sesub.php', {
        'VERSION': 'unv',
        'q': '智慧',
        'gb': 0
    })
    print(f"Result: {result3}")
    
    await client.close()

asyncio.run(test())
