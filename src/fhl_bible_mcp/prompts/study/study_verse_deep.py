"""
FHL Bible MCP Server - Study Verse Prompt

深入研讀單節經文
"""

from ..base import PromptTemplate


class StudyVerseDeepPrompt(PromptTemplate):
    """研經 - 深入研讀經文 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="study_verse_deep",
            description="深入研讀一節經文，包含經文內容、原文分析、註釋等",
            arguments=[
                {
                    "name": "book",
                    "description": "經卷名稱（中文或英文縮寫）",
                    "required": True
                },
                {
                    "name": "chapter",
                    "description": "章數",
                    "required": True
                },
                {
                    "name": "verse",
                    "description": "節數",
                    "required": True
                },
                {
                    "name": "version",
                    "description": "聖經版本代碼（預設：unv）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        book: str,
        chapter: int,
        verse: int,
        version: str = "unv"
    ) -> str:
        """
        渲染深入研讀經文的 prompt
        
        Args:
            book: 經卷名稱
            chapter: 章數
            verse: 節數
            version: 聖經版本代碼
            
        Returns:
            渲染後的 prompt
        """
        return f"""請幫我深入研讀 {book} {chapter}:{verse}。

請按照以下步驟進行研讀：

1. **經文內容**
   - 使用 get_bible_verse 查詢 {book} {chapter}:{verse} ({version} 版本)
   - 同時獲取包含 Strong's Number 的版本以便原文分析

2. **原文字彙分析**
   - 使用 get_word_analysis 取得該節經文的希臘文/希伯來文分析
   - 列出每個重要字詞的原文、詞性、字型變化

3. **關鍵字詞研究**
   - 針對經文中的關鍵字，使用 lookup_strongs 查詢 Strong's 字典
   - 解釋重要字詞的原文意義、用法、神學含義
   - 列出同源字及其在聖經中的使用

4. **註釋與解經**
   - 使用 get_commentary 查詢該節經文的註釋
   - 綜合不同註釋書的觀點
   - 提供解經要點和應用建議

5. **相關經文連結**
   - 使用 search_bible 搜尋相關主題或關鍵字
   - 列出 3-5 處相關經文供交叉參考

6. **研讀總結**
   - 綜合以上資訊，提供該節經文的：
     * 核心信息
     * 神學意義
     * 實際應用
     * 思考問題

請以結構化、易讀的方式呈現研讀結果。"""
