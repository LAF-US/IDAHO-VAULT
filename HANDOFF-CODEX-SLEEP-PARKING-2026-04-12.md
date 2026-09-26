---
title: HANDOFF - Codex Sleep Parking
created: 2026-04-12
updated: 2026-04-12
status: active
authority: LOGAN
authors:
- ChatGPT Codex
type: handoff
related:
- '2026-04-12'
- 1Password
- AGENT-PROTOCOL
- DOCKET
- JANITOR
- LOGAN
- Obsidian
- Phone Link
- TROUBLE-BUBBLE
- what3words
- codex
---
# HANDOFF - Codex Sleep Parking

## Parking state

This thread is parked for Logan's sleep cycle. The goal is not completion theatre. The goal is to leave the workspace legible for the next Janitor pass.

## Clean lane split

These lanes are currently distinct and should stay distinct unless new evidence explicitly bridges them:

1. **GitHub org migration**
   - anchored by `!/INBOX/images/2026-04-12-screenshot-2026-04-12-013747.jpg`
   - treat as GitHub/account/org migration context

2. **what3words API restriction / quota**
   - anchored by:
     - `!/INBOX/images/2026-04-11-screenshot-2026-04-11-204911.jpg`
     - `!/INBOX/images/2026-04-12-screenshot-2026-04-12-013254.jpg`
   - local 1Password retrieval path is verified
   - direct API probe still returns `HTTP 401`
   - remaining blocker reads as key policy / restriction / entitlement, not missing local secret

3. **Claudius intake and binding**
   - active intake lane
   - should not be merged into the API-key or plugin lanes without explicit linking evidence

4. **Obsidian plugin mechanics**
   - separate active lane
   - keep isolated from GitHub and what3words unless a screenshot or runtime symptom directly ties them together

## Obsidian state

Obsidian is in the intentionally lean recovery posture:

- active plugin list matches `.obsidian/plugin-modes/restricted-recovery.json`
- enabled plugins:
  - `periodic-notes`
  - `settings-search`
  - `tag-wrangler`
  - `nldates-obsidian`
  - `recent-files-obsidian`
- installed plugin directories still number 52, but only 5 are enabled

Current read:

- startup remains fast because the vault is still in restricted recovery
- do not re-enable the heavier agentic / indexing layer casually before a staged test plan

## 1Password / op state

The important boundary truth:

- local desktop `op` access is partially usable even when `op whoami` reports signed out
- repo bootstrap was patched to treat successful live `op vault list` access as a usable desktop-auth signal
- workflow docs were patched to stop conflating local desktop vault names with CI secret-reference paths

This means:

- local secret retrieval is no longer the primary suspected blocker in the what3words lane
- the what3words lane should now be treated as downstream API policy / restriction work

## Intake breadcrumbs

Phone Link intake is behaving usefully. The janitorial move is restraint:

- keep letting Phone Link sweep
- keep classifying screenshots by lane
- do not merge screenshot lanes just because they arrived close together

Relevant image-side note:

- `!/INBOX/images/2026-04-12-agent-to-janitor-lane-classification.md`

## Dirty worktree warning

The workspace contains many local changes across multiple lanes. Do not sweep, stage, or commit broadly without re-triage.

Particularly active surfaces include:

- Obsidian recovery files
- 1Password / what3words docs
- intake and image notes
- unrelated pre-existing vault edits outside this session

## Janitor's first question on re-entry

Before touching code or notes, ask:

> Is this action in the GitHub org migration lane, the what3words API lane, the Claudius intake lane, or the Obsidian plugin lane?

If the answer is "more than one," require explicit evidence.
