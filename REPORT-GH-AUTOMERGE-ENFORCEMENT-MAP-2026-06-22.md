---
title: "Auto-merge Enforcement Map — the live wiring and its tangle"
date: 2026-06-22
updated: 2026-06-22
authority: LOGAN
author: "Claude Code (software NAME; no delegated office) — enforcement map traced from the live .github/ surfaces 2026-06-22; authority field is recorded, not a claim Logan authored these lines (CONSTITUTION § I)"
doc_class: report
status: active
verified-by: "Claude Code — every claim below carries a file:line anchor read directly from the branch, not recalled"
related:
  - "[[WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21]]"
  - "[[AGENT-AUTOMERGE-REENABLED-2026-06-17]]"
  - "[[REPORT-GH-GATES-AUDIT-2026-05-25]]"
  - "[[REPORT-GH-AUTOMATION-AUDIT-2026-04-03]]"
  - "[[VAULT-CONVENTIONS]]"
tags:
  - report
  - agent/coordination
  - automation/auto-merge
---

# Auto-merge Enforcement Map

*Traced by Claude Code from the live `.github/` surfaces, 2026-06-22, as the grounded basis for
planning the four-tier-grid refactor (see [[WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21]]). This maps
**what enforces what today** — it is a map, not a plan. The grid refactor is **deliberate, staged
work, not a Gordian cut**; this document exists so that planning starts from the real wiring instead
of a remembered sketch.*

## TL;DR — the one-sentence shape

`classify_paths.py` runs **exactly once** (at PR creation) and its entire output survives only as a
**`risk/<tier>` label**; everything downstream keys off that label — **except** the arming engine and
the sync-bot, which **independently re-derive risk from hardcoded path lists**. So "risk" is decided
by **three separate mechanisms that must agree but can drift**, and the real merge is gated by the
**GitHub merge queue**, which none of this code controls.

## The chain (producer → label → consumer → arm → queue)

### 1 · Producer — the only place the classifier runs

- **`.github/workflows/agent-auto-pr.yml`** — on an agent branch push, opens the PR.
  - Runs `classify_paths.py` on the changed files (~L90), reads `tier` (binary) + `tier4`.
  - `ensure-labels` creates the `risk/*` labels (~L121), then `gh pr create --label "risk/$RISK_TIER"`
    (~L175) stamps the tier; adds `review/pending` when low (~L145).
- **`.github/scripts/classify_paths.py`** — the classifier. **No other workflow invokes it.**
- ⇒ **The label is the entire interface.** Nothing re-runs the classifier; the consumer reads the
  *label*, not the files.

### 2 · Consumer / arming engine — reads the label, presses the button

- **`.github/workflows/review-feedback-loop.yml`** — `sweep-review-threads` job (L40–66), on
  `pull_request_target` (opened / reopened / ready_for_review / synchronize) → `review_feedback_loop.py sync-pr`.
