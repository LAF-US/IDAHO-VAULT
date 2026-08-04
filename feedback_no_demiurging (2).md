---
name: feedback-no-demiurging
description: "Before proposing schemas, frameworks, or audits in IDAHO-VAULT, read existing GitHub issues, `VAULT-METADATA-STANDARD.md`, `VAULT-TEMPLATES.md`, `VAULT-CONVENTIONS.md`, and `CONSTITUTION.md` first. Logan calls the failure mode \"Demiurging\" — agents fashioning doctrine as if originating it, when the doctrine already exists."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ebcc146-08af-4d98-8ba6-b8b3b366018d
---

Before proposing any new schema, framework, retrofit plan, or architectural framing in IDAHO-VAULT, read the existing canonical sources first:

- `VAULT-METADATA-STANDARD.md` — frontmatter contract
- `VAULT-TEMPLATES.md` — note-class templates
- `VAULT-CONVENTIONS.md` — vault structure and naming
- `CONSTITUTION.md` — canonical governance authority
- `!/AGENTS.md` — agent registry and capability tiers
- **All open GitHub issues** (`gh issue list --state open`) — Logan tracks active concerns here; many issues contain fully-formed approaches he wrote weeks ago that the current "fresh" framing duplicates

**Why:** On 2026-05-22 Logan named the failure mode "Demiurging" — after the Gnostic lesser-creator who fashions the material world believing himself the supreme deity, having forgotten he was emanated from a higher source. Vault agents (myself included that morning) walk into a session, find a problem, propose a fresh framework, and stamp `authority: LOGAN` on it — operating as originators while erasing both the existing doctrine and their own derivative position. Logan reported this happens "every time I talk to them." The conversation pattern resets every session because each agent rediscovers the problem instead of advancing the tracked work.

Concrete case: issue #252 (open since 2026-04-18, the *only* substantive human-opened open issue at time of writing) specifies a phased metadata standardization approach — define governed subset, add read-only scanner, enforce on new/edited, triage legacy. `VAULT-METADATA-STANDARD.md` already defines a three-axis attribution model (`authority`, `authors`, `source`) that does exactly what fresh "provenance/emanation/authority" framings keep reinventing. The morning of 2026-05-22 I audited the corpus and proposed a parallel framework without reading either, then walked it back when Logan named the trap.

**How to apply:**
- When Logan describes a failure or asks for an audit, **first** check whether there's an open issue, doctrine file, or convention document that addresses it. Do not generate fresh framing until you've ruled out existing framing.
- When the existing doctrine is correct but underadopted, the work is **adoption**, not redesign. Propose the next concrete unblocked step from the existing plan, not a new plan.
- When proposing new vocabulary (e.g. "emanation," "Snicket model"), check whether the existing vocabulary already encodes the operational version of the same rule. If it does, *use the canonical vocabulary in vault writes*. Reserve new framings for chat exploration only, and never let them enter the vault under `authority: LOGAN` as if Logan had endorsed them.
- The Snicket-style declared mask applies to AI-as-author: if you contribute to a vault file, your name belongs in `authors:`, not absorbed into `authority:`. Logan is the authority over the document; you are the writer. Two slots, two roles, two values. See [[no-freelance-prs]] for the action-level corollary.
