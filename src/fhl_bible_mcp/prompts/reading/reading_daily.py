"""
FHL Bible MCP Server - Reading Daily Prompt

每日讀經輔助
"""

from ..base import PromptTemplate


class ReadingDailyPrompt(PromptTemplate):
    """讀經 - 每日讀經輔助 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="reading_daily",
            description="每日靈修讀經指引，包含默想和應用",
            arguments=[
                {"name": "passage", "description": "今日經文", "required": False}
            ]
        )
    
    def render(self, passage: str = None) -> str:
        """渲染每日讀經的 prompt"""
        if not passage:
            passage_text = "取得今日金句 (get_verse_of_day)"
        else:
            passage_text = passage
            
        return f"""# 每日讀經 - {passage_text}

## 步驟 1: 獲取經文
**執行**: 取得今日要讀的經文
**輸出**: 經文內容

## 步驟 2: 初步閱讀
**執行**: 閱讀2-3遍
- 整體印象
- 關鍵字詞
**輸出**: 初步理解

## 步驟 3: 默想經文
**執行**: 深入思考經文意義
- 這段說什麼？
- 對我說什麼？
**輸出**: 個人領受

## 步驟 4: 連結生活
**執行**: 將經文應用到生活
- 今天要學習什麼？
- 今天要做什麼？
**輸出**: 具體行動

## 步驟 5: 禱告回應
**執行**: 用經文禱告
**輸出**: 禱告內容

💡 開始: get_verse_of_day
"""
