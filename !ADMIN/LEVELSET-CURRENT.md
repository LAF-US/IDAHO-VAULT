---
tags:
  - administration/levelset
  - administration/current-state
updated: 2026-03-22
auto-update: true
---
# LEVELSET — Current State

**Purpose:** Cross-agent context hub. All agent instances — including external agents with no repo access — should be given this file at session start. Automatically updated by `.github/workflows/levelset-sync.yml` when new LEVELSET reports are committed.

**Authoritative as of:** 2026-03-22

---

## VAULT IDENTITY

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repo:** github.com/loganfinney27/IDAHO-VAULT (public)
**Tool:** Obsidian.md — ~3,000 notes, version-controlled with git
**Purpose:** Personal journalism research vault. All committed content is on the record and publishable.

---

## GOVERNANCE STACK

Read these files in order to orient yourself. If you don't have repo access, ask Logan to paste them.

1. `CONSTITUTION.md` (root) — Core identity and constraints. Logan is human; agents are software.
2. `PROTOCOL.md` (root) — 18 operational terms shared across the swarm.
3. `AGENTS.md` (root) — Agent registry, capability rules, communication rules, boundary rules.
4. `LEVELSET.md` (root) — Living ecosystem status. Current projects, unresolved items, conversation awareness.
5. `!ADMIN/ORIENT-v0.1.md` — STEP-0 LEVELSET prompt for external agents (no direct repo access).

---

## AGENT ROSTER

All AI instances are infrastructure. No instance has standing or decision-making authority.

| Agent | Platform | Capability | Scope | GitHub Access |
|---|---|---|---|---|
| PERMANENT: AUTHORITY: CODE | Claude Code CLI | Direct write | Repo operations, deployment, automation | Full repo read/write |
| PERSISTENT: ADMINISTRATION | Claude (conversation) | Draft only | Constitutional layer, handoffs, judgment calls | None — produces drafts |
| GitHub Copilot (ADMIN GitHub) | GitHub Copilot | Multi-repo admin | GitHub administration | GitHub APIs, all repos |
| Gemini | Google AI | TBD — scope undefined | TBD | TBD |

**Capability levels:**
- **Direct write:** Can commit/push to repo. LEVELSET before significant commits.
- **Multi-repo admin:** GitHub API access across all Logan's repos. Draft PRs for vault changes.
- **Draft only:** Produces drafts; Logan pushes. No direct commits.

---

## CORE PRINCIPLES

These are non-negotiable for all agents:

1. **Logan is human. Agents are software.** Logan directs; agents execute.
2. **Public repo = on the record.** All committed content is publishable.
3. **Off-the-record material is ephemeral.** Never log, never store, never reference.
4. **Chat is ephemeral. Vault is the record.** If chat and vault text disagree, the vault wins.
5. **Everything Claude/Copilot produces is a draft** until Logan verifies.
6. **`!ADMIN/` is canonical** for governance and session artifacts.

---

## CURRENT STATE SNAPSHOT

*(Maintained automatically by `levelset-sync.yml` — do not edit this table manually.)*

| Report File | Date |
|---|---|
| *(no LEVELSET reports found)* | — |

---

## ORIENT v0.1 — External Agent Protocol

For agents with **no direct repo access**, the ORIENT protocol is defined at `!ADMIN/ORIENT-v0.1.md`.

**In brief:** When Logan says "LEVELSET", answer these 6 things in order:
1. WHO YOU ARE — your name, platform, capabilities
2. WHAT YOU KNOW — what's been pasted to you; what you can/cannot access
3. WHAT YOU'VE DONE — what you've produced in THIS conversation
4. WHAT IS UNRESOLVED — pending items, unclear context
5. WHAT YOU NEED — what additional vault excerpts or decisions you need
6. COLLISION RISKS — any risk of conflicting changes or stale assumptions

Then propose 2–4 small, reversible next steps within your actual capabilities.

---

*This file is auto-updated by `.github/workflows/levelset-sync.yml` when new LEVELSET reports are committed. The "Last LEVELSET reports" table is machine-maintained. The rest of this file is updated via PR with Logan's approval.*
