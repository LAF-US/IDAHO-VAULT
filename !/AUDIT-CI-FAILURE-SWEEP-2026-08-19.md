---
title: CI Failure Sweep — 2026-08-19
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, nominal window 2026-08-17T17:05Z–2026-08-19T17:05Z (48h); actual verified coverage narrower — see How
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-19

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (72 workflows per `list_workflows`). All confirmed failures trace to pushes on **stale, long-abandoned agent branches** — not to `main`, and not to any workflow file as it currently exists on `main`. |
| **What** | A single systemic cause, confirmed via two direct job-log quotes: GitHub's platform-level policy *"actions must be pinned to a full-length commit SHA"* is now being enforced, and it hard-rejects the `Set up job` step (before any user script runs — 0 real work attempted) on any branch whose **own copy** of a `.github/workflows/*.yml` file still references an action by tag (`@v4`, `@v6`, `@main`) instead of a SHA. `main`'s current workflow files are **already 100% SHA-pinned** (verified: `grep` across all 53 `.github/workflows/*.yml` files on `main`/this branch found zero unpinned `uses:` lines) — this is not a `main` regression. It is old branches carrying old, pre-pinning copies of these files. |
| **When** | All 68 `failure` + 3 `cancelled` runs found in-window cluster inside one ~60-second burst, **2026-08-19T15:27:52Z–15:28:52Z**, triggered by `loganfinney27` (actor on every sampled run) pushing/merging across many branches near-simultaneously. Before and after that burst, the sampled minutes were clean (`success`/`skipped` only). |
| **Where** | Confirmed on: `claude/resolve-pr-conflicts` (branch's last real commit: **2026-03-30** — carries `actions/checkout@v6` unpinned, verified by direct `git show` of that ref), plus `dependabot/uv/uv-aa7cb66ac2` (`actions/checkout@v4` + `actions/setup-python@v6` unpinned) and ~20 other `codex/*`, `claude/*`, `bot/daily-rollover-*`, `dependabot/*` branches, all old. **Zero failures on `main` itself in the sampled window.** Not a required check on `main`; does not block merges. |
| **Why** | The affected branches predate whatever point `main` finished its own SHA-pinning migration (already complete, per the zero-unpinned grep above) and were never rebased since. GitHub evaluates a `push`-triggered workflow using the **pushed branch's own copy** of the workflow file, not `main`'s — so these branches keep re-triggering the now-enforced policy every time anything touches them, independent of `main`'s health. |
| **How** | Root-caused via direct job-log text (not inference) on two runs: `##[error]The action actions/checkout@v6 is not allowed in LAF-US/IDAHO-VAULT because all actions must be pinned to a full-length commit SHA.` (job 96124816333) and the same message naming `checkout@v4`/`setup-python@v6` (job 96124692702). Confirmed against `main`'s actual file contents (`git show`/`grep`, not recalled). Confirmed `claude/resolve-pr-conflicts`'s branch-tip commit predates any pinning fix (`git log`, `git show <ref>:.github/workflows/auto-pr.yml`). **Coverage caveat, stated plainly rather than implied away:** this repo's `list_workflow_runs` `total_count` and page contents are unstable at this write-throughput (a background sub-agent hit its 20-page cap after covering only ~72 minutes of the 48h window before pagination started returning non-adjacent time ranges — the same instability the 2026-08-12 sweep documented). I supplemented with direct, `workflow_id`-scoped pagination (`auto-pr.yml` specifically, 483 total runs — a tractable number) reaching back to 2026-03-21, which found **zero** occurrences of this SHA-pin failure signature before today's burst, giving reasonable confidence this is a real, bounded, recent event and not something already smeared across the full 48h that a partial sample simply missed. I cannot rule out an unrelated failure elsewhere in the ~46 hours I did not directly sample; none surfaced in any spot-check. |

## Findings

### Incident A — platform SHA-pin enforcement rejecting stale branches' own workflow copies — Confirmed, not code-fixable from `main`

`main` requires no fix; it is already clean. The affected branches are stale (`claude/resolve-pr-conflicts` untouched since 2026-03-30) and this sweep does not rewrite other agents'/branches' history unilaterally — several of the affected branches (`codex/linear-mention-*`, `copilot/*`) appear to be other agents' active or recently-active work, and per CONSTITUTION § I ("Offices are appointments, not inheritances") and § V ("No unauthorized restructuring"), force-editing another lineage's branch is out of scope for a CI sweep. **Next step, for Logan:** this repo already runs `Branch Cleanup` and `Stale Bot PR Cleanup` workflows built for exactly this situation (pruning/rebasing long-abandoned agent branches); letting those run, or a manual prune of branches dead since March/April, resolves this at the root without touching any live agent's work. No `main`-blocking impact today.

### Zero failures found on `main` itself in-window; nothing found blocking merges to `main`.

### Gap in the sweep series itself

The last report in this series was `!/AUDIT-CI-FAILURE-SWEEP-2026-08-12.md` — a 7-day gap before this one, versus the near-daily cadence of the prior six weeks (see file list in Big IF). Not investigated further here (out of scope for a CI-runs sweep), but worth Logan's awareness: whatever schedule drives this routine did not fire, or did not land a report, for a week.

## Big IF

- **This repo's Actions history cannot be exhaustively enumerated in one sweep at current write-throughput**, confirming (a third time now, after 2026-08-12 and earlier sweeps) that `list_workflow_runs` pagination is unreliable here: `total_count` reads in the 100,000+ range repo-wide, and `per_page=100` requests silently return only 30 rows. The reliable workaround used this sweep — scope to a single `workflow_id` (far fewer total runs, e.g. 483 for `auto-pr.yml`) rather than the whole-repo endpoint — is worth writing into whatever doc governs this routine, so the next sweep doesn't re-discover it from scratch.
- **The failure this sweep found is a genuinely different root cause than 2026-08-12's** (`agent-swarm-signing-proof.yml`'s invalid `permissions.administration` key, already fixed) — it is not a recurrence of that incident, and not the Codacy/sync-drift chronic items tracked in GH #822 / Linear LAF-72 either. It is new evidence that a GitHub-side policy (SHA-pin enforcement) was turned on or newly enforced, with a blast radius across every branch that never rebased past `main`'s pinning migration — a class of failure that will keep recurring, once per stale branch, until those branches are cleaned up or rebased, regardless of `main`'s health.
- **The audit-PR pile did shrink since 2026-08-12, partially.** Of the seven open "audit(ci)" PRs that sweep listed (#859, #861, #862, #866, #882, #884, #905), a fresh title search today shows #861, #862, #882, #884, #905 now closed/merged — five of seven. **#859** (2026-07-21 sweep, doc-only, `mergeable_state: behind`) and **#866** (2026-07-27 sweep + a real word-boundary regex fix, `mergeable_state: behind`, 23 comments, explicitly deferred to Logan for an Actions-settings judgment call in its own body) remain open. This sweep does not merge them — both are `behind` `main` (need a rebase first) and #866 in particular says outright it is "Ready for Logan to review and merge," not for an agent to merge unilaterally. Flagging their continued presence rather than adding an eighth.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
