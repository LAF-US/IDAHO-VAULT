<#
.SYNOPSIS
    Reconcile dotfolders between HOME and IDAHO-VAULT.

.DESCRIPTION
    Snapshots or retires a persona chamber (dot-dir) from ~/.foo into the vault.
    Also creates anchor stubs (NAME.md + stub.txt) for vault-only persona chambers.

    Modes:
      -Snapshot:  copy files home→vault, leave home live (default for dry-run)
      -Retire:    move files home→vault (default for -Apply without -Snapshot)
      -Stub:      create anchor stubs without syncing files

    All flags:
      -Apply:   execute changes (without this, runs dry-run / report-only)
      -All:     process all dot-dirs under $HOME sequentially
      -Prune:   delete ~/.foo dir if empty after retire (ignored in -Snapshot)
    -NoCache: skip persistent hash cache
    -Force:   in -All mode, process even large cache/runtime dirs (normally skipped)
    -Quiet:   suppress per-file output

    Performance:
      - Uses [System.IO.DirectoryInfo]::EnumerateFiles (~10x faster than Get-ChildItem)
      - Size-based pre-filter: SHA256 only computed for same-size same-name files
      - Persistent hash cache (!-dotfolder-hashcache.json) reuses hashes across runs
        by matching cached size + LastWriteTime against current file metadata.
        Cache keyed by "home|vault/$dot/$relPath".
      - In-memory hash dedup: within a single run, each file is hashed at most once.

    Secrets:
      Denylist at $secretPatterns catches SSH keys, auth tokens, signing keys, etc.
      at scan time. Refused paths are reported but never written to vault disk.

    Anchor stubs:
      Every vault dot-dir gets NAME.md (frontmatter) + stub.txt ("¿!?") per
      STUB-PERSONAFOLDERS doctrine. Created automatically during -Snapshot/-Apply,
      or standalone via -Stub flag.

.PARAMETER DotName
    Name of the dot-dir to reconcile (with or without leading dot).
    Ignored when -All is set.

.PARAMETER Apply
    Execute changes. Without this, runs dry-run (report only).

.PARAMETER Snapshot
    Copy files from home to vault, keeping home contents live.
    Default is Retire mode (move files, empty home).

.PARAMETER Prune
    Delete ~/.foo directory itself if it becomes empty after retire.
    Ignored in Snapshot mode.

.PARAMETER Stub
    Create anchor stub files (NAME.md + stub.txt) in vault directory.
    Works standalone or combined with Snapshot/Retire.

.PARAMETER All
    Process all existing dot-dirs under $HOME sequentially.
    Each gets its own Write-Progress activity and a summary line.

.PARAMETER NoCache
    Skip reading/writing the persistent hash cache.
    Hashes are still computed per run (no cross-run reuse).

.PARAMETER Quiet
    Suppress per-file output during apply.
#>

