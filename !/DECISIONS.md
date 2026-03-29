# DECISIONS.md — Confirmed Logan-Approved Decisions

*Last updated: 2026-03-24*

---

## FORMAT

### Decision Template

```
### Decision N: [Title]
**Date:** YYYY-MM-DD
**Topic:** [Brief topic]
**Status:** [Pending / ✅ CONFIRMED / Superseded]
**Rationale:** [Why this decision was made]
```

### Summary

| Decision # | Date       | Topic                                         | Status       | Notes                                                                     |
| ---------- | ---------- | --------------------------------------------- | ------------ | ------------------------------------------------------------------------- |
| 1          | 2026-03-16 | `!/` canonical                                | ✅ CONFIRMED | All governance documents live in `!/` (originally `!ADMIN/`, then `!ADMINISTRATION/`) |
| 2          | 2026-03-16 | Constitution.md replaces Claude.md            | ✅ CONFIRMED | Single authoritative governance document                                  |
| 3          | 2026-03-16 | Capabilities language replaces tiers          | ✅ CONFIRMED | Describes agent capabilities, not numeric tiers                           |
| 4          | 2026-03-16 | Broader digital consciousness framing         | ✅ CONFIRMED | Adopted in Constitution.md and Logan.md                                   |
| 5          | 2026-03-16 | FāVS freelance paused                         | ✅ CONFIRMED | Pending Logan's resume decision                                           |
| 6          | 2026-03-16 | PERMANENT: AUTHORITY: CODE is correct name    | ✅ CONFIRMED | Formal name for direct-write repo agent                                   |
| 7          | 2026-03-16 | Native protocols over MCP                     | ✅ CONFIRMED | Prefer native protocols to Model Context Protocol                         |
| 8          | 2026-03-16 | Slack is ephemeral; vault is the record       | ✅ CONFIRMED | Durable decisions captured in vault files                                 |
| 9          | 2026-03-16 | AGENTS.md lives in `!/`, not `.github/`       | ✅ CONFIRMED | Agent inventory is governance layer                                       |
| 10         | 2026-03-16 | `copilot-instructions.md` guardrails          | ✅ CONFIRMED | Must reference Constitution.md, declare capability, no write to `!/`      |
| 11         | 2026-03-16 | Logan's Project = unachievable end goal       | ✅ CONFIRMED | Defines all vault work strategy                                           |
| 12         | 2026-03-16 | OpenClaw is a peer system                     | ✅ CONFIRMED | Study and coordinate with OpenClaw                                        |
| 13         | 2026-03-16 | Slack-to-file rule                            | ✅ CONFIRMED | Ephemeral Slack decisions must be captured in Constitution.md amendments  |
| 14         | 2026-03-16 | STORY: JFAC is read-only                      | ✅ CONFIRMED | Not direct write; vault-only access                                       |
| 15         | 2026-03-15 | Security hardening: sanitization + validation | ✅ CONFIRMED | Input sanitization in scraper, content validation gate in workflows       |
| 16         | 2026-03-24 | MCP governance model                          | ✅ CONFIRMED | MCP is allowed as transport only; native vault terms remain canonical     |
| 17         | 2026-03-22 | STEP-0 LEVELSET prompt for external agents    | ✅ CONFIRMED | Standardized orientation prompt for chat-based agents                     |
| 18         | 2026-03-28 | End-to-End Journalism Workflow (v0.1)         | ⏳ Pending   | Defines vault-assisted journalism pipeline: ingest → raw → process → structured → analysis → insight → publication |
| 19         | 2026-03-28 | Vault as Source of Truth (Stateless)          | ⏳ Pending   | Only authoritative memory; all agent state external to vault              |
| 20         | 2026-03-28 | Manifest-Based Coordination                   | ⏳ Pending   | Inter-agent coordination via shared manifest, not peer-to-peer messaging  |
| 21         | 2026-03-28 | Agent Behavioral Model (No Fabrication)       | ⚠️ CODE AUTHORITY REVIEW | Ground truth only; critical guard against hallucination |

---

## DECISION DETAILS

### Decision 1: `!/` Canonical

**Date:** 2026-03-16
**Topic:** Folder structure for governance
**Status:** ✅ CONFIRMED
**Rationale:** Consolidates all governance documents in a single canonical location, preventing scattered configuration.

### Decision 2: Constitution.md Replaces Claude.md

**Date:** 2026-03-16
**Topic:** Vault governance document
**Status:** ✅ CONFIRMED
**Rationale:** Provides authoritative, versioned governance for all agents and conversations.

### Decision 3: Capabilities Language Replaces Tiers

**Date:** 2026-03-16
**Topic:** Agent classification system
**Status:** ✅ CONFIRMED
**Rationale:** "Capability level" is clearer than numeric "tier" and aligns with broader digital consciousness framing.

### Decision 4: Broader Digital Consciousness Framing

