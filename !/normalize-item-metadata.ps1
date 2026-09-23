param(
    [string]$OutDir = "",
    [switch]$ApplyTitles,
    [switch]$ApplyTags,
    [string[]]$Vaults = @(),
    [int]$MaxEdits = 100,
    [switch]$ForceLargeBatch,
    [string]$ConfirmToken = ""
)

$ErrorActionPreference = "Stop"

function Ensure-OpSession {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
        throw "1Password CLI 'op' is not installed or not on PATH."
    }

    & op signin | Out-Null
}

function Assert-ApplySafety {
    param(
        [int]$TargetCount,
        [int]$MaxEdits,
        [switch]$ForceLargeBatch,
        [string]$ConfirmToken
    )

    if ($ConfirmToken -ne "EDIT_ITEMS") {
        throw "Refusing to edit items without -ConfirmToken EDIT_ITEMS."
    }

    if ($TargetCount -gt $MaxEdits -and -not $ForceLargeBatch.IsPresent) {
        throw "Refusing to edit $TargetCount items because MaxEdits is $MaxEdits. Re-run with a higher -MaxEdits or -ForceLargeBatch."
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

function Get-DisplayHost {
    param([string]$PrimaryHost)
    if (-not $PrimaryHost) { return "" }
    return ($PrimaryHost -replace '^www\.', '')
}

function Get-ImportArtifactTags {
    param([string[]]$Tags)

    $artifactTags = New-Object System.Collections.Generic.List[string]
    foreach ($tag in @($Tags)) {
        if (-not $tag) { continue }
        if ($tag -match '^(Imported .+|CSV Import .+|Starter Kit)$') {
            $artifactTags.Add($tag)
        }
    }

    return @($artifactTags | Select-Object -Unique)
}

function Get-ServiceHints {
    param(
        [string]$Title,
        [string]$Username,
        [string]$PrimaryHost
    )

    $text = (($Title, $Username, $PrimaryHost) -join " ").ToLowerInvariant()
    $hints = New-Object System.Collections.Generic.List[string]

    $patterns = @(
        "openrouter",
        "anthropic",
        "claude",
        "openai",
        "github",
        "gitlab",
        "linear",
        "vertex",
        "google",
        "slack",
        "figma",
        "mistral",
        "huggingface",
        "qodo",
        "what3words",
        "stripe",
        "coinbase",
        "discord",
        "idahoptv"
    )

    foreach ($pattern in $patterns) {
        if ($text -match [regex]::Escape($pattern)) {
            $hints.Add($pattern)
        }
    }

    return @($hints | Select-Object -Unique)
}

function Get-CanonicalApiTitle {
    param(
        [string]$Title,
        [string]$Username,
        [string[]]$Hints
    )

    $titleNorm = Normalize-Value $Title
    $userNorm = Normalize-Value $Username

    if ($titleNorm -eq "openrouter api key" -or $userNorm -eq "openrouter" -or $Hints -contains "openrouter") { return "OpenRouter API Key" }
    if ($titleNorm -eq "anthropic api key" -or $userNorm -eq "claude anthro-key" -or $Hints -contains "anthropic" -or $Hints -contains "claude") { return "Anthropic API Key" }
    if ($titleNorm -eq "linear api key" -or $userNorm -eq "linear_api_key" -or $Hints -contains "linear") { return "Linear API Key" }
    if ($titleNorm -eq "google vertex ai api key" -or $userNorm -eq "google_vertex_ai_api_key" -or (($Hints -contains "google") -and ($Hints -contains "vertex"))) { return "Google Vertex AI API Key" }
    if ($titleNorm -eq "qodo api key" -or $userNorm -eq "qodo_api_key" -or $Hints -contains "qodo") { return "Qodo API Key" }
    if ($titleNorm -eq "what3words api key" -or $Hints -contains "what3words") { return "what3words API Key" }
    if ($titleNorm -eq "mistral api key" -or $Hints -contains "mistral") { return "Mistral API Key" }
    if ($titleNorm -eq "google antigravity to github mcp credential") { return "Google Antigravity to GitHub MCP Credential" }

    return $null
}

function Get-RecommendedTitle {
    param($ItemMeta)

    $currentTitle = [string]$ItemMeta.title
    $username = [string]$ItemMeta.additional_information
    $primaryHost = Get-PrimaryHost -ItemMeta $ItemMeta
    $displayHost = Get-DisplayHost -PrimaryHost $primaryHost
    $hints = @(Get-ServiceHints -Title $currentTitle -Username $username -PrimaryHost $primaryHost)

    if ($ItemMeta.category -eq "API_CREDENTIAL") {
        $canonical = Get-CanonicalApiTitle -Title $currentTitle -Username $username -Hints $hints
        if ($canonical -and $canonical -ne $currentTitle) {
            return $canonical
        }
    }

    $titleNorm = Normalize-Value $currentTitle
    if ($displayHost) {
        if ($titleNorm -eq "login") {
            return $displayHost
        }

        if ($titleNorm -match '^https?://') {
            return $displayHost
        }

        if ($titleNorm -eq (Normalize-Value $primaryHost) -and $primaryHost -ne $displayHost) {
            return $displayHost
        }
    }

    return $null
}

function Get-SuggestedTags {
    param($ItemMeta)

    $tags = New-Object System.Collections.Generic.List[string]
    $username = [string]$ItemMeta.additional_information
    $primaryHost = Get-PrimaryHost -ItemMeta $ItemMeta
    $hints = @(Get-ServiceHints -Title $ItemMeta.title -Username $username -PrimaryHost $primaryHost)

    switch ([string]$ItemMeta.vault.name) {
        "Work" { $tags.Add("work") }
        "Personal" { $tags.Add("personal") }
        "Private" { $tags.Add("private") }
        "Wallet" { $tags.Add("wallet") }
        "Vault" { $tags.Add("managed") }
    }

    switch ([string]$ItemMeta.category) {
        "API_CREDENTIAL" { $tags.Add("api") }
        "SSH_KEY" { $tags.Add("ssh") }
        "LOGIN" { $tags.Add("login") }
        "PASSWORD" { $tags.Add("password") }
    }

    foreach ($hint in $hints) {
        $tags.Add($hint)
    }

    if ((Normalize-Value (($ItemMeta.title, $username, $primaryHost) -join " ")) -match '@idahoptv\.org\b|\bidahoptv\b') {
        $tags.Add("idahoptv")
    }

    if ($primaryHost -match '(creditkarma|venmo|pay\.gov|stlukesbillpay|upstart|personalcapital|freetaxusa|coinbase|stripe|moneylion|moneykey|creditfresh|usbank|bankofamerica|chime|gobank|intuit|turbotax|potlatchno1federalcreditunion)') {
        $tags.Add("financial")
    }

    return @($tags | Where-Object { $_ } | Select-Object -Unique | Sort-Object)
}

function New-MarkdownReport {
    param(
        [string]$Path,
        [array]$Rows
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Item Metadata Normalization")
    $lines.Add("")
    $lines.Add("Generated: $(Get-Date -Format s)")
    $lines.Add("")
    $lines.Add("This report proposes conservative title cleanup and additive tag normalization.")
    $lines.Add("")
    $lines.Add("| Vault | Category | Current Title | Proposed Title | Current Tags | Drop Tags | Final Tags | Username | Host | Item ID |")
    $lines.Add("|---|---|---|---|---|---|---|---|---|---|")

    foreach ($row in $Rows) {
        $currentTags = ($row.current_tags -join ", ")
        $dropTags = ($row.drop_tags -join ", ")
        $finalTags = ($row.final_tags -join ", ")
        $lines.Add("| $($row.vault) | $($row.category) | $($row.current_title) | $($row.proposed_title) | $currentTags | $dropTags | $finalTags | $($row.username) | $($row.host) | $($row.id) |")
    }

    if ($Rows.Count -eq 0) {
        $lines.Add("| none | | | | | | | | | No normalization candidates detected. |")
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

foreach ($itemMeta in $items) {
    if ($Vaults.Count -gt 0 -and $itemMeta.vault.name -notin $Vaults) {
        continue
    }

    if ($itemMeta.category -notin @("LOGIN", "PASSWORD", "API_CREDENTIAL", "SSH_KEY")) {
        continue
    }

    $proposedTitle = Get-RecommendedTitle -ItemMeta $itemMeta
    $suggestedTags = @(Get-SuggestedTags -ItemMeta $itemMeta)
    $currentTags = @()
    if ($itemMeta.tags) {
        $currentTags = @($itemMeta.tags)
    }
    $dropTags = @(Get-ImportArtifactTags -Tags $currentTags)
    $retainedTags = @($currentTags | Where-Object { $_ -notin $dropTags })
    $finalTags = @($retainedTags + $suggestedTags | Where-Object { $_ } | Select-Object -Unique | Sort-Object)

    $titleNeedsChange = $proposedTitle -and ($proposedTitle -ne [string]$itemMeta.title)
    $tagsNeedChange = ($dropTags.Count -gt 0) -or ((Compare-Object -ReferenceObject $currentTags -DifferenceObject $finalTags).Count -gt 0)

    if (-not $titleNeedsChange -and -not $tagsNeedChange) {
        continue
    }

    $rows.Add([pscustomobject]@{
        id             = $itemMeta.id
        vault          = $itemMeta.vault.name
        category       = $itemMeta.category
        current_title  = [string]$itemMeta.title
        proposed_title = if ($proposedTitle) { $proposedTitle } else { "" }
        current_tags   = $currentTags
        drop_tags      = $dropTags
        final_tags     = $finalTags
        username       = [string]$itemMeta.additional_information
        host           = Get-DisplayHost -PrimaryHost (Get-PrimaryHost -ItemMeta $itemMeta)
    })
}

$ordered = $rows | Sort-Object -Property vault, category, current_title

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$jsonPath = Join-Path $OutDir "item-metadata-normalization_$stamp.json"
$mdPath = Join-Path $OutDir "item-metadata-normalization_$stamp.md"
$latestJson = Join-Path $OutDir "item-metadata-normalization_latest.json"
$latestMd = Join-Path $OutDir "item-metadata-normalization_latest.md"

$payload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    apply_titles = [bool]$ApplyTitles
    apply_tags   = [bool]$ApplyTags
    vault_scope  = $Vaults
    max_edits    = $MaxEdits
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

if (-not $ApplyTitles -and -not $ApplyTags) {
    Write-Output "Dry run only. No items edited."
    exit 0
}

Assert-ApplySafety -TargetCount $ordered.Count -MaxEdits $MaxEdits -ForceLargeBatch:$ForceLargeBatch -ConfirmToken $ConfirmToken

$applied = New-Object System.Collections.Generic.List[object]

foreach ($row in $ordered) {
    $editArgs = @($row.id, "--vault", $row.vault)

    if ($ApplyTitles -and $row.proposed_title) {
        $editArgs += @("--title", $row.proposed_title)
    }

    if ($ApplyTags) {
        $editArgs += @("--tags", ($row.final_tags -join ","))
    }

    if ($editArgs.Count -le 3) {
        continue
    }

    & op item edit @editArgs | Out-Null

    $applied.Add([pscustomobject]@{
        edited_at      = (Get-Date).ToString("s")
        id             = $row.id
        vault          = $row.vault
        category       = $row.category
        previous_title = $row.current_title
        new_title      = if ($ApplyTitles -and $row.proposed_title) { $row.proposed_title } else { $row.current_title }
        tags           = if ($ApplyTags) { $row.final_tags } else { $row.current_tags }
    })

    Write-Output "[edited] $($row.vault): $($row.current_title) [$($row.id)]"
}

$appliedJsonPath = Join-Path $OutDir "item-metadata-normalization-applied_$stamp.json"
$appliedMdPath = Join-Path $OutDir "item-metadata-normalization-applied_$stamp.md"
$appliedLatestJson = Join-Path $OutDir "item-metadata-normalization-applied_latest.json"
$appliedLatestMd = Join-Path $OutDir "item-metadata-normalization-applied_latest.md"

$appliedPayload = [pscustomobject]@{
    generated_at = (Get-Date).ToString("s")
    apply_titles = [bool]$ApplyTitles
    apply_tags   = [bool]$ApplyTags
    edited_items = $applied
}

$appliedPayload | ConvertTo-Json -Depth 8 | Set-Content -Path $appliedJsonPath
$appliedPayload | ConvertTo-Json -Depth 8 | Set-Content -Path $appliedLatestJson

$appliedLines = New-Object System.Collections.Generic.List[string]
$appliedLines.Add("# Item Metadata Normalization Applied")
$appliedLines.Add("")
$appliedLines.Add("Generated: $(Get-Date -Format s)")
$appliedLines.Add("")
$appliedLines.Add("| Vault | Category | Previous Title | New Title | Tags | Item ID |")
$appliedLines.Add("|---|---|---|---|---|---|")
foreach ($row in $applied) {
    $appliedLines.Add("| $($row.vault) | $($row.category) | $($row.previous_title) | $($row.new_title) | $($row.tags -join ", ") | $($row.id) |")
}
if ($applied.Count -eq 0) {
    $appliedLines.Add("| none | | | | | No items were edited. |")
}

Set-Content -Path $appliedMdPath -Value ($appliedLines -join "`r`n")
Set-Content -Path $appliedLatestMd -Value ($appliedLines -join "`r`n")

Write-Output "Applied report:"
Write-Output "  $appliedJsonPath"
Write-Output "  $appliedMdPath"
Write-Output "  $appliedLatestJson"
Write-Output "  $appliedLatestMd"
