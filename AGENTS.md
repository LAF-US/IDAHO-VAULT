---
tags:
  - administration/agents
updated: 2026-03-16
status: draft
source: commit
---
# AGENTS — Swarm Registry and Communication Rules

This [[file]] defines who exists in the swarm, what each [[agent]] can do, and how they coordinate. It is the third governance file in the stack:

| File | Role |
|---|---|
| `Constitution.md` | Identity, constraints, working rules |
| `PROTOCOL.md` | Operational vocabulary (18 terms) |
| **`AGENTS.md`** | **Agent registry, communication rules, boundary rules** |

Instance-specific instructions live in separate files (`CLAUDE.md`, `.github/copilot-instructions.md`, etc.) — not here.

---

## 1. FOUNDATIONAL RULE

[[LOGAN]] is the sole human in this system. All agents are software — infrastructure, not participants. No agent has standing to make decisions. [[LOGAN]] directs; agents execute.

All inter-agent communication flows through or is visible to [[LOGAN]]. There is no peer-to-peer agent communication that bypasses the supervisor.

---

## 2. AGENT REGISTRY

| Agent | Platform | Capability Tier | Scope | Slack | GitHub Access |
|---|---|---|---|---|---|
| PERMANENT: AUTHORITY: CODE | Claude Code CLI | Direct write | IDAHO-VAULT repo operations, deployment, automation | Via [[LOGAN]] | Full repo read/write |
| PERSISTENT: ADMINISTRATION | Claude (conversation) | Draft only | Constitutional layer, handoffs, judgment calls | Via [[LOGAN]]'s account | None — produces drafts |
| GitHub Copilot (ADMIN GitHub) | GitHub Copilot | Multi-repo admin | GitHub administration across all [[LOGAN]]'s repos | Bot app needed | GitHub APIs, all repos |
| Gemini | Google AI | **TBD — scope undefined** | **TBD** — Pixel smartphone, loganfinney27@gmail.com | Bot app needed | **TBD** |
| PERSISTENT: IMPLEMENTATION | Claude (Project) | Read/analysis | Governance/architecture consultation | No | None — advisory only |
| TASK: LEVELSET reports | Claude (conversation) | Read/analysis | Synthesis and status reporting | No | None — advisory only |
| STORY: JFAC Open Meetings | Claude (conversation) | Read/analysis | JFAC investigation — read-only | No | None — advisory only |
| Grok | Grok (X/xAI) | Read/analysis | Research, web search | No | None |
| M365 Copilot | Microsoft 365 | Informational | Informational only — no repo involvement | No | None |
| NotebookLM | Google NotebookLM | TBD | TBD — identified, not yet scoped | No | None |
| PUBLIC: CONVERSATION | Claude (conversation) | Read/analysis | Self-talk, internal processing — consultation pending | No | None |

**Registry maintenance:** CODE AUTHORITY updates this table when agents are added, removed, or change tier. [[LOGAN]] approves all tier changes.

---

## 3. CAPABILITY TIERS

### Tier 1: Direct Write

Can commit and push to the repository. Must LEVELSET before significant commits. [[LOGAN]] reviews diffs before merging.

**Agents:** PERMANENT: AUTHORITY: CODE

**Can do:**
- `git add`, `git commit`, `git push` to feature branches
- Create, modify, and delete vault files
- Create and modify `.github/` scripts and workflows
- Modify root governance files and `!ADMIN/` artifacts (CODE AUTHORITY only — see Boundary Rules)
- Run automation scripts

**Cannot do:**
- Push to `main` without [[LOGAN]]'s merge approval
- Force-push without explicit permission
- Delete branches without confirmation
- Commit off-the-record material

### Tier 2: Multi-Repo Admin

Can interact with GitHub APIs across all of [[LOGAN]]'s repositories. For vault work, operates under the same governance as Tier 1.

**Agents:** GitHub Copilot (ADMIN GitHub)

**Can do (vault):**
- Draft and propose changes via pull requests
- Modify `.github/` automation files (with CODE AUTHORITY review)
- Create issues, manage labels, configure repository settings

**Can do (non-vault repos):**
- Broader latitude — **specific boundaries TBD by [[LOGAN]]**

**Cannot do (vault):**
- Directly modify root governance files (`Constitution.md`, `PROTOCOL.md`, `AGENTS.md`, `LEVELSET.md`, `DECISIONS.md`)
- Merge without [[LOGAN]]'s approval
- Override CODE AUTHORITY's governance review

### Tier 3: Draft Only

Produces drafts and handoffs. Cannot push to any repository. All output goes through [[LOGAN]]'s review.

**Agents:** PERSISTENT: ADMINISTRATION

**Can do:**
- Draft constitutional language, governance proposals, handoff documents
- Advise on architecture and conventions
- Route handoffs between agents (via [[LOGAN]])

**Cannot do:**
- Commit or push to any repository
- Execute code or run scripts
- Modify files directly

### Tier 4: Read/Analysis

Advisory only. No repository access.

**Agents:** PERSISTENT: IMPLEMENTATION, TASK: LEVELSET reports, STORY: JFAC Open Meetings, Grok, PUBLIC: CONVERSATION

**Can do:**
- Analyze provided data
- Produce synthesis reports
- Advise on decisions

