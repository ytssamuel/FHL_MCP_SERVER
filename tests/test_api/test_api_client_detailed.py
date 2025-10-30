"""
Unit tests for API client

測試 FHL API 客戶端的 HTTP 請求、重試機制、錯誤處理等功能。
"""
import sys
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

# Add src to path so we can import without src. prefix
sys.path.insert(0, 'src')

from fhl_bible_mcp.api.client import FHLAPIClient
from fhl_bible_mcp.utils.errors import (
    NetworkError,
    APIResponseError,
    RateLimitError,
    DataParseError,
    InvalidParameterError,
    FHLAPIError
)


@pytest.mark.asyncio
async def test_client_initialization():
    """測試客戶端初始化"""
    client = FHLAPIClient(
        base_url="https://test.api.com",
        timeout=60,
        max_retries=5,
        gb=1
    )
    
    assert client.base_url == "https://test.api.com"
    assert client.timeout == 60
    assert client.max_retries == 5
    assert client.gb == 1
    
    await client.close()


@pytest.mark.asyncio
async def test_client_context_manager():
    """測試上下文管理器"""
    async with FHLAPIClient() as client:
        assert client is not None
        assert client._client is not None


@pytest.mark.asyncio
async def test_make_request_success_json():
    """測試成功的 JSON 請求"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "success", "data": "test"}
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response) as mock_get:
        result = await client._make_request("test.php", {"param": "value"})
        
        assert result["status"] == "success"
        assert result["data"] == "test"
        mock_get.assert_called_once()
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_success_text():
    """測試成功的文本請求"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "text/html"}
    mock_response.text = "<html>Test</html>"
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response):
        result = await client._make_request("test.php")
        
        assert result == "<html>Test</html>"
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_api_error_response():
    """測試 API 返回錯誤狀態"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "error", "message": "Invalid query"}
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response):
        with pytest.raises(APIResponseError, match="Invalid query"):
            await client._make_request("test.php")
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_http_error():
    """測試 HTTP 錯誤響應 (4xx, 5xx)"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response):
        with pytest.raises(APIResponseError) as exc_info:
            await client._make_request("test.php")
        assert exc_info.value.status_code == 500
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_rate_limit():
    """測試速率限制錯誤"""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "120"}
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response):
        with pytest.raises(RateLimitError) as exc_info:
            await client._make_request("test.php")
        assert exc_info.value.retry_after == 120
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_json_parse_error():
    """測試 JSON 解析錯誤"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "Not valid JSON"
    
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', return_value=mock_response):
        with pytest.raises(FHLAPIError) as exc_info:
            await client._make_request("test.php")
        # DataParseError 被包裝為 FHLAPIError
        error_msg = str(exc_info.value)
        assert "Failed to parse JSON" in error_msg or "Unexpected error" in error_msg
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_timeout_with_retry():
    """測試超時並重試"""
    client = FHLAPIClient(max_retries=2)
    
    # 第一次和第二次超時，第三次成功
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "success"}
    
    with patch.object(client._client, 'get') as mock_get:
        mock_get.side_effect = [
            httpx.TimeoutException("Timeout 1"),
            httpx.TimeoutException("Timeout 2"),
            mock_response
        ]
        
        with patch('asyncio.sleep', new_callable=AsyncMock):  # 避免實際等待
            result = await client._make_request("test.php")
            
            assert result["status"] == "success"
            assert mock_get.call_count == 3
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_timeout_max_retries():
    """測試超時達到最大重試次數"""
    client = FHLAPIClient(max_retries=1)
    
    with patch.object(client._client, 'get', side_effect=httpx.TimeoutException("Timeout")), \
         patch('asyncio.sleep', new_callable=AsyncMock):
        with pytest.raises(NetworkError, match="max retries exceeded"):
            await client._make_request("test.php")
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_network_error_with_retry():
    """測試網絡錯誤並重試"""
    client = FHLAPIClient(max_retries=1)
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "success"}
    
    with patch.object(client._client, 'get') as mock_get:
        mock_get.side_effect = [
            httpx.NetworkError("Connection failed"),
            mock_response
        ]
        
        with patch('asyncio.sleep', new_callable=AsyncMock):
            result = await client._make_request("test.php")
            
            assert result["status"] == "success"
            assert mock_get.call_count == 2
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_network_error_max_retries():
    """測試網絡錯誤達到最大重試次數"""
    client = FHLAPIClient(max_retries=1)
    
    with patch.object(client._client, 'get', side_effect=httpx.NetworkError("Connection failed")), \
         patch('asyncio.sleep', new_callable=AsyncMock):
        with pytest.raises(NetworkError, match="max retries exceeded"):
            await client._make_request("test.php")
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_unexpected_error():
    """測試意外錯誤"""
    client = FHLAPIClient()
    
    with patch.object(client._client, 'get', side_effect=RuntimeError("Unexpected")):
        with pytest.raises(FHLAPIError, match="Unexpected error"):
            await client._make_request("test.php")
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_default_gb_parameter():
    """測試默認 gb 參數"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "success"}
    
    client = FHLAPIClient(gb=1)
    
    with patch.object(client._client, 'get', return_value=mock_response) as mock_get:
        await client._make_request("test.php", {"param": "value"})
        
        # 檢查調用的參數是否包含 gb
        call_args = mock_get.call_args
        assert call_args[1]["params"]["gb"] == 1
    
    await client.close()


