"""
FHL Bible MCP Server - Search Topic Prompt

主題式查經研究
"""

from ..base import PromptTemplate


class SearchTopicPrompt(PromptTemplate):
    """主題研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="search_topic",
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
        topic: str,
        version: str = "unv",
        max_verses: int = 10
    ) -> str:
        """
        渲染主題研究的 prompt
        
        Args:
            topic: 研究主題
            version: 聖經版本
            max_verses: 最多顯示經文數
            
        Returns:
            渲染後的 prompt
        """
        return f"""請幫我研究聖經中關於「{topic}」的教導。

請按照以下步驟進行主題研究：

1. **經文搜尋**
   - 使用 search_bible 在 {version} 版本中搜尋「{topic}」
   - 先用 count_only=True 查看總共有多少相關經文
   - 列出最相關的 {max_verses} 處經文（包含上下文）

2. **主題查經資料**
   - 使用 get_topic_study 查詢「{topic}」的主題查經資料
   - 涵蓋 Torrey 和 Naves 主題聖經的相關條目
   - 整理出該主題的聖經神學架構

3. **註釋中的討論**
   - 使用 search_commentary 在註釋書中搜尋「{topic}」
   - 摘要重要註釋家對該主題的見解
   - 列出不同神學傳統的觀點

4. **舊約與新約的教導**
   - 分別搜尋舊約和新約中的相關經文
   - 比較兩約對該主題的教導有何異同
   - 觀察該主題在救恩歷史中的發展

5. **原文洞察**（如適用）
   - 找出該主題相關的關鍵希伯來文/希臘文字詞
   - 使用 lookup_strongs 研究原文字義
   - 解釋原文如何豐富我們對該主題的理解

6. **綜合分析與應用**
   - 總結聖經對「{topic}」的整體教導
   - 歸納出 3-5 個核心真理
   - 提供實際生活應用建議
   - 列出進深研讀的方向

請以清晰的結構呈現研究成果，並引用具體經文支持論點。"""