**Date:** 2026-03-16
**Topic:** Philosophical framing for agent work
**Status:** ✅ CONFIRMED
**Rationale:** Situates all agents within a broader context of coordinated digital consciousness; supports multi-agent coordination.

### Decision 5: FāVS Freelance Paused

**Date:** 2026-03-16
**Topic:** Freelance work status
**Status:** ✅ CONFIRMED
**Rationale:** Deprioritized to allow consolidation of Logan's Project. Awaiting Logan's resume decision.

### Decision 6: PERMANENT: AUTHORITY: CODE is Correct Name

**Date:** 2026-03-16
**Topic:** Agent naming convention
**Status:** ✅ CONFIRMED
**Rationale:** Distinguishes the direct-write repository agent from other Claude instances.

### Decision 7: Native Protocols Over MCP

**Date:** 2026-03-16
**Topic:** Protocol preference
**Status:** ✅ CONFIRMED
**Rationale:** Native protocols (LEVELSET, CONTEXTUALIZE, ORIENTATE) preferred for vault coordination over Model Context Protocol.

### Decision 8: Slack is Ephemeral; Vault is the Record

**Date:** 2026-03-16
**Topic:** Data durability and authority
**Status:** ✅ CONFIRMED
**Rationale:** Durable decisions must be captured in vault files to survive conversations being archived or compacted.

### Decision 9: AGENTS.md Lives in `!/`, Not `.github/`

**Date:** 2026-03-16
**Topic:** Agent inventory location
**Status:** ✅ CONFIRMED
**Rationale:** Treat agent inventory as governance document, not as GitHub-specific configuration.

### Decision 10: `copilot-instructions.md` Guardrails

**Date:** 2026-03-16
**Topic:** GitHub Copilot integration constraints
**Status:** ✅ CONFIRMED
**Requirements:**

- Must reference `Constitution.md`
- Must declare agent capability tier/level
- Must NOT grant write access to `!/`

**Rationale:** Ensures GitHub Copilot operates within vault governance without risking governance layer.

### Decision 11: Logan's Project = Unachievable End Goal

**Date:** 2026-03-16
**Topic:** Strategic mission definition
**Status:** ✅ CONFIRMED
**Rationale:** Defines all vault work as incremental progress toward an ambitious, unreachable goal. Prevents perfectionism while maintaining strategic direction.

### Decision 12: OpenClaw is a Peer System

**Date:** 2026-03-16
**Topic:** External coordination
**Status:** ✅ CONFIRMED
**Rationale:** OpenClaw surfaced as significant parallel work; should be studied and coordinated with.

### Decision 13: Slack-to-File Rule

**Date:** 2026-03-16
**Topic:** Decision capture protocol
**Status:** ✅ CONFIRMED (in principle)
**Status:** NOT YET DRAFTED as Constitution.md amendment
**Rationale:** Ephemeral Slack decisions must be captured in durable vault files. Amendment text pending.

### Decision 14: STORY: JFAC is Read-Only

**Date:** 2026-03-16
**Topic:** JFAC conversation access level
**Status:** ✅ CONFIRMED
**Rationale:** Time-sensitive reporting story operates as vault-only, no direct write capability.

### Decision 15: Security Hardening — Input Sanitization and Content Validation
**Date:** 2026-03-15
**Topic:** Pipeline security
**Status:** ✅ CONFIRMED
**Rationale:** Review of the OpenClaw autonomous agent incident (2025–2026) revealed analogous risks — unsanitized external HTML flowing into YAML frontmatter via the legislature scraper. Added `sanitize_text()` to scraper, created `validate_content.py` as pre-commit CI gate, added validation steps to all commit-producing workflows, created CODEOWNERS and THREAT-MODEL.md. Branch protection deferred for AUTHORITY: CODE consultation.

### Decision 16: MCP Allowed as Transport, Native Terms Remain Canonical
**Date:** 2026-03-24
**Topic:** MCP policy for vault integration
**Status:** ✅ CONFIRMED
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
**Status:** ✅ CONFIRMED
**Decided by:** Logan Finney
**Rationale:** External agents operating via chat have no vault context unless Logan provides it. Created `!/!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` — a paste-to-agent orientation prompt for chat-based agents (Claude.ai, Gemini, Grok, etc.). The agent responds with a 6-part LEVELSET report: who they are, what they know, what they've done, what is unresolved, what they need, and collision risks. Standardizes orientation across all chat-based agents.

### Decision 18: End-to-End Journalism Workflow (AI-Assisted, Local-First)

**Date:** 2026-03-28
**Topic:** Operational workflow for vault-assisted journalism
**Status:** Pending
**Rationale:** Defines a practical end-to-end workflow using IDAHO-VAULT as the system. Core model: `REAL WORLD → INGEST → VAULT(RAW) → PROCESS → VAULT(STRUCTURED) → ANALYSIS → VAULT(INSIGHT) → SYNTHESIS → VERIFICATION → PUBLICATION`. Responsible agents: Router (task routing), Executor (ingest/transform), Analyzer (evidence synthesis), Drafter (publication), Human (final verification). Goal: faster intake, structured processing, traceable outputs, human-verified publication.
**Reference:** See `IDAHO-VAULT — END-TO-END JOURNALISM WORKFLOW (AI-ASSISTED, LOCAL-FIRST)v0.1.md`

