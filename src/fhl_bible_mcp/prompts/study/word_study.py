"""
FHL Bible MCP Server - Word Study Prompt

深入研究原文字詞
"""

from ..base import PromptTemplate


class WordStudyPrompt(PromptTemplate):
    """原文字詞研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="word_study",
            description="深入研究希臘文或希伯來文單字",
            arguments=[
                {
                    "name": "strongs_number",
                    "description": "Strong's 編號",
                    "required": True
                },
                {
                    "name": "testament",
                    "description": "約別（OT 或 NT）",
                    "required": True
                },
                {
                    "name": "max_occurrences",
                    "description": "最多顯示的出現次數（預設：20）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        strongs_number: str,
        testament: str,
        max_occurrences: int = 20
    ) -> str:
        """
        渲染原文字詞研究的 prompt
        
        Args:
            strongs_number: Strong's 編號
            testament: 約別（OT/NT）
            max_occurrences: 最多顯示出現次數
            
        Returns:
            渲染後的 prompt
        """
        testament_name = "新約希臘文" if testament.upper() == "NT" else "舊約希伯來文"
        
        return f"""請幫我研究 Strong's #{strongs_number} ({testament_name}) 這個原文字。

請按照以下步驟進行字詞研究：

1. **字典定義**
   - 使用 lookup_strongs 查詢 Strong's #{strongs_number} 的字典條目
   - 提供：
     * 原文拼寫（含發音）
     * 字根來源
     * 基本字義
     * 英文和中文的詳細定義

2. **同源字分析**（僅適用於新約）
   - 列出所有同源字（來自同一字根的相關字詞）
   - 說明各同源字的：
     * Strong's 編號
     * 原文拼寫
     * 中文意義
     * 在聖經中出現的次數
   - 分析這些同源字的語義關係

3. **聖經出現位置**
   - 使用 search_strongs_occurrences 找出該字在聖經中的所有出現位置
   - 列出前 {max_occurrences} 處具代表性的經文
   - 按書卷順序或主題分類整理

4. **語境中的字義變化**
   - 分析該字在不同語境中的用法：
     * 文學體裁（敘事、詩歌、律法、書信等）
     * 作者風格（保羅、約翰、路加等）
     * 時代背景（舊約時期、福音書、早期教會等）
   - 觀察字義的範圍和強調的不同面向
   - 特別注意是否有比喻或象徵用法

5. **神學意義**
   - 探討該字的神學重要性：
     * 在救恩歷史中的角色
     * 與核心教義的關聯
     * 對理解神的屬性或作為的貢獻
   - 引用重要經文說明其神學用法
   - 參考註釋書對該字的神學討論

6. **跨約比較**（如適用）
   - 比較舊約希伯來文與新約希臘文的對應字詞
   - 觀察七十士譯本（LXX）的翻譯選擇
   - 分析新約如何引用或重新詮釋舊約的概念

7. **研究總結與應用**
   - 總結該字的核心意涵
   - 說明正確理解該字如何幫助我們：
     * 更準確理解相關經文
     * 避免常見的誤解
     * 在生活中活出該字的真理
   - 推薦進深研讀的資源或經文

請提供詳盡的分析，並引用具體經文和學術資源。"""
