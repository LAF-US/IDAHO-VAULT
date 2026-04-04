# DECISIONS.md â€” Confirmed Logan-Approved Decisions

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
| 18         | 2026-03-28 | End-to-End Journalism Workflow (v0.1)         | â³ Pending   | Defines vault-assisted journalism pipeline: ingest â†’ raw â†’ process â†’ structured â†’ analysis â†’ insight â†’ publication |
| 19         | 2026-03-28 | Vault as Source of Truth (Stateless)          | â³ Pending   | Only authoritative memory; all agent state external to vault              |
| 20         | 2026-03-28 | Manifest-Based Coordination                   | â³ Pending   | Inter-agent coordination via shared manifest, not peer-to-peer messaging  |
| 21         | 2026-03-28 | Agent Behavioral Model (No Fabrication)       | âš ï¸ CODE AUTHORITY REVIEW | Ground truth only; critical guard against hallucination |
| 22         | 2026-04-03 | Grimoire opened — `!/GRIMOIRE/` canonical     | ✅ CONFIRMED | Chorus Bootstrap Decision 2 executed. Three-layer model (Charter / Corpus / Grimoire) adopted. Codex→Corpus in VAULT-CONVENTIONS.md. Rosetta Stone filed by Gemini. |

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

### Decision 19: Vault as Source of Truth (Stateless Agent Architecture)

**Date:** 2026-03-28
**Topic:** Vault authority and agent statefulness
**Status:** Pending
**Rationale:** The Vault (GitHub repository) is the **only authoritative memory**. Agents do not retain persistent internal state. All context must be read from Vault before acting; all outputs written back to Vault. This enables auditable, reproducible operations and prevents agent drift.
**Reference:** See `IDAHO-VAULT â€” SYSTEM CONTEXT.md` (lines 32â€“48)

### Decision 20: Manifest-Based Coordination Layer

**Date:** 2026-03-28
**Topic:** Inter-agent coordination mechanism
**Status:** Pending
**Rationale:** Agents do not communicate peer-to-peer. Coordination occurs through a shared manifest (e.g., `manifest.json`) and structured file directories. Manifest tracks: file path, status (open/locked/processed), modification timestamp, file type, description, last agent. Agents MUST read manifest before acting and update it after writing. This prevents duplication, locking conflicts, and invisible dependencies.
**Reference:** See `IDAHO-VAULT â€” SYSTEM CONTEXT.md` (lines 117â€“152)

### Decision 21: Agent Behavioral Model â€” Ground Truth Only, No Fabrication

**Date:** 2026-03-28
**Topic:** Operational ethics and guard rails for agent behavior
**Status:** Pending (âš ï¸ **REQUIRES CODE AUTHORITY REVIEW BEFORE PUBLISHING**)
**Critical Safeguards:**
- **Before acting:** Consult available ground truth (Vault excerpts, manifest, explicitly provided files)
- **Avoid assumptions:** If a file is not visible, it does not exist. If a rule is not provided, it is not enforced.
- **Operate within scope:** Do not invent systems, agents, infrastructure, or communications that cannot occur.
- **Communication:** Speak in grounded terms. Avoid roleplay of other agents, simulated handoffs, or references to unverified systems.
- **Failure awareness:** Detect drift into abstraction, assumptions of unavailable data, work duplication from missing state, over-engineering beyond current capability.

**Rationale:** Core guard against agent hallucination, fabrication, and confabulation. Vault integrity depends on this behavioral model.
**Reference:** See `IDAHO-VAULT â€” SYSTEM CONTEXT.md` (lines 398â€“583, esp. 437â€“461, 464â€“485, 531â€“551)

**CODE AUTHORITY REVIEW (2026-03-28, The Abhorsen):**
Principles reviewed. Findings:
- Safeguards 1, 3, 4, 5 are consistent with existing vault governance (`feedback_operations.md`, CONSTITUTION.md principles).
- Safeguard 2 ("If a file is not visible, it does not exist") â€” **note nuance**: applies to external chat agents (who only see what Logan pastes). Code agents with filesystem access (Claude Code, Codex, Gemini CLI) CAN read files not in their active context. Recommend scoping this safeguard to external/chat agents or rewording to "If a file has not been read or provided, do not assume its content."
- No technical conflicts with existing governance identified.
- **Verdict:** Sound principles. Pending Logan's approval to confirm as official decision. Minor reword on Safeguard 2 recommended before publishing.

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
