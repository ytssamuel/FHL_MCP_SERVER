"""
Study prompts module - 深度研經 Prompts
"""

from .study_verse_deep import StudyVerseDeepPrompt
from .study_topic_deep import StudyTopicDeepPrompt
from .study_translation_compare import StudyTranslationComparePrompt
from .study_word_original import StudyWordOriginalPrompt

__all__ = [
    'StudyVerseDeepPrompt',
    'StudyTopicDeepPrompt',
    'StudyTranslationComparePrompt',
    'StudyWordOriginalPrompt',
]
