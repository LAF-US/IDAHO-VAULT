# Convert sort-audit-2026-04-16.md to JSON

$mdPath = "C:\Users\loganf\Documents\IDAHO-VAULT\!\sort-audit-2026-04-16.md"
$jsonPath = "C:\Users\loganf\Documents\IDAHO-VAULT\!\sort-audit-2026-04-16.json"

Write-Host "Converting sort-audit to JSON..." -ForegroundColor Cyan

$content = Get-Content $mdPath -Raw

# Extract summary
$summaryMatch = [regex]::Match($content, '## Summary.*?\| Check \| Count \|.*?(?=##)')
$summary = @{}
if ($summaryMatch.Success) {
    $tableRows = [regex]::Matches($content, '\| (.+?) \| (\d+) \|')
    foreach ($row in $tableRows) {
        $key = $row.Groups[1].Value.Trim()
        $value = [int]$row.Groups[2].Value
        $summary[$key] = $value
    }
}

# Extract misplaced files
$misplacedMatch = [regex]::Match($content, '## Likely Misplaced Files.*?(?=##)')
$misplaced = @()
if ($misplacedMatch.Success) {
    $rows = [regex]::Matches($misplacedMatch.Value, '\| `(.+?)` \| `(.+?)` \| `(.+?)` \| `(.+?)` \|')
    foreach ($row in $rows) {
        $misplaced += [PSCustomObject]@{
            File = $row.Groups[1].Value.Trim()
            CurrentFolder = $row.Groups[2].Value.Trim()
            SuggestedFolder = $row.Groups[3].Value.Trim()
            Reason = $row.Groups[4].Value.Trim()
        }
    }
}

# Extract parent folder files
$parentMatch = [regex]::Match($content, '## Files in parent folders.*?(?=##)')
$parentFolders = @()
if ($parentMatch.Success) {
    $rows = [regex]::Matches($parentMatch.Value, '\| `(.+?)` \| `(.+?)` \| `(.+?)` \|')
    foreach ($row in $rows) {
        $parentFolders += [PSCustomObject]@{
            File = $row.Groups[1].Value.Trim()
            ParentFolder = $row.Groups[2].Value.Trim()
            Subfolders = $row.Groups[3].Value.Trim()
        }
    }
}

# Build JSON object
$auditJson = [PSCustomObject]@{
    Generated = "2026-04-16 23:04 UTC"
    Generator = "GitHub Actions v2"
    Summary = $summary
    LikelyMisplacedFiles = $misplaced
    FilesInParentFolders = $parentFolders
    Note = "Converted from markdown to JSON for posterity. Original file was 17MB+ of audit data."
}

# Save as JSON
$auditJson | ConvertTo-Json -Depth 10 | Out-File $jsonPath -Encoding UTF8

Write-Host "Converted to: $jsonPath" -ForegroundColor Green
Write-Host "JSON size: $((Get-Item $jsonPath).Length / 1KB) KB" -ForegroundColor Yellow

# Remove original .md file
Remove-Item $mdPath -Force
Write-Host "Removed original .md file" -ForegroundColor Green

Write-Host "Done!" -ForegroundColor Cyan
