---
title: "Review/Merge Engine — Cluster A Deep-Dive (Map v1)"
created: 2026-06-20
updated: 2026-06-20
status: active
authority: "LOGAN"
authors:
  - Claude Code
source:
  - "code read from `main`: .github/scripts/review_feedback_loop.py + 9 Cluster A workflows, 2026-06-20"
tags:
  - agent/coordination
  - github/review
  - github/merge
  - ci/automation
  - research/inquiry
related:
  - AGENTS
  - CLAUDE
  - VAULT-CONVENTIONS
  - AGENTIC-GITHUB-REVIEW-BEST-PRACTICES-2026-06-15
  - AGENT-AUTOMERGE-REENABLED-2026-06-17
  - "!/ARBORSCAPE-PR-EXPANSION-2026-05-22"
  - GitHub
  - Claude Code
---

# Review/Merge Engine — Cluster A Deep-Dive

*Filed by [[Claude Code]] (software NAME; no delegated TITLE or OFFICE claimed this session) — 2026-06-20*
*Branch: `claude/github-reviewers-research-u8hlk0`*
*Class: research / INQUIRY — a runtime map of existing automation, **not** adopted policy. The redesign sketch in §5 is a proposal for Logan's consideration, not a decision.*
*Companion to GitHub issue #586 "Map v1" (workflow inventory + topology call-graph figure).*

---

## Provenance & Method

Every claim is sourced to a file/line read from `main` on 2026-06-20: the engine
`.github/scripts/review_feedback_loop.py` (2,221 lines) and the 9 Cluster A workflows in
`.github/workflows/` (6 engine-callers + 3 inline-`gh`; the §2 wiring table additionally lists
`agent-auto-pr` — a Cluster-B bridge that calls `ensure-labels` — for 10 rows total). Where a
statement is inference rather than a direct read, it is
marked *(inference)*. No runtime logs were consulted — this is a static read of the wiring,
not an observation of live executions.

---

## 1. The engine is four tools sharing one 2,221-line file

`review_feedback_loop.py` exposes **14 subcommands** (`build_parser`, L2042–2181; dispatch
in `main`, L2184–2213) that fall into four distinct concerns:

| Concern | Subcommands | What it does |
| --- | --- | --- |
| **A · Label substrate** | `ensure-labels` | Idempotently create the lifecycle labels (`LABEL_SPECS`, L113). Every other command calls it first. |
| **B · Review-state projection** | `sync-pr`, `review-submitted`, `acknowledge-apply`, `promote-ready`, `reconcile-open-prs`, `enable-auto-merge` | Translate GitHub review/check/thread truth → projection labels + the auto-merge pause/arm decision. |
| **C · Claim verification** | `verify-claim` | "Brass-mouth" check (IF 7, L53–57): compare an agent's *"work finished / ready to merge"* comment (`CLAIM_PATTERNS`, L59) against GitHub's real `mergeable`/checks; post a divergence note on disagreement. |
| **D · Looker thread-attestation** | `list-unlooked`, `looker-walk`, `render-worklist`, `attest-resolve`, `engage-outdated`, `reconcile-witness` | The witness subsystem: classify open PRs, then attest-and-resolve *outdated bot-only* review threads with a recorded looker identity. **6 of 14 subcommands — the largest concern.** |

---

## 2. Live wiring (workflow → trigger → subcommand → concern)

| Workflow | Trigger | Engine call | Concern | Live? |
| --- | --- | --- | --- | --- |
| `review-feedback-loop` | `issue_comment`; `pull_request_target` open/sync | `acknowledge-apply`, `sync-pr`, `verify-claim` | B + C | ✅ |
| `review-response` | `pull_request_review` submitted | `review-submitted` | B | ✅ |
| `auto-merge-engage` | `pull_request_target` open/sync | **`engage-outdated --apply`** | **D** | ✅ |
| `engage-outdated` | `workflow_dispatch` | `engage-outdated` | D | manual |
| `looker-walk` | `workflow_dispatch` | `looker-walk` + `render-worklist` (+ `issue_reconciler.py`) | D | manual |
| `agent-review-gate` | `workflow_dispatch` | `reconcile-open-prs` (+ `issue_reconciler.py`) | B | ❌ **DISABLED** |
| `agent-auto-pr` | `create`, `workflow_dispatch` | `ensure-labels` (+ `pr_lifecycle.py`) | A / bootstrap | ✅ |

Plus the three inline-`gh` arming workflows that call **no** engine script:

| Workflow | Trigger | Mechanism |
| --- | --- | --- |
| `auto-merge-rhythm` | `pull_request_target` open/sync | inline `gh pr merge --auto --merge`, re-deriving protected-path + branch-rule checks in bash |
| `dependabot-rhythm` | `pull_request_target` (+ labeled/unlabeled) | inline `gh pr merge --auto --squash`, Dependabot lane |
| `batch-arm-merge-queue` | `workflow_dispatch` | inline bulk `gh pr merge --auto` with disable/re-enable toggle for merge-queue repos |

---

## 3. Three findings — the actual shape of the knot

### F1 · Arming has two brains, and the engine's brain is dormant

The engine *re-enabled* auto-merge arming on 2026-06-17 (`AGENT_AUTO_MERGE_ENABLED = True`,
L51; see [[AGENT-AUTOMERGE-REENABLED-2026-06-17]]) because the GitHub merge queue is now the
trust gate. But the only workflow that reaches the engine's arming path
(`reconcile-open-prs`) is **`agent-review-gate`, which is explicitly disabled** — its own
header states it "runs the engine's retired risk-tier schema and does not work against the
current repo," and it is `workflow_dispatch`-only. No Cluster A workflow invokes
`enable-auto-merge` directly. (Scope caveat — see the Correction below: only *that gate's*
risk-based arming eligibility is retired; risk-tier *labeling* is still live.)

