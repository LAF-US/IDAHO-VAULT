---
title: "Protocol Snapshot from Codex"
date: 2026-05-18
status: snapshot
authority: LOGAN
source: Codex MacBook review
related:
  - CONSTITUTION
  - PROTOCOL
  - AGENT-PROTOCOL
  - LEVELSET
  - PROTOCOL-SUITE-AWR
  - CONVENE
  - CONFERENCE
  - STATUS-CONFERENCE
  - SIGNAL
  - PROTOCOL-PASSBACK-SYNC
  - LAF-USB-PROTOCOL-FRAMEWORK
---

# Protocol Snapshot from Codex - 2026-05-18

This snapshot records Codex's read-only review of existing working, draft, and proposed protocolsets in IDAHO-VAULT. It is an inventory and stabilization aid, not a new protocol.

## Main Finding

The vault already has a real protocol stack, but authority is split across approved `v1.0` files, root draft aliases, active operational notes, and historical/proposed artifacts. The canonization task should mostly be consolidation and de-duplication, not invention.

## Strongest Canon Candidates

- `CONSTITUTION.md` already names "CORE WORKING-SWARM PROTOCOLS TODAY."
- Approved lifecycle files:
  - `ARISE-v1.0-2026-04-27.md`
  - `AWAKEN-v1.0-2026-04-27.md`
  - `ORIENT-v1.0-2026-04-27.md`
  - `CONTEXT-v1.0-2026-04-27.md`
  - `CONVENE-v1.0-2026-04-27.md`
  - `CONFERENCE-v1.0-2026-04-27.md`
  - `RISE-v1.0-2026-04-27.md`
  - `REPORT-v1.0-2026-04-27.md`
- `AGENT-PROTOCOL.md` is active, practical, and tied to actual bootstrap behavior.
- `!-REPO-SLIMMING-PROTOCOL.md` is active, concrete, and already framed as review-first rather than delete-first.

## Working But Needs Canon Pass

- `LEVELSET.md` is important, but still `status: draft`. It has the correct 2026-05-17 correction deprecating `LEVELSET-CURRENT.md`.
- `PROTOCOL.md` is a useful vocabulary layer, but still draft and contains mixed operational/persona-heavy material.
- `PROTOCOL-SUITE-AWR.md` is the older draft.
- `!/PROTOCOL-SUITE-AWR.md` is the active integration version and is identical to `PROTOCOL-SUITE-AWR (2).md`; it needs one canonical copy.

## Draft / Proposed Protocolsets

- `PROTOCOL-STATUS-CONFERENCE.md` is a strong adoption candidate. It solves real readiness and collision issues.
- `SIGNAL.md` is a useful event-push concept, still draft and branch-salvaged.
- `PROTOCOL-PASSBACK-SYNC.md` is useful for terminal context extraction, but draft and old-path references need cleanup.
- `LAF-USB-PROTOCOL-FRAMEWORK.md` is staged, relatively disciplined, and a good infrastructure candidate.
- `AUTO-SYNC-MANIFEST-FRAMEWORK-2026-05-03.md` is an active research note, not yet a protocol.

## Risks / Inconsistencies

- Root aliases like `AWAKEN.md`, `REPORT.md`, `CONVENE.md`, and `CONFERENCE.md` are discoverable but still draft/stub-flavored while approved `v1.0` files exist.
- `CONSTITUTION.md` appears stale on `ARISE`: it says `ARISE v0.1` is draft, but `ARISE-v1.0-2026-04-27.md` says approved.
- `RISE-v1.0-2026-04-27.md` and `REPORT-v1.0-2026-04-27.md` still route state-affecting output to `LEVELSET-CURRENT.md`, which `LEVELSET.md` now explicitly deprecates.
- XKCD is now correctly quarantined/de-escalated; keep it out of canon except as an anti-standard warning.

## Recommended Canonization Order

1. Declare the approved `v1.0` lifecycle files canonical and make root aliases point clearly to them.
2. Promote or revise `LEVELSET.md` because everything else depends on it.
3. Clean `PROTOCOL.md` into a small vocabulary layer.
4. Decide whether `STATUS CONFERENCE`, `SIGNAL`, and `PASSBACK/TOSS` become active-minimal or remain drafts.
5. Keep LAF-USB / Auto-Sync separate as infrastructure protocols, not general swarm governance.

## Operating Principle

This snapshot supports the current direction: stabilize and canonize working project protocols that have survived actual use. Do not proliferate new standards when the work is to clarify the existing stack.

###### [["The world is quiet here."]]
