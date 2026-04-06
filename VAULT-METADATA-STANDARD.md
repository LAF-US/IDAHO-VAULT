---
title: VAULT-METADATA-STANDARD — Header and Footer Standard
created: 2026-03-25
updated: 2026-04-01
status: active
authority: LOGAN
authors:
- ChatGPT Codex
source: issue/LAF-13
related:
- '2026-03-20'
- '2026-03-25'
- '2026-04-01'
- CLI
- ChatGPT
- ISO
- LAF
- LOGAN
- Obsidian
- SSZ
- UTC
- VAULT-TEMPLATES
- chain
- doctrine
- humans
- index
- template
---
# VAULT-METADATA-STANDARD — Header and Footer Standard

This standard defines the metadata contract for markdown files in IDAHO-VAULT so humans and agents produce consistent, durable records.

---

## 1) Scope and Purpose

Use this standard for all new or substantially edited markdown files in the vault, especially governance files, handoffs, source notes, and operational records.

Goals:

- Improve machine readability (automation, sorting, auditability)
- Preserve human readability (quick context at top, clear close at bottom)
- Keep metadata factual while leaving interpretation in prose

### Authority Precedence

When metadata guidance overlaps with template docs or implementation tooling, this file wins for governed markdown notes.

- `!/VAULT-TEMPLATES.md` may add note-class fields and naming rules, but it does not override baseline header/footer or lifecycle policy.
- `.obsidian/` configuration, `.github/` workflows, and `manifest.json` may implement metadata behavior, but they are not the canonical metadata authority.

---

## 2) Header Standard (YAML Frontmatter)

Every governed note begins with YAML frontmatter fenced by `---` lines.

```yaml
---
title: "<document title>"
updated: YYYY-MM-DD
status: <draft|active|superseded|archived>
authority: "<who has decision authority>"
---
```

### Required Header Fields

| Field | Type | Rule | Example |
|---|---|---|---|
| `title` | string | Exact document title in plain text | `"VAULT-METADATA-STANDARD — Header and Footer Standard"` |
| `updated` | date | Last substantive edit date, `YYYY-MM-DD` | `2026-03-25` |
| `status` | enum | One of: `draft`, `active`, `superseded`, `archived` | `active` |
| `authority` | string | Final decision authority for this document | `"LOGAN"` |

### Optional Header Fields

Use only when useful; avoid metadata bloat.

| Field | Type | Use |
|---|---|---|
| `created` | date | Original creation date if different from `updated` |
| `authors` | list[string] | Multiple contributors |
| `source` | string or list[string] | Provenance (`interview`, `commit`, `issue`, URL, etc.) |
| `tags` | list[string] | Obsidian grouping/search |
| `aliases` | list[string] | Alternate titles/names |
| `zone` | enum/string | Governance zone (`constitutional`, `operational`, `data`) |
| `supersedes` | string/list | Pointer to replaced doc(s) |
| `superseded_by` | string | Pointer to replacing doc |
| `review_due` | date | Planned reassessment date |
| `related` | list[string] | Closely linked notes/issues |

---

## 3) Footer / Closing Convention

Use a `## DOCUMENT METADATA` section at the end of the note for a human-readable closeout.

Required footer fields:

- **Created:** `YYYY-MM-DD` (or `Unknown` for legacy notes)
- **Last Updated:** `YYYY-MM-DD`
- **Status:** same value as header status
- **Authority:** same value as header authority

Recommended optional footer fields:

- **Authors:** one or more authors/agents
- **Change Note:** one-line summary of latest substantive change
- **Supersedes / Superseded By:** lineage to related standards

The footer should mirror key lifecycle fields from frontmatter for readers who scan in rendered view and for legacy files that may not have complete YAML.

---

## 4) Timestamp Rules

- Date-only fields use `YYYY-MM-DD`.
- Datetime fields (if needed) use UTC ISO-8601 with `Z` suffix: `YYYY-MM-DDTHH:MM:SSZ`.
- `updated` must be changed whenever meaning, policy, or factual claims materially change.
- Minor typo fixes may keep existing `updated` value unless clarity/meaning changed.

---

## 5) Authorship Rules

- Use `authors` (list) when more than one contributor materially shaped the document.
- If a single contributor, `author` or `authors` with one entry is acceptable; prefer `authors` for consistency.
- Agent names should be explicit (`ChatGPT Codex`, `Claude Code CLI`) and not imply decision authority.
- Human decision ownership belongs in `authority`, not `authors`.

---

## 6) Status Rules

- `draft`: in progress, not adopted
- `active`: currently in force
- `superseded`: replaced by a newer source of truth
- `archived`: retained for history; no further expected updates

Transition requirements:

- When a file becomes `superseded`, populate `superseded_by`.
- New replacement docs should include `supersedes`.
- Do not delete superseded governance docs; preserve historical chain.

---

## 7) Authority Rules

- `authority` identifies who has final say over acceptance and interpretation.
- In this vault, governance documents default to `LOGAN` unless explicitly delegated.
- Agents may draft and revise text but must not claim final authority unless directed.

---

## 8) Metadata vs Prose (Decision Rule)

Put information in metadata when it is:

- Structural (status, dates, authorship, lineage)
- Stable enough to be queried/sorted
- Reused across workflows or automation

Put information in prose when it is:

- Explanatory (reasoning, context, interpretation)
- Narrative (background, analysis, notes)
- Ambiguous or nuanced beyond clean key-value structure

If a value needs interpretation to be understood, keep the canonical detail in prose and store only the minimal index value in metadata.

---

## 9) Minimal Compliant Example

```yaml
---
title: "Example Governance Note"
created: 2026-03-20
updated: 2026-03-25
status: active
authority: "LOGAN"
authors:
  - ChatGPT Codex
tags:
  - administration/standards
---
```

### Example Footer

- **Created:** 2026-03-20
- **Last Updated:** 2026-04-01
- **Status:** Active
- **Authority:** LOGAN
- **Authors:** ChatGPT Codex
- **Change Note:** Established baseline metadata schema and lifecycle rules.

---

## DOCUMENT METADATA

- **Created:** 2026-03-25
- **Last Updated:** 2026-03-25
- **Status:** Active
- **Authority:** LOGAN
- **Authors:** ChatGPT Codex
- **Change Note:** Clarified that metadata doctrine outranks template guidance and implementation tooling when rules overlap.
