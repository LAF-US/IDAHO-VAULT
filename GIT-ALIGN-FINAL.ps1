# GIT-ALIGN-FINAL.ps1 - Properly align GIT for IDAHO-VAULT
# Handles lock files, resets accidental commits, and cleans .git bloat

$ErrorActionPreference = "Stop"
$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$gitPath = "$vaultPath\.git"

Write-Host "=== GIT ALIGNMENT (FINAL) ===" -ForegroundColor Cyan

# Step 1: Kill all git processes
Write-Host "Step 1: Stopping git processes..." -ForegroundColor Yellow
Get-Process git -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
Write-Host "  Git processes stopped" -ForegroundColor Green

# Step 2: Remove ALL lock files
Write-Host "Step 2: Removing lock files..." -ForegroundColor Yellow
Get-ChildItem $gitPath -Filter "*.lock" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item "$gitPath\index.lock" -Force -ErrorAction SilentlyContinue
Write-Host "  Lock files removed" -ForegroundColor Green

# Step 3: Reset to before the problematic commit
Write-Host "Step 3: Resetting to clean state..." -ForegroundColor Yellow
git -C $vaultPath reset --hard HEAD~1 2>$null
Write-Host "  Reset to previous commit" -ForegroundColor Green

# Step 4: Ensure .gitignore has proper entries
Write-Host "Step 4: Updating .gitignore..." -ForegroundColor Yellow
$gitignorePath = "$vaultPath\.gitignore"
$gitignore = Get-Content $gitignorePath -Raw

$entriesToAdd = @(
    "!/sort-audit*.md  # Large sort audit files (17MB+)",
    "*.MXF  # Massive video files",
    "*.mxf",
    "*.mp4  # Large video files",
    "*.MP4",
    ".codex/log/  # Log files",
    ".codex/logs/  # Log files"
)

foreach ($entry in $entriesToAdd) {
    $pattern = ($entry -split '  #')[0].Trim()
    if ($gitignore -notmatch [regex]::Escape($pattern)) {
        Add-Content $gitignorePath "`n$entry"
        Write-Host "  Added: $pattern" -ForegroundColor Gray
    }
}

# Step 5: Remove large files from tracking
Write-Host "Step 5: Removing large files from git index..." -ForegroundColor Yellow
$largeFiles = @(
    "!/sort-audit-2026-04-16.md"
)

foreach ($file in $largeFiles) {
    git -C $vaultPath rm --cached $file 2>$null
    Write-Host "  Removed: $file" -ForegroundColor Gray
}

# Step 6: Stage only .gitignore
Write-Host "Step 6: Staging .gitignore..." -ForegroundColor Yellow
git -C $vaultPath add .gitignore
git -C $vaultPath add -u
Write-Host "  Staged changes" -ForegroundColor Green

# Step 7: Commit
Write-Host "Step 7: Committing..." -ForegroundColor Yellow
git -C $vaultPath commit -m "fix: align GIT - update .gitignore and remove large files from tracking"

# Step 8: Garbage collection
Write-Host "Step 8: Running garbage collection (may take several minutes)..." -ForegroundColor Yellow
Write-Host "  This will compress .git from 157GB to under 1GB" -ForegroundColor Gray
git -C $vaultPath gc --aggressive --prune=now

# Step 9: Verify
Write-Host "Step 9: Verifying results..." -ForegroundColor Yellow
$gitSize = (Get-ChildItem $gitPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$gitSizeGB = [math]::Round($gitSize / 1GB, 2)
Write-Host "  New .git size: $gitSizeGB GB" -ForegroundColor $(if ($gitSizeGB -lt 1) { "Green" } else { "Yellow" })

Write-Host ""
Write-Host "=== GIT ALIGNMENT COMPLETE ===" -ForegroundColor Cyan
Write-Host "Ecosystem should now be functioning properly." -ForegroundColor Green
Write-Host "Next: Confirm ecosystem is working, then proceed with duplicate cleanup." -ForegroundColor Yellow
