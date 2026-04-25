param(
    [string]$Vault = "vault-operations",
    [string]$OutFile = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent $scriptRoot
$commonModule = Join-Path (Split-Path -Parent $scriptRoot) "scripts" "vault-common.ps1"

if (Test-Path $commonModule) {
    . $commonModule
}

if (-not $OutFile) {
    $OutFile = Join-Path $repoRoot ".op" "openrouter.env"
}

$existingEnv = Load-EnvFile $OutFile
if ($existingEnv.ContainsKey("OPENROUTER_API_KEY") -and $existingEnv["OPENROUTER_API_KEY"].StartsWith("sk-")) {
    Write-Output "Env file already exists with valid key. Use -Force to regenerate."
    exit 0
}

if (-not (Assert-OpAvailable)) {
    Write-Warning "1Password CLI not available. Checking for existing env file..."
    if ($existingEnv.ContainsKey("OPENROUTER_API_KEY")) {
        Write-Output "Using existing key from $OutFile"
        exit 0
    }
    Write-Error "No OpenRouter key found. Please either: 1) Sign in to 1Password CLI, or 2) Create .op/openrouter.env manually."
}

$opWhoami = op whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "1Password CLI not signed in. Run 'op signin' or unlock desktop integration."
}

$candidates = @(
    "op://Vault/OpenRouter API Key/credential"
    "op://Vault/openrouter-api-key/credential"
    "op://$Vault/openrouter-api-key/credential"
    "op://$Vault/openrouter/credential"
    "op://Personal/OpenRouter/credential"
    "op://Personal/API Credentials/credential"
)

$resolvedRef = $null

foreach ($candidate in $candidates) {
    & op read $candidate 1>$null 2>$null
    if ($LASTEXITCODE -eq 0) {
        $resolvedRef = $candidate
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
    "ANTHROPIC_AUTH_TOKEN=$resolvedRef"
    "ANTHROPIC_BASE_URL=https://openrouter.ai/api"
    "ANTHROPIC_API_KEY="
) -join "`r`n"

$OutFileDir = Split-Path -Parent $OutFile
if (-not (Test-Path $OutFileDir)) {
    New-Item -ItemType Directory -Path $OutFileDir -Force | Out-Null
}

Set-Content -Path $OutFile -Value $content -NoNewline
Write-Output "Wrote $OutFile using $resolvedRef"