param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$helper = Join-Path $PSScriptRoot "Use-VaultAgentEnv.ps1"
& $helper -Agent "gemini" -IsolateHome -Command @(@("gemini") + $Args)
exit $LASTEXITCODE
