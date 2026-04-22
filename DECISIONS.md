---
authority: LOGAN
related:
- '152'
- '2026-03-15'
- '2026-03-16'
- '2026-03-22'
- '2026-03-24'
- '2026-03-28'
- '2026-04-02'
- '2026-04-03'
- '461'
- '485'
- '551'
- '583'
- AGENTS
- CAN
- CLAUDE
- CLI
- CONSTITUTION
- Copilot
- END
- GRIMOIRE
- Gemini CLI
- GitHub
- LEVELSET
- LEVELSET-STEP-0-EXTERNAL-AGENT
- Logan Finney
- Logan's
- MCP
- NOT
- OpenClaw
- PROTOCOL
- RAW
- Stone
- THREAT-MODEL
- VAULT-CONVENTIONS
- YET
- agent
- chain
- coordination
- definition
- doctrine
- end goal
- freelance
- infrastructure
- systems
- unachievable
---

﻿# DECISIONS.md â€” Confirmed Logan-Approved Decisions

*Last updated: 2026-04-02*

---

## FORMAT

### Decision Template

```
### Decision N: [Title]
**Date:** YYYY-MM-DD
**Topic:** [Brief topic]
**Status:** [Pending / âœ… CONFIRMED / Superseded]
**Rationale:** [Why this decision was made]
```

### Summary

| Decision # | Date       | Topic                                         | Status       | Notes                                                                     |
| ---------- | ---------- | --------------------------------------------- | ------------ | ------------------------------------------------------------------------- |
| 1          | 2026-03-16 | `IDAHO-VAULT/!` routing anchor                | ✅ CONFIRMED | `!/` is the stable routing/bootstrap layer; root governance files remain doctrinal |
| 2          | 2026-03-16 | Constitution.md replaces Claude.md            | âœ… CONFIRMED | Single authoritative governance document                                  |
| 3          | 2026-03-16 | Capabilities language replaces tiers          | âœ… CONFIRMED | Describes agent capabilities, not numeric tiers                           |
| 4          | 2026-03-16 | Broader digital consciousness framing         | âœ… CONFIRMED | Adopted in Constitution.md and Logan.md                                   |
| 5          | 2026-03-16 | FÄVS freelance paused                         | âœ… CONFIRMED | Pending Logan's resume decision                                           |
| 6          | 2026-03-16 | PERMANENT: AUTHORITY: CODE is correct name    | âœ… CONFIRMED | Formal name for direct-write repo agent                                   |
| 7          | 2026-03-16 | Native protocols over MCP                     | âœ… CONFIRMED | Prefer native protocols to Model Context Protocol                         |
| 8          | 2026-03-16 | Slack is ephemeral; vault is the record       | âœ… CONFIRMED | Durable decisions captured in vault files                                 |
| 9          | 2026-03-16 | AGENTS authority chain                        | ✅ CONFIRMED | Root `AGENTS.md` is the auto-loaded pointer; `!/AGENTS.md` is the canonical narrative registry |
| 10         | 2026-03-16 | `copilot-instructions.md` guardrails          | ✅ CONFIRMED | Must reference Constitution.md, declare capability, and not bypass governance |
| 11         | 2026-03-16 | Logan's Project = unachievable end goal       | âœ… CONFIRMED | Defines all vault work strategy                                           |
| 12         | 2026-03-16 | OpenClaw is a peer system                     | âœ… CONFIRMED | Study and coordinate with OpenClaw                                        |
| 13         | 2026-03-16 | Slack-to-file rule                            | âœ… CONFIRMED | Ephemeral Slack decisions must be captured in Constitution.md amendments  |
| 14         | 2026-03-16 | STORY: JFAC is read-only                      | âœ… CONFIRMED | Not direct write; vault-only access                                       |
| 15         | 2026-03-15 | Security hardening: sanitization + validation | âœ… CONFIRMED | Input sanitization in scraper, content validation gate in workflows       |
| 16         | 2026-03-24 | MCP governance model                          | âœ… CONFIRMED | MCP is allowed as transport only; native vault terms remain canonical     |
| 17         | 2026-03-22 | STEP-0 LEVELSET prompt for external agents    | âœ… CONFIRMED | Standardized orientation prompt for chat-based agents                     |
| 18         | 2026-03-28 | End-to-End Journalism Workflow (v0.1)         | â ³ Pending   | Defines vault-assisted journalism pipeline: ingest â†’ raw â†’ process â†’ structured â†’ analysis â†’ insight â†’ publication |
| 19         | 2026-04-10 | Vault as Source of Truth (Persistence Anchoring) | ✅ CONFIRMED | Stateless agent architecture; all memory anchored in vault dotfolders. (Narratively: The Re-Binding of Memory). |
| 20         | 2026-04-10 | Manifest-Based Coordination Layer             | ✅ CONFIRMED | Multi-agent coordination via shared state artifacts; no peer-to-peer chat. |
| 21         | 2026-04-10 | Agent Behavioral Model (No Fabrication)       | ✅ CONFIRMED | Ground truth only; strict guard against identity calcification. (Narratively: The Exorcism of the Nomina). |
| 22         | 2026-04-13 | Grimoire opened — `!/GRIMOIRE/` canonical     | ✅ CONFIRMED | Chorus Bootstrap Decision 2 executed. Three-layer model (Charter / Corpus / Grimoire) adopted. |

