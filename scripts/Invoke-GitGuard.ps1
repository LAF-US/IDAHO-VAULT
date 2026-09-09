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

                # Fail fast instead of hanging a plain `git status`: skip
                # credential prompts, and enforce a hard wall-clock timeout
                # around fetch. http.lowSpeedLimit/lowSpeedTime alone do NOT
                # bound the initial connect phase (verified against the bash
                # wrapper) - an unreachable host can still hang indefinitely,
                # so launch fetch as a real child process and kill it if it
                # outlives the timeout.
                # Use the single-string Arguments property, not ArgumentList
                # (a Collection<string> added in .NET Core 2.1+) - Windows
                # PowerShell 5.1 runs on the older .NET Framework, which
                # doesn't have ArgumentList and would throw here.
                $psi = New-Object System.Diagnostics.ProcessStartInfo
                $psi.FileName = $realGit
                $psi.Arguments = "fetch origin --quiet"
                $psi.EnvironmentVariables["GIT_TERMINAL_PROMPT"] = "0"
                $psi.UseShellExecute = $false
                $psi.RedirectStandardOutput = $true
                $psi.RedirectStandardError = $true
                $proc = [System.Diagnostics.Process]::Start($psi)
                if (-not $proc.WaitForExit(10000)) {
                    # Process.Kill(bool) tree-kill overload needs .NET Core
                    # 3.0+ (PowerShell 7+); fall back to plain Kill() for
                    # Windows PowerShell 5.1's older .NET Framework.
                    try { $proc.Kill($true) } catch { try { $proc.Kill() } catch {} }
                }

                & $realGit branch --set-upstream-to=origin/main main 2>$null
            }
        }
    }

    & $realGit @args
}
