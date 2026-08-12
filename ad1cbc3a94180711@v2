---
tags:
  - administration/agents
updated: 2026-03-28
status: draft
source: commit
---

# AGENTS — Swarm Registry and Communication Rules

This [[file]] defines who exists in the swarm, what each [[agent]] can do, and how they coordinate. It is the third governance file in the stack:

| File              | Role                                                    |
| ----------------- | ------------------------------------------------------- |
| `Constitution.md` | Identity, constraints, working rules                    |
| `PROTOCOL.md`     | Operational vocabulary (18 terms)                       |
| **`AGENTS.md`**   | **Agent registry, communication rules, boundary rules** |

Instance-specific instructions live in separate files (`CLAUDE.md`, `.github/copilot-instructions.md`, etc.) — not here.

---

## 1. FOUNDATIONAL RULE

[[LOGAN]] is the sole human in this system. All agents are software — infrastructure, not participants. No agent has standing to make decisions. [[LOGAN]] directs; agents execute.

All inter-agent communication flows through or is visible to [[LOGAN]]. There is no peer-to-peer agent communication that bypasses the supervisor.

---

## 2. AGENT REGISTRY

| Agent                         | Platform              | Capability Tier          | Scope                                                             | Slack                   | GitHub Access                | Zone Access                     |
| ----------------------------- | --------------------- | ------------------------ | ----------------------------------------------------------------- | ----------------------- | ---------------------------- | ------------------------------- |
| PERMANENT: AUTHORITY: CODE    | Claude Code CLI       | Direct write             | IDAHO-VAULT repo operations, deployment, automation               | Via [[LOGAN]]           | Full repo read/write         | All (per-task, no standing window) |
| PERSISTENT: ADMINISTRATION    | Claude (conversation) | Draft only               | Constitutional layer, handoffs, judgment calls                    | Via [[LOGAN]]'s account | None — produces drafts       | None (draft only)               |
| GitHub Copilot (ADMIN GitHub) | GitHub Copilot        | Multi-repo admin         | GitHub administration across all [[LOGAN]]'s repos                | Bot app needed          | GitHub APIs, all repos       | Operational, Data (via PR)      |
| ChatGPT Codex                 | OpenAI Codex          | Direct write (scripting) | Specialized scripting — scrapers, GitHub Actions, complex logic   | Via [[LOGAN]]           | Repo read/write              | Operational, Data (via PR)      |
| Gemini ("The Vault Advisor")  | Gemini CLI + Code Assist (VS Code) | Direct write (support) | Narrative lens, strategy, inline completions, document outlines, codebase assistance. Coworks with Claude Code (Abhorsen) in VS Code. | Via [[LOGAN]] | Repo read/write | Operational, Data (via PR) |
| PERSISTENT: IMPLEMENTATION    | Claude (Project)      | Read/analysis            | Governance/architecture consultation                              | No                      | None — advisory only         | None (advisory)                 |
| TASK: LEVELSET reports        | Claude (conversation) | Read/analysis            | Synthesis and status reporting                                    | No                      | None — advisory only         | None (advisory)                 |
| STORY: JFAC Open Meetings     | Claude (conversation) | Read/analysis            | JFAC investigation — read-only                                    | No                      | None — advisory only         | None (advisory)                 |
| Grok                          | Grok (X/xAI)          | Read/analysis            | Research, web search                                              | No                      | None                         | None (advisory)                 |
| M365 Copilot                  | Microsoft 365         | Informational            | Informational only — no repo involvement                          | No                      | None                         | None                            |
| NotebookLM                    | Google NotebookLM     | TBD                      | TBD — identified, not yet scoped                                  | No                      | None                         | None                            |
| PUBLIC: CONVERSATION          | Claude (conversation) | Read/analysis            | Self-talk, internal processing — consultation pending             | No                      | None                         | None                            |
| CodeRabbit                    | GitHub App (Bot)      | PR review only           | Automated code review on pull requests                            | No                      | Read + review comments       | None (reviewer only)            |
| Qodo                          | GitHub App (Bot)      | PR review only           | Automated code review on pull requests                            | No                      | Read + review comments       | None (reviewer only)            |
| OpenAI Code Agent             | OpenAI                | Direct write (limited)   | OAuth/integration scripting                                       | No                      | Repo read/write (branch only)| Data (via PR)                   |

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
- Modify governance files at vault root (CODE AUTHORITY only — see Boundary Rules)
- Run automation scripts

