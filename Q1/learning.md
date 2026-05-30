# Q1 – Scale Manipulation Repair: What's Really Going On

## The Big Idea

Charts can lie without lying about the data. By changing how the axis is drawn, you can make a tiny 5% growth look like a massive spike. This question teaches you to spot and fix those tricks.

---

## The 4 Types of Manipulation

### Type A – Truncated Axis (most common)
The Y-axis doesn't start at 0. It starts somewhere close to the data, making small differences look huge.

```
Real data: 840 → 884 (5% growth)
Axis starts at: 714
Visual effect: looks like 400% growth!
```

**Fix:** Set `min: 0` so the axis starts at zero.

---

### Type B – Dual Axis
Two different datasets are shown on two different Y-axes. By stretching one axis, you can make two completely unrelated metrics look like they move together perfectly.

**Fix:** Remove the second axis (`y2`) and normalize both series to percentage change so they're comparable.

---

### Type C – Inverted Axis
The Y-axis is flipped upside down (`reverse: true`). So a line going "up" visually is actually going down in value. A declining metric looks like it's rising.

**Fix:** Set `reverse: false`.

---

### Type D – Log Scale
A logarithmic axis compresses large values. Linear (arithmetic) growth looks flat on a log scale, hiding how fast something is actually accelerating.

**Fix:** Change `type: "logarithmic"` to `type: "linear"`.

---

## How the Grader Works

The grader runs 4 checks on your submission:

1. **Numeric check** — Is your distortion number within 15% of the correct value?
2. **Phrase check** — Does your HTML comment contain one of the exact valid phrases?
3. **Axis fix check** — Did you apply the correct code fix for your manipulation type?
4. **Sanity check** — Does the HTML still have a `<canvas>` and `new Chart(...)`?

All 4 must pass. The phrase check is the trickiest — the grader looks for an **exact string match**, so don't paraphrase.

---

## Why the Distortion Formula is Tricky

For Type A, you might think:

```
ratio = visual_range / data_range = (max - axis_min) / (max - data_min)
```

But the grader uses:

```
ratio = dataMax / (dataMax - axisMin)
```

These give different numbers! Always use the console script to get the exact value rather than calculating manually.

---

## Common Mistakes

| Mistake | Why it fails |
|---------|-------------|
| Paraphrasing the phrase | Grader does exact string match |
| Using the wrong distortion formula | Number will be outside 15% tolerance |
| Forgetting `min: 0` | Axis fix check fails |
| Deleting the canvas or Chart.js call | Sanity check fails |
| Putting comment in wrong place | Comment must be in `<!-- -->` at top of HTML |

---

## The Honest Chart vs The Deceptive Chart

| | Deceptive | Honest |
|---|-----------|--------|
| Axis starts at | Some arbitrary low number | 0 |
| Visual impression | Dramatic spike | Gentle, proportional change |
| Data | Same | Same |
| Distortion | High ratio | 1x (no distortion) |

The data never changes — only the presentation does. That's what makes these tricks so sneaky.
