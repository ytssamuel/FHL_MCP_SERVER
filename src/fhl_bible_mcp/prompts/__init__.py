"""
FHL Bible MCP Server - Prompts

提供預設的對話範本，幫助使用者快速開始聖經研讀。
"""

from .templates import (
    PromptTemplate,
    StudyVersePrompt,
    SearchTopicPrompt,
    CompareTranslationsPrompt,
    WordStudyPrompt,
    PromptManager
)

__all__ = [
    "PromptTemplate",
    "StudyVersePrompt",
    "SearchTopicPrompt",
    "CompareTranslationsPrompt",
    "WordStudyPrompt",
    "PromptManager"
]
