---
title: BRIEF - Budget Tracker Exercise and Logic
created: 2026-04-03
updated: 2026-04-03
status: active
authority: LOGAN
author: OpenAI Codex App Agent "BROTHER"
partner: OpenAI Codex App Agent "SISTER"
type: brief
source: budget-tracker/exercise-logic
related:
- '2026-04-03'
- DFM
- LAF
- LAF-25
- LOGAN
- OpenAI
- budget
- chain
- legislative
---
# BRIEF - Budget Tracker Exercise and Logic

## Summary

This exercise clarified the distinction between the budget tracker as a human-authored workbook and the budget tracker as a publishable dashboard surface.

The workbook is not a generic ledger. It is a right-to-left HTML assembly system in which the human-authored cells on the right drive the public-facing display columns on the left. The automation lane therefore cannot be judged only by whether the latest status is "correct." It must also preserve the semantic role of each column and the workbook's narrative structure.

## What the Exercise Taught

Three truths emerged.

First, the live workbook [!_2026_BUDGETS.xlsx](C:\Users\loganf\Documents\IDAHO-VAULT\!_2026_BUDGETS.xlsx) is the canonical human record. It must be read closely before any derivative work is attempted.

Second, the dated `.msg` minidata chain is useful for current bill state and change detection, but it is not a substitute for the workbook's human-authored narrative fields.

Third, a publishable dashboard view is not the same thing as a workbook-maintenance workflow. The dashboard can be simplified; the canonical workbook cannot be flattened just because a simpler public view would be convenient.

## Column Logic

The original workbook's logic is anchored in the following columns:

- `A:E` are display/output columns assembled from the right-side inputs.
- `G` carries the budget family or type.
- `V` carries the Legislature URL.
- `X` carries the bill label.
- `AB` carries the helper status layer.
- `AG` carries the current action plus compacted prior history.
- `AK` carries short descriptive context.
- `AP` carries the reduction-plan percentage when present.
- `BA` carries the long DFM narrative when present.

The exercise confirmed that `D` and `E` can be repurposed in a derivative workbook only if that repurposing respects the original sources:

- `D` should become the latest update/action surface, using the current state from minidata and the last observed change date from the delta chain.
- `E` should remain a human-readable descriptive surface built from the original workbook's narrative inputs, especially `AG`, `AK`, `AP`, and `BA`.

## Where I Went Wrong

I initially failed this exercise in two ways.

I first treated the dated workbook as if it were safe to flatten into a quickpost artifact by collapsing its narrative fields down to a blunt `DATE: STATUS` form. That destroyed too much human-authored context.

I then had to go back to the untouched original workbook and reread its column roles carefully. Only then did the correct derivative rule become obvious: do not simplify by erasing meaning; simplify by reassembling the existing meaning for the dashboard surface.

## Durable Logic Going Forward

The correct automation pattern is now clearer.

- Use minidata to answer: what is the bill's latest state, and when did that state last change?
- Use the workbook to answer: how should that state be explained to a human reader?
- Keep the live workbook human-authored.
- Build simplified dashboard views only as derivatives.
- Judge success by readability and semantic faithfulness, not just by status correctness.

## Closing Reflection

The core lesson is architectural, not merely procedural.

The budget tracker is a publishing system disguised as a spreadsheet. Any future automation has to behave like a careful adapter between two worlds: machine-readable legislative status feeds and a human-readable public dashboard. If it forgets which world it is touching, it will either produce stale data or strip away meaning.