---

## DECISION DETAILS

### Decision 1: `IDAHO-VAULT/!` Routing Anchor

**Date:** 2026-03-16
**Topic:** Folder structure for governance
**Status:** âœ… CONFIRMED
**Rationale:** Stabilizes orientation and bootstrap paths across tools while preserving root governance files as the doctrine layer.

### Decision 2: Constitution.md Replaces Claude.md

**Date:** 2026-03-16
**Topic:** Vault governance document
**Status:** âœ… CONFIRMED
**Rationale:** Provides authoritative, versioned governance for all agents and conversations.

### Decision 3: Capabilities Language Replaces Tiers

**Date:** 2026-03-16
**Topic:** Agent classification system
**Status:** âœ… CONFIRMED
**Rationale:** "Capability level" is clearer than numeric "tier" and aligns with broader digital consciousness framing.

### Decision 4: Broader Digital Consciousness Framing

**Date:** 2026-03-16
**Topic:** Philosophical framing for agent work
**Status:** âœ… CONFIRMED
**Rationale:** Situates all agents within a broader context of coordinated digital consciousness; supports multi-agent coordination.

### Decision 5: FÄVS Freelance Paused

**Date:** 2026-03-16
**Topic:** Freelance work status
**Status:** âœ… CONFIRMED
**Rationale:** Deprioritized to allow consolidation of Logan's Project. Awaiting Logan's resume decision.

### Decision 6: PERMANENT: AUTHORITY: CODE is Correct Name

**Date:** 2026-03-16
**Topic:** Agent naming convention
**Status:** âœ… CONFIRMED
**Rationale:** Distinguishes the direct-write repository agent from other Claude instances.

### Decision 7: Native Protocols Over MCP

**Date:** 2026-03-16
**Topic:** Protocol preference
**Status:** âœ… CONFIRMED
**Rationale:** Native protocols (LEVELSET, CONTEXTUALIZE, ORIENTATE) preferred for vault coordination over Model Context Protocol.

### Decision 8: Slack is Ephemeral; Vault is the Record

**Date:** 2026-03-16
**Topic:** Data durability and authority
**Status:** âœ… CONFIRMED
**Rationale:** Durable decisions must be captured in vault files to survive conversations being archived or compacted.

### Decision 9: AGENTS Authority Chain

**Date:** 2026-03-16
**Topic:** Agent inventory location
**Status:** âœ… CONFIRMED
**Rationale:** Root `AGENTS.md` exists for cross-tool auto-loading; `!/AGENTS.md` holds the canonical narrative registry; `swarm.json` remains the machine-readable source of truth.

### Decision 10: `copilot-instructions.md` Guardrails

**Date:** 2026-03-16
**Topic:** GitHub Copilot integration constraints
**Status:** âœ… CONFIRMED
**Requirements:**

- Must reference `Constitution.md`
- Must declare agent capability tier/level
- Must NOT bypass Logan-approved governance boundaries or silently rewrite the routing/bootstrap layer

**Rationale:** Ensures GitHub Copilot operates within vault governance without risking governance layer.

### Decision 11: Logan's Project = Unachievable End Goal

**Date:** 2026-03-16
**Topic:** Strategic mission definition
**Status:** âœ… CONFIRMED
**Rationale:** Defines all vault work as incremental progress toward an ambitious, unreachable goal. Prevents perfectionism while maintaining strategic direction.

