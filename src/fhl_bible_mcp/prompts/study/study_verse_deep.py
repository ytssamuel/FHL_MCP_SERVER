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
        book: str = "約翰福音",
        chapter: int = 3,
        verse: int = 16,
        version: str = "unv"
    ) -> str:
        """
        渲染深入研讀經文的 prompt
        
        Args:
            book: 經卷名稱（默認：約翰福音）
            chapter: 章數（默認：3）
            verse: 節數（默認：16）
            version: 聖經版本代碼
            
        Returns:
            渲染後的 prompt
        """
        return f"""# 深入研讀經文 - {book} {chapter}:{verse}

## 步驟 1: 獲取經文內容
**執行**: get_bible_verse 查詢 {book} {chapter}:{verse} ({version})
**輸出**: 經文內容及 Strong's Number 版本

## 步驟 2: 分析原文字彙
**執行**: get_word_analysis 取得希臘文/希伯來文分析
**輸出**: 每個重要字詞的原文、詞性、字型變化

## 步驟 3: 研究關鍵字詞
**執行**: lookup_strongs 查詢關鍵字的 Strong's 字典
**輸出**: 原文意義、用法、神學含義、同源字

## 步驟 4: 查詢註釋解經
**執行**: get_commentary 取得該節經文註釋
**輸出**: 綜合不同註釋書的觀點和應用建議

## 步驟 5: 連結相關經文
**執行**: search_bible 搜尋相關主題或關鍵字
**輸出**: 3-5 處相關經文供交叉參考

## 步驟 6: 綜合研讀總結
**執行**: 整合所有資訊
**輸出**: 核心信息、神學意義、實際應用、思考問題

💡 工具: get_bible_verse, get_word_analysis, lookup_strongs, get_commentary
"""
