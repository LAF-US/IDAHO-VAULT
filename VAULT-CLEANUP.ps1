# VAULT-CLEANUP.ps1 - Governance-Compliant Analysis Script
# Per CONSTITUTION.md: Logan directs; agents execute his will.
# This script ANALYZES only - no deletions without explicit Logan instruction.

$ErrorActionPreference = "SilentlyContinue"
$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$gitPath = "$vaultPath\.git"
$reportPath = "$vaultPath\DEDUPE-REPORT.md"

Write-Host "=== IDAHO-VAULT CLEANUP ANALYSIS ===" -ForegroundColor Cyan
Write-Host "Per CONSTITUTION.md: This script analyzes only." -ForegroundColor Yellow
Write-Host "No files will be deleted without Logan's explicit instruction." -ForegroundColor Yellow
Write-Host ""

# ============ STEP 1: Analyze Git History for Bloat ============
Write-Host "Step 1: Analyzing Git history for large files..." -ForegroundColor Cyan

$largeFiles = git -C $vaultPath rev-list --objects --all | git -C $vaultPath cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' | Where-Object { $_ -match 'blob (\d+)' -and [int]$matches[1] -gt 1MB } | ForEach-Object {
    if ($_ -match 'blob (\d+) (.+)') {
        [PSCustomObject]@{
            Size = [int]$matches[1]
            SizeMB = [math]::Round([int]$matches[1] / 1MB, 2)
            Path = $matches[2]
        }
    }
} | Sort-Object Size -Descending

if ($largeFiles -and $largeFiles.Count -gt 0) {
    Write-Host "  Large files found in Git history:" -ForegroundColor Yellow
    $largeFiles | Select-Object -First 15 | ForEach-Object {
        Write-Host "    $($_.SizeMB) MB - $($_.Path)" -ForegroundColor Gray
    }

    # Generate removal script for Logan's review
    $removeScript = "# Git removal commands - REVIEW BEFORE RUNNING`n# Generated: $(Get-Date)`n`n"
    foreach ($file in $largeFiles) {
        $removeScript += "git -C `"$vaultPath`" rm --cached `"$($file.Path)`"`n"
    }
    $removeScript | Out-File "$vaultPath\GIT-REMOVAL-COMMANDS.txt" -Encoding UTF8
    Write-Host "  Removal commands saved to: GIT-REMOVAL-COMMANDS.txt" -ForegroundColor Green
} else {
    Write-Host "  No large files found in Git history." -ForegroundColor Green
}

# ============ STEP 2: Generate Duplicate Review List ============
Write-Host ""
Write-Host "Step 2: Processing DEDUPE-REPORT.md for review..." -ForegroundColor Cyan

if (Test-Path $reportPath) {
    Write-Host "  Report found: $reportPath" -ForegroundColor Green

    # Parse and categorize duplicate groups for Logan's review
    $reviewPath = "$vaultPath\DUPLICATE-REVIEW.txt"
    $review = "DUPLICATE FILES REVIEW - LOGAN'S DECISION REQUIRED`n"
    $review += "Generated: $(Get-Date)`n"
    $review += "Per CONSTITUTION.md: Logan directs; agents execute.`n"
    $review += "=" * 60 + "`n`n"

    $groups = [regex]::Matches((Get-Content $reportPath -Raw), '### Group (\d+): (.+?)\n\n\*\*Size\*\*: (.+?) \| \*\*Hash\*\*:.*?\n\n``\`\`n(.*?)``\`\`', 'Singleline')

    $groupNum = 0
    $totalDuplicates = 0

    foreach ($group in $groups) {
        $groupNum++
        $groupName = $group.Groups[2].Value.Trim()
        $groupSize = $group.Groups[3].Value.Trim()
        $files = $group.Groups[4].Value.Trim() -split "`n" | Where-Object { $_.Trim() -ne '' }

        if ($files.Count -gt 1) {
            $totalDuplicates += ($files.Count - 1)

            $review += "GROUP $groupNum`: $groupName ($groupSize)`n"
            $review += "-" * 40 + "`n"
            $review += "Files ($($files.Count)):`n"

            for ($i = 0; $i -lt $files.Count; $i++) {
                $marker = if ($i -eq 0) { " [KEEP?]" } else { " [DELETE?]" }
                $review += "  $($i+1). $($files[$i])$marker`n"
            }

            $review += "`nLOGAN'S DECISION: ___ [Keep #__ / Delete all except #__ / Delete all / Keep all]`n`n"
        }
    }

    $review += "=" * 60 + "`n"
    $review += "TOTAL DUPLICATE FILES: $totalDuplicates`n"
    $review += "ACTION REQUIRED: Logan must indicate which files to keep/delete for each group.`n"

    $review | Out-File $reviewPath -Encoding UTF8
    Write-Host "  Review file saved to: DUPLICATE-REVIEW.txt" -ForegroundColor Green
    Write-Host "  Total duplicate files: $totalDuplicates" -ForegroundColor Yellow
}

# ============ STEP 3: Git Folder Size Check ============
Write-Host ""
Write-Host "Step 3: Checking .git folder size..." -ForegroundColor Cyan

if (Test-Path $gitPath) {
    $gitSize = (Get-ChildItem $gitPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $gitSizeMB = [math]::Round($gitSize / 1MB, 2)
    Write-Host "  Current .git size: $gitSizeMB MB" -ForegroundColor $(if ($gitSizeMB -gt 500) { "Yellow" } else { "Green" })

    if ($gitSizeMB -gt 500) {
        Write-Host "  RECOMMENDATION: Run 'git gc --aggressive --prune=now' after removing large files." -ForegroundColor Yellow
    }
}

# ============ STEP 4: Cloud Sync Recommendations ============
Write-Host ""
Write-Host "Step 4: Cloud sync optimization recommendations..." -ForegroundColor Cyan
Write-Host ""
Write-Host "  Add these to cloud drive exclusion list:" -ForegroundColor Yellow
Write-Host "    - *.MXF, *.mxf (21GB+ files in root)" -ForegroundColor Gray
Write-Host "    - *.mp4, *.MP4 (large video files)" -ForegroundColor Gray
Write-Host "    - google-cloud-sdk/ (7,245 files - MISPLACED per VAULT-CONVENTIONS)" -ForegroundColor Gray
Write-Host "    - .git/ (1GB - already synced, but large)" -ForegroundColor Gray
Write-Host "    - __pycache__/, *.pyc (generated files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Per VAULT-CONVENTIONS.md:" -ForegroundColor Yellow
Write-Host "    - Root-flat notes are INTENTIONAL - do not mass-move" -ForegroundColor Gray
Write-Host "    - Only Logan authorizes restructuring of live vault" -ForegroundColor Gray
Write-Host "    - Persona dotfolders are protected boundaries" -ForegroundColor Gray

# ============ SUMMARY ============
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "ANALYSIS COMPLETE - NO CHANGES MADE" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Files generated for Logan's review:" -ForegroundColor White
Write-Host "  1. GIT-REMOVAL-COMMANDS.txt - Large files to remove from git" -ForegroundColor Gray
Write-Host "  2. DUPLICATE-REVIEW.txt - Duplicate groups requiring decisions" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps (Logan's action required):" -ForegroundColor Yellow
Write-Host "  1. Review DUPLICATE-REVIEW.txt and mark decisions" -ForegroundColor Gray
Write-Host "  2. Review GIT-REMOVAL-COMMANDS.txt and approve/modify" -ForegroundColor Gray
Write-Host "  3. Direct agent to execute approved actions" -ForegroundColor Gray
Write-Host ""
