"""
FHL Bible MCP Server - Prompt Templates

⚠️ 此文件已重構為模組化結構，保留以確保向後兼容。

新的結構：
- prompts/base.py - 基礎類別
- prompts/basic/ - 基礎 prompts (help_guide, uri_demo)
- prompts/study/ - 研經 prompts (study_verse, search_topic, compare_translations, word_study)
- prompts/reading/ - 閱讀 prompts (未來實作)
- prompts/manager.py - Prompt 管理器

建議使用新的導入方式：
  from fhl_bible_mcp.prompts import PromptManager
  from fhl_bible_mcp.prompts import StudyVersePrompt, HelpGuidePrompt

舊的 Prompts（向後兼容，已遷移至新模組）:
- help_guide: 使用指南和快速開始 → prompts/basic/help_guide.py
- uri_demo: URI 使用教學和示範 → prompts/basic/uri_demo.py
- study_verse: 深入研讀經文 → prompts/study/study_verse.py
- search_topic: 主題研究 → prompts/study/search_topic.py
- compare_translations: 版本比較 → prompts/study/compare_translations.py
- word_study: 原文字詞研究 → prompts/study/word_study.py
"""

# 為向後兼容，從新模組重新導出所有類別
from .base import PromptTemplate
from .basic import (
    HelpGuidePrompt,
    URIDemoPrompt,
    QuickLookupPrompt,
    ToolReferencePrompt
)
from .study import (
    StudyVersePrompt,
    SearchTopicPrompt,
    CompareTranslationsPrompt,
    WordStudyPrompt
)
from .manager import PromptManager

# 向後兼容的 __all__ 導出
__all__ = [
    'PromptTemplate',
    'HelpGuidePrompt',
    'URIDemoPrompt',
    'QuickLookupPrompt',
    'ToolReferencePrompt',
    'StudyVersePrompt',
    'SearchTopicPrompt',
    'CompareTranslationsPrompt',
    'WordStudyPrompt',
    'PromptManager',
]
