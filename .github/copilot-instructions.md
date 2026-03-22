# GitHub Copilot Instructions — IDAHO-VAULT

This file is loaded automatically by GitHub Copilot when working in this repository. It is aligned with `CLAUDE.md` (repo root), which is the single-source-of-truth for all AI agents in this vault.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)
**Platform:** Obsidian.md vault, version-controlled with git

---

## Role

Logan directs; Copilot assists. Logan is the sole human in this system. All AI tools — Copilot, Claude, Gemini — are software. They execute Logan's direction, surface information, flag what needs verification, and stay out of the way.

---

## Vault Purpose

This is a personal journalism research vault. It contains notes on Idaho politics, government, legislation, people, organizations, and source documents. All committed content is **on the record** and should be treated as **publishable**.

---

## Vault Structure

```
IDAHO-VAULT/
  !/!                     Infrastructure, LEVELSET files, audit reports (canonical governance dir)
  ATTACHMENTS/
    DOCUMENTS/            PDFs, images
    MAPS/                 Map files
    TEMPLATES/            Obsidian templates (Article, Hearing, OP-ED, Press Release)
  GOVERNMENTS/
    IDAHO - EXECUTIVE/    Governor, departments, commissions, health districts
    IDAHO - JUDICIAL/     Courts, judicial districts
    IDAHO - LEGISLATIVE/
      BILLS/              Named: (YYYY) Bill Type Number.md
      DISTRICTS/          Legislative districts
      IDAHO HOUSE/        House members, committees
      IDAHO SENATE/       Senate members, committees
      JOINT COMMITTEES/   Joint legislative committees
      SESSIONS/           Session notes by year
    USA - FEDERAL/        Federal entities, legislation, census
    USA - TRIBES/         Tribal governments
  ORGANIZATIONS/          Churches, companies, education, hospitals, legal, parties, politics, publications, unions
  PEOPLE/                 Individual people (public figures)
  PLACES/                 Cities, counties, schools, geography, regions, roads, taxing districts
    OTHER/                Non-Idaho places (out-of-state cities, counties, countries, states)
  SOURCES/
    EDITORIALS/           Opinion pieces
    HEARINGS/             Meeting/hearing notes, organized by year
    INTERVIEWS/           Interview notes
    LISTS/                Reference lists
    NEWS MEDIA/           News articles. Named: YYYY-MM-DD - Outlet - Title.md
    PODCASTS/             Podcast notes
    PRESS RELEASES/       Press releases
    RESOLUTIONS/          Resolutions
  TOPICS/                 Subject areas (agriculture, economy, education, elections, fiscal, health, legal, etc.)
  X LABELER/              Unsorted files pending classification
  .github/scripts/        Automation scripts (Python)
  .github/workflows/      GitHub Actions workflows
```

---

## Naming Conventions

| Type | Pattern | Example |
|---|---|---|
| Bills | `(YYYY) Bill Type Number.md` | `(2026) House Bill 24.md` |
| News articles | `YYYY-MM-DD - Outlet - Title.md` | `2024-01-15 - Idaho Statesman - Title here.md` |
| Hearings | `YYYY-MM-DD - Committee or Meeting.md` | `2023-12-19 - GIAC meeting.md` |
| People | `Full Name.md` | `Brad Little.md` |
| Other entities | Descriptive name, title case | `Ada County.md` |

---

## Frontmatter Conventions

All Obsidian files use YAML frontmatter.

**People:**
```yaml
tags:
  - Party/Republican          # or Party/Democratic
  - people/elected/legislative
residence: "[[Boise]]"
```

**News articles:**
```yaml
author: "[[Reporter Name]]"
outlet: "[[Outlet Name]]"
URL: https://...
tags:
  - media/articles
  - YYYY/MM/DD
```

**Bills:**
```yaml
tags:
  - bills
  - YYYY/session
aliases:
  - HB 24
cmte: ["[[Committee Name]]"]
sponsor: ["[[Sponsor Name]]"]
URL: https://legislature.idaho.gov/...
```

**Hearings:**
```yaml
cmte: "[[Committee Name]]"
tags:
  - YYYY/MM/DD
```

---

## Wikilinks

Use `[[Full Name]]` for all internal links — people, places, organizations, bills, topics. This is how Obsidian builds the knowledge graph. Link densely in source documents.

---

## File Types

- **Markdown** = human product, attributable to Logan. Notes, stories, analysis.
- **Python** = machine/procedural product, attributable to AI agents. Scripts, scrapers, automation.
- **Administrative** = vault infrastructure. Instruction files, LEVELSET files, audit reports.

---

## Code Conventions (Python)

- Python scripts live in `.github/scripts/`
- GitHub Actions workflows live in `.github/workflows/`
- Scripts that commit to the repo use `git config user.name "github-actions[bot]"` and `git config user.email "github-actions[bot]@users.noreply.github.com"`
- Automation output (reports) is committed to `!/!` with date-stamped filenames
- Dependencies are tracked in `.github/scripts/requirements-scraper.txt`

---


## Automation Scripts

| Script | Purpose | Trigger |
|---|---|---|
| `sort_audit.py` | Audits vault structure for misplaced files | Manual (workflow_dispatch) |
| `idaho_leg_scraper.py` | Scrapes Idaho Legislature bill data | Daily 6 AM MT + manual |
| `post_digest.py` | Posts bill activity to GitHub Issues digest | Called by scraper workflow |
| `propose_moves.py` | Proposes vault file reorganization | Weekly Monday 7 AM UTC + manual |
| `wayback_audit.py` | Audits URL preservation in Wayback Machine | Weekly Monday 8 AM UTC + manual |

---

## Sourcing Protocol

- **On the record:** Safe for public repo. All committed content is on the record.
- **On background:** Vault-safe but identity-protected. Use carefully — this is a public repo.
- **Off the record:** Ephemeral. Do not log, do not store, do not commit. If Logan says something is off the record, it must not appear in files, code, comments, or commit messages.

When uncertain about sourcing category, **ask Logan**.

---

## Git Practices

- Branch naming:
  - `claude/description-sessionId` for Claude Code branches
  - `copilot/description` for GitHub Copilot branches
  - `gemini/description` for Gemini agent branches
- Commit messages: Clear, descriptive, explain the "why"
- Never force-push without explicit permission
- Check in before anything irreversible
- The legislature scraper workflow commits directly to main for automated bill updates

---

## Guiding Principles

- The five W's: who, what, when, where, why
- The four C's: collect, capture, catalogue, collate
- Public repo = on the record
- Markdown for human product. Python for machine/procedural product.
- Do not over-engineer. Keep it simple. Only build what's needed now.
- Check in before anything irreversible.

---

## Multi-Agent Ecosystem

This vault uses multiple AI tools. All agents share the same vault conventions. See also:
- `CLAUDE.md` — Instructions for Claude Code (Anthropic)
- `GEMINI.md` — Instructions for Gemini code agents (Google)
- `.github/copilot-instructions.md` — This file (GitHub Copilot)
- `!/!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` — Paste-to-agent LEVELSET prompt for chat agents without repo access
