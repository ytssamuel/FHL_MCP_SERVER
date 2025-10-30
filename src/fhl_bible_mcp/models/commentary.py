"""
Data models for Bible commentary.
"""

from pydantic import BaseModel, Field


class CommentaryInfo(BaseModel):
    """
    Basic information about a commentary.
    
    Attributes:
        id: Commentary ID
        name: Commentary name
    """

    id: int = Field(..., description="Commentary ID")
    name: str = Field(..., description="Commentary name")


class CommentaryEntry(BaseModel):
    """
    A single commentary entry for a verse or passage.
    
    Attributes:
        title: Entry title
        commentary_name: Name of the commentary
        text: Commentary text content
        previous: Previous section info
        next: Next section info
    """

    title: str = Field(..., description="Entry title")
    commentary_name: str = Field(..., alias="book_name", description="Commentary name")
    text: str = Field(..., alias="com_text", description="Commentary text")
    previous: dict | None = Field(None, alias="prev", description="Previous section")
    next: dict | None = Field(None, description="Next section")

    class Config:
        populate_by_name = True


class CommentaryResponse(BaseModel):
    """
    Response from commentary query API (sc.php).
    
    Attributes:
        status: API status
        record_count: Number of commentary entries
        entries: List of commentary entries
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of entries")
    entries: list[CommentaryEntry] = Field(..., alias="record", description="Commentary entries")

    class Config:
        populate_by_name = True


class CommentaryListResponse(BaseModel):
    """
    Response from commentary list API (sc.php?validbook=1).
    
    Attributes:
        status: API status
        record_count: Number of commentaries
        commentaries: List of available commentaries
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of commentaries")
    commentaries: list[CommentaryInfo] = Field(..., alias="record", description="Commentaries")

    class Config:
        populate_by_name = True


class CommentarySearchResult(BaseModel):
    """
    A search result from commentary search.
    
    Attributes:
        title: Result title
        commentary_id: Commentary book ID
        commentary_name: Commentary name
        book_chinese_full: Chinese book full name
        book_english: English book abbreviation
        start_chapter: Starting chapter
        start_verse: Starting verse
        end_chapter: Ending chapter
        end_verse: Ending verse
    """

    title: str = Field(..., description="Result title")
    commentary_id: int = Field(..., alias="tag", description="Commentary ID")
    commentary_name: str = Field(..., alias="book_name", description="Commentary name")
    book_chinese_full: str = Field(..., alias="chinesef", description="Chinese book full name")
    book_english: str = Field(..., alias="engs", description="English book abbreviation")
    start_chapter: int = Field(..., alias="bchap", description="Start chapter")
    start_verse: int = Field(..., alias="bsec", description="Start verse")
    end_chapter: int = Field(..., alias="echap", description="End chapter")
    end_verse: int = Field(..., alias="esec", description="End verse")

    class Config:
        populate_by_name = True


class CommentarySearchResponse(BaseModel):
    """
    Response from commentary search API (ssc.php).
    
    Attributes:
        status: API status (optional in some responses)
        record_count: Number of results
        results: List of search results
    """

    status: str | None = Field(None, description="API status")
    record_count: int = Field(..., description="Number of results")
    results: list[CommentarySearchResult] = Field(
        default_factory=list, alias="record", description="Search results"
    )

    class Config:
        populate_by_name = True
