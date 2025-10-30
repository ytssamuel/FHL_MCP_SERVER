"""
Tests for search models
"""
import pytest
from src.fhl_bible_mcp.models.search import SearchResult


def test_search_result_creation():
    """Test creating a SearchResult instance"""
    result = SearchResult(
        id=43003016,
        chineses="約",
        engs="John",
        chap=3,
        sec=16,
        bible_text="神愛世人"
    )
    
    assert result.id == 43003016
    assert result.book_chinese == "約"
    assert result.book_english == "John"
    assert result.chapter == 3
    assert result.verse == 16
    assert result.text == "神愛世人"


def test_search_result_aliases():
    """Test SearchResult field aliases"""
    result = SearchResult(
        id=43003016,
        book_chinese="約",
        book_english="John",
        chapter=3,
        verse=16,
        text="神愛世人"
    )
    
    assert result.book_chinese == "約"
    assert result.book_english == "John"
    assert result.chapter == 3
