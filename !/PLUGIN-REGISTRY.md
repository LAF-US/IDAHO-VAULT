---
authority: LOGAN
status: AUTHORITATIVE - no agent enables, disables, installs, or removes plugins without updating this registry
updated: 2026-04-17
related:
  - PLUGIN-TRIAGE-UTF8
  - VAULT-CONVENTIONS
  - LEVELSET-CURRENT
  - AGENTS
  - Obsidian Sync
  - manifest
---

# Plugin Layer Manifest

**Owner:** Logan Finney
**Last audited:** 2026-04-12 by Claude Code (The Abhorsen)
**Primary interface surfaces:** `.obsidian/community-plugins.json`, `.obsidian/plugins/`

This file is the live doctrine, topology, and promotion surface for the
community-plugin layer of IDAHO-VAULT.

The previous flat inventory has been refactored to match the working shape used
by `.crewai/MANIFEST.md`: boundaries first, topology second, promotion rules
third. The plugin layer is now treated as a governed subsystem instead of a
loose pile of installed extensions.

---

## Layer Boundaries

| Surface | Role | Authority |
|---|---|---|
| `!/PLUGIN-REGISTRY.md` | Live doctrine, topology, dependency declarations, and promotion rules for the plugin layer | Current plugin truth |
| `.obsidian/community-plugins.json` | Enabled-plugin runtime interface state | Interface/output surface, not doctrine by itself |
| `.obsidian/plugins/` | Installed plugin payloads, manifests, runtime assets, and local plugin data | Drive/runtime surface |
| `LEVELSET-CURRENT.md` | Ecosystem summary and historical synthesis | Summary only; derivative |
| `VAULT-CONVENTIONS.md` | Shared vault governance and sync boundary rules | Higher-order shared governance |
| Historical triage/audit notes | Preserved reasoning and incident history | Archive only |

---

## Layered Model

| Layer | Meaning | Writable By | Promotion Rule |
|---|---|---|---|
| `CANON` | Durable plugin doctrine: what is allowed, what is enabled, why it exists | Logan or explicitly assigned agents | Canon changes require registry update here |
| `DRIVE` | Installed plugin payloads and tracked configuration surfaces | Logan and assigned agents | Drive changes become durable only when reflected here |
| `RUNTIME` | Machine-local plugin data, caches, indexes, and sync side effects | Obsidian, plugins, local agents | Runtime artifacts do not self-promote |
| `ARCHIVE` | Historical audits, incidents, prior plugin states, UTF-8 incidents, abandoned experiments | Human-curated archival work | Archive informs doctrine but does not overrule it |

Plugin directories are not self-explanatory. Installation state, enabled state,
and doctrinal approval are three different things.

---

## Canonical Required Set

The live plugin layer needs an explicit minimum standing set.

Until now, the registry has clearly separated `installed`, `enabled`, and
`approved`, but it has not clearly separated `enabled` from `required`.
That made the desktop's curated stack look flatter than it really is.

Current priority:

- stage 1 = metadata and frontmatter
- relation fields must stay machine-legible
- periodic note creation must stay deterministic
- normalization must happen without agents improvising schema in prose

### Required core plugins

These core plugins are part of the minimum metadata/frontmatter path.

| Plugin ID | Name | Why it is required now |
|---|---|---|
| `properties` | Properties | Canonical Obsidian UI for viewing and editing YAML/frontmatter-backed note properties |
| `daily-notes` | Daily Notes | Root daily-note entrypoint used by the live daily-note infrastructure and tracked config |
| `templates` | Templates | Applies the tracked markdown templates that seed frontmatter and note structure |

### Required community plugins

These community plugins are the current canon minimum for stage 1.

| Plugin ID | Name | Why it is required now |
|---|---|---|
| `obsidian-linter` | Linter | Normalizes frontmatter-adjacent structure and timestamp fields, and keeps metadata drift from accumulating silently |
| `breadcrumbs` | Breadcrumbs | Reads the `related:` relation mesh and makes frontmatter relations operational instead of inert |
| `periodic-notes` | Periodic Notes | Canonical creation and format wiring for daily, weekly, monthly, quarterly, and yearly note classes |

