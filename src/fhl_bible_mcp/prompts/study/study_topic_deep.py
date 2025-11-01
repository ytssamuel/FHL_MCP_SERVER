"""
FHL Bible MCP Server - Search Topic Prompt

主題式查經研究
"""

from ..base import PromptTemplate


class StudyTopicDeepPrompt(PromptTemplate):
    """研經 - 主題研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="study_topic_deep",
            description="研究聖經中的特定主題",
            arguments=[
                {
                    "name": "topic",
                    "description": "要研究的主題關鍵字",
                    "required": True
                },
                {
                    "name": "version",
                    "description": "聖經版本代碼（預設：unv）",
                    "required": False
                },
                {
                    "name": "max_verses",
                    "description": "最多顯示的經文數量（預設：10）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        topic: str = "愛",
        version: str = "unv",
        max_verses: int = 10
    ) -> str:
        """
        渲染主題研究的 prompt
        
        Args:
            topic: 研究主題（默認：愛）
            version: 聖經版本
            max_verses: 最多顯示經文數
            
        Returns:
            渲染後的 prompt
        """
        return f"""# 主題研究 - 「{topic}」

## 步驟 1: 搜尋相關經文
**執行**: search_bible 在 {version} 中搜尋「{topic}」
**輸出**: 總數統計 + 最相關的 {max_verses} 處經文

## 步驟 2: 查詢主題查經資料
**執行**: get_topic_study 取得「{topic}」的主題查經
**輸出**: Torrey 和 Naves 相關條目，聖經神學架構

## 步驟 3: 搜尋註釋討論
**執行**: search_commentary 在註釋書中搜尋「{topic}」
**輸出**: 註釋家見解摘要，不同神學傳統觀點

## 步驟 4: 比較兩約教導
**執行**: 分別搜尋舊約和新約相關經文
**輸出**: 兩約異同，救恩歷史發展脈絡

## 步驟 5: 研究原文洞察
**執行**: lookup_strongs 查詢關鍵希伯來文/希臘文字詞
**輸出**: 原文字義如何豐富主題理解

## 步驟 6: 綜合分析與應用
**執行**: 整合所有資料
**輸出**: 整體教導總結、3-5個核心真理、生活應用

💡 工具: search_bible, get_topic_study, search_commentary, lookup_strongs
"""
