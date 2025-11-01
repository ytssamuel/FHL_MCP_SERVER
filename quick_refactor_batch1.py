"""快速批量重構剩餘prompts"""
import os
import shutil

# 定義所有需要重構的prompts
PROMPTS_DATA = [
    # 7. special_topical_chain
    ("special/special_topical_chain", "SpecialTopicalChainPrompt", "信心", "both", 900, '''"""
FHL Bible MCP Server - Topical Chain Prompt

主題經文串連研究
"""

from ..base import PromptTemplate


class SpecialTopicalChainPrompt(PromptTemplate):
    """特殊 - 主題經文串連 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_topical_chain",
            description="追蹤特定主題在聖經中的發展脈絡，建立主題經文鏈",
            arguments=[
                {"name": "topic", "description": "研究主題", "required": True},
                {"name": "testament", "description": "約別限制 (OT/NT/both)", "required": False}
            ]
        )
    
    def render(self, topic: str = "信心", testament: str = "both") -> str:
        """渲染主題串連的 prompt"""
        return f"""# 主題經文串連 - {topic}

## 步驟 1: 搜尋主題經文
**執行**: 找出所有與主題相關的經文
- 搜尋範圍: {testament}
- 主題: {topic}
**輸出**: 經文清單與出現次數

## 步驟 2: 建立時間線
**執行**: 按聖經順序排列經文
- 舊約 → 新約發展
- 標記關鍵轉折點
**輸出**: 時間線圖表

## 步驟 3: 分析主題發展
**執行**: 觀察主題如何演進
- 初次出現與背景
- 逐步深化過程
- 高峰與完全揭示
**輸出**: 發展階段分析

## 步驟 4: 識別關鍵經文
**執行**: 找出5-10節核心經文
- 定義性經文
- 轉折性經文
**輸出**: 關鍵經文列表

## 步驟 5: 建立經文鏈
**執行**: 串連相關經文
- 直接引用關係
- 主題呼應關係
**輸出**: 經文串連圖

## 步驟 6: 提煉神學洞見
**執行**: 總結主題的聖經神學
**輸出**: 神學摘要與應用

💡 工具: search_bible, study_topic_deep
"""
'''),
]

BASE_PATH = "c:/Users/USER/Desktop/develope/FHL_MCP_SERVER/src/fhl_bible_mcp/prompts"

for folder, classname, *_, content in PROMPTS_DATA:
    filepath = f"{BASE_PATH}/{folder}.py"
    backup = f"{filepath}.bak"
    
    # 備份
    if os.path.exists(filepath):
        shutil.copy(filepath, backup)
        print(f"✅ 備份: {filepath}")
    
    # 寫入新內容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 重構: {filepath}")

print("\n完成第一批!")
