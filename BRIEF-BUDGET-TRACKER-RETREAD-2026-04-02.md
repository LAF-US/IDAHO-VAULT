---
title: "BRIEF - Budget Tracker Retread"
created: 2026-04-02
updated: 2026-04-02
status: active
authority: "LOGAN"
author: 'OpenAI Codex App Agent "BROTHER"'
partner: 'OpenAI Codex App Agent "SISTER"'
linear_id: "LAF-25"
type: brief
source: budget-tracker/retread
related:
  - LAF-25
---

# BRIEF - Budget Tracker Retread

## Summary

The April 2 budget-tracker lane exposed a distinction that now needs to be made explicit: the workbook is the human-authored canonical record, while minidata is only a source feed for status awareness and delta detection.

## What Happened

The dated `.msg` minidata chain in the vault was used as the authoritative source for snapshot comparison. Sister then applied helper-status updates to the live workbook and manually advanced `S1362` in the event-history fields. A dated April 2 snapshot was overwritten to match the changed workbook.

## What Was Misread

Two incorrect assumptions shaped the lane:

- checksum equality between the live workbook and the dated snapshot was treated as proof that the original spreadsheet structure and semantics had been respected
- helper-status alignment was treated as close to publish readiness even though Excel cached formula values and event-history semantics were not yet settled

A further caution: the script reported `83` helper-status cell updates, but that count was not independently rederived from a preserved pre-fix baseline.

## Current Verified Truth

- The minidata provenance chain is intact.
- `S1362` is the only April 2 appropriations delta.
- The recalculated April 2 snapshot renders correctly in formula-output cells.
- The live workbook still lacks cached formula values and is locked by Excel, so it may appear stale in some viewers.

## Operational Rule Going Forward

- The workbook remains human-authoritative.
- Minidata remains a feed and alerting layer.
- `AB` may be helper-synced by script.
- `AE/AG` must remain human-edited in the workbook’s existing narrative style.
- No automation should invent new event prose or silently rewrite workbook history.

## Open Decision

The next move is not another script write. It is a Logan decision about the Excel-side correction path for the live workbook and the exact publication/export routine that should follow.
