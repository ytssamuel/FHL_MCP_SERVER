"""
FHL Bible MCP Server - Compare Translations Prompt

比較不同聖經譯本
"""

from ..base import PromptTemplate


class StudyTranslationComparePrompt(PromptTemplate):
    """研經 - 版本比較 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="study_translation_compare",
            description="比較不同聖經譯本的翻譯",
            arguments=[
                {
                    "name": "book",
                    "description": "經卷名稱",
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
                    "name": "versions",
                    "description": "要比較的版本代碼列表（逗號分隔）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        book: str = "約翰福音",
        chapter: int = 3,
        verse: int = 16,
        versions: str = "unv,nstrunv,kjv,niv"
    ) -> str:
        """
        渲染版本比較的 prompt
        
        Args:
            book: 經卷名稱（默認：約翰福音）
            chapter: 章數（默認：3）
            verse: 節數（默認：16）
            versions: 版本代碼（逗號分隔）
            
        Returns:
            渲染後的 prompt
        """
        version_list = [v.strip() for v in versions.split(",")]
        version_bullets = "\n".join([f"   - {v}" for v in version_list])
        
        return f"""# 版本比較 - {book} {chapter}:{verse}

## 步驟 1: 獲取各版本經文
**執行**: get_bible_verse 查詢以下版本：
{version_bullets}
**輸出**: 並列顯示各版本翻譯

## 步驟 2: 查詢版本資訊
**執行**: list_bible_versions 取得版本詳細資訊
**輸出**: 各版本特色（直譯/意譯、目標讀者、年代）

## 步驟 3: 分析原文基礎
**執行**: get_word_analysis + lookup_strongs 查詢原文
**輸出**: 關鍵字詞的希臘文/希伯來文及 Strong's 定義

## 步驟 4: 比較翻譯差異
**執行**: 分析字詞選擇、句子結構、語氣風格差異
**輸出**: 差異原因和影響分析

## 步驟 5: 對照原文評估
**執行**: 評估各版本如何處理原文語法和修辭
**輸出**: 字面意義 vs 原文意圖的忠實度分析

## 步驟 6: 提供使用建議
**執行**: 總結優缺點，針對不同目的推薦版本
**輸出**: 深度研經、靈修、初信、講道的版本建議

💡 工具: get_bible_verse, list_bible_versions, get_word_analysis, lookup_strongs
"""
