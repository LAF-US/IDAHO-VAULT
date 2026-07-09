param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir '.github\scripts\phone_link_auto_sweep.py'

if (-not (Test-Path -LiteralPath $pythonScript)) {
    throw "Missing Phone Link sweeper: $pythonScript"
}

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw 'Python was not found on PATH.'
}

& $python.Source $pythonScript @Args
exit $LASTEXITCODE