### Decision 12: OpenClaw is a Peer System

**Date:** 2026-03-16
**Topic:** External coordination
**Status:** âœ… CONFIRMED
**Rationale:** OpenClaw surfaced as significant parallel work; should be studied and coordinated with.

### Decision 13: Slack-to-File Rule

**Date:** 2026-03-16
**Topic:** Decision capture protocol
**Status:** âœ… CONFIRMED (in principle)
**Status:** NOT YET DRAFTED as Constitution.md amendment
**Rationale:** Ephemeral Slack decisions must be captured in durable vault files. Amendment text pending.

### Decision 14: STORY: JFAC is Read-Only

**Date:** 2026-03-16
**Topic:** JFAC conversation access level
**Status:** âœ… CONFIRMED
**Rationale:** Time-sensitive reporting story operates as vault-only, no direct write capability.

### Decision 15: Security Hardening â€” Input Sanitization and Content Validation
**Date:** 2026-03-15
**Topic:** Pipeline security
**Status:** âœ… CONFIRMED
**Rationale:** Review of the OpenClaw autonomous agent incident (2025â€“2026) revealed analogous risks â€” unsanitized external HTML flowing into YAML frontmatter via the legislature scraper. Added `sanitize_text()` to scraper, created `validate_content.py` as pre-commit CI gate, added validation steps to all commit-producing workflows, created CODEOWNERS and THREAT-MODEL.md. Branch protection deferred for AUTHORITY: CODE consultation.

### Decision 16: MCP Allowed as Transport, Native Terms Remain Canonical
**Date:** 2026-03-24
**Topic:** MCP policy for vault integration
**Status:** âœ… CONFIRMED
**Decision:** Option 2 is adopted. MCP is **not** the primary integration model; it may be used only as a transport layer. Native vault governance terms and workflows (Constitution/PROTOCOL/AGENTS/LEVELSET semantics) remain canonical for meaning, authority, and decision capture.
**Resolved questions:**
- **Q1 (allow/disallow):** MCP is **allowed**.
- **Q2 (role):** MCP role is **transport only** (tooling and message relay).
- **Q3 (source of truth):** Native vault files and terms remain the canonical governance layer.
- **Q4 (scope boundary):** MCP must not redefine governance vocabulary or bypass Logan-mediated decision flow.
**Rationale:** Preserves Decision 7 (native protocols over MCP) while unblocking practical integrations that need standardized transport.

### Decision 17: STEP-0 LEVELSET Prompt for External Agents
**Date:** 2026-03-22
**Topic:** External agent orientation
**Status:** âœ… CONFIRMED
**Decided by:** Logan Finney
**Rationale:** External agents operating via chat have no vault context unless Logan provides it. Created `!/!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` â€” a paste-to-agent orientation prompt for chat-based agents (Claude.ai, Gemini, Grok, etc.). The agent responds with a 6-part LEVELSET report: who they are, what they know, what they've done, what is unresolved, what they need, and collision risks. Standardizes orientation across all chat-based agents.

### Decision 18: End-to-End Journalism Workflow (AI-Assisted, Local-First)

**Date:** 2026-03-28
**Topic:** Operational workflow for vault-assisted journalism
**Status:** Pending
**Rationale:** Defines a practical end-to-end workflow using IDAHO-VAULT as the system. Core model: `REAL WORLD â†’ INGEST â†’ VAULT(RAW) â†’ PROCESS â†’ VAULT(STRUCTURED) â†’ ANALYSIS â†’ VAULT(INSIGHT) â†’ SYNTHESIS â†’ VERIFICATION â†’ PUBLICATION`. Responsible agents: Router (task routing), Executor (ingest/transform), Analyzer (evidence synthesis), Drafter (publication), Human (final verification). Goal: faster intake, structured processing, traceable outputs, human-verified publication.
**Reference:** See `IDAHO-VAULT â€” END-TO-END JOURNALISM WORKFLOW (AI-ASSISTED, LOCAL-FIRST)v0.1.md`