param(
    [Parameter(Position = 0)]
    [string]$DotName,

    [switch]$Apply,
    [switch]$Snapshot,
    [switch]$Prune,
    [switch]$Stub,
    [switch]$All,
    [switch]$NoCache,
    [switch]$Force,
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$vaultRoot = $PSScriptRoot
$cachePath = Join-Path $vaultRoot "!-dotfolder-hashcache.json"

# -- Persistent hash cache --
# JSON file keyed by "home|vault/$dot/$relPath" → {size, mtime_ticks, sha256}
# Loaded once at startup, saved once after all processing.
# This avoids recomputing SHA256 for files whose size + LastWriteTime haven't changed.
$globalHashCache = @{}
$cacheDirty = $false

function Read-HashCache {
    if ($NoCache) { return }
    if (-not (Test-Path $cachePath)) { return }
    try {
        $raw = Get-Content -LiteralPath $cachePath -Raw -Encoding UTF8
        if ([string]::IsNullOrEmpty($raw)) { return }
        $parsed = $raw | ConvertFrom-Json
        foreach ($prop in $parsed.PSObject.Properties) {
            $globalHashCache[$prop.Name] = @{
                size   = [long]$prop.Value.size
                mtime  = [long]$prop.Value.mtime
                sha256 = [string]$prop.Value.sha256
            }
        }
    } catch {
        Write-Host "  [WARN] Cache read failed, starting fresh: $_"
    }
}

function Save-HashCache {
    if ($NoCache) { return }
    if (-not $cacheDirty) { return }
    try {
        $globalHashCache | ConvertTo-Json -Compress | Set-Content -LiteralPath $cachePath -Encoding UTF8 -NoNewline
    } catch {
        Write-Host "  [WARN] Cache write failed: $_"
    }
}

# -- Secret patterns --
$secretPatterns = @(
    'id_\w+$',
    'id_\w+\.\w+$',
    '_signing',
    'known_hosts',
    'authorized_keys',
    'allowed_signers',
    '\dPassword/config',
    'auth\.json',
    'signal-cli/data/',
    '_cacache/',
    '\.pem$',
    '\.key$',
    'credentials\.json',
    'token\.json',
    'tokens\.json',
    'oauth.*\.json',
    'client_secret.*\.json',
    'vault-courier-key\.json'
)

function Test-SecretPath($relPath) {
    foreach ($pat in $secretPatterns) {
        if ($relPath -match $pat) { return $true }
    }
    return $false
}

# -- Anchor stub writer --
function Write-StubFiles {
    param([string]$Dot, [string]$VaultDir, [switch]$Quiet)
    $created = @()
    if (-not (Test-Path $VaultDir)) {
        New-Item -ItemType Directory -Path $VaultDir -Force | Out-Null
        $created += "directory .$Dot"
    }
    $stubPath = Join-Path $VaultDir "stub.txt"
    if (-not (Test-Path $stubPath)) {
        Set-Content -Path $stubPath -NoNewline -Value "¿!?"
        if (-not $Quiet) { Write-Host "  [NEW] .\$Dot\stub.txt" }
        $created += "stub.txt"
    }
    $nameFile = "$($Dot.ToUpper()).md"
    $namePath = Join-Path $VaultDir $nameFile
    if (-not (Test-Path $namePath)) {
        $content = @"
---
authority: LOGAN
related:
  - $($Dot.ToUpper())
  - imported_software
  - runtime
---

**.$Dot** — Imported software runtime persona.

$Dot runtime and configuration.
"@
        Set-Content -Path $namePath -Value $content
        if (-not $Quiet) { Write-Host "  [NEW] .\$Dot\$nameFile" }
        $created += $nameFile
    }
    return $created
}

# -- Hash with persistent cache fallback --
function Get-FileHashCached($path, $cacheKey) {
    if (-not $cacheKey) {
        return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    }
    $entry = $globalHashCache[$cacheKey]
    if ($entry) {
        $file = [System.IO.FileInfo]::new($path)
        if ($file.Exists -and $file.Length -eq $entry.size -and $file.LastWriteTimeUtc.Ticks -eq $entry.mtime) {
            return $entry.sha256
        }
    }
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    $file = [System.IO.FileInfo]::new($path)
    $globalHashCache[$cacheKey] = @{
        size   = $file.Length
        mtime  = $file.LastWriteTimeUtc.Ticks
        sha256 = $hash
    }
    $script:cacheDirty = $true
    return $hash
}

# -- Fast file enumeration via .NET --
# DirectoryInfo.EnumerateFiles streams results lazily (no full-collection build).
# ~10x faster than Get-ChildItem -Recurse for large dirs like .codex (15K files).
function Get-RelativeFileMap($root) {
    $map = @{}
    if (-not (Test-Path $root)) { return $map }
    $rootNorm = $root.Replace('\', '/').TrimEnd('/') + '/'
    $dirInfo = New-Object System.IO.DirectoryInfo($root)
    $files = $dirInfo.EnumerateFiles('*', [System.IO.SearchOption]::AllDirectories)
    foreach ($f in $files) {
        $full = $f.FullName.Replace('\', '/')
        $rel = $full.Substring($rootNorm.Length)
        $map[$rel] = @{
            FullName = $f.FullName
            Length   = $f.Length
        }
    }
    return $map
}

# -- Core reconcile logic for one dot-dir --
function Invoke-ReconcileDotDir {
    param(
        [string]$Dot,
        [string]$HomeDir,
        [string]$VaultDir
    )

    $mode = if ($Stub -and -not $Apply -and -not $Snapshot) {
        "STUB (create vault anchor only)"
    } elseif ($Snapshot) {
        "SNAPSHOT (copy, keep home live)"
    } else {
        "RETIRE (move, empty home)"
    }
    if ($Stub -and $mode -notmatch "^STUB ") { $mode += " + STUB" }
    if (-not $Snapshot -and $Prune -and -not $Stub) { $mode += " + PRUNE" }
    if ($Snapshot -and $Prune) { Write-Host "[WARN] -Prune ignored in snapshot mode (home stays live)" }

    if (-not $Quiet) {
        Write-Host ("-" * 60)
        Write-Host "DOTFOLDER: .$Dot"
        Write-Host "  MODE:   $mode"
        Write-Host "  HOME:  $HomeDir"
        Write-Host "  VAULT: $VaultDir"
        Write-Host ("-" * 60)
    }

    $vaultExists = Test-Path $VaultDir
    if (-not $vaultExists) {
        Write-Host "[NEW] VAULT/.$Dot does not exist yet."
    }

    if ($Stub) {
        $stubResult = Write-StubFiles -Dot $Dot -VaultDir $VaultDir -Quiet:$Quiet
        $vaultExists = $true
    }

    if (-not (Test-Path $HomeDir)) {
        if (-not $Quiet) {
            Write-Host "[SKIP] HOME/.$Dot does not exist -- nothing to reconcile."
            if ($Stub) { Write-Host "  Stub files created in vault; no home to sync." }
        }
        return $null
    }

    # -- Scan --
    if (-not $Quiet) { Write-Progress -Activity "Processing .$Dot" -Status "Scanning home..." -PercentComplete 5 }
    $homeFiles = Get-RelativeFileMap $HomeDir

    if (-not $Quiet) { Write-Progress -Activity "Processing .$Dot" -Status "Scanning vault..." -PercentComplete 10 }
    $vaultFiles = Get-RelativeFileMap $VaultDir

    $allRel = @($homeFiles.Keys + $vaultFiles.Keys) | Sort-Object -Unique
    $total = @($allRel).Count
    
    # In apply mode, use the initial scan results for all operations (no re-scan)
    if ($Apply) {
        $initialHomeFiles = $homeFiles
        $initialVaultFiles = $vaultFiles
    }

    $uniqueToHome = @()
    $uniqueToVault = @()
    $identical  = @()
    $conflict   = @()
    $secrets    = @()

    $i = 0
    $scanStart = [datetime]::UtcNow

    foreach ($rel in $allRel) {
        $i++
        $pct = 10 + [int](($i / $total) * 70)
        if (-not $Quiet) { Write-Progress -Activity "Processing .$Dot ($($homeFiles.Count) home files)" -Status "Comparing $i of $total" -CurrentOperation $rel -PercentComplete $pct }

        $inHome = $homeFiles.ContainsKey($rel)
        $inVault = $vaultFiles.ContainsKey($rel)

        if (Test-SecretPath $rel) {
            $secrets += $rel
            continue
        }

        if ($inHome -and -not $inVault) {
            $uniqueToHome += $rel
        } elseif (-not $inHome -and $inVault) {
            $uniqueToVault += $rel
        } elseif ($homeFiles[$rel].Length -ne $vaultFiles[$rel].Length) {
            $conflict += $rel
        } else {
            $hKey = "home/$Dot/$rel"
            $vKey = "vault/$Dot/$rel"

            if (-not $Quiet) { Write-Progress -Activity "Processing .$Dot" -Status "Hashing $i of $total" -CurrentOperation $rel -PercentComplete $pct }
            $hHash = Get-FileHashCached -path $homeFiles[$rel].FullName -cacheKey $hKey
            $vHash = Get-FileHashCached -path $vaultFiles[$rel].FullName -cacheKey $vKey
            if ($hHash -eq $vHash) {
                $identical += $rel
            } else {
                $conflict += $rel
            }
        }
    }

    $scanTime = [datetime]::UtcNow - $scanStart
    if (-not $Quiet) { Write-Progress -Activity "Processing .$Dot" -Completed }

    # -- Report --
    if (-not $Quiet) {
        Write-Host ""
        Write-Host "  HOME:  $($homeFiles.Count) file(s)"
        Write-Host "  VAULT: $($vaultFiles.Count) file(s)"
        Write-Host "  SCAN:  $($scanTime.TotalSeconds.ToString('F1'))s"
        Write-Host ""
    }

    if ($uniqueToHome.Count -gt 0) {
        Write-Host "-- UNIQUE TO HOME ($($uniqueToHome.Count)) --"
        if ($Quiet) { Write-Host "  ($($uniqueToHome.Count) files)" }
        else { foreach ($f in $uniqueToHome) { Write-Host "  + $f" } }
        Write-Host ""
    }

    if ($identical.Count -gt 0) {
        Write-Host "-- IDENTICAL ($($identical.Count)) --"
        if ($Quiet) { Write-Host "  ($($identical.Count) files)" }
        else { foreach ($f in $identical) { Write-Host "  = $f" } }
        Write-Host ""
    }

    if ($conflict.Count -gt 0) {
        Write-Host "-- CONFLICT ($($conflict.Count)) --"
        if ($Quiet) {
            Write-Host "  ($($conflict.Count) files: both versions will be preserved in vault)"
        } else {
            foreach ($f in $conflict) { Write-Host "  ! $f (both versions will be preserved)" }
        }
        Write-Host ""
    }

    if ($uniqueToVault.Count -gt 0) {
        Write-Host "-- UNIQUE TO VAULT ($($uniqueToVault.Count)) --"
        if ($Quiet) { Write-Host "  ($($uniqueToVault.Count) files)" }
        else { foreach ($f in $uniqueToVault) { Write-Host "  - $f" } }
        Write-Host ""
    }

    if ($secrets.Count -gt 0) {
        Write-Host "-- SECRETS REFUSED ($($secrets.Count)) --"
        foreach ($f in $secrets) { Write-Host "  ! $f" }
        Write-Host ""
    }

    if ($uniqueToHome.Count -eq 0 -and $identical.Count -eq 0 -and $conflict.Count -eq 0 -and $secrets.Count -eq 0) {
        Write-Host "  Nothing to reconcile -- HOME/.$Dot and VAULT/.$Dot are in sync."
    }

    $hasMoves = $uniqueToHome.Count -gt 0
    $hasDeletes = $identical.Count -gt 0 -and -not $Snapshot

    if (-not $Apply) {
        if ($hasMoves -or $hasDeletes) {
            $hint = if ($Snapshot) { "pass -Snapshot -Apply to execute" } else { "pass -Apply to execute" }
            Write-Host "--- DRY RUN -- $hint ---"
        }
        return @{
            Dot          = $Dot
            FilesHome    = $homeFiles.Count
            FilesVault   = $vaultFiles.Count
            UniqueToHome = $uniqueToHome.Count
            Identical    = $identical.Count
            Conflict     = $conflict.Count
            Secrets      = $secrets.Count
            ScanSeconds  = $scanTime.TotalSeconds
        }
    }

    # -- APPLY --
    $handledConflicts = @{}
    Write-Host "--- APPLYING ---"

    # -- Handle conflicts first: preserve both versions in vault --
    if ($conflict.Count -gt 0) {
        Write-Host "  [DEBUG] Handling $($conflict.Count) conflicts"
        $ci = 0; $ct = $conflict.Count
        foreach ($rel in $conflict) {
            $ci++
            Write-Host "  [DEBUG] Conflict $ci of $ct - $rel"
            Write-Progress -Activity "Applying .$Dot" -Status "Preserving conflict $ci of $ct" -CurrentOperation $rel -PercentComplete ([int](($ci / $ct) * 100))
            
            # Use initial scan results in apply mode, current otherwise
            $vaultSrc = if ($Apply) { $initialVaultFiles[$rel].FullName } else { $vaultFiles[$rel].FullName }
            $vaultDst = Join-Path $VaultDir "$rel.vault"
            $vaultDstParent = Split-Path -Parent $vaultDst
            if (-not (Test-Path $vaultDstParent)) { New-Item -ItemType Directory -Path $vaultDstParent -Force | Out-Null }
            Write-Host "  PRESERVE vault version: $rel.vault"
            if (Test-Path $vaultSrc) {
                Move-Item -LiteralPath $vaultSrc -Destination $vaultDst -Force
            } else {
                Write-Host "    [WARN] Vault source not found: $vaultSrc"
            }
            
            # Move home file to vault with .home suffix
            $homeSrc = if ($Apply) { $initialHomeFiles[$rel].FullName } else { $homeFiles[$rel].FullName }
            $homeDst = Join-Path $VaultDir "$rel.home"
            $homeDstParent = Split-Path -Parent $homeDst
            if (-not (Test-Path $homeDstParent)) { New-Item -ItemType Directory -Path $homeDstParent -Force | Out-Null }
            $verb = if ($Snapshot) { "COPY" } else { "MOVE" }
            Write-Host "  $verb home version: $rel.home"
            if (Test-Path $homeSrc) {
                if ($Snapshot) {
                    Copy-Item -LiteralPath $homeSrc -Destination $homeDst -Force
                } else {
                    Move-Item -LiteralPath $homeSrc -Destination $homeDst -Force
                }
            } else {
                Write-Host "    [WARN] Home source not found: $homeSrc"
            }
        }
        Write-Progress -Activity "Applying .$Dot" -Completed
    }

    if ($hasMoves) {
        if (-not (Test-Path $VaultDir)) {
            Write-StubFiles -Dot $Dot -VaultDir $VaultDir -Quiet:$Quiet | Out-Null
        }
        $verb = if ($Snapshot) { "COPY" } else { "MOVE" }
        $ai = 0; $at = $uniqueToHome.Count
        foreach ($rel in $uniqueToHome) {
            # Skip files already handled as conflicts
            if ($handledConflicts.ContainsKey($rel)) { continue }
            
            $ai++
            Write-Progress -Activity "Applying .$Dot" -Status "$verb $ai of $at" -CurrentOperation $rel -PercentComplete ([int](($ai / $at) * 100))
            $src = if ($Apply) { $initialHomeFiles[$rel].FullName } else { $homeFiles[$rel].FullName }
            $dst = Join-Path $VaultDir $rel
            $dstParent = Split-Path -Parent $dst
            if (-not (Test-Path $dstParent)) { New-Item -ItemType Directory -Path $dstParent -Force | Out-Null }
            Write-Host "  $verb $rel"
            if ($Snapshot) {
                Copy-Item -LiteralPath $src -Destination $dst -Force
            } else {
                Move-Item -LiteralPath $src -Destination $dst -Force
            }
        }
        Write-Progress -Activity "Applying .$Dot" -Completed
    }

    if ($hasDeletes) {
        $di = 0; $dt = $identical.Count
        foreach ($rel in $identical) {
            $di++
            Write-Progress -Activity "Applying .$Dot" -Status "Deleting identical $di of $dt" -CurrentOperation $rel -PercentComplete ([int](($di / $dt) * 100))
            $path = if ($Apply) { $initialHomeFiles[$rel].FullName } else { $homeFiles[$rel].FullName }
            Write-Host "  DELETE $rel"
            Remove-Item -LiteralPath $path -Force
        }
        Get-ChildItem -LiteralPath $HomeDir -Recurse -Directory -Force | Where-Object {
            @(Get-ChildItem -LiteralPath $_.FullName -Force).Count -eq 0
        } | Remove-Item -Force -ErrorAction SilentlyContinue
        Write-Progress -Activity "Applying .$Dot" -Completed
    }

    if ($Prune -and -not $Snapshot -and (Test-Path $HomeDir)) {
        $remaining = @(Get-ChildItem -LiteralPath $HomeDir -Force)
        if ($remaining.Count -eq 0) {
            Write-Host "  PRUNE ~/.$Dot (empty)"
            Remove-Item -LiteralPath $HomeDir -Force
        } elseif (-not $Quiet) {
            Write-Host "  [SKIP] ~/.$Dot not empty ($($remaining.Count) item(s) remain)"
        }
    }

    if ($conflict.Count -gt 0) {
        Write-Host ""
        Write-Host "  [!!] $($conflict.Count) conflict(s) not resolved:"
        foreach ($f in $conflict) { Write-Host "     $f" }
    }

    Write-Host "--- DONE ---"

    return @{
        Dot          = $Dot
        FilesHome    = $homeFiles.Count
        FilesVault   = $vaultFiles.Count
        UniqueToHome = $uniqueToHome.Count
        Identical    = $identical.Count
        Conflict     = $conflict.Count
        Secrets      = $secrets.Count
        ScanSeconds  = $scanTime.TotalSeconds
    }
}

# -- Main entry point --
Read-HashCache

if ($All) {
    # Known cache/runtime dirs skipped in -All mode to avoid multi-minute scans.
    # These were populated during the initial snapshot and are already gitignored.
    # Pass -Force to process them anyway.
    $skipDirs = @(
        '.cache', '.npm-cache', '.pip-cache', '.uv-cache',
        '.pycache', '.pytest_cache', '.ruff_cache', '.venv',
        '.vscode', '.codex', '.ipynb_checkpoints', '.jupyter'
    )
    $homeDirs = Get-ChildItem -LiteralPath $HOME -Directory -Force | Where-Object { $_.Name -match '^\.' } | Sort-Object Name
    $total = $homeDirs.Count
    $results = @()
    $idx = 0
    foreach ($d in $homeDirs) {
        $idx++
        $dot = $d.Name -replace '^\.', ''
        $dirName = ".$dot"
        if (-not $Force -and $dirName -in $skipDirs) {
            if (-not $Quiet) { Write-Host "[SKIP] $dirName (cache/runtime, use -Force to override)" }
            continue
        }
        $result = Invoke-ReconcileDotDir -Dot $dot -HomeDir $d.FullName -VaultDir (Join-Path $vaultRoot $dirName)
        if ($result) { $results += $result }
    }
    Write-Host ("=" * 60)
    Write-Host "ALL RESULTS ($total dot-dirs)"
    Write-Host ("=" * 60)
    foreach ($r in $results) {
        Write-Host "  .$($r.Dot): $($r.FilesHome) home, $($r.FilesVault) vault, $($r.UniqueToHome) to-sync, $($r.Conflict) conflicts, $($r.Secrets) secrets, $($r.ScanSeconds.ToString('F1'))s"
    }
    $totalHome = 0; $totalUp = 0
    foreach ($r in $results) {
        try { $totalHome += $r.FilesHome } catch {}
        try { $totalUp   += $r.UniqueToHome } catch {}
    }
    Write-Host ""
    Write-Host "TOTAL: $totalHome home files across $total dirs, $totalUp unique-to-home"
} else {
    if ([string]::IsNullOrEmpty($DotName)) {
        Write-Error "DotName is required when -All is not specified."
        exit 1
    }
    $dot = if ($DotName -match "^\.(.+)$") { $matches[1] } else { $DotName }
    $homeDir = Join-Path $HOME ".$dot"
    $vaultDir = Join-Path $vaultRoot ".$dot"
    Invoke-ReconcileDotDir -Dot $dot -HomeDir $homeDir -VaultDir $vaultDir
}

Save-HashCache
