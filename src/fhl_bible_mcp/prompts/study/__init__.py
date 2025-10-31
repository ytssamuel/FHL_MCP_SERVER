"""
Study prompts module - 深度研經 Prompts
"""

from .study_verse import StudyVersePrompt
from .search_topic import SearchTopicPrompt
from .compare_translations import CompareTranslationsPrompt
from .word_study import WordStudyPrompt

__all__ = [
    'StudyVersePrompt',
    'SearchTopicPrompt',
    'CompareTranslationsPrompt',
    'WordStudyPrompt',
]
