param(
    [string]$SourceDir = "$env:USERPROFILE\Downloads\Phone Link",
    [string]$VaultDir = "C:\Users\loganf\Documents\IDAHO-VAULT",
    [string]$TargetSubdir = "INBOX\PHONE-LINK"
)

$ErrorActionPreference = 'Stop'
$TargetDir = Join-Path $VaultDir $TargetSubdir
$LogPath = Join-Path $TargetDir '_phone-link-sweep.log'
$ignoreNames = @('desktop.ini','Thumbs.db','phone-link-auto-sweep.ps1','START-PHONE-LINK-SWEEP.cmd','_phone-link-sweep.log')

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
    if ($ignoreNames -contains $name) { return }
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

while ($true) { Wait-Event -Timeout 5 | Out-Null }
