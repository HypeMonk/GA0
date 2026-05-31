# Ollama + ngrok Setup Guide

Complete setup guide for running a local AI server accessible over the internet.

---

## Prerequisites

- Windows PC
- VS Code installed
- Stable internet connection
- 2-3 GB free disk space

---

## Step 1: Install Ollama

1. Download from https://ollama.com/download
2. Run installer and complete setup
3. Verify installation:

```powershell
ollama --version
```

---

## Step 2: Download Any AI Model

Pull the model:

```powershell
ollama pull gemma2:2b
```

Verify download:

```powershell
ollama list
```

Test the model:

```powershell
ollama run gemma2:2b "Say hello in one word"
```

Press `Ctrl+C` to exit.

---

## Step 3: Configure and Start Ollama Server

### Terminal 1 (PowerShell)

Stop any running Ollama:

```powershell
taskkill /F /IM ollama.exe
```

Wait 5 seconds, then set CORS and start server:

```powershell
$env:OLLAMA_ORIGINS="*"
ollama serve
```

**Keep this terminal running!**

Verify environment variable (optional):

```powershell
echo $env:OLLAMA_ORIGINS
```

Should output: `*`

---

## Step 4: Setup ngrok

### Create Account and Get Token

1. Sign up at https://ngrok.com
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy the token

### Install ngrok

1. Download from https://ngrok.com/download
2. Extract `ngrok.exe` 
3. Place in `C:\ngrok\` (or any folder you prefer)

### Terminal 2 (Command Prompt)

Open a **new** terminal in VS Code:
- Click `+` in terminal panel
- Select **"Command Prompt"** (not PowerShell)

Navigate to ngrok folder:

```cmd
cd C:\ngrok
```

Add your authtoken (replace with your actual token):

```cmd
ngrok config add-authtoken YOUR_TOKEN_HERE
```

---

## Step 5: Start ngrok Tunnel

**Replace `YOUR_EMAIL@ds.study.iitm.ac.in` with your actual email!**

```cmd
ngrok http 11434 --response-header-add "X-Email: YOUR_EMAIL@ds.study.iitm.ac.in" --response-header-add "Access-Control-Allow-Headers: *" --response-header-add "Access-Control-Expose-Headers: X-Email"
```

### Example:

```cmd
ngrok http 11434 --response-header-add "X-Email: 23f200xxx@ds.study.iitm.ac.in" --response-header-add "Access-Control-Allow-Headers: *" --response-header-add "Access-Control-Expose-Headers: X-Email"
```

Copy the **Forwarding** URL from the output:
```
Forwarding    https://abc123def456.ngrok-free.app -> http://localhost:11434
```

**Keep this terminal running!**

---

## Step 6: Test Your Setup

### Browser Test

Visit: `https://YOUR-NGROK-URL.ngrok-free.app/api/version`

You should see JSON:
```json
{"version":"0.x.x"}
```

### Check Headers (Chrome DevTools)

1. Press `F12` on the test page
2. Go to **Network** tab
3. Refresh page (`F5`)
4. Click the `version` request
5. Check **Response Headers**:

Required headers:
```
access-control-allow-origin: *
access-control-allow-headers: *
access-control-expose-headers: X-Email
x-email: YOUR_EMAIL@ds.study.iitm.ac.in
```

---

## Step 7: Submit

Submit your base ngrok URL (without `/api/version`):
```
https://abc123def456.ngrok-free.app
```

**Keep both terminals running until graded!**

---

## Quick Reference

### Terminal 1 (PowerShell) - Ollama
```powershell
# Stop Ollama
taskkill /F /IM ollama.exe

# Set CORS and start
$env:OLLAMA_ORIGINS="*"
ollama serve
```

### Terminal 2 (Command Prompt) - ngrok
```cmd
# Navigate to ngrok
cd C:\ngrok

# Add token (first time only)
ngrok config add-authtoken YOUR_TOKEN

# Start tunnel (replace YOUR_EMAIL)
ngrok http 11434 --response-header-add "X-Email: YOUR_EMAIL@ds.study.iitm.ac.in" --response-header-add "Access-Control-Allow-Headers: *" --response-header-add "Access-Control-Expose-Headers: X-Email"
```

---

## Common Issues

### Port already in use
```powershell
taskkill /F /IM ollama.exe
```

### ngrok not found
```cmd
# Use full path
C:\ngrok\ngrok.exe http 11434 ...
```

### CORS errors
Make sure:
- `$env:OLLAMA_ORIGINS="*"` is set BEFORE `ollama serve`
- Both terminals are still running
- Headers are present in DevTools

### X-Email is null
Check that you:
- Replaced `YOUR_EMAIL` with your actual email
- Added `Access-Control-Expose-Headers: X-Email`
- Can see the header in DevTools

---

## Checklist Before Submitting

- [ ] Terminal 1: `ollama serve` running
- [ ] Terminal 2: `ngrok http 11434` running  
- [ ] Can visit `https://your-url.ngrok-free.app/api/version` in browser
- [ ] DevTools shows `x-email: YOUR_EMAIL@ds.study.iitm.ac.in`
- [ ] DevTools shows `access-control-allow-origin: *`
- [ ] DevTools shows `access-control-expose-headers: X-Email`

---

## What Each Command Does

| Command                                                          | Purpose                                 |
| ---------------------------------------------------------------- | --------------------------------------- |
| `ollama pull gemma2:2b`                                          | Download AI model (1.6 GB)              |
| `$env:OLLAMA_ORIGINS="*"`                                        | Allow cross-origin requests             |
| `ollama serve`                                                   | Start Ollama server on port 11434       |
| `ngrok http 11434`                                               | Create public tunnel to localhost:11434 |
| `--response-header-add "X-Email: ..."`                           | Add email to identify submission        |
| `--response-header-add "Access-Control-Allow-Headers: *"`        | Allow all request headers               |
| `--response-header-add "Access-Control-Expose-Headers: X-Email"` | Let browser read X-Email header         |

---

**Time Required:** 20-30 minutes

**Keep both terminals running until assignment is graded!**
