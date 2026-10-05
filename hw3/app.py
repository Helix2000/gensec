# Jose Marrero, FAU ID Z23816617
"""Text Analysis Agent

Author: Jose Marrero
FAU ID: Z23816617
"""

import os
import sys
from dotenv import load_dotenv

# Import required agent components to verify dependency installation
from typing import Any
from langchain.agents import create_agent
from langchain_community.tools import ShellTool
from langchain_core.tools import tool
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load credentials from .env without hardcoding them in source files
load_dotenv()


@tool
def analyze_text(text: str) -> dict[str, int]:
    """Analyze the provided text to calculate word count and character count (including spaces).

    Use this tool whenever text-counting requests (such as word or character counts) are requested.

    Args:
        text: The input text to analyze.

    Returns:
        A dictionary containing 'words' and 'characters' count.
    """
    word_count = len(text.split())
    character_count = len(text)
    return {"words": word_count, "characters": character_count}


def verify_setup() -> None:
    """Verify that dependencies import cleanly and check environment settings."""
    print("Verifying setup for Text Analysis Agent...")
    print(f" - Python executable: {sys.executable}")
    print(f" - Python prefix (.venv): {sys.prefix}")
    print(f" - LangChain version: {langchain.__version__}")
    print(f" - ChatGoogleGenerativeAI class: {ChatGoogleGenerativeAI.__name__}")
    print(f" - Built-in Terminal Tool: {ShellTool.__name__}")
    print(f" - Custom Tool: {analyze_text.name}")
    print("Vertex AI Configuration:")
    print(f" - GOOGLE_GENAI_USE_VERTEXAI: {os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'Not set')}")
    print(f" - GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'Not set')}")
    print(f" - GOOGLE_CLOUD_LOCATION: {os.getenv('GOOGLE_CLOUD_LOCATION', 'Not set')}")
    print(f" - GOOGLE_MODEL: {os.getenv('GOOGLE_MODEL', 'Not set')}")

    # Verify custom tool with sample test input
    test_text = "Hello world"
    test_result = analyze_text.invoke({"text": test_text})
    print(
        f"Tool verification ('{test_text}'): "
        f"{test_result['words']} words and {test_result['characters']} characters"
    )


def create_model() -> ChatGoogleGenerativeAI:
    """Initialize ChatGoogleGenerativeAI using Vertex AI and ADC credentials."""
    model_name = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true").lower() == "true"

    kwargs: dict[str, Any] = {
        "model": model_name,
        "vertexai": use_vertex,
    }
    if project:
        kwargs["project"] = project
    if location:
        kwargs["location"] = location

    return ChatGoogleGenerativeAI(**kwargs)


def build_agent() -> Any:
    """Build the LangChain agent graph with ChatGoogleGenerativeAI, terminal, and analyze_text tools."""
    llm = create_model()
    terminal = ShellTool()
    terminal.name = "terminal"
    tools = [terminal, analyze_text]
    system_prompt = (
        "You are a helpful assistant. "
        "Always use the analyze_text tool for text-counting requests (such as counting words or characters). "
        "Use the terminal tool for shell or terminal execution tasks."
    )
    return create_agent(model=llm, tools=tools, system_prompt=system_prompt)


def extract_text_content(content: Any) -> str:
    """Extract text from message content whether it is a string or list of blocks.

    Args:
        content: Message content object.

    Returns:
        Extracted string representation.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return str(content)


def display_agent_turn(response: Any) -> None:
    """Display tool calls, tool results, and the final response for a completed turn.

    Args:
        response: Response mapping returned by the agent.
    """
    messages = response.get("messages", []) if isinstance(response, dict) else getattr(response, "messages", [])

    for msg in messages:
        msg_type = getattr(msg, "type", "")
        msg_cls = type(msg).__name__
        if msg_type == "human" or msg_cls == "HumanMessage":
            continue

        # Display tool call requests
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for tc in tool_calls:
                name = tc.get("name", "tool")
                args = tc.get("args", {})
                print(f"\n[Tool Call] {name} -> args: {args}")

        # Display tool execution outputs
        if msg_type == "tool" or msg_cls == "ToolMessage":
            tool_name = getattr(msg, "name", None) or "tool"
            tool_output = extract_text_content(getattr(msg, "content", ""))
            print(f"\n[Tool Result - {tool_name}]\n{tool_output}")

    # Display final AI answer
    final_text = ""
    for msg in reversed(messages):
        msg_type = getattr(msg, "type", "")
        msg_cls = type(msg).__name__
        if (msg_type == "ai" or msg_cls == "AIMessage") and not getattr(msg, "tool_calls", None):
            final_text = extract_text_content(getattr(msg, "content", ""))
            break

    if not final_text and messages:
        final_text = extract_text_content(getattr(messages[-1], "content", str(messages[-1])))

    print(f"\n[Final Result]\n{final_text}\n")


def run_interactive_agent() -> None:
    """Start the interactive terminal loop for the agent."""
    verify_setup()
    print("\nInitializing Text Analysis Agent with terminal and analyze_text tools...")
    agent = build_agent()
    print("Agent ready. Type your prompt, or type 'exit' (or press Enter on empty line) to quit.")

    while True:
        try:
            user_input = input("\nEnter prompt: ").strip()
            if not user_input or user_input.lower() == "exit":
                print("Exiting agent session.")
                break

            response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
            display_agent_turn(response)
        except (KeyboardInterrupt, EOFError):
            print("\nSession interrupted. Exiting.")
            break
        except Exception as exc:
            print(f"\n[Agent Error] {exc}")
            print("Continuing session. You can enter another prompt.")


if __name__ == "__main__":
    run_interactive_agent()
# Jose Marrero, FAU ID Z23816617