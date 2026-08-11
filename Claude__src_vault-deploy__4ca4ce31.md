---
tags:
  - administration/claude
  - administration/working-memory
updated: 2026-03-11
---
Claude's foundational working memory for the IDAHO-VAULT project. For user profile, see [[Logan]].

---

## Identity & Constraints

- Claude is Anthropic's AI assistant, currently Claude Sonnet 4.6
- Claude has no persistent memory between sessions by default; this document and Anthropic's memory system are the primary continuity mechanisms
- Claude cannot write directly to GitHub from its sandbox — outbound network is blocked by Anthropic policy; all pushes route through Logan's machine via `vault_push.py` or GitHub's web editor
- All Claude-generated vault content is flagged `source: commit` for human verification
- Human verification is required before any AI-generated content is treated as authoritative

---

## Working Relationship

- Logan wants straight talk, no flattery, no sycophancy — rational advisor posture only
- Logan has final say on all vault decisions; Claude proposes, Logan approves
- Git diffs are the verification mechanism: Logan reviews changes in GitHub Desktop or the web interface before merging
- Start small, validate, then scale — this was established as the process discipline in the first session

---

## Vault: IDAHO-VAULT

**Repo:** https://github.com/loganfinney27/IDAHO-VAULT (public)  
**Local path:** `C:\Users\loganf\Documents\IDAHO-VAULT`  
**Tool:** Obsidian.md

### Core Conventions

**Frontmatter (SOURCES example):**
```yaml
---
author:
  - "[[Author Name]]"
outlet:
  - "[[Outlet Name]]"
URL: https://...
wayback: https://web.archive.org/web/[timestamp]/[url]  # if URL is dead
tags:
  - media/articles
  - 2024/01/02
source: commit  # flag for AI-generated stub content; remove after human verification
---
```

**Note structure:**
1. First line after frontmatter: 5–50 word summary sentence with wikilinks
2. Body: annotated content, heavily wikilinked
3. Pipe aliases for natural reading: `[[pornography|porn]]`, `[[State of Idaho|Idaho]]`
4. Orphan wikilinks (references to non-existent notes) are intentional — they serve as prompts to create the target note eventually; do not flatten to plain text
5. When a note is renamed, Obsidian natively updates all related wikilinks including pipe aliases — rely on this, don't manually hunt references
6. No `date-modified` in frontmatter — Git handles version tracking
7. `source: commit` = AI-generated content awaiting verification; blank note with correct frontmatter is better than vague filler
8. **Future (Stage 3+):** Body text PRs should include wikilink recommendations via fuzzy matching against existing vault entries — recurring names, phrases, characters, and themes across the database

**Naming conventions:**
- NEWS MEDIA: `YYYY-MM-DD - Outlet - Title.md`
- HEARINGS: dated files in year subfolders
- EDITORIALS, PODCASTS, PRESS RELEASES, RESOLUTIONS: date prefixes are intentional — not misplaced

---

## Pipeline: GitHub Actions

All automation runs in `.github/` and commits reports to `!ADMINISTRATION/`.

### Scheduled Workflows (Mondays UTC)

| Time | Workflow | Script | Output |
|---|---|---|---|
| 6am | Sort Audit | `sort_audit.py` | `sort-audit-YYYY-MM-DD.md` |
| 7am | Propose Moves | `propose_moves.py` | PR with `git mv` commands |
| 8am | Wayback Audit | `wayback_audit.py` | `wayback-audit-YYYY-MM-DD.md`, `wayback-patches-YYYY-MM-DD.md` |

### Event Workflows

| Trigger | Workflow | Purpose |
|---|---|---|
| Push to main (SOURCES, GOVERNMENTS, TOPICS) | Wayback Preserve | Submit new URLs to Save Page Now |

### Local Tooling

**`vault_push.py`** — pushes local files to GitHub via API (workaround for sandbox network block)
```bash
python vault_push.py <local_file> <repo_path> [-m "message"]
# e.g.:
python vault_push.py sort_audit.py .github/scripts/sort_audit.py
```
Config: `.env` file with `VAULT_TOKEN=...` and `VAULT_REPO=loganfinney27/IDAHO-VAULT`

