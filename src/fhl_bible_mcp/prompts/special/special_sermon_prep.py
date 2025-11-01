"""
FHL Bible MCP Server - Sermon Prep Prompt

講道準備輔助
"""

from ..base import PromptTemplate


class SpecialSermonPrepPrompt(PromptTemplate):
    """特殊 - 講道準備 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_sermon_prep",
            description="輔助講道準備，從釋經到應用的完整流程",
            arguments=[
                {"name": "passage", "description": "講道經文", "required": True},
                {"name": "sermon_type", "description": "講道類型", "required": False}
            ]
        )
    
    def render(self, passage: str = "約翰福音 3:16", sermon_type: str = "expository") -> str:
        """渲染講道準備的 prompt"""
        return f"""# 講道準備 - {passage} ({sermon_type})

## 步驟 1: 研讀經文
**執行**: 深入理解經文
- 獲取經文、查閱註釋、原文分析
**輸出**: 釋經基礎

## 步驟 2: 找出大綱
**執行**: 建立講章結構 (3-5點)
**輸出**: 講道大綱

## 步驟 3: 發展內容
**執行**: 充實各論點
- 解釋意義、相關經文、例證說明
**輸出**: 講道內容草稿

## 步驟 4: 連結應用
**執行**: 將真理應用到生活
**輸出**: 應用部分

## 步驟 5: 設計引言與結語
**執行**: 完善講道框架
**輸出**: 完整講章

## 步驟 6: 準備輔助材料
**執行**: 準備投影片與講義
**輸出**: 輔助材料清單

💡 工具: study_verse_deep, get_commentary
"""
