# ============================================================
#  Stoic Market – Backend + Cloudflared Tunnel Launcher
#  Run this script in a PowerShell window.
#  It installs cloudflared if needed, starts the backend,
#  and opens the tunnel automatically.
# ============================================================

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BackendScript = Join-Path $ProjectDir "dashboard_server.py"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🗿  Stoic Market – Tunnel Launcher                  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Python ──────────────────────────────────────────
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python not found. Install from https://python.org" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python found." -ForegroundColor Green

# ── 2. Install cloudflared if missing ────────────────────────
if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Host "[INFO] cloudflared not found. Downloading..." -ForegroundColor Yellow
    $cfDir = "$env:LOCALAPPDATA\cloudflared"
    New-Item -ItemType Directory -Force -Path $cfDir | Out-Null
    $cfExe = "$cfDir\cloudflared.exe"

    $url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    Invoke-WebRequest -Uri $url -OutFile $cfExe -UseBasicParsing
    $env:Path = "$cfDir;" + $env:Path
    Write-Host "[OK] cloudflared installed to $cfDir" -ForegroundColor Green
} else {
    Write-Host "[OK] cloudflared found." -ForegroundColor Green
}

# ── 3. Start backend in a new window ─────────────────────────
Write-Host ""
Write-Host "[INFO] Starting Python backend on port 8080..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$BackendScript`""

# Wait for the backend to initialise
Start-Sleep -Seconds 3

# Quick health check
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8080/api/status" -TimeoutSec 5
    Write-Host "[OK] Backend is live: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Backend health check failed – it may still be starting." -ForegroundColor Yellow
}

# ── 4. Start Cloudflare tunnel ───────────────────────────────
Write-Host ""
Write-Host "[INFO] Starting Cloudflare tunnel (port 8080)..." -ForegroundColor Yellow
Write-Host "       Watch for the URL below and copy it to Vercel." -ForegroundColor Cyan
Write-Host ""
Write-Host "  Vercel → Settings → Environment Variables" -ForegroundColor White
Write-Host "  Key:   BACKEND_URL" -ForegroundColor White
Write-Host "  Value: <the https://xxxx.trycloudflare.com URL>" -ForegroundColor White
Write-Host ""

cloudflared tunnel --url http://localhost:8080
