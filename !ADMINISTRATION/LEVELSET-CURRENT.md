---
tags:
  - administration/levelset
  - administration/current-state
updated: 2026-03-16
auto-update: true
---
# LEVELSET — Current State

**Purpose:** Single-source-of-truth for cross-agent context unification. All Claude and GitHub Copilot instances should read this file on first contact to orient themselves before doing any work. This file is updated automatically by `levelset-sync.yml` when new LEVELSET reports are committed.

**Authoritative as of:** 2026-03-16
**Supersedes:** Individual LEVELSET report files for orientation purposes. Reports themselves remain permanent and are never deleted.

---

## VAULT IDENTITY

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repo:** github.com/loganfinney27/IDAHO-VAULT (public)
**Tool:** Obsidian.md — ~2,900 notes, version-controlled with git
**Purpose:** Personal journalism research vault. All committed content is on the record and publishable.

---

## AGENT ROSTER

All AI instances operating in this vault are infrastructure. No instance has standing or decision-making authority. Logan directs; Claude executes.

| Agent | Tier | Capabilities | Role | Status |
|---|---|---|---|---|
| PERMANENT: CODE AUTHORITY | 1 | Direct repo write access (Claude Code) | Architecture, bulk structural work, infrastructure commits | Active |
| PERSISTENT: ADMINISTRATION | 2 | Targeted push via `vault_push.py`, requires Logan approval | Constitutional layer, conventions, judgment calls | Active |
| STORY: JFAC Open Meetings | 1 | Direct repo access | Bulk vault work for JFAC story | Active |
| TASK: LEVELSET reports | 3 | Read/analysis only, no direct commits | LEVELSET synthesis (on hold) | On hold |
| PROJECT: 2026 Budget Tracker | Unknown | Unknown | Budget tracking | Unknown |
| GitHub Copilot (this agent) | 1 | Direct repo write via GitHub Actions | Code review, workflow fixes, automation | Active |

**Tiers:**
- **Tier 1** — Direct repo write access. Bulk structural work, mass commits, architectural changes.
- **Tier 2** — Targeted push via `vault_push.py`, requires Logan approval. Administrative files, pipeline scripts.
- **Tier 3** — Read/analysis only. No direct commits.

---

## CONSTITUTION & ETHICS

Every agent must read these files before operating:

- **`CLAUDE.md`** (repo root) — Vault structure, naming conventions, sourcing protocols, operating principles. This is the primary constitution for Claude Code sessions.
- **`!ADMINISTRATION/Claude.md`** — Working memory and extended context for PERSISTENT: ADMINISTRATION.
- **`!ADMINISTRATION/Ethics.md`** — Ethical framework: source protection, IPTV production policies, Idaho DHR conflict of interest, public repo obligations.

**Core principles** (non-negotiable):
1. Logan is human. Claude is software. Logan directs; Claude executes.
2. Public repo = on the record. All committed content is publishable.
3. Off-the-record material is ephemeral — never log, never store, never reference.
4. Everything produced by Claude is a draft until Logan verifies.
5. Be vigilant and wary of unreliable narrators — including Claude.

---

## INFRASTRUCTURE

### Automation Pipeline

| Schedule | Workflow | Script | Output |
|---|---|---|---|
| Daily 13:00 UTC | `idaho-leg-scraper.yml` | `idaho_leg_scraper.py` | Bill markdown files in `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/` |
| Monday 06:00 UTC | `sort-audit.yml` | `sort_audit.py` | `!ADMINISTRATION/sort-audit-YYYY-MM-DD.md` |
| Monday 07:00 UTC | `vault-propose-moves.yml` | `propose_moves.py` | PR with `git mv` commands |
| Monday 08:00 UTC | `wayback-audit.yml` | `wayback_audit.py` | `!ADMINISTRATION/wayback-audit-YYYY-MM-DD.md` |
| On push (main) | `wayback-preserve.yml` | (inline) | Submits new URLs to Wayback Machine |
| On LEVELSET commit | `levelset-sync.yml` | (inline) | Updates this file |

### Key Paths

```
CLAUDE.md                            ← root constitution for all agents
!ADMINISTRATION/                     ← vault infrastructure
  LEVELSET-CURRENT.md                ← this file (cross-agent context hub)
  Claude.md                          ← ADMINISTRATION working memory
  Ethics.md                          ← ethics framework
  DECISIONS.md                       ← permanent decision log
  LEVELSET-*.md                      ← individual LEVELSET reports (permanent)
.github/scripts/                     ← Python automation
.github/workflows/                   ← GitHub Actions
GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/  ← auto-populated bill tracking
```

---

## CURRENT STATE SNAPSHOT

**Last LEVELSET reports committed:**

*(Maintained automatically by `levelset-sync.yml` — do not edit this table manually.)*

| Report File | Date |
|---|---|
| `LEVELSET-GITHUB-COPILOT-2026-03-16.md` | 2026-03-16 |
| `LEVELSET-ADMIN-Github-2026-03-15.md` | 2026-03-15 |
| `LEVELSET-v2.md` | 2026-03-13 |

**Active PRs (as of 2026-03-16):**

| PR | Branch | Status | Purpose |
|---|---|---|---|
| #2 | `copilot/fix-token-permissions-and-error-handling` | Open | Scraper error handling + vault-propose-moves GH_TOKEN fix |
| #3 | `copilot/collaboration-context-unification` | Open (this PR) | Cross-swarm context unification |
| #4 | `copilot/consolidate-copilot-efforts` | Open | Multi-agent config files |
| #5 | `claude/public-conversation-setup-zl2oe` | Open | Public conversation setup |
| #6 | `claude/levelset-multi-conversation-zWxJc` | Open | LEVELSET multi-conversation |

---

## UNRESOLVED

| Item | Waiting On | Priority |
|---|---|---|
| Merge PRs #2, #3, #4, #5, #6 to main | Logan's review and approval | High |
| Idaho Legislature Scraper failures | Root cause: empty bill list from legislature.idaho.gov | High |
| Vault Propose Moves failures | GH_TOKEN not passed to `gh pr create` (fixed in PR #2) | High |
| `X LABELER/` unsorted files | Manual triage by Logan | Ongoing |
| Sort audit false positives (Malheur, Multnomah, Orange, Summit counties) | Code fix in `sort_audit.py` | Low |
| PLACES subfolders for misplaced files | Manual moves (flagged in Claude.md Pending Items) | Low |

---

## COLLISION RISKS

**Do not conflict with:**
- PR #2: `idaho_leg_scraper.py` and `vault-propose-moves.yml`
- PR #4: `.github/copilot-instructions.md`, `GEMINI.md`, `CLAUDE.md` updates
- PR #5/#6: `!ADMIN/` directory restructuring

**Note:** Multiple PRs are modifying governance files simultaneously. Logan must review for conflicts before merging.

---

## PROTOCOL REFERENCES

- **LEVELSET protocol:** `!ADMINISTRATION/LEVELSET-v3.2.6.1-PROMPT.md` (latest prompt version)
- **Conversation taxonomy:** PERMANENT / PERSISTENT / TASK / STORY / PROJECT / ISSUE / INQUIRY
- **File attribution:** Markdown = human product (Logan). Python = machine/procedural (Claude). Administrative = vault infrastructure.

---

*This file is auto-updated by `.github/workflows/levelset-sync.yml` when new LEVELSET reports are committed to `!ADMINISTRATION/`. Do not manually edit the "Current State Snapshot" section — it is maintained by automation. The rest of this file changes only via PR with Logan's approval.*
