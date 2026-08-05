param(
    [string]$Mode,
    [switch]$List,
    [switch]$ShowCurrent,
    [switch]$AllowWhileRunning
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$obsidianDir = Join-Path $repoRoot ".obsidian"
$modeDir = Join-Path $obsidianDir "plugin-modes"
$communityPluginsPath = Join-Path $obsidianDir "community-plugins.json"
$backupPath = Join-Path $modeDir "_last-live-backup.json"

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Get-ModeFiles {
    Get-ChildItem -LiteralPath $modeDir -Filter "*.json" |
        Where-Object { $_.Name -notlike "_*" } |
        Sort-Object Name
}

if (-not (Test-Path -LiteralPath $modeDir)) {
    throw "Plugin mode directory not found: $modeDir"
}

if ($List) {
    Get-ModeFiles | ForEach-Object {
        $_.BaseName
    }
    exit 0
}

if ($ShowCurrent) {
    Get-Content -LiteralPath $communityPluginsPath
    exit 0
}

if (-not $Mode) {
    Write-Host "Specify -Mode <name>, or use -List / -ShowCurrent."
    exit 1
}

$modePath = Join-Path $modeDir ($Mode + ".json")
if (-not (Test-Path -LiteralPath $modePath)) {
    throw "Unknown mode '$Mode'. Use -List to see available modes."
}

$obsidianRunning = Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue
if ($obsidianRunning -and -not $AllowWhileRunning) {
    throw "Obsidian appears to be running. Close it before switching modes, or pass -AllowWhileRunning if Logan wants a live swap."
}

$targetPlugins = Get-Content -LiteralPath $modePath -Raw | ConvertFrom-Json
$missingPlugins = @()

foreach ($plugin in $targetPlugins) {
    $pluginPath = Join-Path (Join-Path $obsidianDir "plugins") $plugin
    if (-not (Test-Path -LiteralPath $pluginPath)) {
        $missingPlugins += $plugin
    }
}

if (Test-Path -LiteralPath $communityPluginsPath) {
    $currentRaw = Get-Content -LiteralPath $communityPluginsPath -Raw
    Write-Utf8NoBom -Path $backupPath -Content $currentRaw
}

$json = $targetPlugins | ConvertTo-Json
Write-Utf8NoBom -Path $communityPluginsPath -Content $json

Write-Host ("Applied mode: " + $Mode)
Write-Host ("Enabled plugins: " + $targetPlugins.Count)

if ($missingPlugins.Count -gt 0) {
    Write-Host "Missing plugin directories:"
    $missingPlugins | ForEach-Object { Write-Host ("- " + $_) }
}
