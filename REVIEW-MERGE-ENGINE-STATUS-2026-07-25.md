---
title: "Review/Merge Engine — Status Snapshot (Looker Extraction Begun)"
created: 2026-07-25
updated: 2026-07-25
status: active
authority: "LOGAN"
authors:
  - Claude Code
source:
  - "decision from Logan, 2026-07-25 (session_01Fipj4vEJ5ADPuunn9ed5Hd)"
  - "continues REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20 §5"
  - "code read from branch `claude/shall-rome-lyrics-ok9049`, 2026-07-25"
tags:
  - agent/coordination
  - github/review
  - github/merge
  - ci/automation
related:
  - REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20
  - AGENTS
  - CLAUDE
  - VAULT-CONVENTIONS
---

# Review/Merge Engine — Status Snapshot (2026-07-25)

*Filed by [[Claude Code]] (software NAME; no delegated TITLE or OFFICE this session) — 2026-07-25, session_01Fipj4vEJ5ADPuunn9ed5Hd.*
*Continues the Cluster A deep-dive of 2026-06-20, which mapped the knot and left §5 as a proposal awaiting Logan's decision. Logan has now decided. This snapshot records the decision and the start of the work — so it is not abandoned and re-derived a third time.*

---

## Decisions (Logan, 2026-07-25)

1. **The LOOKER shall be separated into its own system.** This answers the deep-dive's §5
   open question on concern D (the witness/attestation subsystem — `list-unlooked`,
   `looker-walk`, `render-worklist`, `attest-resolve`, `engage-outdated`, `reconcile-witness`,
   6 of the engine's 14 subcommands). It is extracted out of `review_feedback_loop.py`, not
   revived in place. This is the largest concern in the file and was already flagged (deep-dive
   F3) as "a separable tool wearing the engine's skin."

2. **The LABELS need a separate cohesion operation — later.** The label substrate (concern A,
   `ensure-labels` / `LABEL_SPECS`) and the review-state projection labels (concern B) get
   their own dedicated coherence pass as a **distinct, later operation** — not folded into the
   looker split, not started now.

---

## Boundary (code read 2026-07-25)

The looker does not sit in a clean corner of the file — part of it is genuinely shared with
the review-state path, which sets the safe extraction order:

- **Looker-only (clean to move):** `_build_looker_queue`, `_classify_pr_for_looker`,
  `list_unlooked`, `looker_walk`, `render_looker_worklist`, `render_worklist` — the
  read/classify/report side. No non-looker caller.
- **Shared with review-state (move with care, later):** `_resolve_outdated_resolvable_threads`
  (called by the sync path at `review_feedback_loop.py:1364` and `:1549`, not only by
  `engage_outdated`), and transitively `attest_and_resolve` and `_build_attestation`. These
  are the write side and are mocked extensively by `tests/test_review_feedback_loop.py`.

## Extraction order

1. **Read/classify side → its own module** (begun this session): the looker-only functions
   move to a standalone script; the three looker read subcommands leave the engine's parser;
   the `looker-walk` workflow repoints; the read-side tests move. Verified by the test suite.
2. **Write side** (next): extract `attest-resolve` / `engage-outdated` / `reconcile-witness`
   and settle the shared attest core — either duplicated into neither and imported by both, or
   held in a shared library (§5's "shared lib").
3. **Shared library** (§5): common plumbing (`_fetch_pr`, thread walking, label constants)
   imported by both systems, duplicated by neither.

## Sequenced for later (not this pass)

- The **label cohesion operation** (decision 2).
- Any move of the witness system to a schedule remains **off** the table: Logan's standing
  no-cron order governs; the looker stays `workflow_dispatch` / event-driven until the
  chron_clock is established.
