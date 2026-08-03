---
date created: 2026-06-19
author: "Claude — Claude Code instance (branch claude/needs-fix-dispatch-design)"
authority: "LOGAN-REVIEW-REQUIRED — a design proposal for the look-then-resolve engine's
  needs-fix lane. Records intended behavior for review; builds nothing. Authority to
  approve, amend, or shelve reserved to Logan."
doc_class: design
status: proposed
related:
  - "AGENT-AUTOMERGE-REENABLED-2026-06-17.md"
  - ".github/scripts/review_feedback_loop.py"
  - "!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md"
  - CONSTITUTION
---

# DESIGN — the `needs-fix` lane: dispatch the authoring agent to fix, never to stamp

*The last and most consequential apply-pass increment of the look-then-resolve engine
(#399). This is a design for review, not a built thing. Nothing here is wired yet.*

---

## Where this sits

The disposition router (#526 Layer C classification + #529 router) sorts every unresolved
bot review thread into one lane via `_thread_resolution_disposition`:

| Disposition | Built apply-pass? | What acts on it |
| --- | --- | --- |
| `outdated-resolvable` | **yes** (#575 event-driven, #576 reconcile) | witnessed attest-resolve |
| `looked` | n/a | already attested |
| `apply-suggestion` | **yes** (#577, propose-only) | flagged `review/suggestions-ready`; a human / the authoring agent applies |
| `needs-human` | n/a | waits for human judgment |
| **`needs-fix`** | **NO — this design** | *should* dispatch the authoring agent to fix |

`needs-fix` is a **bot-only, substantive finding with no mechanical fix** — the commented
lines still exist, there is no committable suggestion, and a human did not author it. Per
the #529 doctrine, *a reviewer thread is a caught error; the gate exists to make agents fix
it before `main`*. So a bare attest-and-resolve of a `needs-fix` thread is exactly the
rubber-stamp the gate exists to prevent. The engine must **never** resolve it by
attestation. It has to be *fixed*.

## The gap (why this is the heart)

Today the engine classifies a `needs-fix` thread correctly and then **stops**. The PR sits
`blocked` until a human (or an agent, by hand) reads the finding, writes a change, pushes,
and the thread resolves. This is precisely what stalled #551 — its substantive Codex
threads had to be hand-resolved because nothing dispatched a fix. Until this lane is built,
"engaged by default" still leans on a human for every real review finding.

`outdated-resolvable` (#575/#576) and `apply-suggestion` (#577) clear the threads that need
*no judgment*. `needs-fix` is where the substance lives. This is the increment that closes
the gap.

## Design

When the engine sees an unresolved `needs-fix` thread on a PR, it hands the finding to the
**agent that authored the PR** as a work item — it does not resolve, merge, or arm.

### 1. Identify the authoring agent

Reuse the existing swarm vocabulary (`CLAUDE.md` § Swarm Coordination): the `agent:*` label
on the PR (`agent:claude-code`, `agent:codex`, `agent:copilot`, `agent:gemini`), falling
back to the PR's head-branch prefix (`claude/…`, `codex/…`) and then the PR author. The
dispatch names a specific agent; if none can be determined, the thread escalates to
`needs-human` rather than dispatching blindly.

### 2. Dispatch as a work item (not a resolve)

The dispatch surface should ride the rails the vault already coordinates on, **not** a new
queue:

- **Primary:** a comment on the PR thread addressed to the authoring agent, carrying the
  finding (file/line, the reviewer's text, the thread URL) and an explicit instruction:
  *"Fix this on this branch; do not resolve the thread — the resolve is witnessed once the
  lines change."* Plus a label, e.g. `review/needs-fix-dispatched`, so the state is visible
  and mirrors to Linear.
- The authoring agent (a separate Claude Code / Codex / Copilot run, triggered by its own
  assignment mechanism) makes the change, pushes to the PR branch, and the **existing**
  witnessed resolve clears the thread on the next `sync-pr` event because the lines moved.

This keeps the engine's contract intact: **the engine dispatches; the authoring agent
fixes; the resolve stays witnessed.** The engine never writes code and never stamps a
finding closed.

### 3. The loop-guard (the safety-critical part)

A dispatched fix that does not satisfy the reviewer must **not** re-dispatch forever. The
dispatch records an attempt count (in the dispatch marker, parallel to the `looked:` marker
grammar). After **N attempts** (proposed default: 2) the thread escalates to `needs-human`
and stops dispatching — a finding the agent cannot resolve in N tries is a human's call,
not an infinite loop. The marker also prevents duplicate dispatches within an attempt (one
open dispatch per thread at a time).

### 4. Witnessing and idempotency

- The dispatch comment carries a structured marker (`<!-- needs-fix-dispatch: by=…;
  thread=…; attempt=N; v=1 -->`) so re-runs detect an open dispatch and don't repost
  (no comment spam — the same idempotency discipline as the `looked:` markers and the
  `review/suggestions-ready` label).
- Nothing is resolved by the dispatch. Resolution remains the witnessed path, earned by the
  fix.

### 5. Where it fires

Event-driven, consistent with the rest of the engine — **no cron**:

- `sync-pr` (`pull_request_target`): when a push leaves a `needs-fix` thread unresolved.
- `review-submitted` (`pull_request_review`): when a new review adds a `needs-fix` finding.
- `reconcile-open-prs` (push-on-main, post #578): the backlog sweep dispatches any
  `needs-fix` thread without an open dispatch.

## Scope / safety posture

This is the highest-consequence lane: it sets off code-fixing work in response to bot
output. Proposed conservative rollout:

1. **Dispatch-only, never merge/arm.** The engine's act ends at "asked the authoring agent
   to fix." Arming remains gated on the existing eligibility + protected-path + merge-queue
   rules.
2. **Guinea-pig first.** Wire it behind an explicit opt-in (a flag or a single `--pr`
   scope, mirroring how `engage-outdated` proved one PR before the backlog walk), prove one
   real `needs-fix` dispatch end-to-end, then widen.
3. **Protected paths:** dispatch is *surfacing*, not a write or a merge, so it is arguably
   safe on every path — but the conservative first cut may restrict auto-dispatch to
   non-protected PRs and leave governance/CI findings to a human, matching the arming guard.
   **(Open question — see below.)**
4. **Loop-guard hard cap** (N attempts → `needs-human`) is non-negotiable; it ships in the
   first cut, not as a follow-up.

## Open questions for Logan

1. **Dispatch surface** — a PR comment addressed to the agent (visible, rides existing
   rails) vs. a dedicated GitHub Issue with the `agent:*` label (more formal hand-off,
   heavier) vs. a DOCKET entry. Which fits how the swarm actually picks up work?
2. **Who actually executes the fix?** This design dispatches; it assumes the authoring agent
   has a mechanism to *receive* the assignment and run. Does that mechanism exist today, or
   is "the agent notices the comment/label and acts" still manual? If manual, the first cut
   is really "surface a needs-fix work item for the agent/human," same shape as #577's
   propose-only — and the autonomous fix loop is a later increment.
3. **Attempt cap** — is N=2 right before escalating to `needs-human`?
4. **Protected paths** — auto-dispatch everywhere (it's only surfacing), or restrict to
   non-protected PRs in the first cut?

## What this is not

- Not a resolver. It never attest-resolves a `needs-fix` thread; the resolve stays earned by
  a real fix, witnessed.
- Not a merger/armer. Arming is the existing event/eligibility path; the merge queue +
  branch protection remain the gate.
- Not built. This document is the plan; implementation waits on Logan's answers above.

The world is quiet here．Esto Perpetua!
