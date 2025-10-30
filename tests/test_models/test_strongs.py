"""
Tests for Strong's dictionary models
"""
import pytest
from src.fhl_bible_mcp.models.strongs import (
    WordAnalysisItem,
    StrongsEntry,
    RelatedWord
)


def test_word_analysis_item_summary():
    """Test WordAnalysisItem for verse summary (wid=0)"""
    item = WordAnalysisItem(
        id=43003016,
        engs="John",
        chineses="約",
        chap=3,
        sec=16,
        wid=0,
        word="οὕτως γὰρ ἠγάπησεν",
        exp="神愛世人"
    )
    
    assert item.verse_id == 43003016
    assert item.book_english == "John"
    assert item.book_chinese == "約"
    assert item.chapter == 3
    assert item.verse == 16
    assert item.word_id == 0
    assert item.is_summary  # 使用屬性而非方法


def test_word_analysis_item_word():
    """Test WordAnalysisItem for individual word"""
    item = WordAnalysisItem(
        id=43003016,
        engs="John",
        chap=3,
        sec=16,
        wid=3,
        word="ἠγάπησεν",
        sn="00025",
        pro="動詞",
        wform="第一簡單過去 主動 直說語氣",
        orig="ἀγαπάω",
        exp="愛"
    )
    
    assert item.word_id == 3
    assert item.word == "ἠγάπησεν"
    assert item.strongs_number == "00025"
    assert item.part_of_speech == "動詞"
    assert item.lemma == "ἀγαπάω"
    assert not item.is_summary  # 使用屬性而非方法


def test_strongs_entry():
    """Test StrongsEntry model"""
    entry = StrongsEntry(
        sn="00025",
        dic_text="25 agapao {ag-ap-ah'-o}",
        edic_text="25 agapao {ag-ap-ah'-o}",
        dic_type=0,
        orig="ἀγαπάω"
    )
    
    assert entry.strongs_number == "00025"
    assert entry.original_word == "ἀγαπάω"
    assert "agapao" in entry.chinese_definition


def test_related_word():
    """Test RelatedWord model"""
    related = RelatedWord(
        word="ἀγάπη, ης, ἡ",
        csn="00026",
        ccnt=116,  # 使用整數類型
        cexp="愛；愛餐"
    )
    
    assert related.word == "ἀγάπη, ης, ἡ"
    assert related.strongs_number == "00026"
    assert related.occurrences == 116  # 期望整數
    assert "愛" in related.gloss
