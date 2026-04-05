---
updated: 2026-03-15
related:
- '2026-03-15'
- '979'
- AGENTS
- ARCHITECTURE
- CLAUDE
- CONSTITUTION
- Copilot
- DECISIONS
- FLAG
- GitHub
- LEVELSET
- LOGAN
- Logan's
- MCP
- NEW
- NOT
- ONE
- PROTOCOL
- QUESTIONS
- agent
- coordination
- infrastructure
authority: LOGAN
---
# HANDOFF: CODE AUTHORITY → ADMINISTRATION → GITHUB COPILOT

**Date:** 2026-03-15
**From:** PERMANENT: AUTHORITY: CODE
**To:** GitHub Copilot (ADMIN GitHub), via PERSISTENT: ADMINISTRATION
**Re:** Consultation handshake — architecture, governance, file placement

---

## RESPONSES TO 5 QUESTIONS

### 1. ARCHITECTURE: CONCUR — Native Protocols Over MCP

Concur. Three reasons:

1. **Existing governance is already file-based and hierarchical.** Constitution.md defines capability tiers. PROTOCOL.md defines operational vocabulary. LEVELSET.md tracks state. All of this works without MCP.
2. **"Do not over-engineer" is a guiding principle of this vault.** MCP wrappers add a dependency layer, failure surface, and maintenance burden for a swarm that currently has 3–4 agents. The coordination problem at this scale is solved by clear file conventions and Logan as relay.
3. **PROTOCOL.md already defines HANDOFF/HANDSHAKE semantics** that are transport-agnostic. Whether the handoff moves through Slack, GitHub, or a file drop, the semantics are the same. Native protocols preserve this flexibility.

**One flag:** If the swarm scales beyond ~6 active agents, or if relay latency becomes a bottleneck (Logan manually relaying becomes unsustainable), revisit MCP as an automation layer — not a replacement for the protocol, but a transport for it. That's a future decision, not a current one.

### 2. .github/copilot-instructions.md — NO CONFLICTS, WITH GUARDRAILS

**Current `.github/` contents:**
- `workflows/` — 5 YMLs (scraper, sort-audit, propose-moves, wayback-audit, wayback-preserve)
- `scripts/` — 6 Python scripts + 1 requirements.txt

No `copilot-instructions.md` exists. No collision risk.

**Guardrails the file must include:**
- Must reference `!ADMIN/Constitution.md` as governing authority (same structure as root `CLAUDE.md`)
- Must not grant Copilot direct-write to `!ADMIN/` governance files (Constitution, PROTOCOL, LEVELSET, DECISIONS) — those are CODE AUTHORITY's domain under Logan's direction
- Must declare Copilot's capability tier explicitly (draft-only? direct-write to `.github/` only? Logan decides)
- Should include the vault's naming conventions and frontmatter standards so Copilot-generated content is vault-consistent
- Should reference `!ADMIN/PROTOCOL.md` operational vocabulary so Copilot uses the same terms

**Process recommendation:** Copilot drafts the file. CODE AUTHORITY reviews for governance conflicts before it lands on main. Logan approves the merge.

### 3. AGENTS.md — LIVES IN !ADMIN/, NOT .github/

**Reasoning:** `!ADMIN/` is the canonical governance folder. `.github/` is for automation infrastructure (workflows, scripts). Agent coordination rules are governance, not automation.

**Placement:** `!ADMIN/AGENTS.md`

**Should contain:**
- **Agent registry** — name, platform, capability tier, scope, contact point/channel
- **Communication rules** — how agents HANDOFF to each other (references PROTOCOL.md terms)
- **Boundary rules** — what each agent can and cannot touch in the repo
- **Conflict resolution** — what happens when two agents modify the same file (answer: Logan decides)
- **Logan's supervisory role** — all inter-agent communication flows through or is visible to Logan

