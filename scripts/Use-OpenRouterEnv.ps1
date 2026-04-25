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
$commonModule = Join-Path $scriptDir "vault-common.ps1"

if (Test-Path $commonModule) {
    . $commonModule
}

$envFile = Get-EnvFilePath $vaultRoot
$resolver = Get-ResolverScript $vaultRoot
$runtimeHelper = Join-Path $scriptDir "Use-VaultAgentEnv.ps1"

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

$useOp = Assert-OpAvailable

if ($needsRefresh -and $useOp) {
    try {
        & $resolver | Out-Null
    }
    catch {
        Write-Warning "Failed to refresh env file from 1Password: $_"
    }
}

if ($useOp) {
    $opWhoami = op whoami 2>$null
    if ($LASTEXITCODE -eq 0) {
        $envArg = "--env-file=$envFile"
        $command = @("op", "run", $envArg, "--", $CliName)
        if ($Args) {
            $command += $Args
        }
        & $runtimeHelper -Agent $Agent -Command $command
        exit $LASTEXITCODE
    }
}

Write-Warning "1Password CLI not available. Attempting direct env file usage..."
if (-not (Test-Path -LiteralPath $envFile)) {
    Write-Error "Env file not found: $envFile. Run !/resolve-openrouter-secret.ps1 first."
}

$envVars = Load-EnvFile $envFile
foreach ($key in $envVars.Keys) {
    Set-Item -Path "env:$key" -Value $envVars[$key] -ErrorAction SilentlyContinue
}

& $runtimeHelper -Agent $Agent -Command @($CliName) -Args $Args
exit $LASTEXITCODE