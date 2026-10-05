# Jose Marrero, FAU ID Z23816617
"""Text Analysis Agent

Author: Jose Marrero
FAU ID: Z23816617
"""

import os
import sys
from dotenv import load_dotenv

# Import required agent components to verify dependency installation
import langchain
from langchain_community.tools import ShellTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Load credentials from .env without hardcoding them in source files
load_dotenv()


def verify_setup() -> None:
    """Verify that dependencies import cleanly and check environment settings."""
    print("Verifying setup for Text Analysis Agent...")
    print(f" - Python executable: {sys.executable}")
    print(f" - Python prefix (.venv): {sys.prefix}")
    print(f" - LangChain version: {langchain.__version__}")
    print(f" - ChatGoogleGenerativeAI class: {ChatGoogleGenerativeAI.__name__}")
    print(f" - Built-in Terminal Tool: {ShellTool.__name__}")
    print("Vertex AI Configuration:")
    print(f" - GOOGLE_GENAI_USE_VERTEXAI: {os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'Not set')}")
    print(f" - GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'Not set')}")
    print(f" - GOOGLE_CLOUD_LOCATION: {os.getenv('GOOGLE_CLOUD_LOCATION', 'Not set')}")
    print(f" - GOOGLE_MODEL: {os.getenv('GOOGLE_MODEL', 'Not set')}")


if __name__ == "__main__":
    verify_setup()
# Jose Marrero, FAU ID Z23816617