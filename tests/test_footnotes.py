"""
Tests for Footnotes (註腳) APIs

Tests the footnote query functionality (rt.php).
"""

import pytest
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints


@pytest.fixture
def api_client():
    """Create API client fixture"""
    return FHLAPIEndpoints()


@pytest.mark.asyncio
class TestFootnotesAPI:
    """Test Footnotes API endpoints"""
    
    async def test_get_footnote_success(self, api_client):
        """Test querying a valid footnote"""
        result = await api_client.get_footnote(
            book_id=1,  # Genesis
            footnote_id=1
        )
        
        assert result["status"] == "success"
        assert result["record_count"] == 1
        assert result["version"] == "tcv"
        assert "record" in result
        assert len(result["record"]) == 1
        assert "text" in result["record"][0]
        assert "id" in result["record"][0]
        assert result["record"][0]["id"] == 1
    
    async def test_get_footnote_multiple_books(self, api_client):
        """Test footnotes from different books"""
        test_cases = [
            (1, 1, "Gen"),    # Genesis
            (43, 1, "John"),  # John
            (45, 1, "Rom"),   # Romans
        ]
        
        for book_id, footnote_id, expected_engs in test_cases:
            result = await api_client.get_footnote(
                book_id=book_id,
                footnote_id=footnote_id
            )
            
            assert result["status"] == "success", f"Failed for book_id={book_id}"
            assert result["record_count"] == 1, f"No record for book_id={book_id}"
            assert result["engs"] == expected_engs, f"Wrong book for book_id={book_id}"
            
            # Check footnote content exists
            footnote_text = result["record"][0]["text"]
            assert len(footnote_text) > 0, f"Empty footnote for book_id={book_id}"
    
    async def test_get_footnote_simplified(self, api_client):
        """Test footnote with simplified Chinese"""
        result = await api_client.get_footnote(
            book_id=1,
            footnote_id=1,
            use_simplified=True
        )
        
        assert result["status"] == "success"
        assert result["record_count"] == 1
        assert result["version"] == "tcv"
    
    async def test_get_footnote_invalid_id(self, api_client):
        """Test querying a non-existent footnote"""
        result = await api_client.get_footnote(
            book_id=1,
            footnote_id=999999
        )
        
        # Should still return success but with 0 records
        assert result["status"] == "success"
        assert result["record_count"] == 0
    
    async def test_get_footnote_multiple_ids(self, api_client):
        """Test multiple footnote IDs in the same book"""
        book_id = 43  # John
        
        for footnote_id in [1, 2, 5, 10]:
            result = await api_client.get_footnote(
                book_id=book_id,
                footnote_id=footnote_id
            )
            
            assert result["status"] == "success"
            assert result["record_count"] == 1
            assert result["record"][0]["id"] == footnote_id
    
    async def test_get_footnote_version_tcv_only(self, api_client):
        """Test that only TCV version has footnotes"""
        # TCV should have footnotes
        result_tcv = await api_client.get_footnote(
            book_id=1,
            footnote_id=1,
            version="tcv"
        )
        
        assert result_tcv["status"] == "success"
        assert result_tcv["record_count"] == 1
        assert result_tcv["version"] == "tcv"
        
        # Other versions will return errors or 0 records
        # This is expected as only TCV has footnote data
        other_versions = ["unv", "cunp"]
        
        for version in other_versions:
            result = await api_client.get_footnote(
                book_id=1,
                footnote_id=1,
                version=version
            )
            
            # Either returns error status or 0 records - both indicate no footnotes
            if result.get("status") == "success":
                assert result["record_count"] == 0, f"Version {version} should have no footnotes"
            else:
                # Database error is also acceptable - indicates no footnote table for this version
                assert "Fail" in result.get("status", ""), f"Unexpected status for {version}"
    
    async def test_get_footnote_content_quality(self, api_client):
        """Test that footnote content is meaningful"""
        result = await api_client.get_footnote(
            book_id=1,  # Genesis
            footnote_id=1
        )
        
        assert result["status"] == "success"
        assert result["record_count"] == 1
        
        footnote_text = result["record"][0]["text"]
        
        # Footnote should be substantial (more than 10 characters)
        assert len(footnote_text) > 10
        
        # Should contain Chinese characters
        assert any('\u4e00' <= char <= '\u9fff' for char in footnote_text)
