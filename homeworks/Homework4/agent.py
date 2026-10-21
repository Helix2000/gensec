"""Homework 4 MCP agent application.

This agent connects to two MCP servers configured in ``fastagent.config.yaml``:

- ``homework4_custom``: the custom server created for this homework
- ``git``: the official Model Context Protocol Git reference server

The agent is intentionally simple and interactive. It can combine tools from
both servers in one conversation, for example:

1. Use the homework server to verify the FAU ID or transform text.
2. Use the Git server to inspect repository status or history.
3. Combine both results to answer a multi-step user request.

Run it with uv:

    uv run python agent.py

Set your API key in the environment first, for example:

    export OPENAI_API_KEY="your-key"

You can also override the model with ``FASTAGENT_MODEL``.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from fast_agent.core.fastagent import FastAgent


# Make the script runnable from any working directory by switching to the
# folder that contains this file. That keeps fastagent.config.yaml and the
# relative MCP server commands easy to resolve.
os.chdir(Path(__file__).resolve().parent)

MODEL_NAME = os.getenv("FASTAGENT_MODEL", "responses.gpt-5-mini?web_search=off")

fast = FastAgent("Homework 4 Multi-Server Agent")


@fast.agent(
    instruction=(
        "You are a helpful homework assistant with access to two MCP servers: "
        "'homework4_custom' and 'git'. Use both tools when a task requires "
        "multiple steps. Prefer the homework server for the student ID and simple "
        "text utilities, and use the Git server for repository inspection. "
        "When solving a problem, gather the needed facts from the available tools "
        "before answering. The FAU ID for this submission is Z23816617."
    ),
    model=MODEL_NAME,
    servers=["homework4_custom", "git"],
    use_history=True,
)
async def main() -> None:
    """Run the interactive MCP agent."""
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
