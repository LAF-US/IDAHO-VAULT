param(
    [string]$OutDir = "",
    [switch]$SkipIfOpUnavailable
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$scriptRoot = Split-Path -Parent $PSScriptRoot
$commonModule = Join-Path (Split-Path -Parent $scriptRoot) "scripts" "vault-common.ps1"

if (Test-Path $commonModule) {
    . $commonModule
}

. (Join-Path $scriptRoot "1password-policy.ps1")
. (Join-Path $scriptRoot "report-safety.ps1")

function Ensure-OpSession {
    if (-not (Assert-OpAvailable)) {
        return $false
    }
    $result = op whoami 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "1Password CLI not signed in. Run 'op signin' first."
        return $false
    }
    return $true
}

$repoRoot = Split-Path -Parent $scriptRoot
$OutDir = Initialize-ReportOutDir -RepoRoot $repoRoot -RequestedOutDir $OutDir

if (-not (Ensure-OpSession)) {
    if ($SkipIfOpUnavailable) {
        Write-Output "1Password unavailable. Skipping preflight check."
        exit 0
    }
    Write-Warning "1Password preflight check skipped due to unavailable 1Password CLI."
    Write-Output "To skip when 1Password unavailable, use -SkipIfOpUnavailable flag."
}

$policy = Get-1PasswordPolicy
$items = op item list --format json | ConvertFrom-Json
$vaultSummary = $items |
    Group-Object { $_.vault.name } |
    Sort-Object Name |
    ForEach-Object {
        [pscustomobject]@{
            vault      = $_.Name
            role       = $policy.vault_roles.$($_.Name)
            total      = $_.Count
            logins     = ($_.Group | Where-Object { $_.category -eq "LOGIN" }).Count
            api_creds  = ($_.Group | Where-Object { $_.category -eq "API_CREDENTIAL" }).Count
            passwords  = ($_.Group | Where-Object { $_.category -eq "PASSWORD" }).Count
            ssh_keys   = ($_.Group | Where-Object { $_.category -eq "SSH_KEY" }).Count
            other      = ($_.Group | Where-Object { $_.category -notin @("LOGIN","API_CREDENTIAL","PASSWORD","SSH_KEY") }).Count
        }
    }

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$jsonPath = Join-Path $OutDir "1password-preflight_$stamp.json"
$mdPath = Join-Path $OutDir "1password-preflight_$stamp.md"
$latestJson = Join-Path $OutDir "1password-preflight_latest.json"
$latestMd = Join-Path $OutDir "1password-preflight_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    policy_path  = Join-Path $repoRoot ".op" "1password-hygiene-policy.json"
    safety_limits = $policy.safety_limits
    vault_summary = $vaultSummary
}

Write-SafeJsonFile -Path $jsonPath -Object $payload -Depth 6
Write-SafeJsonFile -Path $latestJson -Object $payload -Depth 6

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# 1Password Preflight")
$lines.Add("")
$lines.Add("Generated: $(Get-Date -Format s)")
$lines.Add("")
$lines.Add("| Vault | Role | Total | Logins | API Creds | Passwords | SSH Keys | Other |")
$lines.Add("|---|---|---|---|---|---|---|---|")
foreach ($row in $vaultSummary) {
    $lines.Add("| $($row.vault) | $($row.role) | $($row.total) | $($row.logins) | $($row.api_creds) | $($row.passwords) | $($row.ssh_keys) | $($row.other) |")
}
$lines.Add("")
$lines.Add("Safety limits:")
$lines.Add("")
$lines.Add("- max moves: $($policy.safety_limits.max_moves)")
$lines.Add("- max edits: $($policy.safety_limits.max_edits)")
$lines.Add("- max archives: $($policy.safety_limits.max_archives)")

$markdown = $lines -join "`r`n"
Write-SafeTextFile -Path $mdPath -Content $markdown
Write-SafeTextFile -Path $latestMd -Content $markdown

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"