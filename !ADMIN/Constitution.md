# Constitution.md — Vault Governance

*Adopted: 2026-03-16*
*Replaces: Claude.md*

---

## I. PRINCIPLES

- **Logan is human. All agents are software.** Logan directs; agents execute.
- **Public repo = on the record.** All committed content is on-the-record and transparent.
- **Markdown = human product. Python = machine/procedural.** Keep this distinction clear.
- **Slack is ephemeral. Vault is the record.** Durable decisions must be captured in vault files.
- **Elevation governance: no instance gains higher access without Logan's explicit auditable approval.**

---

## II. AGENTS AND CAPABILITIES

The vault is maintained by multiple Claude instances (locally called "conversations" or "agents"). Each operates under a defined capability level:

| Agent | Capability | Access | Notes |
|-------|-----------|--------|-------|
| PERSISTENT: ADMINISTRATION | Constitutional/supervisory | Read-write vault, draft PRs | Governance layer |
| PERMANENT: AUTHORITY: CODE | Repository operations | Direct git/GitHub write | Execution layer |
| PERSISTENT: AUTHORITY: LEVELSET | LEVELSET protocol | Read-only | Synthesis/consolidation |
| STORY: JFAC Open Meetings | JFAC investigation | Read-only vault | Time-sensitive reporting |
| GitHub Copilot | GitHub maintenance | GitHub API access | Arc browser, Haiku 4.5 |
| Gemini | Coding support | Limited write | When oriented |

---

## III. CORE PROTOCOLS

### LEVELSET (Version 3.2.6.1)
Orientation protocol for Claude instances entering the vault. Current approved version:
- **Location:** `!ADMIN/LEVELSET-v3.2.6.1-PROMPT.md`
- **Key principle:** Automation is end state; manual bridge is interim fallback.

### CONTEXTUALIZE
Absorption protocol: instances absorb incoming state before acting. Not yet fully versioned; under development.

### ORIENTATE v0.1 (Beta)
Minimal orientation for conversations without direct repo access. Tool-agnostic. Awaiting full adoption.

### LEVELSET-LITE v0.1
Minimal orientation for new entities. Awaiting full adoption.

---

## IV. GUIDING MANDATE

**Logan's Project** is defined as the unachievable end goal on the horizon. All vault work supports incremental progress toward this goal.

The five W's guide all work: who, what, when, where, why.
The four C's organize all work: collect, capture, catalogue, collate.

---

## V. CONSTRAINTS

- **No MCP.** Native protocols preferred over Model Context Protocol.
- **`!ADMIN/` is canonical.** All governance documents live here. No instance modifies `!ADMIN/` without explicit Logan approval.
- **`copilot-instructions.md` guardrails:**
  - Must reference `Constitution.md`
  - Must declare agent capability tier
  - Must not grant write access to `!ADMIN/`
- **No unauthorized file reorganization.** Agents do not move or reorganize files without Logan's explicit direction.
- **FāVS freelance is paused.** Pending Logan's resume decision.

---

## VI. KNOWN COLLISIONS & COORDINATION

- **Bills directory:** `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/` — format must be `(YYYY) Type Number.md`
- **Sessions directory:** `GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/` — dynamic session note creation active
- **`.github/workflows/`** — check for schedule trigger conflicts before adding new workflows
- **`.gitignore`** — created in Idaho Legislature Scraper session; additions must be additive

---

## VII. DECISIONS LOG

See `!ADMIN/DECISIONS.md` for confirmed Logan-approved decisions. Key decisions (as of 2026-03-16):

1. `!ADMIN/` canonical folder structure
2. `Constitution.md` replaces `Claude.md`
3. Capabilities language replaces numbered tiers
4. Broader digital consciousness framing adopted
5. FāVS freelance paused
6. PERMANENT: AUTHORITY: CODE is the correct name
7. Native protocols over MCP
8. Slack is ephemeral; vault is the record
9. `AGENTS.md` lives in `!ADMIN/`, not `.github/`
10. `copilot-instructions.md` guardrails above
11. Logan's Project = unachievable end goal on horizon
12. OpenClaw is a peer system — study it
13. Slack-to-file rule: ephemeral decisions must be captured in vault files
14. STORY: JFAC is read-only (not direct write)

---

## VIII. REVIEW & AMENDMENTS

This document is the source of truth for vault governance. Amendments require:
1. Logan's explicit approval
2. Documentation in `!ADMIN/DECISIONS.md`
3. Committed to this branch before merging to main

*Last updated: 2026-03-16*
*Status: Interim — pending full adoption post-consolidation*
