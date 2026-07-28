---
date created: 2026-06-17
author: "Claude — Claude Code instance (branch claude/reenable-agent-automerge)"
authority: "Witness of a governance reversal, made at Logan's explicit direction (2026-06-17, 'Reverse it (record it)'). Records a change to operative behavior; does not rewrite the historical witnesses of the prior decision, which stand. Authority to elevate or further ratify reserved to Logan."
doc_class: witness
status: filed
related:
  - "PR-PIPELINE-CONSTELLATION-WITNESS-2026-06-16.md"
  - ".github/workflows/auto-merge-rhythm.yml"
  - ".github/scripts/review_feedback_loop.py"
  - "!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md"
  - "VERSION-TRANSITIONS.md"
  - CONSTITUTION
---

# WITNESS — Agent-PR auto-merge arming RE-ENABLED (reversing the #521/#527 fail-close)

*What changed, why it is safe now, and what was deliberately left untouched. Made at Logan's
direction on 2026-06-17.*

---

## The prior decision (stands as history — not rewritten)

On 2026-05-26 a batch of automation was suspended, and on 2026-06-16 the auto-merge arm was
**fail-closed**:

- `auto-merge-rhythm.yml` removed the `user.login == 'loganfinney27'` arm — author login is a
  **counterfeit-identity** gate: agents author PRs *as* `loganfinney27` through a shared token,
  so arming on the login armed agent work as if the keyed human had acted (#521/#527).
- `review_feedback_loop.py` set `AGENT_AUTO_MERGE_ENABLED = False`; its `enable-auto-merge` path
  *removed* stale auto-merge state rather than arming.
- The correct replacement was named as "arm only on a trust gate distinct from author login,"
  held pending **#398** (a distinct verified signing identity) and **ARBORSCAPE IF 12**
  (automated `--auto` requires branch protection on `main`, which was then absent).

Those records — the `auto-merge-rhythm.yml` header, `PR-PIPELINE-CONSTELLATION-WITNESS-2026-06-16`,
`.claude/MEMORY/SESSION-2026-06-16`, `SECURITY-CREDENTIAL-CONTAINMENT-2026-05-26` — are left as
the truthful account of what was decided then.

## What changed (2026-06-17)

`main` now lands every change **through the GitHub merge queue** (verified this session by
# 546, #540, #542, #544, #536, #547, #548 all merging via the queue). The merge queue **is**
branch protection on `main` — so:

- **ARBORSCAPE IF 12's precondition is satisfied.** The structural reason the lane was shelved
  ("`main` is unprotected") no longer holds.
- **The trust gate #521 demanded now exists, and it is not author login.** Arming a PR no longer
  asserts "a human approved"; it asserts only "merge once the required checks, reviews, and
  thread-resolution pass." The queue + branch protection are the gate, regardless of who armed.

Therefore `AGENT_AUTO_MERGE_ENABLED` is set **True**, and the engine arms PRs — guarded — when
their last blocking review thread clears.

## The guards that remain (arming stays conservative)

1. **Eligibility** (`evaluate_review_state`): a PR is armed only if it is `risk/low`, past the
   grace window (≥30 min), and not merge-blocked (no draft, no CHANGES_REQUESTED, no current
   unresolved threads). High-risk and unlabeled-risk PRs are not armed.
2. **Protected-path guard** (`_pr_touches_protected_path`, mirrors `auto-merge-rhythm.yml`): a PR
   touching `.github/workflows`, `.github/scripts`, `.codex`, `.openclaw`, `AGENTS.md`,
   `CONSTITUTION.md`, `DECISIONS.md`, `VAULT-CONVENTIONS.md`, `swarm.json`, or `!/*` is **never**
   auto-armed — it waits for human review. Fail-closed: if the changed-file list can't be
   fetched, the PR is treated as protected.
3. **The merge queue + branch protection** gate the actual merge.
4. **The kill-switch**: set `AGENT_AUTO_MERGE_ENABLED = False` to fail-close arming again.

## Where arming fires (event-driven, not cron)

- `sync-pr` (`pull_request_target`): after a push clears the last thread.
- `review-submitted` (`pull_request_review`): after a review clears the last block.
- The manual `batch-arm-merge-queue.yml` remains the bulk/backlog protocol tool.
- `engage-outdated` stays **resolve-only** (its stated contract: "never merges, never arms"); a
  PR it clears is armed by the next event-path pass or the manual presser, not by the engine's
  resolve verb.

## What this does NOT change

- The `auto-merge-rhythm.yml` sync-bot lane (Dependabot/dependency-sync) — it never keyed on
  author login and its narrow scope is still correct.
- #398's signing-identity question — still open and still worth doing for *commit-author* trust;
  it is simply no longer the blocker for *merge-gate* trust, because the queue now supplies that.

###### [["The world is quiet here."]]
