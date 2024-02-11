
# ClipboardGPTApp

ClipboardGPTApp is a Python application that revolutionizes the way you interact with your clipboard on Windows. It enables programmable clipboard operations, allowing the content to be quickly processed by OpenAI's powerful models.

## Features
- **Clipboard Monitoring**: Continuously monitors the clipboard for new text.
- **OpenAI Integration**: Sends clipboard content to OpenAI for processing based on a specified prompt.
- **Customizable Settings**: Includes options for setting the API key, AI model, and command prefix.
- **Logging**: Option to enable logging for tracking app activities and responses.

## Requirements
- Python 3.x
- Tkinter (usually comes with Python)
- `pyperclip` for clipboard operations
- `requests` for making HTTP requests to the OpenAI API
- `threading` and `datetime` for background operations and logging

## Installation
1. Ensure you have Python installed on your Windows machine.
2. Install the required packages using pip:
   ```
   pip install pyperclip requests
   ```
3. Clone or download this repository to your local machine.

## Usage
1. Run the script:
   ```
   python clipboardGPT.py
   ```
2. Once the application starts, you will see a simple UI with options to activate the app, set the API key, and configure other settings.
3. Use the 'Activate' button to start monitoring and processing clipboard content.

## Configuration
- **API Key**: Set your OpenAI API key through the provided button in the UI.
- **Model Selection**: Choose between different AI models like GPT-3.5 Turbo and GPT-4 Turbo.
- **Command Prefix**: Set a custom prefix for your clipboard commands.

## How It Works
- The app monitors your clipboard.
- When new text is detected, it sends this text, along with a predefined command prefix, to OpenAI's API.
- The response from OpenAI is then copied back to the clipboard, making it easy to use the processed content.

## Logging
- Enable or disable logging through the UI.
- Logs are stored in `clipboardGPT_log.txt` with timestamps.

## Disclaimer
This app requires an API key from OpenAI which may incur costs depending on your usage. Please use responsibly and within OpenAI's usage guidelines.

