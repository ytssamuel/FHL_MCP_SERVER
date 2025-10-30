"""
Data models for Bible verses and related data.
"""

from typing import Any

from pydantic import BaseModel, Field


class BibleVerse(BaseModel):
    """
    Represents a single Bible verse.
    
    Attributes:
        book_english: English book abbreviation
        book_chinese: Chinese book abbreviation
        chapter: Chapter number
        verse: Verse number
        text: Verse text content
    """

    book_english: str = Field(..., alias="engs", description="English book abbreviation")
    book_chinese: str = Field(..., alias="chineses", description="Chinese book abbreviation")
    chapter: int = Field(..., alias="chap", description="Chapter number")
    verse: int = Field(..., alias="sec", description="Verse number")
    text: str = Field(..., alias="bible_text", description="Verse text")

    class Config:
        populate_by_name = True


class NavigationInfo(BaseModel):
    """
    Navigation information for previous/next verse or chapter.
    
    Attributes:
        book_chinese: Chinese book abbreviation
        book_english: English book abbreviation
        chapter: Chapter number
        verse: Verse number (optional)
    """

    book_chinese: str = Field(..., alias="chineses", description="Chinese book abbreviation")
    book_english: str = Field(..., alias="engs", description="English book abbreviation")
    chapter: int = Field(..., alias="chap", description="Chapter number")
    verse: int | None = Field(None, alias="sec", description="Verse number")

    class Config:
        populate_by_name = True


class VerseQueryResponse(BaseModel):
    """
    Response from verse query API (qb.php).
    
    Attributes:
        status: API status ("success" or "error")
        record_count: Number of verses returned
        version_name: Full name of the Bible version
        version_code: Short code of the Bible version
        special_font: Special font requirement (0-4)
        verses: List of verses
        previous: Previous verse/chapter info
        next: Next verse/chapter info
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of verses")
    version_name: str = Field(..., alias="v_name", description="Version full name")
    version_code: str = Field(..., alias="version", description="Version code")
    special_font: int = Field(..., alias="proc", description="Special font requirement")
    verses: list[BibleVerse] = Field(..., alias="record", description="List of verses")
    previous: NavigationInfo | None = Field(None, alias="prev", description="Previous verse info")
    next: NavigationInfo | None = Field(None, description="Next verse info")

    class Config:
        populate_by_name = True


class BibleVersion(BaseModel):
    """
    Represents a Bible version/translation.
    
    Attributes:
        code: Version code (e.g., "unv", "kjv")
        name: Version full name
        special_font: Special font requirement (0=none, 1=Greek, 2=Hebrew, 3=Romanization, 4=OpenHan)
        has_strongs: Whether it includes Strong's numbers
        new_testament_only: Whether it's NT only
        old_testament_only: Whether it's OT only
        can_download: Whether offline data can be downloaded
        last_updated: Last update timestamp
    """

    code: str = Field(..., alias="book", description="Version code")
    name: str = Field(..., alias="cname", description="Version full name")
    special_font: int = Field(..., alias="proc", description="Special font requirement")
    has_strongs: bool = Field(..., alias="strong", description="Has Strong's numbers")
    new_testament_only: bool = Field(..., alias="ntonly", description="New Testament only")
    old_testament_only: bool = Field(..., alias="otonly", description="Old Testament only")
    can_download: bool = Field(
        ..., alias="candownload", description="Can download offline data"
    )
    last_updated: str | None = Field(None, alias="version", description="Last update time")

    class Config:
        populate_by_name = True

    @property
    def testament_scope(self) -> str:
        """Get the testament scope as a string."""
        if self.new_testament_only:
            return "NT only"
        elif self.old_testament_only:
            return "OT only"
        else:
            return "both"


class BibleVersionsResponse(BaseModel):
    """
    Response from Bible versions list API (ab.php).
    
    Attributes:
        status: API status
        record_count: Number of versions
        versions: List of Bible versions
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of versions")
    versions: list[BibleVersion] = Field(..., alias="record", description="List of versions")

    class Config:
        populate_by_name = True
