# Q25 – Deploy a POST Analytics Endpoint to Vercel

## What the Question Asks

You need to build and deploy a live Python API on Vercel that:
- Accepts a POST request with a list of regions and a latency threshold
- Reads your personal JSON data file
- Returns stats for each region: average latency, 95th percentile latency, average uptime, and breach count
- Works from any browser (CORS enabled)

Everyone gets a **different JSON data file** based on their email — but the code is the same for everyone. Just plug in your file and deploy.

---

## Step 1 – Set Up Vercel

1. Go to [vercel.com](https://vercel.com) and sign up with your GitHub account
2. Install the Vercel CLI on your computer:
```bash
npm install -g vercel
```
3. Login from terminal:
```bash
vercel login
```

---

## Step 2 – Set Up Your Project Folder

Create a new folder on your computer with this exact structure:

```
my-project/
├── api/
│   ├── index.py
│   └── q-vercel-latency.json   ← your personal json files go here
├── requirements.txt
└── vercel.json
```

### Download Your JSON File

On the exam page, click the **q-vercel-latency.json** download button — this is YOUR personal data file. Save it inside the project folder. Do not use anyone else's file.

### `requirements.txt`
```
fastapi
numpy
```

### `vercel.json`
```json
{
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [
    {
      "src": "/api",
      "dest": "api/index.py",
      "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
      }
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### `api/index.py`
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List
import json

app = FastAPI()

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Expose-Headers": "Access-Control-Allow-Origin",
}

DATA_FILE = Path(__file__).parent / "q-vercel-latency.json"
with open(DATA_FILE) as f:
    telemetry_data = json.load(f)

class AnalyticsRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.get("/api")
def read_root():
    return JSONResponse({"status": "ok"}, headers=CORS_HEADERS)

@app.post("/api")
def analyze_latency(request: AnalyticsRequest):
    results = {}
    for region in request.regions:
        rows = [r for r in telemetry_data if r.get("region") == region]
        if not rows:
            results[region] = {"avg_latency":0,"p95_latency":0,"avg_uptime":0,"breaches":0}
            continue
        latencies = sorted([r["latency_ms"] for r in rows])
        uptimes = [r["uptime_pct"] for r in rows]
        n = len(latencies)
        idx = (n-1)*0.95
        lo = int(idx)
        p95 = latencies[lo]+(idx-lo)*(latencies[lo+1]-latencies[lo]) if lo+1 < n else latencies[lo]
        results[region] = {
            "avg_latency": round(sum(latencies)/n, 2),
            "p95_latency": round(p95, 2),
            "avg_uptime": round(sum(uptimes)/len(uptimes), 3),
            "breaches": sum(1 for lat in latencies if lat > request.threshold_ms),
        }
    return JSONResponse({"regions": results}, headers=CORS_HEADERS)

@app.options("/api")
def options_handler():
    return JSONResponse({}, headers=CORS_HEADERS)
```

---

## Step 3 – Deploy to Vercel

Open terminal inside your project folder and run:

```bash
# Deploy to production
vercel --prod
```

During first deploy, Vercel will ask a few questions:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name?** → press Enter (use default)
- **In which directory is your code?** → `./` (press Enter)

After deploy, you'll get a URL like:
```
https://your-project-name.vercel.app
```

**Submit this URL:** `https://your-project-name.vercel.app/api` -- Don't forget to add /api endpoint

---

## Step 4 – What the Grader Checks

The grader sends a POST request to your URL with your specific regions and threshold, then checks the response:

| Check | Tolerance |
|-------|-----------|
| URL ends with `vercel.app` | Exact |
| HTTP status 200 | Exact |
| `Access-Control-Allow-Origin: *` header present | Exact |
| `avg_latency` per region | ±0.5 |
| `p95_latency` per region | ±0.5 |
| `avg_uptime` per region | ±0.2 |
| `breaches` per region | Exact — no tolerance |

---

## Step 5 – Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `hostname must end with vercel.app` | You submitted a localhost URL — deploy to Vercel first |
| `HTTP 500` | JSON file is missing or in wrong folder — must be inside `api/` not root |
| `Enable CORS with Access-Control-Allow-Origin: *` | CORS middleware is missing — copy the code exactly as shown |
| `Missing stats for region X` | Your response must include all requested regions |
| `avg_latency should be X` | You used someone else's JSON file — download YOUR file from the exam page |
| `breaches should be X` | Breaches uses strict `>` not `>=` — the code above is already correct |
| `numpy not found` | Make sure `numpy` is in `requirements.txt` |
| Vercel shows old version | Run `vercel --prod` again after any code changes |
