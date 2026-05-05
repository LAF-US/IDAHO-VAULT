---
title: "REPORT-RUNTIME-DOC-AUDIT-ROUND-2-2026-04-28"
status: active
authority: codex
doc_class: report
date created: 2026-04-28
related:
  - "DEPENDENCY_RESOLUTION_PLAN.md"
  - "install_dependencies.sh"
  - "scripts/validate_bootstrap.py"
  - "!/CREWAI/BOOTSTRAP-COMPATIBILITY.md"
  - ".crewai/MANIFEST.md"
---

# Runtime Doc Audit - Round 2

## Scope

Round 2 covers dependency/bootstrap portability promises and checkout-bound
truthfulness for the CrewAI shard.

## Classification

### Already implemented before this round

- `src/idaho_vault/bootstrap_contract.py` provides the live bootstrap contract.
- `scripts/Start-CrewAIVault.ps1` and `scripts/Use-VaultAgentEnv.ps1` provide
  the vault-contained local runner path.
- `.crewai/MANIFEST.md` already defines the canonical CrewAI doctrine.

### Partially implemented before this round

- `DEPENDENCY_RESOLUTION_PLAN.md` documented a real macOS-specific blocker, but
  it still read like an active operator plan instead of a platform-bound record.
- `install_dependencies.sh` existed, but it did not clearly describe itself as
  a helper/reference surface subordinate to the bootstrap contract.

### Implemented in this round

- `scripts/validate_bootstrap.py` now provides a single cross-platform preflight
  surface for the checkout-bound CrewAI bootstrap path.
- `!/CREWAI/BOOTSTRAP-COMPATIBILITY.md` is now the canonical output lane for
  bootstrap compatibility snapshots.
- Round 2 doc updates now steer operators toward bootstrap validation first and
  treat the legacy installer flow as helper/reference material.

## Current contract

- The canonical bootstrap path is checkout-bound, vault-local, and rooted in
  `uv.lock`, `.crewai/MANIFEST.md`, `src/idaho_vault/bootstrap_contract.py`,
  and the vault runtime launchers.
- `install_dependencies.sh` is not the authority surface for whether the shard
  is healthy.
- The right verification path is:
  - `python scripts/validate_bootstrap.py`
  - `powershell -ExecutionPolicy Bypass -File .\scripts\Start-CrewAIVault.ps1`
