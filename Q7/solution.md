# Q7 – Count Crawled HTML Files: Solution

## What the Question Asks

You're given a website that works like a real crawl — pages link to other pages, which link to more pages. You need to follow all those links, collect every HTML file, and count how many filenames start with your assigned letters.

Everyone crawls the **same website** but gets **different letter ranges** (e.g. G to Z, A to F, G to L). Just look up your letters in the table below and add them up.

---

## Files Per Letter

| Letter | Count | Letter | Count |
|--------|-------|--------|-------|
| A | 6  | N | 4  |
| B | 2  | O | 7  |
| C | 3  | P | 10 |
| D | 4  | Q | 1  |
| E | 7  | R | 3  |
| F | 8  | S | 12 |
| G | 0  | T | 9  |
| H | 5  | U | 1  |
| I | 3  | V | 3  |
| J | 0  | W | 8  |
| K | 0  | X | 0  |
| L | 2  | Y | 1  |
| M | 7  | Z | 0  |

**Total HTML files found: 106**

---

## Find Your Answer

Just add up the counts for your assigned letters. Examples:

- **G to Z** = 0+5+3+0+0+2+7+4+7+10+1+3+12+9+1+3+8+0+1+0 = **76**
- **G to L** = 0+5+3+0+0+2 = **10**
- **A to F** = 6+2+3+4+7+8 = **30**
- **A to Z** = all letters = **106**

---

## The Script (How We Got These Numbers)

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import Counter

base = "https://sanand0.github.io/tdsdata/crawl_html/"
visited = set()
queue = [base]

while queue:
    url = queue.pop(0)
    if url in visited:
        continue
    visited.add(url)

    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
    except:
        continue

    for a in soup.find_all("a", href=True):
        full = urljoin(url, a["href"])
        if full.startswith(base) and full not in visited:
            queue.append(full)

# Count only .html files
html_files = [u for u in visited if u.endswith(".html") or u.endswith(".htm")]
print(f"Total HTML files found: {len(html_files)}")

counts = Counter(u.split("/")[-1][0].upper() for u in html_files)

print("\n=== Files per letter ===")
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    print(f"{letter}: {counts.get(letter, 0)}")

# Change these to YOUR assigned letters!
start, end = "G", "Z"
total = sum(counts.get(l, 0) for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if start <= l <= end)
print(f"\nTotal from {start} to {end}: {total}")
```

## How the Script Works

The website isn't a simple folder listing — each HTML page contains links to other pages, which link to even more pages. A simple request to the base URL only shows 4 links. You have to follow every link recursively until there's nothing new left to visit.

The script uses a **queue** (BFS — Breadth First Search):

1. Start with the base URL in the queue
2. Visit the first URL, mark it as visited
3. Find all links on that page that stay within the base URL
4. Add any unvisited links to the queue
5. Repeat until the queue is empty

Once all pages are visited, count the filenames by their first letter. Change `start` and `end` to your assigned letters to get your answer.
