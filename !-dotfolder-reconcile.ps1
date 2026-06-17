param(
    [Parameter(Mandatory, Position = 0)]
    [string]$DotName,

    [switch]$Apply,
    [switch]$Snapshot,
    [switch]$Prune,
    [switch]$Stub,
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$vaultRoot = $PSScriptRoot

# Normalize: accept ".claude" or "claude"
$dot = if ($DotName -match "^\.(.+)$") { $matches[1] } else { $DotName }
$homeDir = Join-Path $HOME ".$dot"
$vaultDir = Join-Path $vaultRoot ".$dot"

$unexpectedAtRoot = @()

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
        if (-not $Quiet) { Write-Output "  [NEW] .\$Dot\stub.txt" }
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
        if (-not $Quiet) { Write-Output "  [NEW] .\$Dot\$nameFile" }
        $created += $nameFile
    }

    return $created
}

$mode = if ($Stub -and -not $Apply -and -not $Snapshot) {
    "STUB (create vault anchor only)"
} elseif ($Snapshot) {
    "SNAPSHOT (copy, keep home live)"
} else {
    "RETIRE (move, empty home)"
}
if ($Stub -and $mode -notmatch "^STUB ") { $mode += " + STUB" }
if (-not $Snapshot -and $Prune) { $mode += " + PRUNE (delete empty ~/.foo)" }
if ($Snapshot -and $Prune) { Write-Output "[WARN] -Prune ignored in snapshot mode (home stays live)" }

Write-Output ("-" * 60)
Write-Output "DOTFOLDER: .$dot"
Write-Output "  MODE:   $mode"
Write-Output "  HOME:  $homeDir"
Write-Output "  VAULT: $vaultDir"
Write-Output ("-" * 60)

# Check vault dir exists
$vaultExists = Test-Path $vaultDir
if (-not $vaultExists) {
    Write-Output "[NEW] VAULT/.$dot does not exist yet."
}

# Handle -Stub: create vault anchor stubs regardless of HOME
if ($Stub) {
    $stubResult = Write-StubFiles -Dot $dot -VaultDir $vaultDir -Quiet:$Quiet
    $vaultExists = $true
}

# Check home dir exists
if (-not (Test-Path $homeDir)) {
    Write-Output "[SKIP] HOME/.$dot does not exist -- nothing to reconcile."
    if ($Stub) { Write-Output "  Stub files created in vault; no home to sync." }
    return
}

