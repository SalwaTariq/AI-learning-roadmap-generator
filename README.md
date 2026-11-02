# 🗺️ AI Learning Roadmap Generator

A simple Streamlit app that creates a personalized learning roadmap. Enter a field, your skill level, and the time you have, and an LLM (via the Google Gemini API) generates a phase-by-phase plan with resources and projects.

## Tech stack

- Python
- Streamlit (UI)
- Google Gemini API (`gemini-2.5-flash`)
- Google Colab + Cloudflare Tunnel (optional, for running without a local setup)

## Get a Gemini API key

Create a free key at https://aistudio.google.com/apikey.

## Run locally

```bash
git clone https://github.com/<your-username>/ai-roadmap-generator.git
cd ai-roadmap-generator
pip install -r requirements.txt

# macOS / Linux
export GEMINI_API_KEY="your_key_here"
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_key_here"

streamlit run app.py
```

## Run in Google Colab (with Cloudflare Tunnel)

1. In Colab, add a secret named `GEMINI_API_KEY` (🔑 icon in the sidebar) and enable notebook access.
2. Run these cells in order:

```python
# Cell 1: get the code and install dependencies
!git clone https://github.com/<your-username>/ai-roadmap-generator.git
%cd ai-roadmap-generator
!pip install -q -r requirements.txt
```

```python
# Cell 2: install cloudflared
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
!dpkg -i cloudflared-linux-amd64.deb
```

```python
# Cell 3: load the API key
import os
from google.colab import userdata
os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
```

```python
# Cell 4: start Streamlit
import subprocess, time
subprocess.Popen(
    ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
    stdout=open("streamlit.log", "w"),
    stderr=subprocess.STDOUT,
)
time.sleep(5)
```

```python
# Cell 5: open the tunnel and print the public URL
import subprocess, re
proc = subprocess.Popen(
    ["cloudflared", "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
)
for line in proc.stdout:
    m = re.search(r"https://[-a-z0-9]+\.trycloudflare\.com", line)
    if m:
        print("🚀 App live at:", m.group(0))
        break
```

## Deploy on Streamlit Community Cloud (optional)

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and create a new app from the repo (main file: `app.py`).
3. Under **Advanced settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_key_here"
```

## Project structure

```
ai-roadmap-generator/
├── app.py
├── requirements.txt
└── README.md
```

## Notes

- Never commit your API key. The app reads it from an environment variable or Streamlit secrets.
- If you get a "model not found" error, check https://ai.google.dev/gemini-api/docs/models and update the `MODEL` name at the top of `app.py`.
