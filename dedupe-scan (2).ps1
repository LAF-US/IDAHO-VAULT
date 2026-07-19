# Deduplication Scanner for IDAHO-VAULT
# Scans Root + !/ for true duplicates using MD5 hashing

$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = "Continue"

$vaultPath = "C:\Users\loganf\Documents\IDAHO-VAULT"
$reportPath = "$vaultPath\DEDUPE-REPORT.md"
$statePath = "$vaultPath\.opencode\dedupe-state.json"

# Initialize or load state
if (Test-Path $statePath) {
    $state = Get-Content $statePath | ConvertFrom-Json
    Write-Host "Resuming from previous scan..." -ForegroundColor Yellow
} else {
    $state = @{
        Phase = "SizeGrouping"
        ProcessedFiles = 0
        SizeGroups = @{}
        DuplicateGroups = @()
        StartTime = Get-Date
    }
}

# Phase 1: Collect all files and group by size
if ($state.Phase -eq "SizeGrouping") {
    Write-Host "Phase 1: Collecting files and grouping by size..." -ForegroundColor Cyan

    $allFiles = @()

    # Root files (Obsidian Vault)
    Write-Host "  Scanning root..." -ForegroundColor Gray
    $rootFiles = Get-ChildItem -Path $vaultPath -File | Select-Object FullName, Length, Name, LastWriteTime
    $allFiles += $rootFiles

    # !/ (Nest) files recursively
    Write-Host "  Scanning !/ (Nest)..." -ForegroundColor Gray
    $nestFiles = Get-ChildItem -Path "$vaultPath\!" -File -Recurse | Select-Object FullName, Length, Name, LastWriteTime
    $allFiles += $nestFiles

    Write-Host "  Total files found: $($allFiles.Count)" -ForegroundColor Green

    # Group by size
    Write-Host "  Grouping by file size..." -ForegroundColor Gray
    $sizeGroups = $allFiles | Group-Object Length | Where-Object { $_.Count -gt 1 }

    $state.SizeGroups = @{}
    foreach ($group in $sizeGroups) {
        $state.SizeGroups[$group.Name] = $group.Group | ConvertTo-Json -Compress
    }

    $state.Phase = "Hashing"
    $state.TotalSizeGroups = $sizeGroups.Count
    $state.ProcessedSizeGroups = 0
    $state.FilesToHash = ($sizeGroups | Measure-Object -Property Count -Sum).Sum

    Write-Host "  Size groups with potential duplicates: $($sizeGroups.Count)" -ForegroundColor Green
    Write-Host "  Files requiring hash: $($state.FilesToHash)" -ForegroundColor Green

    $state | ConvertTo-Json -Depth 10 | Out-File $statePath
}

# Phase 2: Hash files in same-size groups
if ($state.Phase -eq "Hashing") {
    Write-Host "Phase 2: Hashing files (same-size groups only)..." -ForegroundColor Cyan

    $duplicateGroups = @()
    $processedHashes = @{}
    $totalFilesToHash = $state.FilesToHash
    $filesHashed = $state.ProcessedFiles

    $sizeGroupKeys = $state.SizeGroups.Keys | Select-Object -Skip $state.ProcessedSizeGroups

    foreach ($sizeKey in $sizeGroupKeys) {
        $groupData = $state.SizeGroups[$sizeKey] | ConvertFrom-Json
        $files = @($groupData)

        if ($files.Count -gt 1) {
            $hashes = @{}

            foreach ($file in $files) {
                $filesHashed++
                $percent = [math]::Round(($filesHashed / $totalFilesToHash) * 100, 1)

                Write-Progress -Activity "Hashing files" -Status "$filesHashed / $totalFilesToHash" -PercentComplete $percent

                try {
                    $hash = Get-FileHash $file.FullName -Algorithm MD5
                    $hashStr = $hash.Hash

                    if ($hashes.ContainsKey($hashStr)) {
                        # Found duplicate
                        $dupGroup = $duplicateGroups | Where-Object { $_.Hash -eq $hashStr }
                        if (-not $dupGroup) {
                            $dupGroup = @{
                                Hash = $hashStr
                                Size = $file.Length
                                Files = @()
                            }
                            $dupGroup.Files += $hashes[$hashStr]
                            $duplicateGroups += $dupGroup
                        }
                        $dupGroup.Files += [PSCustomObject]@{
                            FullName = $file.FullName
                            Name = $file.Name
                            LastWriteTime = $file.LastWriteTime
                        }
                    } else {
                        $hashes[$hashStr] = [PSCustomObject]@{
                            FullName = $file.FullName
                            Name = $file.Name
                            LastWriteTime = $file.LastWriteTime
                        }
                    }
                } catch {
                    # Skip unreadable files
                }
            }
        }

        $state.ProcessedSizeGroups++
        $state.ProcessedFiles = $filesHashed

        # Checkpoint every 10 groups
        if ($state.ProcessedSizeGroups % 10 -eq 0) {
            $state | ConvertTo-Json -Depth 10 | Out-File $statePath
        }
    }

    Write-Progress -Activity "Hashing files" -Completed

    $state.DuplicateGroups = $duplicateGroups
    $state.Phase = "Report"
    $state | ConvertTo-Json -Depth 10 | Out-File $statePath

    Write-Host "  Duplicate groups found: $($duplicateGroups.Count)" -ForegroundColor Green
}

# Phase 3: Generate Report
if ($state.Phase -eq "Report") {
    Write-Host "Phase 3: Generating report..." -ForegroundColor Cyan

    $duplicateGroups = $state.DuplicateGroups
    $totalDuplicates = ($duplicateGroups | ForEach-Object { $_.Files.Count - 1 } | Measure-Object -Sum).Sum
    $recoverableSpace = ($duplicateGroups | ForEach-Object { ($_.Files.Count - 1) * $_.Size } | Measure-Object -Sum).Sum

    $report = @"
# Duplicate Files Report - IDAHO-VAULT

**Generated**: $(Get-Date)
**Scope**: Root (Obsidian Vault) + !/ (Nest)

## Summary

- **Total duplicate groups**: $($duplicateGroups.Count)
- **Total duplicate files**: $totalDuplicates
- **Recoverable space**: $([math]::Round($recoverableSpace / 1MB, 2)) MB

## Duplicate Groups

"@

    $groupNum = 0
    foreach ($dupGroup in $duplicateGroups) {
        $groupNum++
        $fileCount = $dupGroup.Files.Count
        $groupSize = [math]::Round($dupGroup.Size / 1KB, 2)

        $report += "`n### Group $groupNum`: $($dupGroup.Files[0].Name)`n`n"
        $report += "**Size**: $groupSize KB | **Hash**: ``$($dupGroup.Hash)`` | **Files**: $fileCount`n`n"
        $report += "````n"

        foreach ($file in $dupGroup.Files) {
            $report += "$($file.FullName)`n"
        }

        $report += "````n"
    }

    $report | Out-File $reportPath -Encoding UTF8

    Write-Host "  Report saved to: $reportPath" -ForegroundColor Green
    Write-Host "`nDone! Found $totalDuplicates duplicate files." -ForegroundColor Cyan

    # Clean up state file
    Remove-Item $statePath -ErrorAction SilentlyContinue
}

Write-Host "`nScan complete." -ForegroundColor Green
