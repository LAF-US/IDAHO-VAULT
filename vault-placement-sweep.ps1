param(
    [string]$OutDir = "",
    [switch]$Apply,
    [switch]$IncludeLowConfidence,
    [ValidateSet("high", "medium", "low")]
    [string]$ApplyThreshold = "high",
    [string[]]$Vaults = @(),
    [int]$MaxMoves = 25,
    [switch]$ForceLargeBatch,
    [string]$ConfirmToken = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "1password-policy.ps1")
$Policy = Get-1PasswordPolicy

if ($PSBoundParameters.ContainsKey("MaxMoves") -eq $false) {
    $MaxMoves = [int]$Policy.safety_limits.max_moves
}

function Ensure-OpSession {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
        throw "1Password CLI 'op' is not installed or not on PATH."
    }

    & op signin | Out-Null
}

function Assert-ApplySafety {
    param(
        [int]$TargetCount,
        [int]$MaxMoves,
        [switch]$ForceLargeBatch,
        [string]$ConfirmToken
    )

    if ($ConfirmToken -ne "MOVE_ITEMS") {
        throw "Refusing to move items without -ConfirmToken MOVE_ITEMS."
    }

    if ($TargetCount -gt $MaxMoves -and -not $ForceLargeBatch.IsPresent) {
        throw "Refusing to move $TargetCount items because MaxMoves is $MaxMoves. Re-run with a higher -MaxMoves or -ForceLargeBatch."
    }
}

function Normalize-Value {
    param([string]$Value)
    if (-not $Value) { return "" }
    return $Value.Trim().ToLowerInvariant()
}

function Get-PrimaryHost {
    param($ItemMeta)

    if (-not $ItemMeta.urls -or $ItemMeta.urls.Count -eq 0) {
        return ""
    }

    $href = [string]$ItemMeta.urls[0].href
    if (-not $href) {
        return ""
    }

    try {
        if ($href -match '^[a-z]+://') {
            return ([System.Uri]$href).Host.ToLowerInvariant()
        }
    } catch {
    }

    return $href.ToLowerInvariant()
}

function Get-ServiceHints {
    param(
        [string]$Title,
        [string]$Username,
        [string]$PrimaryHost
    )

    $text = (($Title, $Username, $PrimaryHost) -join " ").ToLowerInvariant()
    $hints = New-Object System.Collections.Generic.List[string]

    $patterns = @($Policy.managed_service_hints + $Policy.broad_service_hints)

    foreach ($pattern in $patterns) {
        if ($text -match [regex]::Escape($pattern)) {
            $hints.Add($pattern)
        }
    }

    return @($hints | Select-Object -Unique)
}

