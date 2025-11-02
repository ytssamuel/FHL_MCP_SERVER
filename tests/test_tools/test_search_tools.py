"""
Unit tests for search tools

測試搜尋工具的功能，包括關鍵字搜尋、原文編號搜尋、範圍搜尋等。
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.fhl_bible_mcp.tools.search import search_bible, search_bible_advanced
from src.fhl_bible_mcp.utils.errors import InvalidParameterError


@pytest.mark.asyncio
async def test_search_bible_keyword():
    """測試關鍵字搜尋"""
    mock_response = {
        "status": "success",
        "record_count": 2,
        "record": [
            {
                "chineses": "約翰福音",
                "engs": "John",
                "chap": "3",
                "sec": "16",
                "bible_text": "神愛世人..."
            },
            {
                "chineses": "約翰一書",
                "engs": "1John",
                "chap": "4",
                "sec": "8",
                "bible_text": "神就是愛..."
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="愛", search_type="keyword", scope="all")
        
        assert result["total_count"] == 2
        assert result["query"] == "愛"
        assert result["search_type"] == "keyword"
        assert result["scope"] == "all"
        assert len(result["results"]) == 2
        assert result["results"][0]["book"] == "約翰福音"
        assert result["results"][0]["text"] == "神愛世人..."


@pytest.mark.asyncio
async def test_search_bible_count_only():
    """測試只返回計數"""
    mock_response = {
        "status": "success",
        "record_count": 365,
        "record": []
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="神", count_only=True)
        
        assert result["total_count"] == 365
        assert result["query"] == "神"
        assert "results" not in result


@pytest.mark.asyncio
async def test_search_bible_greek_strong():
    """測試希臘文原文編號搜尋"""
    mock_response = {
        "status": "success",
        "record_count": 1,
        "record": [
            {
                "chineses": "約翰福音",
                "engs": "John",
                "chap": "1",
                "sec": "1",
                "bible_text": "太初有道..."
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="G3056", search_type="greek_number", scope="nt")
        
        assert result["search_type"] == "greek_number"
        assert result["scope"] == "nt"
        assert len(result["results"]) == 1


@pytest.mark.asyncio
async def test_search_bible_hebrew_strong():
    """測試希伯來文原文編號搜尋"""
    mock_response = {
        "status": "success",
        "record_count": 1,
        "record": [
            {
                "chineses": "創世記",
                "engs": "Genesis",
                "chap": "1",
                "sec": "1",
                "bible_text": "起初神創造天地"
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="H1254", search_type="hebrew_number", scope="ot")
        
        assert result["search_type"] == "hebrew_number"
        assert result["scope"] == "ot"


@pytest.mark.asyncio
async def test_search_bible_invalid_search_type():
    """測試無效的搜尋類型"""
    with pytest.raises(InvalidParameterError) as exc_info:
        await search_bible(query="test", search_type="invalid")
    
    assert "無效的搜尋類型" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_bible_invalid_scope():
    """測試無效的搜尋範圍"""
    with pytest.raises(InvalidParameterError) as exc_info:
        await search_bible(query="test", scope="invalid")
    
    assert "無效的搜尋範圍" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_bible_with_pagination():
    """測試分頁參數"""
    mock_response = {
        "status": "success",
        "record_count": 100,
        "record": [
            {
                "chineses": "約翰福音",
                "engs": "John",
                "chap": "3",
                "sec": "16",
                "bible_text": "神愛世人..."
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="神", limit=10, offset=20)
        
        assert result["limit"] == 10
        assert result["offset"] == 20
        assert result["total_count"] == 100


@pytest.mark.asyncio
async def test_search_bible_advanced_no_range():
    """測試進階搜尋（無範圍，應退回一般搜尋）"""
    mock_response = {
        "status": "success",
        "record_count": 1,
        "record": [
            {
                "chineses": "約翰福音",
                "engs": "John",
                "chap": "1",
                "sec": "1",
                "bible_text": "太初有道..."
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        # 不提供範圍
        result = await search_bible_advanced(query="道")
        
        assert result["total_count"] == 1
        assert "range" not in result


@pytest.mark.asyncio
async def test_search_bible_advanced_with_range():
    """測試進階搜尋（指定書卷範圍）"""
    mock_response = {
        "status": "success",
        "record_count": 5,
        "record": [
            {
                "chineses": "創世記",
                "engs": "Genesis",
                "chap": "1",
                "sec": "1",
                "bible_text": "起初神創造天地"
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        with patch('src.fhl_bible_mcp.tools.search.BookNameConverter') as mock_converter:
            mock_converter.get_book_id = MagicMock(side_effect=[1, 5])  # 創世記=1, 申命記=5
            
            result = await search_bible_advanced(
                query="神",
                range_start="創世記",
                range_end="申命記"
            )
            
            assert result["total_count"] == 5
            assert result["range"]["start"] == "創世記"
            assert result["range"]["end"] == "申命記"


@pytest.mark.asyncio
async def test_search_bible_advanced_invalid_range():
    """測試進階搜尋（無效的書卷範圍）"""
    with patch('src.fhl_bible_mcp.tools.search.BookNameConverter') as mock_converter:
        mock_converter.get_book_id = MagicMock(return_value=None)
        
        with pytest.raises(InvalidParameterError) as exc_info:
            await search_bible_advanced(
                query="神",
                range_start="無效書卷",
                range_end="申命記"
            )
        
        assert "無效的書卷範圍" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_bible_advanced_reversed_range():
    """測試進階搜尋（起始書卷大於結束書卷）"""
    with patch('src.fhl_bible_mcp.tools.search.BookNameConverter') as mock_converter:
        mock_converter.get_book_id = MagicMock(side_effect=[5, 1])  # 申命記=5, 創世記=1
        
        with pytest.raises(InvalidParameterError) as exc_info:
            await search_bible_advanced(
                query="神",
                range_start="申命記",
                range_end="創世記"
            )
        
        assert "起始書卷不能大於結束書卷" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_bible_advanced_invalid_search_type():
    """測試進階搜尋（無效的搜尋類型）"""
    with patch('src.fhl_bible_mcp.tools.search.BookNameConverter') as mock_converter:
        mock_converter.get_book_id = MagicMock(side_effect=[1, 5])
        
        with pytest.raises(InvalidParameterError) as exc_info:
            await search_bible_advanced(
                query="神",
                search_type="invalid",
                range_start="創世記",
                range_end="申命記"
            )
        
        assert "無效的搜尋類型" in str(exc_info.value)


@pytest.mark.asyncio
async def test_search_bible_result_formatting():
    """測試搜尋結果格式化"""
    mock_response = {
        "status": "success",
        "record_count": 1,
        "record": [
            {
                "chineses": "馬太福音",
                "engs": "Matthew",
                "chap": "5",
                "sec": "3",
                "bible_text": "虛心的人有福了"
            }
        ]
    }
    
    with patch('src.fhl_bible_mcp.tools.search.FHLAPIEndpoints') as mock_api_class:
        mock_api_instance = AsyncMock()
        mock_api_instance.search_bible = AsyncMock(return_value=mock_response)
        mock_api_class.return_value.__aenter__.return_value = mock_api_instance
        
        result = await search_bible(query="福")
        
        # 驗證結果格式
        assert "results" in result
        assert len(result["results"]) == 1
        
        first_result = result["results"][0]
        assert first_result["book"] == "馬太福音"
        assert first_result["book_eng"] == "Matthew"
        assert first_result["chapter"] == "5"
        assert first_result["verse"] == "3"
        assert first_result["text"] == "虛心的人有福了"
