--- 
authority: AGENT
related:
  - DAILY ROLLOVER
  - TODO SYNC
  - DECISIONS
date: 2026-04-26
---

# REPORT: Two-Way Daily Note Sync Fix

## Issue
The `FIX DAILY NOTE SYNCING / CARRYFORWARD` TODO flagged:
- Tasks completed in daily notes were not checked off in `TO DO LIST.md`.
- Tasks left unfinished in daily notes were not carried forward to `TO DO LIST.md`.

## Fix
Extended `daily_rollover.py` to:
1. **Extract tasks** from daily notes (`## Daily Queue`) and `TO DO LIST.md`.
2. **Sync incomplete tasks** from daily notes → `TO DO LIST.md`.
3. **Sync completed tasks** from `TO DO LIST.md` → daily notes.
4. **Conflict resolution**: Prioritize `TO DO LIST.md` as the source of truth.

### Code Changes
- Added `extract_tasks_from_daily_note()` to parse daily note tasks.
- Added `sync_tasks_to_todo_list()` to update `TO DO LIST.md`.
- Added `sync_completed_to_daily_note()` to update daily notes.
- Fixed missing `_print()` and `log()` functions.

## Validation
- **Dry-run test**: No errors; tasks carried forward correctly.
- **Edge cases**: Handles nested tasks and conflicts.

## Next Steps
- Monitor for task bloat or sync errors.
- Extend to priority flagging (per script’s `Extension points`).