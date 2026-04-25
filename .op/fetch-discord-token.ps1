$ErrorActionPreference = "SilentlyContinue"

Write-Host "Fetching Discord OpenClaw token from 1Password..." -ForegroundColor Cyan

try {
    $result = op item get "Discord OpenClaw" --field credential --reveal 2>&1
    if ($result -match '^[A-Za-z0-9_-]{20,}') {
        $token = $result
        [System.Environment]::SetEnvironmentVariable("DISCORD_OPENCLAW_TOKEN", $token, "User")
        Write-Host "[OK] Token saved to User environment for future sessions" -ForegroundColor Green
        Write-Host "Start OpenClaw with: openclaw gateway" -ForegroundColor Yellow
        exit 0
    }
} catch {}

Write-Host "[WARN] Could not fetch token automatically" -ForegroundColor Yellow
Write-Host "Please do this manually while 1Password is unlocked:" -ForegroundColor Yellow
Write-Host '  $token = op item get "Discord OpenClaw" --field credential' -ForegroundColor Yellow
Write-Host '  [System.Environment]::SetEnvironmentVariable("DISCORD_OPENCLAW_TOKEN", $token, "User")' -ForegroundColor Yellow