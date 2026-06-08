# Ollama + ngrok: One Script Setup Guide

Run everything with a single PowerShell script - no manual terminal management needed!

---

## Prerequisites

Make sure these are already installed:
- [Ollama](https://ollama.com/download) 
- [ngrok](https://ngrok.com/download) (with authtoken already configured)
- VS Code

---

## Step 1: Create the Script File

1. Open **VS Code**
2. Click **File** → **New File**
3. Click **File** → **Save As**
4. Name it `start.ps1`
5. Save it somewhere easy like `C:\Users\HP\start.ps1`

---

## Step 2: Paste the Script

Copy and paste this entire code into the file:

```powershell
# ============================================
# CONFIG - Change only these two lines
# ============================================
$EMAIL = "23f200xxxx@ds.study.iitm.ac.in"
$NGROK_PATH = "C:\Users\HP\ngrok\ngrok.exe"
# ============================================

Write-Host "`n Step 1: Killing all existing Ollama processes..." -ForegroundColor Yellow
taskkill /F /IM ollama.exe /T 2>$null
Start-Sleep -Seconds 3
Write-Host " Ollama killed!" -ForegroundColor Green

Write-Host "`n Step 2: Killing all existing ngrok processes..." -ForegroundColor Yellow
taskkill /F /IM ngrok.exe /T 2>$null
Start-Sleep -Seconds 2
Write-Host " ngrok killed!" -ForegroundColor Green

Write-Host "`n Step 3: Starting Ollama with CORS enabled..." -ForegroundColor Yellow
$env:OLLAMA_ORIGINS = "*"
$env:OLLAMA_HOST = "0.0.0.0:11434"
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Write-Host " Waiting for Ollama to start..." -ForegroundColor Cyan

$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 2
    Write-Host "   ...waiting ($($i*2)s)" -ForegroundColor Gray
}

if (-not $ready) {
    Write-Host " ERROR: Ollama failed to start! Check if ollama is installed." -ForegroundColor Red
    exit 1
}
Write-Host " Ollama is running!" -ForegroundColor Green

Write-Host "`n Step 4: Starting ngrok tunnel..." -ForegroundColor Yellow
Start-Process -FilePath $NGROK_PATH -ArgumentList "http 11434 --response-header-add `"X-Email: $EMAIL`" --response-header-add `"Access-Control-Allow-Headers: *`" --response-header-add `"Access-Control-Expose-Headers: X-Email`"" -WindowStyle Hidden
Start-Sleep -Seconds 4

Write-Host " Fetching ngrok public URL..." -ForegroundColor Cyan
$PUBLIC_URL = $null
for ($i = 0; $i -lt 10; $i++) {
    try {
        $tunnels = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
        $https = $tunnels.tunnels | Where-Object { $_.public_url -like "https://*" }
        if ($https) { $PUBLIC_URL = $https[0].public_url; break }
    } catch {}
    Start-Sleep -Seconds 2
    Write-Host "   ...waiting ($($i*2)s)" -ForegroundColor Gray
}

if (-not $PUBLIC_URL) {
    Write-Host " ERROR: Could not get ngrok URL! Check ngrok path or token." -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " SUCCESS! Submit this URL:" -ForegroundColor Green
Write-Host " $PUBLIC_URL" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

$PUBLIC_URL | Set-Clipboard
Write-Host " URL copied to clipboard!" -ForegroundColor Green
Write-Host " Keep this window open until assignment is graded!`n" -ForegroundColor Yellow
```

---

## Step 3: Edit Your Details

At the top of the file, change these **2 lines only**:

### Line 1: Your Email
```powershell
$EMAIL = "23f200xxxx@ds.study.iitm.ac.in"
```
Replace with your actual student email. Example:
```powershell
$EMAIL = "21f1234567@ds.study.iitm.ac.in"
```

### Line 2: Your ngrok Path
```powershell
$NGROK_PATH = "C:\Users\HP\ngrok\ngrok.exe"
```
Not sure where ngrok is? Run this in terminal:
```powershell
where.exe ngrok
```
Copy the output path and paste it. Example:
```powershell
$NGROK_PATH = "C:\Users\YourName\ngrok\ngrok.exe"
```

**Save the file** after editing (`Ctrl+S`)

---

## Step 4: Run the Script

Open a **PowerShell terminal** in VS Code:
- Click **Terminal** → **New Terminal**
- Make sure it says `PS` (PowerShell)

Run this command (replace path with where you saved the file):

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\HP\start.ps1"
```

---

## Step 5: Get Your URL

Wait for the script to finish (~15-20 seconds). You'll see:

```
 Step 1: Killing all existing Ollama processes...
 Ollama killed!

 Step 2: Killing all existing ngrok processes...
 ngrok killed!

 Step 3: Starting Ollama with CORS enabled...
 Waiting for Ollama to start...
   ...waiting (2s)
 Ollama is running!

 Step 4: Starting ngrok tunnel...
 Fetching ngrok public URL...

========================================
 SUCCESS! Submit this URL:
 https://abc123.ngrok-free.app
========================================

 URL copied to clipboard!
 Keep this window open until assignment is graded!
```

The URL is **automatically copied to your clipboard!**

---

## Step 6: Submit

1. Go to your assignment page
2. Paste the URL (`Ctrl+V`)
3. Submit!

---

## Important Notes

- **Keep the terminal open** until assignment is graded
- **URL changes** every time you run the script - always submit the latest one
- If something breaks, just run the script again - it kills everything and starts fresh

---

## Common Errors

| Error | Fix |
|-------|-----|
| `cannot find the file specified` | Wrong `$NGROK_PATH` - run `where.exe ngrok` to find correct path |
| `Ollama failed to start` | Ollama not installed - download from ollama.com |
| `Could not get ngrok URL` | ngrok token not configured - run `ngrok config add-authtoken YOUR_TOKEN` |
| Script won't run | Use `powershell -ExecutionPolicy Bypass -File "path\to\start.ps1"` |

---

## One-Time ngrok Setup (if not done already)

If you haven't added your ngrok token yet:

1. Go to https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy your token
3. Run in terminal:
```powershell
ngrok config add-authtoken YOUR_TOKEN_HERE
```
Only needed once!
