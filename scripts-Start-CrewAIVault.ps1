param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$helper = Join-Path $PSScriptRoot "Use-VaultAgentEnv.ps1"

if (-not $Args -or $Args.Count -eq 0) {
    $Args = @("run")
}

& $helper -Agent "crewai" -IsolateHome -Command @(@("uv", "run", "crewai") + $Args)
exit $LASTEXITCODE
