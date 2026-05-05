# EXECUTE-DEDUPE.ps1 - Execute duplicate cleanup plan
# Per CONSTITUTION.md: Logan directed "Execute plan" - agent executes
# Keeps shortest-named file per group (likely original), deletes rest

$ErrorActionPreference = "SilentlyContinue"
$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$reportPath = "$vaultPath\DEDUPE-REPORT.md"

Write-Host "=== EXECUTING DUPLICATE CLEANUP ===" -ForegroundColor Cyan
Write-Host "Rule: Keep shortest-named file per group, delete rest" -ForegroundColor Yellow
Write-Host ""

# Read report
$reportContent = Get-Content $reportPath -Raw

# Parse duplicate groups
$groups = [regex]::Matches($reportContent, '### Group (\d+): (.+?)\n\n\*\*Size\*\*: (.+?) \| \*\*Hash\*\*:.*?\n\n``\`\`\n(.*?)\`\`\`\`', 'Singleline')

$totalGroups = $groups.Count
$processedGroups = 0
$totalDeleted = 0
$totalSavedMB = 0

Write-Host "Found $totalGroups duplicate groups" -ForegroundColor Green
Write-Host ""

foreach ($group in $groups) {
    $processedGroups++
    $groupNum = $group.Groups[1].Value.Trim()
    $groupName = $group.Groups[2].Value.Trim()
    
    # Extract file paths
    $filesBlock = $group.Groups[4].Value.Trim()
    $files = $filesBlock -split "`n" | Where-Object { $_.Trim() -ne '' }
    
    if ($files.Count -gt 1) {
        # Find file with shortest name (likely the original)
        $keepFile = $files | Sort-Object { [System.IO.Path]::GetFileNameWithoutExtension($_).Length } | Select-Object -First 1
        
        Write-Progress -Activity "Processing duplicate groups" -Status "Group $groupNum" -PercentComplete (($processedGroups / $totalGroups) * 100)
        
        foreach ($file in $files) {
            if ($file -ne $keepFile -and (Test-Path $file)) {
                $fileInfo = Get-Item $file
                $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
                
                Remove-Item $file -Force
                $totalDeleted++
                $totalSavedMB += $sizeMB
                
                Write-Host "  Deleted: $file ($sizeMB MB)" -ForegroundColor Gray
            }
        }
    }
}

Write-Progress -Activity "Processing duplicate groups" -Completed

Write-Host ""
Write-Host "=== CLEANUP COMPLETE ===" -ForegroundColor Cyan
Write-Host "Deleted: $totalDeleted files" -ForegroundColor Green
Write-Host "Saved: $([math]::Round($totalSavedMB, 2)) MB" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Run git add -A and commit changes" -ForegroundColor Yellow
