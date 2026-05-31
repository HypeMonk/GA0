# FastAPI batch sentiment analysis — Step-by-Step Guide

## What's the Goal?

Build a POST endpoint at /sentiment that accepts multiple sentences and returns their sentiments. You can use any method (Ollama, rule-based, ML model, etc.).


Requirements:
- Accept JSON with array of sentences: {"sentences": ["I love this!", "I'm sad.", ...]}
- Return JSON with results array: {"results": [{"sentence": "I love this!", "sentiment": "happy"}, ...]}
- Valid sentiments: "happy", "sad", or "neutral"
- Return all sentences in the same order as input
- Pass at least 7 out of 10 test cases to get full score

---


## Step 1: Install Dependencies

Open your terminal and run:

```bash
pip install fastapi uvicorn textblob
python -m textblob.download_corpora
```

That's all you need.

---

## Step 2: Create `main.py`

Create a new file called `main.py` and paste this code:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Sentences(BaseModel):
    sentences: list[str]

class ResultItem(BaseModel):
    sentence: str
    sentiment: str

class Result(BaseModel):
    results: list[ResultItem]

# Strong keywords that override TextBlob if found
HAPPY_WORDS = [
    "love", "loved", "loving", "great", "excellent", "amazing", "awesome",
    "fantastic", "wonderful", "happy", "joyful", "excited", "best", "beautiful",
    "perfect", "brilliant", "superb", "delightful", "glad", "enjoy", "enjoyed",
    "fun", "incredible", "grateful", "thankful", "pleased", "cheerful",
    "outstanding", "terrific", "yay", "hooray", "smile", "laughing", "thrilled",
    "ecstatic", "overjoyed", "blessed", "positive", "like", "liked"
]

SAD_WORDS = [
    "hate", "hated", "terrible", "awful", "horrible", "bad", "worst", "sad",
    "disappointed", "disappointing", "upset", "angry", "frustrated", "annoyed",
    "miserable", "depressed", "crying", "cry", "dreadful", "disgusting",
    "dislike", "unfortunately", "failed", "fail", "failure", "poor", "useless",
    "broken", "hurt", "pain", "suffering", "regret", "sorry", "waste",
    "pathetic", "disaster", "ugly", "boring", "dull", "tired", "exhausted",
    "unfortunate", "tragic", "devastated", "hopeless", "helpless", "furious"
]

def get_sentiment(text):
    lower = text.lower()

    # Count keyword hits
    happy_score = sum(1 for w in HAPPY_WORDS if w in lower.split())
    sad_score   = sum(1 for w in SAD_WORDS   if w in lower.split())

    # Get TextBlob polarity (-1 to +1)
    polarity = TextBlob(text).sentiment.polarity

    # Combine: keywords vote + textblob vote
    if happy_score > sad_score:
        keyword_vote = "happy"
    elif sad_score > happy_score:
        keyword_vote = "sad"
    else:
        keyword_vote = "neutral"

    if polarity > 0.1:
        textblob_vote = "happy"
    elif polarity < -0.1:
        textblob_vote = "sad"
    else:
        textblob_vote = "neutral"

    # If both agree, confident answer
    if keyword_vote == textblob_vote:
        return keyword_vote

    # If keywords found a strong signal, trust them
    if happy_score > 0 or sad_score > 0:
        return keyword_vote

    # Otherwise trust TextBlob
    return textblob_vote

@app.post("/sentiment", response_model=Result)
def sentiment_analysis(data: Sentences):
    results = []
    for sentence in data.sentences:
        sentiment = get_sentiment(sentence)
        results.append({"sentence": sentence, "sentiment": sentiment})
    return {"results": results}
```
--- 

## Step 3: Run the Server

In your terminal, navigate to the folder where `main.py` is saved:

```bash
cd path/to/your/folder
```

Then start the server:

```bash
uvicorn main:app --port 8003 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
```

Your server is now live at: **`http://127.0.0.1:8003/sentiment`**

---

You can also open `http://127.0.0.1:8003/docs` in your browser for a free interactive API explorer that FastAPI generates automatically.

---

## Submission

Keep the server running and submit:

```
http://127.0.0.1:8003/sentiment
```
---

## Common Errors & Fixes

### ❌ `Could not import module "app"`
You ran `uvicorn app:app` but your file is named `main.py`.

**Fix:** Match the command to your filename:
```bash
uvicorn main:app --port 8003 --reload   # if file is main.py
uvicorn app:app  --port 8003 --reload   # if file is app.py
```

---

### ❌ `Address already in use` / `Port 8003 is in use`
Something is already running on that port (maybe a previous server you didn't stop).

**Fix:** Either stop the old server (Ctrl+C in the terminal running it), or use a different port:
```bash
uvicorn main:app --port 8009 --reload
```
---

### ❌ CORS error in browser
If you're accessing the API from a web page and getting a CORS error, make sure the `app.add_middleware(CORSMiddleware, ...)` block is in your code and the server was restarted after adding it.

---
