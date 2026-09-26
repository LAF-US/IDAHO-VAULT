---
title: CI Failure Sweep — 2026-07-28
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-27T12:38Z to 2026-07-28T12:30Z
owner: Logan Finney
---

## 5W Summary

| | |
| --- | --- |
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; Claude Code (this session, scheduled). No human-caused breakage. |
| **What** | 10 `failure`-conclusion runs across 4 workflows, collapsing to 3 distinct causes (one fixed this pass); plus 28 `action_required` (routine Copilot-bot approval gate, not failures) and 4 `cancelled` (benign concurrency supersede). 0 `startup_failure`, 0 `timed_out`. `main` is green at head `543d1a69`. |
| **When** | 2026-07-27T12:38Z – 2026-07-28T12:30Z |
| **Where** | `claude/apply-patch-fixes-9gesn5` (PR #871, since merged), `claude/shall-rome-lyrics-ok9049` (PR #854), `codex/python-automation-hardening-v2` (PR #562) + its merge-queue entry. |
| **Why** | See per-item below. |
| **How** | See per-item next step. |

## Blocking / repeated

Nothing currently blocks `main` or a merge. `mergefreeze` is the real merge gate per the 2026-07-11 correction already on record in #822.

## New findings

1. **Auto PR for Agent Branches — `gh: Argument list too long` (run `30331910962`, 2026-07-28T05:32:59Z, `claude/apply-patch-fixes-9gesn5`).** **Category: Code.** `gh pr create --body "$BODY"` embedded the full `git diff --stat` output inline in argv; on a ~6,326-file diffstat this exceeded the OS `ARG_MAX`. Root-caused and explicitly left open in PR #871's own body ("left for Logan"). **Fixed, not just re-flagged:** PR #872 (draft, this session) switches to `--body-file` with a temp file, which has no such limit.
2. **Redaction Damage Policy / Secret Pattern Policy / Daily Notes Placeholder Check — same branch, same commit window (05:33:02Z).** **Category: Configuration (expected, not a bug).** All three are pre-existing content the PR #871 author already reviewed and deliberately excluded from that lint pass: pre-existing `***REMOVED***` redaction scars in 9 files (#739's known pattern), a Discord OAuth2 doc's example `client_secret` in 2 files, and one daily note carrying a `[[TODAY]]` token. Documented in #871's own merged body under "60 files excluded." Not a new problem — confirmed by reading the specific flagged lines directly, not inferred.
3. **Agent Review Response — GraphQL `RATE_LIMIT` (4 runs, 2026-07-27T19:25:13–37Z, PR #854, `claude/shall-rome-lyrics-ok9049`).** **Category: Transient/Infrastructure.** `review_feedback_loop.py`'s `_fetch_pr()` call failed: `API rate limit already exceeded for user ID 136375980` — the numeric GitHub user ID for `loganfinney27`. This workflow authenticates via `secrets.MERGE_QUEUE_TOKEN || secrets.GITHUB_TOKEN` (`.github/workflows/review-response.yml:30`); a `RATE_LIMIT` error attributed to a specific *user* ID (rather than an app/installation) is consistent with `MERGE_QUEUE_TOKEN` being a personal-access token scoped to Logan's own account, whose GraphQL quota is shared across everything else that account does — not verified further than the log text itself (`*` — haven't confirmed `MERGE_QUEUE_TOKEN`'s actual token type via 1Password or GitHub settings). All 4 failures landed in one burst and did not recur afterward; self-resolved. First time this specific error has appeared in this thread's (#822) sweep history.
4. **Python integrity check (`check-paths` job, "subprocess call missing timeout") — 2 runs (2026-07-27T15:49:52Z / 15:51:49Z), `codex/python-automation-hardening-v2` (PR #562) and its `gh-readonly-queue/main/pr-562-*` merge-queue entry.** **Category: Code**, but pre-existing/chronic on that specific branch (first flagged in the 2026-07-11 sweep on this same issue, recurring since) and it's that PR's own author's active WIP, not a vault-wide regression. Not touched here.

## Big IF

None this pass — no new architectural or systemic risk surfaced beyond what's already tracked in #822's history. The rate-limit item (finding 3) is worth a one-time confirmation of `MERGE_QUEUE_TOKEN`'s actual token type given the swarm's overall API call volume, but it's a single self-resolved burst, not a demonstrated recurring problem — flagged, not escalated.
