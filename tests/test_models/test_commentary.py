"""
Tests for commentary models
"""
import pytest
from src.fhl_bible_mcp.models.commentary import (
    CommentaryInfo,
    CommentaryEntry
)


def test_commentary_info():
    """Test CommentaryInfo model"""
    info = CommentaryInfo(
        id=1,
        name="信望愛註釋"
    )
    
    assert info.id == 1
    assert info.name == "信望愛註釋"


def test_commentary_entry():
    """Test CommentaryEntry model"""
    entry = CommentaryEntry(
        title="約翰福音 3:16",
        book_name="信望愛註釋",
        com_text="神愛世人的偉大宣告..."
    )
    
    assert entry.title == "約翰福音 3:16"
    assert entry.commentary_name == "信望愛註釋"
    assert "神愛世人" in entry.text


def test_commentary_entry_with_navigation():
    """Test CommentaryEntry with previous/next navigation"""
    entry = CommentaryEntry(
        title="約翰福音 3:16",
        book_name="信望愛註釋",
        com_text="神愛世人...",
        prev={"book": "John", "chapter": 3, "verse": 15},
        next={"book": "John", "chapter": 3, "verse": 17}
    )
    
    assert entry.previous is not None
    assert entry.next is not None
    assert entry.previous["verse"] == 15
    assert entry.next["verse"] == 17
