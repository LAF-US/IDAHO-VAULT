# Invoke-GitGuard.ps1
# Defines a `git` PowerShell function that auto-reconnects the IDAHO-VAULT
# origin remote before delegating to the real git executable. See
# !-AGENT-GIT-GUARDRAILS.md for install instructions.
#
# Dot-source this from your PowerShell profile ($PROFILE):
#   . "<repo root>\scripts\Invoke-GitGuard.ps1"
#
# A PowerShell function named `git` shadows the git application automatically
# for interactive/session use - no PATH reordering, admin rights, or Git
# Bash/WSL required, matching this vault's Windows-first operating
# constraints.

function global:git {
    $repoName = "IDAHO-VAULT"
    $repoUrl = "https://github.com/LAF-US/IDAHO-VAULT.git"

    $realGit = (Get-Command -CommandType Application git -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty Source)

    if (-not $realGit) {
        Write-Error "git-guard: could not find a real git executable on PATH"
        return
    }

    # Detect the repo by worktree folder name, not by inspecting the origin
    # remote's URL - that value disappears the moment `git remote remove
    # origin` runs, which is exactly when the guard needs to fire.
    $topLevel = & $realGit rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $topLevel) {
        $leaf = Split-Path -Leaf $topLevel
        if ($leaf -ieq $repoName) {
            $hasOrigin = (& $realGit remote 2>$null) -contains "origin"
            if (-not $hasOrigin) {
                & $realGit remote add origin $repoUrl 2>$null
                & $realGit fetch origin 2>$null
                & $realGit branch --set-upstream-to=origin/main main 2>$null
            }
        }
    }

    & $realGit @args
}
