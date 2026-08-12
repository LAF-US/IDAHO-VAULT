param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$script = Join-Path $PSScriptRoot "start_codex_openrouter.py"
python $script @Args
exit $LASTEXITCODE
