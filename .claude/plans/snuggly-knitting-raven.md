# Daily Note System + Plugin Rationalization

## Context

Logan's requirement (from 2026-04-05 daily note): "REMEMBER, AGENTS - I want the dailynote to auto-generate, with a smart-updated template, and the display appearance color synced to today's daily note's weekday field."

Full 140-plugin audit completed. Logan approved the following decisions:
- **YES:** Enable `roygbiv-day-accent` (Logan+Copilot plugin), retire Templater startup script
- **YES:** Enable `tag-wrangler`, `nldates-obsidian`, `periodic-notes`, `graph-nested-tags`
- **KEEP:** `calendarium` stays enabled (back pocket)
- **SWITCH:** Template goes pure core tokens — remove Templater `<% %>` dependency for yesterday/tomorrow

---

## Execution Plan

### Step 1: Enable `roygbiv-day-accent` plugin

Add `roygbiv-day-accent` to `.obsidian/community-plugins.json`.
This plugin (by Logan+Copilot, April 3) reads the active note's `weekday:` frontmatter, applies the matching body class, handles midnight rollover, and works on mobile. Replaces the Templater startup script entirely.

### Step 2: Delete `_templates/roygbiv-startup.md`

The Templater startup script is now redundant. Delete the file.
If `_templates/` is empty after deletion, remove the directory too.
Logan no longer needs to configure Templater's "Startup Templates" setting.

### Step 3: Enable 4 high-value dormant plugins

Add to `.obsidian/community-plugins.json`:
- `tag-wrangler` — rename/merge/search tags (pre-CHAINFIRE essential)
- `nldates-obsidian` — natural language dates in notes
- `periodic-notes` — enhanced daily/weekly/monthly note management
- `graph-nested-tags` — nested tag visualization in graph view

### Step 4: Rewrite template to pure core tokens

Remove all Templater `<% %>` syntax from `DAILY NOTE TEMPLATE.md`. Use only core `{{date:}}` tokens. Leave `yesterday:` and `tomorrow:` empty — `periodic-notes` handles date navigation natively, and Linter's `yaml-timestamp` handles `date created`/`date modified`.

```yaml
---
title: {{date:YYYY-MM-DD}}
aliases:
  - {{date:YYYY-MM-DD}}
  - {{date:MMMM D, YYYY}}
  - {{date:MMMM Do, YYYY}}
  - {{date:D MMMM YYYY}}
  - {{date:dddd, MMMM D, YYYY}}
linter-yaml-title-alias: {{date:YYYY-MM-DD}}
yesterday:
tomorrow:
weekday:
  - {{date:dddd}}
tags:
  - today
  - {{date:YYYY/MM/DD}}
  - dailynote
---
obsidian://open?vault=IDAHO-VAULT&file={{date:YYYY-MM-DD}}

[[TO DO LIST]]
```

**Why pure core:** Works identically on both devices (desktop and phone). No Templater dependency. `yesterday`/`tomorrow` were `null` in most existing daily notes anyway. `periodic-notes` provides prev/next day navigation without frontmatter fields.

### Step 5: Simplify Logan's Settings walkthrough

With `roygbiv-day-accent` handling color and pure core tokens in the template, Logan's remaining manual steps shrink to:

**Core Daily Notes** (Settings → Core Plugins → Daily Notes):
- ✅ "Open daily note on startup" → ON (already done by Logan)

**Templater** (Settings → Community Plugins → Templater):
- Template folder location → `_templates` (already done by Logan)
- ✅ "Trigger Templater on new file creation" → ON (already done by Logan)
- ~~Startup Templates~~ → **REMOVE `_templates/roygbiv-startup`** (no longer needed)

### Step 6: Commit

Stage: `.obsidian/community-plugins.json`, `DAILY NOTE TEMPLATE.md`, deletion of `_templates/roygbiv-startup.md`

### Files modified

| File | Action |
|------|--------|
| `.obsidian/community-plugins.json` | MODIFY — add 5 plugins (roygbiv-day-accent, tag-wrangler, nldates-obsidian, periodic-notes, graph-nested-tags) |
| `DAILY NOTE TEMPLATE.md` | REWRITE — pure core tokens, no Templater |
| `_templates/roygbiv-startup.md` | DELETE — superseded by roygbiv-day-accent plugin |

### Logan's remaining manual step

- Settings → Templater → Startup Templates → **remove** `_templates/roygbiv-startup` (since the file will be gone)

---

## Verification

1. Reopen Obsidian → accent color should be **violet** (Sunday) via `roygbiv-day-accent` plugin reading `weekday: Sunday` from 2026-04-05 daily note
2. Navigate to a different daily note (e.g. 2026-04-04, Saturday) → accent should change to **indigo**
3. Tomorrow: Obsidian opens → auto-creates `2026-04-06.md` with all core tokens filled, `weekday: Monday` → accent turns **red**
4. Tags panel shows `tag-wrangler` context menu on right-click
5. `nldates-obsidian` responds to natural language date input
6. No Templater errors (startup script gone, no tokens to process)

### CHAINFIRE interaction note

When CHAINFIRE eventually runs, it will strip `[[TO DO LIST]]` wikilink in the template body (templates are at repo root, not in `!/` exclusion zone). Add `DAILY NOTE TEMPLATE.md` to CHAINFIRE's exclusion list, or regenerate post-burn.
