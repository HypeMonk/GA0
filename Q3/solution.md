# Q3 – The Bug Hunter: Property-Based Testing Guide

## What the Question Asks

You're given a **buggy Python function**. Regular unit tests don't catch the bug because they only test small, obvious inputs. Your job is to write a **Hypothesis property test** that automatically finds an input where the buggy function gives the wrong answer.

The grader runs your test against:
1. The **buggy function** — your test must **fail** here (finds the bug)
2. The **correct function** — your test must **pass** here (no false alarms)

You pass only if both conditions are met.

---

## Important: The Grader Uses a Fake Hypothesis

The grader runs in-browser using a **custom fake `st` module** — not real Hypothesis. This means:

- `st.integers(min_value, max_value)` ✅ works
- `st.lists(elements, min_size, max_size)` ✅ works
- `st.text(alphabet, min_size, max_size)` ✅ works
- `st.sampled_from(values)` ✅ works
- `st.floats()` ✅ works
- `st.integers(...).filter(...)` ❌ **does NOT exist — will crash!**

Always use `st.sampled_from()` instead of `.filter()`.

---

## Step 1 – Find Your Assigned Variant

Run this on the **exam page console**:

```javascript
{
const email = JSON.parse(localStorage.getItem('user') || '{}')?.email;
fetch('https://exam.sanand.workers.dev/exam-tds-2026-05-ga0.js')
  .then(r => r.text())
  .then(async code => {
    const { default: seedrandom } = await import('https://cdn.jsdelivr.net/npm/seedrandom@3/+esm');
    const scenarios = [
      {id:"sort-1", name:"Inventory Sort", functionName:"sort_inventory", type:"sort"},
      {id:"sort-2", name:"Ranked Queue Sort", functionName:"sort_ranked_queue", type:"sort"},
      {id:"sort-3", name:"Metrics Sort", functionName:"sort_metrics", type:"sort"},
      {id:"sort-4", name:"Schedule Sort", functionName:"sort_schedule", type:"sort"},
      {id:"rev-1", name:"Ticket Revenue", functionName:"compute_ticket_revenue", type:"revenue"},
      {id:"rev-2", name:"Ad Revenue", functionName:"compute_ad_revenue", type:"revenue"},
      {id:"rev-3", name:"Subscription Revenue", functionName:"compute_subscription_revenue", type:"revenue"},
      {id:"rev-4", name:"Retail Revenue", functionName:"compute_retail_revenue", type:"revenue"},
      {id:"leap-1", name:"Billing Date Parser", functionName:"parse_billing_date", type:"leap"},
      {id:"leap-2", name:"Report Date Parser", functionName:"parse_report_date", type:"leap"},
      {id:"leap-3", name:"Schedule Date Parser", functionName:"parse_schedule_date", type:"leap"},
      {id:"dedupe-1", name:"User Tag Dedupe", functionName:"dedupe_user_tags", type:"dedupe"},
      {id:"dedupe-2", name:"Category Dedupe", functionName:"dedupe_categories", type:"dedupe"},
      {id:"dedupe-3", name:"Topic Dedupe", functionName:"dedupe_topics", type:"dedupe"},
      {id:"page-1", name:"Feed Pagination", functionName:"paginate_feed", type:"pagination"},
      {id:"page-2", name:"Search Pagination", functionName:"paginate_search", type:"pagination"},
      {id:"page-3", name:"Invoice Pagination", functionName:"paginate_invoices", type:"pagination"},
      {id:"avg-1", name:"Sensor Moving Average", functionName:"moving_avg_sensor", type:"moving_avg"},
      {id:"avg-2", name:"Price Moving Average", functionName:"moving_avg_price", type:"moving_avg"},
      {id:"avg-3", name:"Latency Moving Average", functionName:"moving_avg_latency", type:"moving_avg"},
    ];
    const rng = seedrandom(`${email}#q-bug-hunter-property-based-testing`);
    const mine = scenarios[Math.floor(rng() * scenarios.length)];
    console.log("✅ Scenario name:", mine.name);
    console.log("✅ Function name:", mine.functionName);
    console.log("✅ Bug type:", mine.type);
    console.log("\n👉 Use the solution for type:", mine.type);
    console.log("👉 Replace function name with:", mine.functionName);
  });
}
```

**Example output:**
```
✅ Scenario name: Subscription Revenue
✅ Function name: compute_subscription_revenue
✅ Bug type: revenue
👉 Use the solution for type: revenue
👉 Replace function name with: compute_subscription_revenue
```

---

## Step 2 – Pick Your Solution


Find your **bug type** below and copy the code.

(IMPORTANT) Replace the function name(extracted by script) with yours.

---

### Type: `sort` — Sorting Bug
**What the bug does:** Incorrectly swaps equal adjacent elements at even indices, breaking sort for lists with duplicates.
**Fix:** Use only 3 possible values with 4+ elements — forces duplicates every time (pigeonhole principle).

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(min_value=1, max_value=3), min_size=4, max_size=8))
def test_sort(nums):
    # Replace sort_inventory with YOUR function name
    result = sort_inventory(nums)
    assert result == sorted(nums)
```

