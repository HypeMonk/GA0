## There are 2 answers.. TRY BOTH one by one

## ANSWER 1:

```js
function convertToMarkdown(text) {
  const NORMAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const normalArr = [...NORMAL];

  const boldChars = [];
  for (let i = 0; i < 26; i++) boldChars.push(String.fromCodePoint(0x1D5D4 + i));
  for (let i = 0; i < 26; i++) boldChars.push(String.fromCodePoint(0x1D5EE + i));
  for (let i = 0; i < 10; i++) boldChars.push(String.fromCodePoint(0x1D7EC + i));
  const italChars = [];
  for (let i = 0; i < 26; i++) italChars.push(String.fromCodePoint(0x1D608 + i));
  for (let i = 0; i < 26; i++) italChars.push(String.fromCodePoint(0x1D622 + i));
  const monoChars = [];
  for (let i = 0; i < 26; i++) monoChars.push(String.fromCodePoint(0x1D670 + i));
  for (let i = 0; i < 26; i++) monoChars.push(String.fromCodePoint(0x1D68A + i));
  for (let i = 0; i < 10; i++) monoChars.push(String.fromCodePoint(0x1D7F6 + i));

  const boldMap = new Map(boldChars.map((c, i) => [c, normalArr[i]]));
  const italMap = new Map(italChars.map((c, i) => [c, normalArr[i]]));
  const monoMap = new Map(monoChars.map((c, i) => [c, normalArr[i]]));
  const BULLETS = new Set(["\u2022", "\u25E6", "\u25AA", "\u25B8", "\u2023"]);

  function getType(c) {
    if (boldMap.has(c)) return "bold";
    if (italMap.has(c)) return "ital";
    if (monoMap.has(c)) return "mono";
    return "other";
  }
  function decode(c) {
    return boldMap.get(c) ?? italMap.get(c) ?? monoMap.get(c) ?? c;
  }
  function isRegularAsciiLetterOrDigit(c) {
    const code = c.codePointAt(0);
    return (code >= 65 && code <= 90) || (code >= 97 && code <= 122) || (code >= 48 && code <= 57);
  }
  function isMonoLine(line) {
    if (line.trim() === "") return false;
    const chars = [...line];
    let hasContent = false;
    for (const c of chars) {
      if (/\s/.test(c)) continue;
      if (monoMap.has(c)) { hasContent = true; continue; }
      if (boldMap.has(c) || italMap.has(c)) return false;
      if (isRegularAsciiLetterOrDigit(c)) return false;
      hasContent = true;
    }
    return hasContent;
  }

  const lines = text.split("\n");
  const inCodeBlock = new Array(lines.length).fill(false);
  let i = 0;
  while (i < lines.length) {
    if (isMonoLine(lines[i])) {
      let j = i;
      while (j < lines.length && isMonoLine(lines[j])) j++;
      if (j - i >= 3) for (let k = i; k < j; k++) inCodeBlock[k] = true;
      i = j;
    } else {
      i++;
    }
  }

  function formatInline(str) {
    const chars = [...str];
    let out = "";
    let idx = 0;
    while (idx < chars.length) {
      const c = chars[idx];
      const type = getType(c);
      if (type === "bold" || type === "ital" || type === "mono") {
        let lastSameIdx = idx;
        let j = idx + 1;
        while (j < chars.length) {
          const t = getType(chars[j]);
          if (t === type) { lastSameIdx = j; j++; }
          else if (t === "other") {
            if (type === "mono" && !isRegularAsciiLetterOrDigit(chars[j])) j++;
            else if ((type === "bold" || type === "ital") && /\s/.test(chars[j])) j++;
            else break;
          } else break;
        }
        // For mono: also include trailing non-space punctuation (e.g. semicolons)
        if (type === "mono") {
          let k = lastSameIdx + 1;
          while (k < chars.length && getType(chars[k]) === "other"
                 && !isRegularAsciiLetterOrDigit(chars[k]) && !/\s/.test(chars[k])) {
            lastSameIdx = k++;
          }
        }
        let run = "";
        for (let k = idx; k <= lastSameIdx; k++) run += decode(chars[k]);
        const wrap = type === "bold" ? "**" : type === "ital" ? "*" : "`";
        out += wrap + run + wrap;
        idx = lastSameIdx + 1;
      } else {
        out += c;
        idx++;
      }
    }
    return out;
  }

  const result = [];
  let inBlock = false;
  for (let li = 0; li < lines.length; li++) {
    const line = lines[li];
    if (inCodeBlock[li]) {
      if (!inBlock) { result.push("```"); inBlock = true; }
      result.push([...line].map(c => decode(c)).join(""));
    } else {
      if (inBlock) { result.push("```"); inBlock = false; }
      const chars = [...line];
      const firstNonSpace = chars.findIndex(c => !/\s/.test(c));
      if (firstNonSpace !== -1 && BULLETS.has(chars[firstNonSpace])) {
        const rest = chars.slice(firstNonSpace + 1).join("").trimStart();
        result.push("- " + formatInline(rest));
      } else {
        result.push(formatInline(line));
      }
    }
  }
  if (inBlock) result.push("```");
  return result.join("\n");
}
```

## ANSWER 2:

```js
function convertToMarkdown(text) {
  const NORMAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const normalArr = [...NORMAL];

  const boldChars = [];
  for (let i = 0; i < 26; i++) boldChars.push(String.fromCodePoint(0x1D5D4 + i));
  for (let i = 0; i < 26; i++) boldChars.push(String.fromCodePoint(0x1D5EE + i));
  for (let i = 0; i < 10; i++) boldChars.push(String.fromCodePoint(0x1D7EC + i));
  
  const italChars = [];
  for (let i = 0; i < 26; i++) italChars.push(String.fromCodePoint(0x1D608 + i));
  for (let i = 0; i < 26; i++) italChars.push(String.fromCodePoint(0x1D622 + i));
  
  const monoChars = [];
  for (let i = 0; i < 26; i++) monoChars.push(String.fromCodePoint(0x1D670 + i));
  for (let i = 0; i < 26; i++) monoChars.push(String.fromCodePoint(0x1D68A + i));
  for (let i = 0; i < 10; i++) monoChars.push(String.fromCodePoint(0x1D7F6 + i));

  const boldMap = new Map(boldChars.map((c, i) => [c, normalArr[i]]));
  const italMap = new Map(italChars.map((c, i) => [c, normalArr[i]]));
  const monoMap = new Map(monoChars.map((c, i) => [c, normalArr[i]]));

  const BULLETS = new Set(["\u2022", "\u25E6", "\u25AA", "\u25B8", "\u2023"]);

  function getType(c) {
    if (boldMap.has(c)) return "bold";
    if (italMap.has(c)) return "ital";
    if (monoMap.has(c)) return "mono";
    return "other";
  }
  
  function decode(c) {
    return boldMap.get(c) ?? italMap.get(c) ?? monoMap.get(c) ?? c;
  }
  
  function isRegularAsciiLetterOrDigit(c) {
    const code = c.codePointAt(0);
    return (code >= 65 && code <= 90) || (code >= 97 && code <= 122) || (code >= 48 && code <= 57);
  }
  
  function isMonoLine(line) {
    if (line.trim() === "") return false;
    const chars = [...line];
    let hasContent = false;
    for (const c of chars) {
      if (/\s/.test(c)) continue;
      if (monoMap.has(c)) { hasContent = true; continue; }
      if (boldMap.has(c) || italMap.has(c)) return false;
      if (isRegularAsciiLetterOrDigit(c)) return false;
      hasContent = true;
    }
    return hasContent;
  }

  const lines = text.split("\n");
  const inCodeBlock = new Array(lines.length).fill(false);

  let i = 0;
  while (i < lines.length) {
    if (isMonoLine(lines[i])) {
      let j = i;
      while (j < lines.length && isMonoLine(lines[j])) j++;
      // Using >= 2 to safely catch multi-line blocks (including the 2-line example provided)
      if (j - i >= 2) for (let k = i; k < j; k++) inCodeBlock[k] = true;
      i = j;
    } else {
      i++;
    }
  }

  function formatInline(str) {
    const chars = [...str];
    let out = "";
    let idx = 0;
    while (idx < chars.length) {
      const c = chars[idx];
      const type = getType(c);

      if (type === "bold" || type === "ital" || type === "mono") {
        let lastSameIdx = idx;

        let j = idx + 1;
        while (j < chars.length) {
          const t = getType(chars[j]);
          if (t === type) { lastSameIdx = j; j++; }
          else if (t === "other") {
            if (type === "mono" && !isRegularAsciiLetterOrDigit(chars[j])) j++;
            else if ((type === "bold" || type === "ital") && /\s/.test(chars[j])) j++;
            else break;
          } else break;
        }

        if (type === "mono") {
          let k = lastSameIdx + 1;
          while (k < chars.length && getType(chars[k]) === "other"
                 && !isRegularAsciiLetterOrDigit(chars[k]) && !/\s/.test(chars[k])) {
            lastSameIdx = k++;
          }
        }
        
        let run = "";
        for (let k = idx; k <= lastSameIdx; k++) run += decode(chars[k]);
        
        // FIX 1: Corrected the Markdown wrapper assignments
        const wrap = type === "bold" ? "**" : type === "ital" ? "*" : "`";
        out += wrap + run + wrap;
        idx = lastSameIdx + 1;
      } else {
        out += c;
        idx++;
      }
    }
    return out;
  }

  const result = [];
  let inBlock = false;
  for (let li = 0; li < lines.length; li++) {
    const line = lines[li];
    if (inCodeBlock[li]) {
      // FIX 2: Push actual code fences instead of empty strings
      if (!inBlock) { result.push("```"); inBlock = true; }
      result.push([...line].map(c => decode(c)).join(""));
    } else {
      if (inBlock) { result.push("```"); inBlock = false; }
      const chars = [...line];
      const firstNonSpace = chars.findIndex(c => !/\s/.test(c));
      if (firstNonSpace !== -1 && BULLETS.has(chars[firstNonSpace])) {
        const rest = chars.slice(firstNonSpace + 1).join("").trimStart();
        result.push("- " + formatInline(rest));
      } else {
        result.push(formatInline(line));
      }
    }
  }
  if (inBlock) result.push("```");
  return result.join("\n");
}
```
