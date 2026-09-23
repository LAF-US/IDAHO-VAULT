---
title: "Worm Watch Hardening"
updated: 2026-05-17
status: active
authority: LOGAN
related:
  - GitHub
  - Shai-Hulud
  - Node
  - Python
  - SSH
  - Docker
  - security
  - secrets
---

# Worm Watch Hardening

This note records the local posture for package-manager worm defense in
`IDAHO-VAULT`.

## Operating Rule

Package installation is code execution. Treat these commands as high-trust
actions:

- `npm install`
- `npm ci`
- `pip install`
- `uv sync`
- Docker builds from unfamiliar images or Dockerfiles
- workflow jobs that run dependency installs while secrets are available

## Local Defaults

- Dependency installation should require human approval.
- Tokens, SSH keys, `.env` files, package-manager auth files, and service
  account JSON must not be committed.
- Runtime logs, caches, shell snapshots, extracted text caches, and tool-local
  identity files should remain local unless Logan explicitly promotes them as
  public records.
- Use the repository secret-pattern checker before staging sensitive changes:

```powershell
git diff --cached --name-only --diff-filter=ACMR -z |
  python .github/scripts/check_secret_patterns.py --paths-from-stdin
```

For a full tracked-file check:

```powershell
git ls-files -z |
  python .github/scripts/check_secret_patterns.py --paths-from-stdin
```

## High-Risk Surfaces

- `pull_request_target` workflows with write permissions
- `id-token: write` in GitHub Actions
- auto-merge workflows
- package publish workflows
- local editor auto-approval rules
- `node_modules`, `.venv`, package caches, and Obsidian plugin caches

## Current Posture

As of this witness pass, the root Node surface is small and has only Prettier
as a dependency. The Python surface is broader because CrewAI and supporting
tools pull a real dependency graph. The main hardening work is therefore not
"panic about every package"; it is keeping credentials scarce, scoped, and out
of install-time execution paths.

