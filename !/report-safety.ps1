function Get-SafeReportOutDir {
    param(
        [string]$RepoRoot,
        [string]$RequestedOutDir
    )

    if ($RequestedOutDir) {
        return [System.IO.Path]::GetFullPath($RequestedOutDir)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $RepoRoot ".state\1password-reports"))
}

function Test-IsPathWithinRoot {
    param(
        [string]$Path,
        [string]$Root
    )

    $fullPath = [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
    $fullRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd('\')

    return $fullPath.StartsWith("$fullRoot\", [System.StringComparison]::OrdinalIgnoreCase) -or
        $fullPath.Equals($fullRoot, [System.StringComparison]::OrdinalIgnoreCase)
}

function Assert-ReportOutDirSafe {
    param(
        [string]$RepoRoot,
        [string]$OutDir
    )

    $resolvedOutDir = [System.IO.Path]::GetFullPath($OutDir)
    $resolvedRepoRoot = [System.IO.Path]::GetFullPath($RepoRoot)

    if (Test-IsPathWithinRoot -Path $resolvedOutDir -Root $resolvedRepoRoot) {
        $stateRoot = [System.IO.Path]::GetFullPath((Join-Path $resolvedRepoRoot ".state"))
        $tmpRoot = [System.IO.Path]::GetFullPath((Join-Path $resolvedRepoRoot ".tmp"))

        if (-not (Test-IsPathWithinRoot -Path $resolvedOutDir -Root $stateRoot) -and -not (Test-IsPathWithinRoot -Path $resolvedOutDir -Root $tmpRoot)) {
            throw "Refusing to write reports under tracked repo paths. Use a gitignored path under .state or .tmp, or an absolute path outside the repo."
        }

        $tracked = @(& git -C $resolvedRepoRoot ls-files -- $resolvedOutDir 2>$null)
        if ($tracked.Count -gt 0) {
            throw "Refusing to write reports into a tracked path: $resolvedOutDir"
        }
    }
}

function Initialize-ReportOutDir {
    param(
        [string]$RepoRoot,
        [string]$RequestedOutDir
    )

    $resolvedOutDir = Get-SafeReportOutDir -RepoRoot $RepoRoot -RequestedOutDir $RequestedOutDir
    Assert-ReportOutDirSafe -RepoRoot $RepoRoot -OutDir $resolvedOutDir
    New-Item -ItemType Directory -Force -Path $resolvedOutDir | Out-Null
    return $resolvedOutDir
}

function Test-ReportContentSafe {
    param([string]$Content)

    $patterns = @(
        'op://',
        'sk-ant-[A-Za-z0-9_-]+',
        'sk-or-v1-[A-Za-z0-9_-]+',
        'sk-proj-[A-Za-z0-9_-]+',
        'ghp_[A-Za-z0-9]+',
        'github_pat_[A-Za-z0-9_]+',
        'AIza[0-9A-Za-z\-_]{20,}',
        'ya29\.[0-9A-Za-z\-_]+',
        '1//[0-9A-Za-z\-_]+',
        'xox[baprs]-[0-9A-Za-z-]+',
        '-----BEGIN [A-Z ]*PRIVATE KEY-----',
        '"private_key"\s*:',
        '"refresh_token"\s*:',
        '"access_token"\s*:'
    )

    foreach ($pattern in $patterns) {
        if ($Content -match $pattern) {
            throw "Refusing to write report content that matches a secret-like pattern: $pattern"
        }
    }
}

function Write-SafeTextFile {
    param(
        [string]$Path,
        [string]$Content
    )

    Test-ReportContentSafe -Content $Content
    Set-Content -Path $Path -Value $Content -Encoding utf8
}

function Write-SafeJsonFile {
    param(
        [string]$Path,
        $Object,
        [int]$Depth = 8
    )

    $json = $Object | ConvertTo-Json -Depth $Depth
    Write-SafeTextFile -Path $Path -Content $json
}
