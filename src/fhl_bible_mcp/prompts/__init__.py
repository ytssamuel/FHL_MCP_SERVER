"""
FHL Bible MCP Server - Prompts

提供預設的對話範本，幫助使用者快速開始聖經研讀。

模組化結構：
- base: 基礎類別
- basic: 基礎入門 prompts (help_guide, uri_demo)
- study: 深度研經 prompts (study_verse, search_topic, compare_translations, word_study)
- reading: 閱讀相關 prompts (未來實作)
- manager: Prompt 管理器
"""

# 從新的模組化結構導入
from .base import PromptTemplate
from .manager import PromptManager

# 基礎 prompts (Phase 1 完成)
from .basic import (
    HelpGuidePrompt,
    URIDemoPrompt,
    QuickLookupPrompt,
    ToolReferencePrompt
)

# 研經 prompts
from .study import (
    StudyVersePrompt,
    SearchTopicPrompt,
    CompareTranslationsPrompt,
    WordStudyPrompt
)

# 為向後兼容，保留舊的 import 路徑
# （從 templates.py 導入會自動使用新模組）
try:
    from .templates import PromptManager as _OldPromptManager
except ImportError:
    _OldPromptManager = None

__all__ = [
    # 基礎
    "PromptTemplate",
    "PromptManager",
    
    # 基礎 prompts (Phase 1 完成 ✅)
    "HelpGuidePrompt",
    "URIDemoPrompt",
    "QuickLookupPrompt",
    "ToolReferencePrompt",
    
    # 研經 prompts
    "StudyVersePrompt",
    "SearchTopicPrompt",
    "CompareTranslationsPrompt",
    "WordStudyPrompt",
]
