---
title: "2026 Chronology Pass"
date: 2026-05-04
authority: LOGAN
status: active
type: research-note
tags:
  - chronology
  - 2026
  - governance
  - runtime
  - persona
  - registry
related:
  - CONSTITUTION
  - VAULT-METADATA-STANDARD
  - ROLE-MANIFEST-2026-05-04
  - PERSONA-PERSISTENCE-2026-05-03
  - STUB-PERSONAFOLDERS-2026-05-03
  - NOUS-RESEARCH-HERMES-AGENT-2026-04-28
  - OPENROUTER-2026-04-28
---

# 2026 Chronology Pass

This pass reads the 2026 documentation and vault materials in date order,
with filename dates as the primary sort key and frontmatter dates as fallback
only when needed.

Scope:

- prioritize governance, registry, coordination, runtime, and persona/docs
- include daily notes and capture notes when they anchor a dated decision
- treat source articles as background unless they changed the system vocabulary

## Chronology

| Date range | What changed | Anchor docs |
|---|---|---|
| 2026-01 to 2026-03-15 | Early-year source captures and daily notes set the background; the vault is already using timeline-oriented capture and reporting habits before the governance stack settles. | `2026-03-16.md`, `2026-03-10 - I Built My Own Local AI Agent with OpenClaw + Obsidian What Nobody Tells You.md`, early 2026 source notes |
| 2026-03-16 | The first big governance surface lands: constitution language, metadata doctrine, and early swarm/levelset work appear together. The vault starts formalizing durable records instead of leaving everything in chat. | [CONSTITUTION.md](/Users/logan/IDAHO-VAULT/CONSTITUTION.md), [VAULT-METADATA-STANDARD.md](/Users/logan/IDAHO-VAULT/VAULT-METADATA-STANDARD.md), `2026-03-16.md`, `LEVELSET-CASCADE-2026-03-16.md` |
| 2026-03-25 to 2026-03-29 | Metadata rules are formalized, then the swarm directive narrows the safe operating mode: analyze, draft, checkpoint, avoid destructive changes. Coordination shifts from ad hoc conversation toward explicit task lanes. | [VAULT-METADATA-STANDARD.md](/Users/logan/IDAHO-VAULT/VAULT-METADATA-STANDARD.md), [2026-03-29 SWARM DIRECTIVE via Linear.md](/Users/logan/IDAHO-VAULT/2026-03-29%20SWARM%20DIRECTIVE%20via%20Linear.md), `HANDOFF-Swarm-Coordination-2026-03-29.md` |
| 2026-04-02 to 2026-04-12 | Registry repair, doctrine updates, and audit surfaces proliferate. The vault starts separating live routing from narrative residue and treating historical surfaces as non-live by default. | `HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02.md`, `!DOCTRINAL-EVOLUTION-ESSAY-2026-04-12.md`, `!VAULTED-CENSUS-2026-04-12.md`, `!DOTFOLDER-STABILITY-AUDIT-2026-04-12.md` |
| 2026-04-13 to 2026-04-18 | The tree, routing, and report layers become more explicit. Explorer companions and report notes multiply, and the vault starts documenting tool lanes and structural boundaries instead of assuming them. | `!/ARBORSCAPING-REPORT-2026-04-16.md`, `!/REPORT-SWARM-LEVEL-CLI-REVIEW-2026-04-17.md`, `!/REPORT-METADATA-FRONTMATTER-FINDINGS-2026-04-18.md`, `!/REPORT-PROJECT-HEALTH-2026-04-18.md` |
| 2026-04-19 to 2026-04-26 | OpenCode becomes a clear runtime/toolchain surface. OpenCode ecosystem, skills, SDK, GitHub integration, and MCP docs clarify that orchestration and tools are separate from the model layer. | [2026-04-26 - Ecosystem.md](/Users/logan/IDAHO-VAULT/2026-04-26%20-%20Ecosystem.md), [2026-04-26 - Agent Skills.md](/Users/logan/IDAHO-VAULT/2026-04-26%20-%20Agent%20Skills.md), [2026-04-26 - SDK.md](/Users/logan/IDAHO-VAULT/2026-04-26%20-%20SDK.md), [2026-04-26 - GitHub.md](/Users/logan/IDAHO-VAULT/2026-04-26%20-%20GitHub.md), [2026-04-26 - MCP servers.md](/Users/logan/IDAHO-VAULT/2026-04-26%20-%20MCP%20servers.md) |
| 2026-04-26 to 2026-04-28 | Big Pickle, OpenRouter, Hermes, and local Ollama preferences get separated into model versus runtime language. Big Pickle is documented as a model target, while Hermes/OpenClaw/OpenCode remain orchestration surfaces. | [LEVELSET-BIG-PICKLE-2026-04-25.md](/Users/logan/IDAHO-VAULT/!/LEVELSET-BIG-PICKLE-2026-04-25.md), [OPENROUTER-2026-04-28.md](/Users/logan/IDAHO-VAULT/OPENROUTER-2026-04-28.md), [NOUS-RESEARCH-HERMES-AGENT-2026-04-28.md](/Users/logan/IDAHO-VAULT/NOUS-RESEARCH-HERMES-AGENT-2026-04-28.md), `2026-04-28.md` |
| 2026-05-03 to 2026-05-04 | Persona work becomes explicit and schema-driven. Persona is defined as the dotfolder/chamber contract, stub vs imported chambers are separated, and the role manifest formalizes the layer split. Sync policy is written down, but the actual runtime-to-vault sync mechanism is still under development. | [PERSONA-PERSISTENCE-2026-05-03.md](/Users/logan/IDAHO-VAULT/PERSONA-PERSISTENCE-2026-05-03.md), [STUB-PERSONAFOLDERS-2026-05-03.md](/Users/logan/IDAHO-VAULT/STUB-PERSONAFOLDERS-2026-05-03.md), [ROLE-MANIFEST-2026-05-04.md](/Users/logan/IDAHO-VAULT/ROLE-MANIFEST-2026-05-04.md), [CONSTITUTION.md](/Users/logan/IDAHO-VAULT/CONSTITUTION.md) |

## Key Shifts

1. `persona` moved from a loose voice/narrative label to the dotfolder schema
   and chamber contract.
2. `model`, `runtime/orchestrator`, `persona`, and `record` are now treated as
   distinct layers.
3. OpenCode documents explain the toolchain layer; Hermes/OpenRouter docs
   explain runtime/model routing; Big Pickle is a model target, not an
   orchestration persona.
4. The vault now distinguishes sync policy from sync mechanism. The policy
   exists; the mechanism is still being built.

## Reading Order For The Next Pass

1. `CONSTITUTION.md`
2. `VAULT-METADATA-STANDARD.md`
3. `2026-03-29 SWARM DIRECTIVE via Linear.md`
4. `!/AGENTS.md` and `swarm.json`
5. OpenCode docs from 2026-04-26
6. OpenRouter and Hermes docs from 2026-04-28
7. Persona persistence, stub personafolders, role manifest, and constitution
   updates from 2026-05-03 to 2026-05-04

## Notes

- This is a control-plane chronology, not an exhaustive transcription of every
  2026 source note.
- The timeline is reproducible from filename dates and anchored by the
  governance files above.
- If the vault needs a more exhaustive 2026 corpus chronology later, this note
  is the starting scaffold, not the final form.
