# GIT-ALIGN.ps1 - Align GIT properly for IDAHO-VAULT
# Removes large files from tracking and cleans up .git bloat

$ErrorActionPreference = "Stop"
$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$gitPath = "$vaultPath\.git"

Write-Host "=== GIT ALIGNMENT ===" -ForegroundColor Cyan

# Kill any lingering git processes
Get-Process git -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Remove all lock files
Get-ChildItem $gitPath -Filter "*.lock" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
Remove-Item "$gitPath\index.lock" -Force -ErrorAction SilentlyContinue
Write-Host "Lock files cleared" -ForegroundColor Green

# Ensure .gitignore has all necessary entries
Write-Host "Checking .gitignore..." -ForegroundColor Yellow

$gitignorePath = "$vaultPath\.gitignore"
$gitignore = Get-Content $gitignorePath -Raw

# Add entries if missing
$entriesToCheck = @(
    "!/sort-audit*.md",
    "*.MXF",
    "*.mxf",
    "*.mp4",
    "*.MP4",
    ".codex/log/",
    ".codex/logs/",
    ".cursor/debug-logs/"
)

foreach ($entry in $entriesToCheck) {
    if ($gitignore -notmatch [regex]::Escape($entry)) {
        Add-Content $gitignorePath "`n$entry"
        Write-Host "  Added: $entry" -ForegroundColor Gray
    }
}

# Remove large files from tracking
Write-Host "Removing large files from tracking..." -ForegroundColor Yellow

$largeFiles = @(
    "!/sort-audit-2026-04-16.md"
)

foreach ($file in $largeFiles) {
    if (git -C $vaultPath ls-files $file 2>$null) {
        Write-Host "  Removing: $file" -ForegroundColor Gray
        git -C $vaultPath rm --cached $file 2>$null
    }
}

# Commit the changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git -C $vaultPath add .gitignore
git -C $vaultPath add -u
git -C $vaultPath commit -m "fix: align GIT - remove large files from tracking"

# Run garbage collection
Write-Host "Running garbage collection (this may take a while)..." -ForegroundColor Yellow
git -C $vaultPath gc --aggressive --prune=now

# Check new .git size
$newSize = (Get-ChildItem $gitPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
Write-Host "New .git size: $([math]::Round($newSize / 1MB, 2)) MB" -ForegroundColor Green

Write-Host "=== GIT ALIGNMENT COMPLETE ===" -ForegroundColor Cyan
Write-Host "Next: Confirm ecosystem is functioning, then run duplicate cleanup." -ForegroundColor Yellow