- **`.github/scripts/review_feedback_loop.py`**:
  - `_risk_tier_for_pr` (L1037) — reads the **label** (`risk/nope>high>med>low`), body is fallback only.
  - `evaluate_review_state` (L1056) — `eligible_for_auto_merge = AGENT_AUTO_MERGE_ENABLED and
    risk=="low" and not risk_nope and grace_elapsed and not merge_blocked` (L1094). `merge_blocked` =
    draft / CHANGES_REQUESTED / open current threads.
  - `_maybe_arm_auto_merge` (L277) — arms **only if** eligible **AND** `not _pr_touches_protected_path`.
  - `_arm_auto_merge` (L204) — `gh pr merge --squash --delete-branch --auto`; toggles off→on to
    re-fire the enqueue transition (merge-queue quirk, verified on #508); stamps `merge/auto` (L299).
  - `AGENT_AUTO_MERGE_ENABLED` (~L50) — the kill-switch (set False to fail-close arming).

### 3 · The real merge gate (outside this code)

- GitHub **branch protection + merge queue on `main`**. Arming only presses `--auto`; the PR merges
  only once the **required checks** pass: `check-secret-patterns`, `check-large-files`, `check-paths`,
  `check-dotfolder-anchors` (named in `auto-merge-rhythm.yml` L88). The merge queue is the distinct
  trust gate that let arming be re-enabled 2026-06-17 ([[AGENT-AUTOMERGE-REENABLED-2026-06-17]]).

### 4 · The second lane (dependency sync-bot only)

- **`.github/workflows/auto-merge-rhythm.yml`** — fires only for `github-actions[bot]` PRs titled
  `chore: sync requirements.txt and uv.lock` (L46–48). Has its **own** protected-path `case` list
  (L67), verifies the four checks itself, then `gh pr merge --auto --merge`.

### 5 · Reconciliation lanes (self-healing — the queue never re-fires `--auto`)

- `reconcile-open-prs` (L1565) / `_build_reconciliation_report` (L1287, re-arms at L1370), surfaced by
  `pr_loop_watchdog.py`; driven by `auto-merge-engage.yml` + `batch-arm-merge-queue.yml`. Re-runs the
  same evaluate→arm across all open PRs on a schedule, catching PRs that went green after their last event.

## The tangle (the knots, named)

> **K1 — risk is computed three times, three ways.** (a) `classify_paths.py` (filetype + depth →
> label); (b) `review_feedback_loop.PROTECTED_PATH_PATTERNS` (L102: `.github/*`, `.codex/*`,
> `.openclaw/*`, `AGENTS.md`, `CONSTITUTION.md`, `DECISIONS.md`, `VAULT-CONVENTIONS.md`, `swarm.json`,
> `!/*`); (c) `auto-merge-rhythm.yml`'s inline `case` list (L67). They overlap but are **not identical**
> and can drift independently.

> **K2 — the classifier already knows what the path lists re-check.** `classify_paths` pins
> `.github/`, governance files, and dotfolders to **`depth=high`** — the *same* surfaces that lists (b)/(c)
> protect. The consumer **ignores** that and re-vetoes by glob. The depth axis *should* be the single
> source of truth; today it is shadowed by two hand-maintained lists.

> **K3 — pending semantic flip.** Arming keys on `risk=="low"` (L1094). The grid says **`—/—`
> (no risk label) is the arm state and `low` is a *flag that holds*.** Flipping this naively would make
> the engine arm on the *absence* of a label — which also matches a **not-yet-classified** PR.

> **K4 — no positive "clear" marker.** Because of K3, distinguishing "classified `—/—`" from "never
> classified" needs a **positive marker** the producer stamps, not mere label absence.

> **K5 — merge-strategy mismatch.** The engine arms `--squash --delete-branch`; the sync-bot lane uses
> `--merge`. Two strategies live in one repo.

> **K6 — label namespaces interplay.** `risk/*` (classify), `merge/auto` (arming state, L84),
> `review/pending` (low-but-waiting). The grid's two parallel labels (`risk/<ft>` + `risk/<depth>`)
> must coexist with `merge/auto`'s disable-path bookkeeping (`apply_review_state_projection`).

## Implications for the grid refactor (planning inputs, NOT decisions)

1. **Producer must stamp the label *pair*** (`risk/<filetype>` + `risk/<depth>`), and `_risk_tier_for_pr`
   must read the pair → route per the grid cell, instead of collapsing to one tier.
2. **Resolve K2 first, or in lockstep:** route the protected-path veto **through the classifier's depth
   axis** so K1's three lists collapse to one source of truth. (Branch-protection's *own* required
   checks stay independent — those are GitHub-side, correctly.)
3. **K3/K4 together:** the arm gate becomes "`—/—` clear-marker present", never "no labels."
4. **All lanes must read the same model:** `sync-pr`, `reconcile-open-prs`, AND the sync-bot lane —
   or the sync-bot lane is explicitly carved out as a separate, narrow contract.
5. **Decide K5** (one merge strategy) as part of the same pass.
6. **Stage it.** Producer label-pair → consumer pair-read → veto-consolidation → clear-marker gate →
   per-cell routing. Each increment independently reviewable; none is a single cut.

## To plan (deliberate — held)

- Close the grid's six open cells (Logan; see the witness).
- Sequence the staged migration above into reviewable increments.
- Decide whether the sync-bot lane folds into the unified model or stays a separate contract.

###### [["The world is quiet here."]]
