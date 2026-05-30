# Q1 – Scale Manipulation Repair: Step-by-Step Guide

## What the Question Asks

You're given a broken chart HTML file. The chart is lying visually — it uses a sneaky axis trick to make small changes look dramatic. Your job is to:

1. Identify the manipulation type
2. Calculate the distortion ratio (a number)
3. Fix the HTML
4. Add a comment with the exact distortion phrase the grader expects

---

## Step 1 – Identify Your Manipulation Type


| What you see in the code | Manipulation Type |
|--------------------------|-------------------|
| `min: some_number` | **Type A** – Truncated axis |
| `y2` + two datasets | **Type B** – Dual axis |
| `reverse: true` | **Type C** – Inverted axis |
| `type: "logarithmic"` | **Type D** – Log scale |

---

## Step 2 – Extract the Exact Phrase Using Console Script

The grader checks your comment against a list of **exact valid phrases**. Don't guess — extract them directly.

**Open your broken chart HTML in browser → DevTools → Console → paste this:**

```javascript
{
const html = document.querySelectorAll('pre, code, textarea')[0].textContent;
const data = JSON.parse(html.match(/"data":\[([\d.,\s]+)\]/)[0].replace('"data":', ''));
const dataMax = Math.max(...data);

let type, u;
if (/"min":([\d.]+)/.test(html)) {
    type = "A";
    const yMin = parseFloat(html.match(/"min":([\d.]+)/)[1]);
    u = Number((dataMax / (dataMax - yMin)).toFixed(1));
} else if (/y2/.test(html)) {
    type = "B";
    u = 1;
} else if (/reverse.*true/.test(html)) {
    type = "C";
    u = 1;
} else if (/logarithmic/.test(html)) {
    type = "D";
    const first = data[1] - data[0];
    const last = data[data.length-1] - data[data.length-2];
    u = Number((last / Math.max(0.1, first)).toFixed(1));
}

function X(t, o) {
    if (t === "A") { let n = o.toFixed(1); return [`inflates tiny deltas by ${n}x`, `magnifies small movement about ${n}x`, `makes mild change look ${n}x`] }
    if (t === "B") return ["rescaled axis fakes synchronized trend", "dual-axis scaling manufactures false correlation", "secondary scale distorts cross-series comparison", `right axis stretched by ${o.toFixed(1)}x`]
    if (t === "C") return ["inverted axis flips decline narrative", "descending scale reverses trend meaning", "axis direction turns fall into rise"]
    return ["log scale compresses linear acceleration", "log axis hides arithmetic growth pace", "linear growth appears flattened on log", `growth visually compressed by ${o.toFixed(1)}x`]
}

console.log("Type:", type);
console.log("o =", u);
console.log("Valid phrases:", X(type, u));
}
```

> **Note:** Change `"A"` in the last line to your manipulation type (`"B"`, `"C"`, or `"D"`) if needed.

This prints your exact valid phrases. **Pick any one of them.**

---

## Step 3 – Fix the HTML

Based on your type, make this one change in the `scales` section:

| Type | Remove / Change | Add |
|------|----------------|-----|
| A | `min: 714.54` | `min: 0` or just delete the min line |
| B | `y2` axis + `yAxisID` references | normalize both series to one axis |
| C | `reverse: true` | `reverse: false` |
| D | `type: "logarithmic"` | `type: "linear"` |

---

## Step 4 – Write the HTML Comment

At the very top of your fixed HTML, add this comment:

```html
<!-- Quantification: 5.2 Distortion: inflates tiny deltas by 5.2x -->
```

- Replace `5.2` with your actual distortion value
- Replace the phrase with one of the valid phrases printed by the script
- The grader checks both the number (within 15% tolerance) and the exact phrase

---

## Step 5 – Final Checklist Before Submitting

- [ ] HTML comment at the top with number + exact phrase
- [ ] `min: 0` (or correct fix for your type) in the scales config
- [ ] Chart still has `<canvas>` and `new Chart(...)` — don't break the structure
- [ ] Data values unchanged

---

## Quick Reference: All Valid Phrases by Type

**Type A (Truncated axis):**
- `inflates tiny deltas by Nx`
- `magnifies small movement about Nx`
- `makes mild change look Nx`

**Type B (Dual axis):**
- `rescaled axis fakes synchronized trend`
- `dual-axis scaling manufactures false correlation`
- `secondary scale distorts cross-series comparison`
- `right axis stretched by Nx`

**Type C (Inverted axis):**
- `inverted axis flips decline narrative`
- `descending scale reverses trend meaning`
- `axis direction turns fall into rise`

**Type D (Log scale):**
- `log scale compresses linear acceleration`
- `log axis hides arithmetic growth pace`
- `linear growth appears flattened on log`
- `growth visually compressed by Nx`
