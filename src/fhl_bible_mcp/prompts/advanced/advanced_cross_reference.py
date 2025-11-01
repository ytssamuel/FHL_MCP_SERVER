"""
Advanced Cross Reference Prompt

交叉引用研究
"""

from ..base import PromptTemplate


class AdvancedCrossReferencePrompt(PromptTemplate):
    """進階 - 交叉引用研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="advanced_cross_reference",
            description="深入研究經文的交叉引用，建立經文網絡",
            arguments=[
                {"name": "reference", "description": "經文引用", "required": True}
            ]
        )
    
    def render(self, reference: str = "約翰福音 3:16") -> str:
        """渲染交叉引用研究的 prompt"""
        return f"""# 交叉引用研究 - {reference}

## 步驟 1: 獲取主經文
**執行**: 取得研究的經文
- 經文: {reference}
**輸出**: 完整經文內容

## 步驟 2: 找直接引用
**執行**: 識別直接引用關係
- 本節引用的舊約經文
- 新約中引用本節的經文
**輸出**: 直接引用清單

## 步驟 3: 找主題相關
**執行**: 搜尋相同主題的經文
- 關鍵字搜尋
- 主題串連
**輸出**: 主題相關經文

## 步驟 4: 找對照經文
**執行**: 找出對比或補充的經文
- 相似教導
- 對立觀點
**輸出**: 對照經文分析

## 步驟 5: 建立經文網絡
**執行**: 繪製經文關係圖
**輸出**: 經文網絡圖

## 步驟 6: 綜合解讀
**執行**: 從多處經文理解真理
**輸出**: 綜合解經

💡 工具: search_bible, get_commentary
"""
