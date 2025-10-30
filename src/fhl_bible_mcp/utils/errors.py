"""
Custom error definitions for FHL Bible API client.
"""


class FHLAPIError(Exception):
    """Base exception for all FHL API errors."""

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)

    def __str__(self) -> str:
        return self.message


class NetworkError(FHLAPIError):
    """
    Raised when network connection fails.
    
    Examples:
        - Connection timeout
        - DNS resolution failure
        - Server unreachable
    """

    def __init__(self, message: str = "Network connection failed", *args: object) -> None:
        super().__init__(message, *args)


class InvalidParameterError(FHLAPIError):
    """
    Raised when invalid parameters are provided to API methods.
    
    Examples:
        - Invalid book name
        - Chapter/verse out of range
        - Invalid version code
    """

    def __init__(self, parameter: str, value: object, reason: str = "") -> None:
        msg = f"Invalid parameter '{parameter}': {value}"
        if reason:
            msg += f" - {reason}"
        self.parameter = parameter
        self.value = value
        self.reason = reason
        super().__init__(msg)


class APIResponseError(FHLAPIError):
    """
    Raised when API returns an error response.
    
    Examples:
        - 404 Not Found
        - 500 Internal Server Error
        - Malformed JSON response
    """

    def __init__(
        self,
        message: str = "API returned an error response",
        status_code: int | None = None,
        response_text: str | None = None,
        *args: object,
    ) -> None:
        if status_code:
            message = f"{message} (status code: {status_code})"
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message, *args)


class RateLimitError(FHLAPIError):
    """
    Raised when API rate limit is exceeded.
    
    This is a custom error that can be used if rate limiting is implemented
    in the future.
    """

    def __init__(
        self,
        message: str = "API rate limit exceeded",
        retry_after: int | None = None,
        *args: object,
    ) -> None:
        if retry_after:
            message = f"{message}. Retry after {retry_after} seconds"
        self.retry_after = retry_after
        super().__init__(message, *args)


class DataParseError(FHLAPIError):
    """
    Raised when response data cannot be parsed or validated.
    
    Examples:
        - Invalid JSON structure
        - Missing required fields
        - Type validation errors
    """

    def __init__(
        self,
        message: str = "Failed to parse API response data",
        raw_data: object = None,
        *args: object,
    ) -> None:
        self.raw_data = raw_data
        super().__init__(message, *args)


class BookNotFoundError(InvalidParameterError):
    """
    Raised when a book name cannot be resolved.
    
    This is a specialized InvalidParameterError for book names.
    """

    def __init__(self, book_name: str) -> None:
        super().__init__(
            parameter="book",
            value=book_name,
            reason="Book not found. Please check the spelling or use a valid book code.",
        )
        self.book_name = book_name


class VersionNotFoundError(InvalidParameterError):
    """
    Raised when a Bible version code is not found.
    
    This is a specialized InvalidParameterError for version codes.
    """

    def __init__(self, version_code: str) -> None:
        super().__init__(
            parameter="version",
            value=version_code,
            reason="Version not found. Use list_bible_versions() to see available versions.",
        )
        self.version_code = version_code
