"""
測試 FHL Bible MCP Resources

測試所有 Resource URI 處理器的功能。
"""

import asyncio
import sys
from pathlib import Path

# 將專案根目錄加入 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from fhl_bible_mcp.api.client import FHLAPIClient
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.resources.handlers import ResourceRouter


async def test_bible_resources():
    """測試 bible:// 資源"""
    print("\n" + "="*60)
    print("測試 1: Bible 資源 (bible://)")
    print("="*60)
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試 bible://verse
    print("\n1.1 測試 bible://verse/unv/John/3/16")
    result = await router.handle_resource("bible://verse/unv/John/3/16")
    print(f"URI: {result['uri']}")
    print(f"MIME Type: {result['mimeType']}")
    content = result['content']
    print(f"版本: {content['version_name']}")
    print(f"經文數量: {len(content['verses'])}")
    if content['verses']:
        verse = content['verses'][0]
        print(f"經文: {verse['book']} {verse['chapter']}:{verse['verse']}")
        print(f"內容: {verse['text'][:50]}...")
    
    # 測試 bible://chapter
    print("\n1.2 測試 bible://chapter/unv/Gen/1")
    result = await router.handle_resource("bible://chapter/unv/Gen/1")
    content = result['content']
    print(f"版本: {content['version_name']}")
    print(f"經文數量: {len(content['verses'])}")
    if content['verses']:
        first_verse = content['verses'][0]
        print(f"第一節: {first_verse['text'][:50]}...")
    
    # 測試帶 query 參數的 URI
    print("\n1.3 測試 bible://verse/unv/John/3/16?strong=true")
    result = await router.handle_resource("bible://verse/unv/John/3/16?strong=true")
    content = result['content']
    print(f"包含 Strong's Number: 是")
    print(f"經文數量: {len(content['verses'])}")
    
    await endpoints.close()
    print("\n✅ Bible 資源測試完成")


async def test_strongs_resources():
    """測試 strongs:// 資源"""
    print("\n" + "="*60)
    print("測試 2: Strong's 資源 (strongs://)")
    print("="*60)
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試新約希臘文
    print("\n2.1 測試 strongs://nt/25 (ἀγαπάω - 愛)")
    result = await router.handle_resource("strongs://nt/25")
    print(f"URI: {result['uri']}")
    content = result['content']
    print(f"Strong's Number: {content.get('strongs_number')}")
    print(f"原文: {content.get('original_word')}")
    if content.get('related_words'):
        print(f"同源字數量: {len(content['related_words'])}")
        print(f"第一個同源字: {content['related_words'][0].get('word')}")
    
    # 測試舊約希伯來文
    print("\n2.2 測試 strongs://ot/430 (אֱלֹהִים - 神)")
    result = await router.handle_resource("strongs://ot/430")
    content = result['content']
    print(f"Strong's Number: {content.get('strongs_number')}")
    print(f"原文: {content.get('original_word')}")
    
    await endpoints.close()
    print("\n✅ Strong's 資源測試完成")


async def test_commentary_resources():
    """測試 commentary:// 資源"""
    print("\n" + "="*60)
    print("測試 3: Commentary 資源 (commentary://)")
    print("="*60)
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試註釋查詢
    print("\n3.1 測試 commentary://John/3/16")
    result = await router.handle_resource("commentary://John/3/16")
    print(f"URI: {result['uri']}")
    content = result['content']
    if content.get('commentaries'):
        print(f"找到註釋數量: {len(content['commentaries'])}")
        if content['commentaries']:
            first = content['commentaries'][0]
            print(f"第一個註釋: {first.get('commentary_name')}")
            print(f"標題: {first.get('title', 'N/A')[:50]}...")
    else:
        print("找到註釋數量: 0")
    
    # 測試帶 commentary_id 參數
    print("\n3.2 測試 commentary://John/3/16?commentary_id=1")
    result = await router.handle_resource("commentary://John/3/16?commentary_id=1")
    content = result['content']
    if content.get('commentaries'):
        print(f"找到註釋數量: {len(content['commentaries'])}")
    else:
        print("找到註釋數量: 0")
    
    await endpoints.close()
    print("\n✅ Commentary 資源測試完成")


async def test_info_resources():
    """測試 info:// 資源"""
    print("\n" + "="*60)
    print("測試 4: Info 資源 (info://)")
    print("="*60)
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試版本列表
    print("\n4.1 測試 info://versions")
    result = await router.handle_resource("info://versions")
    print(f"URI: {result['uri']}")
    content = result['content']
    print(f"版本數量: {len(content.get('versions', []))}")
    if content.get('versions'):
        first = content['versions'][0]
        print(f"第一個版本: {first.get('name')} ({first.get('code')})")
    
    # 測試書卷列表
    print("\n4.2 測試 info://books")
    result = await router.handle_resource("info://books")
    content = result['content']
    print(f"書卷數量: {len(content.get('books', []))}")
    if content.get('books'):
        first = content['books'][0]
        print(f"第一卷書: {first.get('chinese_full')} ({first.get('english_short')})")
    
    # 測試新約書卷
    print("\n4.3 測試 info://books?testament=NT")
    result = await router.handle_resource("info://books?testament=NT")
    content = result['content']
    print(f"新約書卷數量: {len(content.get('books', []))}")
    
    # 測試註釋書列表
    print("\n4.4 測試 info://commentaries")
    result = await router.handle_resource("info://commentaries")
    content = result['content']
    print(f"註釋書數量: {len(content.get('commentaries', []))}")
    if content.get('commentaries'):
        first = content['commentaries'][0]
        print(f"第一本註釋書: {first.get('name')}")
    
    await endpoints.close()
    print("\n✅ Info 資源測試完成")


async def test_resource_list():
    """測試支援的資源列表"""
    print("\n" + "="*60)
    print("測試 5: 列出支援的資源")
    print("="*60)
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    supported = router.list_supported_resources()
    
    for category, resources in supported.items():
        print(f"\n{category.upper()} 資源:")
        for resource in resources:
            print(f"  - {resource['uri']}")
            print(f"    說明: {resource['description']}")
            print(f"    範例: {resource['example']}")
    
    await endpoints.close()
    print("\n✅ 資源列表測試完成")


async def main():
    """執行所有測試"""
    print("\n" + "="*60)
    print("FHL Bible MCP Resources 測試")
    print("="*60)
    
    try:
        await test_bible_resources()
        await test_strongs_resources()
        await test_commentary_resources()
        await test_info_resources()
        await test_resource_list()
        
        print("\n" + "="*60)
        print("✅ 所有測試完成!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
