---
title: BRIEF - Budget Tracker Workbook + Dashboard
created: 2026-04-02
updated: 2026-04-02
status: active
authority: LOGAN
authors:
- ChatGPT Codex
type: brief
source: budget-tracker/workbook-dashboard
related:
- '2026-04-01'
- '2026-04-02'
- CSV
- ChatGPT
- LOGAN
- README
- budget
- chain
- syntax
---
# BRIEF - Budget Tracker Workbook + Dashboard

## Summary

As of 2026-04-02, the budget tracker lane is stable with the live workbook preserved and the dashboard pipeline still manual. The minidata mail chain is the provenance source, and the two scripts serve distinct roles: one for timeline deltas and one for helper status sync only. No automation should rewrite the workbook event history without manual review.

## Workbook State

The live workbook remains [!_2026_BUDGETS.xlsx](/C:/Users/loganf/Documents/IDAHO-VAULT/!_2026_BUDGETS.xlsx). Dated snapshots are expected after meaningful changes, following the `!_2026_BUDGETS_YYYY-MM-DD.xlsx` pattern (current snapshot present: [!_2026_BUDGETS_2026-04-02.xlsx](/C:/Users/loganf/Documents/IDAHO-VAULT/!_2026_BUDGETS_2026-04-02.xlsx)). The rules are unchanged:

- `AB` is a helper status field only and may be synced by script.
- `AE` and `AG` are human-controlled current-event fields and must preserve event history; new events should push prior events down in the existing sheet style.
- No invented `AG` syntax should be introduced.

## Minidata Provenance

The vault’s dated `.msg` originals are the authoritative inputs for the minidata chain, with extracted CSVs kept as reproducible working sources (for example [MiniData File for April 01 2026.msg](/C:/Users/loganf/Documents/IDAHO-VAULT/MiniData%20File%20for%20April%2001%202026.msg) and [minidata-2026-04-01.csv](/C:/Users/loganf/Documents/IDAHO-VAULT/minidata-2026-04-01.csv)). The timeline tool [minidata_appropriations_timeline.py](/C:/Users/loganf/Documents/IDAHO-VAULT/.github/scripts/minidata_appropriations_timeline.py) reads the `.msg` originals by default; the CSVs are provenance, not automatic workbook input.

## Dashboard Export Path

Flourish upload is still manual. The documented CSV export path in [README-CSV-EXPORT.md](/C:/Users/loganf/Documents/IDAHO-VAULT/.github/scripts/README-CSV-EXPORT.md) describes scraper output, not workbook edits or event-history maintenance. Keep that distinction explicit when preparing dashboard updates.

## Risks / Drift

The largest drift risk is assuming scraper CSV exports are equivalent to the minidata mail chain or to the workbook’s event-history fields. The pipeline must not auto-apply raw minidata into `AE/AG`, and the narrative style in `AG` must not be reinvented.

## Next Focus

Use [minidata_appropriations_timeline.py](/C:/Users/loganf/Documents/IDAHO-VAULT/.github/scripts/minidata_appropriations_timeline.py) to identify deltas, then use [update_budget_tracker_from_minidata.py](/C:/Users/loganf/Documents/IDAHO-VAULT/.github/scripts/update_budget_tracker_from_minidata.py) only for `AB` helper sync. If a real event change is required, update `AE/AG` manually while preserving the prior event in the sheet’s existing history style, then generate a new dated snapshot.
