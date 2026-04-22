---
title: VAULT-TEMPLATES — Document Class and Template System
created: 2026-03-25
updated: 2026-04-01
status: draft
authority: LOGAN
authors:
  - ChatGPT Codex
source: issue/LAF-9
related:
  - '2026-03-25'
  - '2026-04-01'
  - CONSTITUTION
  - ChatGPT
  - DAILY NOTE
  - DAILY NOTE TEMPLATE
  - DECISIONS
  - FLAG
  - GitHub
  - Home
  - ISO
  - LAF
  - LOGAN
  - OBSIDIAN DAILY NOTE
  - Obsidian
  - PROTOCOL
  - VAULT-METADATA-STANDARD
  - VAULT-ZONES
  - 'Yes'
  - canon
  - doctrine
  - infrastructure
  - links
  - meeting
  - template
date created: Wednesday, April 1st 2026, 11:16:49 pm
date modified: Monday, April 6th 2026, 4:30:52 pm
---

# VAULT-TEMPLATES — Document Class and Template System

This file defines the canonical template system for IDAHO-VAULT. Its purpose is to eliminate ambiguity in document routing, naming, and maintenance.

---

## 1) Document Class Registry

| Class | Purpose | Required Filename Pattern | Canonical Home | Template Required |
| ----- | ------- | ------------------------- | -------------- | ----------------- |
| `news_media` | Capture reported stories and source excerpts | `YYYY-MM-DD - Outlet - Title.md` | repo root | Yes |
| `hearing_note` | Committee/hearing/live-meeting notes | `YYYY-MM-DD - Committee or Meeting.md` | repo root | Yes |
| `bill` | Legislative bill tracking and links | `(YYYY) Bill Type Number.md` | repo root | Yes |
| `person` | Public figure profile/reference note | `Full Name.md` | repo root | Yes |
| `organization` | Institution/entity profile note | `Organization Name.md` | repo root | Yes |
| `place` | Place/civic geography profile note | `Place Name.md` | repo root | Yes |
| `topic` | Thematic research hub | `Topic Name.md` | repo root | Yes |
| `interview` | Interview source notes | `Interview YYYY-MM-DD Name.md` | repo root | Yes |
| `press_release` | Publisher-issued press release source | `YYYY-MM-DD - Organization - Title.md` | repo root | Yes |
| `daily_log` | Daily rolling notes and backlog triage | `YYYY-MM-DD.md` | repo root | Optional |
| `misc_reference` | Catch-all reference content pending reclass | Descriptive title | repo root | No (transitional only) |

**Rule:** New recurring content types must be added to this table before they are treated as first-class classes.

**Routing clarification:** In the live vault, note classes route to repo root unless Logan explicitly establishes a different infrastructure zone. Taxonomy is carried by filename, metadata, and `wikilinks`, not by deep category folders. Older folder-tree examples are historical context, not standing move instructions.

---

## 2) Template Inventory (Canonical IDs)

Templates are identified by stable IDs independent of filename.

| Template ID | Applies to Class | Priority |
| ----------- | ---------------- | -------- |
| `tpl-news-media-v1` | `news_media` | Required |
| `tpl-hearing-note-v1` | `hearing_note` | Required |
| `tpl-bill-v1` | `bill` | Required |
| `tpl-person-v1` | `person` | Required |
| `tpl-organization-v1` | `organization` | Required |
| `tpl-place-v1` | `place` | Required |
| `tpl-topic-v1` | `topic` | Required |
| `tpl-interview-v1` | `interview` | Required |
| `tpl-press-release-v1` | `press_release` | Required |
| `tpl-daily-log-v1` | `daily_log` | Optional |

---

## 2.1) Live Daily Note Infrastructure

The `daily_log` class is currently implemented through the live root template and automation stack rather than by a full registry-field retrofit on every existing daily note instance.

- Active creation template: `DAILY NOTE TEMPLATE.md`
- Active Obsidian wiring: `.obsidian/daily-notes.json`
- Active automation canon: `.github/scripts/daily_rollover.py`, `.github/scripts/tidy_daily_notes.py`, `.github/scripts/expand_date_aliases.py`
- During this repair lane, existing daily notes do not need `doc_class`, `template_id`, or `template_version` retrofitted.