### Additional scoped requirements

Some enabled plugins are required, but for narrower reasons than stage-1
metadata/frontmatter authoring.

| Plugin ID | Name | Required scope | Why it is required in that scope |
|---|---|---|---|
| `dataview` | Dataview | Corpus query/render contract | Existing notes and registry doctrine already assume Dataview-backed inspection and inline query availability |
| `obsidian-local-rest-api` | Local REST API | Desktop agent runtime | Required runtime server for the local Obsidian-to-agent bridge on the desktop engine-room device |
| `mcp-tools` | MCP Tools | Desktop agent runtime | Required bridge layer for the current MCP/agent ecosystem; depends on `obsidian-local-rest-api` being live |
| `roygbiv-day-accent` | ROYGBIV Day Accent | Desktop operator context | Custom local plugin that binds desktop accent state to `weekday:` frontmatter on the most recently worked daily note and persists that state across navigation/restart |

These are real requirements, but they are not the same claim as “required to
create and normalize frontmatter.”

### Enabled and legitimate, but not currently canon-required

These plugins may remain enabled and useful, but the registry does not
currently declare them required by a live lane.

| Plugin ID | Name | Current standing |
|---|---|---|
| `tag-wrangler` | Tag Wrangler | Useful maintenance surface for frontmatter tags, but not currently declared required |
| `nldates-obsidian` | Natural Language Dates | Input convenience only; not currently declared required |
| `obsidian-tasks-plugin` | Tasks | Task workflow layer; important but not yet declared required by current doctrine |
| `templater-obsidian` | Templater | Enabled tooling surface, but not currently proven by the live root templates as a requirement |

### Dormant and not required for stage 1

- `calendar`
- `calendarium`
- `keep-the-rhythm`
- `obsidian-5e-statblocks`
- `obsidian-dice-roller`

These may be legitimate future systems, but they currently have no standing in
the metadata/frontmatter minimum.

---

## Current Narrow Scope: Time And Workflow

For the current plugin question, narrow the issue to the live time-management
loop rather than the whole vault UX.

The operative loop today is:

`daily-notes` -> `DAILY NOTE TEMPLATE.md` -> `TO DO LIST.md` -> `.github/scripts/daily_rollover.py`

with `periodic-notes` handling recurring note classes and
`roygbiv-day-accent` providing weekday-bound desktop state.

That means:

- the vault is currently file-first, not calendar-first
- task truth currently lives in markdown checkboxes plus carryforward scripts
- a time plugin becomes required only if this loop breaks without it
- stage-1 metadata doctrine still applies underneath this narrower time scope

### Canon time/workflow plugin set

| Plugin ID | Standing in this scope | Why it matters now |
|---|---|---|
| `daily-notes` | Required | Live daily-note entrypoint bound to the tracked daily-note template |
| `templates` | Required | Applies the tracked template that seeds the daily note's structure and links |
| `periodic-notes` | Required | Creates the active daily/weekly/monthly/quarterly/yearly note classes used by the current note cadence |
| `roygbiv-day-accent` | Scoped required | Reads `weekday:` frontmatter from the active daily-note flow and keeps desktop operator context aligned |

### Enabled, useful, but not yet canon-required for time/workflow

| Plugin ID | Current standing | Why it is not required yet |
|---|---|---|
| `obsidian-tasks-plugin` | Workflow-adjacent | The live task loop currently works on plain markdown checkboxes in daily notes and `TO DO LIST.md`; no canon query or automation contract yet requires Tasks-specific syntax |
| `obsidian-day-planner` | Workflow-adjacent | Configured and potentially useful, but no tracked template, doctrine surface, or automation currently depends on its timeline UI |
| `nldates-obsidian` | Input convenience | Helps with typing dates, but the time system does not rely on it to remain lawful |

### Explicitly out of current time/workflow scope

