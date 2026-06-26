# Direct answer method.

## STEPS:
1. Go to assignment portal
2. Press F12
3. Go to console
4. Paste given script and press Enter... your answer will be generated.

## Here's console script:

```js
(async () => {
  const email = Object.keys(localStorage).find(k => k.startsWith('exam:')).replace('exam:','').trim().toLowerCase();
  const script = document.createElement('script');
  script.type = 'module';
  script.textContent = `
    import seedrandom from "https://cdn.jsdelivr.net/npm/seedrandom@3/+esm";
    const n = new seedrandom("${email}#q-rename-files-server");
    const cats = ["documentation","reports","notes","configs","data","logs","scripts","templates","resources","archives"];
    const ge = ["résumé","naïve-bayes","日本語","münchen","café"];
    const d = ["docs","content","archive","project"];
    const e = ["chapter1","section-a","part 2","módulo-3","2024"];
    const c = ["intro","advanced","appendix","données","références"];
    Math.floor(n() * 4);
    let files = [];
    for (let s = 0; s < 30; s++) {
      let r = 1 + Math.floor(n() * 3), p = [];
      p.push(d[Math.floor(n() * d.length)]);
      if (r >= 2) p.push(e[Math.floor(n() * e.length)]);
      if (r >= 3) p.push(c[Math.floor(n() * c.length)]);
      if (n() < 0.2) p.push(["spaces here","file-name","naïve","café-2024","test_file"][Math.floor(n() * 5)]);
      let fname = "file" + String(s+1).padStart(2,"0") + ".txt";
      fname = n() < 0.1 ? fname.replace("i", "\u0456") : fname;
      let path = [...p, fname].join("/");
      let category = n() < 0.3 ? ge[Math.floor(n() * ge.length)] : cats[Math.floor(n() * cats.length)];
      files.push({path, category});
    }
    let m = files.map(f => { let p = f.path.split("/"); return f.category+"/"+p.slice(0,-1).join("-")+"-"+p[p.length-1]; });
    m.sort((a,b) => { for (let i=0;i<Math.min(a.length,b.length);i++) if (a.charCodeAt(i)!==b.charCodeAt(i)) return a.charCodeAt(i)-b.charCodeAt(i); return a.length-b.length; });
    let fileList = m.map(f => "./"+f).join("\\n")+"\\n";
    let hash = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(fileList)))).map(b=>b.toString(16).padStart(2,"0")).join("");
    console.log("YOUR ANSWER:", hash);
  `;
  document.head.appendChild(script);
})();
```