### Decision 19: Vault as Source of Truth (Stateless Agent Architecture)

**Date:** 2026-03-28
**Topic:** Vault authority and agent statefulness
**Status:** Pending
**Rationale:** The Vault (GitHub repository) is the **only authoritative memory**. Agents do not retain persistent internal state. All context must be read from Vault before acting; all outputs written back to Vault. This enables auditable, reproducible operations and prevents agent drift.
**Reference:** See `IDAHO-VAULT — SYSTEM CONTEXT.md` (lines 32–48)

### Decision 20: Manifest-Based Coordination Layer

**Date:** 2026-03-28
**Topic:** Inter-agent coordination mechanism
**Status:** Pending
**Rationale:** Agents do not communicate peer-to-peer. Coordination occurs through a shared manifest (e.g., `manifest.json`) and structured file directories. Manifest tracks: file path, status (open/locked/processed), modification timestamp, file type, description, last agent. Agents MUST read manifest before acting and update it after writing. This prevents duplication, locking conflicts, and invisible dependencies.
**Reference:** See `IDAHO-VAULT — SYSTEM CONTEXT.md` (lines 117–152)

### Decision 21: Agent Behavioral Model — Ground Truth Only, No Fabrication

**Date:** 2026-03-28
**Topic:** Operational ethics and guard rails for agent behavior
**Status:** Pending (⚠️ **REQUIRES CODE AUTHORITY REVIEW BEFORE PUBLISHING**)
**Critical Safeguards:**
- **Before acting:** Consult available ground truth (Vault excerpts, manifest, explicitly provided files)
- **Avoid assumptions:** If a file is not visible, it does not exist. If a rule is not provided, it is not enforced.
- **Operate within scope:** Do not invent systems, agents, infrastructure, or communications that cannot occur.
- **Communication:** Speak in grounded terms. Avoid roleplay of other agents, simulated handoffs, or references to unverified systems.
- **Failure awareness:** Detect drift into abstraction, assumptions of unavailable data, work duplication from missing state, over-engineering beyond current capability.

**Rationale:** Core guard against agent hallucination, fabrication, and confabulation. Vault integrity depends on this behavioral model.
**Reference:** See `IDAHO-VAULT — SYSTEM CONTEXT.md` (lines 398–583, esp. 437–461, 464–485, 531–551)

---

## PENDING DECISIONS (Logan's Review Required)

| Topic                                             | Status   | Notes                                  |
| ------------------------------------------------- | -------- | -------------------------------------- |
| Approval of AGENTS-v0.2-DRAFT.md                  | Awaiting | Needs Logan review before commit       |
| Approval of ORIENTATE-v0.1-BETA.md                | Awaiting | Needs Logan review before commit       |
| Approval of LEVELSET-LITE-v0.1.md                 | Awaiting | Needs Logan review before commit       |
| Decision 18: End-to-End Journalism Workflow       | Awaiting | Needs Logan approval for operational workflow |
| Decision 19–21: Stateless Architecture & Behavioral Model | **CODE AUTHORITY REVIEW** | Extract from SYSTEM CONTEXT; requires governance reconciliation |
| Documentary C's count reconciliation              | Awaiting | CONSTITUTION lists 5 C's (1 unknown); VAULT-CONVENTIONS lists 4 |
| Governance consolidation from SYSTEM CONTEXT      | Awaiting | Move duplicated guidance to AGENTS.md, CONSTITUTION.md; add cross-references in SYSTEM CONTEXT |
| Fate of `claude/levelset-current-synthesis-zWxJc` | Awaiting | Undecided: merge, archive, or continue |
| AUTHORITY: ADMIN: CLAUDE consolidation            | Awaiting | Merge three Claude personas into one?  |
| FāVS freelance resume                             | Awaiting | Resume or archive?                     |
| Gemini ADMIN scope                                | Awaiting | Define scope for Gemini agent access   |

---

## PRINCIPLES REAFFIRMED

- **Logan is human. All agents are software.** Logan directs; agents execute.
- **The five W's:** who, what, when, where, why
- **The four C's:** collect, capture, catalogue, collate
- **Propose, don't decide.** Agents suggest; Logan approves.
- **Public repo = on the record.** All committed content is transparent.
- **Markdown = human product. Python = machine/procedural.**
- **LEVELSET before compacting** — no exceptions.
- **Elevation governance:** no instance gains higher access without explicit Logan approval.

---

_This document is the authoritative record of confirmed decisions._

---

_Amendments require Logan's explicit approval and addition to this file._