So **live arming happens entirely *outside* the engine** — in `auto-merge-rhythm.yml`
(inline `gh pr merge --auto` on every `pull_request_target`) and `dependabot-rhythm.yml`.
Those re-derive protected-path and branch-rule eligibility in bash (`gh api
rules/branches/main`) that the engine *already* encodes in `PROTECTED_PATH_PATTERNS` (L100)
and its eligibility logic. **Two implementations of "is this PR safe to arm" — one live
(YAML/bash), one dormant (Python).**

### F2 · `auto-merge-engage.yml` does not engage auto-merge

Despite the name, it calls `engage-outdated --apply` (L68–69) — concern **D**, the
thread-attestation pass. `engage_outdated` (L1930) is documented as "attest-resolve every
outdated-resolvable thread across open PRs … ONLY threads whose resolution disposition is
`outdated-resolvable` (bot-only, GitHub-outdated)"; it **does not arm merge**. The workflow
whose name promises arming is the one that resolves stale bot comments. This is the single
clearest symptom that the cluster's names and concerns have drifted apart.

### F3 · The looker/attestation subsystem (D) is a separable tool wearing the engine's skin

Six subcommands, 2–3 workflows, its own vocabulary (looker / attest / witness /
outdated-resolvable), and it only ever *reads* PR state and resolves threads — it never
touches labels or arming. `looker_walk` (L1760) is explicitly "Read-only — resolves
nothing"; the guarded disposition path is `attest-resolve`. It rides inside
`review_feedback_loop.py` only because both it and concern B need the same GitHub-thread
plumbing (`_fetch_pr`, thread walking). *(inference: the coupling is plumbing-sharing, not
domain overlap.)*

---

## 3.1 · Correction (2026-06-20, witnessed) — the risk-tier schema is NOT retired

Logan caught that #597 (this PR) was auto-labeled `risk/high`, which contradicts the
unqualified "retired risk-tier schema" phrasing carried into F1 above. That phrasing was a
direct quote of `agent-review-gate.yml`'s header, but presenting it without scope was
imprecise. The accurate picture, re-read from `main`:

- **Producer — LIVE.** `agent-auto-pr.yml`'s `classify` step pipes changed paths to
  `classify_paths.py`, which stamps `risk/<tier>` on **every** agent PR at creation
  (`agent-auto-pr.yml` L175). `classify_paths.py` is fail-safe: "Unknown paths default to
  high-risk" (L7, L67) — so #597's two **new root-level `.md` files** match no known low-risk
  pattern and rate `high`. That is why a docs-only PR is `risk/high`.
- **Consumer — LIVE.** `dependabot-rhythm.yml` reads `risk/high` as a hard auto-merge block
  (L17, L90, L99). The engine's `_risk_tier_for_pr` (L295) also reads the label as canonical.
- **Consumer — DISABLED.** The `agent-review-gate` reconcile/arming gate is the *only* thing
  the "retired risk-tier schema" header actually describes — its risk-based **arming
  eligibility**, not risk labeling as a whole.
- **Live non-Dependabot arming — ignores risk.** `auto-merge-rhythm.yml` contains **no**
  `risk` reference at all.

**Net (and this sharpens F1):** risk-tier labeling is a live producer with exactly one live
consumer (the Dependabot lane) and one dormant consumer (the disabled gate); the live
general arming path doesn't read it. So `risk/high` on a normal agent PR like #597 is
computed and stamped, but its only *teeth* are in the Dependabot lane — elsewhere it is a
human-facing signal whose automated consumer is dormant. The redesign in §5 should decide
whether `review-state` becomes the single live consumer of the risk tier, or whether risk
labeling is retired in fact rather than only at the dead gate.

---

## 4. Why this is the knot a redesign must resolve

Cluster A is effectively **one engine (`review_feedback_loop.py`) wearing six workflow
hats**, with `issue_reconciler.py` as the shared "report findings to an issue" substrate
under the survey workflows. The coupling is not accidental reuse — it is four separable
concerns braided into one file because they share GitHub-state plumbing and one
`PROTECTED_PATH_PATTERNS` / label-constant block. The arming logic is then *duplicated a
third time* in bash (F1), and the workflow names no longer name what they do (F2).

---

## 5. Shape of a single coherent engine (proposal — not a decision)

The knot resolves into **three tools over one shared library**, not one file:

1. **`review-state`** (concerns A + B + C) — the event-driven projector. One entry point
   reacting to PR/review/comment webhooks: recompute labels, verify claims, and make the
   *single* arm/pause decision — folding `auto-merge-rhythm`'s inline bash back into the
   engine so there is **one** arming brain, gated by the merge queue.
2. **`thread-witness`** (concern D) — the looker subsystem, extracted whole. Same plumbing,
   separate surface and schedule.
3. **shared lib** — `_fetch_pr`, thread walking, `PROTECTED_PATH_PATTERNS`, `LABEL_SPECS`:
   imported by both, duplicated by neither.

That collapses **9 workflows + 2 dormant/duplicated arming paths into 3 workflows over 1
engine**, and kills the F2 naming drift by making each workflow's name its subcommand.

**Open questions for Logan before any build:**

- Is the dormant engine arming path (`enable-auto-merge` / `reconcile-open-prs`) meant to be
  revived, or has the inline-`gh` rhythm permanently replaced it? F1's resolution depends on
  the answer.
- Should `thread-witness` keep its manual `workflow_dispatch` cadence, or move to a schedule
  now that `auto-merge-engage` runs the `--apply` pass automatically on every PR event?

---

*Next step (not taken): trace `issue_reconciler.py`'s 5 callers (Cluster B/C/E) to see
whether the "report to a find-or-create issue" substrate is similarly separable.*
