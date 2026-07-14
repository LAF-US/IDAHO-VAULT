param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Ensure-OpSession {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
        throw "1Password CLI 'op' is not installed or not on PATH."
    }

    & op signin | Out-Null
}

function Get-CanonicalApiTitle {
    param(
        [string]$Username
    )

    switch -Regex ($Username) {
        '^OpenRouter$' { return 'OpenRouter API Key' }
        '^Claude anthro-key$' { return 'Anthropic API Key' }
        '^LINEAR_API_KEY$' { return 'Linear API Key' }
        '^GOOGLE_VERTEX_AI_API_KEY$' { return 'Google Vertex AI API Key' }
        '^QODO_API_KEY$' { return 'Qodo API Key' }
        '^Google Antigravity to GitHub MCP$' { return 'Google Antigravity to GitHub MCP Credential' }
        default { return $null }
    }
}

Ensure-OpSession

$items = op item list --format json | ConvertFrom-Json
$targets = New-Object System.Collections.Generic.List[object]

foreach ($item in $items) {
    if ($item.category -ne 'API_CREDENTIAL') {
        continue
    }

    if ($item.title -ne 'API Credentials') {
        continue
    }

    $full = op item get $item.id --format json | ConvertFrom-Json
    $usernameField = $full.fields | Where-Object { $_.id -eq 'username' } | Select-Object -First 1
    $username = [string]$usernameField.value
    $canonical = Get-CanonicalApiTitle -Username $username

    if (-not $canonical) {
        continue
    }

    if ($full.title -eq $canonical) {
        continue
    }

    $targets.Add([pscustomobject]@{
        id        = $full.id
        vault     = $full.vault.name
        old_title = $full.title
        username  = $username
        new_title = $canonical
    })
}

if ($targets.Count -eq 0) {
    Write-Output "No managed API credential renames required."
    exit 0
}

foreach ($target in $targets) {
    if ($DryRun) {
        Write-Output "[dry-run] $($target.vault): $($target.old_title) [$($target.username)] -> $($target.new_title)"
        continue
    }

    & op item edit $target.id --vault $target.vault --title $target.new_title | Out-Null
    Write-Output "[renamed] $($target.vault): $($target.old_title) [$($target.username)] -> $($target.new_title)"
}
