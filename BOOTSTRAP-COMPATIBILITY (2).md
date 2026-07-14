# Bootstrap Compatibility Report

This is the canonical Round 2 bootstrap/dependency compatibility snapshot.

## Bootstrap Contract

- Overall status: `PASS`

| Check | Status | Detail |
| --- | --- | --- |
| `pyproject` | `PASS` | `pyproject.toml` exposes the CrewAI project and script contract |
| `lockfile` | `PASS` | `uv.lock` present and references CrewAI dependencies |
| `manifest-json` | `PASS` | `.crewai/manifest.json` registers the active bootstrap crew |
| `training-doctrine` | `PASS` | training doctrine matches the live bootstrap posture |
| `launcher` | `PASS` | launcher routes CrewAI through the vault-contained runtime helper |
| `config-surfaces` | `PASS` | bootstrap config surfaces present |
| `runtime-surface` | `PASS` | runtime containment maps CrewAI state into vault-local paths |
| `python-version` | `PASS` | repo Python marker present: `3.13.3` |
| `bootstrap-crew` | `PASS` | `src/idaho_vault/crew.py` present |
| `manifest-doc` | `PASS` | `.crewai/MANIFEST.md` present |

## Runtime And Dependency Notes

| Check | Status | Severity | Detail |
| --- | --- | --- | --- |
| Requirements lock surface | `OK` | `error` | `requirements.txt` present |
| uv lock surface | `OK` | `error` | `uv.lock` present |
| Vault launcher | `OK` | `error` | `scripts/Start-CrewAIVault.ps1` present |
| Runtime containment helper | `OK` | `error` | `scripts/Use-VaultAgentEnv.ps1` present |
| CrewAI doctrine | `OK` | `error` | `.crewai/MANIFEST.md` present |
| Bootstrap report lane | `OK` | `warn` | `!/CREWAI` present |
| uv CLI | `OK` | `warn` | `uv` available at `C:\Users\loganf\AppData\Local\Programs\Python\Python313\Scripts\uv.EXE` |
| CrewAI import | `FAIL` | `warn` | `import crewai` failed: No module named 'crewai' |
| Repo entrypoint import | `OK` | `info` | `idaho_vault.main` imports from the checkout-bound `src/` package. |
| Legacy installer helper | `OK` | `warn` | `install_dependencies.sh` clearly advertises its helper-only posture. |

## Scope Notes

- The canonical CrewAI bootstrap path remains checkout-bound and vault-local.
- `install_dependencies.sh` is a helper/reference surface, not the canonical truth surface.
- The live bootstrap contract is defined by `src/idaho_vault/bootstrap_contract.py`, `.crewai/MANIFEST.md`, `uv.lock`, and the vault launchers.