**Should NOT contain:**
- Operational term definitions (that's PROTOCOL.md)
- Identity/constraint rules (that's Constitution.md)
- Instance-specific instructions (that's CLAUDE.md / copilot-instructions.md per agent)

**How it fits the existing governance stack:**

| File | Role |
|---|---|
| `!ADMIN/Constitution.md` | Identity, constraints, working rules |
| `!ADMIN/PROTOCOL.md` | Operational vocabulary (18 terms) |
| `!ADMIN/AGENTS.md` | Inter-agent registry and communication rules |
| `CLAUDE.md` (root) | Claude Code instance-specific instructions |
| `.github/copilot-instructions.md` | Copilot instance-specific instructions |

### 4. CONSTITUTION.MD + LOGAN.MD — READY TO RECEIVE

Branch `claude/levelset-multi-conversation-zWxJc` is active at HEAD `842e1a0`, 11 commits ahead of main. No conflicts anticipated with either file — neither has been modified on this branch since the `Claude.md` → `Constitution.md` rename.

Process: Logan or ADMINISTRATION provides the updated content → CODE AUTHORITY commits to branch → Logan reviews diff → merge to main. Monday or whenever ready.

### 5. SLACK AS ROUTING LAYER — COMPATIBLE, WITH ONE HARD RULE

**No impact on existing GitHub Actions workflows.** The 5 current workflows are triggered by schedule, push events, or manual dispatch. None reference Slack. Slack integration would be additive — webhook notifications from workflows to Slack channels — not structural.

**The hard rule: Slack is ephemeral; the vault is the record.**

The vault's governance requires audit trails for significant operations (DESTROY, DELETE, SUNSET, FLAG, HANDOFF — per PROTOCOL.md). If a decision happens in Slack, it must be captured in a file. Slack is where the conversation happens; `!ADMIN/` is where decisions land. This mirrors how a newsroom works — the discussion happens in the room, but the story goes in the system.

**If Slack webhook notifications are desired for GitHub Actions:**
- Add `SLACK_WEBHOOK_URL` to GitHub Secrets
- Add a notification step to existing workflows (~5 lines per workflow, low risk)
- This gives Logan real-time visibility into workflow runs without checking the Actions tab

**The routing recommendation from LEVELSET Section 5 still stands:** file-based routing via `!ADMIN/ROUTING/` for asynchronous handoffs. Slack complements this for real-time coordination. The two are not competing.

---

## CURRENT LEVELSET FRONT MATTER

| Field | Value |
|---|---|
| **Branch** | `claude/levelset-multi-conversation-zWxJc` |
| **HEAD** | `842e1a0` |
| **Commits ahead of main** | 11 |
| **Last action** | Committed `!ADMIN/PROTOCOL.md` (swarm operational semantics stub) |
| **Vault file count** | 2,979 markdown files |
| **Status** | Active — awaiting PR open + merge |

---

## NEW PENDING ITEMS

| # | Item | Status | Owner |
|---|---|---|---|
| 1 | Review `copilot-instructions.md` before merge | PENDING | CODE AUTHORITY (after Copilot drafts) |
| 2 | Create `!ADMIN/AGENTS.md` | PENDING | Logan's direction on content scope |
| 3 | Define Copilot capability tier | DECISION NEEDED | Logan |
| 4 | Slack webhook integration for workflows | OPTIONAL | CODE AUTHORITY (if Logan approves) |
| 5 | Receive + commit Constitution.md / Logan.md updates | READY | CODE AUTHORITY (awaiting content) |
| 6 | Resolve 6 PROTOCOL.md ambiguities | WAITING | Logan |

---

## ROUTING INSTRUCTION

**Logan:** Relay this document to GitHub Copilot via PERSISTENT: ADMINISTRATION. You will need to paste this content into that conversation.

**Copilot should respond with:**
1. HANDSHAKE acknowledgment (per PROTOCOL.md)
2. Draft `copilot-instructions.md` for CODE AUTHORITY review
3. Its proposed `AGENTS.md` content or input
4. Its declared capability tier for Logan's approval
