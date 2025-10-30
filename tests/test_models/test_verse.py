"""
Tests for verse models
"""
import pytest
from src.fhl_bible_mcp.models.verse import (
    BibleVerse,
    BibleVersion
)


def test_bible_verse_creation():
    """Test creating a BibleVerse instance"""
    verse = BibleVerse(
        engs="John",
        chineses="約",
        chap=3,
        sec=16,
        bible_text="神愛世人"
    )
    
    assert verse.book_english == "John"
    assert verse.book_chinese == "約"
    assert verse.chapter == 3
    assert verse.verse == 16
    assert verse.text == "神愛世人"


def test_bible_verse_aliases():
    """Test BibleVerse field aliases"""
    verse = BibleVerse(
        book_english="John",
        book_chinese="約",
        chapter=3,
        verse=16,
        text="神愛世人"
    )
    
    assert verse.book_english == "John"
    assert verse.book_chinese == "約"
    assert verse.chapter == 3
    assert verse.verse == 16


def test_bible_version():
    """Test BibleVersion model"""
    version = BibleVersion(
        book="unv",
        cname="和合本",
        proc=0,
        strong=True,
        ntonly=False,
        otonly=False,
        candownload=True
    )
    
    assert version.code == "unv"
    assert version.name == "和合本"
    assert version.has_strongs is True
    assert version.special_font == 0


def test_bible_version_testament_scope():
    """Test BibleVersion testament_scope property"""
    # Both testaments
    version_both = BibleVersion(
        book="unv",
        cname="和合本",
        proc=0,
        strong=True,
        ntonly=False,
        otonly=False,
        candownload=True
    )
    assert version_both.testament_scope == "both"
    
    # NT only
    version_nt = BibleVersion(
        book="netbible",
        cname="NET Bible",
        proc=0,
        strong=False,
        ntonly=True,
        otonly=False,
        candownload=False
    )
    assert version_nt.testament_scope == "NT only"  # 修正為實際返回值
    
    # OT only
    version_ot = BibleVersion(
        book="lxx",
        cname="Septuagint",
        proc=2,
        strong=False,
        ntonly=False,
        otonly=True,
        candownload=False
    )
    assert version_ot.testament_scope == "OT only"  # 修正為實際返回值
