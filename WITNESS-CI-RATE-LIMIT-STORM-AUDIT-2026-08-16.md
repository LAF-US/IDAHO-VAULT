---
title: "Witness — 48h CI failure audit: review-bot rate-limit storm (2026-08-16)"
created: 2026-08-16
updated: 2026-08-16
status: active
authority: LOGAN
doc_class: witness
authors:
  - Claude Code — session_01LTD66ZEF1tduSVnbvcR6H7
related:
  - CONSTITUTION
  - VAULT-CONVENTIONS
tags:
  - witness
  - ci
  - github-actions
  - rate-limit
  - review-bots
  - test-infrastructure
---

# Witness — 48h CI failure audit: review-bot rate-limit storm

Scheduled routine audit of `LAF-US/IDAHO-VAULT` GitHub Actions failures over the prior
48 hours, per Logan's standing scheduled task. This note anchors the durable record;
the live GitHub Issue carries the coordination thread.

**Scope note on verification:** GitHub's Actions API returned `total_count: 3597` for
all-time `status=failure` runs and would not honor `per_page` beyond 30 rows per call
through the MCP tool available this session. Findings below are built from ~8 sampled
pages (≈240 runs) spanning 2026-08-12 through 2026-08-16T17:10Z, plus direct job-log
reads for representative runs in each category, plus a direct read of the triggering
workflow and script source. This is a sampled, not exhaustive, count — stated as such
rather than implied as a full census.

## 5W Summary

