param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$helper = Join-Path $PSScriptRoot "Use-VaultAgentEnv.ps1"
& $helper -Agent "codex" -Command @(@("codex") + $Args)
exit $LASTEXITCODE
