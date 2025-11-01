"""
FHL Bible MCP Server - Bible Trivia Prompt

聖經知識問答
"""

from ..base import PromptTemplate


class SpecialBibleTriviaPrompt(PromptTemplate):
    """特殊 - 聖經知識問答 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_bible_trivia",
            description="生成聖經知識問答題目，適合小組活動或教學",
            arguments=[
                {"name": "category", "description": "問答類別", "required": False},
                {"name": "difficulty", "description": "難度級別", "required": False}
            ]
        )
    
    def render(self, category: str = "all", difficulty: str = "medium") -> str:
        """渲染聖經知識問答的 prompt"""
        return f"""# 聖經知識問答

**類別**: {category}
**難度**: {difficulty}

## 步驟 1: 選擇主題
**執行**: 確定問答範圍
- 人物、地點、事件、教義等
**輸出**: 主題清單

## 步驟 2: 設計問題
**執行**: 創建問答題目 (5-10題)
- 選擇題
- 是非題
- 簡答題
**輸出**: 問題清單

## 步驟 3: 提供答案
**執行**: 給出正確答案及經文依據
**輸出**: 答案與經文引用

## 步驟 4: 加入延伸
**執行**: 提供額外資訊
- 背景說明
- 相關經文
**輸出**: 延伸資料

💡 類別: 人物/地點/事件/教義/書卷
💡 難度: easy/medium/hard
"""
