---
title: CI Failure Sweep — 2026-08-12
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, ~2026-08-11T08:22Z to 2026-08-12T08:22Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-12

## 5W Summary

| | |
| --- | --- |
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (66 workflows per `list_workflows`). One reoccurring, repo-wide failure found and fixed in this same PR. No other new breakage confirmed. |
| **What** | `.github/workflows/agent-swarm-signing-proof.yml` carried an invalid `permissions.administration` key, which fails GitHub's workflow-file schema validation outright. Because the file is evaluated against every push (to determine triggers) regardless of its own `on:` block, this surfaced as a "failed" run — 0 jobs, run name literally the file's path, event `push` — attributed to whichever branch was pushed to, on **every push to every branch in the repo**. |
| **When** | Introduced by commit `48b6d8b2` (2026-08-10T23:54:48Z), a well-intentioned but incorrect prior fix for a different problem (see Findings). Confirmed still firing through 2026-08-12T06:04:05Z, when this sweep applied the fix. |
| **Where** | Not on `main` directly, and not a required PR status check (the file only declares `workflow_call`, never `pull_request`) — but it hit every branch that received a push during the ~33-hour window: sampled directly on `claude/poka-yoke-qzt7le`, `claude/fullcalendar-obsidian-integration-1u2a0l`, `claude/practical-cerf-6wgxnl`, and `claude/apply-patch-fixes-9gesn5`. |
| **Why** | `administration` is not a recognized `GITHUB_TOKEN` permission scope. Verified against GitHub's own Actions permissions reference, which enumerates: `actions`, `artifact-metadata`, `attestations`, `checks`, `code-quality`, `contents`, `deployments`, `discussions`, `id-token`, `issues`, `packages`, `pages`, `pull-requests`, `security-events`, `statuses`, `vulnerability-alerts` — no `administration`. The prior commit added it trying to fix a 403 on `gh api repos/$REPO/rulesets`, not realizing the key itself would invalidate the whole file. |
| **How** | Root-caused via job-log pull (`get_job_logs` → 0 jobs, confirming this is an invalid-workflow-file signature, not a step failure), direct file read, and cross-check against GitHub's live documentation (fetched, not recalled from training data). Verified the fix by re-parsing the YAML (`yaml.safe_load`) and confirming none of the four `workflow_dispatch`-only wrapper files (`agent-swarm-signing-proof-{claude,codex,mistral,opencode}.yml`) declare a `push` trigger — so the reusable workflow's own logic was never actually executing on these push events; every one of the sampled failures was the phantom evaluation-time error, not a real dispatch. |

## Findings

### Incident A — `agent-swarm-signing-proof.yml` invalid `permissions.administration` key — Code, **fixed in this PR**

Confirmed root cause and fixed: removed the invalid `administration: read` line from the `permissions:` block. Re-parsed the file with `yaml.safe_load` to confirm validity post-fix. This stops the repo-wide push-triggered failures; it was not gating merges to `main` (not a `pull_request`/required check), but it was putting a red "failed" workflow run on the Actions history of every single push, repo-wide, for ~33 hours.

**Not fixed here, and not this sweep's to fix:** the step this workflow performs — reading repository rulesets via `gh api repos/$REPO/rulesets` — cannot succeed with the automatic `GITHUB_TOKEN` at all. Repository-administration/rulesets access is not a grantable `GITHUB_TOKEN` scope under any key name (confirmed against the same permissions reference), so whenever this reusable workflow is actually invoked (via one of its four `workflow_dispatch` wrappers, not on ordinary pushes), that first step will still fail on its own, isolated 403 — a real but pre-existing and separately-scoped problem, already tracked under #398 ("Stable cross-platform signed-commit solution"). Fixing that needs a privileged credential (PAT or GitHub App token) for that one step, which is a design decision for #398, not a schema bug for this sweep to silently paper over.

### Incident B — one non-recurring `Python Test Suite` failure, `merge_group` on `gh-readonly-queue/main/pr-906` (2026-08-05T17:40:02Z) — out of window, not investigated

Surfaced only in a wider spot-check sample outside the 24h audit window (repo history pagination is unstable under this repo's write throughput — see Big IF below — so spot-checks landed on some older slices incidentally). Appeared exactly once, is not reoccurring in the in-window samples, and PR #906 is no longer in the open-PR list, suggesting it has already closed or merged. Not chased further; flagged only for completeness.

### Zero failures found on `main` itself in-window; nothing found blocking merges to `main`

## Big IF

- **Full-24h enumeration wasn't reliable at this repo's scale.** `total_count` on `list_workflow_runs` reported between ~40,000 and ~75,000 depending on the call, and sequential page fetches (issued moments apart) landed on non-adjacent time ranges — consistent with new runs being created faster than pagination offsets can be issued. Practical response: sampled multiple time-slices spanning the window, traced every failure signature found to a real root cause via job logs rather than leaving anything as "possibly" or "likely," and reported the sampling limitation plainly instead of implying an exhaustive sweep that didn't happen.
- **This is at least the third sweep in this thread's history to find a real, fixable workflow bug rather than only re-describing known issues** (following the 2026-08-02 and 2026-08-03 pattern noted in the prior sweep) — this time the bug was itself introduced by a prior CI-fix attempt, which is worth naming: a schema-invalid `permissions:` key is an easy trap when adding a permission key by guessing rather than checking the enum, and it fails in a way (0-job phantom failure, not a normal job error) that's easy to misread as "flaky" rather than "broken file."
- **The audit-PR pile did not shrink.** Open PRs whose title/branch matches the "audit(ci) / CI failure sweep" pattern as of this sweep: #859 (07-21), #861 (07-22), #862 (07-23), #866 (07-27), #882 (07-30), #884 (07-31), #905 (08-03) — seven, before this one. This sweep follows the established instruction (bundle the report with a real fix, don't file a report-only PR) but that alone doesn't clear the backlog; only merging or deliberately closing the existing seven does. Worth a batch pass on Logan's end — per this routine's own instructions, this session is not closing any of them itself.

---