@pytest.mark.asyncio
async def test_validate_params_success():
    """測試參數驗證成功"""
    client = FHLAPIClient()
    
    params = {"book": "John", "chapter": 3, "verse": 16}
    client._validate_params(params, ["book", "chapter", "verse"])
    
    # 如果沒有拋出異常，則驗證成功
    await client.close()


@pytest.mark.asyncio
async def test_validate_params_missing_required():
    """測試缺少必需參數"""
    client = FHLAPIClient()
    
    params = {"book": "John"}
    
    with pytest.raises(InvalidParameterError) as exc_info:
        client._validate_params(params, ["book", "chapter"])
    
    assert exc_info.value.parameter == "chapter"
    await client.close()


@pytest.mark.asyncio
async def test_validate_params_none_value():
    """測試參數值為 None"""
    client = FHLAPIClient()
    
    params = {"book": "John", "chapter": None}
    
    with pytest.raises(InvalidParameterError) as exc_info:
        client._validate_params(params, ["book", "chapter"])
    
    assert exc_info.value.parameter == "chapter"
    await client.close()


@pytest.mark.asyncio
async def test_build_url_no_params():
    """測試構建 URL（無參數）"""
    client = FHLAPIClient(base_url="https://api.test.com")
    
    url = client._build_url("test.php")
    
    assert url == "https://api.test.com/test.php"
    
    await client.close()


@pytest.mark.asyncio
async def test_build_url_with_params():
    """測試構建 URL（帶參數）"""
    client = FHLAPIClient(base_url="https://api.test.com", gb=0)
    
    url = client._build_url("test.php", {"book": "John", "chapter": 3})
    
    assert "https://api.test.com/test.php?" in url
    assert "book=John" in url
    assert "chapter=3" in url
    assert "gb=0" in url
    
    await client.close()


@pytest.mark.asyncio
async def test_retry_request_exponential_backoff():
    """測試重試機制的指數退避"""
    client = FHLAPIClient(max_retries=2)
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"status": "success"}
    
    sleep_times = []
    
    async def mock_sleep(seconds):
        sleep_times.append(seconds)
    
    with patch.object(client._client, 'get') as mock_get:
        mock_get.side_effect = [
            httpx.TimeoutException("Timeout"),
            httpx.TimeoutException("Timeout"),
            mock_response
        ]
        
        with patch('asyncio.sleep', side_effect=mock_sleep):
            await client._make_request("test.php")
            
            # 驗證指數退避: 2^1=2, 2^2=4
            assert sleep_times == [2, 4]
    
    await client.close()


@pytest.mark.asyncio
async def test_client_base_url_strip_trailing_slash():
    """測試 base_url 自動移除尾部斜線"""
    client = FHLAPIClient(base_url="https://api.test.com/")
    
    assert client.base_url == "https://api.test.com"
    
    await client.close()
