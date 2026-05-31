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

## Step 2 – Select Valid Phrase by Type (pick any one of them as per your graph type)

The grader checks your comment against a list of **exact valid phrases**. 

**Type A (Truncated axis)** [(ratio = dataMax / (dataMax - axisMin))]
- `inflates tiny deltas by {ratio}`
- `magnifies small movement about {ratio}`
- `makes mild change look {ratio}`

**Type B (Dual axis):**
- `rescaled axis fakes synchronized trend`
- `dual-axis scaling manufactures false correlation`
- `secondary scale distorts cross-series comparison`
- `right axis stretched by Nx`

**Type C (Inverted axis):**
- `inverted axis flips decline narrative`
- `descending scale reverses trend meaning`
- `axis direction turns fall into rise`

**Type D (Log scale)** [ratio: (last / Math.max(0.1, first))]
- `log scale compresses linear acceleration`
- `log axis hides arithmetic growth pace`
- `linear growth appears flattened on log`
- `growth visually compressed by {ratio}`

---

## Step 3 – Fix the HTML (can be done by any AI)

Based on your type, make this one change in the `scales` section:

| Type | Remove / Change | Add |
|------|----------------|-----|
| A | `min: 714.54` | `min: 0` or just delete the min line |
| B | `y2` axis + `yAxisID` references | normalize both series to one axis |
| C | `reverse: true` | `reverse: false` |
| D | `type: "logarithmic"` | `type: "linear"` |

---

## Step 4 – Write the HTML Comment (MUST)

At the very top of your fixed HTML, add this comment:

```html
<!-- Quantification: 5.2 Distortion: inflates tiny deltas by 5.2x -->
```

- Replace `5.2` with your actual distortion value
- Replace the phrase with one of the valid phrases.
- The grader checks both the number (within 15% tolerance) and the exact phrase

---

## Step 5 – Final Checklist Before Submitting

- [ ] HTML comment at the top with number + exact phrase
- [ ] `min: 0` (or correct fix for your type) in the scales config
- [ ] Chart still has `<canvas>` and `new Chart(...)` — don't break the structure
- [ ] Data values unchanged

---

