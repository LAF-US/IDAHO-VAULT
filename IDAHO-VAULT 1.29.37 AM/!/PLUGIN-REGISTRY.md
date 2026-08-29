---
authority: LOGAN
status: AUTHORITATIVE — no agent enables, disables, installs, or removes plugins without updating this registry
updated: 2026-04-12
related:
  - PLUGIN-TRIAGE-UTF8
  - VAULT-CONVENTIONS
  - LEVELSET-CURRENT
  - AGENTS
  - Obsidian Sync
---

# PLUGIN REGISTRY — Authoritative Record

**Owner:** Logan Finney
**Last audited:** 2026-04-12 by Claude Code (The Abhorsen)
**Source of truth:** This file governs `.obsidian/community-plugins.json` and `.obsidian/plugins/`

---

## Governing Rule

**No agent may enable, disable, install, or remove any community plugin without:**
1. Updating this registry first (or simultaneously)
2. Recording the change in the Activity Log at the bottom of this file
3. Stating the rationale

Violations of this rule are a TRIPLEX boundary breach. Agents: if you're about to touch `.obsidian/plugins/` or `community-plugins.json`, read this file first.

---

## Summary (2026-04-12)

| Metric | Count | Size |
|---|---|---|
| Enabled | 26 | 128 MB |
| Dormant (configured) | 28 | 43 MB |
| **Total installed** | **54** | **171 MB** |
| Largest single plugin | mcp-tools | 117 MB (69% of total) |

---

## ENABLED — 26 Plugins

### Infrastructure / Agent Layer

| Plugin ID | Name | Version | Size | Depends On | Rationale |
|---|---|---|---|---|---|
| `obsidian-git` | Git | v2.38.0 | 732 KB | — | Git integration for vault version control |
| `obsidian-local-rest-api` | Local REST API | v3.5.0 | 2,530 KB | — | REST API server for MCP bridge; required by agent ecosystem |
| `mcp-tools` | MCP Tools | v0.2.27 | **117,479 KB** | `obsidian-local-rest-api` | MCP bridge connecting Claude Desktop to vault; semantic search, templates |
| `obsidian-linter` | Linter | v1.31.2 | 892 KB | — | Frontmatter formatting, YAML standardization on save |

### Navigation / Search

| Plugin ID | Name | Version | Size | Depends On | Rationale |
|---|---|---|---|---|---|
| `breadcrumbs` | Breadcrumbs | v4.4.4 | 892 KB | — | Keystone: navigates `related:` frontmatter links in zettelkasten |
| `omnisearch` | Omnisearch | v1.28.2 | 606 KB | — | Full-text vault search with index |
| `settings-search` | Settings Search | v1.3.10 | 18 KB | — | Search within Obsidian settings panels |
| `recent-files-obsidian` | Recent Files | v1.7.6 | 61 KB | — | Recently opened file list |
| `home-tab` | Home tab | v1.2.2 | 369 KB | — | Browser-like search tab for local files |
| `obsidian42-strange-new-worlds` | Strange New Worlds | v2.3.7 | 107 KB | — | Visual indicators of vault interconnection |
| `tag-wrangler` | Tag Wrangler | v0.6.4 | 131 KB | — | Rename, merge, toggle tags from tags view |
| `smart-connections` | Smart Connections | v4.1.8 | 951 KB | — | Semantic search and AI-powered related content |
| `smart-connections-visualizer` | Smart Connections Visualizer | v1.0.27 | 217 KB | `smart-connections` | Visual graph of semantic connections |

### Content Creation / Editing

| Plugin ID | Name | Version | Size | Depends On | Rationale |
|---|---|---|---|---|---|
| `templater-obsidian` | Templater | v2.18.1 | 337 KB | — | Template engine for vault note creation |
| `ai-templater` | AI for Templater | v1.0.20 | 278 KB | `templater-obsidian` | AI extension for Templater; uses OpenAI client |
| `nldates-obsidian` | Natural Language Dates | v0.6.2 | 346 KB | — | Date-links from natural language input |
| `obsidian-icon-shortcodes` | Icon Shortcodes | v0.9.7 | 435 KB | — | Emoji/icon insertion with shortcodes |
| `dataview` | Dataview | v0.5.68 | 1,275 KB | — | Complex data views, inline queries |
| `obsidian-tasks-plugin` | Tasks | v7.23.1 | 840 KB | — | Task tracking across vault with dates, recurrence |
| `obsidian-day-planner` | Day Planner | v0.28.0 | 1,533 KB | — | Day planning with clean UI |
| `wikipedia-search` | Wikipedia Helper | v2.7.0 | 110 KB | — | Search and link Wikipedia articles |
| `handwritten-notes` | Handwritten Notes | v1.4.0 | 259 KB | — | PDF annotation with stylus |
| `msg-handler` | MSG Handler | v0.0.6 | 1,030 KB | — | Display/search Outlook MSG files in vault |
| `letterboxd-rss-sync` | Letterboxd Diary RSS Sync | v1.3.0 | 46 KB | — | Syncs Letterboxd diary (personal) |

### Daily Notes / Calendar

| Plugin ID | Name | Version | Size | Depends On | Rationale |
|---|---|---|---|---|---|
| `periodic-notes` | Periodic Notes | v0.0.17 | 177 KB | — | Daily/weekly/monthly note management |
| `roygbiv-day-accent` | ROYGBIV Day Accent | v1.0.0 | 3 KB | `periodic-notes` | Weekday accent color rotation (built by Logan+Copilot 2026-04-03) |

---

## DORMANT — 28 Plugins (installed but not enabled)

