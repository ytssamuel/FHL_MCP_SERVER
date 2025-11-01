"""
Advanced Parallel Gospels Prompt

四福音對觀研究
"""

from ..base import PromptTemplate


class AdvancedParallelGospelsPrompt(PromptTemplate):
    """進階 - 四福音對觀研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="advanced_parallel_gospels",
            description="比較四福音書的平行記載，分析異同與神學重點",
            arguments=[
                {"name": "event", "description": "事件名稱", "required": True},
                {"name": "references", "description": "平行經文引用", "required": False}
            ]
        )
    
    def render(self, event: str = "登山寶訓", references: str = "") -> str:
        """渲染四福音對觀的 prompt"""
        return f"""# 四福音對觀 - {event}

## 步驟 1: 找出平行經文
**執行**: 識別四福音中的平行記載
**輸出**: 平行經文對照表

## 步驟 2: 比較內容異同
**執行**: 逐節對比分析
- 共同記載、獨特細節、順序差異
**輸出**: 異同對照表

## 步驟 3: 分析作者視角
**執行**: 理解各作者的神學強調
- 馬太(君王)、馬可(僕人)、路加(人子)、約翰(神子)
**輸出**: 作者特色分析

## 步驟 4: 識別獨特內容
**執行**: 找出各福音書的特殊記載
**輸出**: 獨特性分析

## 步驟 5: 綜合神學意義
**執行**: 整合四福音的見證
**輸出**: 綜合神學洞見

## 步驟 6: 實際應用
**執行**: 從多角度認識真理
**輸出**: 應用建議

💡 工具: get_bible_verse, study_translation_compare
"""
