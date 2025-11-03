"""
API Validation Tests for Articles (文章) Endpoints

Tests the json.php endpoint with various search parameters.
"""

import asyncio
import json


async def test_articles_api():
    """Test articles search API with various parameters"""
    import aiohttp
    
    base_url = "http://www.fhl.net/api/json.php"
    
    print("="*70)
    print("Testing Articles API (json.php)")
    print("="*70)
    
    # Test cases
    test_cases = [
        {
            "name": "Search by title (愛)",
            "params": {"title": "愛", "gb": 0}
        },
        {
            "name": "Search by author (陳鳳翔)",
            "params": {"author": "陳鳳翔", "gb": 0}
        },
        {
            "name": "Search by column (women3)",
            "params": {"ptab": "women3", "gb": 0}
        },
        {
            "name": "Search by date (2025.10.19)",
            "params": {"pubtime": "2025.10.19", "gb": 0}
        },
        {
            "name": "Search by content (信心)",
            "params": {"txt": "信心", "gb": 0}
        },
        {
            "name": "Search by abstract (耶穌)",
            "params": {"abst": "耶穌", "gb": 0}
        },
        {
            "name": "Combined search (title + author)",
            "params": {"title": "愛", "author": "陳", "gb": 0}
        },
        {
            "name": "Simplified Chinese",
            "params": {"title": "爱", "gb": 1}
        },
        {
            "name": "No parameters (should fail)",
            "params": {}
        },
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, test in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test['name']}")
            print("-" * 70)
            print(f"Parameters: {test['params']}")
            
            try:
                async with session.get(base_url, params=test['params'], timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        print(f"Status: {response.status} OK")
                        print(f"API Status: {data.get('status')}")
                        print(f"Record Count: {data.get('record_count', 0)}")
                        
                        if data.get('status') == 1:
                            records = data.get('record', [])
                            if records and len(records) > 0:
                                print("\nFirst article:")
                                first = records[0]
                                print(f"  Title: {first.get('title', 'N/A')}")
                                print(f"  Author: {first.get('author', 'N/A')}")
                                print(f"  Column: {first.get('column', 'N/A')} ({first.get('ptab', 'N/A')})")
                                print(f"  Date: {first.get('pubtime', 'N/A')}")
                                print(f"  Abstract: {first.get('abst', 'N/A')[:100]}...")
                        elif data.get('status') == 0:
                            print(f"API Error: {data.get('result', 'Unknown error')}")
                    else:
                        print(f"HTTP Status: {response.status}")
                        text = await response.text()
                        print(f"Response: {text[:200]}")
                        
            except asyncio.TimeoutError:
                print("⏱️  Request timeout (30s)")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*70)
    print("Articles API Testing Complete")
    print("="*70)


async def test_articles_response_structure():
    """Test and analyze the response structure"""
    import aiohttp
    
    print("\n" + "="*70)
    print("Analyzing Articles API Response Structure")
    print("="*70)
    
    base_url = "http://www.fhl.net/api/json.php"
    params = {"title": "愛", "gb": 0}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                
                print("\nResponse Structure:")
                print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
                print("...")
                
                if data.get('status') == 1 and data.get('record_count', 0) > 0:
                    records = data.get('record', [])
                    if records:
                        print("\nArticle Fields:")
                        first_article = records[0]
                        for key in first_article.keys():
                            value = first_article[key]
                            value_preview = str(value)[:100] if value else "None"
                            print(f"  - {key}: {value_preview}...")
                
                print("\nData Statistics:")
                print(f"  Total records: {data.get('record_count', 0)}")
                if data.get('record'):
                    print(f"  Records returned: {len(data.get('record', []))}")
                    
                    # Analyze columns
                    columns = set()
                    for article in data.get('record', []):
                        if article.get('ptab'):
                            columns.add(article['ptab'])
                    print(f"  Unique columns: {', '.join(sorted(columns))}")


async def test_column_discovery():
    """Try to discover available columns"""
    import aiohttp
    
    print("\n" + "="*70)
    print("Discovering Article Columns")
    print("="*70)
    
    base_url = "http://www.fhl.net/api/json.php"
    
    # Known column codes to test
    test_columns = [
        "women3", "sunday", "youth", "family", "theology",
        "bible_study", "devotion", "mission", "church", "culture"
    ]
    
    found_columns = []
    
    async with aiohttp.ClientSession() as session:
        for column in test_columns:
            print(f"\nTesting column: {column}")
            params = {"ptab": column, "gb": 0}
            
            try:
                async with session.get(base_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('status') == 1 and data.get('record_count', 0) > 0:
                            records = data.get('record', [])
                            if records:
                                first = records[0]
                                column_name = first.get('column', 'N/A')
                                print(f"  ✅ Found: {column} = {column_name} ({data.get('record_count')} articles)")
                                found_columns.append({
                                    "code": column,
                                    "name": column_name,
                                    "count": data.get('record_count')
                                })
                        else:
                            print(f"  ❌ No data for column: {column}")
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
    
    print("\n" + "="*70)
    print("Column Discovery Summary")
    print("="*70)
    print(f"\nFound {len(found_columns)} columns:\n")
    for col in found_columns:
        print(f"  {col['code']}: {col['name']} ({col['count']} articles)")


if __name__ == "__main__":
    print("\n🔍 FHL Articles API Validation Tests\n")
    
    # Run tests
    asyncio.run(test_articles_api())
    asyncio.run(test_articles_response_structure())
    asyncio.run(test_column_discovery())
    
    print("\n✅ All validation tests complete!\n")
