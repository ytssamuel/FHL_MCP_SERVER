"""
Data models for Strong's dictionary and word analysis.
"""

from pydantic import BaseModel, Field


class WordAnalysisItem(BaseModel):
    """
    Represents analysis of a single word in original language.
    
    Attributes:
        verse_id: Absolute verse ID
        book_english: English book abbreviation
        chapter: Chapter number
        verse: Verse number
        word_id: Word position (0 for verse summary)
        word: Original word (or full verse if word_id=0)
        strongs_number: Strong's number (if word_id>0)
        part_of_speech: Part of speech (if word_id>0)
        morphology: Morphological analysis (if word_id>0)
        lemma: Dictionary form (if word_id>0)
        gloss: Translation/meaning
        note: Additional notes
    """

    verse_id: int = Field(..., alias="id", description="Absolute verse ID")
    book_english: str = Field(..., alias="engs", description="English book abbreviation")
    chapter: int = Field(..., alias="chap", description="Chapter number")
    verse: int = Field(..., alias="sec", description="Verse number")
    word_id: int = Field(..., alias="wid", description="Word position (0=summary)")
    word: str = Field(..., description="Original word or verse text")
    strongs_number: str | None = Field(None, alias="sn", description="Strong's number")
    part_of_speech: str | None = Field(None, alias="pro", description="Part of speech")
    morphology: str | None = Field(None, alias="wform", description="Morphological analysis")
    lemma: str | None = Field(None, alias="orig", description="Dictionary form")
    gloss: str = Field(..., alias="exp", description="Translation/meaning")
    note: str | None = Field(None, alias="remark", description="Additional notes")
    
    # For word_id=0 only
    book_chinese: str | None = Field(None, alias="chineses", description="Chinese book abbreviation")
    book_chinese_full: str | None = Field(None, alias="chinesef", description="Chinese book full name")

    class Config:
        populate_by_name = True

    @property
    def is_summary(self) -> bool:
        """Check if this is the verse summary (word_id=0)."""
        return self.word_id == 0


class WordAnalysisResponse(BaseModel):
    """
    Response from word analysis API (qp.php).
    
    Attributes:
        status: API status
        record_count: Number of words + 1 (verse summary)
        testament: Testament (0=NT, 1=OT)
        previous: Previous verse navigation
        next: Next verse navigation
        words: List of word analysis items
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of items")
    testament: int = Field(..., alias="N", description="Testament (0=NT, 1=OT)")
    previous: dict | None = Field(None, alias="prev", description="Previous verse")
    next: dict | None = Field(None, description="Next verse")
    words: list[WordAnalysisItem] = Field(..., alias="record", description="Word analysis items")

    class Config:
        populate_by_name = True

    @property
    def testament_name(self) -> str:
        """Get testament name."""
        return "New Testament" if self.testament == 0 else "Old Testament"

    @property
    def verse_summary(self) -> WordAnalysisItem | None:
        """Get the verse summary (word_id=0)."""
        for word in self.words:
            if word.is_summary:
                return word
        return None

    @property
    def individual_words(self) -> list[WordAnalysisItem]:
        """Get only individual word analysis (word_id>0)."""
        return [w for w in self.words if not w.is_summary]


class RelatedWord(BaseModel):
    """
    Represents a word related to a Strong's entry (cognates).
    
    Attributes:
        word: Original word
        strongs_number: Strong's number
        occurrences: Number of occurrences in Bible
        gloss: Chinese meaning
    """

    word: str = Field(..., description="Original word")
    strongs_number: str = Field(..., alias="csn", description="Strong's number")
    occurrences: int = Field(..., alias="ccnt", description="Occurrence count")
    gloss: str = Field(..., alias="cexp", description="Chinese meaning")

    class Config:
        populate_by_name = True


class StrongsEntry(BaseModel):
    """
    Represents a Strong's dictionary entry.
    
    Attributes:
        strongs_number: Strong's number (with leading zeros)
        chinese_definition: Chinese dictionary text
        english_definition: English dictionary text
        dictionary_type: 0 for NT (Greek), 1 for OT (Hebrew)
        original_word: The original Greek/Hebrew word
        related_words: List of related/cognate words (NT only)
    """

    strongs_number: str = Field(..., alias="sn", description="Strong's number")
    chinese_definition: str = Field(..., alias="dic_text", description="Chinese definition")
    english_definition: str = Field(..., alias="edic_text", description="English definition")
    dictionary_type: int = Field(..., alias="dic_type", description="Dictionary type (0=NT, 1=OT)")
    original_word: str = Field(..., alias="orig", description="Original word")
    related_words: list[RelatedWord] = Field(
        default_factory=list, alias="same", description="Related words"
    )

    class Config:
        populate_by_name = True

    @property
    def testament(self) -> str:
        """Get testament name."""
        return "New Testament" if self.dictionary_type == 0 else "Old Testament"

    @property
    def language(self) -> str:
        """Get language name."""
        return "Greek" if self.dictionary_type == 0 else "Hebrew"


class StrongsDictionaryResponse(BaseModel):
    """
    Response from Strong's dictionary API (sd.php).
    
    Attributes:
        status: API status
        record_count: Should be 1
        entries: List containing one dictionary entry
    """

    status: str = Field(..., description="API status")
    record_count: int = Field(..., description="Number of entries")
    entries: list[StrongsEntry] = Field(..., alias="record", description="Dictionary entries")

    class Config:
        populate_by_name = True

    @property
    def entry(self) -> StrongsEntry | None:
        """Get the first (and only) entry."""
        return self.entries[0] if self.entries else None
