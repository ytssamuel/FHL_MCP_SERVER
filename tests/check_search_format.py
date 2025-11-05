"""
快速檢查 search_bible 返回的實際結果格式
"""

import asyncio
import json
from fhl_bible_mcp.tools.search import search_bible


async def check_results():
    print("=" * 60)
    print("檢查 search_bible greek_number 返回格式")
    print("=" * 60)
    print()
    
    # 測試 G1344
    print("📝 查詢 G1344 (greek_number)...")
    result = await search_bible(
        query="1344",
        search_type="greek_number",
        scope="nt",
        version="unv",
        limit=10
    )
    
    print(f"\n返回結構:")
    print(f"- Keys: {list(result.keys())}")
    print(f"- Total count: {result.get('total_count', 'N/A')}")
    print(f"- Results count: {len(result.get('results', []))}")
    
    if result.get('results'):
        print(f"\n第一筆結果:")
        first = result['results'][0]
        print(json.dumps(first, ensure_ascii=False, indent=2))
        
        print(f"\n前 5 筆結果摘要:")
        for i, verse in enumerate(result['results'][:5], 1):
            book = verse.get('book', 'N/A')
            chapter = verse.get('chapter', 'N/A')
            verse_num = verse.get('verse', 'N/A')
            text = verse.get('text') or verse.get('content', '')
            print(f"{i}. {book} {chapter}:{verse_num}")
            print(f"   {text[:60]}...")
    else:
        print("\n⚠️ 沒有返回結果")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(check_results())