### AI / LLM (6 plugins — LLM sprawl, Checkpoint 4 of PLUGIN-TRIAGE-UTF8)

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `ai-image-analyzer` | AI Image Analyzer | v1.2.1 | 598 KB | Yes | PENDING |
| `bmo-chatbot` | BMO Chatbot | v2.3.3 | 450 KB | Yes | PENDING |
| `large-language-models` | Large Language Models | v0.23.0 | 1,557 KB | Yes | PENDING |
| `nexus-ai-chat-importer` | Nexus AI Chat Importer | v1.5.7 | 1,100 KB | Yes | PENDING |
| `taskbone-ocr-plugin` | Taskbone | v2.3.2 | 348 KB | Yes | PENDING |
| `text-extractor` | Text Extractor | v0.7.0 | 6,817 KB | Yes | PENDING |

### Content Organization (6 plugins)

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `make-md` | make.md | v1.3.4 | 5,759 KB | Yes | PENDING |
| `notebook-navigator` | Notebook Navigator | v2.5.6 | 4,786 KB | Yes | PENDING |
| `quickadd` | QuickAdd | v2.12.0 | 4,179 KB | Yes | PENDING |
| `obsidian-folder-index` | Folder Index | v1.0.30 | 43 KB | Yes | PENDING |
| `map-of-content` | Map of Content | v1.4.0 | 134 KB | Yes | PENDING |
| `links` | Links | v1.17.51 | 212 KB | Yes | PENDING |

### Calendar / Date (overlaps with enabled `periodic-notes`)

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `calendar` | Calendar | v1.5.10 | 138 KB | Yes | PENDING |
| `calendarium` | Calendarium | v2.1.0 | 1,040 KB | Yes | PENDING |
| `keep-the-rhythm` | Keep the Rhythm | v0.2.8 | 363 KB | Yes | PENDING |

### PDF / Document (overlaps with enabled `handwritten-notes`)

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `obsidian-extract-pdf-highlights` | PDF Highlights | v0.0.4 | 3,816 KB | Yes | PENDING |
| `pdf-plus` | PDF++ | v0.40.31 | 1,092 KB | Yes | PENDING |

### Table / Editing

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `table-editor-obsidian` | Advanced Tables | v0.22.1 | 268 KB | Yes | PENDING |
| `editing-toolbar` | Editing Toolbar | v4.0.2 | 629 KB | Yes | PENDING |
| `cmdr` | Commander | v0.5.4 | 146 KB | Yes | PENDING |

### Visual / UI

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `obsidian-icon-folder` | Iconize | v2.14.7 | 407 KB | Yes | PENDING |
| `oz-image-plugin` | Image in Editor | v2.2.6 | 161 KB | Yes | PENDING |
| `obsidian-admonition` | Admonition | v11.0.3 | 1,302 KB | Yes | PENDING |

### Specialty

| Plugin ID | Name | Version | Size | Has Config | Logan's Decision |
|---|---|---|---|---|---|
| `obsidian-leaflet-plugin` | Leaflet | v6.0.5 | 1,561 KB | Yes | PENDING — maps |
| `obsidian-5e-statblocks` | Fantasy Statblocks | v4.10.3 | 3,016 KB | Yes | PENDING — D&D |
| `obsidian-dice-roller` | Dice Roller | v11.4.2 | 904 KB | Yes | PENDING — D&D |
| `loom` | Loom | v1.22.6 | 2,121 KB | Yes | PENDING |
| `translate` | Translate | v1.4.9 | 1,191 KB | Yes | PENDING |

---

## Dependency Tree

```
obsidian-local-rest-api
  └── mcp-tools (MCP bridge requires REST API server)

smart-connections
  └── smart-connections-visualizer

templater-obsidian
  └── ai-templater

periodic-notes
  └── roygbiv-day-accent (reads weekday frontmatter from daily notes)

breadcrumbs
  └── (reads `related:` frontmatter — keystone for zettelkasten navigation)

dataview
  └── (many notes may contain inline dataview queries)
```

---

## Sync Storage Impact

With "Installed community plugins: ON" on the laptop, ALL 54 plugin directories sync to the Obsidian Sync remote.

| Category | Size | % of Sync budget |
|---|---|---|
| mcp-tools alone | 117 MB | 11.4% of 1 GB |
| Other enabled (25) | 11 MB | 1.1% |
| Dormant (28) | 43 MB | 4.2% |
| **Total plugins** | **171 MB** | **16.7%** |

If dormant plugins are removed: 171 → 128 MB (saves 43 MB / 4.2%).
If mcp-tools is excluded: 171 → 54 MB (saves 117 MB / 11.4%).

---

## Activity Log

| Date | Agent | Action | Rationale |
|---|---|---|---|
| 2026-04-12 | Claude (Abhorsen) | Created this registry | No authoritative plugin record existed; agents toggling plugins without governance |
| 2026-04-05 | Claude (Abhorsen) | Enabled +5: roygbiv-day-accent, tag-wrangler, nldates-obsidian, periodic-notes, graph-nested-tags | Daily note system + ROYGBIV accent (`ec09efd`) |
| 2026-04-05 | Codex (Janitor) | Corrupted community-plugins.json to 140 entries (UTF-16 LE) | Incident — caught and reverted |
| 2026-03-28 | Claude (Abhorsen) | Plugin auth inventory audit | MCP connector audit (PLUGIN-AUTH-INVENTORY-2026-03-28.md) |

---

*This registry is the authoritative source for plugin state. LEVELSET-CURRENT, VAULT-CONVENTIONS, and community-plugins.json derive from it — not the other way around. Logan decides. The vault witnesses.*
