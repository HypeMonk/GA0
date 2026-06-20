# Q4: Execute a Bash Pipeline using the `llm` CLI Tool 

## What This Question Asks

Write a single bash pipeline command that uses Simon Willison's `llm` CLI tool to fetch some data and process it with AI.

> ✅ You only need to **type the command** in the answer box.
> ❌ You do **NOT** need to install anything or actually run it.
> ❌ You do **NOT** need an AIPipe token to submit.

The validator (GPT-5 Nano) just **reads your command** and checks if it looks correct. It never executes it.

---

## How Grading Works

Your answer passes if GPT-5 Nano responds starting with **"YES"**. It checks:

- Does it use Simon Willison's `llm` CLI tool?
- Is it a valid bash pipeline (has `|`)?
- Would it actually accomplish the stated task?
- Is it practical and executable?

**One hard rule from source code:** your command MUST contain the word `llm` — instant fail otherwise.

---

## Your Task Varies Per Student

The question picks **one of 10 tasks** based on your email seed. Look at your exam page to see which task you got, then find your command below.

---

## The Confirmed Working Pattern

```bash
curl -s "[api-url]" | jq -r '.[field]' | llm -s "[detailed instruction]"
```

- `curl -s` → fetches data from an API silently
- `jq -r '.[field]'` → extracts the relevant text field from JSON
- `llm -s` → passes it to the LLM with a system prompt instruction
- For local data (files, git, env) → skip curl and jq, pipe directly to `llm -s`

---

## All 10 Commands — Find Yours and Copy-Paste

### Task 1
**"fetch weather data from wttr.in for London and extract just the temperature in Celsius"**
```bash
llm -f https://wttr.in/London?format=j1 | jq -r '.current_condition[0].temp_C'
```

---

### Task 2
**"list all JavaScript files in the current directory and summarize their purpose in one line each"**
```bash
find . -name "*.js" -type f | llm -s "List all these JavaScript files and summarize their likely purpose in one line each based on their filenames"
```

---

### Task 3
**"read a JSON file and convert it to a markdown table"**
```bash
cat data.json | llm -s "Convert this JSON data into a well-formatted markdown table"
```

---

### Task 4
**"analyze git commit messages from the last 10 commits and suggest areas for improvement"**
```bash
git log --oneline -10 | llm -s "Analyze these git commit messages from the last 10 commits and suggest specific areas for improvement in commit message quality and project practices"
```

---

### Task 5
**"fetch the top Hacker News story title and generate 3 alternative headlines"**
```bash
curl -s "https://hacker-news.firebaseio.com/v1/topstories.json" | jq -r '.[0]' | xargs -I{} curl -s "https://hacker-news.firebaseio.com/v1/item/{}.json" | jq -r '.title' | llm -s "Generate 3 alternative headlines for this Hacker News story title, making them more engaging and creative"
```

---

### Task 6
**"find all TODO comments in Python files in the current directory and prioritize them by urgency"**
```bash
grep -r "TODO" --include="*.py" . | llm -s "Analyze these TODO comments found in Python files and prioritize them by urgency, explaining which should be addressed first and why"
```

---

### Task 7
**"get the latest Bitcoin price from a crypto API and explain if it's a good time to buy"**
```bash
curl -s "https://api.coindesk.com/v1/bpi/currentprice.json" | jq -r '.bpi.USD.rate' | llm -s "The following is the current Bitcoin price in USD. Analyze this price and explain in simple terms whether it might be a good time to buy, considering general market factors"
```

---

### Task 8
**"read a CSV file and generate a brief statistical summary with insights"**
```bash
cat data.csv | llm -s "Generate a brief statistical summary of this CSV data with key insights, trends, and notable patterns"
```

---

### Task 9 ✅ Confirmed Working
**"fetch a random Wikipedia article summary and rewrite it for a 10-year-old audience"**
```bash
curl -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | jq -r '.extract' | llm -s "Rewrite this Wikipedia summary for a 10-year-old audience, making it simple and fun to read"
```

---

### Task 10
**"list all environment variables and identify which ones might contain sensitive information"**
```bash
env | llm -s "Review these environment variables and identify which ones might contain sensitive information such as passwords, API keys, or tokens, explaining why each is potentially sensitive"
```

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| Forgetting `llm` in the command | Always include `llm` — hard fail without it |
| Using `llm` without `-s` flag | Use `llm -s "..."` for system prompt style |
| Short vague prompt | Write a detailed, clear instruction |
| Submitting the output instead of the command | Submit the command text itself |
| Not parsing JSON before `llm` | Use `jq -r '.[field]'` for API responses |
| Copying someone else's command | Tasks vary per student — check which task you got |

---

## Quick Checklist

- [ ] Checked which of the 10 tasks I got on my exam page
- [ ] Found the matching command above
- [ ] Command contains the word `llm`
- [ ] Command uses `llm -s "..."` with a detailed prompt
- [ ] Command has at least one `|` pipe in it
- [ ] Submitted the command text (not any output)
