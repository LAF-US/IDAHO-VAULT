# EXECUTE-DEDUPE-FAST.ps1 - Process duplicates from state file
# Per CONSTITUTION.md: "Execute plan" - Logan directed, agent executes

$ErrorActionPreference = "SilentlyContinue"
$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$statePath = "$vaultPath\.opencode\dedupe-state.json"

Write-Host "=== EXECUTING DUPLICATE CLEANUP (FAST) ===" -ForegroundColor Cyan

# Load state
$state = Get-Content $statePath | ConvertFrom-Json
$duplicateGroups = $state.DuplicateGroups

Write-Host "Duplicate groups: $($duplicateGroups.Count)" -ForegroundColor Green
Write-Host "Rule: Keep shortest-named file per group" -ForegroundColor Yellow
Write-Host ""

$totalDeleted = 0
$totalSavedBytes = 0

foreach ($group in $duplicateGroups) {
    $files = @($group.Files)
    
    if ($files.Count -gt 1) {
        # Find file with shortest name (likely original)
        $keepFile = $files | Sort-Object { $_.Name.Length } | Select-Object -First 1
        
        foreach ($file in $files) {
            if ($file.FullName -ne $keepFile.FullName) {
                if (Test-Path $file.FullName) {
                    $fileInfo = Get-Item $file.FullName
                    $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
                    
                    Remove-Item $file.FullName -Force
                    $totalDeleted++
                    $totalSavedBytes += $fileInfo.Length
                    
                    Write-Host "Deleted: $($file.Name) ($sizeMB MB)" -ForegroundColor Gray
                }
            }
        }
    }
}

$savedMB = [math]::Round($totalSavedBytes / 1MB, 2)

Write-Host ""
Write-Host "=== CLEANUP COMPLETE ===" -ForegroundColor Cyan
Write-Host "Deleted: $totalDeleted files" -ForegroundColor Green
Write-Host "Saved: $savedMB MB" -ForegroundColor Green
Write-Host ""
Write-Host "Next: git add -A && git commit -m 'cleanup: remove duplicate files'" -ForegroundColor Yellow