| Plugin ID | Status | Why it stays out of scope now |
|---|---|---|
| `calendar` | Dormant | The live loop does not depend on a separate calendar-pane plugin |
| `calendarium` | Dormant | Installed, but current config has no live calendars and no daily-note binding |
| `keep-the-rhythm` | Dormant | No current doctrinal or automation dependency |

Time/workflow can widen later, but the present canon should stay anchored to
the loop Logan is actually trying to make reliable.

---

## Selection Principles

Required does not mean fashionable, expansive, or merely convenient.

A plugin earns standing here only when it is:

- tied to a live lane, device role, or workflow contract
- smaller and more dependable than the available alternatives
- explicit about what it depends on
- survivable when it fails
- not duplicating another enabled plugin without a named reason

### Durability Preference Order

When choosing or promoting plugins, prefer this order:

1. Obsidian core plugin
2. tracked vault-native code or tiny local custom plugin
3. lightweight, maintained community plugin with clear scope
4. heavy community plugin with meaningful operational benefit
5. connector or AI-heavy plugin with external/runtime dependencies

The burden of proof rises as a plugin becomes heavier, more overlapping, or
more dependent on external services.

### Redundancy Doctrine

Redundancy is desirable at the workflow level, not as indiscriminate plugin
overlap.

- Keep the note truth in markdown and frontmatter whenever possible.
- Prefer plugins that read or normalize existing note structure over plugins
  that become the only place truth can live.
- If a required plugin fails, there should still be a lawful manual or lower
  layer path to continue work.
- Two plugins that solve the same problem need a named division of labor or one
  of them should lose standing.

### Dependency Rule

Required status is not just a statement of usefulness. It is a dependency
claim.

- Every required plugin must declare what lower layer it relies on.
- Hard dependencies must be named explicitly here instead of inferred from
  runtime luck.
- Prefer dependency chains that terminate in core plugins, tracked markdown,
  frontmatter, or tiny local code.
- Be cautious about declaring one community plugin required if it only exists
  to prop up another heavier community plugin.
- If a required plugin depends on another required plugin, both the dependency
  and the fallback path must stay visible in this registry.

### Maintenance And Exit Rule

Community plugins fail, stagnate, or bloat over time. Required status therefore
needs an exit story.

- A required community plugin should have at least one of these:
  active maintenance, a local replacement path, or a lawful manual fallback.
- If a plugin becomes abandonware and the vault cannot continue without it, the
  real bug is architectural and must be corrected.
- Large plugins receive extra scrutiny because install size, bundled
  dependencies, and hidden feature overlap all raise the operational cost.
- Canon should prefer durable usefulness over novelty, convenience, or
  ecosystem hype.

### Bloat Rule

Do not make a plugin required if:

- its main value is cosmetic and no workflow depends on it
- its job can be done just as well by a lighter surface already in the stack
- it introduces a second source of truth
- it depends on abandoned infrastructure without a fallback path

### Fallback Expectations For Current Required Plugins

| Plugin ID | Scope | Fallback if plugin breaks | Failure severity |
|---|---|---|---|
| `properties` | Frontmatter editing | Raw YAML editing in markdown | Low |
| `daily-notes` | Daily-note creation | Manual creation of ISO daily notes from tracked template | Medium |
| `templates` | Template insertion | Manual copy/use of tracked template files | Medium |
| `obsidian-linter` | Metadata normalization | Manual cleanup plus repo scripts and review discipline | Medium |
| `breadcrumbs` | Relation rendering | `related:` frontmatter remains readable in note source | Low |
| `periodic-notes` | Recurring note creation | `daily-notes` + `templates` for daily flow, manual recurring-note creation for longer periods | Medium |
| `dataview` | Query/render contract | Notes remain valid; query-driven dashboards and inline readouts degrade | Medium |
| `obsidian-local-rest-api` | Desktop agent runtime | Human vault use continues; local agent bridge degrades | High for agent runtime, low for human authoring |
| `mcp-tools` | Desktop agent runtime | Human vault use continues; MCP-specific workflows degrade | High for agent runtime, low for human authoring |
| `roygbiv-day-accent` | Desktop operator context | Accent persistence degrades; daily-note metadata remains intact | Low |

