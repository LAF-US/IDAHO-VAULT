param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$script = Join-Path $PSScriptRoot "sta***REMOVED***claude_openrouter.py"
python $script @Args
exit $LASTEXITCODE
