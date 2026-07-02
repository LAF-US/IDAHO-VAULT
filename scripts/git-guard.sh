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
# git binary will never contain it.
real_git=""
old_ifs=$IFS
IFS=:
for dir in $PATH; do
  [ -n "$dir" ] || continue
  candidate="$dir/git"
  [ -x "$candidate" ] || continue
  [ -f "$candidate" ] || continue
  grep -qa "GIT_GUARD_MARKER=idaho-vault-git-guard-v1" "$candidate" 2>/dev/null && continue
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
# exactly when the guard needs to fire.
toplevel=$("$real_git" rev-parse --show-toplevel 2>/dev/null)
if [ -n "$toplevel" ]; then
  case "$(basename "$toplevel")" in
    "$REPO_NAME"|"$(printf '%s' "$REPO_NAME" | tr '[:upper:]' '[:lower:]')")
      if ! "$real_git" remote 2>/dev/null | grep -qx origin; then
        "$real_git" remote add origin "$REPO_URL" 2>/dev/null
        "$real_git" fetch origin 2>/dev/null
        "$real_git" branch --set-upstream-to=origin/main main 2>/dev/null
      fi
      ;;
  esac
fi

exec "$real_git" "$@"
