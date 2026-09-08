param(
    [switch]$DryRun,
    [string[]]$Vaults = @(),
    [int]$MaxArchiveCount = 25,
    [switch]$ForceLargeBatch,
    [string]$ConfirmToken = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "1password-policy.ps1")
$Policy = Get-1PasswordPolicy

if ($PSBoundParameters.ContainsKey("MaxArchiveCount") -eq $false) {
    $MaxArchiveCount = [int]$Policy.safety_limits.max_archives
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
        [int]$MaxArchiveCount,
        [switch]$ForceLargeBatch,
        [string]$ConfirmToken
    )

    if ($ConfirmToken -ne "ARCHIVE_ITEMS") {
        throw "Refusing to archive without -ConfirmToken ARCHIVE_ITEMS."
    }

    if ($TargetCount -gt $MaxArchiveCount -and -not $ForceLargeBatch.IsPresent) {
        throw "Refusing to archive $TargetCount items because MaxArchiveCount is $MaxArchiveCount. Re-run with a higher -MaxArchiveCount or -ForceLargeBatch."
    }
}

function Normalize-Value {
    param([string]$Value)
    if (-not $Value) { return "" }
    $v = $Value.Trim().ToLowerInvariant()
    $v = $v -replace '^https?://', ''
    $v = $v -replace '^www\.', ''
    return $v
}

function Build-ArchiveKey {
    param(
        [string]$Title,
        [string]$Username,
        [string]$Category,
        [string]$Site
    )

    $t = Normalize-Value $Title
    $u = Normalize-Value $Username
    $c = Normalize-Value $Category
    $s = Normalize-Value $Site

    if ($t -eq "login" -and $s) {
        $t = $s
    }

    return "$c|$t|$u"
}

Ensure-OpSession

$items = op item list --format json | ConvertFrom-Json
$rows = New-Object System.Collections.Generic.List[object]

foreach ($item in $items) {
    if ($Vaults.Count -gt 0 -and $item.vault.name -notin $Vaults) {
        continue
    }

    if ($item.category -notin @("LOGIN", "PASSWORD")) {
        continue
    }

    $username = [string]$item.additional_information
    $site = ""
    if ($item.urls -and $item.urls.Count -gt 0) {
        $href = [string]$item.urls[0].href
        if ($href) {
            try {
                if ($href -match '^[a-z]+://') {
                    $uri = [System.Uri]$href
                    $site = $uri.Host
                }
            } catch {
                $site = $href
            }
        }
    }

    $key = Build-ArchiveKey -Title $item.title -Username $username -Category $item.category -Site $site

    $rows.Add([pscustomobject]@{
        key        = $key
        id         = $item.id
        vault      = $item.vault.name
        title      = $item.title
        username   = $username
        site       = $site
        updated_at = [datetime]$item.updated_at
    })
}

$targets = New-Object System.Collections.Generic.List[object]

$groups = $rows | Group-Object key | Where-Object { $_.Count -gt 1 }
foreach ($group in $groups) {
    $sorted = $group.Group | Sort-Object -Property @{ Expression = "updated_at"; Descending = $true }, @{ Expression = "id"; Descending = $false }
    $keeper = $sorted[0]
    foreach ($candidate in ($sorted | Select-Object -Skip 1)) {
        if ($candidate.updated_at -ge $keeper.updated_at) {
            continue
        }

        $targets.Add([pscustomobject]@{
            key        = $group.Name
            id         = $candidate.id
            vault      = $candidate.vault
            title      = $candidate.title
            username   = $candidate.username
            updated_at = $candidate.updated_at.ToString("s")
            keeper_id  = $keeper.id
        })
    }
}

if ($targets.Count -eq 0) {
    Write-Output "No stale duplicate candidates to archive."
    exit 0
}

if (-not $DryRun) {
    Assert-ApplySafety -TargetCount $targets.Count -MaxArchiveCount $MaxArchiveCount -ForceLargeBatch:$ForceLargeBatch -ConfirmToken $ConfirmToken
}

foreach ($target in $targets) {
    if ($DryRun) {
        Write-Output "[dry-run] archive $($target.vault): $($target.title) [$($target.username)] id=$($target.id) keep=$($target.keeper_id)"
        continue
    }

    & op item delete $target.id --vault $target.vault --archive | Out-Null
    Write-Output "[archived] $($target.vault): $($target.title) [$($target.username)] id=$($target.id) keep=$($target.keeper_id)"
}