function Get-VaultRecommendation {
    param($ItemMeta)

    $currentVault = [string]$ItemMeta.vault.name
    $title = [string]$ItemMeta.title
    $category = [string]$ItemMeta.category
    $username = [string]$ItemMeta.additional_information
    $usernameNorm = Normalize-Value $username
    $primaryHost = Get-PrimaryHost -ItemMeta $ItemMeta
    $text = Normalize-Value (($title, $username, $primaryHost) -join " ")
    $hints = @(Get-ServiceHints -Title $title -Username $username -PrimaryHost $primaryHost)

    $targetVault = $null
    $confidence = "low"
    $reasons = New-Object System.Collections.Generic.List[string]

    if ($category -in @("API_CREDENTIAL", "SSH_KEY")) {
        $targetVault = "Vault"
        $confidence = "high"
        $reasons.Add("API credentials and SSH keys are managed centrally in Vault.")
    }

    if (Test-PatternListMatch -Text $text -Patterns $Policy.idahoptv_patterns) {
        $targetVault = "Work"
        $confidence = "high"
        $reasons.Add("Uses an idahoptv.org identity or org-specific handle.")
    }

    if ($currentVault -eq "Wallet") {
        $targetVault = "Wallet"
        if ($confidence -ne "high") {
            $confidence = "low"
        }
        $reasons.Add("Already stored in Wallet; leave unless there is a stronger signal.")
    } elseif (Test-PatternListMatch -Text $primaryHost -Patterns $Policy.financial_host_patterns) {
        $targetVault = "Wallet"
        if ($confidence -ne "high") {
            $confidence = "high"
        }
        $reasons.Add("Financial/billing service belongs in Wallet.")
    }

    if (-not $targetVault -and ($hints | Where-Object { $_ -in @($Policy.managed_service_hints) }).Count -gt 0) {
        $targetVault = "Vault"
        $confidence = "medium"
        $reasons.Add("Developer/tooling credential matches managed services tracked in Vault.")
    }

    if (-not $targetVault -and (Test-PatternListMatch -Text $text -Patterns $Policy.personal_email_patterns)) {
        $targetVault = "Personal"
        $confidence = "medium"
        $reasons.Add("Personal email identity.")
    }

    if (-not $targetVault -and $currentVault -in @("Private", "Personal")) {
        $targetVault = "Personal"
        $confidence = "low"
        $reasons.Add("Defaulting consumer/login items to Personal.")
    }

    if (-not $targetVault) {
        $targetVault = $currentVault
        $confidence = "low"
        $reasons.Add("No strong re-homing signal.")
    }

    return [pscustomobject]@{
        current_vault = $currentVault
        target_vault  = $targetVault
        confidence    = $confidence
        title         = $title
        category      = $category
        username      = $username
        host          = $primaryHost
        hints         = $hints
        reasons       = @($reasons | Select-Object -Unique)
    }
}

