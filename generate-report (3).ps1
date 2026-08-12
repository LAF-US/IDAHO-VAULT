# Generate dedupe report from state file

$statePath = "C:\Users\loganf\Documents\IDAHO-VAULT\.opencode\dedupe-state.json"
$reportPath = "C:\Users\loganf\Documents\IDAHO-VAULT\DEDUPE-REPORT.md"

$state = Get-Content $statePath | ConvertFrom-Json
$duplicateGroups = $state.DuplicateGroups

$totalDuplicates = 0
$recoverableBytes = 0

foreach ($group in $duplicateGroups) {
    $fileCount = ($group.Files | Measure-Object).Count
    $totalDuplicates += ($fileCount - 1)
    $recoverableBytes += ($fileCount - 1) * $group.Size
}

$report = "# Duplicate Files Report - IDAHO-VAULT`n`n"
$report += "**Generated**: $(Get-Date)`n"
$report += "**Scope**: Root (Obsidian Vault) + !/ (Nest)`n`n"
$report += "## Summary`n`n"
$report += "- **Duplicate groups**: $($duplicateGroups.Count)`n"
$report += "- **Total duplicate files**: $totalDuplicates`n"
$report += "- **Recoverable space**: $([math]::Round($recoverableBytes / 1MB, 2)) MB`n`n"
$report += "## Duplicate Groups`n`n"

$groupNum = 0
foreach ($group in $duplicateGroups) {
    $groupNum++
    $fileCount = ($group.Files | Measure-Object).Count
    $groupSizeKB = [math]::Round($group.Size / 1KB, 2)

    $report += "### Group $groupNum`: $($group.Files[0].Name)`n`n"
    $report += "**Size**: $groupSizeKB KB | **Hash**: ``$($group.Hash)`` | **Files**: $fileCount`n`n"
    $report += "````n"

    foreach ($file in $group.Files) {
        $report += "$($file.FullName)`n"
    }

    $report += "````n`n"
}

$report | Out-File $reportPath -Encoding UTF8
Write-Host "Report saved to: $reportPath"
Write-Host "Groups: $($duplicateGroups.Count), Duplicates: $totalDuplicates, Space: $([math]::Round($recoverableBytes / 1MB, 2)) MB"
