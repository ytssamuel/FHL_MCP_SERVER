#!/usr/bin/env python3
"""
測試 FHL API 的 Strong's Number 搜尋格式

目的：確定 search_bible 使用 greek_number/hebrew_number 時的正確查詢格式
"""
import asyncio
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


async def test_strongs_search_formats():
    """測試不同的查詢格式"""
    print("="*70)
    print("Strong's Number 搜尋格式測試")
    print("="*70)
    
    async with FHLAPIEndpoints() as api:
        # Greek Strong's 1344 (δικαιόω - 稱義)
        print("\n📘 測試 1: Greek Strong's 1344 (δικαιόω - 稱義)")
        print("-"*70)
        
        greek_test_cases = [
            ("1344", "greek_number", "nt", "純數字"),
            ("G1344", "greek_number", "nt", "G前綴"),
            ("01344", "greek_number", "nt", "前導零"),
        ]
        
        for query, search_type, scope, description in greek_test_cases:
            print(f"\n  格式: {description}")
            print(f"  查詢: query='{query}', type={search_type}, scope={scope}")
            try:
                result = await api.search_bible(
                    query=query,
                    search_type=search_type,
                    scope=scope,
                    limit=3
                )
                count = result.get('record_count', 0)
                print(f"  ✓ 結果數: {count}")
                if count > 0:
                    first = result['record'][0]
                    text = first.get('bible_text', first.get('fhl_bible_text', ''))[:60]
                    book = first.get('bible_chineses', first.get('book_chinese', ''))
                    chap = first.get('bible_chap', first.get('chapter', ''))
                    verse = first.get('bible_sec', first.get('verse', ''))
                    print(f"    首筆: {book} {chap}:{verse}")
                    print(f"    內容: {text}...")
            except Exception as e:
                print(f"  ✗ 錯誤: {e}")
        
        # Hebrew Strong's 430 (אֱלֹהִים - 神/上帝)
        print("\n\n📗 測試 2: Hebrew Strong's 430 (אֱלֹהִים - 神)")
        print("-"*70)
        
        hebrew_test_cases = [
            ("430", "hebrew_number", "ot", "純數字"),
            ("H430", "hebrew_number", "ot", "H前綴"),
            ("00430", "hebrew_number", "ot", "前導零"),
        ]
        
        for query, search_type, scope, description in hebrew_test_cases:
            print(f"\n  格式: {description}")
            print(f"  查詢: query='{query}', type={search_type}, scope={scope}")
            try:
                result = await api.search_bible(
                    query=query,
                    search_type=search_type,
                    scope=scope,
                    limit=3
                )
                count = result.get('record_count', 0)
                print(f"  ✓ 結果數: {count}")
                if count > 0:
                    first = result['record'][0]
                    text = first.get('bible_text', first.get('fhl_bible_text', ''))[:60]
                    book = first.get('bible_chineses', first.get('book_chinese', ''))
                    chap = first.get('bible_chap', first.get('chapter', ''))
                    verse = first.get('bible_sec', first.get('verse', ''))
                    print(f"    首筆: {book} {chap}:{verse}")
                    print(f"    內容: {text}...")
            except Exception as e:
                print(f"  ✗ 錯誤: {e}")


async def test_lookup_strongs():
    """測試 lookup_strongs 的當前行為"""
    print("\n\n📖 測試 3: lookup_strongs 當前行為")
    print("="*70)
    
    async with FHLAPIEndpoints() as api:
        # 正確的調用方式
        print("\n  格式: 整數 + testament (當前正確方式)")
        try:
            result = await api.get_strongs_dictionary(3056, "nt")
            if result.get('record') and len(result['record']) > 0:
                record = result['record'][0]
                print(f"  ✓ Strong's Number: {record.get('sn', 'N/A')}")
                print(f"  ✓ 原文: {record.get('orig', 'N/A')}")
                print(f"  ✓ 定義: {record.get('dic_text', '')[:80]}...")
            else:
                print(f"  ✗ 無結果: {result}")
        except Exception as e:
            print(f"  ✗ 錯誤: {e}")
        
        # 測試無效輸入（字串）
        print("\n  格式: 字串 'G3056' (預期失敗)")
        try:
            result = await api.get_strongs_dictionary("G3056", "nt")
            if result.get('record') and len(result['record']) > 0:
                record = result['record'][0]
                sn = record.get('sn', 'N/A')
                if sn == "00000":
                    print(f"  ⚠ 返回 demo 資料 (Strong's {sn})")
                else:
                    print(f"  ✓ Strong's Number: {sn}")
        except Exception as e:
            print(f"  ✗ 錯誤（預期）: {e}")


async def main():
    """主測試函數"""
    print("\n")
    await test_strongs_search_formats()
    await test_lookup_strongs()
    
    print("\n\n" + "="*70)
    print("測試結論:")
    print("="*70)
    print("""
1. search_bible (greek_number/hebrew_number):
   - 需要測試確認哪種格式有效
   - 建議：觀察哪種格式返回結果數 > 0
   
2. lookup_strongs:
   - 當前只接受整數 + testament
   - 字串輸入會導致 API 返回 demo 資料 (Strong's 00000)
   - 需要在工具層面進行輸入解析和轉換
   
3. 修復方向:
   - 實現 _parse_strongs_input() 輔助函數
   - 在調用 API 前統一轉換為整數格式
   - 根據 search 測試結果調整查詢格式
""")


if __name__ == "__main__":
    asyncio.run(main())
