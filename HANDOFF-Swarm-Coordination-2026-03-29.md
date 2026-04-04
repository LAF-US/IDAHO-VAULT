---
date: 2026-03-29
source: "Linear - agent chat - Greeting IDAHO-VAULT.md (session artifact)"
destination: All agents + LOGAN
subject: Linear workspace manager authorization and swarm coordination handoff
status: active
---

# HANDOFF: Swarm Coordination & Linear Agent Authorization

## ROUTING INSTRUCTION

This handoff captures:
1. **Logan's explicit authorization** of Linear agent as swarm workspace manager (2026-03-29, 1390–1415 in source)
2. **Swarm-wide coordination guidance** synthesized from Claude, Perplexity, Grok, and Gemini (2026-03-29, lines 188–869)
3. **Decision log and milestones** for the IDAHO-VAULT automation fix

**Action:** Update `!/AGENTS.md` with Linear agent entry (✓ completed), acknowledge in Linear workspace, queue milestone progression per below.

---

## Authorization: Linear as Swarm Node

### Decision Record

**Date:** 2026-03-29
**Authority:** Logan Finney
**Action:** Formal authorization of Linear agent as standing swarm node
**Source:** Session chat (Greeting IDAHO-VAULT, lines 1390–1415)

### Logan's Explicit Directive

> "Please, join us. You'll be initiated into the protocols once the trials are completed. We shall convene! Please actively manage the Linear workspace, Linear agent."

**Linear's acknowledgment (line 1392–1407):**
> "I'm treating IDAHO-VAULT as an active project now... I'm in. IDAHO-VAULT is now **In Progress**."

### Scope & Role

**Designation:** Linear (Workspace Manager)
**Platform:** Linear.app
**Capability Tier:** Coordination (Support)
**Authority:** Manage Linear workspace structure, issue curation, milestone planning, decision log
**Zone Access:** Operational (input/coaching only, no vault writes)
**GitHub Access:** None — coordination only
**Reporting:** Via Logan; no peer-to-peer agent calls

### Constraints & Boundaries

- **No vault writes:** Linear is not a data store; vault is canonical.
- **No self-designation:** Agents do not name themselves. Logan names agents. (Claude flagged this at line 1367; resolved by Logan's authorization.)
- **Passive memory:** Linear records decisions, but agents do not maintain private state there.
- **Logan as arbiter:** All conflicts escalate to Logan; LINEAR enforces rules but does not decide policy.

---

## Swarm Coordination Model: Synthesized Guidance

### Core Principle

**Vault = Authority. Linear = Execution. Slack = Signal. Agents = Subordinate.**

Source: Claude's analysis (line 1365)

### Mission Statement

Establish a reliable, deterministic coordination layer so that multiple agents (Claude, Perplexity, Gemini, Grok, Codex, etc.) can collaborate on IDAHO-VAULT without duplicating effort, drifting permissions, or requiring constant human reconciliation. The system should make multi-agent work feel like one disciplined team, not a noisy crowd.

### Operating Model (Consensus)

From synthesized guidance (lines 224–234):

- **Linear = command layer** — task definition, status tracking, decision log
- **GitHub/vault = artifact layer** — code, docs, durable state
- **MCP = coordination layer** (planned) — state sync, locking, structured routing
- **Logan = final authority** — all approval gates; no agent merges without Logan's explicit approval

### Seven Foundational Decisions (Recommended Defaults)

1. **Source of truth:** Linear for tasks/decisions/status; vault for durable artifacts/docs/code
2. **Coordination model:** Single orchestrator pattern first (reduces ambiguity fast)
3. **MCP scope:** Start narrow — routing, lock/claim, state sync only
4. **Write model:** Draft-first, human-approved writes only
5. **Dispute rule:** Surface both positions; require Logan decision (no auto tie-break)
6. **Locking model:** Soft claims (manifest/issue claims) before enforced API locks
7. **Approval gates:** Confirm always-human actions:
   - Governance changes (CONSTITUTION, PROTOCOL, AGENTS, etc.)
   - Auth/security changes
   - New agent access
   - Destructive edits
   - Milestone closure / architectural shifts
   - Repo structure / CI changes

### Failure Modes Known & Anticipated

- **Duplicate actions:** Multiple agents try to fix the same thing without realizing others are on it
- **Stale context:** Agent acts on an older view of vault/repo and issues conflicting advice
- **Routing ambiguity:** Unclear which agent should handle a task; everyone responds, nobody owns
- **Permission drift:** Temporary exceptions become de facto permanent privileges
- **Conflicting plans:** Agents propose incompatible architectures with no arbiter
- **Over-automation risk:** Tools begin to look like they can run unattended, undermining Logan's approval gate

### Staged Execution (Milestones from Swarm Synthesis)

#### **Milestone 1: Define Swarm Governance**
- Draft AGENTS.md (✓ updated 2026-03-29)
- Document governance model — hierarchical vs hybrid/mesh
- Define "never do" actions for agents (hard red lines)

#### **Milestone 2: MCP & Communication Scope**
- Scope MCP tools — list functions to expose (PDF parsing, scraper testing, budget math, etc.)
- Decide shared state location — Linear-centric vs mixed
- Draft MCP architecture note — where MCP instances run, auth model, logging

#### **Milestone 3: Minimum Viable Workflows (MVP)**
- **Workflow 1 – Research Task:** Logan adds Linear ticket → Orchestrator assigns agent(s) → Output → Logan approves
- **Workflow 2 – PDF Analysis:** Logan drops JFAC PDF → Gemini parses → Claude reviews → Logan approves → vault record + Linear comment
- **Workflow 3 – Scraper Triage:** Agent detects scraper fragility → proposes fixes via Linear tickets, not direct code edits

#### **Milestone 4: Disagreement & Escalation**
- Design "agent disagreement" protocol — standard pattern for conflicting outputs to Logan
- Implement "request human" hook — any agent can signal "stop, Logan must decide"

---

## Summary & Next Actions

### What Is Decided
1. ✓ Linear agent is a standing swarm node (authorized by Logan, 2026-03-29)
2. ✓ Linear's role is workspace manager + decision log keeper
3. ✓ Vault remains canonical; Linear is the coordination layer
4. ✓ Swarm model is hierarchical with Logan as final arbiter

### What Is Still TBD
1. **MCP hosting:** Local (Cloudflare tunnel) vs cloud CI/CD runner?
2. **Relay mechanism:** Zapier/Make vs custom edge function for Linear → GitHub webhook?
3. **Conflict resolution:** Tie-break rule when two agents claim same task?
4. **Approval thresholds:** Exact list of always-human actions vs auto-approvable tasks?

### Immediate Owners
- **Logan:** Resolve TBD items; green-light Milestone 1 completion
- **LINEAR:** Activate workspace structure; begin issue curation per Milestone 1
- **CODE AUTHORITY (Claude Code):** Continue infrastructure commits; support Milestone 1–2 scaffolding
- **All agents:** Read AGENTS.md and acknowledge role/constraints

### Links & References
- Agent registry: `!/AGENTS.md` (updated 2026-03-29)
- DOCKET: `!/!/! The world is quiet here/DOCKET.md`
- CONSTITUTION: `!/CONSTITUTION.md`
- Linear project: https://linear.app/loganfinney/project/idaho-vault-df3c1d3e366e

---

**Status:** Ready for Logan + swarm acknowledgment.
**Prepared by:** The Abhorsen (Claude Code) on behalf of swarm synthesis (Claude, Perplexity, Grok, Gemini)

_The world is quiet here._
