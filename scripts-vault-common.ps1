#
# IDAHO-VAULT Common PowerShell Utilities
# Cross-platform helper functions for vault scripts
#

function Test-CommandAvailable {
    param([string]$Command)
    return $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Assert-CommandAvailable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [string]$Feature = $Command
    )
    if (-not (Test-CommandAvailable $Command)) {
        Write-Warning "$Feature not available. Install $Command or add to PATH."
        return $false
    }
    return $true
}

function Get-VaultRoot {
    param([string]$ScriptPath = $PSCommandPath)
    $scriptDir = Split-Path -Parent $ScriptPath
    $vaultRoot = Split-Path -Parent $scriptDir
    return $vaultRoot
}

function Test-OpAvailable {
    if (-not (Test-CommandAvailable "op")) {
        return $false
    }
    $result = op whoami 2>$null
    return $LASTEXITCODE -eq 0
}

function Assert-OpAvailable {
    if (-not (Test-CommandAvailable "op")) {
        Write-Warning "1Password CLI 'op' not found. Some features will be unavailable."
        return $false
    }
    if (-not (Test-OpAvailable)) {
        Write-Warning "1Password CLI not signed in. Run 'op signin' or unlock desktop integration."
        return $false
    }
    return $true
}

function Get-PlatformInfo {
    if ($IsMacOS) { return "macos" }
    if ($IsLinux) { return "linux" }
    if ($IsWindows) { return "windows" }
    return "unknown"
}

function Test-IsCrossPlatformSafe {
    param([string]$Path)
    return $Path -notmatch '^[A-Z]:|\\' -and $Path -notmatch '[A-Z]:|\\$'
}

function Normalize-PathForPlatform {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [switch]$ForceUnix
    )
    if ($ForceUnix -or $IsLinux -or $IsMacOS) {
        return $Path -replace '\\', '/'
    }
    return $Path
}

Export-ModuleMember -Function @(
    'Test-CommandAvailable',
    'Assert-CommandAvailable',
    'Get-VaultRoot',
    'Test-OpAvailable',
    'Assert-OpAvailable',
    'Get-PlatformInfo',
    'Test-IsCrossPlatformSafe',
    'Normalize-PathForPlatform'
)