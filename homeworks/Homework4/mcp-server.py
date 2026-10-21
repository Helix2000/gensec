"""Homework 4 custom MCP server.

This server uses FastMCP to expose a few simple tools for the homework
submission. Run it with uv, for example:

    uv run python gensec/homeworks/Homework4/mcp-server.py stdio

If no transport argument is provided, the server starts with HTTP transport.
"""

from __future__ import annotations

import sys

from fastmcp import FastMCP


STUDENT_ID = "Z23816617"

mcp = FastMCP("hw4_custom_server")


@mcp.tool()
def get_student_id() -> str:
    """Return the FAU student ID for this homework submission."""
    return STUDENT_ID


@mcp.tool()
def reverse_text(text: str) -> str:
    """Return the provided text in reverse order."""
    return text[::-1]


@mcp.tool()
def summarize_text(text: str) -> dict[str, int]:
    """Return simple statistics about the provided text."""
    return {
        "characters": len(text),
        "words": len(text.split()),
        "lines": len(text.splitlines()) or 1,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
