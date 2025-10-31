"""特殊用途 Prompts

這個模組包含特殊用途的對話範本：
- SpecialSermonPrepPrompt: 講道準備
- SpecialDevotionalPrompt: 靈修材料
- SpecialMemoryVersePrompt: 背經輔助
- SpecialTopicalChainPrompt: 主題串連
- SpecialBibleTriviaPrompt: 聖經問答
"""

from .special_sermon_prep import SpecialSermonPrepPrompt
from .special_devotional import SpecialDevotionalPrompt
from .special_memory_verse import SpecialMemoryVersePrompt
from .special_topical_chain import SpecialTopicalChainPrompt
from .special_bible_trivia import SpecialBibleTriviaPrompt

__all__ = [
    "SpecialSermonPrepPrompt",
    "SpecialDevotionalPrompt",
    "SpecialMemoryVersePrompt",
    "SpecialTopicalChainPrompt",
    "SpecialBibleTriviaPrompt",
]
