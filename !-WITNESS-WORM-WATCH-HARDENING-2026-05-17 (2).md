---
title: "Witness - Worm Watch Hardening"
updated: 2026-05-17
status: active
authority: LOGAN
related:
  - GitHub
  - Shai-Hulud
  - security
  - secret-pattern
  - CODEX
---

# Witness - Worm Watch Hardening

## Summary

Codex performed a local worm-watch sanity pass after recent Shai-Hulud package
manager reporting. No Shai-Hulud marker files or known indicator strings were
found in the root package surfaces, root `node_modules`, or local `.venv`.

The meaningful findings were local secret hygiene and automation posture:

- A tracked private key existed at `.ollama/id_ed25519`.
- VS Code terminal auto-approval included `npm install` and `npm run build`.
- Several ignored runtime/cache/log surfaces were still tracked.
- Full tracked-file secret scanning was not scheduled separately from the
  changed-file policy check.

## Actions Taken In This Branch

- Removed `npm install` and `npm run build` from VS Code terminal
  auto-approval.
- Added ignore coverage for `.op/`, `.factory/certs/`, Ollama identity keys,
  Claude shell snapshots, and Obsidian debug log rotations.
- Untracked the exposed Ollama identity files and local runtime/cache/log
  surfaces while leaving the local files on disk.
- Tightened the secret-pattern checker so placeholder values and
  `process.env.*` reads do not mask the signal from real findings.
- Added a scheduled/manual full tracked-file secret scan workflow.
- Added this witness report and a companion operator manual.

## Remaining Logan Actions

- Rotate or regenerate the Ollama SSH identity associated with
  `.ollama/id_ed25519`.
- Decide whether git history purging is warranted for the exposed key.
- Re-authenticate GitHub CLI before publish/PR automation; the current local
  `gh` token is invalid.
- Keep package installation commands behind explicit approval during active
  worm-watch conditions.

## Verification

The full tracked-file secret scan was run locally after cleanup:

```powershell
git ls-files -z |
  python .github/scripts/check_secret_patterns.py --paths-from-stdin
```

Result: `secret-pattern guard: OK`.

