param(
    [string]$SourceDir = "$env:USERPROFILE\Downloads\Phone Link",
    [string]$VaultDir = "C:\Users\loganf\Documents\IDAHO-VAULT",
    [string]$TargetSubdir = "INBOX\PHONE-LINK"
)

$ErrorActionPreference = 'Stop'
$TargetDir = Join-Path $VaultDir $TargetSubdir
$LogPath = Join-Path $TargetDir '_phone-link-sweep.log'

$mutexName = 'Global\IDAHO_VAULT_PHONE_LINK_SWEEP'
$createdNew = $false
$mutex = New-Object System.Threading.Mutex($true, $mutexName, [ref]$createdNew)
if (-not $createdNew) {
    Write-Output 'Phone Link autosweep is already running. Exiting duplicate launch.'
    exit 0
}

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

function Write-Log([string]$msg) {
    $line = "$(Get-Date -Format s)  $msg"
    Add-Content -Path $LogPath -Value $line
}

function Test-Unlocked([string]$Path) {
    for ($i = 0; $i -lt 20; $i++) {
        try {
            $stream = [System.IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
            $stream.Close()
            return $true
        } catch {
            Start-Sleep -Milliseconds 300
        }
    }
    return $false
}

function Move-One([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return }
    $name = [System.IO.Path]::GetFileName($Path)
    if ($name -in @('desktop.ini','Thumbs.db')) { return }
    if ($name -like '~$*' -or $name -like '*.tmp' -or $name -like '*.crdownload') { return }

    if (-not (Test-Unlocked -Path $Path)) {
        Write-Log "SKIP (locked): $name"
        return
    }

    $dest = Join-Path $TargetDir $name
    if (Test-Path -LiteralPath $dest) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($name)
        $ext = [System.IO.Path]::GetExtension($name)
        $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
        $dest = Join-Path $TargetDir ("$base-$stamp$ext")
    }

    Move-Item -LiteralPath $Path -Destination $dest -Force
    Write-Log "MOVED: $name -> $dest"
}

Get-ChildItem -LiteralPath $SourceDir -File -Force | ForEach-Object { Move-One -Path $_.FullName }
Write-Log "Watcher active. Source='$SourceDir' Target='$TargetDir'"

$fsw = New-Object System.IO.FileSystemWatcher $SourceDir
$fsw.IncludeSubdirectories = $false
$fsw.EnableRaisingEvents = $true

Register-ObjectEvent -InputObject $fsw -EventName Created -Action {
    Move-One -Path $Event.SourceEventArgs.FullPath
} | Out-Null

Register-ObjectEvent -InputObject $fsw -EventName Renamed -Action {
    Move-One -Path $Event.SourceEventArgs.FullPath
} | Out-Null

$createdSub = Get-EventSubscriber | Where-Object { $_.SourceObject -eq $fsw -and $_.EventName -eq 'Created' } | Select-Object -First 1
$renamedSub = Get-EventSubscriber | Where-Object { $_.SourceObject -eq $fsw -and $_.EventName -eq 'Renamed' } | Select-Object -First 1

try {
    while ($true) { Wait-Event -Timeout 5 | Out-Null }
}
finally {
    if ($createdSub) { Unregister-Event -SubscriptionId $createdSub.SubscriptionId -ErrorAction SilentlyContinue }
    if ($renamedSub) { Unregister-Event -SubscriptionId $renamedSub.SubscriptionId -ErrorAction SilentlyContinue }
    if ($fsw) { $fsw.Dispose() }
    if ($mutex) {
        try { $mutex.ReleaseMutex() | Out-Null } catch {}
        $mutex.Dispose()
    }
}
