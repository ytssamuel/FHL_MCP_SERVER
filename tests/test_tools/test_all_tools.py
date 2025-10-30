"""
測試所有 MCP Tools 的功能

這個腳本會測試 FHL Bible MCP Server 的所有工具函數。
"""

import asyncio
from fhl_bible_mcp.tools import (
    # 經文查詢
    get_bible_verse,
    get_bible_chapter,
    query_verse_citation,
    # 搜尋
    search_bible,
    search_bible_advanced,
    # 原文研究
    get_word_analysis,
    lookup_strongs,
    search_strongs_occurrences,
    # 註釋與研經
    get_commentary,
    list_commentaries,
    search_commentary,
    get_topic_study,
    # 資訊查詢
    list_bible_versions,
    get_book_list,
    get_book_info,
    search_available_versions,
    # 多媒體
    get_audio_bible,
    list_audio_versions,
    get_audio_chapter_with_text,
)


async def test_verse_tools():
    """測試經文查詢工具"""
    print("\n" + "=" * 60)
    print("測試 1: 經文查詢工具")
    print("=" * 60)

    # 測試 1.1: 查詢單節經文
    print("\n1.1 查詢約翰福音 3:16")
    result = await get_bible_verse(book="約", chapter=3, verse="16")
    print(f"✓ 版本: {result['version_name']}")
    print(f"✓ 經文: {result['verses'][0]['text']}")

    # 測試 1.2: 查詢整章
    print("\n1.2 查詢詩篇 23 篇")
    result = await get_bible_chapter(book="詩", chapter=23)
    print(f"✓ 共 {result['record_count']} 節")
    print(f"✓ 第一節: {result['verses'][0]['text']}")

    # 測試 1.3: 經文引用查詢
    print("\n1.3 查詢引用字串 '太 5:3-10'")
    result = await query_verse_citation(citation="太 5:3-10")
    print(f"✓ 共 {result['record_count']} 節")
    print(f"✓ 第一節: {result['verses'][0]['text']}")


async def test_search_tools():
    """測試搜尋工具"""
    print("\n" + "=" * 60)
    print("測試 2: 搜尋工具")
    print("=" * 60)

    # 測試 2.1: 關鍵字搜尋
    print("\n2.1 搜尋關鍵字 '平安'")
    result = await search_bible(query="平安", limit=5)
    print(f"✓ 總共找到 {result['total_count']} 筆")
    print(f"✓ 顯示 {len(result['results'])} 筆")
    if result['results']:
        print(f"✓ 第一筆: {result['results'][0]['book']} {result['results'][0]['chapter']}:{result['results'][0]['verse']}")

    # 測試 2.2: 僅計數
    print("\n2.2 搜尋關鍵字 '愛' (僅計數)")
    result = await search_bible(query="愛", count_only=True)
    print(f"✓ 總共找到 {result['total_count']} 筆")


async def test_strongs_tools():
    """測試原文研究工具"""
    print("\n" + "=" * 60)
    print("測試 3: 原文研究工具")
    print("=" * 60)

    # 測試 3.1: 字彙分析
    print("\n3.1 分析約翰福音 3:16 的原文")
    result = await get_word_analysis(book="John", chapter=3, verse=16)
    print(f"✓ 約別: {result['testament']}")
    print(f"✓ 原文: {result['original_text'][:50]}...")
    print(f"✓ 共 {result['word_count']} 個字")
    if result['words']:
        print(f"✓ 第一個字: {result['words'][0]['word']} (Strong's #{result['words'][0]['strongs_number']})")

    # 測試 3.2: Strong's 字典查詢
    print("\n3.2 查詢 Strong's #25 (agapao - 愛)")
    result = await lookup_strongs(number=25, testament="NT")
    print(f"✓ Strong's: {result['strongs_number']}")
    print(f"✓ 原文: {result['original_word']}")
    print(f"✓ 定義: {result['chinese_definition'][:100]}...")
    if 'related_words' in result:
        print(f"✓ 同源字: {len(result['related_words'])} 個")


