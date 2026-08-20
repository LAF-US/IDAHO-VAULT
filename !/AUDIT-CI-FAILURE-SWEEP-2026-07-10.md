---
title: CI Failure Sweep — 2026-07-10
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-09T04:35Z to 2026-07-10T04:35Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-10

## 5W Summary

| | |
| --- | --- |
| **Who** | No new human-caused breakage. Two duplicate/stale open PRs found and reconciled (below) — not a CI failure, but the same "unaddressed pile" pattern this sweep exists to interrupt. |
| **What** | 25 failing runs across 6 workflows in-window: Codacy Security Scan (13, chronic — day 4, still blocked on Logan), Sync Plugin Registry (2, chronic self-heal was written but never landed), Sync Agent Discovery Index (2, same), `claude-sign.yml` startup failure (1, isolated to draft PR #450's own branch), Python Test Suite (1, same branch), Action Pin Policy (1, same branch), Review Feedback Loop (2, transient GitHub 504s while creating a label named `risk/—`). 3 further "failure"-labeled runs on PR #831 were concurrency-group cancellations mislabeled by GitHub as `failure`, not real breakage. |
| **When** | 2026-07-09T04:35Z – 2026-07-10T04:35Z (fully paged, no gaps; see agent transcript for page-by-page verification) |
| **Where** | Codacy: every push/PR to `main`. Sync drift: `logan/obsidian`. Others: isolated to `claude/draft-signing-via-action-2026-06-01` (PR #450, intentional draft) and PR #831 (closed today, see below). |
| **Why** | See per-item below; root causes for the recurring items are already fully diagnosed in #822. |
| **How** | Shipped fixes this pass rather than re-filing findings (see below) — continuing the standing instruction not to let this become another opened-and-unaddressed report. |

## Shipped this pass

1. **PR #481 (oldest actionable open PR, open since 2026-06-06) — fixed and brought current.** Resolved its 3 remaining open review threads (orphaned duplicate corpus file, mixed wikilink/markdown-link styles, inconsistent `Status`/`STATUS` casing) and added a Verification Note flagging 2 source-citation mismatches CodeRabbit's review had raised but never actually got resolved (a "thread housekept as outdated" ≠ "substance fixed" gap). Branch synced clean against current `main` via `update_pull_request_branch`. Blocked only on the known Codacy token gap (below) and Logan's call on the 2 flagged citations.
2. **PR #831 closed as a duplicate.** It contained an independent rework of #481's same 3 threads from a session the day before, built on the premise that #481's branch had an unrelated-history problem with `main`. That premise didn't hold — direct fix + branch sync worked cleanly. Rather than leave two PRs carrying the same content, closed #831 and pointed reviewers to #481.
3. **PR #834 opened (draft) to recover real infra work that #831 also carried and would otherwise have been lost when #831 was closed.** Self-heal jobs for the chronic `logan/obsidian` drift checks (Sync Plugin Registry / Sync Agent Discovery Index — tracked in #822 since 2026-07-08, "recommended... never implemented across two more sweeps") plus a tested exemption so this report's own naming convention stops tripping the Redaction Damage Policy guard on itself. This is why Sync Plugin Registry / Sync Agent Discovery Index still show 2 fresh failures each in this window: the fix was written and verified locally on 2026-07-09 but never actually merged. Marked draft pending Logan (or a follow-up sweep) re-confirming the test suite and watching one live `logan/obsidian` push exercise the self-heal job.

## Blocking / repeated

- **Codacy Security Scan (13 runs, 100% of in-window pushes to `main`) — day 4 of the same block.** Root cause fully diagnosed in #822: `CODACY_PROJECT_TOKEN` was never provisioned (not in `.op/secrets.template.md`'s inventory). All underlying SARIF-formatter bugs were fixed on 2026-07-08; this is now purely a missing-credential wall (`Could not get remote project configuration: No credentials found.`). Not fixable by an agent — needs Logan to either provision the token via 1Password + repo secret, or decide to retire the workflow. Flagging directly rather than re-filing: **this has now blocked every push/PR to `main` for 4 consecutive daily sweeps (LAF-71 through this one) with no change in status.**
- **Sync Plugin Registry / Sync Agent Discovery Index** — see "Shipped this pass" above; fix exists (PR #834, draft), just never landed.

## New findings

1. **Broken risk-tier labels (`risk/—`, `filetype:risk/—`, `depth:risk/—`) applied to PRs, e.g. #481.** `classify_paths.py`'s own comments describe a `—` (em-dash) sentinel for an "undetermined" tier that's explicitly documented as safe because the binary `risk/low`/`risk/high` label contract only ever consumes the collapsed binary value — but the labels actually observed on-PR show the em-dash landing in the literal label text, contradicting that design note. **Category: Code.** This is also very likely the direct cause of the `Review Feedback Loop` 504s in this window (`gh label create risk/— ...` timing out against GitHub's label API — a literal em-dash in a label name is unusual input, plausibly slower to normalize/index than an ASCII label). Next step: whoever's mid-refactor on `classify_paths.py`'s tier4/consumer wiring should check where the richer `tier4`/`filetype` fields are being applied as literal GitHub labels instead of staying internal — not something to guess-fix without reading the labeling workflow directly.
2. **PR #831 had 3 checks reported as `failure` that were actually `cancelled` underneath** (concurrency-group preemption from rapid successive pushes during active CI-sweep work on that branch, now moot since the PR is closed) — a run-level/job-level status mismatch worth remembering next time a "failure" doesn't reproduce: check the job, not just the run, before treating it as a real break.

## Big IF

- **The Codacy block is now old enough (4 sweeps) that re-diagnosing it is no longer the useful action — only Logan's decision unblocks it.** Every sweep since 2026-07-07 has correctly identified the same root cause and the same two remediation paths (provision token / retire workflow). Continuing to note it accurately but not act on it is not the same as progress; surfacing this explicitly rather than letting it read as "still investigating."
- **Duplicate/superseding PRs are a variant of the same "unaddressed pile" problem this sweep exists to interrupt**, just at the PR level instead of the audit-report level — #481/#831 is the second instance in as many weeks (the first being the #463→#821 rework noted in the 2026-07-08 sweep). Worth a standing check before opening a new PR to "fix" old content: search for an existing open PR touching the same files first.
- **No Discord connector was available in this session** (confirmed via tool search — same gap noted in the 2026-07-09 follow-up). Could not post there.
