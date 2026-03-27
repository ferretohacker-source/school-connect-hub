# Ferreto AI (Advanced School Project)

Ferreto AI is a **desktop voice assistant** inspired by Alexa/Jarvis behavior.
It runs in the background, wakes on **"Hey Ferreto"**, answers questions from online sources, and performs PC actions such as opening YouTube in Chrome.

## Advanced Capabilities

- Wake word interaction: `hey ferreto`
- Voice-to-text + text-to-speech conversation
- Internet answers with concise summaries
- Chrome-powered search:
  - `search in chrome climate change`
  - `search python loops`
- Smart actions:
  - `open youtube`
  - `open chrome`
  - `open notepad`
  - `open website github.com`
  - `open file C:\\Users\\Name\\Documents\\report.pdf`
  - `time`, `date`, `system info`
- Startup support on Windows login

## Commands You Can Speak

- **Wake**: `hey ferreto`
- **Web**:
  - `open youtube`
  - `search in chrome <query>`
  - `open website <name/url>`
- **Apps**:
  - `open app notepad`
  - `open app calculator`
  - `open chrome`
- **System**:
  - `time`
  - `date`
  - `system info`
- **Knowledge**:
  - `what is machine learning`
  - `who is marie curie`
- **Control**:
  - `sleep`
  - `shutdown ferreto`

## Project Structure

```
.
├── main.py
├── ferreto
│   ├── __init__.py
│   ├── assistant.py
│   ├── knowledge.py
│   ├── speech.py
│   ├── system_actions.py
│   └── utils.py
├── install_startup_windows.py
├── requirements.txt
└── README.md
```

## Setup

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python main.py
```

## Auto-start on Windows

```bash
python install_startup_windows.py
```

This creates `FerretoAIStartup.bat` in the user Startup folder.

## Notes

- For best accuracy, use a clear microphone and low-noise room.
- Online answers/search require internet.
- If Chrome is not installed, browser actions fall back to default browser.
