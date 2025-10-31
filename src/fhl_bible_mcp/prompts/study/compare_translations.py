"""
FHL Bible MCP Server - Compare Translations Prompt

比較不同聖經譯本
"""

from ..base import PromptTemplate


class CompareTranslationsPrompt(PromptTemplate):
    """版本比較 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="compare_translations",
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
        book: str,
        chapter: int,
        verse: int,
        versions: str = "unv,nstrunv,kjv,niv"
    ) -> str:
        """
        渲染版本比較的 prompt
        
        Args:
            book: 經卷名稱
            chapter: 章數
            verse: 節數
            versions: 版本代碼（逗號分隔）
            
        Returns:
            渲染後的 prompt
        """
        version_list = [v.strip() for v in versions.split(",")]
        version_bullets = "\n".join([f"   - {v}" for v in version_list])
        
        return f"""請幫我比較 {book} {chapter}:{verse} 在不同譯本中的翻譯。

請按照以下步驟進行版本比較：

1. **各版本經文**
   - 使用 get_bible_verse 查詢以下版本的經文：
{version_bullets}
   - 並列顯示各版本的翻譯

2. **版本資訊**
   - 使用 list_bible_versions 查詢這些版本的詳細資訊
   - 說明各版本的特色（直譯/意譯、目標讀者、出版年代等）

3. **原文分析**
   - 使用 get_word_analysis 取得該節經文的原文分析
   - 列出關鍵字詞的希臘文/希伯來文及其基本意義
   - 使用 lookup_strongs 查詢重要字詞的 Strong's 字典定義

4. **翻譯差異分析**
   - 比較各版本在以下方面的差異：
     * 字詞選擇（特別是神學關鍵詞）
     * 句子結構
     * 語氣和風格
     * 是否添加解釋性詞語
   - 分析這些差異的原因和影響

5. **原文對照**
   - 將各版本的翻譯與原文進行對照
   - 評估各版本如何處理原文的特殊語法或修辭
   - 指出哪些版本更貼近原文字面意義
   - 指出哪些版本更清楚傳達原文意圖

6. **翻譯評估與建議**
   - 總結各版本的優缺點
   - 針對不同研讀目的推薦合適的版本：
     * 深度研經
     * 靈修默想
     * 初信者閱讀
     * 公開講道引用
   - 建議如何綜合使用多個版本以獲得更全面的理解

請提供詳細的分析，並用表格或對照方式清楚呈現比較結果。"""