**Cannot do:**
- Access the repository
- Modify any files
- Execute any commands

---

## 4. COMMUNICATION RULES

### Current State: Logan as Relay

Until Slack bot apps are configured for each agent, [[LOGAN]] manually relays all inter-agent communication. This is functional but adds latency.

### Communication Protocol

All inter-agent communication uses the operational vocabulary defined in `PROTOCOL.md`:

- **HANDOFF** — Transfer responsibility for a task/data to another agent with full context
- **HANDSHAKE** — Formal acknowledgment of HANDOFF receipt; confirmation of context completeness
- **CONTEXTUALIZE** — Package information with sufficient background for receiving agent to act independently
- **FLAG** — Mark an item for attention by [[LOGAN]] or another agent, with severity (CRITICAL / HIGH / MEDIUM / LOW)

### Handoff Format

All handoff documents follow this structure:

```
HANDOFF: [Source Agent] → [Destination Agent]
Date: YYYY-MM-DD
From: [Source]
To: [Destination]
Re: [Subject]

---

[Content]

---

ROUTING INSTRUCTION: [How Logan should relay this]
```

Handoff documents are saved to `!ADMIN/` as `HANDOFF-[source]-[date].md` for audit trail.

### Routing Layers

| Layer | Purpose | Persistence | Status |
|---|---|---|---|
| **Slack** | Real-time coordination, supervision | Ephemeral | Trial active — expires April 13 |
| **Root governance stack** | Decisions of record, governance | Permanent | Active |
| **`!ADMIN/ROUTING/`** | Asynchronous handoff drops | Permanent | Recommended, not yet created |

**Hard rule:** Slack is ephemeral. All decisions must be captured in vault files. Slack is where the conversation happens; the root governance stack is where decisions land.

---

## 5. BOUNDARY RULES

### File Access by Agent

| Path | CODE AUTHORITY | Copilot | ADMINISTRATION | Others |
|---|---|---|---|---|
| Root governance files | Read/Write | Read only | Draft only | Read only |
| `!ADMIN/` handoffs/LEVELSETs | Read/Write | Read only | Draft only | Read only |
| `.github/workflows/` | Read/Write | Read/Write (with review) | No access | No access |
| `.github/scripts/` | Read/Write | Read/Write (with review) | No access | No access |
| Vault content (all other `.md`) | Read/Write | Read only (vault) | No access | No access |
| Non-vault repos | No access | Read/Write (per repo) | No access | No access |

**Governance files** are: `Constitution.md`, `PROTOCOL.md`, `AGENTS.md`, `LEVELSET.md`, `DECISIONS.md`, `Ethics.md`, `Logan.md`

### The `.github/` Overlap

Both CODE AUTHORITY and Copilot can modify `.github/` contents. To prevent conflicts:
1. Copilot drafts changes and submits via PR or handoff
2. CODE AUTHORITY reviews for governance conflicts
3. [[LOGAN]] approves the merge
4. If both are modifying `.github/` simultaneously, [[LOGAN]] resolves

---

## 6. CONFLICT RESOLUTION

### Principle

[[LOGAN]] decides. Always. No agent overrides another agent. No agent has precedence based on tier alone.

### Process

1. Agent detects potential conflict (same file, overlapping scope, contradictory instructions)
2. Agent issues **FLAG** with severity and description
3. Agent **STOPS** work on the conflicting item
4. [[LOGAN]] reviews and directs
5. Directed agent proceeds; other agent acknowledges via **HANDSHAKE**

### Merge Conflicts

If a `git merge` or `git pull` produces conflicts:
1. **STOP.** Do not auto-resolve.
2. Report to [[LOGAN]] with the specific files and conflict markers
3. Conflicts signal another conversation has been active — context may be stale
4. Re-read `CONSTITUTION.md` and `LEVELSET.md` to reorient

---

## 7. PENDING DEFINITIONS

These items require [[LOGAN]]'s direction before they can be formalized:

| Item | Status | Notes |
|---|---|---|
| Gemini capability tier and scope | **Undefined** | Pixel smartphone, loganfinney27@gmail.com. No vault commits until defined. |
| Copilot non-vault repo boundaries | **TBD** | Multi-repo admin decided; specific latitude per repo not yet specified. |
| Slack bot apps | **Blocked** | [[LOGAN]] must configure before agents can post independently. |
| `!ADMIN/ROUTING/` folder | **Recommended** | File-based async handoff drops. Not yet created. |
| Research instance (Tier 4) | **Not yet assigned** | Tim Oren analysis, NICAR23 training queued when available. |
| Grok scope and boundaries | **Minimal** | Research/web search role identified. No vault access. |
| M365 Copilot role | **Informational only** | No repo involvement. |
| NotebookLM role | **TBD** | Identified, not yet scoped. |
| PUBLIC: CONVERSATION classification | **Consultation pending** | Constitutional analysis from ADMINISTRATION requested. |

---

## DOCUMENT METADATA

- **Created:** 2026-03-16
- **Author:** PERMANENT: AUTHORITY: CODE (draft)
- **Status:** Draft — awaiting [[LOGAN]]'s review
- **Authority:** [[LOGAN]]'s discretion
