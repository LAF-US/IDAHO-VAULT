---
title: CI Failure Sweep — 2026-07-30
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-29T12:10Z to 2026-07-30T12:24Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-30

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; Claude Code (this session, scheduled). No human-caused breakage. |
| **What** | 6 `failure`-conclusion runs (1 workflow, already fixed upstream before this sweep started) + 1 batch of ~13 `action_required` runs (1 push, routine approval gate) + 3 `cancelled` (benign concurrency supersede). 0 `startup_failure`, 0 `timed_out`. Every previously-chronic item in this thread (Codacy Security Scan, Codacy Coverage Reporter, Sync Plugin Registry/Sync Agent Discovery Index self-heal) confirmed resolved and holding — not just quiet today, structurally fixed. |
| **When** | 2026-07-29T12:10Z – 2026-07-30T12:24Z |
| **Where** | `main` (0 failures across ~330 completed runs, checked back past the 24h cutoff); PR #875 (the 6 real failures, self-resolved on the PR); PR #880 (the approval-gate batch). |
| **Why / How** | Per item below. |

**`main` is green** at head `ca667a5d`; nothing blocks a merge or a deploy.

## Findings

1. **Daily Notes Placeholder Check (`validate-daily-notes.yml` / `check-date-placeholders`) — 6 failures, PR #875, 2026-07-29T22:33Z–2026-07-30T01:02Z. FIXED, not just re-flagged.** Root cause was a real bug in the check itself: it searched for `[[YESTERDAY]]`/`[[TODAY]]`/`[[TOMORROW]]` wikilink tokens, but the vault's actual Templater/Obsidian templates emit `<% ... %>` and `{{...}}` — so the check missed real unrendered placeholders (`2026-04-22.md`'s frontmatter had three) while flagging a hand-written, non-template line (`2026-04-16.md:26`) as if it were template residue. PR #875's own author fixed this directly (commit `c035090`, 2026-07-30T03:07:11Z): corrected predicate, widened scope from daily notes to all five periodic note types, repaired `2026-04-22.md`'s stale placeholders. Confirmed both post-fix runs (03:07:28Z, 03:15:52Z) are `success`. **Category: Code (real bug), already fixed on the PR branch** — not yet on `main` since #875 is still open.
2. **~13-workflow `action_required` batch, 2026-07-30T00:30:59Z, branch `claude/poka-yoke-qzt7le`.** Traced to the specific PR via `get_workflow_run` rather than trusting the branch name alone: this is **PR #880** (a small draft auto-PR from `github-actions[bot]`), not the earlier #865 that used the same branch name before it merged and the branch was recreated from `main`. Same routine GitHub approval gate on bot-triggered workflow runs this thread has documented since LAF-70/#633 — self-resolved 13 minutes later (00:43:15Z, same branch, all green). **Category: Infrastructure (by-design gate), not a failure.**
3. **No other failures found in-window** across all workflow files individually checked (Python Test Suite, Codacy Security Scan, Codacy Coverage Reporter, Cross-Platform Smoke, Secret Pattern Policy/Full Scan, Redaction Damage Policy, Agent Review Gate, Auto-merge chain (engage/enqueue/rhythm/batch-arm), Review Feedback Loop, Agent Review Response, `opencode`, Sync Dependencies, all `check-*`/`*-policy` content gates, Sort Audit, Janitor Sweep, Daily Rollover, Wayback Audit/Preserve, Dependabot Rhythm, `claude-sign`, and more) — no `startup_failure`, no stuck `in_progress`/`queued` runs.

## Chronic items — status check (all clear)

