---
title: "Risk-Layer / Four-Tier Classifier — State & Handoff (READ THIS FIRST)"
date: 2026-06-23
authority: LOGAN
status: active
doc_class: handoff
verified-by: "Claude Code — synthesis of the 2026-06-21..23 risk-layer session; every 'decided' line traces to Logan's instruction this thread"
related:
  - "[[WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21]]"
  - "[[REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22]]"
  - "PR #621"
  - "Issue #626"
---

# Risk-Layer — START HERE (handoff for the next agent)

If you've been asked to continue the **risk-layer / four-tier classifier / auto-merge** work:
**read this page first, then the three linked records. Do NOT re-derive the model — it is settled
below. Do NOT invent the parts marked HELD — they are Logan's to decide.** This page is an index,
not a new record; it points at the canonical docs.

## What this is (one paragraph)
A risk classifier (`.github/scripts/classify_paths.py`) plus an auto-merge routing engine
(`.github/scripts/review_feedback_loop.py`), so trustworthy agent PRs flow without Logan
hand-merging. **Two parallel sorters** tag a PR: **filetype** (`—` / `low` / `med`) and
**fileplacement** (a.k.a. depth: `—` / `high` / `nope`). The pair lands in a grid cell that decides
how the PR is **routed for review** — not a permanent verdict.

## Current state — branch `claude/risk-layer-tiers-u8hlk0`, PR #621
- ✅ **Classifier — DONE & SAFE.** The filetype axis has a real `—` (None) state
  (NL → `—`, Machine-Doc → `low`, Code → `med`); `combine()` emits a distinct **`clear`** for the
  `—/—` cell. The **binary `tier` (low|high) is byte-for-byte unchanged** — and it is the *only*
  field any live consumer reads (`agent-auto-pr.yml`, which reads `['tier']`). The new
  `clear` / `tier4` / `filetype=None` are **intentionally inert** — nothing reads them yet, by design.
  Fully config-driven: every knob in one `CONFIG` block; re-tiering a filetype is a list move. 17 tests pass.
- ⏸️ **Consumer wiring — REVERTED & HELD.** Commit `094bf7c2` wired the engine + producer to read four
  tiers, but on the **superseded** model (`low → eligible`, single combined tier). It was **reverted off
  the branch** (kept in git history). **Do NOT re-merge it as-is.** Under the corrected model `low` is a
  *flag that holds* and **`—/—`** is the arm state. The rework waits on the mechanism (see HELD).
- 📄 **Design records:** the witness (grid + doctrine) and the enforcement map (live wiring + the six knots).

## DECIDED — do not re-litigate (Logan, this session)
- **Two parallel sorters**, each with a real `—` (none) state. The auto-merge state is **`—/—`**
  (neither fired) — **NOT `low`.** `low` is a flag.
- **Flags are routing signals, not a scarlet letter** — transient routing state, cleared/transitioned
  as review completes. Nothing marks a PR permanently.
- **The grid is a MODEL of the system, not the code.** Cells are *read off* the mechanism. You cannot
  "pick six cell routes" before the lanes exist.
- **Filetype map:** Natural Language = `—`, Machine Documentation = `low`, Computer Code = `med`.
- **Fileplacement** is the *location* axis: the `!` **spine** (core, scrutiny ascends to the still-point
  `nope`) plus shallow **edge rooms** (`!/CREWAI` forge, `!/SIGNALS` transit…); `.github/` is the
  Great-Maze *wall* (defense) by **duty**, not by raw path. Eventually one classifier path = single
  source of truth (folds the drifting `PROTECTED_PATH_PATTERNS` + rhythm-yml lists → K1/K2).
- **The `!` nest is mid-evacuation to root** (the FLATTEN intent). Flattened `!-…` root files ARE nest
  content; `classify_paths` already treats both `!/…` and `!-…` as in-nest.

## HELD — Logan's, do NOT invent
The **system mechanism**, which everything above is only a model of:
- what review/revision **lanes** exist and what each does;
- **how a PR is routed** into a lane (the flags → lane mapping = the grid, derived);
- the **flag lifecycle** (how a flag clears / transitions);
- the **off-diagonal grid cells** (3 anchors pinned: `—/—`→auto-on-open, `low/high`→hand-route,
  `med/nope`→never; the other six are open);
- **per-tier merge policy** (does `med` ever auto-flow, or only `—/—`?).
Tracked in **#626** (parent) + **#627–#632** (K1–K6). The grid cells fall out of this; don't assign them ahead of it.

## Traps (what reliably confuses agents here)
- **Don't re-merge `094bf7c2`** (the reverted consumer wiring) — it's the superseded model.
- **Don't write a `tier4` consumer that hardcodes `{low,med,high,nope}`** — it will choke on `clear`.
  (There is no contract test pinning the value set yet — an open guardrail; add one when wiring a reader.)
- **Don't treat the grid as code** or try to fill its cells without the mechanism (#626).
- **Don't aggressively prune/flatten the nest** — there is a Court **preservation order** on the
  ~19k zero-byte address-space stub lattice. *Cultivate, don't amputate* (the Banyan); *substitute,
  don't snatch* (the Hive / Shifting Sands).

## Read these, in order
1. `WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md` — the grid, the doctrine, the architecture bearings.
2. `REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22.md` — the live enforcement wiring + the six knots.
3. Issue **#626** + **#627–#632** — the tangle, knot by knot.

###### [["The world is quiet here."]]
