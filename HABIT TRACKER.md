---
title: HABIT TRACKER
linter-yaml-title-alias: HABIT TRACKER
date created: Saturday, April 18th 2026, 12:00:00 am
date modified: Saturday, April 18th 2026, 12:00:00 am
authority: LOGAN
related:
  - DAILY NOTE TEMPLATE
  - TO DO LIST
---

# HABIT TRACKER

This note defines the habits.
Daily checkoffs happen in each daily note, not here.

## Daily Habits

- Morning startup and orient to live surfaces
- Review [[TO DO LIST]] and choose today's Top 3
- Advance one WORK item
- Advance one VAULT item
- Handle one PERSONAL or admin item
- End-of-day close and carryforward

## Weekly Habits

- Review the backlog and prune stale tasks
- Review inbox and captures
- Review active branches, PRs, and open loops
- Adjust the daily system if it is drifting

## Completed Habit Entries Today

```dataview
TASK
FROM ""
WHERE completed AND contains(text, "#habit") AND file.name = dateformat(date(today), "yyyy-MM-dd")
SORT completion ASC
```

## Recent Habit Completions

```dataview
TASK
FROM ""
WHERE completed AND contains(text, "#habit")
SORT completion DESC
LIMIT 20
```
