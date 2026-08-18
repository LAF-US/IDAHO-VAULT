---
title: CI Failure Sweep — 2026-08-12
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, LAF-US/IDAHO-VAULT, 2026-08-10T19:39:33Z to 2026-08-12T19:39:33Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-12

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `LAF-US/IDAHO-VAULT`. `loganfinney27` (agent-driven pushes) and `github-merge-queue[bot]` account for nearly all triggering actors; no new human-caused breakage. |
| **What** | 273 workflow runs concluded `failure` in the window. Swept by `list_workflow_runs(status=failure)`, paginated back to the 48h cutoff, then verified with `get_workflow_jobs`/job-log pulls per distinct category rather than trusting the run-count alone. 213 of the 273 (78%) turned out to be one non-blocking artifact, not 213 separate problems — confirmed by pulling a live PR's actual check-runs list and finding it absent. Six real, distinct categories remain; two are already fixed in an open PR from another live session. |
| **When** | 2026-08-10T19:39:33Z – 2026-08-12T19:39:33Z. |
| **Where** | Dominant volume on `claude/apply-patch-fixes-9gesn5` (PR #962, actively iterating), `claude/looker-attestation-wording-qzt7le`, `claude/shall-rome-lyrics-ok9049`; a handful of one-offs on `main`, PR #572, PR #940, PR #885, PR #837/#503. Zero runs verified as an actual PR-blocking gate. |
| **Why** | Per-incident root cause below, each backed by a quoted log excerpt or a direct API check — not inferred from pattern-matching. |
| **How** | Category breakdown: Non-blocking artifact (1 incident, 213 runs), Code — already fixed elsewhere (2 incidents, 34 runs), Code — unaddressed (2 incidents, 17 runs), Infra/transient (1 incident, 6 runs), External service (1 incident, 1 run), Content debt (1 incident, 1 run). |

## Findings

### Incident A — `agent-swarm-signing-proof.yml` "failure" on every push — Non-blocking artifact, verified

213 runs (78% of the window's total), all `conclusion: failure`, 0 jobs, 0s duration, since 2026-08-10T23:56Z (when PR #471 merged the refactor splitting this file into a `workflow_call`-only reusable target for the 4 dispatch-only App-signing-lane wrappers tracked in issue #398). A plain `push` has no matching trigger for a `workflow_call`-only file, yet the Actions run list records a failure for it anyway.

Verified, not assumed: `get_workflow_jobs` on every sampled run returns `{"jobs":{"total_count":0}}`; `get_workflow_run_logs_url` 404s; and — the check that actually settles it — `pull_request_read get_check_runs` on PR #962's head commit lists all 17 real checks on that commit, and this workflow is not among them. It is not a required check, not even a visible one. `github-merge-queue[bot]` is the actor on 47 of the 213 entries, but PR #471 (which introduced the refactor) merged cleanly through that same queue. Not blocking anything. Commented on issue #398 with this finding rather than opening a new issue, since it's directly relevant to that issue's own App-signing design.

### Incident B — Codacy Security Scan: SARIF upload rejects null `tool.driver.rules` — Code, already fixed (PR #962)

19 runs, 2026-08-11T22:52Z – 2026-08-12T18:46Z, mostly `claude/looker-attestation-wording-qzt7le` and `main`. Codacy's SARIF export emits `"rules": null` when a tool component carries no rule metadata; the SARIF schema requires an array, so `upload-sarif` rejects the whole document:

> `##[error]Unable to upload "results-normalised.sarif" as it is not valid SARIF: - instance.runs[0].tool.driver.rules is not of a type(s) array` (run 31629240677)

PR #962 §2 (open, another live Claude Code session, `session_015oRnkWnNkTL7R2umjen42b`) drops the null `rules`/`extensions` keys before upload. Not duplicated here.

### Incident C — Check Dotfolder Anchors: `.codacy/` missing its anchor — Configuration, already fixed (PR #962)

15 runs, same window, same branches. `.codacy/` landed on `main` (commit `3d617a3d`) without its required `<NAME>.md` anchor per `STUB-PERSONAFOLDERS-2026-05-03.md`, so the guard fails on `main` itself and everything built from it:

> `dotfolder-anchor guard: dotfolders missing their <NAME>.md anchor: - .codacy/CODACY.md` (run 31629240667)

PR #962 §4 adds `.codacy/CODACY.md`, byte-identical to the established `.github/GITHUB.md` stub shape. Not duplicated here.

### Incident D — Secret Pattern Policy: recurring false positive on vendored plugin bundles — Code, unaddressed, fix proposed (issue #967)

16 runs, mostly `claude/shall-rome-lyrics-ok9049` (12). The guard trips `generic_secret_assignment` on the same 3 lines inside vendored, minified third-party Obsidian plugin bundles every time a branch touches or rebases over them:

> `.obsidian/plugins/obsidian-local-rest-api/main.js:58166 [generic_secret_assignment]`
> `.obsidian/plugins/smart-connections/main.js:2838 [generic_secret_assignment]`
> `.obsidian/plugins/smart-connections/main.js:16766 [generic_secret_assignment]`
> (run 31544229800)

`.codacy.yaml` already excludes `.obsidian/plugins/*/main.js` from Codacy's own scan; `check_secret_patterns.py` has not adopted the same exclusion. Looked at implementing this directly during the sweep — `check_secret_patterns.py`'s content-match allowance logic (`is_allowed_content_match` / `_chain_allowance_applies`) is a carefully fenced, five-condition, span-tied piece of security logic with its own extensive design rationale in the source comments. Hand-editing it under sweep time pressure, without a paired regression test, is exactly the kind of rushed change that logic is designed to resist. Filed as GitHub issue #967 with full reproduction instead of patching it live.

### Incident E — Cross-workflow TLS/certificate verification failures against github.com — Infra, unaddressed, root cause not isolated

6 runs across 3 unrelated workflows. `review_feedback_loop.py`'s `acknowledge_apply` step and `pr_lifecycle.py`'s branch-cleanup step both fail at the identical call site (`gh_cli.py`'s `_run()` wrapping `gh label create`):

> `Post "https://api.github.com/repos/LAF-US/IDAHO-VAULT/labels": tls: failed to verify certificate: x509: certificate is not valid for any names, but wanted to match api.github.com` (runs 31544233793, 31558145426)

CodeQL's "Analyze (python)" job on PR #572 hit the git-level equivalent, 3/3 retries exhausted:

> `fatal: unable to access 'https://github.com/LAF-US/IDAHO-VAULT/': server certificate verification failed. CAfile: none CRLfile: none` (run 31528575045)

Each instance looks like runner-side network flake in isolation; recurring 3 times across unrelated code paths in one 48h window is what makes it worth naming rather than dismissing per-incident. No vault-side fix identified — flagging for Logan in case it recurs and warrants a GitHub Support report.

### Incident F — Codacy Coverage Reporter assumes a `tests/` directory exists — Configuration, unaddressed, fix proposed (issue #967)

1 run, PR #940 (`claude/practical-cerf-pc0mw5`). `uv run coverage run -m pytest tests -v` is unconditional:

> `ERROR: file or directory not found: tests` → `##[error]Process completed with exit code 4.` (run 31535568798, job `coverage`)

That branch simply has no `tests/` directory. Narrow, single occurrence this window, but will recur on any future content-only PR. Filed alongside Incident D in issue #967 rather than patched live, for the same reason: a workflow-behavior change deserves its own small PR and verification, not a drive-by edit bundled into an audit report.

### Incident G — Two single-occurrence items, not investigated further

- Redaction Damage Policy (run 31453333787, `claude/lint-config-stubs-qzt7le`): flagged an added line in `eslint.config.js:33` as matching the marker-glued-to-letters shape tracked in issue #739. The cited source line was inspected and contains a normal prose comment with no visible redaction marker; record this as a likely policy false positive under existing issue #739 rather than an untracked new incident.
- Running Copilot Code Review (run 31565802005, PR #885): GitHub Copilot's own `sweagentd` backend timed out reporting results — `TimeoutError: The operation was aborted due to timeout`. External Copilot-service-side flake, no vault-side action possible.

Also noted but not counted as a failure: Validate Agent Content (run 31457472663, `agent/adr-canon-core-portability`) flagged ~15 pre-existing files (oversized files, old tweet-archive false positives, malformed frontmatter) unrelated to that branch's own diff — repo-wide backlog debt, not this branch's fault.

## Big IF

- **The 213-run dominant category would have looked like the sweep's headline finding if the check-runs cross-reference hadn't been pulled.** Run-count alone said "agent-swarm-signing-proof.yml is 78% of all CI failures, urgent." Actually checking whether it appears on a live PR's real checks said "it doesn't gate anything." Both facts are true; only the second one tells Logan what to do about it (nothing, low-priority cleanup). Worth keeping as a standing habit for future sweeps: a high run-count is a lead, not a verdict, until checked against what actually gates a merge.
- **This sweep found two categories already fixed in-flight (PR #962) and confirmed it before writing anything new** — avoided duplicating Incidents B and C. Cheap to check (`get_check_runs` + reading the open PR's own description), and it's the difference between a sweep that adds signal and one that adds noise to an already-open PR's diff.
- **The audit-PR pile is the known risk here, and this sweep chose not to grow it silently.** Per the 2026-08-03 sweep's own Big IF, only 3 of the daily sweep PRs opened since 2026-07-08 have ever merged to `main`; most sit open. This sweep's own PR is documentation-only (zero workflow/script changes) specifically so it's trivial to merge — and the two real, fixable findings (Incidents D and F) were deliberately routed to a single new tracking issue (#967) rather than a second report-shaped PR, so the backlog gets one small actionable item instead of one more audit artifact.

---
Cross-posted: GitHub issue #398 (comment, Incident A), GitHub issue #967 (new, Incidents D + F), Linear LAF-78, Slack #all-logan-finney, Discord #ledger (via Zapier).