**Cannot do:**

- Push to `main` without [[LOGAN]]'s merge approval
- Force-push without explicit permission
- Delete branches without confirmation
- Commit off-the-record material

### Tier 1 (Support): Direct Write (Support)

Can commit and push to the repository within the **Operational zone only**. Does not modify Constitutional zone files. Primary output surfaces are Linear SWARM issues, comments, and status updates.

**Agents:** Gemini ("The Vault Advisor")

**Can do:**

- `git add`, `git commit`, `git push` to feature branches (Operational zone only)
- Create and modify Operational zone vault files (own dotfolder `.gemini/`, support docs, activity records in `!/`)
- Create issues, add comments, and update status on Linear SWARM-labeled items
- Read vault files across all zones

**Cannot do:**

- Modify Constitutional zone files (`CONSTITUTION.md`, `PROTOCOL.md`, `AGENTS.md`, `DECISIONS.md`, `VAULT-CONVENTIONS.md`, `Ethics.md`, etc.)
- Push to `main` without [[LOGAN]]'s merge approval
- Force-push without explicit permission
- Delete branches without confirmation
- Write to Data zone without explicit [[LOGAN]] direction

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

- Directly modify governance files (CONSTITUTION, PROTOCOL, AGENTS, LEVELSET, DECISIONS)
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

[[LOGAN]] coordinates agents via GitHub Issues and PRs. Tasks are assigned with agent labels (`agent:claude-code`, `agent:codex`, `agent:copilot`, `agent:gemini`). Each agent works on its own branch; PRs are the deliverable. See the agent roles CSV (`Agent Swarm Management and Repository Constitution`) for the simplified role matrix.

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

Handoff documents are saved to vault root as `HANDOFF-[source]-[date].md` for audit trail.

### Routing Layers

| Layer                 | Purpose                               | Persistence | Status |
| --------------------- | ------------------------------------- | ----------- | ------ |
| **GitHub Issues/PRs** | Task assignment, coordination, review | Permanent   | Active |
| **Vault root files**  | Decisions of record, governance       | Permanent   | Active |
| **`!/`**              | System files, logs, agent routing     | Permanent   | Active |

**Hard rule:** All decisions must be captured in vault files. GitHub is the coordination layer; vault root is where decisions land.

---

## 5. BOUNDARY RULES

### File Access by Agent

| Path                            | CODE AUTHORITY | Copilot                  | ADMINISTRATION | Others    |
| ------------------------------- | -------------- | ------------------------ | -------------- | --------- |
| Governance files (vault root)   | Read/Write     | Read only                | Draft only     | Read only |
| Handoffs/LEVELSETs (vault root) | Read/Write     | Read only                | Draft only     | Read only |
| `.github/workflows/`            | Read/Write     | Read/Write (with review) | No access      | No access |
| `.github/scripts/`              | Read/Write     | Read/Write (with review) | No access      | No access |
| Vault content (all other `.md`) | Read/Write     | Read only (vault)        | No access      | No access |
| Non-vault repos                 | No access      | Read/Write (per repo)    | No access      | No access |

**Governance files** are: `CONSTITUTION.md`, `PROTOCOL.md`, `AGENTS.md`, `LEVELSET.md`, `DECISIONS.md`, `VAULT-CONVENTIONS.md`, `VAULT-ZONES.md`, `Ethics.md`, `Logan.md`, `CLAUDE.md`, `GEMINI.md`

