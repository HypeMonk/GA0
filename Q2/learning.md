# Q2 – Binary Eval Rubric: Understanding the Question

## What Is This Question Asking?

You need to write a set of YES/NO questions that an AI can use to automatically grade student work. The AI reads a student's output and answers each of your questions. Your questions are then scored based on how well they separate good work from bad work.

---

## Why Binary Checks?

Vague questions like "Is this good?" give inconsistent results from an AI judge. But specific yes/no questions like "Does this use a WITH clause?" are reliable and consistent — the AI either sees it or doesn't.

---

## What Makes a Check Good vs Bad?

| Good Check | Bad Check |
|-----------|-----------|
| Specific and observable from output | Vague or subjective |
| Answers YES for GOOD, NO for POOR | Answers the same for everything |
| Correlation > 0.7 with ground truth | Degenerate (always YES or always NO) |
| Tests one clear feature | Tests multiple ambiguous things |

---

## How the Grader Scores You

Each check is run against 20 hidden examples (10 GOOD, 10 POOR). For each check:

1. AI answers YES or NO for each example
2. Grader computes **correlation** between AI answers and true labels
3. Check **passes** if: correlation > 0.7 AND not degenerate (not always YES or always NO)
4. You need at least **4 checks to pass** out of your total

---

## The 4 Categories

Everyone gets assigned one of these categories based on their email:

| Category | What you're grading |
|----------|-------------------|
| `sql_query_quality` | SQL queries for analytics |
| `data_analysis_narrative` | Business insight paragraphs |
| `api_documentation` | API endpoint docs |
| `prompt_engineering` | Prompts for structured output |

Your required number of checks is also email-based: either **5, 6, or 7**.

---

## How We Reverse-Engineered the Hidden Examples

The exam JS file (`exam-tds-2026-05-ga0.js`) is loaded publicly in the browser. By fetching it and parsing the `Et` object, we can extract all hidden examples with their labels before submitting.

**Script to find your category and check count:**

```javascript
{
const email = JSON.parse(localStorage.getItem('user') || '{}')?.email;

fetch('https://exam.sanand.workers.dev/exam-tds-2026-05-ga0.js')
  .then(r => r.text())
  .then(async code => {
    const { default: seedrandom } = await import('https://cdn.jsdelivr.net/npm/seedrandom@3/+esm');
    function St(t, o) { return t[Math.floor(o() * t.length)]; }
    const start = code.indexOf('Et={data_analysis');
    const chunk = code.substring(start + 3);
    let depth = 0, end = 0;
    for(let i = 0; i < chunk.length; i++) {
      if(chunk[i] === '{') depth++;
      else if(chunk[i] === '}') { depth--; if(depth === 0) { end = i+1; break; } }
    }
    const Et = eval('(' + chunk.substring(0, end) + ')');
    const rng = seedrandom(`${email}#q-binary-eval-rubric`);
    const myCategory = St(Object.keys(Et), rng);
    const myCheckCount = St([5,6,7], rng);
    console.log("✅ Your category:", myCategory);
    console.log("✅ Required checks:", myCheckCount);
  });
}
```

---

## How to Write Checks From Hidden Examples

Once you see the hidden examples, look for features that appear in **every GOOD** but **never in POOR**:

**Example for sql_query_quality:**
- Every GOOD has `WITH` → write a check about CTEs
- Every GOOD has `COALESCE` → write a check about NULL handling
- Every GOOD has `GROUP BY` → write a check about aggregation
- Every POOR is a bare SELECT → checks about CTEs will be perfect separators

**Compound checks are powerful** — combining two features (e.g. "CTE AND COALESCE") gives even higher correlation because both must be present.

---

## Common Errors and Fixes

| Error | Fix |
|-------|-----|
| "You must submit exactly N checks" | Count your lines — must match exactly |
| "Line X must end with ?" | Every line must end with a question mark |
| "Duplicate checks detected" | Each check must be meaningfully different |
| "Insufficient calibrated checks: X/N passed" | Some checks are too vague or degenerate — make them more specific |
| Check is degenerate (always YES) | Too broad — add more specific conditions |
| Check is degenerate (always NO) | Too strict — loosen the condition |
| Low correlation (< 0.7) | Check doesn't separate GOOD from POOR well — look at hidden examples more carefully |

---

## Key Insight

The hidden examples are **publicly accessible** in the exam JS file. Every student gets the same hidden examples for their category — only the category and check count differ by email. Once you know your category, the checks above are tuned to score 6/6 or 7/7.
