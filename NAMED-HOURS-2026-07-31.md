---
title: NAMED HOURS — The Day Shape in Full Calendar
aliases:
  - NAMED HOURS
  - Named Hours
  - Day Shape
updated: 2026-08-12
status: superseded
authority: "Proposed by Claude Code, session_013ie6MP332hZgSgAiSkyPZ7. Authority NOT assumed as LOGAN.
  This note is unratified and governs nothing. The original `authority: LOGAN`
  line was written by this session without warrant; Logan objected to it on PR
  #885 and it is withdrawn here. Promotion is his alone. OVERRULED by Logan on
  PR #885, 2026-08-12: \"fullcalendar.io proposal overruled\". Kept for
  posterity at his instruction, not as a live proposal."
superseded_by: cron_clock
date created: Friday, July 31st 2026
tags:
  - doctrine
  - plugin
  - time
related:
  - PLUGIN-REGISTRY
  - VAULT-CONVENTIONS
  - DAILY NOTE TEMPLATE
  - TO DO LIST
---

> [!warning] Overruled — kept as a record, not a proposal
>
> Logan overruled the fullcalendar.io proposal on PR #885 (2026-08-12) and
> asked that the markdown be kept for posterity. Everything below is preserved
> as written on 2026-07-31, and **none of it is live**:
>
> - **The times in the table below are wrong.** They were measured off a
>   reference render before the day's geometry was settled. The real spans are
>   in `cron_clock`: Dawn, Noon and Dusk at 480 minutes each, Yan through Azer
>   at 204 each, twelve minutes owned by nothing. Boundaries fall on `:01`,
>   `:27`, `:53`, `:18`, `:43`, `:09`, `:35` — not on the `:00`/`:30` marks
>   this note assumes.
> - **`.obsidian/snippets/named-hours.css` no longer exists.** It was removed
>   with the proposal. References to it below are historical. It could not have
>   rendered the settled geometry in any case: it selects FullCalendar's
>   30-minute slot lanes by `data-time`, and no boundary above coincides with
>   one.
> - **The plugin was never installed**, and nothing here asserts otherwise.
>
> What survives the overrule is the naming — ten spans, seven of them counted
> off a shepherd's score, three hinges — and that lives in `cron_clock` now.

The working day is cut into ten named blocks. Seven of them carry a
shepherd's-count name — **Yan, Tan, Tethera, Methera, Pits, Sethera, Azer** —
and the three hinges are plain: **Dawn**, **Noon**, **Dusk**. The count is the
point: a block is named by its position in the day, not by what happens to be
scheduled inside it. The shape is the same every day whether or not anything
is on it.

This note *was* a **proposal** for those blocks — never canon, and nothing was
ever bound by it. It is now overruled; see the banner above. The text from here
down is the 2026-07-31 proposal as written.

---

## The blocks

| # | Block | Start | End | Length | Color |
| --- | --- | --- | --- | --- | --- |
| — | Dawn | 06:00 | 07:00 | 1h00 | `#b6b6b6` |
| 1 | Yan | 07:00 | 08:30 | 1h30 | `#d85c79` |
| 2 | Tan | 08:30 | 10:00 | 1h30 | `#db793a` |
| 3 | Tethera | 10:00 | 11:30 | 1h30 | `#d8bd63` |
| — | Noon | 11:30 | 12:30 | 1h00 | `#888888` |
| 4 | Methera | 12:30 | 14:00 | 1h30 | `#5aaf81` |
| 5 | Pits | 14:00 | 15:30 | 1h30 | `#6b8bdd` |
| 6 | Sethera | 15:30 | 17:00 | 1h30 | `#a47cb0` |
| 7 | Azer | 17:00 | 18:30 | 1h30 | `#aa61bb` |
| — | Dusk | 18:30 | 19:30 | 1h00 | `#707070` |

Dawn to Dusk is 13h30. The three hinges are one hour each — they carry names, they are
just outside the shepherd's count; the seven
counted blocks are ninety minutes each. Noon is centered on 12:00 rather than
starting there — it is the hinge, not the afternoon's first block.

### Provenance of these values

Times and hex values were read off Logan's reference render (uploaded
2026-07-31, session `session_013ie6MP332hZgSgAiSkyPZ7`): block boundaries by
measuring against the render's hour gridlines, colors by sampling the fill of
each block. Every boundary landed on a `:00` or `:30`, which is what makes the
CSS below possible.

**Two things are inferred, not read.** The reference render is cropped just
past 19:00, so Dusk's **end time is assumed** to be 19:30 by symmetry with
Dawn and Noon — the render does not show it. And nothing in the render or the
vault fixes whether the frame is meant to shift on weekends. Both are Logan's
to settle; the `*` wildcard applies until he does.

