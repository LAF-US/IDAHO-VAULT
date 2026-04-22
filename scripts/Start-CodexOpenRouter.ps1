param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$script = Join-Path $PSScriptRoot "sta***REMOVED***codex_openrouter.py"
python $script @Args
exit $LASTEXITCODE
