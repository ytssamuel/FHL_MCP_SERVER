"""
FHL Bible MCP Server - Resources

提供 MCP Resources 功能,允許 AI 透過 URI 存取聖經資料。
"""

from .handlers import (
    ResourceHandler,
    BibleResourceHandler,
    StrongsResourceHandler,
    CommentaryResourceHandler,
    InfoResourceHandler,
    ResourceRouter
)

__all__ = [
    "ResourceHandler",
    "BibleResourceHandler",
    "StrongsResourceHandler",
    "CommentaryResourceHandler",
    "InfoResourceHandler",
    "ResourceRouter"
]
