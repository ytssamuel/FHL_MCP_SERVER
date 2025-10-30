"""
Data models for Bible search functionality.
"""

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """
    Represents a single search result verse.
    
    Attributes:
        id: Absolute verse ID in the Bible
        book_chinese: Chinese book abbreviation
        book_english: English book abbreviation
        chapter: Chapter number
        verse: Verse number
        text: Verse text
    """

    id: int = Field(..., description="Absolute verse ID")
    book_chinese: str = Field(..., alias="chineses", description="Chinese book abbreviation")
    book_english: str = Field(..., alias="engs", description="English book abbreviation")
    chapter: int = Field(..., alias="chap", description="Chapter number")
    verse: int = Field(..., alias="sec", description="Verse number")
    text: str = Field(..., alias="bible_text", description="Verse text")

    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    """
    Response from Bible search API (se.php).
    
    Attributes:
        status: API status ("success" or "error")
        search_type: Type of search (0=keyword, 1=Greek number, 2=Hebrew number)
        query: Original search query
        record_count: Total number of results found
        results: List of matching verses
    """

    status: str | None = Field(None, description="API status")
    search_type: str = Field(..., alias="orig", description="Search type")
    query: str = Field(..., alias="key", description="Search query")
    record_count: int = Field(..., description="Number of results")
    results: list[SearchResult] = Field(default_factory=list, alias="record", description="Search results")

    class Config:
        populate_by_name = True

    @property
    def search_type_name(self) -> str:
        """Get human-readable search type name."""
        type_map = {"0": "keyword", "1": "Greek number", "2": "Hebrew number"}
        return type_map.get(self.search_type, "unknown")
