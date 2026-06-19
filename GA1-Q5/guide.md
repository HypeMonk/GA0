# Q5: Reorganize Files with Shell Commands — Student Guide

## What This Question Asks

You have 30 `.txt` files scattered in nested folders.
Each file has a `category:` tag on its first line.
Your job: flatten and reorganize them by category, then submit a hash.

```
# Before
docs/chapter1/lesson1.txt     ← contains "category: reports" inside

# After
reports/docs-chapter1-lesson1.txt
```

> ⚠️ Every student gets a **different ZIP file**, so your hash will be unique. Do not copy someone else's hash.

---

## Step 1: Download and Extract the ZIP

- Click **"Download Files (ZIP)"** on the exam page
- Extract it into a folder (right-click → Extract, or use `unzip`)
- You should see nested folders with `.txt` files inside

---

## Step 2: Open Your Terminal

| OS | What to use |
|---|---|
| Windows | WSL or Git Bash |
| Mac/Linux | Terminal |

Navigate into your extracted folder:

```bash
cd /path/to/extracted-folder
```

---

## Step 3: Create the Script

Create a file called `reorganize.sh` inside the same folder:

```bash
nano reorganize.sh
```

Paste this script:

```bash
#!/usr/bin/env bash

# Reorganize .txt files by their category tag
find . -type f -name "*.txt" -print0 |
while IFS= read -r -d '' file; do
    category=$(grep -m 1 "^category:" "$file" | cut -d' ' -f2- | tr -d '\r')
    [ -z "$category" ] && continue
    mkdir -p "$category"
    relpath="${file#./}"
    newname=$(printf '%s' "$relpath" | tr '/' '-')
    mv "$file" "$category/$newname"
done

# Remove empty directories
find . -type d -empty -delete

# Generate verification hash (excluding script and README)
echo ""
echo "Your hash:"
find . -type f \
    ! -name "*.sh" \
    ! -name "README.md" \
    | LC_ALL=C sort | sha256sum
```

Save and exit: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## Step 4: Run the Script

```bash
bash reorganize.sh
```

---

## Step 5: Copy Your Hash

You'll see output like:

```
Your hash:
3f9a1cb2d4e7f8a0...  -
```

Copy only the **64-character hex string** (everything before the space). That's your answer. ✅

---

## How the Script Works (Line by Line)

| Part | What it does |
|---|---|
| `find . -type f -name "*.txt" -print0` | Finds all `.txt` files safely (handles spaces in names) |
| `grep -m 1 "^category:"` | Reads only the FIRST category line in each file |
| `cut -d' ' -f2-` | Extracts the category name after `"category: "` |
| `tr -d '\r'` | Removes Windows-style line endings (common bug!) |
| `relpath="${file#./}"` | Strips the leading `./` from the path |
| `tr '/' '-'` | Turns `docs/chapter1/file.txt` → `docs-chapter1-file.txt` |
| `mkdir -p "$category"` | Creates the category folder (only if it doesn't exist) |
| `mv "$file" "$category/$newname"` | Moves and renames the file |
| `find . -type d -empty -delete` | Cleans up empty leftover folders |
| `LC_ALL=C sort` | Sorts consistently across all systems (crucial for hash match!) |

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| Running the script twice on same files | Re-extract the ZIP fresh before running |
| Not using `LC_ALL=C sort` | Always use it — plain `sort` gives wrong hash on some systems |
| Using `set -e` at the top | Causes silent exits if any file has no category — remove it |
| Excluding wrong files from hash | Only exclude `*.sh` and `README.md` |
| Copying someone else's hash | Each student's ZIP is different — run it yourself |

---

## Quick Checklist

- [ ] Downloaded MY zip file from the exam page
- [ ] Extracted it into a clean folder
- [ ] Created `reorganize.sh` inside that folder
- [ ] Ran `bash reorganize.sh`
- [ ] Copied the 64-character hash
- [ ] Submitted only the hex string (no spaces, no `-`)