async def test_commentary_tools():
    """測試註釋與研經工具"""
    print("\n" + "=" * 60)
    print("測試 4: 註釋與研經工具")
    print("=" * 60)

    # 測試 4.1: 列出註釋書
    print("\n4.1 列出所有註釋書")
    result = await list_commentaries()
    print(f"✓ 共 {result['total_count']} 本註釋書")
    for comm in result['commentaries'][:3]:
        print(f"  - [{comm['id']}] {comm['name']}")

    # 測試 4.2: 查詢註釋
    print("\n4.2 查詢約翰福音 3:16 的註釋")
    result = await get_commentary(book="John", chapter=3, verse=16, commentary_id=1)
    print(f"✓ 共 {result['commentary_count']} 筆註釋")
    if result['commentaries']:
        print(f"✓ 第一筆: {result['commentaries'][0]['commentary_name']}")

    # 測試 4.3: 主題查經
    print("\n4.3 查詢主題 '信心'")
    result = await get_topic_study(keyword="信心")
    print(f"✓ 共 {result['total_count']} 筆")
    if result.get('results'):
        print(f"✓ 第一筆來源: {result['results'][0]['source']}")
        if result['results'][0].get('topic'):
            print(f"✓ 第一筆主題: {result['results'][0]['topic']}")


async def test_info_tools():
    """測試資訊查詢工具"""
    print("\n" + "=" * 60)
    print("測試 5: 資訊查詢工具")
    print("=" * 60)

    # 測試 5.1: 列出聖經版本
    print("\n5.1 列出所有聖經版本")
    result = await list_bible_versions()
    print(f"✓ 共 {result['total_count']} 個版本")
    print(f"✓ 第一個: {result['versions'][0]['name']} ({result['versions'][0]['code']})")

    # 測試 5.2: 書卷列表
    print("\n5.2 列出新約書卷")
    result = await get_book_list(testament="NT")
    print(f"✓ 共 {result['total_count']} 卷")
    print(f"✓ 第一卷: {result['books'][0]['chi_full']} ({result['books'][0]['eng_short']})")

    # 測試 5.3: 書卷資訊
    print("\n5.3 查詢約翰福音的資訊")
    result = await get_book_info(book="約")
    print(f"✓ 編號: {result['id']}")
    print(f"✓ 約別: {result['testament']}")
    print(f"✓ 中文全名: {result['names']['chinese']['full']}")
    print(f"✓ 英文全名: {result['names']['english']['full']}")


async def test_audio_tools():
    """測試多媒體工具"""
    print("\n" + "=" * 60)
    print("測試 6: 多媒體工具")
    print("=" * 60)

    # 測試 6.1: 列出音檔版本
    print("\n6.1 列出有聲聖經版本")
    result = await list_audio_versions()
    print(f"✓ 共 {result['total_count']} 個版本")
    for ver in result['versions'][:5]:
        print(f"  - [{ver['code']}] {ver['name']}")

    # 測試 6.2: 查詢音檔
    print("\n6.2 查詢約翰福音 3 章的音檔")
    result = await get_audio_bible(book="約", chapter=3)
    print(f"✓ 版本: {result['version_name']}")
    print(f"✓ 經卷: {result['book']} ({result['book_eng']})")
    print(f"✓ 章: {result['chapter']}")
    if 'mp3' in result['audio_files']:
        print(f"✓ MP3: {result['audio_files']['mp3'][:60]}...")


async def main():
    """執行所有測試"""
    print("\n" + "=" * 60)
    print("FHL Bible MCP Server - Tools 功能測試")
    print("=" * 60)

    try:
        await test_verse_tools()
        await test_search_tools()
        await test_strongs_tools()
        await test_commentary_tools()
        await test_info_tools()
        await test_audio_tools()

        print("\n" + "=" * 60)
        print("✅ 所有測試完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
