---
title: pyproject.toml Dependency Provenance — 2026-08-04
type: audit
status: draft
updated: 2026-08-04
authority: LOGAN
authors:
- Claude Code (measurement only; no change to pyproject.toml proposed or made)
scope: pyproject.toml dependency and config sections, src/idaho_vault/, LAF-US/IDAHO-VAULT
owner: Logan Finney
---

# pyproject.toml Dependency Provenance — 2026-08-04

## Why this exists

`pyproject.toml` was trimmed to a stub, with the stated reason: *"I trimmed
everything, intentionally. I don't trust that any of that was actually required
beyond sloth and pride."*

That is a testable claim, so it was tested. This note records the result. It
proposes nothing and changes nothing — `pyproject.toml` is untouched by the PR
carrying this file. Logan's ruling was **evidence only, restore nothing**.

## 5W Summary

| | |
| --- | --- |
| **Who** | Measured by Claude Code session `015oRnkWnNkTL7R2umjen42b`. Two errors in the measurement were caught by reviewers (Copilot, Qodo) and are recorded below rather than quietly fixed. |
| **What** | Every section removed from `pyproject.toml`, classified by what actually depends on it: the `.github/` automation, the `src/idaho_vault/` scaffold, or nothing but a self-asserting artifact. |
| **When** | 2026-08-04, against `main` at `5a1b7fbd`. |
| **Where** | `pyproject.toml`, `uv.lock`, `src/idaho_vault/**`, `.github/scripts/**`, `tests/**`. |
| **Why** | Three PRs in one night restored, re-removed, and re-restored the same content. The disagreement was never about the file — it was about which parts anything actually needs. |
| **How** | Import analysis, CLI-invocation analysis, dependency re-resolution, and running the suite against progressively larger configurations. Commands and outputs below. |

## Finding A — Load-bearing for the `.github/` automation

| Item | Evidence |
| --- | --- |
| `pytest`, `coverage` | `uv sync` on the stub resolves 2 packages and installs `packaging`; pytest is absent, so `test` and `coverage` cannot run |
| `pygit2` | imported by `.github/scripts/sync_obsidian_plugin_registry.py` |
| `jupytext` | **not imported** — `.github/scripts/jupytext_sync_paired.py` invokes `jupytext --sync` via `subprocess`; `check-notebooks-paired.yml` runs that script and `tests/test_helper_scripts.py` covers it |
| `pyyaml`, `openpyxl` | imported across `tests/` and `.github/scripts/` |
| `requires-python` | absent, uv warns `No requires-python value found` and defaults to `>=3.13`, which drops the 3.10 half of the `smoke` matrix |
| `[tool.pytest.ini_options] pythonpath` | test modules load the CI scripts by file path and cannot resolve `gh_cli` without it |

## Finding B — Load-bearing only for `src/idaho_vault/`

`crewai`, `flask`, `pydantic`, `[build-system]`, `[tool.hatch.build.targets.wheel]`.

Measured by re-resolving with the three runtime deps removed:

```
uv.lock with    crewai/flask/pydantic:  165 packages
uv.lock without crewai/flask/pydantic:   54 packages
```

**111 of 165 packages — 67% of the dependency tree — exist for that scaffold.**
That is what pulls in `tokenizers`, `uvicorn`, `starlette`, `websockets`,
`textual`, and the `huggingface-hub` that Finding C's frozen count then pins.

What the scaffold is, by measurement:

- **No workflow invokes it.** Zero references across `.github/workflows/`.
- **It never reaches a real LLM.** `src/idaho_vault/crew.py:8` —
  `from idaho_vault.mock_llm import StaticValidationLLM`.
- **5 of 42 test files** import it.
- Outside the package, `crewai`/`flask`/`pydantic` are imported only by root
  `main.py` and two `src-idaho_vault-*` NETWEB path-aliases — copies of itself.

## Finding C — Required by nothing but a self-asserting artifact

Zero imports **and** zero CLI invocations anywhere for `huggingface-hub`,
`requests-oauthlib`, `honcho-ai`, `ruff`, and `packaging`.

