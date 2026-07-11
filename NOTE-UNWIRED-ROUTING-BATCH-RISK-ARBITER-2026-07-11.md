---
title: "NOTE — Batch Automation, Risk Labeller, and Arbiter Sortition: Three Unwired Pieces of One Intended Routing System"
updated: 2026-07-11
status: draft
authority: LOGAN
author: "Claude Code (no delegated persona, title, or office claimed this session)"
tags:
  - agent/coordination
  - ci/automation
  - github/merge
  - research/inquiry
related:
  - REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20
  - WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21
  - VAULT-CONVENTIONS
  - CONSTITUTION
---

# NOTE — Three Unwired Pieces of One Intended Routing System

*Filed by Claude Code, 2026-07-11, session `claude/practical-cerf-l13ka2`. Deferred by Logan's own direction: "note for now," not act now. No redesign proposed here — just the sourced observation, so it doesn't have to be re-discovered later.*

## What Logan said

> "The 'batch' automations were intended to be a varied set of flowchart logic-gate sequenced tools to route PRs to the appropriate fix lanes... but unfortunately the contractor cobbled everything together into several misleadingly named monoscripts."

> "it's a 'note for now' along with two adjacent yet related systems, the risk labeller and the sortition arbiter"

Both lines are Logan's own words, `[told]`, this session. Everything below is what I verified against the actual code today to ground that claim — not assumed from it.

## What I verified, per system

**1. Batch automation (`batch-arm-merge-queue.yml` + inline `gh` calls) — confirmed monoscript, no lane routing.**
Ran a live `dry_run: true` dispatch today (run `29162177905`) against all 32 open non-draft PRs. The script computes each PR's real `mergeStateStatus` (`CLEAN`/`UNSTABLE`/`BEHIND`/`BLOCKED`/`DIRTY`) but only branches on it into two buckets: `BEHIND` gets an actual branch-update, everything else not already `CLEAN`/`UNSTABLE` — whether it's `DIRTY` (a real merge conflict, 6 of 32 PRs today) or `BLOCKED` (failing checks or missing review, 23 of 32 PRs today) — gets the identical blind `gh pr merge --auto` no-op arm. There is no code path that distinguishes "needs conflict resolution" from "needs a check fixed" from "needs your review," despite the workflow's own header comments describing exactly that intended distinction ("DIRTY … is left for a human" — but the code arms it anyway, same as `BLOCKED`).

**2. Risk labeller (`classify_paths.py`) — the classifier exists; the routing was explicitly deferred, in writing, by a prior session.**
The script itself documents this. Its own top-of-file comment: *"the routing MECHANISM (lanes, flag lifecycle, grid-cell routes) is HELD for Logan — see issue #626 + `WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`. The grid is a model, not code."* So this isn't new: a prior session already built the two-axis classifier (`filetype: —/low/med`, `depth: —/high/nope`) that produces the `risk/*` labels visible on every PR, confirmed exactly one consumer reads it today — `agent-auto-pr.yml` reads the binary `tier` field only. Nothing else (not the batch arm script, not the arbiter sortition below) varies its behavior by risk tier at all.

**3. Sortition arbiter (`arbiter_sortition.py` / `arbiter-sortition.yml`) — fixed draw, no risk input.**
`--arbiter-count 2` is a constant passed from the workflow file, not derived from a PR's risk labels. The reviewer pool (`ALL_REVIEWERS`) is a flat hardcoded set of 5 bots + Logan; there's no tier-based expansion (e.g., more/stricter arbiters for a `depth:high` PR touching `.github/**`) despite the risk classifier sitting right there, already labeling every PR before sortition runs.

## The connecting thread

All three systems run on every PR, in sequence, and each one *could* read the risk classification the one before it produced — but none of them do except the single `tier` read in `agent-auto-pr.yml`. That's the concrete shape of "cobbled together into monoscripts" from where I sat today: not that any one script is broken, but that the intended flowchart (classify → route to a lane by risk+state → arbiter selection scaled to that lane) collapsed into three independent scripts that happen to run near each other, each blind to the others' output.

## Aside, possibly useful later (not part of the deferred item)

`arbiter_sortition.py`'s own comment documents a CodeQL modeling fact directly relevant to the open alert I'm currently working on PR #562: *"CodeQL's command-line-injection sanitizer only recognizes comparisons against a literal constant, and a regex `.fullmatch()` does not register as one."* That's independent, prior-session confirmation of exactly what I was inferring today from `install-skill-from-github.py`'s persistent CodeQL alert surviving two rounds of regex-based validation (`_validate_ref`/`_validate_owner_repo`). Worth remembering if that alert (or ones like it) comes up again: CodeQL wants a literal-constant comparison, not a regex match, to recognize a barrier.

## Status

Deferred, per Logan. Not touching `.github/workflows/**` or `.github/scripts/**` for this — logged so the next pass (mine or anyone else's) doesn't have to re-derive it from scratch.
