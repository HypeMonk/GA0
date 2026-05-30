# FastAPI Student Data Server — Step-by-Step Guide

## What's the Goal?

You have a CSV file with student data (studentId, class). You need to build a small web server that:
- Serves all students at `/api`
- Filters by class when you add `?class=1A` to the URL
- Allows any website to access it (CORS)

---

## Step 1: Install Dependencies

Open your terminal and run:

```bash
pip install fastapi uvicorn
```

That's all you need.

---

## Step 2: Check Your CSV

Your CSV file should look like this:

```
studentId,class
1,1A
2,1B
3,12Z
```

Two columns exactly: `studentId` and `class`. Note the column names — they're case-sensitive.

---

## Step 3: Create `main.py`

Create a new file called `main.py` and paste this code:

```python
import csv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = r"C:\Users\YourName\Downloads\q-fastapi.csv"  # ← CHANGE THIS

def load_students(filepath: str):
    students = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })
    return students

students = load_students(CSV_PATH)

@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    if class_:
        return {"students": [s for s in students if s["class"] in class_]}
    return {"students": students}
```

**The only line you need to change:** `CSV_PATH` — set it to wherever your CSV file is saved.

### How to find your CSV path

| OS | Example path |
|----|-------------|
| Windows | `r"C:\Users\YourName\Downloads\q-fastapi.csv"` |
| Mac/Linux | `"/home/yourname/downloads/q-fastapi.csv"` |

> **Windows tip:** Use `r"..."` (raw string) so backslashes don't cause issues.

---

## Step 4: Run the Server

In your terminal, navigate to the folder where `main.py` is saved:

```bash
cd path/to/your/folder
```

Then start the server:

```bash
uvicorn main:app --port 8005 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8005 (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
```

Your server is now live at: **`http://127.0.0.1:8005/api`**

---

## Step 5: Test It

Open your browser or use curl:

```bash
# All students
curl http://127.0.0.1:8005/api

# Only class 1A
curl "http://127.0.0.1:8005/api?class=1A"

# Class 1A and 1B together
curl "http://127.0.0.1:8005/api?class=1A&class=1B"
```

Expected response format:

```json
{
  "students": [
    { "studentId": 1, "class": "1A" },
    { "studentId": 2, "class": "1B" }
  ]
}
```

You can also open `http://127.0.0.1:8005/docs` in your browser for a free interactive API explorer that FastAPI generates automatically.

---

## Submission

Keep the server running and submit:

```
http://127.0.0.1:8005/api
```

The grader will test it by sending requests like `?class=1A&class=2B` and checking the response matches the CSV data.

---

## Common Errors & Fixes

### ❌ `Could not import module "app"`
You ran `uvicorn app:app` but your file is named `main.py`.

**Fix:** Match the command to your filename:
```bash
uvicorn main:app --port 8005 --reload   # if file is main.py
uvicorn app:app  --port 8005 --reload   # if file is app.py
```

---

### ❌ `FileNotFoundError: q-fastapi.csv`
Python can't find your CSV file.

**Fix:** Use the full absolute path in `CSV_PATH`:
```python
# Windows
CSV_PATH = r"C:\Users\YourName\Downloads\q-fastapi.csv"

# Mac/Linux
CSV_PATH = "/Users/yourname/downloads/q-fastapi.csv"
```

---

### ❌ `Address already in use` / `Port 8005 is in use`
Something is already running on that port (maybe a previous server you didn't stop).

**Fix:** Either stop the old server (Ctrl+C in the terminal running it), or use a different port:
```bash
uvicorn main:app --port 8006 --reload
```

---

### ❌ `KeyError: 'studentId'` or `KeyError: 'class'`
Your CSV column names don't match exactly.

**Fix:** Open the CSV and check the first row. Column names are case-sensitive. If your CSV has `StudentID` instead of `studentId`, update the code:
```python
"studentId": int(row["StudentID"]),   # match exactly what's in the CSV header
```

---

### ❌ Server starts but returns empty `{"students": []}`
Your `?class=` value doesn't match what's in the CSV.

**Fix:** Check the exact class names in your CSV. `1a` and `1A` are different. Use the exact casing.

---

### ❌ CORS error in browser
If you're accessing the API from a web page and getting a CORS error, make sure the `app.add_middleware(CORSMiddleware, ...)` block is in your code and the server was restarted after adding it.

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install fastapi uvicorn` |
| Start server | `uvicorn main:app --port 8005 --reload` |
| Stop server | `Ctrl + C` |
| All students | `http://127.0.0.1:8005/api` |
| Filter by class | `http://127.0.0.1:8005/api?class=1A` |
| Multiple classes | `http://127.0.0.1:8005/api?class=1A&class=1B` |
| Interactive docs | `http://127.0.0.1:8005/docs` |
