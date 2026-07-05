#!/bin/sh
# git-guard: auto-reconnects the IDAHO-VAULT origin remote before delegating
# to the real git. See !-AGENT-GIT-GUARDRAILS.md for install instructions.
#
# Install as ~/bin/git (not ~/bin/git-guard) with ~/bin ahead of the real
# git's directory in PATH, so plain `git ...` calls actually go through this
# wrapper instead of resolving straight to the system git.
#
# GIT_GUARD_MARKER=idaho-vault-git-guard-v1

REPO_NAME="IDAHO-VAULT"
REPO_URL="https://github.com/LAF-US/IDAHO-VAULT.git"

# Identify "self" (this wrapper, or any other copy of it) by content, not by
# $0. Argv[0] reflects whatever the calling shell chose to pass, which is not
# guaranteed to be an absolute, dereferenced path across every shell - so
# comparing paths can under- or over-match. Grepping each PATH candidate for
# this script's own marker line is shell-agnostic and unambiguous: the real
# git binary will never contain it. `-q` alone (no `-a`) is enough: `-a` is a
# GNU/BSD extension, not POSIX, and may be rejected by a minimal grep; we
# only need the match/no-match exit status, not the printed output.
real_git=""
old_ifs=$IFS
IFS=:
for dir in $PATH; do
  [ -n "$dir" ] || continue
  candidate="$dir/git"
  [ -x "$candidate" ] || continue
  [ -f "$candidate" ] || continue
  grep -q "GIT_GUARD_MARKER=idaho-vault-git-guard-v1" "$candidate" >/dev/null 2>&1 && continue
  real_git=$candidate
  break
done
IFS=$old_ifs

if [ -z "$real_git" ]; then
  echo "git-guard: could not find a real git executable on PATH (excluding self)" >&2
  exit 127
fi

# Detect the repo by worktree folder name, not by grepping .git/config for
# the repo name - that string lives only in the remote URL, so it vanishes
# from .git/config the moment `git remote remove origin` runs, which is
# exactly when the guard needs to fire. Compare case-insensitively (matches
# Invoke-GitGuard.ps1's -ieq) so a differently-cased checkout still matches.
toplevel=$("$real_git" rev-parse --show-toplevel 2>/dev/null)
if [ -n "$toplevel" ]; then
  leaf_lower=$(basename "$toplevel" | tr '[:upper:]' '[:lower:]')
  repo_lower=$(printf '%s' "$REPO_NAME" | tr '[:upper:]' '[:lower:]')
  if [ "$leaf_lower" = "$repo_lower" ]; then
    if ! "$real_git" remote 2>/dev/null | grep -qx origin; then
      "$real_git" remote add origin "$REPO_URL" 2>/dev/null
      # Fail fast instead of hanging a plain `git status`: skip credential
      # prompts, and enforce a hard wall-clock timeout around fetch. Verified
      # that http.lowSpeedLimit/lowSpeedTime alone do NOT bound the initial
      # connect phase - an unreachable host can still hang indefinitely, so
      # this backgrounds the fetch and kills it after GIT_GUARD_FETCH_TIMEOUT
      # seconds. Not using GNU `timeout`/`gtimeout` since it isn't guaranteed
      # present (notably on stock macOS).
      GIT_GUARD_FETCH_TIMEOUT=${GIT_GUARD_FETCH_TIMEOUT:-10}
      GIT_TERMINAL_PROMPT=0 "$real_git" fetch origin --quiet 2>/dev/null &
      fetch_pid=$!
      waited=0
      while [ "$waited" -lt "$GIT_GUARD_FETCH_TIMEOUT" ]; do
        kill -0 "$fetch_pid" 2>/dev/null || break
        sleep 1
        waited=$((waited + 1))
      done
      if kill -0 "$fetch_pid" 2>/dev/null; then
        kill "$fetch_pid" 2>/dev/null
      fi
      wait "$fetch_pid" 2>/dev/null
      "$real_git" branch --set-upstream-to=origin/main main 2>/dev/null
    fi
  fi
fi

exec "$real_git" "$@"
