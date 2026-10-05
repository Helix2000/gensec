# Text Analysis Agent

**Author:** Jose Marrero  
**FAU ID:** Z23816617  

The Text Analysis Agent is an interactive command-line assistant powered by Google Vertex AI (`gemini-2.5-flash`) and built with LangChain. The agent selects appropriate tools to assist with text inspection and shell-based tasks.

---

## Agent Tools

1. **`analyze_text`**:
   - **Description**: A custom LangChain tool (`@tool`) designed specifically for text-counting tasks.
   - **Input**: `text` (`str`).
   - **Output**: A dictionary containing `words` (word count) and `characters` (character count).
   - **Mechanism**: Splits on whitespace via Python's `str.split()` and counts all characters using `len()`.

2. **`terminal`**:
   - **Description**: Built using LangChain's built-in `ShellTool`.
   - **Input**: Shell commands (`str`).
   - **Output**: Standard output and error streams resulting from executed shell commands.

---

## Setup and Execution in Google Cloud Shell

Follow these steps inside your Google Cloud Shell environment:

### 1. Navigate to the Homework Directory
```bash
cd /home/jmarrero2025/gensec/hw3
```

### 2. Configure Environment Variables
Copy the sample environment file to `.env`:
```bash
cp .env.example .env
```

Verify that `.env` contains the required Vertex AI settings:
```dotenv
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=gensec-marrero-jmarrero2025
GOOGLE_CLOUD_LOCATION=global
GOOGLE_MODEL=gemini-2.5-flash
```

### 3. Synchronize Dependencies
Install the project dependencies into an isolated virtual environment (`.venv`) using `uv`:
```bash
uv sync
```

### 4. Vertex AI Authentication
The agent connects to Vertex AI using **Application Default Credentials (ADC)**.
- Ensure your Cloud Shell session has active access to the project `gensec-marrero-jmarrero2025`.
- If running outside an authenticated Cloud Shell session or if prompted, authenticate your ADC credentials:
  ```bash
  gcloud auth application-default login
  ```

### 5. Run the Agent
Launch the interactive session:
```bash
uv run python app.py
```

To exit the application, type `exit` or submit an empty prompt at the `Enter prompt:` prompt.

---

## Tested Examples

- **Text Analysis Example**:
  - **User Prompt**: `How many words and characters are in "Hello world"?`
  - **Tool Invocations**: `[Tool Call] analyze_text -> args: {'text': 'Hello world'}`
  - **Tool Output**: `{'words': 2, 'characters': 11}`
  - **Final Result**: Confirms that `"Hello world"` contains 2 words and 11 characters.

- **Terminal Execution Example**:
  - **User Prompt**: `Run the terminal command to show the current working directory.`
  - **Tool Invocations**: `[Tool Call] terminal -> args: {'commands': 'pwd'}`
  - **Tool Output**: `/home/jmarrero2025/gensec/hw3`
  - **Final Result**: Reports the current working path.

---

## Limitations & Security Considerations

1. **Whitespace Tokenization**: The `analyze_text` tool counts words strictly using Python's `str.split()`. Hyphenated words or words separated by non-standard punctuation without spaces are treated as single words.
2. **Character Count Scope**: Character counts are calculated using `len(text)` and include all characters, spaces, punctuation, and newline characters.
3. **Stateless Turns**: Each user query is executed independently without preserving multi-turn conversation memory history across separate prompts.
4. **Unrestricted Terminal Execution**: The built-in `terminal` tool executes arbitrary shell commands directly in the host environment without sandboxing, input sanitization, or execution safeguards. Exercise caution when prompting commands that alter files or system states.