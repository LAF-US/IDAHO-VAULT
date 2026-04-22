param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "gemini", "crewai", "antigravity")]
    [string]$Agent,

    [switch]$IsolateHome,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Command
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vaultRoot = Split-Path -Parent $scriptDir
$originalUserProfile = $env:USERPROFILE

function Ensure-Dir {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Set-EnvValue {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Value
    )

    $resolved = [System.IO.Path]::GetFullPath($Value)
    Ensure-Dir -Path $resolved
    [System.Environment]::SetEnvironmentVariable($Name, $resolved, "Process")
}

$sharedPaths = @{
    TMP                = Join-Path $vaultRoot ".tmp"
    TEMP               = Join-Path $vaultRoot ".tmp"
    TMPDIR             = Join-Path $vaultRoot ".tmp"
    UV_CACHE_DIR       = Join-Path $vaultRoot ".uv-cache"
    PIP_CACHE_DIR      = Join-Path $vaultRoot ".pip-cache"
    NPM_CONFIG_CACHE   = Join-Path $vaultRoot ".npm-cache"
    XDG_CACHE_HOME     = Join-Path $vaultRoot ".cache"
    XDG_STATE_HOME     = Join-Path $vaultRoot ".state"
    PYTHONPYCACHEPREFIX = Join-Path $vaultRoot ".pycache"
}

foreach ($entry in $sharedPaths.GetEnumerator()) {
    Set-EnvValue -Name $entry.Key -Value $entry.Value
}

$agentHomeRoot = Join-Path $vaultRoot ".agent-home"
Ensure-Dir -Path $agentHomeRoot

switch ($Agent) {
    "codex" {
        Set-EnvValue -Name "CODEX_HOME" -Value (Join-Path $agentHomeRoot "codex")
    }
    "claude" {
        $roaming = Join-Path $agentHomeRoot "claude\\AppData\\Roaming"
        $local = Join-Path $agentHomeRoot "claude\\AppData\\Local"
        Set-EnvValue -Name "APPDATA" -Value $roaming
        Set-EnvValue -Name "LOCALAPPDATA" -Value $local
    }
    "gemini" {
        $roaming = Join-Path $agentHomeRoot "gemini\\AppData\\Roaming"
        $local = Join-Path $agentHomeRoot "gemini\\AppData\\Local"
        Set-EnvValue -Name "APPDATA" -Value $roaming
        Set-EnvValue -Name "LOCALAPPDATA" -Value $local
        $IsolateHome = $true
    }
    "antigravity" {
        $roaming = Join-Path $agentHomeRoot "antigravity\\AppData\\Roaming"
        $local = Join-Path $agentHomeRoot "antigravity\\AppData\\Local"
        Set-EnvValue -Name "APPDATA" -Value $roaming
        Set-EnvValue -Name "LOCALAPPDATA" -Value $local
        $IsolateHome = $true
    }
    "crewai" {
        $roaming = Join-Path $agentHomeRoot "crewai\\AppData\\Roaming"
        $local = Join-Path $agentHomeRoot "crewai\\AppData\\Local"
        Set-EnvValue -Name "APPDATA" -Value $roaming
        Set-EnvValue -Name "LOCALAPPDATA" -Value $local
        $IsolateHome = $true
    }
}

if ($IsolateHome) {
    $homeRoot = Join-Path $agentHomeRoot $Agent
    Ensure-Dir -Path $homeRoot
    [System.Environment]::SetEnvironmentVariable("HOME", $homeRoot, "Process")
    [System.Environment]::SetEnvironmentVariable("USERPROFILE", $homeRoot, "Process")

    $drive = [System.IO.Path]::GetPathRoot($homeRoot).TrimEnd("\")
    $homePath = $homeRoot.Substring($drive.Length)
    [System.Environment]::SetEnvironmentVariable("HOMEDRIVE", $drive, "Process")
    [System.Environment]::SetEnvironmentVariable("HOMEPATH", $homePath, "Process")

    $userGitConfig = Join-Path $originalUserProfile ".gitconfig"
    if (Test-Path -LiteralPath $userGitConfig) {
        [System.Environment]::SetEnvironmentVariable("GIT_CONFIG_GLOBAL", $userGitConfig, "Process")
    }
}

if (-not $Command -or $Command.Count -eq 0) {
    Write-Host "Agent: $Agent"
    Write-Host "Vault root: $vaultRoot"
    Write-Host "TMP: $env:TMP"
    Write-Host "UV_CACHE_DIR: $env:UV_CACHE_DIR"
    Write-Host "PIP_CACHE_DIR: $env:PIP_CACHE_DIR"
    Write-Host "NPM_CONFIG_CACHE: $env:NPM_CONFIG_CACHE"
    if ($env:CODEX_HOME) {
        Write-Host "CODEX_HOME: $env:CODEX_HOME"
    }
    Write-Host "APPDATA: $env:APPDATA"
    Write-Host "LOCALAPPDATA: $env:LOCALAPPDATA"
    Write-Host "HOME: $env:HOME"
    Write-Host "USERPROFILE: $env:USERPROFILE"
    exit 0
}

$commandName = $Command[0]
$commandArgs = @()
if ($Command.Count -gt 1) {
    $commandArgs = $Command[1..($Command.Count - 1)]
}

& $commandName @commandArgs
exit $LASTEXITCODE