---

### Type: `revenue` — Integer Overflow Bug 
**What the bug does:** Subtracts 2^32 when result exceeds signed 32-bit max, giving wrong negative numbers for large inputs.
**Fix:** Use large values that push the product above 2,147,483,647.

```python
from hypothesis import given, strategies as st

@given(
    st.integers(min_value=20000, max_value=120000),
    st.integers(min_value=20000, max_value=120000),
)
def test_revenue(price, quantity):
    # Replace compute_subscription_revenue with YOUR function name
    assert compute_subscription_revenue(price, quantity) == price * quantity
```

---

### Type: `leap` — Leap Day Bug
**What the bug does:** Returns Feb 28 instead of Feb 29 for leap year dates like 2000-02-29.
**Fix:** Use `sampled_from` with known leap years — do NOT use `.filter()` as it doesn't exist in the grader.

```python
from hypothesis import given, strategies as st

LEAP_YEARS = [y for y in range(2000, 2025) if y % 4 == 0]

@given(st.sampled_from(LEAP_YEARS))
def test_leap_date(year):
    date_str = f"{year}-02-29"
    # Replace parse_billing_date with YOUR function name
    result = parse_billing_date(date_str)
    assert result.day == 29
    assert result.month == 2
    assert result.year == year
```

---

### Type: `dedupe` — Case-Insensitive Dedup Bug
**What the bug does:** Treats `"A"` and `"a"` as duplicates and removes one, but it should only remove exact duplicates.
**Fix:** Use alphabet with both upper and lowercase letters to force case variants.

```python
from hypothesis import given, strategies as st

@given(st.lists(
    st.text(alphabet="ABCDEFGabcdefg", min_size=1, max_size=2),
    min_size=2, max_size=10
))
def test_dedupe(items):
    # Replace dedupe_user_tags with YOUR function name
    result = dedupe_user_tags(items)
    seen = []
    expected = []
    for item in items:
        if item not in seen:
            seen.append(item)
            expected.append(item)
    assert result == expected
```

---

### Type: `pagination` — Offset Equals Limit Bug
**What the bug does:** When `offset == limit`, it adds 1 to offset, returning the wrong slice.
**Fix:** Use overlapping small ranges for offset and limit so `offset == limit` occurs frequently.

```python
from hypothesis import given, strategies as st

@given(
    st.lists(st.integers(), min_size=10, max_size=20),
    st.integers(min_value=0, max_value=5),
    st.integers(min_value=0, max_value=5),
)
def test_pagination(items, offset, limit):
    # Replace paginate_feed with YOUR function name
    result = paginate_feed(items, offset, limit)
    assert result == items[offset:offset + limit]
```

---

### Type: `moving_avg` — Zero in Window Bug
**What the bug does:** Returns `NaN` for any window containing exactly one zero instead of computing the real average.
**Fix:** Allow zeros in the value range and assert exact expected values.

```python
from hypothesis import given, strategies as st

@given(
    st.lists(st.integers(min_value=-10, max_value=10), min_size=3, max_size=10),
    st.integers(min_value=2, max_value=3),
)
def test_moving_avg(values, window):
    # Replace moving_avg_sensor with YOUR function name
    result = moving_avg_sensor(values, window)
    expected = [sum(values[i:i+window]) / window for i in range(len(values) - window + 1)]
    assert result == expected
```

---

## Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `Your submission must include at least one @given(...) decorator` | Make sure `@given(...)` is on the line above your test function |
| `Define at least one test function whose name starts with test_` | Function name must start with `test_` |
| `Hypothesis did not discover the bug within 1000 examples` | Widen your strategy — use larger/smaller ranges that hit the failing region |
| `Your property also fails on the correct implementation` | Your assertion is wrong — the correct function also fails it. Check your logic |
| `Test setup error` | Check imports and indentation |
| Crash with no message | You probably used `.filter()` — replace with `st.sampled_from()` |

---

## Key Insight

The function name **changes per student** but the bug is the same within a type group:
- `sort_inventory`, `sort_ranked_queue`, `sort_metrics`, `sort_schedule` → all same **sort bug**
- `compute_ticket_revenue`, `compute_ad_revenue` etc. → all same **overflow bug**
- `parse_billing_date`, `parse_report_date` etc. → all same **leap day bug**
- `dedupe_user_tags`, `dedupe_categories` etc. → all same **case dedup bug**
- `paginate_feed`, `paginate_search` etc. → all same **offset==limit bug**
- `moving_avg_sensor`, `moving_avg_price` etc. → all same **zero in window bug**

Just find your function name from the script and swap it into the right solution!
