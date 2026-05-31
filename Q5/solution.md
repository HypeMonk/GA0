# FastAPI Code interpreter Server — Step-by-Step Guide

## What's the Goal?

Scenario: You're building a code execution service that not only runs Python code but also uses AI to analyze errors and identify the exact line numbers where errors occur.

Your Task: Create a FastAPI endpoint POST /code-interpreter that executes Python code and uses AI to analyze errors.

System Architecture:

- Tool Function: Executes Python code and returns exact output
- AI Agent: Analyzes errors (only when they occur) to identify line numbers
---

## Step 1: Install Dependencies

Open your terminal and run:

```bash
pip install fastapi uvicorn
```

That's all you need.

---

## Step 2: Get a api key

Your CSV file should look like this:

- Go to aipipe.org
- Log in with student mail
- Get your api token
---

## Step 3: Create `main.py`

Create a new file called `main.py` and paste this code:

```python
# main.py
import os
import json
import re
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from io import StringIO
import sys
import traceback

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
AI_API_TOKEN = os.environ.get("AI_API_TOKEN") #Replace with your api key
CHAT_URL = os.environ.get("https://aipipe.org/openrouter/v1/chat/completions")  

# ----------------------------
# FastAPI setup
# ----------------------------
app = FastAPI(title="Code Interpreter with AI Error Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request & Response Models
# ----------------------------
class CodeRequest(BaseModel):
    code: str

class CodeResponse(BaseModel):
    error: List[int]
    result: str

# ----------------------------
# Tool Function: Execute Python code
# ----------------------------
def execute_python_code(code: str) -> dict:
    """
    Execute Python code and return exact output or traceback.
    """
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()
        return {"success": True, "output": output}

    except Exception:
        output = traceback.format_exc()
        return {"success": False, "output": output}

    finally:
        sys.stdout = old_stdout

# ----------------------------
# AI Error Analysis with Fallback
# ----------------------------
def analyze_error_with_ai(code: str, traceback_text: str) -> List[int]:
    """
    Use Gemini to identify error line numbers. Fallback to parsing traceback if AI fails.
    """
    prompt = f"""
Analyze this Python code and its traceback.
Return only **JSON**, no explanations.
Use this exact format:

{{
  "error_lines": [line_numbers]
}}

CODE:
{code}

TRACEBACK:
{traceback_text}
"""

    headers = {
        "Authorization": f"Bearer {AI_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gemini-2.0-flash-exp",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0
    }

    error_lines = []

    try:
        response = requests.post(CHAT_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        ai_text = data["choices"][0]["message"]["content"]

        # Try to parse AI JSON
        try:
            result = json.loads(ai_text)
            error_lines = result.get("error_lines", [])
        except json.JSONDecodeError:
            print("AI returned invalid JSON:", ai_text)
            error_lines = []

    except requests.exceptions.RequestException as e:
        print("AIPipe request failed:", e)
        error_lines = []

    # ----------------------------
    # Fallback: parse Python traceback
    # ----------------------------
    if not error_lines:
        # Extract all line numbers from traceback
        matches = re.findall(r'File "<string>", line (\d+)', traceback_text)
        if matches:
            error_lines = [int(matches[-1])]  # take only the last one
        else:
            error_lines = []

    return error_lines

# ----------------------------
# API Endpoint
# ----------------------------
@app.post("/code-interpreter", response_model=CodeResponse)
def code_interpreter(request: CodeRequest):
    execution = execute_python_code(request.code)

    if execution["success"]:
        return CodeResponse(error=[], result=execution["output"])
    else:
        error_lines = analyze_error_with_ai(request.code, execution["output"])
        return CodeResponse(error=error_lines, result=execution["output"])
```

**The only line you need to change:** `AI_API_TOKEN` — Replace with your api key.

---

## Step 4: Run the Server

In your terminal, navigate to the folder where `main.py` is saved:

```bash
cd path/to/your/folder
```

Then start the server:

```bash
uvicorn main:app --port 8002 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
```

Your server is now live at: **`http://127.0.0.1:8002/code-interpreter`**

---

You can also open `http://127.0.0.1:8005/docs` in your browser for a free interactive API explorer that FastAPI generates automatically.

---

## Submission

Keep the server running and submit:

```
http://127.0.0.1:8002/code-interpreter
```
---

## Common Errors & Fixes

### ❌ `Could not import module "app"`
You ran `uvicorn app:app` but your file is named `main.py`.

**Fix:** Match the command to your filename:
```bash
uvicorn main:app --port 8002 --reload   # if file is main.py
uvicorn app:app  --port 8002 --reload   # if file is app.py
```

---

### ❌ `Address already in use` / `Port 8005 is in use`
Something is already running on that port (maybe a previous server you didn't stop).

**Fix:** Either stop the old server (Ctrl+C in the terminal running it), or use a different port:
```bash
uvicorn main:app --port 8006 --reload
```
---

### ❌ CORS error in browser
If you're accessing the API from a web page and getting a CORS error, make sure the `app.add_middleware(CORSMiddleware, ...)` block is in your code and the server was restarted after adding it.

---
