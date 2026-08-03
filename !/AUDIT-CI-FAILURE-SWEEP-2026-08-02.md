---
title: CI Failure Sweep — 2026-08-02
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-08-01T20:01:26Z to 2026-08-02T20:01:26Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-02

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; Claude Code (this session, scheduled routine). No new human-caused breakage identified. |
| **What** | 734 workflow runs observed in-window; 14 non-success (~1.9%). Six distinct failure signatures, all isolated to three non-`main` branches — zero non-success runs on `main`. |
| **When** | 2026-08-01T20:01:26Z – 2026-08-02T20:01:26Z. Two clusters: ~08:37–09:13 UTC (10 failures, one branch) and ~16:37–19:22 UTC (4 failures, two branches). |
| **Where** | 10 of 14 on `test/subtle-alien-landing` (PR #470's head branch). 4 of 14 split across `codex/python-automation-hardening-v2` (PR #562's head branch) and `claude/harden-py-automation-followup-562` (no open PR found for this branch in the fetched PR list). |
| **Why** | See "Blocking / repeated" below — nothing new; both clusters continue previously-flagged, branch-scoped conditions. |
| **How** | See per-signature categories below. No category required guessing past what job/log evidence actually showed — two signatures are marked **unclassified** rather than assigned a category, because the retrieved log excerpts only showed post-failure cleanup output, not the actual failing assertion. |

### Failure signatures

| Workflow | Conclusion | Count | Branch | Category | Root cause |
|---|---|---|---|---|---|
| `opencode.yml` | `action_required` | 4 | `claude/harden-py-automation-followup-562` (2), `codex/python-automation-hardening-v2` (2) | Configuration | Workflow gated behind manual approval before any job runs (0 jobs created); same recurring bot-trigger-approval family documented across #617/#644/#700, exact conclusion-type match not independently confirmed against those bodies this sweep. |
| Python Test Suite | `failure` | 2 | `test/subtle-alien-landing` | Code (unverified) | "Run test suite" step exited non-zero. Log tail only captured post-test cleanup, not the actual assertion/traceback — root cause not confirmed, not guessed. |
| Codacy Coverage Reporter | `failure` | 2 | `test/subtle-alien-landing` | Code (unverified) | Same commit/window as the Python Test Suite failures above; correlated, not confirmed to be the identical underlying assertion. |
| NETWEB Path Portability Check | `failure` | 2 | `test/subtle-alien-landing` | Code (unverified) | "Check for cross-platform path violations" step failed; log tail only showed git cleanup, not the violation output itself. |
| Cross-Platform Smoke | `failure` | 2 | `test/subtle-alien-landing` | Infrastructure (unverified) | Both `ubuntu-latest` and `macos-latest` matrix jobs **succeeded**; both `windows-latest` jobs failed at the `actions/checkout` step itself, before any test ran. Whether this is a Windows path-length/portability issue (this branch is also failing the NETWEB check on the same commit) or an unrelated runner flake was not confirmed. |
| `dependabot-rhythm.yml` | `failure` | 2 | `test/subtle-alien-landing` | Unclassified | `total_count: 0` jobs on both runs — failed before any job was scheduled (workflow-level, not step-level). No error content retrievable via the job/log APIs. Does not match the mechanism described in #676 (Version Transition Ledger check failing on Dependabot-authored PRs) — this is a `push` event on a manual branch, not a Dependabot PR. Flagged as a distinct, currently-undocumented signature; low priority, confined to one non-`main` scratch branch. |

## Blocking / repeated

- **`main` is unaffected.** All 14 non-success runs are on `test/subtle-alien-landing`, `codex/python-automation-hardening-v2`, or `claude/harden-py-automation-followup-562` — none on `main`, and no `pull_request` run targeting `main` failed in-window.
- **`test/subtle-alien-landing` (PR #470) continues to fail the same categories of checks flagged in the 2026-07-31 sweep** (unresolved malformed/duplicated content in `!/GRIMOIRE_caution_contains-false-doctrines/` files, noted there as a review comment rather than resolved unilaterally — a doctrine call, not this routine's to make). Today's Python Test Suite / Codacy Coverage Reporter / NETWEB failures on that branch are consistent with, not new evidence against, that standing diagnosis. PR #470 remains `mergeable_state: blocked`, labeled `arbiter/loganfinney27`.
- **opencode `action_required` on PR #562's branch does not appear to be a required/blocking check** — 7 of the newest open PRs (#562, #563, #877, #872, #866, #875, #884) were checked via combined external-status API and all showed `success` on the non-Actions contexts present. **Gap, stated plainly:** that API does not surface native GitHub Actions check-run results, and the native check-runs endpoint was not queried per-PR this sweep (budget). So "not blocking" here is a partial read, not a confirmed clean bill for those 7 PRs' Actions checks specifically.

## New findings

- `dependabot-rhythm.yml` failing with zero scheduled jobs on a `push` to `test/subtle-alien-landing` (see table) does not match any previously cross-referenced issue's documented symptom. Confined to one non-`main` branch; not investigated further this sweep given the low blast radius.

## Big IF

- **The daily audit-PR series has itself become the pile it exists to prevent.** Checked directly against `main`'s tree and full commit history: of the eleven `AUDIT-CI-FAILURE-SWEEP-*` reports filed since this thread (#822) opened on 2026-07-08, only **three** ever landed on `main` — 2026-07-08 (via #821), 2026-07-09 (#828), and 2026-07-20 (direct commit `dfc836d3`). The other **eight**, spanning 2026-07-11 through 2026-07-31 (#838, #859, #861, #862, #866, #878, #882, #884), remain open, unmerged, mostly draft. This sweep's own scheduling instructions explicitly warn against adding a ninth. Accordingly: **this file is not being opened as its own standalone PR.** It's landing bundled with substantive fix work from the same session (see the `#514` plugin-registry fix on this branch), and the findings above are posted to the existing GitHub/Linear/Slack/Discord surfaces below rather than a tenth cross-post-only artifact. Whether the eight stuck report PRs get merged, closed, or superseded is Logan's call, not this routine's — flagging the count rather than acting on it.
- No native Discord connector is installed for this org (checked via connector list); Discord is reached through the enabled Zapier integration (`#ledger`), consistent with prior sweeps.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
