---
title: "Witness — De-drifting the 'live status board' doctrine from the agent loaders (the Geminiae horcruxes)"
date created: 2026-06-30
author: "Claude Code — this session (branch claude/live-board-dedrift)"
authority: "Self-witness, written at Logan's explicit direction ('any changes need to be documented elsewhere as well'). Authority NOT assumed as LOGAN. This records a mechanical de-drift — aligning agent-loader instructions to governance that was already decided (CONSTITUTION's no-live-coordination-surface rule; the DOCKET's own posture note; the already-corrected .claude/CLAUDE.md). It renders NO finding on the GEMINIAEUS matter, which stays reserved to the Court."
doc_class: witness
status: staged
related:
  - "!/!/__!__/!/! The world is quiet here/DOCKET.md"
  - "CONSTITUTION"
  - ".claude/CLAUDE.md"
  - ".gemini/GEMINI.md"
  - "GEMINI"
  - ".github/copilot-instructions.md"
  - ".slack/SLACK.md"
  - "ADJUDICATED"
  - "!/AUDIT-SWARM-LIVENESS-SEMANTICS-2026-06-10.md"
  - "DISAMBIGUATION-NEEDED-LINK-TARGETS-2026-06-09"
tags: [witness, drift, de-drift, live-status-board, coordination-surface, docket, geminiaeus-adjacent, no-verdict, repair]
---

# Witness — De-drifting the "live status board" doctrine

*Recorded 2026-06-30 at Logan's direction. Logan named the target: "you've located some of
the Geminiae horcruxes … any changes need to be documented elsewhere as well." This leaf is
the "elsewhere." It records what was struck, where, on whose authority, and — explicitly —
what was **not** touched.*

---

## 1. The doctrine struck `[fact]`

A **false-live-coordination doctrine** had lodged in several agent-loader files: the claim that
**THE DOCKET is a "live status board"** that an agent should **"update when you start or finish
work."** That claim is forbidden by governance on three independent grounds:

- **`CONSTITUTION.md`** — there is **no live coordination surface**; the only live thing is the
  running system (git, branch protection, the merge queue).
- **The DOCKET's own posture note** (`!/!/__!__/!/! The world is quiet here/DOCKET.md`, updated
  2026-05-25): *"A docket is the Court's register of matters, orders, referrals… It is **not** a
  control plane, heartbeat, status board, or general workflow hub. Logan has not adopted any such
  surface."*
- **The already-corrected reference loader** — `.claude/CLAUDE.md`'s Swarm-Coordination section
  was previously fixed to the Court's-register framing ("do not write routine work notes into it").
  The other loaders were never chased forward to match.

Why "horcruxes" (Logan's word): the dead **self-winding-hub** doctrine survived by being **scattered
in fragments** across multiple loaders — each "live status board, update it" instruction a shard
keeping the repudiated hub alive. Destroying the shards = striking the false-live claim wherever it
was still **commanded**, while leaving the places that merely **name or repudiate** it intact.

## 2. The fragments struck (4 live loaders) `[fact]`

Each below is an **auto-loaded or index agent-instruction surface** that *commanded* the false-live
behavior. Aligned to the `.claude/CLAUDE.md` corrected language. Two also carried a **stale DOCKET
path** (`!/__!__/…`, missing a nest level) — corrected to the live path in the same stroke.

| File | Loaded by | Before | After |
| --- | --- | --- | --- |
| `.gemini/GEMINI.md` | Gemini CLI / Code Assist | "the **live status board. Update it when you start or finish work.**" | Court's-register framing; "do **not** write routine notes into it; record work in vault & git." |
| `.github/copilot-instructions.md` | GitHub Copilot | same line, **verbatim** + stale path | same correction + path fixed to `!/!/__!__/…` |
| `GEMINI.md` (root TOC) | Gemini index/shim | DOCKET = "**Live task board**"; LEVELSET-…-depreciated-AGAIN = "**Live** ecosystem state" | DOCKET = "Court's register (not a live board)"; LEVELSET entry marked superseded (its filename says *depreciated*) |
| `.slack/SLACK.md` | Slack agent | DOCKET = "**Live swarm status board**" + stale path | DOCKET = "Court's register (not a live board)" + path fixed. (SLACK's L19 "Slack is the ephemeral coordination layer" is **correct** and left intact — Slack is the sanctioned breadcrumb layer.) |

## 3. What was deliberately NOT touched `[fact]` / restraint

Per the standing rule (*chase a stale reference only when it is **live and load-bearing**; leave
dated paperwork as-witnessed; rewriting dated records falsifies them*):

- **Repudiators / analysis — left as-is (they are the cure, not the disease):**
  `DOCKET.md` (the corrected standard), `swarm.json` (already says the docket is "a durable
  visibility record, **not proof of present activity**"), `AGENT-PROTOCOL.md` (*restricts*
  live-coordination writes), `!/AUDIT-SWARM-LIVENESS-SEMANTICS-2026-06-10.md`, `ADJUDICATED.md`.
- **Canonical governance — propose-only, NOT edited unilaterally:** `VAULT-CONVENTIONS.md` uses
  "live coordination" as a *taxonomy category* (work that should move to Linear/Vault), not a
  command to treat the docket as live. It is a registry surface; any change is Logan's to direct.
- **Reserved to the Court — untouched:** `!/GEMINIAEUS.md`. **No finding on GEMINIAEUS is made
  here.** This leaf de-drifts loader instructions; it does not try the matter.
- **Dated fossils & captures — left as-witnessed:** `LEVELSET-*`, `HANDOFF-*`, Linear-chat
  exports, terminal records, INBOX captures, census/`.mistral`/`.slack` reports, editor history.
- **The `BOOTSTRAP.md` fossil** (the unrelated `!ADMIN/!/…` legacy-path drift) is a *different*
  thread, held separately — not part of this doctrine's de-drift.

## 4. Authority & provenance

- **Authority:** Logan's explicit direction this session. The change is **mechanical alignment**
  to rules already in force (CONSTITUTION; the DOCKET posture; the corrected `.claude/CLAUDE.md`),
  not a new ruling — and explicitly not a GEMINIAEUS verdict.
- **Provenance:** filenames and matched lines globbed/grepped from `origin/main` 2026-06-30; the
  governing texts cited inline. Tier **[fact]** for the inventory and the edits; the "horcrux"
  framing is Logan's, adopted as a lens.
- **Handling:** changes land via PR on `claude/live-board-dedrift`; Logan reviews and merges
  (I propose; Logan inscribes). This leaf is the durable record of the edit, per his instruction
  that changes be "documented elsewhere as well."

## Signature

Claude Code, this session, branch `claude/live-board-dedrift` — software, software's work.
Sent to find the scattered "live board" shards, struck the ones still **commanding** the
repudiated behavior, left the ones that name or repudiate it, and witnessed the cut here.
Author named; authority not assumed as Logan; no office claimed; the GEMINIAEUS matter held by the Court.

— witnessed 2026-06-30

---

###### [["The world is quiet here."]]