---

## Why the frame is CSS and the events are markdown

Full Calendar (`obsidian-full-calendar`) is the Obsidian integration for
fullcalendar.io — it is literally that library rendered inside a leaf. It
gives two things this vault can use, and they answer two different questions.

**The frame — where the named blocks come from.** Full Calendar bundles
FullCalendar v5, whose time grid emits a `data-time` attribute on every slot
(`<td class="fc-timegrid-slot-lane" data-time="07:00:00">`). A stylesheet can
therefore paint 07:00–08:30 without any plugin knowing what "Yan" is. That is
what `named-hours.css` does: the day-shape is a background frame, drawn by the
theme layer, present in every **time-grid** view — day and week — and
unaffected if the plugin's own data is lost. Month and list views have no slot
lanes, so they carry no frame.

The alternative — writing the ten blocks into each daily note as events — was
rejected. Full Calendar assigns color **per calendar**, not per event, so ten
blocks written as daily-note events render in one flat color. The rainbow is
only reachable from CSS. Seeding them would also put ten lines of pure
scaffolding into every daily note, which the vault's own carryforward scripts
would then have to learn to ignore.

**The events — what actually happens in a block.** Full Calendar's *daily
note* calendar type reads events straight out of the daily note as list items
under a chosen heading, with times as Dataview inline fields:

```markdown
## Day planner

- [ ] Floor session gavel-in  [startTime:: 09:00]  [endTime:: 10:30]
- [x] Budget hearing writeup  [startTime:: 14:00]  [endTime:: 15:30]
```

Markdown stays the truth; the calendar is a view onto it. Checked items show
as completed. This keeps the arrangement inside the vault's file-first
posture (`!/PLUGIN-REGISTRY.md` § "Current Narrow Scope: Time And Workflow") —
no separate event store, nothing to lose, and the day is still readable in a
plain text editor.

The two layers do not touch: the frame says *what kind of hour this is*, the
events say *what is in it*.

---

## Wiring it up

Plugin binaries are gitignored (`.obsidian/plugins/*/main.js`), so this
repository cannot install anything on the desktop — these are the steps for
Logan's machine. **Nothing in this vault currently asserts the plugin is
installed, and nothing should until it is.**

1. **Install.** Community plugins → browse → *Full Calendar*
   (id `obsidian-full-calendar`, latest release v0.10.7). The upstream repo
   `obsidian-community/obsidian-full-calendar` is **archived and read-only** —
   it takes no further commits, so v0.10.7 is where it stays. Archived is not
   abandoned: the code is preserved and installable, and the bands here depend
   only on the DOM it emits. But nothing upstream will be fixed, so adopting it
   is a decision to accept a frozen dependency. Logan's call, not this note's.
2. **Add the calendar.** Settings → Full Calendar → add a calendar of type
   **Daily note**, with heading **`Day planner`**. Only one daily-note
   calendar can be active at a time. It requires the Daily Notes core plugin
   or Periodic Notes — both are already canon-required here.
3. **Enable the frame.** Settings → Appearance → CSS snippets → toggle on
   **named-hours**.
4. **Check the seam.** Open a daily note, add an event through the calendar,
   and confirm the list item lands under the existing `## Day planner`
   heading rather than being appended to the end of the note. Full Calendar
   appends the heading to the *bottom* of a file that lacks it, which on a
   daily note would put it below the `#phonetonote` capture tail — this is
   why the heading is seeded in `DAILY NOTE TEMPLATE.md`.

### Tuning

`--nh-band-strength` in the snippet controls how loudly the bands read behind
events; it ships at `26%`. Raise it toward `100%` for the full-saturation look
of the reference render. Set it low if the bands compete with the events.

The band labels are a separate, clearly-marked section at the foot of the
snippet — delete it for bare color bands.

### What breaks it

- **Changing `slotDuration`** away from FullCalendar's 30-minute default.
  Every `data-time` selector in the snippet is written against `:00`/`:30`
  slots and would need rewriting.
- **A plugin major version** that moves to FullCalendar v6+ or renames the
  timegrid classes. The band selectors are the coupling point; the block
  table above is not, and survives.
- **Renaming the `Day planner` heading** in the daily note without changing
  it in the plugin's calendar settings.

---

## See Also

- `.obsidian/snippets/named-hours.css` — the frame
- `!/PLUGIN-REGISTRY.md` — plugin standing and the time/workflow scope
- `DAILY NOTE TEMPLATE.md` — where the `Day planner` heading is seeded
- `VAULT-CONVENTIONS.md` — frontmatter, naming, git practice
