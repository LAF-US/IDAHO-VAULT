param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude")]
    [string]$Agent,

    [Parameter(Mandatory = $true)]
    [string]$CliName,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vaultRoot = Split-Path -Parent $scriptDir
$envFile = Join-Path $vaultRoot ".op\openrouter.env"
$resolver = Join-Path $vaultRoot "!\resolve-openrouter-secret.ps1"
$runtimeHelper = Join-Path $scriptDir "Use-VaultAgentEnv.ps1"

if (-not (Get-Command op -ErrorAction SilentlyContinue)) {
    Write-Error "1Password CLI 'op' is not installed or not on PATH."
}

$requiredKeys = switch ($Agent) {
    "codex" { @("OPENAI_API_KEY", "OPENAI_BASE_URL") }
    "claude" { @("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY") }
}

$needsRefresh = -not (Test-Path -LiteralPath $envFile)
if (-not $needsRefresh) {
    $content = Get-Content -LiteralPath $envFile -Raw
    foreach ($requiredKey in $requiredKeys) {
        if ($content -notmatch "(?m)^$([regex]::Escape($requiredKey))=") {
            $needsRefresh = $true
            break
        }
    }
}

if ($needsRefresh) {
    & $resolver | Out-Null
}

$null = & op whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration first."
}

$envArg = "--env-file=$envFile"
$command = @("op", "run", $envArg, "--", $CliName)
if ($Args) {
    $command += $Args
}

& $runtimeHelper -Agent $Agent -Command $command
exit $LASTEXITCODE
