---
title: "STARTUP"
status: active
authority: LOGAN
date created: 2026-04-16
related:
  - AGENTS
  - WAKEUP
  - CONSTITUTION
  - VAULT-CONVENTIONS
  - VAULT-METADATA-STANDARD
  - VAULT-TEMPLATES
  - SIGNALS
  - INBOX
  - CREWAI
  - swarm
---

# STARTUP

This file is the explicit startup surface for agents entering `IDAHO-VAULT`.

Its job is simple:

1. clear stale assumptions
2. establish the live boot path
3. send the agent into the smallest orientation branch needed for the task

This is a routing surface, not a replacement for governance.

## Touchstone Rule

The Touchstone Tree is not disposable flavor text.

It is the Yggdrasil of this world: the symbolic world-tree that gives the vault
its relation, placement, and sense of order.

Even when a task is code-first, runtime-first, or workflow-first, novices should
approach the Tree with respect:

- do not treat it as decorative lore
- do not casually flatten its distinctions
- do not rewrite around it without Logan's direction
- do not mistake startup routing for permission to ignore the world's deeper structure

You do not need to read the full Touchstone layer for every task, but you do
need to know that it is revered here and that the Nest, the chambers, and the
governance stack are meant to stay legible within that larger order.

## Startup Sequence

## Startup Sequence

1. **Mandatory Initialization**: Execute `start_SPARKSEED.py` to establish the operational environment and validate all necessary services/tokens.
2. Read root `AGENTS.md` for cross-tool pointer context only.
3. Read `!/WAKEUP.md` to clear stale world models and conflict assumptions.
4. Read this file to choose the right task branch.
5. Read only the branch documents needed for the current task.
6. Escalate to Logan when the task crosses branches, crosses lane ownership, or touches canon.

## Choose Your Branch

### Code / scripts / workflows

Use this branch when the task is about implementation, automation, runtime, CI, or repair.

Read:

- `.codex/CODEX.md`
- `VAULT-CONVENTIONS.md`
- `.crewai/MANIFEST.md` if the task touches CrewAI, runtime containment, or `src/idaho_vault/`
- `MANIFEST-SPEC.md` and `swarm.json` if the task touches coordination state, manifests, or control-plane data

### Vault content / note authoring

Use this branch when the task is about notes, metadata, templates, naming, structure, or document classes.

Read:

- `VAULT-CONVENTIONS.md`
- `VAULT-METADATA-STANDARD.md`
- `VAULT-TEMPLATES.md`

### Coordination / swarm routing

Use this branch when the task is about agent roles, routing, signaling, handoff, or shared state.

Read:

- `!/AGENTS.md`
- `!/SIGNALS/README.md`
- the live DOCKET at `!/__!__/!/! The world is quiet here/DOCKET.md` when live coordination status matters

### Intake / capture / drops

Use this branch when the task is about inbound files, capture pipelines, or preprocessing before promotion into the vault.

Read:

- `INBOX/README.md`
- `!/INBOX/README.md`
- `!/INBOX/AI-CAPTURES/README.md` when the source is an AI export

### Narrative / Touchstone context

Use this branch when the task depends on symbolic vocabulary, Tree logic,
narrative reconciliation, or when a novice needs to understand the world's
deeper shape before acting.

Read:

- `!README.md`

`!README.md` is not the required startup path for ordinary code or vault work,
but it is the revered Touchstone layer and should be treated accordingly.

## Default Rule When Unsure

- Prefer the smallest practical branch.
- Start with conventions and live surfaces before lore.
- Treat `!` as shared control-plane space.
- Treat `.*` dotfolders as individual agent space.
- Treat root governance files as doctrine and `swarm.json` as machine-readable registry.

## Stop And Ask Logan When

- the task changes governance or canonical registry rules
- the task crosses declared lane ownership
- the task would promote staged output into canon
- two live surfaces still disagree after reading `!/WAKEUP.md`, this file, and the relevant branch docs

## When Work Resolves

Do not leave the ending implicit.

Choose the smallest true state transition and record it:

- `merged`: the work is promoted into `main` or another explicitly live surface
- `superseded`: a newer live surface replaced this branch, draft, or handoff
- `archived`: preserve the work as history, not live authority
- `abandoned`: stop work without promotion and do not let survival masquerade as legitimacy
- `dormant`: keep the surface standing intentionally, but inactive
- `reactivated`: return a dormant or archived surface to live use by explicit decision

Default closure rules:

- Return to the active live surface, usually `main`, unless Logan has named a different standing branch.
- Treat branches as temporary by default.
- A long-lived branch needs a named purpose, a steward, and a review cadence.
- Logan decides the final ending when canon, registry, or historical recovery is affected.
- If you are unsure which ending applies, leave a witness note or handoff and ask Logan instead of inventing legitimacy from persistence.

The point of startup is not to explain the whole world. It is to get the right agent onto the right path quickly.