# Secret patterns that must never be ingested into a public vault
$secretPatterns = @(
    'id_\w+$',              # id_ed25519, id_rsa (no extension)
    'id_\w+\.\w+$',         # id_ed25519.pub, id_rsa.priv
    '_signing',             # claude_code_signing (private key) + .pub variant
    'known_hosts',
    'authorized_keys',
    'allowed_signers',      # email/identity mapping — personal info
    '\dPassword/config',    # 1Password SSH agent config
    'auth\.json',           # any dot-dir auth state with live credentials
    'signal-cli/data/',     # Signal identity private keys
    '_cacache/',            # npm package cache (can embed tokens)
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

# Scan both trees
function Get-RelativeFileMap($root) {
    $map = @{}
    if (-not (Test-Path $root)) { return $map }
    $rootNorm = $root.Replace('\', '/').TrimEnd('/') + '/'
    Get-ChildItem -LiteralPath $root -Recurse -File -Force | ForEach-Object {
        $full = $_.FullName.Replace('\', '/')
        $rel = $full.Substring($rootNorm.Length)
        $map[$rel] = @{
            FullName = $_.FullName
            Length   = $_.Length
            Hash     = $null
        }
    }
    return $map
}

$homeFiles = Get-RelativeFileMap $homeDir
$vaultFiles = Get-RelativeFileMap $vaultDir
$allRel = ($homeFiles.Keys + $vaultFiles.Keys) | Sort-Object -Unique

$uniqueToHome = @()
$uniqueToVault = @()
$identical  = @()
$conflict   = @()
$secrets    = @()

# Precompute hashes lazily
$hashCache = @{}
function Get-FileHashCached($path) {
    if (-not $hashCache.ContainsKey($path)) {
        $hashCache[$path] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    }
    return $hashCache[$path]
}

foreach ($rel in $allRel) {
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
        $hHash = Get-FileHashCached $homeFiles[$rel].FullName
        $vHash = Get-FileHashCached $vaultFiles[$rel].FullName
        if ($hHash -eq $vHash) {
            $identical += $rel
        } else {
            $conflict += $rel
        }
    }
}

$fileCountHome = $homeFiles.Count
$fileCountVault = $vaultFiles.Count

Write-Output ""
Write-Output "  HOME:  $fileCountHome file(s)"
Write-Output "  VAULT: $fileCountVault file(s)"
Write-Output ""

if ($uniqueToHome.Count -gt 0) {
    Write-Output "-- UNIQUE TO HOME (cruft to review, candidate to move to vault) --"
    foreach ($f in $uniqueToHome) { Write-Output "  + $f" }
    Write-Output ""
}

if ($identical.Count -gt 0) {
    Write-Output "-- IDENTICAL (safe to delete from home) --"
    foreach ($f in $identical) { Write-Output "  = $f" }
    Write-Output ""
}

if ($conflict.Count -gt 0) {
    Write-Output "-- CONFLICT (same name, different content -- manual review needed) --"
    foreach ($f in $conflict) { Write-Output "  ! $f" }
    Write-Output ""
}

if ($uniqueToVault.Count -gt 0) {
    Write-Output "-- UNIQUE TO VAULT (left alone -- vault is authoritative) --"
    foreach ($f in $uniqueToVault) { Write-Output "  - $f" }
    Write-Output ""
}

if ($secrets.Count -gt 0) {
    Write-Output "-- SECRETS (refused -- will never be ingested into public vault) --"
    foreach ($f in $secrets) { Write-Output "  ! $f" }
    Write-Output ""
}

if ($uniqueToHome.Count -eq 0 -and $identical.Count -eq 0 -and $conflict.Count -eq 0 -and $secrets.Count -eq 0) {
    Write-Output "  Nothing to reconcile -- HOME/.$dot and VAULT/.$dot are in sync."
}

# Determine what work there is to do
$hasMoves = $uniqueToHome.Count -gt 0
$hasDeletes = $identical.Count -gt 0 -and -not $Snapshot
$hasAnything = $hasMoves -or $hasDeletes -or $secrets.Count -gt 0 -or $conflict.Count -gt 0
if (-not $Apply) {
    if ($hasMoves -or $hasDeletes) {
        $hint = if ($Snapshot) { "pass -Snapshot -Apply to execute" } else { "pass -Apply to execute" }
        Write-Output "--- DRY RUN -- $hint ---"
    } elseif (-not $hasAnything) {
        # Nothing at all
    }
    return
}

if (-not $hasMoves -and -not $hasDeletes) {
    if ($secrets.Count -gt 0 -or $conflict.Count -gt 0) {
        Write-Output "  No auto-actionable items (secrets and conflicts require manual handling)."
    }
    return
}

# -- APPLY --

Write-Output "--- APPLYING ---"

# 1. Ingest unique-to-home files into vault
if ($hasMoves) {
    if (-not (Test-Path $vaultDir)) {
        Write-StubFiles -Dot $dot -VaultDir $vaultDir -Quiet:$Quiet | Out-Null
    }
    $verb = if ($Snapshot) { "COPY" } else { "MOVE" }
    foreach ($rel in $uniqueToHome) {
        $src = $homeFiles[$rel].FullName
        $dst = Join-Path $vaultDir $rel
        $dstParent = Split-Path -Parent $dst
        if (-not (Test-Path $dstParent)) { New-Item -ItemType Directory -Path $dstParent -Force | Out-Null }

        Write-Output "  $verb $rel"
        if ($Snapshot) {
            Copy-Item -LiteralPath $src -Destination $dst -Force
        } else {
            Move-Item -LiteralPath $src -Destination $dst -Force
        }
    }
}

# 2. Delete identical files from home (retire mode only)
if ($hasDeletes) {
    foreach ($rel in $identical) {
        $path = $homeFiles[$rel].FullName
        Write-Output "  DELETE $rel"
        Remove-Item -LiteralPath $path -Force
    }
    # Clean empty directories left behind
    Get-ChildItem -LiteralPath $homeDir -Recurse -Directory -Force | Where-Object {
        @(Get-ChildItem -LiteralPath $_.FullName -Force).Count -eq 0
    } | Remove-Item -Force -ErrorAction SilentlyContinue
}

# 2b. Prune: delete the home dot-directory itself if empty (retire mode only)
if ($Prune -and -not $Snapshot -and (Test-Path $homeDir)) {
    $remaining = @(Get-ChildItem -LiteralPath $homeDir -Force)
    if ($remaining.Count -eq 0) {
        Write-Output "  PRUNE ~/.$dot (empty)"
        Remove-Item -LiteralPath $homeDir -Force
    } else {
        Write-Output "  [SKIP] ~/.$dot not empty ($($remaining.Count) item(s) remain) – not pruning"
    }
}

# 3. Conflicts are NOT auto-resolved -- user must handle
if ($conflict.Count -gt 0) {
    Write-Output ""
    Write-Output "  [!!] $($conflict.Count) conflict(s) not resolved:"
    foreach ($f in $conflict) { Write-Output "     $f" }
}

Write-Output "--- DONE ---"