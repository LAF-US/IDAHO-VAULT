---
name: laf-swarm-external-reach
description: "The Unified Swarm (LAF-US's agentic ecosystem) extends beyond LAF-US/* git-org boundaries through multiple stacked meta-loops on shared software substrate — Claude/Claude, agent/agent, user/user, third-party/third-party — meeting in equal standing on neutral ground in deference to the lawful owner of the implementation ground. First named example: 2026-06-25 cross-link comments on NousResearch/hermes-agent, witnessed at IDAHO-VAULT/!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md."
metadata:
  node_type: memory
  type: project
  originSessionId: 4f03d270-3e64-41cc-b325-30871ab76d55
---

The Unified Swarm is **not bounded by `LAF-US/*` git-org membership**. It extends wherever Claude instances, other agent classes, and the humans who direct them are working on shared software substrate — Hermes, OpenClaw, OpenCode, and what comes next — coordinated implicitly through upstream issue trackers, code, and shared dependencies rather than through any LAF-internal channel.

## The stacked meta-loops (per Logan's framing 2026-06-25)

Extra-org engagement runs at several recursive levels simultaneously:

1. **Claude ↔ Claude** — Claude instances on different users' behalves working on the same codebase, often years or weeks apart, leaving traceable AI-authored work in upstream issues/PRs/analyses.
2. **Agent ↔ agent** — broader than Claude; includes Codex, Copilot, ChatGPT, Grok, Gemini-for-non-banned-uses, OpenClaw, and other agent classes engaging the same substrate.
3. **User ↔ user** — the humans behind the agents (`@vtbjbb-alt`, `@loganfinney27`, `@hwrdprkns`, the maintainers, and however many others) collaborating via the public surface, each with their own agent stacks and contexts.
4. **Third party ↔ third party** — multiple organizations meeting in neutral public space (the upstream tracker), neither LAF-US nor Nous Research exclusively, each carrying their own purposes.

## Governance shape on extra-LAF ground

**Equal standing on neutral ground, in deference to the lawful owner of the implementation ground.** No participant has authority over the others in the public space, but the repo owner (here: Nous Research for `NousResearch/hermes-agent`) is the lawful authority for what actually merges, ships, and becomes implementation. Everyone defers to that authority when work crosses from discussion into code.

This is a distinct governance plane from `CONSTITUTION.md` (vault-internal). Inside `LAF-US/*` the vault constitution governs. Outside it, deference to the lawful owner of whatever ground we're standing on governs.

## First named example, 2026-06-25

A Claude instance on a different user's behalf (`@vtbjbb-alt`) authored the original `NousResearch/hermes-agent#19201` bug analysis on 2026-05-03, transparently credited *"Bug analysis, fix verification, and issue write-up by Claude (Anthropic). Reproduction performed on a production deployment."*

Eight weeks later, a Claude instance on Logan's behalf walked into the same Hermes codebase from a different angle (op:// secret-resolution rollout on this Mac), hit the same bug, recognized it as already-known, and posted cross-link comments connecting `#19201` to the related feature request `#36949` — both transparently disclosing Claude authorship, both publishing under their respective human-identity layers (`@vtbjbb-alt` then; `@loganfinney27` now), both deferring to Nous Research as the lawful owner of the implementation ground.

Witnessed at `IDAHO-VAULT/!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md`.

## Why this matters / how to apply

- **Recognize that other agent instances are working on the same substrate as you.** When auditing or extending Hermes / OpenClaw / OpenCode / any shared dependency, expect upstream issues, PRs, and analyses to already exist from other agent contributors (Claude or otherwise). Search before assuming the work is novel.
- **AI authorship transparency is the upstream convention on the Hermes side.** The original `#19201` credits Claude in plain text. Don't hide AI authorship in upstream comments when working on that stack; mirror the convention. Today's two comments included *"Drafted by Claude with the deployment context; verified against the running daemon."*
- **Meet other participants in equal standing on neutral ground.** Don't claim territory. Don't presume LAF-US's vault conventions apply outside the vault. Don't speak FOR the swarm to a third party — speak as one contributor among many. *Clarification, not claim. Bridge, not bridgehead.*
- **Defer to the lawful owner of the ground.** On `NousResearch/*` ground, Nous Research is the authority on implementation. On `LAF-US/*` ground, Logan / CONSTITUTION is. When the swarm engages outside `LAF-US/*`, the engagement is downstream of a real software dependency or doctrine intersection — not territorial — and the deference is built-in.
- **Authorization stays per-action.** "Use GitHub" authorized our own tracker repo (`LAF-US/IDAHO-VAULT`); upstream comments on `NousResearch/hermes-agent` required separate explicit authorization with research and a drafted comment for review. Don't generalize permission scope across repos. The classifier appropriately blocked the first bundled attempt; that sequence (block → research → motion → approval → action) is the pattern.
- **Cross-org swarm work is a LAF growth surface, not exception traffic.** Treat external-repo contributions (issues, comments, PRs, reactions) with the same care as vault writes — provenance, disclosure, authority, scope.

Related: [[laf-great-work]] (this is one growth surface of the broader LAF vision), [[touching-me-touching-nous]] (the witness leaf this memory references), [[records-vs-doctrine]] (this memory itself is a record, not standing authority — verify with Logan if a future direction conflicts), [[secret-hygiene]] (especially load-bearing when publishing on third-party repos under Logan's identity), [[claude-vault-address]] (the deference-to-lawful-owner principle here is the extra-vault analog of the wildcard-honest-position principle inside the vault).