| | Finding |
|---|---|
| **Who** | ~15–20 third-party AI review-bot GitHub Apps installed on the repo (`tenki-reviewer`, `cr-gpt`, `hyrax-ai`, `precogs-ai`, `codereviewbot-ai`, `codacy-production`, `revieko-architecture-drift-radar`, `insight-code-accessibility`, `railo-dev`, `blue-cave-toolbox`, `pr-insights-tagger`, `ai-code-reviewr`, `codelens-ai`, `rams-design-review`, `haiec-compliance`, others); `.github/scripts/review_feedback_loop.py`'s `acknowledge-apply` job; `Codacy Security Scan`; CodeQL `Code Quality` checks; PR author `loganfinney27` |
| **What** | (1) A live GitHub-API rate-limit storm: `Review Feedback Loop` failing on effectively every run, taking `Codacy Security Scan` SARIF upload and CodeQL `Code Quality` checks down with it as collateral damage on PR #950 and #962. (2) A high volume of *apparent* `Agent Swarm Signing Proof` failures in the Actions run list — already diagnosed as a non-blocking artifact, not a live problem (see correction below). |
| **When** | Storm actively firing 2026-08-16T16:42Z–17:10Z+ UTC (still live at last sample — every 2–9 seconds). |
| **Where** | `.github/workflows/review-feedback-loop.yml` (`acknowledge-copilot-apply` job) → `.github/scripts/review_feedback_loop.py`; `.github/workflows/codacy.yml`; CodeQL quality workflow |
| **Why** | See root-cause chain below. |
| **How (next step)** | Fixed this session: reordered `ensure_labels()` in `acknowledge_apply()` so it only runs on the actual label-mutation path, not on every incoming comment. See fix + regression tests below. Recommend Logan review whether all ~15–20 review-bot Apps need to stay installed (org-level call, out of this session's scope). |

## Root cause (verified from job logs, not inferred)

1. Every commit pushed to an open PR (today: #962, #950) causes all ~15–20 installed
   review-bot GitHub Apps to post a comment within the same second. Several are
   themselves broken/unfunded: `tenki-reviewer` — *"Insufficient balance to process
   this code review"*; `cr-gpt` — missing `OPENAI_API_KEY`; `codelens-ai` — pinned to
   a deprecated Gemini model (`gemini-2.0-flash` no longer available); `codereviewbot-ai`
   — past its free-tier cap ("2 reviews per 4 hours").
2. `.github/workflows/review-feedback-loop.yml`'s `acknowledge-copilot-apply` job has
   **no filter** on comment author or content — it fires on every `issue_comment` on
   every PR, bot noise included.
3. **The actual bug:** `review_feedback_loop.py::acknowledge_apply()` called
   `ensure_labels()` — a sweep of 5 `gh label create --force` calls plus a
   `gh label delete` — **unconditionally, before** checking whether the comment even
   matched an `@copilot apply changes` request. Every one of the 15–20 bot comments
   per push was therefore paying for 6 GitHub API calls plus a full checkout
   (38,497 files) it never needed.
4. That burst of near-simultaneous, mostly-wasted API calls exhausted the shared
   GitHub App installation's rate limit: `HTTP 403: API rate limit exceeded for
   installation`.
5. Because the token pool is shared per-installation, the same exhaustion broke
   **unrelated** concurrent jobs: `Codacy Security Scan`'s SARIF upload step and
   CodeQL's `Code Quality` status-reporting step, both failing with the identical
   `API rate limit exceeded for installation` error in the same windows, on both
   PR #950 and #962.
6. Self-sustaining: confirmed still active at 17:10:17Z (the last data point pulled
   during this audit), roughly one `Review Feedback Loop` failure every 2–9 seconds.

## Fix applied this session

`.github/scripts/review_feedback_loop.py` — moved `ensure_labels()` inside the
`if DEFAULT_PENDING_LABEL not in labels:` branch of `acknowledge_apply()`, so it only
runs on the path that actually adds the label, not on every incoming comment. Four
regression tests added to `tests-test_review_feedback_loop.py` covering: non-apply
comments, untrusted authors, and the already-labeled idempotent case all skip
`ensure_labels()`/`pr_view` entirely; the genuine trusted-apply path still calls it.
All four pass.

This does not touch which review-bot Apps are installed or how many run per push —
that's an org-level judgment call for Logan, not something this session assumed
standing to decide. It stops the vault's *own* automation from amplifying the bot
noise into an API-rate-limit outage for unrelated CI.

## Secondary finding: the vault's Python test suite has never run

Fixing the fix required actually running `tests-test_review_feedback_loop.py`, which
surfaced that **none of the ten `tests-test_*.py` files at repo root have ever
successfully executed**, for three independent, stacked reasons — verified directly,
not inferred:

1. `conftest.py`'s `pytest_ignore_collect` hook excluded everything at repo root
   except the (empty) `tests/` directory. Running bare `pytest` from repo root
   collected **zero** tests. Fixed: the hook now also allows root-level
   `tests-test_*.py` files, matching the convention all ten files actually use.
2. Every one of the ten files computed its own path as
   `Path(__file__).resolve().parents[1]`, which is correct only if the file lives one
   directory *below* repo root — but all ten live *at* repo root. Fixed uniformly
   (`parents[1]` → `parents[0]`) across all ten.
3. `tests-test_review_feedback_loop.py` additionally never added `.github/scripts/`
   to `sys.path`, so the module's own `import gh_cli` / `from pr_threads import ...`
   failed. Fixed, following the existing working pattern already used in
   `tests-test_stale_bot_prs.py`.
4. **No CI workflow invokes `pytest` at all** — confirmed by grep across
   `.github/workflows/*.yml`. Not changed this session (adding a new required CI
   check is an architecture decision with real blast radius; flagging for Logan
   rather than deciding it unilaterally).

With collection actually working, `tests-test_review_feedback_loop.py` now shows
**4 pre-existing, unrelated failures** (stale assertions in `evaluate_review_state`
tests, and a reference to `_resolve_outdated_advisory_threads`, which no longer
exists under that name) — left **as found**, not silently "fixed" by guessing at
current intended behavior. The other 9 files were fixed only for the identical
path/collection bug; four of them (`tests-test_five_wizards.py`,
`tests-test_sparkseed.py`, `tests-test_runtime_doc_tools.py`,
`tests-test_validate_bootstrap.py`) still fail to collect on unrelated missing-module
errors (`idaho_vault.five_wizards`, `idaho_vault.sparkseed`,
`scripts/health_monitor.py`, `scripts/validate_bootstrap.py` not found at the paths
they import from). These are real, separate gaps — not fixed here, named honestly
as follow-up rather than left implicit.

## Second correction: the collection fix was incomplete

The original fix above (conftest.py's `pytest_ignore_collect` allowing
`tests-test_*.py` at root) was necessary but not sufficient, and this session's
own verification never caught it: every check after that fix used an explicit
filename (`pytest tests-test_review_feedback_loop.py`), never a bare `pytest`
invocation with no file arguments. `pytest_ignore_collect` only governs whether
a *path* is visited at all — pytest still applies its own `python_files` glob
(default `test_*.py`/`*_test.py`) to decide which files within an allowed path
actually become test modules. `tests-test_*.py` matches neither default
pattern, so bare `pytest` still collected **zero tests**, silently, even after
the "fix." Caught only because rebasing this PR onto `main` after several days
picked up a genuinely new root-level test file (`test_doctrinal_flatten.py`,
added by unrelated work on `main`) — bare `pytest` failed to find *that* file
either, which is what prompted checking bare invocation directly for the first
time.

Fixed properly this time, verified end-to-end rather than by explicit filename:
added `[tool.pytest.ini_options] python_files = ["test_*.py", "tests-test_*.py"]`
to `pyproject.toml`, and widened the `conftest.py` hook to allow both prefixes
(not just `tests-test_`) at root. `pytest` with no arguments now collects 32
tests directly.

That also means the earlier "4 pre-existing failures" count was an
undercount — it only reflected `tests-test_review_feedback_loop.py`, the one
file this session had actually run in full. Running the whole suite for the
first time surfaces **12 pre-existing failures** across five files
(`tests-test_review_feedback_loop.py`, `tests-test_helper_scripts.py`,
`tests-test_phone_link_intake.py`, `tests-test_stale_bot_prs.py`,
`tests-test_validate_content.py`) plus the 4 collection errors already
documented above. Same disposition as before: left as found, not silently
patched by guessing at current intended behavior, since none of these
functions were touched by this session's actual fix and diagnosing each one
correctly needs more context than a CI-audit session should assume it has.

## Correction: Agent Swarm Signing Proof is not a live problem

An earlier draft of this note (and the first-posted PR comment) flagged the volume of
`Agent Swarm Signing Proof` red X's in the Actions run list as a second, separate
chronic failure needing investigation. That was wrong, and it was already wrong to
ask before checking: Linear issue **LAF-78** (`CI failure sweep 2026-08-12`, filed by
a prior scheduled-audit session four days before this one) already diagnosed this
exact pattern. `agent-swarm-signing-proof.yml` is `workflow_call`-only — its real
triggers are the 4 dispatch-only wrapper workflows per issue #398's App-signing
design — and cannot itself be triggered by `push`. It nonetheless shows `failure` in
the Actions run list on every push, with **0 jobs and a 404 logs URL** (confirmed
independently in this session: `get_job_logs` on one of these runs returned
`total_jobs: 0`, matching LAF-78's finding exactly). LAF-78 confirmed non-blocking by
cross-referencing a live PR's actual check-runs list — the workflow isn't on it — and
commented the finding on GitHub issue #398.

Issue #398 itself is real, large, and still open — a multi-month design effort for
agent-identity-bound commit signing, not a CI-monitoring matter. That work continues
on its own track and is untouched by this session. What's corrected here is narrower:
the *Actions-run-list red X's* for this one workflow are a known, non-blocking
artifact, not a fresh finding this audit needed to raise.

## Addendum (2026-08-18): the storm recurred on this PR, from a different source

On 2026-08-18T11:00–11:03Z, PR #984 (this fix's own PR) hit the identical
`##[error]API rate limit exceeded for installation.` error on four check runs at
head `ab7214e4d8895356e095398fbde491b1c4fd6472`: `Codacy Security Scan`,
`Analyze (python)` ×2, `Analyze (javascript-typescript)`, `Analyze (actions)` —
verified directly from job logs (jobs `95687636588`, `95687627766`, and their
duplicates from a parallel CodeQL run). `acknowledge-copilot-apply` shows
`skipped` on this run, confirming this session's fix is working — the vault's
own script is no longer contributing to the exhaustion. The recurrence traces
to a different source: **the number of installed third-party review-bot Apps
has grown since 2026-08-16, not shrunk.** This single PR run shows ~30 distinct
bot/check names active within the same ~90-second window (Repowise, CircleCI,
DeepScan, GitGuardian, Corgea, Aikido, secuarden, CodeRifts ×2, Sieve,
guardrails, Blue Cave, dpulls, CodeFactor, cubic, Graphite, gitStream, Sourcery,
mergefreeze, frost, CommitCheck, CodeRabbit, PRLintReloaded, Hound, Revieko,
pre-commit.ci, semgrep-cloud-platform, plus the vault's own checks), versus the
~15–20 named on 2026-08-16. This confirms the root-cause chain's step 1 (bot
volume) as the live, ongoing driver, independent of step 3 (this vault's own
script, now fixed). The disposition — how many of these Apps stay installed —
remains an org-level call for Logan, as originally flagged; this session does
not have standing to uninstall GitHub Apps. Posted to PR #984:
https://github.com/LAF-US/IDAHO-VAULT/pull/984#issuecomment-5327821256

## Addendum (2026-08-18): a NETWEB violation actually breaks Windows CI, not just warns

The same PR #984 run's `smoke (windows-latest, 3.10)` and
`smoke (windows-latest, 3.13)` jobs both failed at checkout, before any test
code ran:

```
##[error]error: invalid path '"consistent with" ≠ evidence.md'
```

That file lives at the repo root on `main` (unrelated to PR #984's diff) and
contains literal double-quote characters — already listed in `ILLEGAL_CHARS` in
`.github/scripts/check_portable_paths.py`. The NETWEB gate (`check-portable-paths.yml`)
deliberately only *warns* on tracked paths that predate a PR, never fails them
(`VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)"), so this violation
has been sitting as a report-only warning on every PR without ever being
confirmed to cause an actual failure — until now. Per `VAULT-CONVENTIONS.md`
line 762, `smoke (windows-latest)` is a non-required check and gates neither
queue entry nor merge, so this is not blocking. Per `GIT-CONTROL-SURFACES-2026-05-17`,
renaming a tracked path is a destructive git-control-surface change requiring
Logan's explicit instruction — flagged here for his disposition, not acted on
by this session.

## Provenance

Compiled by Claude Code, session `session_01LTD66ZEF1tduSVnbvcR6H7`, from direct
`mcp__github__actions_list` / `get_job_logs` / `pull_request_read` reads and direct
repository file reads on 2026-08-16 (original) and 2026-08-18 (addenda). Where a
number above is a sample rather than a census, it is stated as one.
