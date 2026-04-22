param(
    [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutDir) {
    $OutDir = Join-Path $repoRoot ".op\reports"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$patterns = @(
    @{ name = "1password_refs"; pattern = 'op://' },
    @{ name = "openrouter_key_name"; pattern = 'OPENROUTER_API_KEY' },
    @{ name = "openai_key_name"; pattern = 'OPENAI_API_KEY' },
    @{ name = "anthropic_key_name"; pattern = 'ANTHROPIC_API_KEY' },
    @{ name = "google_creds_name"; pattern = 'GOOGLE_APPLICATION_CREDENTIALS' },
    @{ name = "openrouter_sk_value"; pattern = 'sk-or-v1-' },
    @{ name = "anthropic_sk_value"; pattern = 'sk-ant-' },
    @{ name = "openai_sk_value"; pattern = 'sk-proj-|sk-[A-Za-z0-9]{20,}' }
)

$results = New-Object System.Collections.Generic.List[object]

foreach ($entry in $patterns) {
    $matches = rg -n --hidden --glob '!**/node_modules/**' --glob '!**/.git/**' --glob '!**/.claude/cache/**' --glob '!**/.codex/sessions/**' --glob '!**/.codex/log/**' --glob '!**/.op/reports/**' $entry.pattern $repoRoot 2>$null
    if (-not $matches) {
        continue
    }

    foreach ($line in $matches) {
        $results.Add([pscustomobject]@{
            rule  = $entry.name
            match = $line
        })
    }
}

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$jsonPath = Join-Path $OutDir "security-sweep_$stamp.json"
$mdPath = Join-Path $OutDir "security-sweep_$stamp.md"
$latestJson = Join-Path $OutDir "security-sweep_latest.json"
$latestMd = Join-Path $OutDir "security-sweep_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    findings     = $results
}

$payload | ConvertTo-Json -Depth 6 | Set-Content -Path $jsonPath
$payload | ConvertTo-Json -Depth 6 | Set-Content -Path $latestJson

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# Security Sweep")
$lines.Add("")
$lines.Add("Generated: $(Get-Date -Format s)")
$lines.Add("")
$lines.Add("This report is path-and-line oriented. Review findings before treating them as leaks.")
$lines.Add("")
$lines.Add("| Rule | Match |")
$lines.Add("|---|---|")
foreach ($finding in $results) {
    $safe = $finding.match -replace '\|', '\|'
    $lines.Add("| $($finding.rule) | $safe |")
}
if ($results.Count -eq 0) {
    $lines.Add("| none | no findings |")
}

Set-Content -Path $mdPath -Value ($lines -join "`r`n")
Set-Content -Path $latestMd -Value ($lines -join "`r`n")

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"