### Current Required Dependency Map

| Plugin ID | Requirement class | Hard dependency | Redundancy posture |
|---|---|---|---|
| `properties` | Foundational core | Markdown files with YAML/frontmatter | Raw source editing remains lawful |
| `daily-notes` | Foundational core | Tracked daily-note naming/config contract | Manual ISO-note creation remains lawful |
| `templates` | Foundational core | Tracked template files in the vault | Manual template copy remains lawful |
| `obsidian-linter` | Foundational community | The repo's metadata/frontmatter conventions | Manual cleanup and repo review remain lawful |
| `breadcrumbs` | Foundational community | `related:` frontmatter and note links | Frontmatter stays readable without rendering help |
| `periodic-notes` | Foundational community | Tracked periodic-note config and note classes | Daily flow can fall back to `daily-notes` plus manual recurring-note creation |
| `dataview` | Scoped community | Markdown/frontmatter corpus | Query dashboards degrade; notes remain valid |
| `obsidian-local-rest-api` | Scoped community | Obsidian desktop runtime and local vault access | Human use survives without the bridge |
| `mcp-tools` | Scoped community | `obsidian-local-rest-api` and the local MCP runtime | MCP workflows degrade; note truth remains in markdown |
| `roygbiv-day-accent` | Scoped local custom | `weekday:` frontmatter on live daily notes | Visual state degrades without damaging the note |

---

## Current State

| Key | Value |
|---|---|
| Enabled plugins | 26 |
| Canonical required core plugins | 3 |
| Canonical required community plugins | 3 |
| Additional scoped required community plugins | 4 |
| Dormant installed plugins | 28 |
| Total installed plugins | 54 |
| Total plugin payload size | 171 MB |
| Largest single plugin | `mcp-tools` at 117 MB |
| Governing interface file | `.obsidian/community-plugins.json` |
| Governing doctrine file | `!/PLUGIN-REGISTRY.md` |
| Promotion gate | No plugin-state change counts as legitimate until this registry is updated |

---

## Dependency Declaration Pattern

CrewAI's source layout declares three different things separately:

1. workspace members
2. dependency groups
3. source wiring

This plugin layer now follows the same doctrinal pattern.

### Plugin membership

Plugin membership is the installed set present in `.obsidian/plugins/`.

### Plugin activation

Plugin activation is the enabled set expressed in
`.obsidian/community-plugins.json`.

### Plugin requirement

Plugin requirement is the minimum standing set declared in the `Canonical
Required Set` section above.

### Plugin dependency wiring

Dependency relations are declared here explicitly and must not be inferred only
from local runtime behavior.

That separation matters because a plugin can be:

- installed but dormant
- enabled but dependent on another plugin
- enabled but not required
- required only inside a specific lane or device role
- required without carrying the whole plugin layer on its back
- present on disk but not doctrinally approved

---

## Live Topology

### Enabled plugin sets

#### Infrastructure / Agent Layer

| Plugin ID | Name | Version | Size | Depends On | Purpose | Status |
|---|---|---|---|---|---|---|
| `obsidian-git` | Git | v2.38.0 | 732 KB | - | Git integration for vault version control | Enabled |
| `obsidian-local-rest-api` | Local REST API | v3.5.0 | 2,530 KB | - | REST API server for MCP bridge; required by agent ecosystem | Enabled |
| `mcp-tools` | MCP Tools | v0.2.27 | 117,479 KB | `obsidian-local-rest-api` | MCP bridge connecting Claude Desktop to vault; semantic search, templates | Enabled |
| `obsidian-linter` | Linter | v1.31.2 | 892 KB | - | Frontmatter formatting and YAML normalization on save | Enabled |

#### Navigation / Search

