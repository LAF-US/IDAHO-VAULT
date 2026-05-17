param(
    [string]$OutDir = "",
    [switch]$IncludeAllItems,
    [ValidateSet("api-surface", "account-surface", "all")]
    [string]$Mode = "api-surface"
)

$ErrorActionPreference = "Stop"

function Ensure-OpSession {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
        throw "1Password CLI 'op' is not installed or not on PATH."
    }

    & op signin | Out-Null
}

function Get-ServiceHints {
    param(
        [string]$Title,
        [string]$Username,
        [string]$UrlBlob
    )

    $text = (($Title, $Username, $UrlBlob) -join " ").ToLowerInvariant()
    $hints = @()

    $patterns = @(
        "openrouter",
        "anthropic",
        "claude",
        "openai",
        "gpt",
        "vertex",
        "google",
        "github",
        "linear",
        "slack",
        "figma",
        "mistral",
        "huggingface",
        "xai",
        "grok"
    )

    foreach ($pattern in $patterns) {
        if ($text -match [regex]::Escape($pattern)) {
            $hints += $pattern
        }
    }

    return ($hints | Select-Object -Unique)
}

function Get-ManagedServices {
    return @(
        "openrouter",
        "anthropic",
        "claude",
        "openai",
        "gpt",
        "vertex",
        "google",
        "github",
        "linear",
        "what3words",
        "mistral",
        "huggingface",
        "slack",
        "figma",
        "xai",
        "grok"
    )
}

function Get-CanonicalTitle {
    param($Row)

    $u = [string]$Row.username
    $h = @($Row.service_hints)

    if ($u -eq "OpenRouter" -or $h -contains "openrouter") { return "OpenRouter API Key" }
    if ($u -eq "Claude anthro-key" -or $h -contains "anthropic" -or $h -contains "claude") { return "Anthropic API Key" }
    if ($u -eq "LINEAR_API_KEY" -or $h -contains "linear") { return "Linear API Key" }
    if ($u -eq "GOOGLE_VERTEX_AI_API_KEY" -or ($h -contains "vertex" -and $h -contains "google")) { return "Google Vertex AI API Key" }
    if ($h -contains "github") { return "GitHub Credential" }
    if ($h -contains "openai") { return "OpenAI Credential" }
    if ($h -contains "what3words") { return "what3words API Key" }
    if ($h -contains "mistral") { return "Mistral API Key" }
    if ($h -contains "huggingface") { return "Hugging Face Credential" }
    if ($h -contains "slack") { return "Slack Credential" }
    if ($h -contains "google") { return "Google Credential" }

    return $null
}

function Get-CleanupRecommendation {
    param($Row)

    if ($Row.category -eq "API_CREDENTIAL") {
        $canonical = Get-CanonicalTitle -Row $Row
        if ($Row.title -eq "API Credentials" -and $canonical) {
            return "Rename to '$canonical'; keep credential field stable."
        }
        return "API credential looks in-scope."
    }

    if ($Row.category -eq "LOGIN" -and $Row.service_hints.Count -gt 0) {
        return "Check whether this should stay a login item or be replaced by a dedicated API credential item."
    }

    if ($Row.category -eq "SSH_KEY") {
        return "SSH key item; verify intended repo/service coverage."
    }

    return "Review."
}

function Get-ConcealedFieldRefs {
    param($Fields)

    $refs = @()
    foreach ($field in ($Fields | Where-Object { $_.type -eq "CONCEALED" })) {
        $refs += [pscustomobject]@{
            label     = $field.label
            field_id  = $field.id
            reference = $field.reference
        }
    }

    return $refs
}

