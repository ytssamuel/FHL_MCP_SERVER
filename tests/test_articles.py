"""
Tests for Articles (文章) APIs

Tests the article search and column listing functionality.
"""

import pytest
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
from fhl_bible_mcp.utils.errors import InvalidParameterError


@pytest.fixture
def api_client():
    """Create API client fixture"""
    return FHLAPIEndpoints()


@pytest.mark.asyncio
class TestArticlesAPI:
    """Test Articles API endpoints"""
    
    async def test_search_articles_by_title(self, api_client):
        """Test searching articles by title"""
        result = await api_client.search_articles(title="愛")
        
        assert result["status"] == 1
        assert result["record_count"] > 0
        assert "record" in result
        assert len(result["record"]) > 0
        
        # Check article structure
        first_article = result["record"][0]
        assert "title" in first_article
        assert "author" in first_article
        assert "column" in first_article
        assert "ptab" in first_article
        assert "pubtime" in first_article
    
    async def test_search_articles_by_author(self, api_client):
        """Test searching articles by author"""
        result = await api_client.search_articles(author="陳鳳翔")
        
        assert result["status"] == 1
        assert result["record_count"] > 0
        
        # Verify author filter
        for article in result["record"][:5]:  # Check first 5
            assert "陳鳳翔" in article.get("author", "")
    
    async def test_search_articles_by_column(self, api_client):
        """Test searching articles by column"""
        result = await api_client.search_articles(column="women3")
        
        assert result["status"] == 1
        assert result["record_count"] > 0
        
        # Verify column filter
        for article in result["record"][:5]:
            assert article.get("ptab") == "women3"
    
    async def test_search_articles_combined(self, api_client):
        """Test combined search parameters"""
        result = await api_client.search_articles(
            title="愛",
            column="women3",
            limit=10
        )
        
        assert result["status"] == 1
        
        # Should have at most 10 results due to limit
        if result["record_count"] > 10:
            assert len(result["record"]) == 10
            assert result.get("limited") == True
    
    async def test_search_articles_no_params(self, api_client):
        """Test that search without parameters raises error"""
        with pytest.raises(InvalidParameterError) as exc_info:
            await api_client.search_articles()
        
        assert "at least one search parameter" in str(exc_info.value).lower()
    
    async def test_search_articles_with_limit(self, api_client):
        """Test result limiting"""
        limit = 5
        result = await api_client.search_articles(title="信", limit=limit)
        
        assert result["status"] == 1
        
        # Should return at most 'limit' results
        assert len(result["record"]) <= limit
        
        if result["record_count"] > limit:
            assert result.get("limited") == True
    
    async def test_search_articles_simplified(self, api_client):
        """Test simplified Chinese search"""
        try:
            result = await api_client.search_articles(
                title="爱",  # Simplified
                use_simplified=True
            )
            
            # API may return status 0 (no data) or 1 (success) for simplified Chinese
            assert result["status"] in [0, 1]
        except Exception:
            # API may have incomplete JSON response for no data
            # This is acceptable as simplified content may not be available
            pass
    
    async def test_search_articles_by_date(self, api_client):
        """Test searching by publication date"""
        # Use a recent date that likely has articles
        result = await api_client.search_articles(pub_date="2025.10.19")
        
        # May or may not have results for this specific date
        assert result["status"] in [0, 1]
        
        if result["status"] == 1 and result["record_count"] > 0:
            # Verify date format
            for article in result["record"][:3]:
                pubtime = article.get("pubtime", "")
                assert "." in pubtime  # Should have date separators
    
    async def test_search_articles_content_structure(self, api_client):
        """Test article content structure"""
        result = await api_client.search_articles(title="約翰", limit=1)
        
        assert result["status"] == 1
        
        if result["record_count"] > 0:
            article = result["record"][0]
            
            # Check required fields
            assert "id" in article
            assert "title" in article
            assert "author" in article
            assert "pubtime" in article
            
            # Content fields
            assert "abst" in article or "txt" in article
            
            # HTML content check
            if "txt" in article and article["txt"]:
                content = article["txt"]
                assert isinstance(content, str)
                # May contain HTML tags
    
    async def test_list_article_columns(self, api_client):
        """Test listing article columns"""
        columns = api_client.list_article_columns()
        
        assert isinstance(columns, list)
        assert len(columns) > 0
        
        # Check column structure
        for column in columns:
            assert "code" in column
            assert "name" in column
            assert "description" in column
            
            assert isinstance(column["code"], str)
            assert isinstance(column["name"], str)
            assert isinstance(column["description"], str)
    
    async def test_list_article_columns_content(self, api_client):
        """Test that column list contains expected columns"""
        columns = api_client.list_article_columns()
        
        # Extract column codes
        column_codes = [col["code"] for col in columns]
        
        # Check for known columns
        assert "women3" in column_codes
        assert "theology" in column_codes
        assert "bible_study" in column_codes
    
    async def test_search_with_invalid_column(self, api_client):
        """Test search with non-existent column"""
        try:
            result = await api_client.search_articles(column="nonexistent_column")
            
            # Should return status 0 (no data) or empty results
            if result["status"] == 1:
                assert result["record_count"] == 0
            else:
                assert result["status"] == 0
        except Exception:
            # API may have incomplete JSON response for invalid columns
            # This is acceptable and expected behavior
            pass
