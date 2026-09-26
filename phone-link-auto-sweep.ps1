param(
    [string]$SourceDir,
    [string]$VaultDir,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir '.github\scripts\phone_link_auto_sweep.py'

if (-not (Test-Path -LiteralPath $pythonScript)) {
    throw "Missing Phone Link autosweep script: $pythonScript"
}

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw 'Python was not found on PATH.'
}

# Translate the legacy -SourceDir/-VaultDir contract to the Python watcher's
# --source/--vault-root options before appending any remaining arguments.
$pythonArgs = @()
if ($SourceDir) { $pythonArgs += @('--source', $SourceDir) }
if ($VaultDir) { $pythonArgs += @('--vault-root', $VaultDir) }
$pythonArgs += $RemainingArgs

& $python.Path $pythonScript @pythonArgs
exit $LASTEXITCODE
