---
created: 2026-03-23
source: commit
status: draft
verified-through: 2026-03-23
related:
- '2026-03-15'
- '2026-03-16'
- '2026-03-22'
- '2026-03-23'
- AGENTS
- BOOTSTRAP
- BRANCH-STATUS-2026-03-22
- CLAUDE
- CONTEXT-PASSOVER-COPILOT-2026-03-16
- CONTEXT-VAULT-2026-03-16
- ChatGPT
- Copilot
- FLAG
- GEMINI
- GITHUB-AGENT-SETUP-SUMMARY-2026-03-22
- GitHub
- HANDOFF-CODE-TO-CLAUDE-2026-03-23
- HANDOFF-CODE-TO-GEMINI-2026-03-23
- HANDOFF-CODE-TO-SWARM-2026-03-15
- LEVELSET
- LEVELSET-EXTERNAL-AGENT-PROMPT
- LOGAN
- Logan's
- M365
- NOT
- NotebookLM
- PROTOCOL
- PROTOCOL-PASSBACK-SYNC
- PUBLIC
- SET
- TOSS
- USE
- agent
- coordination
authority: LOGAN
---
# READY STATE — VAULT CONTEXT PACKAGE (2026-03-23)

**Author:** ChatGPT Codex
**Role:** Direct-write support agent acting under LOGAN's instruction
**Purpose:** Provide a verified, relay-ready context snapshot so additional vault agents can start from shared ground without re-discovering core repo state.
**Audience:** Gemini, Claude, and any Logan-routed swarm agent that needs an on-record starting point.

---

## 1. WHAT THIS PACKAGE IS

This file is a verified context snapshot for the current repo-visible state on 2026-03-23. It is meant to reduce repeated orientation work across agents.

It is **not** an authorization document. LOGAN remains the sole decision-maker. Agents execute; they do not decide.

It is **not** a claim of total truth about Logan's broader system. It only summarizes what is directly visible in this repository and its tracked governance/context files.

---

## 2. GOVERNING ASSUMPTIONS

1. LOGAN is the human supervisor and sole decision-maker.
2. All agent-to-agent coordination flows through or is visible to LOGAN.
3. Public repo means on-the-record.
4. Durable decisions belong in vault files; ephemeral chat is not the system of record.
5. Agents must distinguish verified repo state from described-but-unverified conversational claims.

---

## 3. VERIFIED CONTROLLING FILES TO READ FIRST

For any agent starting work, these are the minimum files to absorb before acting:

1. `CLAUDE.md` — shared vault conventions, naming, frontmatter, sourcing, git practices.
2. `AGENTS.md` — current agent registry, capability tiers, boundary rules, and communication rules.
3. `PROTOCOL.md` — definitions for HANDOFF, HANDSHAKE, CONTEXTUALIZE, FLAG, and related coordination terms.
4. `GEMINI.md` — Gemini-specific framing and constraints.
5. `!ADMIN/LEVELSET-EXTERNAL-AGENT-PROMPT.md` — bootstrap prompt for agents without direct repo access.
6. `!ADMIN/PROTOCOL-PASSBACK-SYNC.md` — TOSS/BOOTSTRAP/HANDSHAKE extraction-and-ingestion workflow.

---

## 4. VERIFIED CURRENT SWARM SHAPE

Visible current agent roles in `AGENTS.md`:

- **PERMANENT: AUTHORITY: CODE** — direct write for repo operations and automation.
- **PERSISTENT: ADMINISTRATION** — draft-only constitutional/governance support.
- **GitHub Copilot (ADMIN GitHub)** — multi-repo admin, PR and GitHub maintenance role.
- **ChatGPT Codex** — direct-write scripting/support role, repo read/write.
- **Gemini ("The Vault Advisor")** — advisory, narrative/political context, no code touch.
- Additional read/analysis entities include PERSISTENT: IMPLEMENTATION, TASK: LEVELSET reports, STORY: JFAC Open Meetings, Grok, M365 Copilot, NotebookLM, PUBLIC: CONVERSATION.

Current communication model:
- GitHub Issues and PRs are the active coordination layer.
- Vault files are the durable record.
- `!/` and `!ADMIN/` are active storage locations for prompts, routing, and context packages.

---

## 5. VERIFIED CURRENT SUPPORTING MATERIALS

Already present and reusable:

- `!ADMIN/BRANCH-STATUS-2026-03-22.md` — branch triage and merge-order report.
- `!ADMIN/GITHUB-AGENT-SETUP-SUMMARY-2026-03-22.md` — summary of prior branch/merge support work.
- `CONTEXT-VAULT-2026-03-16.md` — context-preservation dump from multi-conversation collapse.
- `CONTEXT-PASSOVER-COPILOT-2026-03-16.md` — verified passover guide for Copilot.
- `HANDOFF-CODE-TO-SWARM-2026-03-15.md` and related handoffs — earlier relay docs.
- `!ADMIN/LEVELSET-EXTERNAL-AGENT-PROMPT.md` — reusable startup prompt for non-repo agents.
- `!ADMIN/PROMPTS/BOOTSTRAP.md` and `!ADMIN/PROMPTS/TOSS.md` — Logan-run prompts for extracting and vaulting context.

This means the vault already has the beginnings of a repeatable context-ingestion system; what was missing was a fresh, simplified ready-state packet for current agents.

---

## 6. WHAT AN INCOMING AGENT SHOULD ASSUME

### If the agent DOES have repo access

- Read the six controlling files listed above.
- Treat repo text as canonical over paraphrased claims.
- Before changing governance or automation files, compare work against current `AGENTS.md`, `PROTOCOL.md`, and branch-status/context docs.
- If overlapping work is detected, FLAG and pause for LOGAN.

### If the agent DOES NOT have repo access

- Use `!ADMIN/LEVELSET-EXTERNAL-AGENT-PROMPT.md` as the startup prompt.
- Work only from text Logan pastes into the conversation.
- Do not claim repo visibility.
- Produce drafts, analysis, summaries, or recommendations only.

---

## 7. KNOWN RISKS / COLLISION SURFACES

1. **Governance duplication risk** — root governance files and `!ADMIN/` support files coexist; agents must confirm which file is authoritative before editing.
2. **Stale branch risk** — branch-status reporting already notes stale and collision-prone branches; branch assumptions should be rechecked before implementation.
3. **Process-artifact sprawl** — multiple handoffs, context dumps, and LEVELSET-style files exist; agents should prefer current controlling docs over older process artifacts.
4. **Capability overclaim risk** — external agents must not imply repo, Slack, or GitHub account access they do not have.

---

## 8. IMMEDIATE READY-TO-USE PACKAGE SET

This ready-state file is paired with two direct handoff packets:

- `!ADMIN/CONTEXTS/HANDOFF-CODE-TO-GEMINI-2026-03-23.md`
- `!ADMIN/CONTEXTS/HANDOFF-CODE-TO-CLAUDE-2026-03-23.md`

Use those files when Logan wants to brief a specific agent quickly.

---

## 9. STATUS

**State:** Ready for relay.

**What is done:**
- Shared repo-visible context has been condensed into a current packet.
- Agent-specific handoffs have been prepared for Gemini and Claude.
- Materials are stored in `!ADMIN/CONTEXTS/` for re-use.

**What is not done:**
- No claims are made here about Slack bot setup, live private conversations, or external services.
- No new decisions were made.
- No existing agent output outside the repo was treated as verified unless committed in files.

---

**Routing note for Logan:** Relay this file first if an agent needs a general orientation. Then relay the agent-specific handoff packet.
