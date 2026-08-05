# IDAHO-VAULT Untracked Stabilization Files

Last checked: 2026-05-07

## Decision

Do not commit, delete, or ignore the current untracked stabilization files yet.

Treat them as a local stabilization work bundle that needs review before it becomes part of the canonical vault history.

## Why

The untracked files are concentrated and purposeful, but the evidence is mixed:

- Markdown reports describe the system as stabilized or complete.
- `STABILIZATION-STATUS.json` still records failed/degraded checks for Ollama, OpenRouter, and governance files.
- `SKEPTICAL-VERIFICATION.json` has `"Overall": false`.
- Several scripts and a notebook appear to be implementation or verification artifacts, not just documentation.

That means the safe novice-coder move is to preserve the bundle, review it, and only commit a smaller coherent subset later.

## Current Untracked Files

From `C:\Users\loganf\Documents\IDAHO-VAULT`:

```text
?? !/FINAL-STABILIZATION-REPORT.md
?? !/SKEPTICAL-VERIFICATION.json
?? !/STABILIZATION-PLAN.md
?? !/STABILIZATION-REPORT.md
?? !/STABILIZATION-STATUS.json
?? !/STABILIZATION-SUMMARY.md
?? !/STATE/
?? !/SimpleStabilization.ps1
?? !/StabilizationSystem.ipynb
?? !/VaultStabilization.psm1
?? !/final-verification.ps1
?? !/skeptical-verification.ps1
?? !/test-simple-stabilization.ps1
?? !/test-stabilization.ps1
?? STABILIZATION-COMPLETE.md
```

Files under `!/STATE/`:

```text
!/STATE/final-verification.json
!/STATE/skeptical-test.json
!/STATE/test-001.json
```

## Recommended Next Action

When ready, review the PowerShell module and tests first:

```powershell
Get-Content C:\Users\loganf\Documents\IDAHO-VAULT\!\VaultStabilization.psm1
Get-Content C:\Users\loganf\Documents\IDAHO-VAULT\!\test-stabilization.ps1
Get-Content C:\Users\loganf\Documents\IDAHO-VAULT\!\skeptical-verification.ps1
```

Then choose one of these outcomes:

1. Commit the working module, tests, and accurate status docs.
2. Move the bundle to a dated archive outside the repo.
3. Keep only the plan/report docs and discard generated state after review.

Do not add these paths to `.gitignore` until that choice is made.
