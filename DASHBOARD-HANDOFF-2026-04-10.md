---
authority: CLAUDE
date: 2026-04-10
status: needs-logan
related:
- "!_2026_BUDGETS.xlsx"
- "!_2026_BUDGETS_flourish_export_2026-04-10.csv"
- .github/scripts/update_budget_tracker_from_minidata.py
---

# Budget Tracker Dashboard Handoff — 2026-04-10

**TL;DR.** I did NOT run the live sync. The dry-run would have regressed every bill. I exported your April 9 15:41 workbook state (cached values only) to a Flourish-shaped CSV. You decide what goes to the dashboard.

## What I did

- **Read** `!_2026_BUDGETS.xlsx` with `data_only=True` (no writes).
- **Wrote** `!_2026_BUDGETS_flourish_export_2026-04-10.csv` — 351 rows, 14 unique bills, columns: `bill_id, bill_label, budget, program, agency, division, status, last_event_date, last_event_action, link, row`.
- **Did not touch** the workbook, the scraper, or any sync.

## Current unique-bill status (from workbook cache, April 9 15:41)

| Bill  | Status  |
| ----- | ------- |
| H0847 | PASSED  |
| H0848 | PASSED  |
| S1331 | PASSED  |
| S1361 | PASSED  |
| S1362 | TO GOV* |
| S1363 | PASSED  |
| S1373 | PASSED  |
| S1375 | FAILED  |
| S1380 | PASSED  |
| S1381 | PASSED  |
| S1382 | FAILED  |
| S1383 | PASSED  |
| S1384 | PASSED  |
| S1385 | PASSED  |

This reflects **your** manual updates as of April 9, not minidata.

## Why I did not run the sync

`.github/scripts/update_budget_tracker_from_minidata.py` has a latent bug: it compares minidata status to workbook status for **equality only**, never ordering. When minidata is stale (as it is — April 3) and you've manually advanced the workbook past it, the "change" it detects is actually a regression.

Dry-run from the April 3 minidata against today's workbook proposed these 10 regressions:

```
S1361:  LAW+        -> To Gov          (regression)
H0847:  LAW+        -> Pres signed*    (regression)
H0848:  LAW+        -> Pres signed*    (regression)
S1380:  LAW+        -> H PASSED*       (regression)
S1381:  LAW+        -> H PASSED*       (regression)
S1382:  H FAILED    -> H 3rd Rdg*      (regression)
S1383:  LAW+        -> H PASSED*       (regression)
S1384:  LAW+        -> H PASSED*       (regression)
S1385:  LAW+        -> H PASSED*       (regression)
S1362:  To Gov*     -> S 3rd Rdg       (regression)
```

**DO NOT run the live sync against the April 3 minidata.** It will destroy your manual work.

## What's not in this snapshot

1. **Session-end vetoes.** You said the Governor issued line-item vetoes after session end. None of that is in the workbook or any minidata we have. S1362 still shows `TO GOV*`; any of the `PASSED` bills could actually have line-item strikes. I can't fix that without the Governor's transmittal letter or a news source.
2. **Fresh minidata.** The LSO feed in the vault is from April 3 (mtime April 6 22:30). LSO blocks scraping; the feed arrives by email. You need a fresh CSV before the sync script is useful again.
3. **The 69 missing Approp bills.** Minidata has 83 Approp bills; workbook has 14. The gap is research (DFM Agency Reduction Plans, JFAC motions), not an auto-fill task.

## What you should do next

**If Flourish reads a manual CSV upload:**
1. Open `!_2026_BUDGETS_flourish_export_2026-04-10.csv`.
2. Apply any known veto overrides by hand.
3. Upload to Flourish Studio.

**If Flourish reads a live data connection:**
1. The workbook's cached values are what Flourish will serve. Your April 9 15:41 save is already live-ish, minus vetoes.
2. Open the workbook, apply veto overrides in column BB (`STATUS_OVERRIDE`), save. Flourish will pick it up on next refresh.

**Before next minidata sync (either flow):**
1. Fix `update_budget_tracker_from_minidata.py` to refuse writes that would move a bill's status backward in the progression `INTRODUCED → ADVANCED → TO_GOV → PASSED/FAILED`. Or gate the whole script behind a manual confirmation when the minidata is more than N days old.
2. Get a post-April-9 minidata CSV into the vault.

## Files

- `!_2026_BUDGETS_flourish_export_2026-04-10.csv` — the export (vault root, gitignored alongside the workbook)
- `!_2026_BUDGETS.xlsx` — untouched, April 9 15:41
- This note — `DASHBOARD-HANDOFF-2026-04-10.md`

-Claude
