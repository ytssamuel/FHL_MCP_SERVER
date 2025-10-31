"""
FHL Bible MCP Server - Prompt Templates

⚠️ 此文件已重構為模組化結構，保留以確保向後兼容。

新的結構：
- prompts/base.py - 基礎類別
- prompts/basic/ - 基礎 prompts (basic_help_guide, basic_uri_demo, basic_quick_lookup, basic_tool_reference)
- prompts/study/ - 研經 prompts (study_verse_deep, study_topic_deep, study_translation_compare, study_word_original)
- prompts/reading/ - 閱讀 prompts (reading_daily, reading_chapter, reading_passage - Phase 2)
- prompts/manager.py - Prompt 管理器

命名規則：
- basic_*: 基礎類 prompts
- reading_*: 讀經類 prompts  
- study_*: 研經類 prompts
- special_*: 特殊類 prompts
- advanced_*: 進階類 prompts

建議使用新的導入方式：
  from fhl_bible_mcp.prompts import PromptManager
  from fhl_bible_mcp.prompts import BasicHelpGuidePrompt, StudyVerseDeepPrompt

Prompts 命名更新（向後兼容層）:
- basic_help_guide: 使用指南 → prompts/basic/basic_help_guide.py
- basic_uri_demo: URI 使用示範 → prompts/basic/basic_uri_demo.py  
- basic_quick_lookup: 快速查經 → prompts/basic/basic_quick_lookup.py
- basic_tool_reference: 工具參考 → prompts/basic/basic_tool_reference.py
- study_verse_deep: 深入研讀經文 → prompts/study/study_verse_deep.py
- study_topic_deep: 主題研究 → prompts/study/study_topic_deep.py
- study_translation_compare: 版本比較 → prompts/study/study_translation_compare.py
- study_word_original: 原文字詞研究 → prompts/study/study_word_original.py
"""

# 為向後兼容，從新模組重新導出所有類別
from .base import PromptTemplate
from .basic import (
    BasicHelpGuidePrompt,
    BasicURIDemoPrompt,
    BasicQuickLookupPrompt,
    BasicToolReferencePrompt
)
from .reading import (
    ReadingDailyPrompt,
    ReadingChapterPrompt,
    ReadingPassagePrompt
)
from .study import (
    StudyVerseDeepPrompt,
    StudyTopicDeepPrompt,
    StudyTranslationComparePrompt,
    StudyWordOriginalPrompt
)
from .special import (
    SpecialSermonPrepPrompt,
    SpecialDevotionalPrompt,
    SpecialMemoryVersePrompt,
    SpecialTopicalChainPrompt,
    SpecialBibleTriviaPrompt
)
from .manager import PromptManager

# 為了向後兼容，提供舊名稱的別名
HelpGuidePrompt = BasicHelpGuidePrompt
URIDemoPrompt = BasicURIDemoPrompt
QuickLookupPrompt = BasicQuickLookupPrompt
ToolReferencePrompt = BasicToolReferencePrompt
StudyVersePrompt = StudyVerseDeepPrompt
SearchTopicPrompt = StudyTopicDeepPrompt
CompareTranslationsPrompt = StudyTranslationComparePrompt
WordStudyPrompt = StudyWordOriginalPrompt

# Phase 3 special prompts 沒有舊名稱，直接使用新名稱
# (無需 alias，因為是新增的 prompts)

# 向後兼容的 __all__ 導出
__all__ = [
    'PromptTemplate',
    # Phase 1: Basic prompts (基礎類)
    'BasicHelpGuidePrompt',
    'BasicURIDemoPrompt',
    'BasicQuickLookupPrompt',
    'BasicToolReferencePrompt',
    # Phase 2: Reading prompts (讀經類) ✅
    'ReadingDailyPrompt',
    'ReadingChapterPrompt',
    'ReadingPassagePrompt',
    # Study prompts (研經類)
    'StudyVerseDeepPrompt',
    'StudyTopicDeepPrompt',
    'StudyTranslationComparePrompt',
    'StudyWordOriginalPrompt',
    # Phase 3: Special prompts (特殊用途) ✅
    'SpecialSermonPrepPrompt',
    'SpecialDevotionalPrompt',
    'SpecialMemoryVersePrompt',
    'SpecialTopicalChainPrompt',
    'SpecialBibleTriviaPrompt',
    # 舊名稱別名（向後兼容）
    'HelpGuidePrompt',
    'URIDemoPrompt',
    'QuickLookupPrompt',
    'ToolReferencePrompt',
    'StudyVersePrompt',
    'SearchTopicPrompt',
    'CompareTranslationsPrompt',
    'WordStudyPrompt',
    # Manager
    'PromptManager',
]
