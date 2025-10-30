"""
Tests for error handling
"""
import pytest
from src.fhl_bible_mcp.utils.errors import (
    FHLAPIError,
    NetworkError,
    InvalidParameterError,
    APIResponseError,
    RateLimitError
)


def test_fhl_api_error():
    """Test base FHLAPIError"""
    error = FHLAPIError("基礎錯誤")
    
    assert str(error) == "基礎錯誤"
    assert isinstance(error, Exception)


def test_network_error():
    """Test NetworkError"""
    error = NetworkError("網路連接失敗")
    
    assert str(error) == "網路連接失敗"
    assert isinstance(error, FHLAPIError)


def test_invalid_parameter_error():
    """Test InvalidParameterError"""
    error = InvalidParameterError("book", "invalid_value", "書卷名稱不存在")
    
    assert "book" in str(error)
    assert "invalid_value" in str(error)
    assert isinstance(error, FHLAPIError)


def test_api_response_error():
    """Test APIResponseError"""
    error = APIResponseError("API 返回錯誤狀態")
    
    assert "API" in str(error)
    assert isinstance(error, FHLAPIError)


def test_rate_limit_error():
    """Test RateLimitError"""
    error = RateLimitError("請求頻率過高")
    
    assert "頻率" in str(error)
    assert isinstance(error, FHLAPIError)


def test_error_with_cause():
    """Test error with cause"""
    original_error = ValueError("原始錯誤")
    try:
        raise NetworkError("網路錯誤") from original_error
    except NetworkError as error:
        assert error.__cause__ is original_error


def test_raise_network_error():
    """Test raising NetworkError"""
    with pytest.raises(NetworkError):
        raise NetworkError("測試網路錯誤")


def test_raise_invalid_parameter():
    """Test raising InvalidParameterError"""
    with pytest.raises(InvalidParameterError):
        raise InvalidParameterError("test_param", "invalid", "測試參數錯誤")


def test_catch_fhl_api_error():
    """Test catching FHLAPIError"""
    try:
        raise NetworkError("測試錯誤")
    except FHLAPIError as e:
        assert isinstance(e, NetworkError)
        assert "測試錯誤" in str(e)


def test_error_inheritance():
    """Test error class inheritance"""
    assert issubclass(NetworkError, FHLAPIError)
    assert issubclass(InvalidParameterError, FHLAPIError)
    assert issubclass(APIResponseError, FHLAPIError)
    assert issubclass(RateLimitError, FHLAPIError)
