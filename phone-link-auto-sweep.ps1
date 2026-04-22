param(
    [string]$SourceDir = "$env:USERPROFILE\Downloads\Phone Link",
    [string]$VaultDir = "C:\Users\loganf\Documents\IDAHO-VAULT"
)

$ErrorActionPreference = 'Stop'
$TargetDir = $VaultDir
$LogPath = Join-Path $VaultDir '!\INBOX\_phone-link-watcher.log'

$mutexName = 'Global\IDAHO_VAULT_PHONE_LINK_SWEEP'
$createdNew = $false
$mutex = $null
try {
    $mutex = New-Object System.Threading.Mutex($true, $mutexName, [ref]$createdNew)
} catch [System.Threading.AbandonedMutexException] {
    # Previous process crashed without releasing. Ownership is granted — continue.
    $mutex = $_.Exception.Mutex
    $createdNew = $true
    Write-Warning 'Phone Link sweep: orphaned mutex reclaimed from crashed process.'
}
if (-not $createdNew) {
    Write-Output 'Phone Link autosweep is already running. Exiting duplicate launch.'
    exit 0
}

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null

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

function Get-ShortFileHash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.Substring(0, 16).ToLowerInvariant()
}

function Resolve-Destination([string]$Path) {
    $name = [System.IO.Path]::GetFileName($Path)
    $dest = Join-Path $TargetDir $name
    if (-not (Test-Path -LiteralPath $dest)) {
        return @{
            Path = $dest
            Disposition = 'direct'
        }
    }

    $incomingHash = Get-ShortFileHash -Path $Path
    $existingHash = Get-ShortFileHash -Path $dest
    if ($incomingHash -eq $existingHash) {
        return @{
            Path = $null
            Disposition = 'duplicate'
        }
    }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($name)
    $ext = [System.IO.Path]::GetExtension($name)
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $attempt = 0
    while ($true) {
        $suffix = if ($attempt -eq 0) { "$stamp-$incomingHash" } else { "$stamp-$incomingHash-$attempt" }
        $candidate = Join-Path $TargetDir ("$base-$suffix$ext")
        if (-not (Test-Path -LiteralPath $candidate)) {
            return @{
                Path = $candidate
                Disposition = 'collision'
            }
        }

        if ((Get-ShortFileHash -Path $candidate) -eq $incomingHash) {
            return @{
                Path = $null
                Disposition = 'duplicate'
            }
        }

        $attempt++
    }
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

    $resolution = Resolve-Destination -Path $Path
    if ($null -eq $resolution.Path) {
        Write-Log "SKIP (duplicate): $name"
        return
    }

    $dest = $resolution.Path
    while ($true) {
        try {
            Move-Item -LiteralPath $Path -Destination $dest -ErrorAction Stop
            Write-Log "MOVED: $name -> $dest"
            return
        }
        catch {
            if (-not (Test-Path -LiteralPath $Path)) { return }
            if ($_.Exception -isnot [System.IO.IOException]) { throw }

            $resolution = Resolve-Destination -Path $Path
            if ($null -eq $resolution.Path) {
                Write-Log "SKIP (duplicate): $name"
                return
            }

            $dest = $resolution.Path
        }
    }
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