Legacy root files `DAILY NOTE.md` and `OBSIDIAN DAILY NOTE.md` are archival backlink targets, not active daily-note infrastructure.

---

## 3) Standard Template Structure

Each required template follows this section order:

1. **YAML frontmatter**
2. **Summary block** (2-4 sentences)
3. **Key facts / timeline**
4. **Linked entities** (`wikilinks`)
5. **Sources / URLs**
6. **Open questions / follow-ups**

### 3.1 Required Frontmatter Keys (all required templates)

```yaml
title: "<document title>"
doc_class: <class id>
template_id: <template id>
template_version: v1
status: draft
updated: YYYY-MM-DD
tags: []
```

These template keys define the note instance. Governance and operational notes must also satisfy the baseline metadata rules in `!/VAULT-METADATA-STANDARD.md`.

### 3.2 Class-Specific Required Keys

| Class | Required Additional Keys |
| ----- | ------------------------ |
| `news_media` | `author`, `outlet`, `url`, `published` |
| `hearing_note` | `cmte`, `meeting_date`, `location` |
| `bill` | `bill_number`, `session_year`, `bill_type`, `url` |
| `person` | `role`, `affiliation`, `residence` |
| `organization` | `org_type`, `jurisdiction`, `url` |
| `place` | `place_type`, `jurisdiction` |
| `topic` | `scope`, `related_topics` |
| `interview` | `interview_date`, `subject`, `interviewer` |
| `press_release` | `issuer`, `published`, `url` |

---

## 4) Naming Rules

1. Filename rules are class-bound and deterministic (see registry).
2. Do not append `(2)` or ad-hoc suffixes to canonical notes. Resolve duplication by merge/redirect.
3. Keep title case for entity names; preserve legal punctuation (apostrophes, hyphens).
4. Date-leading source files use ISO dates (`YYYY-MM-DD`) in local event date, not publish scrape date.
5. If class is unknown at creation time, stage in place with `doc_class: misc_reference`, then reclassify.

---

## 5) Routing and Maintenance Rules

1. **Create:** select class first, then instantiate matching template.
2. **Validate:** check filename pattern and required frontmatter keys.
3. **Route:** keep note-corpus files in repo root unless Logan explicitly directs a move into a dedicated system or infrastructure path.
4. **Link:** add at least three meaningful `wikilinks` for graph integrity.
5. **Review:** if content fails class validation, keep it in place until corrected.

Routing in this vault is conservative. Rename and normalize first; folder moves are exceptional.

---

## 5.1) Legacy Template Artifacts

The following files are retained for historical context or backlink preservation unless Logan explicitly directs otherwise:

- `DAILY NOTE.md` — archived legacy artifact, not active infrastructure
- `OBSIDIAN DAILY NOTE.md` — archived legacy artifact, not active infrastructure
- `template.md` — legacy backlink target; removable only after link cleanup or replacement

---

## 6) Constitutional Framework Interaction

This system is subordinate to constitutional governance:

- `CONSTITUTION.md` defines authority and constraints; templates cannot override it.
- `VAULT-ZONES.md` controls who can write where. Template compliance does not grant write access.
- `PROTOCOL.md` controls operational terms (HANDOFF, FLAG, etc.) when template/routing conflicts appear.
- `DECISIONS.md` records Logan-approved changes to classes or naming standards.
- GitHub workflows, `manifest.json`, and related transport state are execution infrastructure only. They may coordinate writes but do not define note classes or override vault doctrine.

**Change control:**

- Major template schema changes (new required keys, class renames, path remaps) require a tracked decision entry.
- Minor non-breaking edits (clarifications, examples) can ship as regular governance PR updates.

---

## 7) Minimum Compliance Checklist

- [ ] `doc_class` present and valid
- [ ] `template_id` + `template_version` present
- [ ] Filename matches class pattern
- [ ] File routed to correct class home
- [ ] Required class-specific fields present
- [ ] Contains actionable linked entities and source references

---

## DOCUMENT METADATA

- **Created:** 2026-03-25
- **Last Updated:** 2026-04-01
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** ChatGPT Codex
- **Change Note:** Rebased template policy onto the root-flat vault layout and clarified the daily-note and transport-boundary implementation rules.