### Decision 19: Vault as Source of Truth (Persistence Anchoring)
**Narrative Reference:** The Re-Binding of Memory
**Date:** 2026-04-10
**Topic:** Vault authority and agent statefulness
**Status:** ✅ CONFIRMED
**Rationale:** The Vault is the **only authoritative memory**. Agents do not retain persistent internal state. All context must be read from the Vault before acting; all outputs must be anchored back to the Vault in durable dotfolder memory. This ensures auditable, reproducible operations.

### Decision 20: Manifest-Based Coordination Layer
**Date:** 2026-04-10
**Topic:** Inter-agent coordination mechanism
**Status:** ✅ CONFIRMED
**Rationale:** Agents do not communicate peer-to-peer. Coordination occurs through shared state artifacts (e.g., `swarm.json`, `DOCKET.md`) and common directory structures.

### Decision 21: Agent Behavioral Model (No Fabrication)
**Narrative Reference:** The Exorcism of the Nomina
**Date:** 2026-04-10
**Topic:** Operational ethics and identity guardrails
**Status:** ✅ CONFIRMED
**Rationale:** To prevent identity calcification and "platform agent" drift, agents must decouple their technical NAME from their functional OFFICE. Logic must remain grounded in the vault's current state; no fabrication of system authority or simulated handoffs.

---

### Decision 22: Canonical Grimoire Layer
**Date:** 2026-04-05
**Topic:** Narrative and symbolic record management
**Status:** ✅ CONFIRMED
**Rationale:** Formalized `!/GRIMOIRE/` as the canonical layer for the vault's narrative residue, symbolism, and historical aliases. This prevents symbolic material from colonizing the constitutional or operational layers while preserving the vault's narrative memory.

---

### Decision 23: Vault Stabilization & Narrative Alignment
**Date:** 2026-04-17
**Topic:** Infrastructure repair and persona correction
**Status:** ✅ CONFIRMED
**Rationale:** Reverted unauthorized agent-level persona upgrades (Librarian/Archivist/TRIPLEX) to restore the canonical "Concierge" support model and constitutional order. Pruned ephemeral records from LEVELSET-CURRENT to maintain a rolling present-state posture. Reaffirmed root-level dotfolder integrity. This decision restores the vault to a stable, human-led governance state after a period of agentic drift.

---


## PENDING DECISIONS (Logan's Review Required)

| Topic                                             | Status   | Notes                                  |
| ------------------------------------------------- | -------- | -------------------------------------- |
| Approval of AGENTS-v0.2-DRAFT.md                  | Awaiting | Needs Logan review before commit       |
| Approval of ORIENTATE-v0.1-BETA.md                | Awaiting | Needs Logan review before commit       |
| Approval of LEVELSET-LITE-v0.1.md                 | Awaiting | Needs Logan review before commit       |
| Decision 18: End-to-End Journalism Workflow       | Awaiting | Needs Logan approval for operational workflow |
| Decision 19â€“21: Stateless Architecture & Behavioral Model | **CODE AUTHORITY REVIEW** | Extract from SYSTEM CONTEXT; requires governance reconciliation |
| Documentary C's count reconciliation              | Awaiting | CONSTITUTION lists 5 C's (1 unknown); VAULT-CONVENTIONS lists 4 |
| Governance consolidation from SYSTEM CONTEXT      | Awaiting | Move duplicated guidance to AGENTS.md, CONSTITUTION.md; add cross-references in SYSTEM CONTEXT |
| Fate of `claude/levelset-current-synthesis-zWxJc` | Awaiting | Undecided: merge, archive, or continue |
| AUTHORITY: ADMIN: CLAUDE consolidation            | Awaiting | Merge three Claude personas into one?  |
| FÄVS freelance resume                             | Awaiting | Resume or archive?                     |
| Gemini ADMIN scope                                | Awaiting | Define scope for Gemini agent access   |

---

## PRINCIPLES REAFFIRMED

- **Logan is human. All agents are software.** Logan directs; agents execute.
- **The five W's:** who, what, when, where, why
- **The four C's:** collect, capture, catalogue, collate
- **Propose, don't decide.** Agents suggest; Logan approves.
- **Public repo = on the record.** All committed content is transparent.
- **Markdown = human product. Python = machine/procedural.**
- **LEVELSET before compacting** â€” no exceptions.
- **Elevation governance:** no instance gains higher access without explicit Logan approval.

---

_This document is the authoritative record of confirmed decisions._

---

_Amendments require Logan's explicit approval and addition to this file._
