---
title: PLUGIN-MODES-2026-04-11
status: draft
authority: LOGAN
related:
  - '2026-04-11'
  - Breadcrumbs
  - LEVELSET-CURRENT
  - LOGAN
  - Obsidian Sync
  - PLUGIN-TRIAGE
  - plugins
---
# PLUGIN-MODES-2026-04-11

This note translates the existing agentic plugin triage record into practical Obsidian operating modes.

## Records consulted

- `PLUGIN-TRIAGE-UTF8.md` - unresolved checkpoint structure, 49-vs-12 discrepancy, dormant inventory, Breadcrumbs decision gate.
- `LEVELSET-CURRENT.md` - desktop engine-room model, mobile Restricted Mode model, daily-note stack, 140-plugin audit summary.
- `!\__!__\!\! The world is quiet here\DOCKET.md` - active coordination record and prior Obsidian triage breadcrumb.
- `!\__!__\!\! The world is quiet here\DOCKET-ARCHIVE.md` - archived note that "Obsidian Plugin Recovery" was treated as complete on 2026-04-04.

## What the older record says

- The intended device split was already documented:
  - Desktop = engine room with the full plugin stack.
  - Mobile = Restricted Mode capture device with 0 community plugins.
- `LEVELSET-CURRENT.md` reports 49 community plugins enabled on desktop as of 2026-04-05.
- `PLUGIN-TRIAGE-UTF8.md` documents that the repo copy of `.obsidian/community-plugins.json` only showed 12 entries, so the git record was not matching the live desktop record.
- The same triage note left four checkpoints open:
  - authoritative plugin-count confirmation
  - Breadcrumbs field choice
  - dormant-plugin cleanup
  - AI / LLM plugin keep list

## Current local troubleshooting state

For startup recovery on 2026-04-11, the live `.obsidian/community-plugins.json` was reduced to a minimal safe set:

- `periodic-notes`
- `settings-search`
- `tag-wrangler`
- `nldates-obsidian`
- `recent-files-obsidian`

That is a recovery posture, not a final doctrine.

To make this repeatable, local mode snapshots now live in `.obsidian/plugin-modes/`, and a switch helper now lives at `scripts/set-obsidian-plugin-mode.ps1`.

With Obsidian closed, `.obsidian/workspace.json` has now been reset to a plain recovery layout with only ordinary core panes. Closed-state backups exist at:

- `.obsidian/workspace.pre-troubleshoot-2026-04-11.json`
- `.obsidian/workspace.pre-recovery-cleanup-2026-04-11.json`

## Logic tree

If Obsidian is unstable or struggling to open:
- Stay in `Restricted Recovery`.

If Obsidian opens cleanly and Logan mainly needs today's note, light navigation, and low-friction writing:
- Move to `Writing / Daily Notes`.

If the session goal is structure, graph traversal, zettelkasten navigation, or backlink-led browsing:
- Move to `Graph / Navigation`.

If the session goal is agent interop, vault automation, or external-system handshakes:
- Move to `Agent Ops`.

If the session goal is semantic exploration, associative recall, or AI-assisted lookup:
- Move to `Research / Semantic`.

If the session goal is PDFs, handwriting, OCR, or captured documents:
- Move to `Capture / Media`.

Only after startup is calm and the desktop count is reconciled against the historical record:
- Consider `Full Engine Room`.

## Proposed modes

### 1. Restricted Recovery

Use when:
- startup is brittle
- workspace panes are misbehaving
- Logan only needs access, daily notes, and basic navigation

Plugin group:
- `periodic-notes`
- `settings-search`
- `tag-wrangler`
- `nldates-obsidian`
- `recent-files-obsidian`

### 2. Writing / Daily Notes

Use when:
- the priority is writing, dailies, timestamps, and calm navigation
- Logan wants the daily-note system without the full graph or agent stack

Plugin group:
- `periodic-notes`
- `nldates-obsidian`
- `recent-files-obsidian`
- `tag-wrangler`
- `settings-search`
- `roygbiv-day-accent`
- `home-tab`
- `templater-obsidian` if needed

### 3. Graph / Navigation

Use when:
- Logan is traversing `related:` links
- the zettelkasten address space is the main work surface
- note-structure and retrieval matter more than automation

Plugin group:
- `breadcrumbs`
- `omnisearch`
- `tag-wrangler`
- `recent-files-obsidian`
- `home-tab`

Note:
- This mode depends on the unresolved Breadcrumbs checkpoint from `PLUGIN-TRIAGE-UTF8.md`.

### 4. Agent Ops

Use when:
- Logan wants machine-facing vault work
- REST, MCP, git, message handling, or templated automation is the goal

Plugin group:
- `obsidian-local-rest-api`
- `mcp-tools`
- `msg-handler`
- `obsidian-git`
- `templater-obsidian`
- `ai-templater`

Risk:
- This is the highest-friction mode short of the full stack and should not be the default startup set while recovery is underway.

### 5. Research / Semantic

Use when:
- Logan wants exploratory retrieval rather than strict note writing
- semantic graph work or associative lookup is the point

Plugin group:
- `smart-connections`
- `smart-connections-visualizer`
- `omnisearch`
- `wikipedia-search`
- `notebook-navigator`

Risk:
- Several workspace-sensitive panes appear tied to this territory and should be enabled only after startup proves stable.

### 6. Capture / Media

Use when:
- the session is about PDFs, handwriting, OCR, or imported materials

Plugin group:
- `handwritten-notes`
- `pdf-plus`
- `obsidian-extract-pdf-highlights`
- `taskbone-ocr-plugin`
- `text-extractor`

### 7. Full Engine Room

Use when:
- Logan explicitly wants the historic desktop role described in `LEVELSET-CURRENT.md`
- the plugin count has been reconciled
- workspace cleanup is complete

Definition:
- The broader 49-plugin desktop stack documented on 2026-04-05, restored intentionally rather than all at once.

## Local mode files

- `restricted-recovery.json` - current low-risk startup mode
- `desktop-pre-troubleshoot-2026-04-11.json` - backed-up 23-plugin pre-reduction desktop set
- `writing-daily-notes.json`
- `graph-navigation.json`
- `agent-ops.json`
- `research-semantic.json`
- `capture-media.json`
- `_last-live-backup.json` - most recent pre-switch copy of `.obsidian/community-plugins.json`

These are operational snapshots, not claims that the historical 49-plugin desktop state has already been fully reconstructed.

## Enable-last list

The current `.obsidian/workspace.json` still tries to restore several custom panes that are strong candidates for startup friction:

- `msg-handler-search-view`
- `notebook-navigator`
- `mk-path-view`
- `smart-connections-visualizer`
- `smart-lookup-view`
- `Strange New Worlds`
- `todo`
- `planner-timeline`
- `chronology-calendar-view`
- `loom`
- `loom-siblings`

These should be treated as enable-last or post-reset surfaces until the workspace file is cleaned with Obsidian fully closed.

## Working recommendation

- Keep `Restricted Recovery` as the current default until startup is calm.
- Promote to `Writing / Daily Notes` first, because it honors the previously documented desktop/mobile split without reintroducing the whole pane ecosystem.
- Add `Graph / Navigation` next once Logan is ready to resolve the Breadcrumbs field decision.
- Treat `Agent Ops` and `Research / Semantic` as opt-in session modes, not always-on startup modes.
- Delay `Full Engine Room` until the historical plugin count and workspace state are both reconciled.
