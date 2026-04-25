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

function Get-EnvFilePath {
    param([string]$VaultRoot)
    return Join-Path $VaultRoot ".op" "openrouter.env"
}

function Get-ResolverScript {
    param([string]$VaultRoot)
    return Join-Path $VaultRoot "!" "resolve-openrouter-secret.ps1"
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

function Load-EnvFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$EnvFilePath
    )
    if (-not (Test-Path -LiteralPath $EnvFilePath)) {
        Write-Verbose "Env file not found: $EnvFilePath"
        return @{}
    }
    $env = @{}
    Get-Content -LiteralPath $EnvFilePath | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $env[$matches[1].Trim()] = $matches[2].Trim()
        }
    }
    return $env
}

function Get-RepoEnvVars {
    param([string]$VaultRoot)
    $envFile = Get-EnvFilePath $VaultRoot
    return Load-EnvFile $envFile
}

function Invoke-WithOpOrEnvFallback {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$OpBlock,

        [Parameter(Mandatory = $true)]
        [scriptblock]$EnvFallback,

        [Parameter(Mandatory = $true)]
        [string]$VaultRoot
    )
    if (Assert-OpAvailable) {
        return & $OpBlock
    }
    $envVars = Get-RepoEnvVars $VaultRoot
    if ($envVars.Count -eq 0) {
        Write-Warning "No fallback environment available. Some features may not work."
    }
    return & $EnvFallback $envVars
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
    'Get-EnvFilePath',
    'Get-ResolverScript',
    'Test-OpAvailable',
    'Assert-OpAvailable',
    'Load-EnvFile',
    'Get-RepoEnvVars',
    'Invoke-WithOpOrEnvFallback',
    'Get-PlatformInfo',
    'Test-IsCrossPlatformSafe',
    'Normalize-PathForPlatform'
)