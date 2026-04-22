param(
    [string]$Vault = "vault-operations",
    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

if (-not $OutFile) {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $OutFile = Join-Path $repoRoot ".op\openrouter.env"
}

if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
    Write-Error "1Password CLI 'op' is not installed or not on PATH."
}

$null = & op whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration first."
}

$candidates = @(
    "op://Personal/API Credentials/credential",
    "op://Personal/OpenRouter/password",
    "op://$Vault/openrouter-api-key/credential",
    "op://$Vault/openrouter-api-key/password",
    "op://$Vault/openrouter/credential",
    "op://$Vault/openrouter/password",
    "op://$Vault/openrouter-api/credential",
    "op://$Vault/openrouter-api/password",
    "op://$Vault/open-router-api-key/credential",
    "op://$Vault/open-router-api-key/password"
)

$resolvedRef = $null

foreach ($candidate in $candidates) {
    $secretRef = $candidate
    & op read $secretRef 1>$null 2>$null
    if ($LASTEXITCODE -eq 0) {
        $resolvedRef = $secretRef
        break
    }
}

if (-not $resolvedRef) {
    Write-Error "Could not resolve any known OpenRouter secret reference in vault '$Vault'."
}

$content = @(
    "OPENROUTER_API_KEY=$resolvedRef"
    "OPENAI_API_KEY=$resolvedRef"
    "OPENAI_BASE_URL=https://openrouter.ai/api/v1"
    "OPENAI_MODEL=openrouter/auto"
) -join "`r`n"

Set-Content -Path $OutFile -Value $content -NoNewline
Write-Output "Wrote $OutFile using $resolvedRef"