- **Codacy Security Scan** — 15/15 non-cancelled runs succeeded in-window. The #864 fix (2026-07-24, pinned checksum-verified CLI) is holding at 6 days.
- **Codacy Coverage Reporter** — 28/29 succeeded (remaining 1 is item #2's routine gate, not a failure). This was still broken as of the 2026-07-24 sweep (account-token gap); now clearly resolved — first sweep in this thread reporting it clean.
- **Sync Plugin Registry / Sync Agent Discovery Index** — verified directly by reading `main`'s current `.github/workflows/sync-plugin-registry.yml` and `sync-agents-bootstrap.yml`: both now carry the self-heal job scoped to `logan/obsidian` (from #831/#834), landed since the 2026-07-20 sweep last confirmed it was still only parked. No `logan/obsidian` plugin/agent-config pushes occurred in-window to exercise it, but the fix is structurally in place, not just quiet.
- **`check-notebooks-paired`** — 0 failures in-window (18 runs). PR #862 (the jupytext-pin fix) is still open but green; no recurrence today.

## Oldest-open-PR pass

Picked **PR #596** ("Land live Vault snapshot updates," open since 2026-06-20) — no prior sweep session had touched its own review threads. Resolved 4 of 6 open threads and shipped one real fix directly to its branch (`7232087`): `manifest.json`'s `generated_at` was stale (`2026-04-23`) despite this PR's own plugin-count changes; restamped to match. The other three resolved threads were stale bot comments already addressed in the PR's own history (`calendar_date` group, a blank-line fix, a `MOC.md` alias with nothing to actually collide with — verified no `map of content.md` file exists anywhere in the repo). Left one `swarm.json` naming nitpick open/advisory (matches the plugin-registry generator's own intentional two-schema output, not a bug this PR introduced).

**Correction (2026-08-09), replacing the original "new finding" below:** the claim that PR #596 hit the pre/post-purge "unrelated histories" break was wrong, and repeated exactly the error the 2026-07-11 sweep (`AUDIT-CI-FAILURE-SWEEP-2026-07-11.md:67-69`) had already warned against: `git merge` was run in a **shallow local clone**, where `fatal: refusing to merge unrelated histories` is a known artifact of insufficient fetch depth, not proof the histories are actually unrelated. Copilot's review on PR #882 caught this. Re-verified properly this time: unshallowed the clone (`git fetch --depth=5000 origin main <branch>`), confirmed `git rev-parse --is-shallow-repository` returns `false`, and re-ran the test — `git merge-base origin/main origin/test/dotfolder-live-snapshot-with-drive-migration-attempt` **succeeds**, returning `7931b46f` (PR #596's own recorded base SHA — a completely ordinary common ancestor). A real `git merge --no-commit` from that state produces ordinary `CONFLICT (modify/delete)` results on ~20 files (mostly `THE-GEMSTONE/*` folder-index placeholders #596's branch deleted that `main` independently touched afterward) — a normal, mechanically resolvable merge conflict, not a structural history break. `mergeable_state: dirty` on #596 was always just this. Retracting the "third confirmed instance" claim entirely; it should not be cited going forward. Whether the #463/#821 case itself holds up under the same full-history test is a separate, still-open question — not re-verified here.

## Big IF (Insights and Findings)

- **First fully-clean sweep in this 23-day series.** Every item this thread has tracked as chronic (Codacy Security Scan, Codacy Coverage Reporter, Sync Plugin Registry self-heal) is now independently confirmed resolved and structurally holding, not merely quiet for one window. The only two non-`main` conclusions in 24h were a real bug already fixed by its own PR's author before this sweep started, and a routine bot-triggered approval gate.
- ~~The pre/post-purge "unrelated histories" break (2026-07-08's Big IF) now has three confirmed instances (#463/#821, and today #596) rather than one.~~ **Retracted (2026-08-09) — see the correction under "Oldest-open-PR pass" above.** The #596 instance was a shallow-clone testing artifact, not a real recurrence. The genuinely load-bearing insight here is narrower than originally stated: **a shallow local clone makes `git merge`'s "unrelated histories" error unreliable as evidence, and this exact mistake was made twice in this thread** (2026-07-08's original #463/#821 diagnosis, not independently re-checked here; and this sweep's #596 claim, now disproven). Any future sweep citing this break must first confirm `git rev-parse --is-shallow-repository` is `false` on the clone doing the testing, or verify via `git merge-base` succeeding rather than a bare `git merge` failing.
- **Branch-name reuse after merge can misattribute a workflow run to the wrong PR if you trust `head_branch` alone.** `claude/poka-yoke-qzt7le` served PR #865 (merged 2026-07-28) and, after being recreated from `main`, PR #880 (opened 2026-07-30) — a run listing showed the branch name but the actual PR association required a direct `get_workflow_run` lookup to get right. Worth checking this explicitly rather than assuming in future sweeps that share a branch name across a merge boundary.

Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment, not a new ticket), Slack #all-logan-finney, Discord #ledger (via Zapier).

Claude-Session: <https://claude.ai/code/session_01Dbbr4r32bPDaQiWX4R3f1u>
