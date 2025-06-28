# Python-AI-Agent

An interactive AI-powered command-line tool for code assistance, file management, and Python script execution. This project integrates Google’s Gemini API 2.0 Flash to generate responses, invoke functions, and interact with your local filesystem securely.

## Features

- **Natural language AI assistant:** Generate code explanations, fixes, and recommendations using Google Gemini API.
- **File management:** Read and write files safely within a designated working directory.
- **Python script execution:** Run Python files programmatically with output capturing.
- **Command-line interface:** Easily interact with the assistant through simple commands.
- **Detailed logging:** Optional verbose mode for debugging API calls and function results.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SeccreDev/Python-AI-Agent.git
    cd Python-AI-Agent
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set your Gemini API key in a .env file:
    ```bash
    GEMINI_API_KEY=your-API-key-here
    ```

## Usage
Run the main script with your prompt:

```bash
python main.py "Write 3 sentences about your favorite Oblivion character" --verbose
```

## License
[MIT](https://choosealicense.com/licenses/mit/)