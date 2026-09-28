---
title: CI Failure Sweep — 2026-08-07
type: audit
status: historical
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-08-06T05:45Z to 2026-08-07T05:48Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-07 (Retracted)

> **Correction, added after the fact-finding below was first written:** this sweep's core conclusion — that `pyproject.toml`'s reduction to a minimal stub was accidental corruption needing restoration — was wrong, and PR #935's proposed restoration has been retracted. #928 ("Delete tests/", open since 2026-08-05) deletes the whole `tests/` suite plus `python-test-suite.yml`/`codacy-coverage-reporter.yml`, because the tests were judged to pass without exercising what they claimed to cover; that thread already treated the minimal manifest as the deliberate current state in comments predating this sweep. #934 is Logan's own hand-edit on that same minimal state, adding back only `pytest`/`uv` — not the full dependency-groups/build-system/CrewAI runtime set this sweep restored. This PR therefore retains current main's minimal manifest, lockfile, and requirements export. The commit-tracing below remains as a historical record of what `a2766c40` changed and when; the inference that the change was unwanted, and the restoration proposed below, are retracted.

## 5W Summary

| | |
| --- | --- |
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`. Root-cause commit `a2766c40` carries the author trailer "Logan A. Finney"; not asserting who/what actually produced it beyond that metadata (see Incident A). |
| **What** | Pulled 30 workflow runs in the window: 21 branch runs, 5 PR #934/Copilot runs, 2 `audit/gitignore-836` runs, and 2 `main` runs. The original review recorded the run-level outcomes (failure, cancellation, or success) separately from GitHub's run-level rollup; the analysis below is retained only as a retracted historical record. |
| **When** | 2026-08-06T05:45Z – 2026-08-07T05:48Z. |
| **Where** | `main` itself (blocking, since the 05:48 merge of PR #933), the now-merged `claude/apply-patch-fixes-9gesn5` branch (ran red ~2 days before merging anyway), and the still-open `audit/gitignore-836` / PR #934 (inherited + compounded the same root cause). |
| **Why** | The original analysis attributed both incidents to `pyproject.toml` losing `[dependency-groups].dev`/`[build-system]`, which it concluded prevented `uv sync` from installing `pytest`/`coverage`. That evidence trail is retained historically, but the causal interpretation and proposed restoration are retracted; see the correction above. |
| **How** | Historical category analysis: the Code root-cause attribution and its claimed cascading downstream failures are retracted; the Transient observation remains that 2 job-level `cancelled` results were misreported as run-level `failure` due to concurrency-group supersession on rapid pushes, not a real defect. |

## Findings

### Incident A — historical dependency-restoration finding — **retracted; see correction above**

`main`'s **Python Test Suite** and **Codacy Coverage Reporter** failed on the push that merged PR #933 (runs [31151793960](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31151793960) / [31151793916](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31151793916), 2026-08-07T05:48Z): `error: Failed to spawn: pytest` / `coverage` — `No such file or directory`. `uv sync` was resolving only the `packaging` package.

Traced with `git log -S "Just like a .gitignore file" --all` (a distinctive marker string left in the broken file) to commit `a2766c40` (2026-08-04T00:12:37Z, author trailer "Logan A. Finney", **commit message that is literally just that trailer text and nothing else**): it replaced `pyproject.toml`'s `dependencies`, `[build-system]`, `[project.scripts]`, and the entire `[dependency-groups].dev` block (`pytest`, `coverage`, `ruff`, `jupytext`) with a 9-line stub — **twelve minutes after** `4bebc445` had just finished restoring the file from an *earlier, identical* incident ("restore pyproject.toml gutted by PR #891's merge-conflict resolution", `70b801a0`/`da3161fd`). The automated `sync-dependencies` workflow then faithfully propagated the stub into `uv.lock`/`requirements.txt` four minutes later (`01f3ac00`).

That commit lived on `claude/apply-patch-fixes-9gesn5`, which then ran red for the entire window this sweep covers before merging into `main` unfixed:

- `Python Test Suite` — same `uv sync` gap, 7× (runs 31075065811, 31075360652, 31075630564, 31075726694, 31076128695, 31106976965, 31107124623).
- `Codacy Coverage Reporter` — cascading from the above (`coverage.xml` never generated because the test step it depends on never ran): 31075065871, 31075360646, 31075630596, 31075726705, 31076128845, 31106977110, 31107124539.
- `check-notebooks-paired` — a *different-shaped* symptom of the exact same cause: its version-pin one-liner (`next(p['version'] for p in lock['package'] if p['name'] == 'jupytext')`) has no default, and with `jupytext` gone from `uv.lock` it raises unhandled `StopIteration` (31075065884, 31075360692, 31075630565, 31075726658, 31076128827, 31106979066, 31107124586).

This branch was red on every single push for ~2 days and merged into `main` anyway — worth a look at whether required-checks/branch-protection actually gates this repo's merges, separate from this fix.

**Original proposed fix — retracted:** PR #935 initially restored `pyproject.toml` and `uv.lock` from `4bebc445` and regenerated `requirements.txt`. The historical local verification recorded `558 passed, 2 failed` from `uv run pytest tests`; the two failures are described in Incident A-1. This proposed restoration has been removed, and PR #935 now retains current main's deliberate minimal dependency state.

#### Incident A-1 — two tests now visibly fail against Logan's deliberate `.gitignore` simplification — Configuration, needs a decision, not fixed here

During the original, now-retracted restoration, `tests/test_dotfolder_gitignore_policy.py::test_salvaged_secret_and_runtime_variants_are_ignored` and `tests/test_security_surface_quarantine.py::...test_unreviewed_bridge_session_and_launcher_surfaces_are_quarantined` failed. Both assert specific `.gitignore` patterns (`.mcp.json`, `session-export-*/`, `gpg-agent.conf`, various salvaged-secret path shapes) that `loganfinneyPTV` deliberately removed on 2026-08-03 (`3591a4bb`, "Simplify .gitignore: track by default, ignore only secrets and exhaust"). They were masked until now only because `main` couldn't run `pytest` at all. Not touched in PR #935 — reverting the `.gitignore` simplification or relaxing the tests is a policy call, not a side effect of a dependency fix.

### Incident B — `audit/gitignore-836` / PR #934 inherited Incident A's root cause and compounded it — Code, not fixed here (different branch's own history)

`audit/gitignore-836` merged `main` after `a2766c40` landed, then made it worse: `b40e72be` ("Update pyproject.toml") added `pytest`/`uv` back, but as plain runtime `dependencies`, not by restoring `[dependency-groups]`/`[build-system]`; `a673e0b2` ("Update uv.lock") then regenerated the lock from that still-malformed `pyproject.toml`, and the result **fails to parse** — `error: Failed to parse uv.lock ... missing field 'version'` (run [31148281336](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31148281336), 2026-08-07T04:43Z). Same root cause as Incident A, different branch, further along a bad path. Two other events on this branch/PR — `Code Quality: PR #934` and `Running Copilot Code Review` at 20:57–20:58Z — are job-level `cancelled` (confirmed via `list_workflow_jobs`, not `failure`; GitHub reported the run-level conclusion as `failure` but both jobs show `cancelled`, consistent with concurrency-group supersession from the next push landing ~15 minutes into the run). Not a real defect; miscategorized by the run-level rollup. This is a different branch's historical state and is not remediated here; any future work must be re-evaluated against current `main`, rather than restoring the dependency model retracted above.

## Big IF

- **The original analysis described this as the same file being gutted for a third time** (PR #891's merge-conflict resolution → restoration; `a2766c40` twelve minutes after that restoration → this PR's now-retracted proposed restoration; `audit/gitignore-836` inheriting and compounding it a third time). That interpretation is historical, not a basis for restoring prior dependency sections. Any future guard would need a separately approved invariant for the deliberate minimal model, rather than treating `[dependency-groups]`, `[build-system]`, or `[project.scripts]` as required.
- **A branch ran red for ~2 days on the exact tests this repo had added to catch dependency regressions, and merged into `main` anyway.** Whether that reflects required-check configuration or a merge past a known-red state is worth Logan's attention separately from this retracted analysis; this PR does not restore the prior dependency model or alter merge gating.
- **The commit that caused the regression has a broken commit message** (literally just the `Author:` git trailer, nothing else) — consistent with a mechanical slip (bad `git checkout <old-sha> -- pyproject.toml`, a script that mis-templated its commit message, or similar) rather than a deliberate edit. Not asserting more than the metadata shows; flagging because "confident output with no valid emanation chain" is exactly the failure this sweep exists to catch, and I'd rather name the gap than guess at intent.

---
This historical analysis and its proposed dependency restoration are retracted in PR #935.
