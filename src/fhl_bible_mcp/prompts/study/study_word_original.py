"""
FHL Bible MCP Server - Word Study Prompt

深入研究原文字詞
"""

from ..base import PromptTemplate


class StudyWordOriginalPrompt(PromptTemplate):
    """研經 - 原文字詞研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="study_word_original",
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
        strongs_number: str = "G26",
        testament: str = "NT",
        max_occurrences: int = 20
    ) -> str:
        """
        渲染原文字詞研究的 prompt
        
        Args:
            strongs_number: Strong's 編號（默認：G26，愛 agape）
            testament: 約別（OT/NT）（默認：NT）
            max_occurrences: 最多顯示出現次數
            
        Returns:
            渲染後的 prompt
        """
        testament_name = "新約希臘文" if testament.upper() == "NT" else "舊約希伯來文"
        
        return f"""# 原文字詞研究 - Strong's #{strongs_number} ({testament_name})

## 步驟 1: 查詢字典定義
**執行**: lookup_strongs #{strongs_number}
**輸出**: 原文拼寫、字根、基本字義、詳細定義

## 步驟 2: 搜尋出現位置
**執行**: search_strongs_occurrences 找出聖經中的所有位置
**輸出**: 前 {max_occurrences} 處具代表性經文

## 步驟 3: 分析語境用法
**執行**: 比較不同文學體裁、作者風格中的字義變化
**輸出**: 語義範圍和特殊用法分析

## 步驟 4: 探討神學意義
**執行**: 研究該字在救恩歷史和核心教義中的角色
**輸出**: 神學重要性和關鍵經文引用

## 步驟 5: 跨約比較 (如適用)
**執行**: 對照舊約希伯來文與新約希臘文的對應關係
**輸出**: LXX翻譯選擇和新約詮釋分析

## 步驟 6: 總結與應用
**執行**: 綜合核心意涵，提供理解和生活應用建議
**輸出**: 研究總結、避免誤解、實踐方向

💡 工具: lookup_strongs, search_strongs_occurrences
"""