| Plugin ID | Name | Version | Size | Depends On | Purpose | Status |
|---|---|---|---|---|---|---|
| `breadcrumbs` | Breadcrumbs | v4.4.4 | 892 KB | - | Keystone navigation across `related:` frontmatter links | Enabled |
| `omnisearch` | Omnisearch | v1.28.2 | 606 KB | - | Full-text vault search with index | Enabled |
| `settings-search` | Settings Search | v1.3.10 | 18 KB | - | Search within Obsidian settings panels | Enabled |
| `recent-files-obsidian` | Recent Files | v1.7.6 | 61 KB | - | Recently opened file list | Enabled |
| `home-tab` | Home tab | v1.2.2 | 369 KB | - | Browser-like search tab for local files | Enabled |
| `obsidian42-strange-new-worlds` | Strange New Worlds | v2.3.7 | 107 KB | - | Visual indicators of vault interconnection | Enabled |
| `tag-wrangler` | Tag Wrangler | v0.6.4 | 131 KB | - | Rename, merge, and toggle tags | Enabled |
| `smart-connections` | Smart Connections | v4.1.8 | 951 KB | - | Semantic search and AI-powered related content | Enabled |
| `smart-connections-visualizer` | Smart Connections Visualizer | v1.0.27 | 217 KB | `smart-connections` | Visual graph of semantic connections | Enabled |

#### Content Creation / Editing

| Plugin ID | Name | Version | Size | Depends On | Purpose | Status |
|---|---|---|---|---|---|---|
| `templater-obsidian` | Templater | v2.18.1 | 337 KB | - | Template engine for vault note creation | Enabled |
| `ai-templater` | AI for Templater | v1.0.20 | 278 KB | `templater-obsidian` | AI extension for Templater; uses OpenAI client | Enabled |
| `nldates-obsidian` | Natural Language Dates | v0.6.2 | 346 KB | - | Date-links from natural language input | Enabled |
| `obsidian-icon-shortcodes` | Icon Shortcodes | v0.9.7 | 435 KB | - | Emoji and icon insertion with shortcodes | Enabled |
| `dataview` | Dataview | v0.5.68 | 1,275 KB | - | Complex data views and inline queries | Enabled |
| `obsidian-tasks-plugin` | Tasks | v7.23.1 | 840 KB | - | Cross-vault task tracking | Enabled |
| `obsidian-day-planner` | Day Planner | v0.28.0 | 1,533 KB | - | Day planning with clean UI | Enabled |
| `wikipedia-search` | Wikipedia Helper | v2.7.0 | 110 KB | - | Search and link Wikipedia articles | Enabled |
| `handwritten-notes` | Handwritten Notes | v1.4.0 | 259 KB | - | PDF annotation with stylus | Enabled |
| `msg-handler` | MSG Handler | v0.0.6 | 1,030 KB | - | Display and search Outlook MSG files in vault | Enabled |
| `letterboxd-rss-sync` | Letterboxd Diary RSS Sync | v1.3.0 | 46 KB | - | Syncs Letterboxd diary | Enabled |

#### Daily Notes / Calendar

| Plugin ID | Name | Version | Size | Depends On | Purpose | Status |
|---|---|---|---|---|---|---|
| `periodic-notes` | Periodic Notes | v0.0.17 | 177 KB | - | Daily, weekly, and monthly note management | Enabled |
| `roygbiv-day-accent` | ROYGBIV Day Accent | v1.0.0 | 3 KB | `periodic-notes` | Weekday accent color rotation | Enabled |

### Dormant installed topology

Dormant plugins are installed but not part of the live enabled topology.

#### AI / LLM

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `ai-image-analyzer` | AI Image Analyzer | v1.2.1 | 598 KB | Yes | Dormant / pending Logan |
| `bmo-chatbot` | BMO Chatbot | v2.3.3 | 450 KB | Yes | Dormant / pending Logan |
| `large-language-models` | Large Language Models | v0.23.0 | 1,557 KB | Yes | Dormant / pending Logan |
| `nexus-ai-chat-importer` | Nexus AI Chat Importer | v1.5.7 | 1,100 KB | Yes | Dormant / pending Logan |
| `taskbone-ocr-plugin` | Taskbone | v2.3.2 | 348 KB | Yes | Dormant / pending Logan |
| `text-extractor` | Text Extractor | v0.7.0 | 6,817 KB | Yes | Dormant / pending Logan |

