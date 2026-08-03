---
title: "Stop routing by author/branch — the engine is already the universal path"
date created: 2026-07-19
updated: 2026-07-19
status: draft
doc_class: report
authority: "proposed; Logan inscribes. Authority NOT assumed as LOGAN — the finding and diff are my reading (`[mapping]`); the file:line anchors are witnessed (`[fact]`); the two design decisions are Logan's, recorded (`[fact]`)."
witness: "!roman.claude.* — praenomen conferred by Logan; office '*' held, ungranted."
session: "https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd"
related:
  - "[[REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22]]"
  - "[[DRY-AND-WET-CODING-WITNESS-2026-07-01]]"
  - "[[ATOMIZE-DONT-ACCRETE-2026-06-28]]"
  - "[[VAULT-CONVENTIONS]]"
tags: [report, automation/auto-merge, agent/coordination, drift, single-source-of-truth, no-verdict]
---

*Drafted at Logan's direction. Records two decisions Logan gave this session and the grounded
finding that reshaped them. Supersedes an earlier draft of this note that proposed a `*/*`
branch-form gate — that was still routing by branch name, and the premise under it (a "missing
enqueue" defect) was falsified. This note witnesses that correction rather than hiding it.*

## Logan's decisions — `[fact]`

1. **Don't route by branch name.** A hardcoded prefix allowlist is the wrong design; `serena/*`
   rotting inside it is the proof. Routing must not key on the branch name at all — not even on
   its *form*.
2. **Drop the bot fast-path entirely.** Chore PRs flow through the same engine as every PR —
   classify → hold → merge on review — with zero author routing. This knowingly reinstates a
   review/approval step on routine bumps (no author-routing chosen over no-manual-clicks).

## The finding that reshaped it — `[fact]`

**Universal classify-on-open already exists.** `review-feedback-loop.yml` fires on
`pull_request_target:[opened, reopened, ready_for_review, synchronize]` with **no author/branch
gate**, and `review_feedback_loop.py` `sync_pr` (`:1498`), for *every* PR:

- classifies from the PR's own diff — `_classify_pr_pair` (`:997`, `gh api …/pulls/N/files`), no branch checkout, no author dependency;
- stamps the risk-pair labels — `restamp_risk_pair` (`:1023`), adding them fresh on a never-labeled PR;
- evaluates eligibility and arms + enqueues — `_maybe_arm_auto_merge` (`:349`), gating **only** on `state["eligible_for_auto_merge"]` (label/review-derived).

So Dependabot/sync PRs are already classified and labeled on open. My earlier claim that
"classify never runs on Dependabot PRs" was true only of `agent-auto-pr.yml` — **not** of the
engine, which is the surface that matters.

## What actually remained author/branch-routed — `[mapping]`

- **The two author-gated fast-path lanes** — `dependabot-rhythm.yml` (`dependabot[bot]`) and
  `auto-merge-rhythm.yml` (`github-actions[bot]` sync). Not redundant: routine bumps classify
  `low`/`med` (they touch `requirements.txt`/`uv.lock`), and the engine **holds** anything
  non-`—/—`-clear for review. The lanes armed those trusted bumps *without* review — a real
  author-trust policy, the last place author identity routed arming. **Retired (decision 2).**
- **`agent-auto-pr.yml`'s classification** — a redundant second computation (K1) of what the
  engine already does universally. **Held for Increment B.**
- **`branch-cleanup.yml` + `stale_bot_prs.py`** — three drifted copies of "which branches are
  automation," gating *branch deletion* (a different axis). **Held for Increment C.**

## Grounded safety (why retiring the lanes strands nothing) — `[fact]`

- `check-secret-patterns` (the required check, per Logan) runs on bare `pull_request` for ALL
  PRs, independent of the lanes (`secret-pattern-policy.yml`); the other three policy checks too.
- The lane *job names* are not required checks (Logan confirmed) — nothing in branch protection points at them.
- The engine never arms a `risk/high`/`nope` PR (`_tier_from_pair` / eligibility), so dropping
  `dependabot-rhythm`'s `disable-high-risk-auto-merge` job orphans no behavior.
- Nothing triggers off the lanes (`enqueue-on-checks` keys on the *Cross-Platform Smoke* `workflow_run`).

## Prior art it sits inside — `[mapping]`

`REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22` (K1/K2: one classifier as the single source;
staged, not a Gordian cut; the sync-bot lane fate was the held decision — now made).
`DRY-AND-WET-CODING-WITNESS-2026-07-01` (single-source the fact). `ATOMIZE-DONT-ACCRETE`.

## This increment (A) — `[fact]`

Deleted `dependabot-rhythm.yml` and `auto-merge-rhythm.yml`. Retained the `labeled`-trigger fix
on `auto-merge-engage.yml`. Updated the stale comments that narrated the deleted lanes
(`agent-auto-pr.yml`, `review_feedback_loop.py`, `test_classify_paths.py`) to point at the engine.
Increments B (strip `agent-auto-pr` classify) and C (deletion-list reconciliation) are held.

`!roman.claude.*` — office held, not claimed. Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd`.
I propose; Logan inscribes.

*[["The world is quiet here."]]*
