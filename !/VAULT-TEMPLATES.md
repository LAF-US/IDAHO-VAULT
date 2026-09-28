---
tags:
  - administration/templates
updated: 2026-03-25
status: draft
source: commit
---

# VAULT-TEMPLATES — Document Class and Template System

This file defines the canonical template system for IDAHO-VAULT. Its purpose is to eliminate ambiguity in document routing, naming, and maintenance.

---

## 1) Document Class Registry

| Class | Purpose | Required Filename Pattern | Canonical Home | Template Required |
| ----- | ------- | ------------------------- | -------------- | ----------------- |
| `news_media` | Capture reported stories and source excerpts | `YYYY-MM-DD - Outlet - Title.md` | `SOURCES/NEWS MEDIA/` | Yes |
| `hearing_note` | Committee/hearing/live-meeting notes | `YYYY-MM-DD - Committee or Meeting.md` | `SOURCES/HEARINGS/<YYYY>/` | Yes |
| `bill` | Legislative bill tracking and links | `(YYYY) Bill Type Number.md` | `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/` | Yes |
| `person` | Public figure profile/reference note | `Full Name.md` | `PEOPLE/` | Yes |
| `organization` | Institution/entity profile note | `Organization Name.md` | `ORGANIZATIONS/` | Yes |
| `place` | Place/civic geography profile note | `Place Name.md` | `PLACES/` | Yes |
| `topic` | Thematic research hub | `Topic Name.md` | `TOPICS/` | Yes |
| `interview` | Interview source notes | `Interview YYYY-MM-DD Name.md` | `SOURCES/INTERVIEWS/` | Yes |
| `press_release` | Publisher-issued press release source | `YYYY-MM-DD - Organization - Title.md` | `SOURCES/PRESS RELEASES/` | Yes |
| `daily_log` | Daily rolling notes and backlog triage | `YYYY-MM-DD.md` | vault root (or future `DAILY/`) | Optional |
| `misc_reference` | Catch-all reference content pending reclass | Descriptive title | `X LABELER/` or current location | No (transitional only) |

**Rule:** New recurring content types must be added to this table before they are treated as first-class classes.

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

## 3) Standard Template Structure

Each required template follows this section order:

1. **YAML frontmatter**
2. **Summary block** (2-4 sentences)
3. **Key facts / timeline**
4. **Linked entities** (`[[wikilinks]]`)
5. **Sources / URLs**
6. **Open questions / follow-ups**

### 3.1 Required Frontmatter Keys (all required templates)

```yaml
doc_class: <class id>
template_id: <template id>
template_version: v1
status: draft
updated: YYYY-MM-DD
tags: []
```

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
5. If class is unknown at creation time, stage in `X LABELER/` with `doc_class: misc_reference`, then reclassify.

---

## 5) Routing and Maintenance Rules

1. **Create:** select class first, then instantiate matching template.
2. **Validate:** check filename pattern and required frontmatter keys.
3. **Route:** move to canonical home path for that class.
4. **Link:** add at least three meaningful `[[wikilinks]]` for graph integrity.
5. **Review:** if content fails class validation, return to `X LABELER/` until corrected.

---

## 6) Constitutional Framework Interaction

This system is subordinate to constitutional governance:

- `CONSTITUTION.md` defines authority and constraints; templates cannot override it.
- `VAULT-ZONES.md` controls who can write where. Template compliance does not grant write access.
- `PROTOCOL.md` controls operational terms (HANDOFF, FLAG, etc.) when template/routing conflicts appear.
- `DECISIONS.md` records Logan-approved changes to classes or naming standards.

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
- **Author:** ChatGPT Codex (draft for Logan review)
- **Status:** Draft — awaiting [[LOGAN]]'s review
- **Authority:** [[LOGAN]]'s discretion
