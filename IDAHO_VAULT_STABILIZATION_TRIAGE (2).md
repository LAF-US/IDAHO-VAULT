# IDAHO-VAULT Stabilization Triage

Last checked: 2026-05-07

## Summary

The stabilization bundle is worth preserving, but it is not commit-ready as-is.

The main issue is not that everything failed. Some checks are false negatives caused by path assumptions that do not match the current vault layout.

## What Exists In The Repo

These governance files exist at the vault root:

```text
CONSTITUTION.md
LEVELSET.md
AGENTS.md
```

The stabilization scripts currently check for some governance files under `!\`, including:

```text
!\LEVELSET-STEP-0-EXTERNAL-AGENT.md
!\AGENTS.md
```

Those paths do not match the actual current repo layout, so compliance checks can fail even when the canonical files exist.

## Keep

Likely useful source files:

```text
!/SimpleStabilization.ps1
!/VaultStabilization.psm1
!/test-stabilization.ps1
!/final-verification.ps1
!/skeptical-verification.ps1
```

Likely useful documentation, after correcting status language:

```text
!/STABILIZATION-PLAN.md
!/STABILIZATION-REPORT.md
!/STABILIZATION-SUMMARY.md
!/FINAL-STABILIZATION-REPORT.md
```

## Fix Before Commit

1. Update compliance checks to look for root-level `LEVELSET.md` and `AGENTS.md`.
2. Make the reports match the JSON results. Do not call the system fully stabilized while `Overall` is false or key dependencies are degraded.
3. Decide whether `SimpleStabilization.ps1` or `VaultStabilization.psm1` is canonical. Right now the verification scripts use the simple script, while the fuller module is separate.
4. Make 1Password checks account-aware if they are kept, because `op vault list --account my.1password.com` works more reliably than plain `op whoami` in this environment.
5. Avoid committing generated state files unless the vault intentionally tracks run history.

## Archive Or Regenerate

Generated state/output files:

```text
!/SKEPTICAL-VERIFICATION.json
!/STABILIZATION-STATUS.json
!/STATE/final-verification.json
!/STATE/skeptical-test.json
!/STATE/test-001.json
```

Notebook:

```text
!/StabilizationSystem.ipynb
```

The notebook may be useful as a development artifact, but it should be reviewed separately before committing.

## Recommended Next Patch

Make a narrow script-only patch:

1. Fix `Check-LEVELSETCompliance` in `!/SimpleStabilization.ps1`.
2. Fix `Perform-LEVELSETCheck` in `!/VaultStabilization.psm1`.
3. Rerun the verification scripts.
4. Update reports only after the new results are known.

Do not commit yet.
