"""
MCP Tools 模組

提供所有 FHL Bible MCP Server 的工具函數。
"""

# 經文查詢工具
from .verse import (
    get_bible_verse,
    get_bible_chapter,
    query_verse_citation,
)

# 搜尋工具
from .search import (
    search_bible,
    search_bible_advanced,
)

# 原文研究工具
from .strongs import (
    get_word_analysis,
    lookup_strongs,
    search_strongs_occurrences,
)

# 註釋與研經工具
from .commentary import (
    get_commentary,
    list_commentaries,
    search_commentary,
    get_topic_study,
)

# 資訊查詢工具
from .info import (
    list_bible_versions,
    get_book_list,
    get_book_info,
    search_available_versions,
)

# 多媒體工具
from .audio import (
    get_audio_bible,
    list_audio_versions,
    get_audio_chapter_with_text,
)

__all__ = [
    # 經文查詢
    "get_bible_verse",
    "get_bible_chapter",
    "query_verse_citation",
    # 搜尋
    "search_bible",
    "search_bible_advanced",
    # 原文研究
    "get_word_analysis",
    "lookup_strongs",
    "search_strongs_occurrences",
    # 註釋與研經
    "get_commentary",
    "list_commentaries",
    "search_commentary",
    "get_topic_study",
    # 資訊查詢
    "list_bible_versions",
    "get_book_list",
    "get_book_info",
    "search_available_versions",
    # 多媒體
    "get_audio_bible",
    "list_audio_versions",
    "get_audio_chapter_with_text",
]

