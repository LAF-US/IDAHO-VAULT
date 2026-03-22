# LEVELSET v1 — IDAHO-VAULT

**Date:** 2026-03-16
**Author:** Claude (at Logan Finney's direction)
**Purpose:** First formal LEVELSET checkpoint. Establishes baseline vault state for context injection.

---

## Vault State

| Directory | Markdown Files | Purpose |
|---|---|---|
| !ADMINISTRATION/ | 15 | Infrastructure, audits, LEVELSET files |
| ATTACHMENTS/ | 4 | Templates (Article, Hearing, OP-ED, Press Release) |
| GOVERNMENTS/ | 392 | Executive, legislative, judicial, federal, tribal |
| ORGANIZATIONS/ | 241 | Churches, companies, education, hospitals, parties, etc. |
| PEOPLE/ | 503 | Public figures |
| PLACES/ | 1,091 | Cities, counties, schools, geography, regions |
| SOURCES/ | 168 | News articles, hearings, interviews, press releases |
| TOPICS/ | 430 | Subject areas (agriculture, economy, education, etc.) |
| X LABELER/ | 134 | Unsorted files pending classification |
| **Total** | **~2,978** | |

## Automation

| Script | File | Status |
|---|---|---|
| Legislature scraper | `idaho_leg_scraper.py` | Active — daily 6 AM MT |
| Bill digest poster | `post_digest.py` | Active — called by scraper |
| Sort audit | `sort_audit.py` | Active — manual dispatch |
| Propose moves | `propose_moves.py` | Active |
| Wayback audit | `wayback_audit.py` | Active |

| Workflow | File | Status |
|---|---|---|
| `idaho-leg-scraper.yml` | Legislature scraper + digest | Active |
| `sort-audit.yml` | Vault sort audit | Active |
| `vault-propose-moves.yml` | File move proposals | Active |
| `wayback-audit.yml` | Wayback Machine audit | Active |
| `wayback-preserve.yml` | Wayback preservation | Active |

## Infrastructure

- **CLAUDE.md** — Single source of truth for Claude operations. Loaded automatically.
- **`.claude/settings.json`** — SessionStart hook for context injection on promptless awakening.
- **`!ADMINISTRATION/DECISIONS.md`** — Architectural decision log.
- **`.gitignore`** — Excludes Python artifacts, IDE files, OS files, `.env`, `*.vault.json`.

## Key Conventions

- All committed content is **on the record** and **publishable**.
- Markdown = human product (Logan). Python = machine product (Claude).
- Wikilinks (`[[Full Name]]`) for all internal references.
- Branch naming: `claude/description-sessionId`.

## Context Injection

As of this LEVELSET, the vault now includes a `.claude/settings.json` SessionStart hook. On any Claude Code session start — including promptless agent awakenings — the hook injects:

1. Current date and branch
2. Pointer to this LEVELSET file
3. Pointer to CLAUDE.md and DECISIONS.md
4. Owner identity and sourcing reminder

This ensures no Claude agent operates in a contextless state within this vault.

---

*This file is permanent. It is never deleted, never overwritten. Future LEVELSETs are additive.*
