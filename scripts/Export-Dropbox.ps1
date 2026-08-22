<#
.SYNOPSIS
    Pull everything reachable from the Dropbox rclone remote to a local
    destination, with a manifest captured BEFORE the copy and a checksum
    verification AFTER. Windows counterpart to export-dropbox.sh.

.DESCRIPTION
    Built for the "subscription expired, get everything out" scenario.

    Grounding: rclone remotes are already configured per
    BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS.md (remote "dropbox:"). This
    script auto-detects whichever Dropbox remote exists.

    IMPORTANT — rclone CANNOT export Dropbox Paper documents or orphaned
    blocks from unlinked devices. Those account for the ~304 GB gap between
    `rclone about` (309 GB) and the file API (~5.2 GB). Use the browser steps
    in DROPBOX-EXPORT-RUNBOOK for those.

    No Git Bash / WSL / admin rights required (per CLAUDE.md Windows rules).

.PARAMETER Destination
    Local folder to copy into. Created if missing.

.PARAMETER Remote
    Optional rclone remote name (e.g. "dropbox:"). Auto-detected if omitted.

.EXAMPLE
    .\Export-Dropbox.ps1 -Destination "D:\DROPBOX-EXPORT-2026-06-23"

.EXAMPLE
    .\Export-Dropbox.ps1 -Destination "D:\DROPBOX-EXPORT" -Remote "dropbox:"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [Parameter(Mandatory = $false)]
    [string]$Remote
)

$ErrorActionPreference = "Stop"

# ---- locate rclone ----------------------------------------------------------
if (-not (Get-Command rclone -ErrorAction SilentlyContinue)) {
    Write-Error "rclone not found on PATH. Install with 'scoop install rclone' and re-run."
    exit 3
}
Write-Host ">> rclone: $((rclone version) | Select-Object -First 1)"

# ---- auto-detect the Dropbox remote ----------------------------------------
if ([string]::IsNullOrWhiteSpace($Remote)) {
    $Remote = (rclone listremotes | Where-Object { $_ -match 'dropbox' } | Select-Object -First 1)
    if ([string]::IsNullOrWhiteSpace($Remote)) {
        Write-Error "No Dropbox remote found in 'rclone listremotes'. Configure one with 'rclone config' or pass -Remote."
        exit 4
    }
}
if (-not $Remote.EndsWith(":")) { $Remote = "$Remote`:" }
Write-Host ">> Using remote: $Remote"

# ---- destination + log scaffolding -----------------------------------------
$Stamp    = Get-Date -Format "yyyy-MM-dd_HHmmss"
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$LogDir   = Join-Path $Destination "_export-logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Manifest = Join-Path $LogDir "manifest-$Stamp.jsonl"
$CopyLog  = Join-Path $LogDir "copy-$Stamp.log"
$CheckLog = Join-Path $LogDir "check-$Stamp.log"
$Summary  = Join-Path $LogDir "summary-$Stamp.txt"

Write-Host ">> Destination: $Destination"
Write-Host ">> Logs:        $LogDir"

# ---- preflight: quota + reachability ---------------------------------------
Write-Host ">> Preflight: rclone about $Remote"
"=== rclone about $Remote ($Stamp) ===" | Out-File -FilePath $Summary -Encoding utf8
rclone about $Remote 2>&1 | Tee-Object -FilePath $Summary -Append
"" | Out-File -FilePath $Summary -Append -Encoding utf8
"=== top-level dirs (rclone lsd) ===" | Out-File -FilePath $Summary -Append -Encoding utf8
rclone lsd $Remote 2>&1 | Tee-Object -FilePath $Summary -Append
"=== shared-folder probe (--dropbox-shared-folders) ===" | Out-File -FilePath $Summary -Append -Encoding utf8
rclone lsd $Remote --dropbox-shared-folders 2>&1 | Tee-Object -FilePath $Summary -Append

# ---- manifest BEFORE copy ---------------------------------------------------
Write-Host ">> Capturing full manifest -> $Manifest"
rclone lsjson $Remote --recursive --hash | Out-File -FilePath $Manifest -Encoding utf8

# ---- the copy (resumable / idempotent) -------------------------------------
Write-Host ">> Copying $Remote -> $Destination  (log: $CopyLog)"
rclone copy $Remote $Destination `
    --transfers 8 `
    --checkers 16 `
    --retries 5 `
    --low-level-retries 10 `
    --track-renames `
    --create-empty-src-dirs `
    --stats 30s `
    --stats-one-line `
    --log-level INFO `
    --log-file $CopyLog `
    --progress

# ---- verify -----------------------------------------------------------------
Write-Host ">> Verifying with rclone check (log: $CheckLog)"
rclone check $Remote $Destination --one-way --log-file $CheckLog --log-level INFO
if ($LASTEXITCODE -eq 0) {
    Write-Host ">> VERIFY: OK — every source file is present at destination."
} else {
    Write-Warning ">> VERIFY: MISMATCHES found. Inspect $CheckLog before deleting anything in Dropbox."
}

# ---- summary ----------------------------------------------------------------
@"

=== EXPORT SUMMARY ($Stamp) ===
Remote:      $Remote
Destination: $Destination
Manifest:    $Manifest
Copy log:    $CopyLog
Check log:   $CheckLog

REMINDER: rclone cannot export Dropbox Paper docs or orphaned device blocks.
If 'rclone about' above shows far more used space than was copied, do the
browser steps in DROPBOX-EXPORT-RUNBOOK before the subscription lapses.
"@ | Tee-Object -FilePath $Summary -Append

Write-Host ">> Done. Review $Summary"
