param(
    [string]$SourceDir = "$env:USERPROFILE\Downloads\Phone Link",
    [string]$VaultDir = "C:\Users\loganf\Documents\IDAHO-VAULT",
    [string]$PythonScript = ".github/scripts/phone_link_intake.py"
)

$ErrorActionPreference = 'Stop'
$TargetDir = Join-Path $VaultDir "!\INBOX"
$LogPath = Join-Path $TargetDir "_phone-link-watcher.log"
$PidPath = Join-Path $TargetDir "_phone-link-watcher.pid"

$mutexName = 'Global\IDAHO_VAULT_PHONE_LINK_SWEEP'
$createdNew = $false
$mutex = New-Object System.Threading.Mutex($true, $mutexName, [ref]$createdNew)
if (-not $createdNew) {
    if (-not (Test-Path -Path $TargetDir)) { New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null }
    $line = "$(Get-Date -Format s)  Phone Link watcher is already running. Exiting duplicate launch."
    Write-Output $line
    Add-Content -Path $LogPath -Value $line
    exit 0
}

# Ensure directories exist
if (-not (Test-Path -Path $SourceDir)) { New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null }
if (-not (Test-Path -Path $TargetDir)) { New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null }

# Persist the watcher PID so stop/restart can work without CIM access.
Set-Content -Path $PidPath -Value $PID -Encoding ascii

function Write-Log([string]$msg) {
    $line = "$(Get-Date -Format s)  $msg"
    Write-Output $line
    Add-Content -Path $LogPath -Value $line
}

function Invoke-Intake {
    Write-Log "TRIGGER: Launching Python intake authority..."
    $fullScriptPath = Join-Path $VaultDir $PythonScript
    try {
        # Run the Python script with --live-write
        # Note: We can pipe output to the log or just run it. 
        # Using --live-write is the mandatory bypass for the guardrails.
        & python $fullScriptPath --live-write | ForEach-Object { Write-Log "  PYTHON: $_" }
    } catch {
        Write-Log "ERROR: Python intake failed: $_"
    }
}

# Initial sweep
Invoke-Intake

Write-Log "Watcher active. Monitoring '$SourceDir'..."

$fsw = New-Object System.IO.FileSystemWatcher $SourceDir
$fsw.IncludeSubdirectories = $false
$fsw.EnableRaisingEvents = $true

# Debounce timer to avoid multiple rapid calls
$timer = New-Object System.Timers.Timer
$timer.Interval = 2000 # 2 seconds
$timer.AutoReset = $false

$action = {
    $timer.Stop()
    $timer.Start()
}

$onTimerElapsed = {
    Invoke-Intake
}

Register-ObjectEvent -InputObject $fsw -EventName Created -Action $action | Out-Null
Register-ObjectEvent -InputObject $fsw -EventName Renamed -Action $action | Out-Null
Register-ObjectEvent -InputObject $timer -EventName Elapsed -Action $onTimerElapsed | Out-Null

$createdSub = Get-EventSubscriber | Where-Object { $_.SourceObject -eq $fsw -and $_.EventName -eq 'Created' } | Select-Object -First 1
$renamedSub = Get-EventSubscriber | Where-Object { $_.SourceObject -eq $fsw -and $_.EventName -eq 'Renamed' } | Select-Object -First 1
$timerSub = Get-EventSubscriber | Where-Object { $_.SourceObject -eq $timer -and $_.EventName -eq 'Elapsed' } | Select-Object -First 1

try {
    while ($true) { Wait-Event -Timeout 5 | Out-Null }
}
finally {
    if ($createdSub) { Unregister-Event -SubscriptionId $createdSub.SubscriptionId -ErrorAction SilentlyContinue }
    if ($renamedSub) { Unregister-Event -SubscriptionId $renamedSub.SubscriptionId -ErrorAction SilentlyContinue }
    if ($timerSub) { Unregister-Event -SubscriptionId $timerSub.SubscriptionId -ErrorAction SilentlyContinue }
    if ($fsw) { $fsw.Dispose() }
    if ($timer) { $timer.Dispose() }
    if (Test-Path -Path $PidPath) { Remove-Item -Path $PidPath -Force -ErrorAction SilentlyContinue }
    if ($mutex) {
        try { $mutex.ReleaseMutex() | Out-Null } catch {}
        $mutex.Dispose()
    }
}
