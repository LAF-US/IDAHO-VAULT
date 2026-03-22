---
tags:
  - administration/orient
  - administration/context
updated: 2026-03-22
---
# CONTEXT PASTE BUNDLE — External Agent Orientation

**Purpose:** Pre-packaged context Logan can paste to any external agent (no repo access) to orient them before giving them a task. Update this file when the vault state changes significantly.

**How to use:**
1. Paste `!ADMIN/ORIENT-v0.1.md` first — gives the agent its operating rules.
2. Then paste this file — gives the agent the vault's current context.
3. Say "LEVELSET" to confirm they've absorbed the context.
4. Then give them their task.

---

## PASTE BLOCK — START

*(Copy everything between START and END markers into your chat.)*

---

**IDAHO-VAULT CONTEXT — PASTE BUNDLE**
*For: External agent orientation | Updated: 2026-03-22*

---

### 1. VAULT IDENTITY

- **Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television (IPTV), Boise, Idaho
- **Repo:** github.com/loganfinney27/IDAHO-VAULT (public)
- **Tool:** Obsidian.md — ~3,000 notes, version-controlled with git
- **Purpose:** Personal journalism research vault covering Idaho politics, government, legislation, people, organizations, sources, and topics. All committed content is on the record and publishable.

---

### 2. CORE PRINCIPLES (NON-NEGOTIABLE)

1. Logan is human. You are software. Logan directs; you execute.
2. Public repo = on the record. Everything committed is publishable.
3. Off-the-record material is ephemeral. Never log, never store.
4. Chat is ephemeral. Vault is the record. Vault text wins over chat.
5. All your output is a draft until Logan verifies.
6. Do not introduce new governance structures, protocol names, or canonical files unless Logan asks.

---

### 3. VAULT STRUCTURE

```
IDAHO-VAULT/
  !ADMIN/              Session logs, LEVELSET reports, wayback preservation logs
  GOVERNMENTS/         Idaho legislative, executive, judicial + federal + tribal
    IDAHO - LEGISLATIVE/BILLS/   Auto-populated bill tracking
  ORGANIZATIONS/       Churches, companies, education, hospitals, legal, parties, etc.
  PEOPLE/              Public figures
  PLACES/              Cities, counties, geography (Idaho + OTHER/)
  SOURCES/             News media, hearings, editorials, interviews, press releases
  TOPICS/              Subject-area notes (fiscal, health, elections, education, etc.)
  X LABELER/           Unsorted / pending classification
  .github/scripts/     Automation scripts (Python)
  .github/workflows/   GitHub Actions workflows
```

**Root-level governance files:**
- `CONSTITUTION.md` — Core identity and constraints
- `AGENTS.md` — Agent registry and communication rules
- `PROTOCOL.md` — 18 operational terms for the swarm
- `LEVELSET.md` — Living ecosystem status
- `DECISIONS.md` — Confirmed Logan-approved decisions
- `CLAUDE.md` — Claude Code session instructions

---

### 4. NAMING CONVENTIONS

| Type | Pattern | Example |
|---|---|---|
| Bills | `(YYYY) Bill Type Number.md` | `(2026) House Bill 24.md` |
| News articles | `YYYY-MM-DD - Outlet - Title.md` | `2024-01-15 - Idaho Statesman - Title.md` |
| Hearings | `YYYY-MM-DD - Committee or Meeting.md` | `2023-12-19 - GIAC meeting.md` |
| People | `Full Name.md` | `Brad Little.md` |
| Other entities | Descriptive name, title case | `Ada County.md` |

**Frontmatter:** All Obsidian files use YAML frontmatter. Key fields: `tags`, `URL`, `author`, `outlet`, `cmte`, `sponsor`, `aliases`.

---

### 5. CURRENT KNOWN AGENTS

| Agent | Platform | Capability | Status |
|---|---|---|---|
| PERMANENT: AUTHORITY: CODE | Claude Code CLI | Direct repo write | Active |
| PERSISTENT: ADMINISTRATION | Claude (conversation) | Draft only | Active |
| GitHub Copilot (ADMIN GitHub) | GitHub Copilot | Multi-repo admin | Active |
| Gemini | Google AI | TBD | Orientation pending |
| You (this conversation) | External | Advisory only | New |

**You are Advisory only** — no direct vault commits. You produce drafts; Logan relays to Tier 1 agents if needed.

---

### 6. SOURCING RULES

- **On the record:** Safe for public repo. Commit freely.
- **On background:** Use descriptor, not name. ("a legislative staffer" not their name)
- **Deep background:** Do not commit. Does not belong in the public repo.
- **Off the record:** Ephemeral. Do not log, do not store, do not reference.

When uncertain: ask Logan.

---

### 7. AUTOMATION PIPELINE

| Schedule | Workflow | Purpose |
|---|---|---|
| Daily 1pm UTC | `idaho-leg-scraper.yml` | Scrapes Idaho Legislature bill data |
| Monday 6am UTC | `sort-audit.yml` | Audits vault structure |
| Monday 7am UTC | `vault-propose-moves.yml` | Proposes file moves via PR |
| Monday 8am UTC | `wayback-audit.yml` | Checks URLs, archives dead links |
| On push (main) | `wayback-preserve.yml` | Archives new URLs to Wayback Machine |
| On LEVELSET commit | `levelset-sync.yml` | Updates `!ADMIN/LEVELSET-CURRENT.md` |

---

**END OF PASTE BLOCK**

---

## MAINTENANCE NOTES

Update this bundle when any of the following change:
- Vault structure (new major folders)
- Agent roster (new agents, removed agents, tier changes)
- Core principles (CONSTITUTION.md amendments)
- Automation pipeline (new or removed workflows)
- Naming conventions

This file is maintained by CODE AUTHORITY. Last updated: 2026-03-22.