function New-MarkdownReport {
    param(
        [string]$Path,
        [array]$Rows
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Vault Placement Sweep")
    $lines.Add("")
    $lines.Add("Generated: $(Get-Date -Format s)")
    $lines.Add("")
    $lines.Add("This report is metadata-only. It proposes likely destination vaults for misplaced items.")
    $lines.Add("")
    $lines.Add("| Confidence | Current | Target | Category | Title | Username | Host | Item ID | Rationale |")
    $lines.Add("|---|---|---|---|---|---|---|---|---|")

    foreach ($row in $Rows) {
        $rationale = ($row.reasons -join "; ")
        $lines.Add("| $($row.confidence) | $($row.current_vault) | $($row.target_vault) | $($row.category) | $($row.title) | $($row.username) | $($row.host) | $($row.id) | $rationale |")
    }

    if ($Rows.Count -eq 0) {
        $lines.Add("| none | | | | | | | | No move candidates detected. |")
    }

    Set-Content -Path $Path -Value ($lines -join "`r`n")
}

function Get-ConfidenceRank {
    param([string]$Confidence)

    switch ($Confidence) {
        "high" { return 3 }
        "medium" { return 2 }
        "low" { return 1 }
        default { return 0 }
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutDir) {
    $OutDir = Join-Path $repoRoot ".op\reports"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Ensure-OpSession

$items = op item list --format json | ConvertFrom-Json
$candidates = New-Object System.Collections.Generic.List[object]

foreach ($itemMeta in $items) {
    if ($Vaults.Count -gt 0 -and $itemMeta.vault.name -notin $Vaults) {
        continue
    }

    if ($itemMeta.category -notin @("LOGIN", "PASSWORD", "API_CREDENTIAL", "SSH_KEY")) {
        continue
    }

    $rec = Get-VaultRecommendation -ItemMeta $itemMeta

    if ($rec.target_vault -eq $rec.current_vault) {
        continue
    }

    if (-not $IncludeLowConfidence.IsPresent -and $rec.confidence -eq "low") {
        continue
    }

    $candidates.Add([pscustomobject]@{
        id            = $itemMeta.id
        current_vault = $rec.current_vault
        target_vault  = $rec.target_vault
        confidence    = $rec.confidence
        category      = $rec.category
        title         = $rec.title
        username      = $rec.username
        host          = $rec.host
        hints         = $rec.hints
        reasons       = $rec.reasons
    })
}

$ordered = $candidates | Sort-Object -Property @{ Expression = "confidence"; Descending = $false }, @{ Expression = "current_vault"; Descending = $false }, @{ Expression = "target_vault"; Descending = $false }, @{ Expression = "title"; Descending = $false }

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$jsonPath = Join-Path $OutDir "vault-placement-sweep_$stamp.json"
$mdPath = Join-Path $OutDir "vault-placement-sweep_$stamp.md"
$latestJson = Join-Path $OutDir "vault-placement-sweep_latest.json"
$latestMd = Join-Path $OutDir "vault-placement-sweep_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    apply        = [bool]$Apply
    include_low_confidence = [bool]$IncludeLowConfidence
    apply_threshold = $ApplyThreshold
    vault_scope  = $Vaults
    max_moves    = $MaxMoves
    candidates   = $ordered
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $jsonPath
$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $latestJson
New-MarkdownReport -Path $mdPath -Rows $ordered
New-MarkdownReport -Path $latestMd -Rows $ordered

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"

if (-not $Apply) {
    Write-Output "Dry run only. No items moved."
    exit 0
}

$thresholdRank = Get-ConfidenceRank -Confidence $ApplyThreshold
$movable = $ordered | Where-Object { (Get-ConfidenceRank -Confidence $_.confidence) -ge $thresholdRank }

Assert-ApplySafety -TargetCount $movable.Count -MaxMoves $MaxMoves -ForceLargeBatch:$ForceLargeBatch -ConfirmToken $ConfirmToken

$moveLog = New-Object System.Collections.Generic.List[object]

foreach ($row in $movable) {
    & op item move $row.id --current-vault $row.current_vault --destination-vault $row.target_vault | Out-Null
    $moveLog.Add([pscustomobject]@{
        moved_at      = (Get-Date).ToString("s")
        id            = $row.id
        title         = $row.title
        category      = $row.category
        username      = $row.username
        confidence    = $row.confidence
        current_vault = $row.current_vault
        target_vault  = $row.target_vault
        rationale     = ($row.reasons -join "; ")
    })
    Write-Output "[moved] $($row.current_vault) -> $($row.target_vault): $($row.title) [$($row.id)]"
}

$moveJsonPath = Join-Path $OutDir "vault-placement-applied_$stamp.json"
$moveLatestJson = Join-Path $OutDir "vault-placement-applied_latest.json"
$moveMdPath = Join-Path $OutDir "vault-placement-applied_$stamp.md"
$moveLatestMd = Join-Path $OutDir "vault-placement-applied_latest.md"

$movePayload = [pscustomobject]@{
    generated_at    = (Get-Date).ToString("s")
    apply_threshold = $ApplyThreshold
    moved_count     = $moveLog.Count
    moved_items     = $moveLog
}

$movePayload | ConvertTo-Json -Depth 8 | Set-Content -Path $moveJsonPath
$movePayload | ConvertTo-Json -Depth 8 | Set-Content -Path $moveLatestJson

$moveLines = New-Object System.Collections.Generic.List[string]
$moveLines.Add("# Vault Placement Applied")
$moveLines.Add("")
$moveLines.Add("Generated: $(Get-Date -Format s)")
$moveLines.Add("")
$moveLines.Add("Apply threshold: $ApplyThreshold")
$moveLines.Add("")
$moveLines.Add("| Confidence | From | To | Category | Title | Username | Item ID | Rationale |")
$moveLines.Add("|---|---|---|---|---|---|---|---|")
foreach ($row in $moveLog) {
    $moveLines.Add("| $($row.confidence) | $($row.current_vault) | $($row.target_vault) | $($row.category) | $($row.title) | $($row.username) | $($row.id) | $($row.rationale) |")
}
if ($moveLog.Count -eq 0) {
    $moveLines.Add("| none | | | | | | | No items met the apply threshold. |")
}

Set-Content -Path $moveMdPath -Value ($moveLines -join "`r`n")
Set-Content -Path $moveLatestMd -Value ($moveLines -join "`r`n")

Write-Output "Applied report:"
Write-Output "  $moveJsonPath"
Write-Output "  $moveMdPath"
Write-Output "  $moveLatestJson"
Write-Output "  $moveLatestMd"
