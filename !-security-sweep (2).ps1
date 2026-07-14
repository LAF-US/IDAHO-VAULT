param(
    [string]$OutDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$scriptRoot = Split-Path -Parent $PSScriptRoot
$commonModule = Join-Path (Split-Path -Parent $scriptRoot) "scripts" "vault-common.ps1"

if (Test-Path $commonModule) {
    . $commonModule
}

$repoRoot = Split-Path -Parent $scriptRoot
if (-not $OutDir) {
    $OutDir = Join-Path $repoRoot ".op" "reports"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

if (-not (Assert-CommandAvailable "rg" "ripgrep")) {
    Write-Warning "ripgrep (rg) not found. Security sweep will use slower fallback with Select-String."
}

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

$excludeGlobs = @('**/node_modules/**', '**/.git/**', '**/.claude/cache/**', '**/.codex/sessions/**', '**/.codex/log/**', '**/.op/reports/**')

foreach ($entry in $patterns) {
    if (Test-CommandAvailable "rg") {
        $matches = rg -n --hidden $entry.pattern $repoRoot 2>$null | Where-Object {
            $line = $_
            $excluded = $false
            foreach ($glob in $excludeGlobs) {
                if ($line -match [regex]::Escape($glob)) {
                    $excluded = $true
                    break
                }
            }
            -not $excluded
        }
    }
    else {
        $matches = Get-ChildItem -Path $repoRoot -Recurse -File -Exclude "*.dll","*.exe","*.bin" -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch 'node_modules|\.git|\.claude/cache|\.codex/sessions|\.codex/log|\.op/reports' } |
            Select-String -Pattern $entry.pattern -SimpleMatch |
            ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line }
    }

    if (-not $matches) {
        continue
    }

    foreach ($line in $matches) {
        $parts = $line -split ':', 4
        $path = if ($parts.Length -ge 1) { $parts[0] } else { "" }
        $lineNumber = if ($parts.Length -ge 2) { $parts[1] } else { "" }
        $results.Add([pscustomobject]@{
            rule = $entry.name
            path = $path
            line = $lineNumber
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
$lines.Add("This report is sanitized. It records file paths and line numbers only, never matched secret content.")
$lines.Add("")
$lines.Add("| Rule | Path | Line |")
$lines.Add("|---|---|---|")
foreach ($finding in $results) {
    $safePath = $finding.path -replace '\|', '\|'
    $lines.Add("| $($finding.rule) | $safePath | $($finding.line) |")
}
if ($results.Count -eq 0) {
    $lines.Add("| none | no findings | |")
}

Set-Content -Path $mdPath -Value ($lines -join "`r`n")
Set-Content -Path $latestMd -Value ($lines -join "`r`n")

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"