---
title: CI Failure Sweep — 2026-07-11
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-10T12:06:43Z to 2026-07-11T12:06:43Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-11

## Process note before the findings

This is the 8th consecutive daily sweep report in this series (LAF-52 through LAF-74, GH #644 through #822/#835). Several of the last five have repeated the identical Codacy diagnosis in near-identical wording and repeated "no Discord connector" verbatim — that pattern is the thing this run was explicitly told not to add to. So: no new GitHub issue, no new Linear ticket. This lands as a comment on the existing tracking issue (#822) and existing ticket (LAF-74), and the one item with a concrete fix was shipped, not just re-described.

## 5W Summary

| | |
|---|---|
| **Who** | No human-caused breakage. One correction to a claim made by this session's own research pass (below). |
| **What** | 3 distinct failure patterns, 15 failed runs: Codacy Security Scan (13, known day-5 credential gap), Secret Pattern Policy (1, real hit — see correction), `check-portable-paths.yml` (1, new, isolated to another agent's active branch). |
| **When** | 2026-07-10T12:06:43Z – 2026-07-11T12:06:43Z |
| **Where** | Codacy: every push/PR to `main`, repo-wide. Secret Pattern Policy: `logan/obsidian` push. `check-portable-paths.yml`: `codex/python-automation-hardening-v2` PR only. |
| **Why** | See per-item below. |
| **How** | Codacy needs Logan's provision-vs-retire call (day 5, unchanged). Secret Pattern Policy needs Logan's confirmation of a de-escalating fact this sweep found, not urgent remediation. `check-portable-paths.yml` is isolated to another agent's branch — flagged there, not touched. |

## Repeated, not blocking (corrected — see bottom of report)

**Codacy Security Scan (13/13 runs failed this window)** — unchanged for the 5th consecutive day. **Correction, posted after Logan's review of this report: Codacy is noise, not a blocker** — confirmed directly against PR #503's own merge (it went in via the `mergefreeze` check alone, `state: success`, with no Codacy status even listed as required). This report originally filed it under "Blocking / repeated"; that header overstated its severity. Leaving the rest of this entry as originally written, since the credential-gap diagnosis itself is still accurate — only the "blocking" framing was wrong. Same error as every prior sweep: `Could not get remote project configuration: No credentials found.` (`CODACY_PROJECT_TOKEN` never provisioned). Confirmed directly from job logs this run, including on this session's own PR #837 (run 29152276934) — the failure fired on a 1-line `.coderabbit.yaml` comment fix, which cannot itself have caused a Codacy credentials error; it's the same repo-wide gap. **Category: Configuration.** Not re-diagnosing further — the diagnosis has been stable since 2026-07-08 (#822). Needs Logan: provision `CODACY_PROJECT_TOKEN` or retire the workflow.

## Correction to a prior claim (this session's own research pass)

My own research pass on this sweep initially reported the Secret Pattern Policy hit (run 29129900847, `logan/obsidian`, 2026-07-10T23:15:41Z, flagging `google_api_key`-shaped material in `- Find Adventures Near You, Track Your Progress, Share.md` and `session-join-pattern (6).md`) as "self-resolved" because the next push on that branch succeeded. **I checked that claim against the actual current branch content before writing it here, and it's wrong.** The flagged file is still present on `logan/obsidian` (HEAD `3830a43d` as of this sweep) with the same key-shaped strings — the later push only succeeded because Secret Pattern Policy scans the *diff*, not full history, so an unrelated subsequent commit doesn't re-flag material already committed. Nothing here was actually resolved; a later commit just didn't touch it again.

Having verified that, here's the fuller picture, checked directly rather than assumed: `session-join-pattern (6).md` is a false positive — it's example Kotlin code for an SDK session-join call, where a variable assignment happens to match the checker's generic-assignment shape, not a real secret. The Google-Maps-key-shaped string is real and present, but scanning the full `logan/obsidian` tree for the same pattern (`AIzaSy[A-Za-z0-9_-]{33}`) found it in **9 files total**, resolving to only **2 distinct key values** reused across all 9. All 9 are saved-webpage-capture notes (e.g. this one is an AllTrails-style "Find Adventures Near You" page save) where the key appears inside Google Static Maps tile-image URLs — the source website's own client-side embed key, baked into the page's HTML when it was captured, not a credential issued to or owned by this vault. That's consistent with a recurring, structural false-positive class from this vault's page-capture workflow, not 9 separate leaked secrets — but I can't independently confirm from here whether either key carries any HTTP-referrer restriction, so this still needs Logan's eyes once, not a repeat of "worth a look" with no resolution path. **Suggested next step:** Logan confirms these are third-party embed keys (5-minute check), then Secret Pattern Policy gets a narrow exemption for this specific URL shape (`maps.googleapis.com/maps/vt?...&key=...` inside saved-webpage-capture files) so this stops re-flagging on every future page save — same pattern as the Redaction Damage Policy exemption already shipped for audit reports (#831/#834).

## New findings

1. **`check-portable-paths.yml` — 1 failure, `codex/python-automation-hardening-v2` PR (run 29141816215, 2026-07-11T05:49:20Z).** Real hit: `.claude/skills/run-idaho-vault/driver.py:75` — a `subprocess` call with no `timeout=`. **Category: Code.** Isolated to another agent's active branch; flagged there, not fixed here per this run's explicit instruction not to touch other agents' in-progress work.

## Verified as not recurring this window (with the caveat that matters)

**Sync Plugin Registry / Sync Agent Discovery Index** — 0 failures in this window, versus chronic daily failures through 2026-07-09. This is **not** confirmation that the self-heal fix landed — it hasn't. PR #831 and PR #834 (duplicate self-heal fixes for this exact chronic issue) are both still open, and Logan's 2026-07-10 comment on #822 explicitly said he's not touching either "until you say which way you want it to go" — respected here, neither PR touched this run. Zero failures this window most likely just means no push to `logan/obsidian` touched plugin/agent config in this specific 24h slice, not that the underlying chronic issue is fixed. Don't read this as resolved.

## Work shipped this run (not just findings)

**The "unrelated histories" claim in this section is wrong. Before relying on anything below, skip ahead to "Correction, posted after Logan's review" at the end of this report — the original text is preserved here uncorrected as the record of the error.**

Per this run's instruction to pick up one of the oldest open PRs and drive it toward merge: picked **PR #503** (open since 2026-06-09, 32 days, four reviewers — Sourcery, Copilot, CodeRabbit×2 — all flagging the identical stale-comment issue, never addressed).

- Fixed the actual issue on #503's own branch (commit `c2340795`) and resolved all 4 review threads.
- Found the real reason it sat for 32 days: #503's branch predates the "Clean history - secrets purged" rewrite and shares no common ancestor with `main` (`git merge` refuses it: "unrelated histories") — the same structural break already documented for PR #463/#821 in the 2026-07-08 sweep. Confirmed this is now the **second** independently-confirmed instance of that break, not a one-off.
- Reworked the same 1-file diff fresh onto current `main`: **PR #837** (draft, CI green except the known repo-wide Codacy gap above). Commented on #503 pointing to #837 and recommending Logan close #503 as superseded once #837 merges — did not close it myself.
- Subscribed to #837's activity; will keep watching it through to merge or close.

## Big IF

**The daily-sweep process itself may be the bigger finding.** This is the 8th sweep report in a row (going back to 2026-06-20/LAF-52), several of which re-diagnosed the same Codacy gap in nearly identical wording, and the "no Discord connector" line has now been repeated verbatim across at least 3 separate days' Slack posts (2026-07-06, 07-08, 07-09) without anyone questioning whether that connector will ever exist. Meanwhile PR #481/#831/#834 have been sitting in an acknowledged overlapping-content limbo since 2026-07-09 with an explicit Logan hold on touching them further. Worth considering, for Logan: does this sweep need to run daily, or would a lower cadence (or a cadence that only reports *changes* since the last sweep rather than the full state) reduce the volume without losing the signal — especially since the one structurally-recurring blocker (Codacy) has needed exactly one decision from Logan for 5 days running, and no amount of additional daily re-diagnosis moves it forward.

## Correction, posted after Logan's review

Logan reviewed this report and caught two errors in it directly. Recording both here rather than quietly editing them away, per this vault's own Repair doctrine (witness the error, don't paper over it).

**1. "PR #503 can't merge via the normal GitHub button" was wrong.** Logan merged #503 himself, via the ordinary GitHub squash-merge, seconds after I filed this report — flatly disproving the claim. Root cause of my error, checked directly: my working checkout of this repo is a **shallow git clone**, truncated at commit `bf0393b7` (2026-07-06) — `git rev-parse --is-shallow-repository` returns `true`, and `origin/main` shows only 51 commits reachable locally. When I ran `git merge origin/main <PR-503-branch>` locally and got `fatal: refusing to merge unrelated histories`, I concluded the two branches had no common ancestor *on GitHub*. That conclusion doesn't follow: a shallow clone's truncated object graph can produce exactly this symptom locally even when the real, full history on GitHub is entirely ordinary. I never checked whether my clone was shallow before drawing that conclusion — I should have. Logan's specific catch (a secret scrub dated a month before #503 opened cannot produce unrelated history against a branch created *after* that scrub) is correct and is what should have stopped me: I had the chronology backwards and didn't sanity-check it against the shallow-clone possibility before writing it into four separate durable records (this file, PR #837's body, a comment on #503, and a comment on GH #822).

This also means the same claim in the 2026-07-08 sweep report (`!/AUDIT-CI-FAILURE-SWEEP-2026-07-08.md`, re: PR #463/#821) is now **unverified, not confirmed false** — I have not independently re-checked that one this session, and I'm not asserting it's wrong without checking. Flagging it with the `*` wildcard rather than repeating it as settled fact: worth a from-a-full-clone re-check before it's cited again.

**Practical effect:** PR #837 (my rework of #503 onto `main`) is now fully redundant — diffed byte-for-byte identical to what #503 already merged as `d9efb2fa`. Not closing it myself (out of scope for this run), but commented on it recommending Logan close it as redundant, and corrected the record on #503's own thread and on GH #822.

**2. No Discord route was wrong — and had been wrongly repeated for at least 3 prior days.** I'd only ever checked `ListConnectors` (claude.ai-native connectors) and a Slack-only search; I never called Zapier's own `list_enabled_zapier_actions`, which shows a Discord app enabled with 11 actions including `send_channel_message`, targeting two channels (`ledger`, `purgatory`). Used it this time — see the `ledger` channel for this report's Discord post. Correcting the "no Discord connector available" line that multiple prior sessions (including this one, earlier today) posted to Slack as settled fact.
