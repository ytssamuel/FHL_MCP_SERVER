"""
Test to find which Bible versions support Apocrypha
"""
import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test_versions():
    client = FHLAPIEndpoints()
    
    print("=" * 70)
    print("查詢支援次經的聖經版本")
    print("=" * 70)
    
    # Get all versions
    versions_result = await client.get_bible_versions()
    
    if versions_result.get("status") == "success":
        print(f"\n總共有 {versions_result['record_count']} 個版本")
        print("\n檢查哪些版本支援次經...")
        print("-" * 70)
        
        # Common versions to test
        test_versions = [
            "nrsv",      # New Revised Standard Version (有次經)
            "kjv",       # King James Version (無次經)
            "cv",        # Catholic Version (天主教版本，應該有次經)
            "cnet",      # Chinese NET (不確定)
            "unv",       # 和合本 (無次經)
        ]
        
        print("\n測試常見版本:")
        for version_code in test_versions:
            print(f"\n測試版本: {version_code}")
            
            # Try to get Tobit 1:1 with this version
            result = await client._make_request('qsub.php', {
                'chineses': '多',
                'chap': 1,
                'sec': 1,
                'version': version_code,
                'gb': 0
            })
            
            if result.get('status') == 'success' and result.get('record_count', 0) > 0:
                print(f"  ✅ {version_code} 支援次經！")
                verse = result['record'][0]
                print(f"     經文: {verse.get('bible_text', '')[:50]}...")
            else:
                print(f"  ❌ {version_code} 不支援次經")
        
        # List all versions that might support Apocrypha
        print("\n\n所有版本列表（尋找可能支援次經的版本）:")
        print("-" * 70)
        for v in versions_result.get('record', []):
            book = v.get('book', '')
            cname = v.get('cname', '')
            ntonly = v.get('ntonly', 0)
            otonly = v.get('otonly', 0)
            
            # 次經通常在舊約聖經版本中
            if ntonly == 0:  # Not NT-only
                print(f"{book:15s} - {cname:30s} (NT-only: {ntonly}, OT-only: {otonly})")
    
    await client.close()

asyncio.run(test_versions())
