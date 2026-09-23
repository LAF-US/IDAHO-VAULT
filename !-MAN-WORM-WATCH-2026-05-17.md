---
title: "worm-watch(7)"
updated: 2026-05-17
status: active
authority: LOGAN
related:
  - GitHub
  - package managers
  - Shai-Hulud
  - secret-pattern
  - CI
---

# worm-watch(7)

## NAME

worm-watch - local operator checks for package-manager worm exposure

## SYNOPSIS

```powershell
git status --short --branch
git ls-files -z | python .github/scripts/check_secret_patterns.py --paths-from-stdin
rg -n -S "pull_request_target|id-token:\\s*write|contents:\\s*write" .github/workflows
rg -n -S "preinstall|postinstall|prepare|npm publish|twine|setup.mjs|router_init|router_runtime" package.json package-lock.json pyproject.toml requirements.txt uv.lock .github
```

## DESCRIPTION

`worm-watch` is a lightweight sanity check for supply-chain malware risk in
`IDAHO-VAULT`. It does not prove the machine is clean. It checks the repo
surfaces most relevant to worms like Shai-Hulud: package manifests, install
hooks, CI permissions, package publishing routes, and committed secrets.

## CHECKS

1. Confirm the worktree state before touching anything.
2. Scan all tracked files for secret paths and secret-looking values.
3. Inspect package manifests and lockfiles for suspicious install hooks.
4. Inspect GitHub Actions for risky trust boundaries.
5. Keep dependency install commands behind human approval.
6. Treat any committed private key or token as compromised.

## FILES

- `.github/scripts/check_secret_patterns.py`
- `.github/workflows/secret-pattern-policy.yml`
- `.github/workflows/secret-pattern-full-scan.yml`
- `.gitignore`
- `.vscode/settings.json`

## EXIT STATUS

- `0`: no configured secret pattern found
- `1`: possible secret material detected

## REMEDIATION

Rotate exposed credentials first. After rotation, remove credential files from
git tracking, strengthen `.gitignore`, and run the full tracked-file scan
again. Removing a file from the current tree does not purge it from git
history.

