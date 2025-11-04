"""
FHL Bible MCP Server - Entry Point

This module provides the entry point for running the MCP server via:
    python -m fhl_bible_mcp
"""

import asyncio
import sys

from fhl_bible_mcp.server import main


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