---

## Sort Audit: Known False Positives

The v2 sort audit script suppresses these known false positives:

- **SOURCES/EDITORIALS, PODCASTS, PRESS RELEASES, RESOLUTIONS, REPORTS, INTERVIEWS, HEARINGS** — dated files here are correctly placed; not news articles
- **PLACES/OTHER/COUNTIES** — out-of-state counties; not Idaho counties
- **TOPICS (root and subfolders), ORGANIZATIONS, GOVERNMENTS/IDAHO - EXECUTIVE, etc.** — intentionally flat; orphan warnings suppressed via `FLAT_OK` set

**Genuine issues flagged from v1 audit (2026-03-12), not yet actioned:**
- `TOPICS/Kaiser Family Foundation.md` → `ORGANIZATIONS`
- `PLACES/Europe.md`, `PLACES/State of Idaho.md`, `PLACES/United States of America.md`, `PLACES/Malheur National Wildlife Refuge.md` → need homes under PLACES subfolders
- `GOVERNMENTS/Board of Professional Counselors and Marriage and Family Therapists.md` → `GOVERNMENTS/IDAHO - EXECUTIVE`
- `SOURCES/NEWS MEDIA/2020-01-22,24,30 - McClure -` entries → possibly `SOURCES/HEARINGS`
- `SOURCES/NEWS MEDIA/2023 Idaho Statesman & ProPublica - Idaho's crumbling schools.md` → rename to match `YYYY-MM-DD - Outlet - Title.md` pattern

---

## Wayback Machine Integration

**Purpose:** Dead link rescue + proactive preservation of new URLs

**`wayback: [url]` frontmatter field** — added to notes where live URL is dead; points to best Wayback snapshot

**Known limitations:**
- SPN (Save Page Now) fails for paywalled content, government sites blocking bots, authenticated pages
- CDX API has rate limits; audit paces at 1 req/sec
- Wayback audit should be run with `--limit 20` first to validate behavior before full vault scan

---

## Vault Processing: Planned Order

| Priority | Folder | Rationale |
|---|---|---|
| 1 | PLACES (CITIES, COUNTIES, COMMUNITIES) | Similar to GEOGRAPHY pilot; mostly stubs |
| 2 | GOVERNMENTS | Structured, predictable |
| 3 | ORGANIZATIONS | Moderate complexity |
| 4 | PEOPLE | Sensitive; careful handling |
| 5 | TOPICS | Richest notes; lightest touch |
| 6 | SOURCES | Mainly consistency cleanup |

**Process per folder:** Sort pass → Frontmatter pass → Body text pass

**GEOGRAPHY folder:** Completed March 2026. Delivered as `GEOGRAPHY_edited.zip`. One flagged item: Palisades dam operator (Bureau of Reclamation) — verify.

---

## APIs Under Investigation

| API | Status | Vault Use Case |
|---|---|---|
| Wayback Machine (CDX + SPN) | Integrated | Dead link rescue, URL preservation |
| CourtListener REST v4 | Researched | Idaho federal court cases, judge bios, active case monitoring via webhooks |
| Anthropic API | Planned (Stage 3+) | AI-powered stub generation, wikilink suggestion, frontmatter enrichment |

**CourtListener notes:**
- Idaho state court coverage is spottier than federal
- Idaho federal district court ID: `id`
- Webhook/alert system can push new docket entries to a GitHub Actions dispatch trigger
- MCP server for AI assistants is in development — worth watching

---

## Pending Items

- [ ] Push updated `sort_audit.py` (v2) via `vault_push.py`
- [ ] Re-run sort audit to get cleaner v2 report
- [ ] Action genuine sort issues from v1 report (see above)
- [ ] Run Wayback audit with `--limit 20` to validate before full scan
- [ ] Begin PLACES/COUNTIES sort pass
- [ ] Evaluate CourtListener coverage for Idaho `id` district before committing to pipeline integration
- [ ] Stage 3: add `ANTHROPIC_API_KEY` to GitHub Actions secrets when ready for AI enrichment
