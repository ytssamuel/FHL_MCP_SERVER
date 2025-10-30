"""
FHL Bible API Client

Handles HTTP requests to the Faith, Hope, Love Bible API with error handling,
retry mechanism, and logging.
"""

import asyncio
import logging
from typing import Any
from urllib.parse import urlencode

import httpx

from fhl_bible_mcp.utils.errors import (
    APIResponseError,
    DataParseError,
    FHLAPIError,
    NetworkError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class FHLAPIClient:
    """
    Client for interacting with the FHL Bible API.
    
    This client handles:
    - HTTP requests with proper headers
    - Automatic retry with exponential backoff
    - Error handling and logging
    - Response validation
    
    Attributes:
        base_url: Base URL for the FHL API
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
    """

    def __init__(
        self,
        base_url: str = "https://bible.fhl.net/json/",
        timeout: int = 30,
        max_retries: int = 3,
        gb: int = 0,  # 0 for Traditional Chinese, 1 for Simplified Chinese
    ) -> None:
        """
        Initialize the FHL API client.
        
        Args:
            base_url: Base URL for the FHL API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            gb: Chinese variant (0=Traditional, 1=Simplified)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.gb = gb
        
        # Create async HTTP client
        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": "FHL-Bible-MCP-Server/0.1.0",
                "Accept": "application/json, text/html",
            },
        )
        
        logger.info(
            f"FHL API Client initialized: base_url={base_url}, "
            f"timeout={timeout}s, max_retries={max_retries}"
        )

    async def __aenter__(self) -> "FHLAPIClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
        logger.debug("FHL API Client closed")

    async def _make_request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        retry_count: int = 0,
    ) -> dict[str, Any] | str:
        """
        Make an HTTP request to the FHL API with retry logic.
        
        Args:
            endpoint: API endpoint (e.g., "qb.php")
            params: Query parameters
            retry_count: Current retry attempt number
            
        Returns:
            Parsed JSON response or raw text
            
        Raises:
            NetworkError: When network connection fails
            APIResponseError: When API returns an error
            RateLimitError: When rate limit is exceeded
        """
        if params is None:
            params = {}
        
        # Add default gb parameter if not specified
        if "gb" not in params:
            params["gb"] = self.gb
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.debug(f"Making request to {url} with params: {params}")
            
            response = await self._client.get(url, params=params)
            
            # Log response details
            logger.debug(
                f"Response status: {response.status_code}, "
                f"content-type: {response.headers.get('content-type', 'unknown')}"
            )
            
            # Handle rate limiting (if implemented by API)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(retry_after=retry_after)
            
            # Handle client/server errors
            if response.status_code >= 400:
                raise APIResponseError(
                    message=f"API request failed",
                    status_code=response.status_code,
                    response_text=response.text[:500],  # Limit error text length
                )
            
            # Try to parse as JSON
            content_type = response.headers.get("content-type", "")
            
            if "application/json" in content_type:
                try:
                    data = response.json()
                    
                    # Check for API-level error status
                    if isinstance(data, dict) and data.get("status") == "error":
                        raise APIResponseError(
                            message=f"API returned error: {data.get('message', 'Unknown error')}",
                            status_code=response.status_code,
                        )
                    
                    logger.debug(f"Successfully parsed JSON response")
                    return data
                    
                except ValueError as e:
                    raise DataParseError(
                        message=f"Failed to parse JSON response: {str(e)}",
                        raw_data=response.text[:500],
                    )
            else:
                # Return raw text for non-JSON responses (e.g., CSV, XML)
                logger.debug(f"Returning raw text response")
                return response.text
        
        except httpx.TimeoutException as e:
            error_msg = f"Request timeout after {self.timeout}s"
            logger.warning(f"{error_msg}: {url}")
            
            if retry_count < self.max_retries:
                return await self._retry_request(endpoint, params, retry_count, error_msg)
            
            raise NetworkError(f"{error_msg} (max retries exceeded)")
        
        except httpx.NetworkError as e:
            error_msg = f"Network error: {str(e)}"
            logger.warning(f"{error_msg}: {url}")
            
            if retry_count < self.max_retries:
                return await self._retry_request(endpoint, params, retry_count, error_msg)
            
            raise NetworkError(f"{error_msg} (max retries exceeded)")
        
        except RateLimitError:
            # Re-raise rate limit errors without retry
            raise
        
        except APIResponseError:
            # Re-raise API errors without retry
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error in API request: {str(e)}")
            raise FHLAPIError(f"Unexpected error: {str(e)}")

    async def _retry_request(
        self,
        endpoint: str,
        params: dict[str, Any] | None,
        retry_count: int,
        error_msg: str,
    ) -> dict[str, Any] | str:
        """
        Retry a failed request with exponential backoff.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            retry_count: Current retry attempt number
            error_msg: Error message from previous attempt
            
        Returns:
            API response
        """
        retry_count += 1
        wait_time = 2**retry_count  # Exponential backoff: 2, 4, 8 seconds
        
        logger.info(
            f"Retrying request (attempt {retry_count}/{self.max_retries}) "
            f"after {wait_time}s: {error_msg}"
        )
        
        await asyncio.sleep(wait_time)
        return await self._make_request(endpoint, params, retry_count)

    def _validate_params(self, params: dict[str, Any], required: list[str]) -> None:
        """
        Validate that required parameters are present.
        
        Args:
            params: Parameters to validate
            required: List of required parameter names
            
        Raises:
            InvalidParameterError: When required parameters are missing
        """
        from fhl_bible_mcp.utils.errors import InvalidParameterError
        
        for param in required:
            if param not in params or params[param] is None:
                raise InvalidParameterError(
                    parameter=param,
                    value=None,
                    reason="This parameter is required",
                )

    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """
        Build a full URL with query parameters.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Complete URL with query string
        """
        url = f"{self.base_url}/{endpoint}"
        if params:
            # Add default gb parameter
            if "gb" not in params:
                params["gb"] = self.gb
            url += f"?{urlencode(params)}"
        return url