They are present because `tests/test_uv_dependency_submission.py` hardcodes:

```python
self.assertEqual(len(self.resolved), 164)
```

and separately asserts `ruff` appears in the resolved set.

`[tool.crewai]` and `[project.scripts]` are present because `_check_pyproject`
in `src/idaho_vault/bootstrap_contract.py` greps this file for literal strings:

```python
required_tokens = (
    'name = "idaho-vault"',
    'type = "crew"',                            # [tool.crewai]
    'idaho_vault = "idaho_vault.main:run"',     # [project.scripts]
)
```

Both artifacts live **inside** `src/idaho_vault/` — the scaffold asserts
requirements about the project that exists to host the scaffold, verified by
tests that import the scaffold.

Drop everything in this finding and the suite fails **5 tests in exactly 2
files**: `test_uv_dependency_submission.py`, and the two `threshold_runner`
tests that call `build_contract_report_for_root`. No import breaks. No behavior
changes.

The frozen `164` has a specific failure mode worth naming: it must be
hand-edited by anyone who legitimately adds or removes a dependency, so it only
ever fires on the person doing real work.

## Finding D — `[project.scripts]` is latently broken

`src/idaho_vault/main.py`:

```python
def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
```

`_require_checkout` then demands `AGENTS.md` and `CONSTITUTION.md` under that
path, so a non-editable wheel install would compute a root inside
`site-packages` and exit immediately. Raised by Qodo; verified as **latent, not
active** — `uv sync` installs the workspace root editable, so `__file__` stays in
the checkout:

```
$ .venv/bin/python -c "import idaho_vault; print(idaho_vault.__file__)"
/home/user/IDAHO-VAULT/src/idaho_vault/__init__.py
computed repo root: /home/user/IDAHO-VAULT   AGENTS.md: True   CONSTITUTION.md: True
```

So the one `[project.scripts]` entry a string-grep keeps alive is also the one
that would ship broken if the package were ever installed normally.

## Measurement log

```
stub as-is                                     pytest not installed at all
+ genuinely-imported deps, build-system, dev   538 passed, 5 failed
+ [tool.crewai], [project.scripts], ruff, huggingface-hub
                                               541 passed, 2 failed
+ requests-oauthlib, honcho-ai, jupytext       543 passed, 59 subtests
```

## Corrections to this audit's own method

Recorded because the method's blind spots matter more than its conclusions.

1. **An import-only audit undercuts.** The first pass classified `jupytext` as
   unused on the strength of `git grep` for `import`. It is genuinely used, via
   `subprocess`. Caught by Copilot in review. `ruff` survives the correction;
   the error was lumping the two together. Finding C's remaining entries were
   re-checked for CLI invocation before classification.
2. **A failing test is not proof of a requirement.** The first pass cited
   `bootstrap_contract.py` and `test_uv_dependency_submission.py` as evidence
   that sections were *required*. Both are agent-authored assertions living
   inside the very subsystem whose necessity was in question. Conformance to a
   self-asserting artifact was mistaken for a functional need.
3. **`author:` is not provenance.** Two commits in this history are authored by
   `Logan A. Finney <136375980+loganfinney27@users.noreply.github.com>` with
   `committer: GitHub`. That is the same account agents act under; PR comments
   written by this session appear under it too. Intent stated by Logan directly
   in conversation is grounded; intent inferred from a commit author field is
   not. Per `.claude/CLAUDE.md`: the name identifies the account, only the
   session id identifies the run.

## Consequence of restoring nothing

While `pyproject.toml` is a stub, `test` and `coverage` fail on **every** PR in
the repository, because a bare `uv sync` — which is what the workflows run, not
`--frozen` — resolves 2 packages and `pytest` is not among them. Recorded as an
accepted cost of the ruling, not as an outstanding defect.

## See also

- `!/AUDIT-CI-FAILURE-SWEEP-2026-08-03.md` — the sweep series this sits beside
- PR #904 (merged), #916 (merged), #905 — the restore / re-remove / measure cycle