#### Content Organization

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `make-md` | make.md | v1.3.4 | 5,759 KB | Yes | Dormant / pending Logan |
| `notebook-navigator` | Notebook Navigator | v2.5.6 | 4,786 KB | Yes | Dormant / pending Logan |
| `quickadd` | QuickAdd | v2.12.0 | 4,179 KB | Yes | Dormant / pending Logan |
| `obsidian-folder-index` | Folder Index | v1.0.30 | 43 KB | Yes | Dormant / pending Logan |
| `map-of-content` | Map of Content | v1.4.0 | 134 KB | Yes | Dormant / pending Logan |
| `links` | Links | v1.17.51 | 212 KB | Yes | Dormant / pending Logan |

#### Calendar / Date

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `calendar` | Calendar | v1.5.10 | 138 KB | Yes | Dormant / pending Logan |
| `calendarium` | Calendarium | v2.1.0 | 1,040 KB | Yes | Dormant / pending Logan |
| `keep-the-rhythm` | Keep the Rhythm | v0.2.8 | 363 KB | Yes | Dormant / pending Logan |

#### PDF / Document

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `obsidian-extract-pdf-highlights` | PDF Highlights | v0.0.4 | 3,816 KB | Yes | Dormant / pending Logan |
| `pdf-plus` | PDF++ | v0.40.31 | 1,092 KB | Yes | Dormant / pending Logan |

#### Table / Editing

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `table-editor-obsidian` | Advanced Tables | v0.22.1 | 268 KB | Yes | Dormant / pending Logan |
| `editing-toolbar` | Editing Toolbar | v4.0.2 | 629 KB | Yes | Dormant / pending Logan |
| `cmdr` | Commander | v0.5.4 | 146 KB | Yes | Dormant / pending Logan |

#### Visual / UI

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `obsidian-icon-folder` | Iconize | v2.14.7 | 407 KB | Yes | Dormant / pending Logan |
| `oz-image-plugin` | Image in Editor | v2.2.6 | 161 KB | Yes | Dormant / pending Logan |
| `obsidian-admonition` | Admonition | v11.0.3 | 1,302 KB | Yes | Dormant / pending Logan |

#### Specialty

| Plugin ID | Name | Version | Size | Has Config | Status |
|---|---|---|---|---|---|
| `obsidian-leaflet-plugin` | Leaflet | v6.0.5 | 1,561 KB | Yes | Dormant / pending Logan |
| `obsidian-5e-statblocks` | Fantasy Statblocks | v4.10.3 | 3,016 KB | Yes | Dormant / pending Logan |
| `obsidian-dice-roller` | Dice Roller | v11.4.2 | 904 KB | Yes | Dormant / pending Logan |
| `loom` | Loom | v1.22.6 | 2,121 KB | Yes | Dormant / pending Logan |
| `translate` | Translate | v1.4.9 | 1,191 KB | Yes | Dormant / pending Logan |

---

## Dependency Declarations

These are the explicit dependency declarations for the current plugin layer.

| Parent | Child | Dependency type | Operational note |
|---|---|---|---|
| `obsidian-local-rest-api` | `mcp-tools` | Required runtime dependency | MCP bridge depends on the REST API server being live |
| `smart-connections` | `smart-connections-visualizer` | Feature dependency | Visualizer is subordinate to Smart Connections |
| `templater-obsidian` | `ai-templater` | Functional dependency | AI for Templater extends the Templater surface |
| `periodic-notes` | `roygbiv-day-accent` | Data dependency | ROYGBIV reads weekday frontmatter from daily-note flow |
| `weekday:` frontmatter on live daily notes | `roygbiv-day-accent` | Desktop state contract | The plugin resolves the day from note frontmatter and persists the last active day when the current note has no weekday block |
| `daily-notes` + `templates` | `periodic-notes` | Stage-1 creation contract | The live periodic-note path depends on tracked template and daily-note config surfaces staying aligned |
| `breadcrumbs` | `related:` frontmatter | Data contract | Keystone reader of the vault relation mesh |
| `dataview` | inline dataview queries in notes | Data contract | Queries in corpus assume Dataview availability |

