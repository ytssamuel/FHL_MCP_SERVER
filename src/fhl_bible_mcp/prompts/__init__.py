"""
FHL Bible MCP Server - Prompts

提供預設的對話範本，幫助使用者快速開始聖經研讀。

模組化結構：
- base: 基礎類別
- basic: 基礎入門 prompts (basic_help_guide, basic_uri_demo, basic_quick_lookup, basic_tool_reference)
- reading: 讀經輔助 prompts (reading_daily, reading_chapter, reading_passage) ✅
- study: 深度研經 prompts (study_verse_deep, study_topic_deep, study_translation_compare, study_word_original)
- manager: Prompt 管理器

命名規則：
- basic_*: 基礎類 prompts (適合新手)
- reading_*: 讀經類 prompts (日常讀經)
- study_*: 研經類 prompts (深度研究)
- special_*: 特殊類 prompts (特定用途)
- advanced_*: 進階類 prompts (進階功能)
"""

# 從新的模組化結構導入
from .base import PromptTemplate
from .manager import PromptManager

# 基礎 prompts (Phase 1 完成 ✅)
from .basic import (
    BasicHelpGuidePrompt,
    BasicURIDemoPrompt,
    BasicQuickLookupPrompt,
    BasicToolReferencePrompt
)

# 讀經 prompts (Phase 2 完成 ✅)
from .reading import (
    ReadingDailyPrompt,
    ReadingChapterPrompt,
    ReadingPassagePrompt
)

# 研經 prompts (深度研究)
from .study import (
    StudyVerseDeepPrompt,
    StudyTopicDeepPrompt,
    StudyTranslationComparePrompt,
    StudyWordOriginalPrompt
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
    "BasicHelpGuidePrompt",
    "BasicURIDemoPrompt",
    "BasicQuickLookupPrompt",
    "BasicToolReferencePrompt",
    
    # 讀經 prompts (Phase 2 完成 ✅)
    "ReadingDailyPrompt",
    "ReadingChapterPrompt",
    "ReadingPassagePrompt",
    
    # 研經 prompts (深度研究)
    "StudyVerseDeepPrompt",
    "StudyTopicDeepPrompt",
    "StudyTranslationComparePrompt",
    "StudyWordOriginalPrompt",
]
