param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$helper = Join-Path $PSScriptRoot "Use-VaultAgentEnv.ps1"
& $helper -Agent "claude" -Command @(@("claude") + $Args)
exit $LASTEXITCODE