This section is the plugin-layer analogue of CrewAI's separated workspace and
source declarations: dependency edges live here, not only in memory.

---

## Writable Surfaces

| Surface | Purpose | Persistence |
|---|---|---|
| `!/PLUGIN-REGISTRY.md` | Plugin doctrine, topology, and dependency declarations | Durable in git |
| `.obsidian/community-plugins.json` | Enabled-plugin list used by Obsidian | Durable in git, interface state |
| `.obsidian/plugins/*/manifest.json` | Installed plugin identity and version metadata | Durable in git when tracked |
| `.obsidian/plugins/*/data.json` | Plugin-local settings and credentials | Ephemeral / gitignored |
| `.obsidian/plugins/*/cache/` | Plugin caches and generated indexes | Ephemeral / gitignored |
| `.smart-env/`, `.makemd/`, `.space/` | Plugin runtime support, embeddings, and app state | Ephemeral / local runtime |
| `LEVELSET-CURRENT.md` | Ecosystem summary derived from the plugin layer | Durable in git, derivative |

---

## Promotion Rules

1. No agent may enable, disable, install, or remove a community plugin without
   updating this manifest first or in the same change set.
2. Runtime observations do not become doctrine until captured here.
3. A plugin directory on disk does not make the plugin live; enabled topology
   is governed jointly by this manifest and `.obsidian/community-plugins.json`.
4. Plugin-local `data.json`, caches, embeddings, and other runtime artifacts
   never self-promote into canon.
5. Dependency relations must be declared here when they matter operationally.
6. `LEVELSET-CURRENT.md`, `VAULT-CONVENTIONS.md`, and interface files may
   summarize plugin state, but this manifest remains the live plugin authority.

---

## Sync Storage Impact

With "Installed community plugins: ON" on the laptop, all 54 plugin directories
sync to the Obsidian Sync remote.

| Category | Size | Share |
|---|---|---|
| `mcp-tools` alone | 117 MB | 11.4% of 1 GB |
| Other enabled plugins | 11 MB | 1.1% |
| Dormant installed plugins | 43 MB | 4.2% |
| Total plugin payload | 171 MB | 16.7% |

If dormant plugins are removed: 171 MB -> 128 MB.
If `mcp-tools` is excluded: 171 MB -> 54 MB.

---

## Activity Log

| Date | Agent | Action | Rationale |
|---|---|---|---|
| 2026-04-17 | Codex (The Lexicographer) | Added canonical required-plugin tiers for stage 1, query/render, and desktop agent runtime | Separate minimum standing plugins from the broader enabled desktop stack and avoid flattening all requirements into one bucket |
| 2026-04-12 | Codex (The Lexicographer) | Refactored flat plugin registry into manifest form | Align plugin layer with CrewAI-style layer boundaries, topology, writable surfaces, and promotion rules |
| 2026-04-12 | Claude (The Abhorsen) | Created original plugin registry | No authoritative plugin record existed; agents were toggling plugins without governance |
| 2026-04-05 | Claude (The Abhorsen) | Enabled `roygbiv-day-accent`, `tag-wrangler`, `nldates-obsidian`, `periodic-notes`, `graph-nested-tags` | Daily-note system and ROYGBIV accent work |
| 2026-04-05 | Codex (The Janitor) | Corrupted `community-plugins.json` to 140 entries (UTF-16 LE) | Incident - caught and reverted |
| 2026-03-28 | Claude (The Abhorsen) | Plugin auth inventory audit | MCP connector audit (`PLUGIN-AUTH-INVENTORY-2026-03-28.md`) |

---

*This manifest is the authoritative source for plugin doctrine and topology.
Interface state, ecosystem summaries, and runtime payloads derive from it; they
do not replace it.*
