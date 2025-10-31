"""
Advanced Prompts Module

進階功能對話範本，包含：
- advanced_cross_reference: 交叉引用分析
- advanced_parallel_gospels: 符類福音對照
- advanced_character_study: 聖經人物研究
"""

from .advanced_cross_reference import AdvancedCrossReferencePrompt
from .advanced_parallel_gospels import AdvancedParallelGospelsPrompt
from .advanced_character_study import AdvancedCharacterStudyPrompt

__all__ = [
    "AdvancedCrossReferencePrompt",
    "AdvancedParallelGospelsPrompt",
    "AdvancedCharacterStudyPrompt",
]