function New-MarkdownReport {
    param(
        [string]$Path,
        [array]$Rows,
        [array]$Duplicates
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Credential Sweep")
    $lines.Add("")
    $lines.Add("Generated: $(Get-Date -Format s)")
    $lines.Add("")
    $lines.Add("This report is sanitized. It includes item metadata and secret references, never secret values.")
    $lines.Add("")
    $lines.Add("## High-Signal Credentials")
    $lines.Add("")
    $lines.Add("| Vault | Title | Category | Username | Hints | Concealed Refs | Item ID | Canonical Title | Action |")
    $lines.Add("|---|---|---|---|---|---|---|---|---|")

    foreach ($row in $Rows) {
        $refs = if ($row.concealed_refs.Count -gt 0) {
            ($row.concealed_refs | ForEach-Object { $_.reference }) -join "<br>"
        } else {
            ""
        }

        $hints = ($row.service_hints -join ", ")
        $lines.Add("| $($row.vault) | $($row.title) | $($row.category) | $($row.username) | $hints | $refs | $($row.id) | $($row.canonical_title) | $($row.action) |")
    }

    $lines.Add("")
    $lines.Add("## Duplicate Candidates")
    $lines.Add("")

    if ($Duplicates.Count -eq 0) {
        $lines.Add("None detected by title/category/username heuristics.")
    } else {
        $lines.Add("| Key | Count | Item IDs |")
        $lines.Add("|---|---|---|")
        foreach ($dup in $Duplicates) {
            $lines.Add("| $($dup.key) | $($dup.count) | $($dup.ids -join ', ') |")
        }
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
$detailRows = New-Object System.Collections.Generic.List[object]
$managedServices = @(Get-ManagedServices)

foreach ($item in $items) {
    $category = $item.category
    $metadataUsername = [string]$item.additional_information
    $metadataUrlBlob = ""
    if ($item.urls) {
        $metadataUrlBlob = (($item.urls | ForEach-Object { $_.href }) -join " ")
    }
    $metadataHints = @(Get-ServiceHints -Title $item.title -Username $metadataUsername -UrlBlob $metadataUrlBlob)

    $candidate = $IncludeAllItems.IsPresent -or
        $category -eq "API_CREDENTIAL" -or
        ($category -in @("LOGIN", "PASSWORD", "SSH_KEY") -and $metadataHints.Count -gt 0)
    if (-not $candidate) {
        continue
    }

    $full = op item get $item.id --format json | ConvertFrom-Json
    $usernameField = $full.fields | Where-Object { $_.id -eq "username" } | Select-Object -First 1
    $urlBlob = ""
    if ($full.urls) {
        $urlBlob = (($full.urls | ForEach-Object { $_.href }) -join " ")
    }

    $concealedRefs = @(Get-ConcealedFieldRefs -Fields $full.fields)
    $serviceHints = @(Get-ServiceHints -Title $full.title -Username $usernameField.value -UrlBlob $urlBlob)

    $managedHintMatch = @($serviceHints | Where-Object { $_ -in $managedServices })

    $modeMatch = switch ($Mode) {
        "api-surface" {
            ($category -eq "API_CREDENTIAL") -or ($category -eq "SSH_KEY") -or
            (($category -in @("LOGIN", "PASSWORD")) -and (($managedHintMatch | Where-Object { $_ -in @("openrouter","anthropic","claude","openai","vertex","github","linear","what3words","mistral","huggingface","xai","grok") }).Count -gt 0))
        }
        "account-surface" {
            ($category -in @("LOGIN", "PASSWORD")) -and ($managedHintMatch.Count -gt 0)
        }
        default {
            ($category -eq "API_CREDENTIAL") -or ($category -eq "SSH_KEY") -or ($managedHintMatch.Count -gt 0)
        }
    }

    $isInteresting = $IncludeAllItems.IsPresent -or $modeMatch

    if (-not $isInteresting) {
        continue
    }

    $row = [pscustomobject]@{
        id             = $full.id
        vault          = $full.vault.name
        title          = $full.title
        category       = $full.category
        username       = [string]$usernameField.value
        service_hints  = $managedHintMatch
        concealed_refs = $concealedRefs
        canonical_title = ""
        action         = ""
    }
    $row.canonical_title = [string](Get-CanonicalTitle -Row $row)
    $row.action = Get-CleanupRecommendation -Row $row
    $detailRows.Add($row)
}

$duplicateGroups = $detailRows |
    Group-Object { "{0}|{1}|{2}|{3}" -f $_.vault, $_.title, $_.username, ($_.service_hints -join ",") } |
    Where-Object { $_.Count -gt 1 } |
    ForEach-Object {
        [pscustomobject]@{
            key   = $_.Name
            count = $_.Count
            ids   = $_.Group.id
        }
    }

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$modeSlug = $Mode -replace '[^a-zA-Z0-9_-]', '-'
$jsonPath = Join-Path $OutDir "credential-sweep_${modeSlug}_$stamp.json"
$mdPath = Join-Path $OutDir "credential-sweep_${modeSlug}_$stamp.md"
$latestJson = Join-Path $OutDir "credential-sweep_${modeSlug}_latest.json"
$latestMd = Join-Path $OutDir "credential-sweep_${modeSlug}_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    items        = $detailRows
    duplicates   = $duplicateGroups
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $jsonPath
$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $latestJson
New-MarkdownReport -Path $mdPath -Rows $detailRows -Duplicates $duplicateGroups
New-MarkdownReport -Path $latestMd -Rows $detailRows -Duplicates $duplicateGroups

Write-Output "Wrote:"
Write-Output "  $jsonPath"
Write-Output "  $mdPath"
Write-Output "  $latestJson"
Write-Output "  $latestMd"
