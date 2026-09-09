$ErrorActionPreference = 'Stop'
Set-Location C:/Users/loganf/Documents/IDAHO-VAULT
$prs = @(375,374,353,310,300,299,281,245,232,227,191,173,128,127,126,125,124,123,94,92,91,90,86,85,84,43)
$results = @()
foreach ($n in $prs) {
  $tipFilesRaw = git log "closed-pr/$n" -1 --name-only --format="" 2>$null
  $tipFiles = @($tipFilesRaw | Where-Object { $_ -ne "" -and $_ -ne $null })
  $msg = git log "closed-pr/$n" -1 --format="%s" 2>$null
  Write-Output "=== PR#$n — $msg ==="
  Write-Output "  TIP_FILE_COUNT: $($tipFiles.Count)"
  $checked = 0
  foreach ($f in $tipFiles) {
    if ($checked -ge 20) { Write-Output "  ... ($($tipFiles.Count - 20) more)"; break }
    $checked++
    git cat-file -e "origin/main:$f" 2>$null
    $exists = if ($LASTEXITCODE -eq 0) { "EXISTS" } else { "MISSING" }
    Write-Output "  [$exists] $f"
  }
}
