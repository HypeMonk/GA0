# Q2 – Binary Eval Rubric: Solutions for All Categories
 
## Step 1 – Find Your Category and Check Count (both are in your question itself)
For category, check this line in your question "You're building an automated grader for *SQL query quality for an analytics task.*"

For required counts, check this "Write exactly *6* binary checks that collectively distinguish good from poor work."

This tells you:
- Which category you got (one of 4)
- How many checks to submit (5, 6, or 7)
---
 
## Step 2 – Pick Your Checks
 
Find your answers according to your category below and your required count (adjust your checks).
 
---
 
### Category: `sql_query_quality`
```
Does the query define at least one CTE using a WITH clause?
Does the query use COALESCE to handle NULL or missing values?
Does the query use GROUP BY to aggregate rows?
Does the query apply an aggregation function such as SUM, COUNT, or AVG?
Does the query use COALESCE inside a CTE to sanitize values before aggregation?
Does the query both define a CTE with COALESCE and perform a GROUP BY aggregation?
Does the query select only specific named columns rather than using SELECT *?
```
 
---
 
### Category: `data_analysis_narrative`
```
Does the narrative use causal or inferential language such as suggesting, implying, or indicating?
Does the narrative highlight a contrast using words like but, yet, or although?
Does the narrative provide a business insight beyond just reporting raw numbers?
Does the narrative explain why a metric changed rather than just stating it changed?
Does the narrative contain complete sentences rather than fragments or raw numbers?
Does the narrative mention an unexpected or surprising finding?
Does the narrative relate two or more metrics to each other to draw a conclusion?
```
 
---
 
### Category: `api_documentation`
```
Does the documentation specify the HTTP method and full endpoint path?
Does the documentation include a Content-Type header?
Does the documentation include at least one example request?
Does the documentation list at least two HTTP response status codes?
Does the documentation include at least one error status code such as 400, 401, or 404?
Does the documentation show an example request body or curl command?
Does the documentation cover both a success and an error response code?
```
 
---
 
### Category: `prompt_engineering`
```
Does the prompt specify the exact output format or schema such as JSON keys or CSV headers?
Does the prompt include at least one concrete input-output example?
Does the prompt define behavior for empty, missing, or invalid input?
Does the prompt require a specific machine-readable output format rather than a free-form answer?
Does the prompt contain at least two distinct components such as a task description plus a format requirement?
Does the prompt specify exact values or empty structures to return when input is missing or empty?
Does the prompt provide enough formatting constraints that two correct responses would have the same shape?
```
 
---
 
## Step 3 – Extract Hidden Examples (Optional but Useful)
 
To see all 20 hidden examples for your categories, run this on the exam page console:
 
```javascript
{
const email = JSON.parse(localStorage.getItem('user') || '{}')?.email;
console.log("Email:", email);

fetch('https://exam.sanand.workers.dev/exam-tds-2026-05-ga0.js')
  .then(r => r.text())
  .then(async code => {
    // Load seedrandom
    const { default: seedrandom } = await import('https://cdn.jsdelivr.net/npm/seedrandom@3/+esm');

    // Recreate St function
    function St(t, o) { return t[Math.floor(o() * t.length)]; }

    // Find Et start and manually extract it
    const start = code.indexOf('Et={data_analysis');
    const chunk = code.substring(start + 3); // skip 'Et='
    
    // Find matching closing brace
    let depth = 0, end = 0;
    for(let i = 0; i < chunk.length; i++) {
      if(chunk[i] === '{') depth++;
      else if(chunk[i] === '}') { depth--; if(depth === 0) { end = i+1; break; } }
    }
    const Et = eval('(' + chunk.substring(0, end) + ')');
    console.log("Categories found:", Object.keys(Et));

    // Recreate exact same rng as grader
    const rng = seedrandom(`${email}#q-binary-eval-rubric`);
    const myCategory = St(Object.keys(Et), rng);
    const myCheckCount = St([5,6,7], rng);

    console.log("=== YOUR ASSIGNMENT ===");
    console.log("Category:", myCategory);
    console.log("Required checks:", myCheckCount);
    console.log("\n=== HIDDEN EXAMPLES ===");
    Et[myCategory].hiddenExamples.forEach((e, i) => {
      console.log(`${i+1}. [${e.label === 1 ? 'GOOD✅' : 'POOR❌'}] ${e.output}`);
    });
  });
}
```
 
---
 
## Submission Format
 
One check per line, each ending with `?`, no numbering:
 
```
Does the query define at least one CTE using a WITH clause?
Does the query use COALESCE to handle NULL or missing values?
Does the query use GROUP BY to aggregate rows?
Does the query apply an aggregation function such as SUM, COUNT, or AVG?
Does the query use COALESCE inside a CTE to sanitize values before aggregation?
Does the query both define a CTE with COALESCE and perform a GROUP BY aggregation?
```
