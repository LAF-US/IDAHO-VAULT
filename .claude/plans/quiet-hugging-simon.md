# Plan: Restrict Budget Tracker to "Approp," Bills Only

## Context

**Directive:** "Only 'Approp,' bills are the budgets."

The `!_2026_BUDGETS.xlsx` tracker was built from a broader set of legislative bills, but Logan's rule is that only true appropriations bills belong there. In the minidata CSV feed, DFM/LSO marks appropriations bills by starting the **title** field with the literal string `Approp,` (e.g. `"Approp, jud branch, FY 2027 maint"`, `"Approp, PERSI, add'l"`). This is a naming convention, not a structured flag.

Examples from `minidata-2026-04-01.csv`:
```
H0847,"Approp, jud branch, FY 2027 maint",LAW+,
H0868,"Approp, PERSI, add'l",LAW+,
H0919,"Approp, perm bldg fund, orig",LAW+,
```

Note: `H Approp` appearing in the **status** column is unrelated — it just means a bill currently sits in House Appropriations committee. That is NOT the signal we filter on.

## Current Filtering State

**None.** `update_budget_tracker_from_minidata.py:167-169` extracts bill IDs from workbook columns V (URL) and X (label), then syncs whatever matches in minidata. Non-Approp bills are treated identically to Approp ones. The timeline script (`minidata_appropriations_timeline.py`) uses a hardcoded `TRACKED_BILLS` list that mixes Approp and non-Approp — it was never the enforcement point.

## Approach

Add a single filter gate at the **sync script** level (`update_budget_tracker_from_minidata.py`), keyed on `title.startswith("Approp,")` from the minidata row.

**Verified against `minidata-2026-04-01.csv`:** 73 rows have titles beginning with `Approp` — that is the ONLY appropriations convention actually present in LSO's minidata feed. There is no `Supp approp,` or `Trustee,` prefix; supplementals are marked inside the `Approp,` title itself (e.g. `"Approp, PERSI, add'l"`, `"Approp, OITS, add'l"`), and trustee/benefit payments use other title patterns that are not part of the budget tracker. A single-prefix filter is sufficient.

Rationale:

- **Minidata is the authoritative source.** The rule lives closest to the data that defines it.
- **The workbook stays canonical.** We do not delete human-authored rows; we only refuse to sync non-Approp bills going forward.
- **Dashboard inherits automatically.** Downstream exports read the workbook; if workbook events for non-Approp bills stop advancing, the dashboard naturally drops them without an additional filter.

## Implementation

### File: `.github/scripts/update_budget_tracker_from_minidata.py`

**Change 1 — Add Approp gate in `load_minidata_rows` (line ~100):**

Only load rows where `title.startswith("Approp,")`. Every downstream lookup (`minidata_rows[bill_id]` at line 168) then naturally misses non-Approp bills, and they get skipped by the existing `if not bill_id or bill_id not in minidata_rows: continue` guard at line 168 — no second code path needed.

```python
def load_minidata_rows(path: Path) -> dict[str, tuple[str, str, str]]:
    rows: dict[str, tuple[str, str, str]] = {}
    with path.open("r", encoding="cp1252", newline="") as handle:
        for row in csv.reader(handle):
            if not row or len(row) < 3:
                continue
            bill_id = row[0].strip().upper()
            if not bill_id:
                continue
            title = row[1].strip()
            if not title.startswith("Approp,"):  # NEW: Approp-only gate
                continue
            status = row[2].strip()
            vote = row[3].strip() if len(row) > 3 else ""
            rows[bill_id] = (title, status, vote)
    return rows
```

**Change 2 — Surface the filter in the summary print (line ~232):**

Add `print(f"approp_only_filter: active ({len(minidata_rows)} approp bills loaded)")` so dry-run output makes the constraint visible.

### File: `.github/scripts/minidata_appropriations_timeline.py`

**No code change** — it already only walks the hardcoded `TRACKED_BILLS`. But run a **read-only audit**: check each entry in `TRACKED_BILLS` (lines 9-24) against `minidata-2026-04-01.csv` and flag any whose title does not start with `Approp,`. Report to Logan; do not modify without sign-off.

### Workbook disposition

Logan's read: "there shouldn't be any" non-Approp rows in `!_2026_BUDGETS.xlsx`. We will **audit first, not assume**:

**Pre-flight audit (read-only):** Walk the workbook, extract each row's bill ID (V/X columns), look it up in minidata, and print any row whose title does NOT start with `Approp,`. This is additive to the dry-run output — call it `stray_non_approp_rows: [bill_id, ...]`.

- If the audit prints zero strays → the filter is purely forward-looking; nothing to clean up.
- If the audit prints some → Logan decides per-row what to do. The sync script does NOT delete or modify them automatically (narrative columns AG/AK/BA are human-authored).

## Critical Files

- `.github/scripts/update_budget_tracker_from_minidata.py` — ADD Approp filter (line ~109)
- `.github/scripts/minidata_appropriations_timeline.py` — AUDIT `TRACKED_BILLS` (read-only)
- `!_2026_BUDGETS.xlsx` — NOT modified by this plan; non-Approp rows remain for Logan to prune
- `minidata-2026-04-01.csv` — source of truth for Approp designation

## Verification

1. **Dry-run:** `python .github/scripts/update_budget_tracker_from_minidata.py --dry-run`
   - New `approp_only_filter: active (N approp bills loaded)` line appears
   - New `stray_non_approp_rows: [...]` line appears (expected empty per Logan)
   - `row_changes` count is ≤ prior baseline
   - Every bill in the change report has a title starting with `Approp,`
2. **TRACKED_BILLS audit:** Print each entry's title from minidata; flag any whose title does not start with `Approp,`.
3. **Gate:** Do not run the live (non-dry) sync until Logan confirms the dry-run output — in particular the `stray_non_approp_rows` list.

---

Status: **Ready for approval.**
