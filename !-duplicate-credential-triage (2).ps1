param(
    [string]$OutDir = "",
    [ValidateSet("strict", "broad")]
    [string]$Mode = "strict"
)

$ErrorActionPreference = "Stop"

function Ensure-OpSession {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
        throw "1Password CLI 'op' is not installed or not on PATH."
    }

    & op signin | Out-Null
}

function Normalize-Value {
    param([string]$Value)
    if (-not $Value) { return "" }
    $v = $Value.Trim().ToLowerInvariant()
    $v = $v -replace '^https?://', ''
    $v = $v -replace '^www\.', ''
    return $v
}

function Build-DupeKey {
    param(
        [string]$Title,
        [string]$Username,
        [string]$Category,
        [string]$Site,
        [string]$Mode
    )

    $t = Normalize-Value $Title
    $u = Normalize-Value $Username
    $c = Normalize-Value $Category
    $s = Normalize-Value $Site

    if ($t -eq "login" -and $s) {
        $t = $s
    }

    if ($Mode -eq "strict") {
        return "$c|$t|$u"
    }

    if ($u) {
        return "$u|$c"
    }

    return "$c|$t"
}

function New-MarkdownReport {
    param(
        [string]$Path,
        [array]$Groups
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Duplicate Credential Triage")
    $lines.Add("")
    $lines.Add("Generated: $(Get-Date -Format s)")
    $lines.Add("")
    $lines.Add("This report is non-destructive. It suggests current vs stale candidates based on updated timestamps and duplicate grouping heuristics.")
    $lines.Add("")

    foreach ($group in $Groups) {
        $lines.Add("## $($group.key)")
        $lines.Add("")
        $lines.Add("| Status | Vault | Title | Username | Updated | Item ID |")
        $lines.Add("|---|---|---|---|---|---|")

        foreach ($item in $group.items) {
            $lines.Add("| $($item.status) | $($item.vault) | $($item.title) | $($item.username) | $($item.updated_at) | $($item.id) |")
        }

        $lines.Add("")
    }

    if ($Groups.Count -eq 0) {
        $lines.Add("No duplicate candidates found.")
    }

    Set-Content -Path $Path -Value ($lines -join "`r`n")
}

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutDir) {
    $OutDir = Join-Path $repoRoot ".op\reports"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Ensure-OpSession

$items = op item list --format json | ConvertFrom-Json
$rows = New-Object System.Collections.Generic.List[object]

foreach ($item in $items) {
    if ($item.category -notin @("LOGIN", "API_CREDENTIAL", "SSH_KEY", "PASSWORD")) {
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

    $key = Build-DupeKey -Title $item.title -Username $username -Category $item.category -Site $site -Mode $Mode

    $rows.Add([pscustomobject]@{
        key        = $key
        id         = $item.id
        vault      = $item.vault.name
        title      = $item.title
        username   = $username
        category   = $item.category
        site       = $site
        updated_at = [datetime]$item.updated_at
    })
}

$groups = $rows |
    Group-Object key |
    Where-Object { $_.Count -gt 1 } |
    ForEach-Object {
        $sorted = $_.Group | Sort-Object updated_at -Descending
        $itemsOut = New-Object System.Collections.Generic.List[object]

        for ($i = 0; $i -lt $sorted.Count; $i++) {
            $status = if ($i -eq 0) { "current-candidate" } else { "stale-candidate" }
            $itemsOut.Add([pscustomobject]@{
                status     = $status
                id         = $sorted[$i].id
                vault      = $sorted[$i].vault
                title      = $sorted[$i].title
                username   = $sorted[$i].username
                updated_at = $sorted[$i].updated_at.ToString("s")
            })
        }

        [pscustomobject]@{
            key   = $_.Name
            count = $_.Count
            items = $itemsOut
        }
    } |
    Sort-Object -Property @{ Expression = "count"; Descending = $true }, @{ Expression = "key"; Descending = $false }

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$jsonPath = Join-Path $OutDir "duplicate-triage_${Mode}_$stamp.json"
$mdPath = Join-Path $OutDir "duplicate-triage_${Mode}_$stamp.md"
$latestJson = Join-Path $OutDir "duplicate-triage_${Mode}_latest.json"
$latestMd = Join-Path $OutDir "duplicate-triage_${Mode}_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    mode         = $Mode
    groups       = $groups
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $jsonPath
$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $latestJson
New-MarkdownReport -Path $mdPath -Groups $groups
New-MarkdownReport -Path $latestMd -Groups $groups

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"
