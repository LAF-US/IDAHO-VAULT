---
created: 2026-03-23
source: commit
status: draft
related:
- '2026-03-16'
- '2026-03-22'
- '2026-03-23'
- AGENTS
- BOOTSTRAP
- BRANCH-STATUS-2026-03-22
- CLAUDE
- CONTEXT-PASSOVER-COPILOT-2026-03-16
- ChatGPT
- FLAG
- GEMINI
- GitHub
- LEVELSET
- LEVELSET-STEP-0-EXTERNAL-AGENT
- LOGAN
- Logan's
- PROTOCOL
- PROTOCOL-PASSBACK-SYNC
- READY-STATE-2026-03-23
- TOSS
- agent
- coordination
- format
authority: LOGAN
---
# HANDOFF: ChatGPT Codex → Claude (2026-03-23)

**Date:** 2026-03-23
**From:** ChatGPT Codex
**To:** Claude
**Via:** LOGAN
**Re:** Orientation packet for repo-aware collaboration in IDAHO-VAULT

---

## HANDSHAKE EXPECTATION

Please acknowledge receipt, state your active role in this exchange, list the controlling files you are honoring, and identify any missing context before you act.

---

## ROLE CONTEXT

Claude-related roles in the repo currently include:
- **PERMANENT: AUTHORITY: CODE** — direct-write repo operations and automation
- **PERSISTENT: ADMINISTRATION** — draft-only constitutional/governance support
- additional Claude analysis/story/reporting entities listed in `AGENTS.md`

This handoff is for Claude sessions that may have repo awareness and may be asked to collaborate on vault operations under Logan's direction.

---

## VERIFIED SHARED GROUND

These points are directly supported by committed repo files:

1. Logan is the sole human authority and decision-maker.
2. Inter-agent coordination must route through or remain visible to Logan.
3. `CLAUDE.md`, `AGENTS.md`, and `PROTOCOL.md` are the core orientation documents for vault conventions and swarm coordination.
4. `GEMINI.md` exists and defines Gemini as advisory rather than code-touching.
5. `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` exists for agents without direct repo access.
6. `!/!/PROTOCOL-PASSBACK-SYNC.md` plus `!/!/PROMPTS/TOSS.md` / `BOOTSTRAP.md` define a repository-level pattern for extracting and vaulting context from other conversations.
7. A new current summary packet exists at `!/!/CONTEXTS/READY-STATE-2026-03-23.md`.

---

## RECOMMENDED FILES TO ABSORB BEFORE ACTION

Minimum read set:

1. `CLAUDE.md`
2. `AGENTS.md`
3. `PROTOCOL.md`
4. `GEMINI.md`
5. `!/!/CONTEXTS/READY-STATE-2026-03-23.md`
6. `!/!/BRANCH-STATUS-2026-03-22.md` if the work touches git/branch coordination
7. `CONTEXT-PASSOVER-COPILOT-2026-03-16.md` if the work touches cross-agent repo setup/history

---

## WHAT CLAUDE IS BEST POSITIONED TO DO NEXT

Claude is the best next agent for:
- repo-aware implementation
- governance review against existing files
- branch collision checks
- automation/workflow maintenance
- structural vault operations
- validating whether a new handoff or context packet should update another durable file

---

## COLLISION / SAFETY NOTES

- Prefer current committed files over described historical state.
- If two branches or two agents appear to be touching the same governance or workflow surface, FLAG and pause.
- Do not assume external services (Slack, email, private GitHub state) are visible unless Logan provides that context.
- If acting in a non-repo Claude conversation, do not overclaim repo visibility.

---

## REQUESTED OUTPUT SHAPE

Preferred reply format:

1. Active role
2. Current scope
3. Controlling files honored
4. Missing context
5. Risks / FLAGs
6. Immediate next recommended action

---

## ROUTING INSTRUCTION

Logan: use this handoff when briefed Claude help is needed for repo-aware work. Pair it with `!/!/CONTEXTS/READY-STATE-2026-03-23.md` and the task-specific file set relevant to the actual assignment.