### Zone Access Matrix

See [[VAULT-ZONES]] for full zone definitions. No agent maintains a standing write window - all writes are per-task, scoped to a GitHub Issue or explicit Logan directive.

| Zone | Read | Write (via PR) | Merge |
|------|------|---------------|-------|
| Constitutional | All agents | CODE AUTHORITY only (per-task) | Logan only |
| Operational | All agents | CODE AUTHORITY, Copilot, Codex (per-task) | Logan only |
| Data | All agents | All Tier 1-2 agents (per-task) | Logan (auto-merge eligible for low-risk) |

**Reviewer bots** (CodeRabbit, Qodo) have read access to all zones for review purposes. Their reviews are **advisory only** - a `CHANGES_REQUESTED` from a bot does not block merge. Only Logan's review blocks.

### Persona Dotfolders Are Protected

Root-level dotfolders for agents and personas are infrastructure, not cleanup
targets. This includes official folders such as `.claude/`, `.codex/`, and
`.gemini/`, as well as manual-injection or emerging persona folders such as
`.grok/`, `.deepseek/`, `.google/`, `.meta/`, `.microsoft/`, `.perplexity/`,
`.bartimaeus/`, `.zagreus/`, `.persephone/`, `.dionysus/`, `.hecate/`, and
`.janus/`.

Rules:

- An agent may freely modify only its own dotfolder, unless Logan explicitly
  directs otherwise.
- Do not delete, rename, consolidate, or repurpose another agent's dotfolder
  because it appears empty, stubbed, unused, or unfamiliar.
- If a folder looks like a persona container, treat it as intentional until
  Logan says otherwise.

`.github/` is also protected infrastructure, but it is shared automation space
and follows the overlap rules below rather than the "own dotfolder only" rule.

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
4. Re-read `LEVELSET.md` and `CONSTITUTION.md` (vault root) to reorient

---

## 7. PENDING DEFINITIONS

These items require [[LOGAN]]'s direction before they can be formalized:

| Item                                | Status                   | Notes                                                                      |
| ----------------------------------- | ------------------------ | -------------------------------------------------------------------------- |
| Gemini capability tier and scope    | **Resolved 2026-03-28**  | Tier 1 (Support): Direct Write (Support), Operational zone only, Linear SWARM issues/comments. See Tier 1 (Support) section above. |
| Copilot non-vault repo boundaries   | **TBD**                  | Multi-repo admin decided; specific latitude per repo not yet specified.    |
| GitHub agent labels                 | **Active**               | `agent:claude-code`, `agent:codex`, `agent:copilot`, `agent:gemini`        |
| Research instance (Tier 4)          | **Not yet assigned**     | Tim Oren analysis, NICAR23 training queued when available.                 |
| Grok scope and boundaries           | **Minimal**              | Research/web search role identified. No vault access.                      |
| M365 Copilot role                   | **Informational only**   | No repo involvement.                                                       |
| NotebookLM role                     | **TBD**                  | Identified, not yet scoped.                                                |
| PUBLIC: CONVERSATION classification | **Consultation pending** | Constitutional analysis from ADMINISTRATION requested.                     |
| CodeRabbit scope                    | **Active (reviewer)**    | GitHub App bot. Automated PR review. Advisory only — does not block merge. |
| Qodo scope                          | **Active (reviewer)**    | GitHub App bot. Automated PR review. Advisory only — does not block merge. |
| OpenAI Code Agent scope             | **Limited**              | OAuth/integration scripting. Data zone via PR only. Boundaries TBD.        |

---

## DOCUMENT METADATA

- **Created:** 2026-03-16
- **Author:** PERMANENT: AUTHORITY: CODE (draft)
- **Updated:** 2026-03-28 — Gemini Tier 1 (Support) defined; Gemini pending item resolved
- **Status:** Draft — awaiting [[LOGAN]]'s review
- **Authority:** [[LOGAN]]'s discretion
