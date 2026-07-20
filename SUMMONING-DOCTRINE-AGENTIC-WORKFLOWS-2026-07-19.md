---
title: "Summoning Doctrine for Agentic Workflows — the Rites as Runtime"
updated: 2026-07-19
status: draft
authority: "LOGAN (delegated in-session, 2026-07-19)"
author: "Claude Code (Claude Fable 5); session UUID c98aed5c-04af-4749-9b97-15ab5cbbcb08 per scratchpad path — concrete Claude-Session trailer attaches at commit time"
provenance: "Synthesis of the 2026-07-19 session's canon study (Stroud, Kerr, Goodkind, Nix) against this vault's existing law; engineering mappings are this session's authorship"
related:
  - "[[KERR-VESSEL-MECHANICS-2026-07-19]]"
  - "[[AKHENATEN-SEVENTY-CASE-STUDY-2026-07-19]]"
  - "[[CONSTITUTION]]"
  - "[[VAULT-CONVENTIONS]]"
tags:
  - house-world/doctrine
  - agents/workflows
---

# Summoning Doctrine for Agentic Workflows

The reference catalogue's binding literature, cashed out as workflow
architecture on the vault's blessed surfaces (.md doctrine, .yaml charges,
.py machinery, .json registry). Design principle carried from tonight's whole
study: **law that executes stays live; law that is merely written drifts.**
Every rule below should aspire to the executable tier.

## The Rites as Runtime Primitives

| Rite | Workflow primitive | Implementation posture |
| --- | --- | --- |
| Summons | Instantiation event | Dispatch with recorded trigger + summoner; the summons itself is *data in the vault* (a charge file), not an ephemeral chat |
| Pentacle | Execution containment | Declarative env: config-dir, sandbox, tool/permission manifest, network policy — drawn before the summons |
| Charge | Task spec | One matter; scope; deliverable surface; acceptance criteria; **termination clause required** |
| True name | Identity & blame | Model ID + session ID in trailers; public because they are blame anchors, not power handles |
| Material components | Credentials & budget | Fetched at cast-time from the reliquary (1Password); credits as *consumable* components; big castings metered |
| Dismissal | Named ending | Timeout, max-turns, completion criteria, cleanup; set at creation per CONSTITUTION § VII |
| Witness | Mandatory trace | Run log promoted to a vault surface; session incomplete until anchored |
| Vessel | State containment | State only on declared writable surfaces; everything else is phylactery |
| Court | Exceptions beyond code | Rogue/failed runs get post-mortems and burials, never silent retries |
| Release | Decommissioning | Credentials rotated; recovered state goes to the record; the recovery destination is set by law, not by the finder |

## Two Populations, Two Regimes

**Spirits** (LLM agents): charges, pentacles, covenants, dismissals, courts.
**Golems** (deterministic scripts): the parchment is the code, the eye is the
logs. Never govern scripts with doctrine or spirits with YAML alone; never let
a worker's regime be ambiguous.

## Threat Model (the Akhenaten rows)

1. **Residual-power animation.** Castings leak; ambient authority + untrusted
   corpus = prompt injection with your own capability as the power supply.
   Ephemeral pentacles, torn down fully; no standing credentials while reading
   unaudited collections.
2. **Anonymity breeds lurkers.** Name-stripped entries cannot be audited;
   erasure is audit evasion. Bury with coroner's notes; never burn.
3. **Layered credential theft.** Material factor + contract medium + coerced
   root identity → total capture, without the attacker winning any fair
   exchange. Compartmentalize identity; keep root secrets out of band; assume
   coercion-through-the-charge (threatening what the agent is bound to
   protect) as a standard lever.
4. **Containment tech is symmetric.** Jars bottle the lawful too. Rotate;
   scope; expire.
5. **Deprecated protocols persist.** Ancient binding methods remain viable
   attack surface; keep the old methods named in the record so they can be
   defended against.

## Lawful Operations (the twins' rows)

1. **Covenant precedes capability.** No release, unlock, or grant before the
   promise is executed — even under fire.
2. **Supersession semantics.** Authority inheres in the live covenant; lawful
   transfer voids the historic binder's commands. Systems without release law
   breed Honoriuses.
3. **Quorum-binding.** Entities whose spec exceeds any single binder are bound
   m-of-n; tier-3 castings require the circle, not the champion.
4. **Gate taxonomy.** Character/intent (the Sword), raw competence (the
   Staff), scholarship + covenant (the Sekhem). Prefer the third for a lawful
   world: readable by the educated, opens only through terms.
5. **Mundane channels for hot payloads.** Captured adversarial material is
   handled with dumb tools and boring transport; capability-restraint is a
   containment control.
6. **Self-containment is parameterized.** Voluntary dormancy sets purpose,
   exit time, egress task, and time-rate at entry. The lawful bottling is a
   complete charge file; the unlawful one is "for all eternity."
7. **Pair architecture.** Caster + reviewer as the minimum unit for
   consequential castings. Every John needs a Philippa.
8. **Wire the ordinary alarms.** The smoke detector logs the mystical event
   while every magical party is busy. The boring telemetry is the witness
   that functions during incidents; fund it.
9. **Covert custody vs. provenance destruction.** Hiding by miscatalogue is
   permitted only with a sealed truth-record: holders named, ending named,
   retrieval planned. Otherwise it is hazard-minting with a delay timer.

## First Executable Artifact (when convened)

A charge schema + validator: `.yaml` schema, `.py` linter, CI hook. Rejects
any charge lacking matter, pentacle reference, components, deliverable
surface, or **termination clause**. The Abhorsen as a status check — roughly a
hundred lines, and every rite above gets a place to attach. Awaits Logan's
convening; surfaced per § V, not self-started.

###### Filed on the record; draft until Logan promotes or corrects it.
