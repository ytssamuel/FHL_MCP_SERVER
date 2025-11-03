"""
測試 FHL API 端點可行性

測試項目:
1. 測試 bible.fhl.net/json/ 端點
2. 測試 bible.fhl.net/api/ 端點 
3. 測試 www.fhl.net/api/json.php
4. 測試 www.fhl.net/api/json_all.php
"""

import requests
import json
from datetime import datetime

def test_endpoint(url, params=None, description=""):
    """測試單一端點"""
    print(f"\n{'='*70}")
    print(f"測試: {description}")
    print(f"URL: {url}")
    if params:
        print(f"參數: {params}")
    print(f"{'='*70}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"狀態碼: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            # 嘗試解析 JSON
            try:
                data = response.json()
                print(f"✅ JSON 解析成功")
                print(f"回應結構:")
                print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")
                return True, data
            except json.JSONDecodeError:
                print(f"⚠️ 無法解析為 JSON")
                print(f"回應內容 (前 500 字元):")
                print(response.text[:500])
                return False, response.text
        else:
            print(f"❌ 請求失敗")
            print(f"回應: {response.text[:500]}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"❌ 請求超時")
        return False, None
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 連線錯誤: {e}")
        return False, None
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False, None

def main():
    print(f"FHL API 端點可行性測試")
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    results = []
    
    # ========================================================================
    # 1. 測試現有的 bible.fhl.net/json/ 端點
    # ========================================================================
    
    print("\n" + "="*70)
    print("第一部分: 測試現有 bible.fhl.net/json/ 端點")
    print("="*70)
    
    # 1.1 測試版本列表
    success, data = test_endpoint(
        "https://bible.fhl.net/json/ab.php",
        description="聖經版本列表 (ab.php)"
    )
    results.append(("bible.fhl.net/json/ab.php", success))
    
    # 1.2 測試經文查詢
    success, data = test_endpoint(
        "https://bible.fhl.net/json/qb.php",
        params={"chineses": "約", "chap": 3, "sec": 16, "version": "unv", "gb": 0},
        description="經文查詢 (qb.php) - 約翰福音 3:16"
    )
    results.append(("bible.fhl.net/json/qb.php", success))
    
    # 1.3 測試搜尋
    success, data = test_endpoint(
        "https://bible.fhl.net/json/se.php",
        params={"VERSION": "unv", "orig": 0, "q": "愛", "RANGE": 0, "limit": 5, "gb": 0},
        description="經文搜尋 (se.php) - 搜尋「愛」"
    )
    results.append(("bible.fhl.net/json/se.php", success))
    
    # ========================================================================
    # 2. 測試 bible.fhl.net/api/ 端點 (新路徑)
    # ========================================================================
    
    print("\n" + "="*70)
    print("第二部分: 測試 bible.fhl.net/api/ 端點")
    print("="*70)
    
    # 2.1 測試版本列表
    success, data = test_endpoint(
        "https://bible.fhl.net/api/ab.php",
        description="聖經版本列表 (api/ab.php)"
    )
    results.append(("bible.fhl.net/api/ab.php", success))
    
    # 2.2 測試經文查詢
    success, data = test_endpoint(
        "https://bible.fhl.net/api/qb.php",
        params={"chineses": "約", "chap": 3, "sec": 16, "version": "unv", "gb": 0},
        description="經文查詢 (api/qb.php) - 約翰福音 3:16"
    )
    results.append(("bible.fhl.net/api/qb.php", success))
    
    # 2.3 測試搜尋
    success, data = test_endpoint(
        "https://bible.fhl.net/api/se.php",
        params={"VERSION": "unv", "orig": 0, "q": "愛", "RANGE": 0, "limit": 5, "gb": 0},
        description="經文搜尋 (api/se.php) - 搜尋「愛」"
    )
    results.append(("bible.fhl.net/api/se.php", success))
    
    # ========================================================================
    # 3. 測試 www.fhl.net/api/json.php
    # ========================================================================
    
    print("\n" + "="*70)
    print("第三部分: 測試 www.fhl.net/api/json.php (文章 API)")
    print("="*70)
    
    # 3.1 不帶參數測試
    success, data = test_endpoint(
        "http://www.fhl.net/api/json.php",
        description="文章列表 (json.php) - 無參數"
    )
    results.append(("www.fhl.net/api/json.php (無參數)", success))
    
    # 3.2 帶 gb 參數
    success, data = test_endpoint(
        "http://www.fhl.net/api/json.php",
        params={"gb": 0},
        description="文章列表 (json.php) - gb=0"
    )
    results.append(("www.fhl.net/api/json.php (gb=0)", success))
    
    # 3.3 搜尋特定專欄
    success, data = test_endpoint(
        "http://www.fhl.net/api/json.php",
        params={"ptab": "sunday", "gb": 0},
        description="文章列表 (json.php) - 週日專欄"
    )
    results.append(("www.fhl.net/api/json.php (ptab=sunday)", success))
    
    # 3.4 搜尋關鍵字
    success, data = test_endpoint(
        "http://www.fhl.net/api/json.php",
        params={"title": "愛", "gb": 0},
        description="文章列表 (json.php) - 標題包含「愛」"
    )
    results.append(("www.fhl.net/api/json.php (title=愛)", success))
    
    # ========================================================================
    # 4. 測試 www.fhl.net/api/json_all.php
    # ========================================================================
    
    print("\n" + "="*70)
    print("第四部分: 測試 www.fhl.net/api/json_all.php (列出所有文章)")
    print("="*70)
    
    # 4.1 不帶參數
    success, data = test_endpoint(
        "http://www.fhl.net/api/json_all.php",
        description="所有文章列表 (json_all.php) - 無參數"
    )
    results.append(("www.fhl.net/api/json_all.php (無參數)", success))
    
    # 4.2 帶 gb 參數
    success, data = test_endpoint(
        "http://www.fhl.net/api/json_all.php",
        params={"gb": 0},
        description="所有文章列表 (json_all.php) - gb=0"
    )
    results.append(("www.fhl.net/api/json_all.php (gb=0)", success))
    
    # ========================================================================
    # 總結
    # ========================================================================
    
    print("\n" + "="*70)
    print("測試結果總結")
    print("="*70)
    
    print(f"\n共測試 {len(results)} 個端點:\n")
    
    for endpoint, success in results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"{status} - {endpoint}")
    
    success_count = sum(1 for _, success in results if success)
    print(f"\n成功: {success_count}/{len(results)}")
    print(f"成功率: {success_count/len(results)*100:.1f}%")
    
    print("\n" + "="*70)
    print("測試完成")
    print("="*70)

if __name__ == "__main__":
    main()
