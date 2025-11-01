"""
FHL Bible MCP Server - Memory Verse Prompt

經文背誦輔助
"""

from ..base import PromptTemplate


class SpecialMemoryVersePrompt(PromptTemplate):
    """特殊 - 經文背誦 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_memory_verse",
            description="協助經文背誦，提供記憶技巧和應用提醒",
            arguments=[
                {"name": "verse", "description": "要背誦的經文", "required": True}
            ]
        )
    
    def render(self, verse: str = "約翰福音 3:16") -> str:
        """渲染經文背誦的 prompt"""
        return f"""# 經文背誦 - {verse}

## 步驟 1: 獲取經文
**執行**: 取得完整經文
- 經文: {verse}
**輸出**: 經文內容及引用

## 步驟 2: 理解意義
**執行**: 先理解再背誦
- 經文意思
- 關鍵字詞
**輸出**: 經文解釋

## 步驟 3: 分段記憶
**執行**: 將經文分成小段
- 每段3-5個字
- 逐段記憶
**輸出**: 分段方案

## 步驟 4: 使用技巧
**執行**: 應用記憶法
- 首字記憶法
- 圖像聯想法
- 韻律記憶法
**輸出**: 記憶提示

## 步驟 5: 反覆練習
**執行**: 多次複誦
- 看著背、不看背
- 每日複習
**輸出**: 練習計畫

## 步驟 6: 實際應用
**執行**: 在生活中使用
**輸出**: 應用場景

💡 建議: 每週背誦1-2節
"""
