---
title: Big IFs — Budget Tracker 2026
updated: 2026-04-11
status: filed
authority: claude
doc_class: misc_reference
template_id: tpl-misc-reference-v1
source: Claude Code session 2026-04-10 → 2026-04-11 (pre-archive)
related:
- "2026-04-10"
- "2026-04-11"
- Big IFs
- "!_2026_BUDGETS.xlsx"
- "!_2026_BUDGETS_flourish_export_2026-04-10.csv"
- DASHBOARD-HANDOFF-2026-04-10
- Approp
- Flourish
- JFAC
- LSO
- minidata
- budgets
- sync
- dashboard
- Governor
- veto
- line-item veto
- Agency Reduction Plans
---

# Big IFs — Budget Tracker 2026

**Source:** Claude Code (The Abhorsen), single session 2026-04-10 → 2026-04-11
**Filed by:** Claude on branch `codex/live-state-snapshot`
**Trigger:** "PREPARE to be ARCHIVED — RECORD AND REPORT all Big IFs into the CANONICAL LEDGER"
**Scope:** Everything learned during the Approp-only filter, minidata↔workbook comparison, subtype taxonomy, and aborted dashboard sync.

This is a pre-archive dump. The conversation window is about to be closed, stored, and eventually deleted. What's here is what I want a future Claude (or Logan) to be able to recover.

---

## 1. The Canonical Convention

**"Approp bills" = minidata rows whose title field starts with the literal string `Approp,`.**

- Verified against `minidata-2026-04-01.csv`: 73 rows (April 1 snapshot); 83 rows in the April 3 snapshot.
- This is a NAMING convention, not a structured flag. There is no `type` column in minidata.
- **`H Approp` in the status column is unrelated** — it means the bill currently sits in House Appropriations committee, not that the bill itself is an appropriation.
- **There is no `Supp approp,` or `Trustee,` prefix in LSO minidata.** Supplementals are marked inside the `Approp,` title itself (e.g. `"Approp, PERSI, add'l"`, `"Approp, H&W, medicaid, add'l"`). I confabulated those prefixes from an AskUserQuestion option on 2026-04-10; Logan caught it; feedback memory `feedback_verify_conventions.md` now exists to prevent the replay.

## 2. The Subtype Taxonomy (5-bucket)

Logan defined and I adopted:

1. **FY26 Supplemental** — current-year add-ons (closes gaps in the year already in progress).
2. **FY26 Reduction** — current-year cuts (Agency Reduction Plans, DFM-authored).
3. **FY27 Maintenance** — upcoming-year base (continuing operations).
4. **FY27 Enhancement** — upcoming-year new money / expansions.
5. **Trailer (Policy Bill Pay-For)** — policy bills that move money as a byproduct, filed alongside the companion policy measure.

**Session calendar rule (Logan, verbatim):** *"In a GIVEN SESSION, the Legislature is setting MAINTENANCE & ENHANCEMENT for the UPCOMING year (FY27 here) with optional SUPPLEMENTAL & REDUCTION for the CURRENT year (FY26 here)."*

**Idaho fiscal year** = July 1 – June 30. Session runs ~January–March/April.

**Caveat surfaced mid-session:** single-FY classification by title alone is insufficient. S1433 (H&W Medicaid) is a split-FY bill covering both FY26 and FY27, discoverable only from the LSO bill page — the minidata title `Approp, H&W, medicaid, add'l` does not encode that.

## 3. Workbook Architecture (`!_2026_BUDGETS.xlsx`)

- **Shape:** 352 rows × 53+ columns. Gitignored. Local-only. Apr 9 15:41 is the last save.
- **Assembly pattern:** right-to-left. Columns A–E are TEXTJOIN formulas assembling a Flourish-shaped display. Columns F+ are source/HTML fragments and event history.
- **Source columns:** G=BUDGET, J=PROGRAM, N=AGENCY, R=DIVISION, V=LINK, X=BILL, AB=STATUS (formula), AE=DATE, AG=DESCRIPTION, BB=STATUS_OVERRIDE, BA=DFM_TEXT.
- **Event history:** AE/AG is the newest event; AH/AI, AJ/AK, … AT/AU are older events shifted rightward on each sync. 8 slots total.
- **Column AB is a FORMULA.** Do not write to it. Use BB (`STATUS_OVERRIDE`) instead.
- **Column E (`Status (Simplified)`) is plain text,** written directly by the sync script.
- **openpyxl `data_only=True` returns `None` for A–D** because Excel calculates on open; openpyxl does not. The source columns (G/J/N/R/V/X/AE/AG/BB) have real cached values and are the safe read surface.
- **S1331 has 108 rows.** Not data bloat. Each row = one agency impact line from the **DFM Agency Reduction Plans** PDF. One bill → many rows by design.
- **14 unique bills populated** (as of 2026-04-09 save): H0847, H0848, S1331, S1361, S1362, S1363, S1373, S1375, S1380–S1385.
- **69 Approp bills in minidata are missing from the workbook.** Those are research tasks (transcribing JFAC motions / DFM plans), not auto-fill gaps.

## 4. The Sync Script Regression Bug (CRITICAL)

**File:** `.github/scripts/update_budget_tracker_from_minidata.py`
**Lines:** ~180–185 (the `if current_date == snapshot_date and current_summary == raw_status: continue` block, and its `else` branch).

**The bug:** The script compares workbook status to minidata status for **equality only**. It has no concept of status ordering. When minidata is stale and the workbook has been manually advanced past it, the script detects "a change" and writes the stale value, regressing the workbook.

**What I almost did on 2026-04-10:** Ran a dry-run that reported `37 row_changes, 0 strays`. Looked clean. It was not. Every single change was a regression. The script passed its own checks because its checks don't model time.

**The 10 proposed regressions from the aborted 2026-04-10 dry-run (April 3 minidata vs April 9 workbook):**

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

**The fix (not yet implemented):** Status-lattice with a "never move backward" rule. Something like:

```
INTRODUCED < ADVANCED < TO_GOV < PASSED
                                \ FAILED  (terminal)
```

Or: gate the whole script behind a manual `--i-have-fresh-minidata` confirmation when `minidata.mtime` is more than N days old.

**The other fix I did implement on 2026-04-10:** Approp-only gate in `load_minidata_rows()`, plus `find_stray_non_approp_rows()` read-only audit. Filter is active; 83 Approp bills load from minidata; 0 strays in the workbook.

## 5. The Dashboard Handoff (Apr 10 artifacts)

- **`!_2026_BUDGETS_flourish_export_2026-04-10.csv`** — 351 rows, 14 unique bills, cached from Apr 9 15:41 workbook save. Non-destructive pure read. Status priority: `BB override > E cached > simplified(AG)`.
- **`DASHBOARD-HANDOFF-2026-04-10.md`** — vault-root handoff note documenting the regression risk, the two-branch decision tree (manual CSV upload vs live data connection), and what's missing.
- **Status distribution at Apr 9:** `PASSED: 166, INTRODUCED: 148, FAILED: 15, TO GOV*: 10, WITHDRAWN: 1, MOTION FAILED: 1, '-': 10`.
- **Unique-bill status table** — see DASHBOARD-HANDOFF-2026-04-10.md §"Current unique-bill status".

## 6. What's NOT In the Snapshot (known gaps)

1. **Session-end governor's line-item vetoes.** The Governor issued them after session adjournment. None are in any minidata or the workbook. S1362 still shows `TO GOV*`; any `PASSED` row could have line-item strikes. Requires the Governor's transmittal letter or a news source.
2. **Post-April-3 minidata.** LSO blocks fetch-scraping. Minidata arrives by email as `.msg` attachments. The vault's freshest is Apr 3 (mtime Apr 6 22:30). The `budget-tracker-csv-export.yml` workflow that uses the scraper is broken; manual Flourish upload is the documented fallback.
3. **The 69 missing Approp bills.** Research task, not a data gap.
4. **Flourish delivery mechanism** — Logan did not confirm whether Flourish uses manual CSV upload (path a) or a live data connection (path b). Default action taken: export CSV anyway (costs nothing in path a, harmless in path b).

---

## Big IFs (the real ones)

### IF 1 — Time-Aware Sync

**IF** the sync script models status-ordering as a lattice with a "never move backward" rule, then **Logan can run it safely even when minidata is stale**, because regressions become errors instead of silent overwrites. This is the single highest-leverage fix to this pipeline. Without it, every future sync is a coin flip between "helpful update" and "destroyed manual work."

### IF 2 — Unified Status Provenance

**IF** the workbook tracks per-field provenance (which source wrote which value: LSO minidata, DFM plan, news story, governor's office, Logan by hand), then **conflict resolution becomes a first-class operation** instead of an accident of last-writer-wins. Right now the workbook has no memory of where any given cell came from; that's why the April 3 minidata sync looked like an "update" when it was actually a rollback of Logan's Apr 9 manual work.

### IF 3 — Veto-Aware Data Model

**IF** the tracker distinguishes `PASSED (whole)` from `PASSED (with line-item strikes)` at the data model level, then **the dashboard can honestly represent a post-session Idaho budget**, where the governor's pen has shaped final appropriations in ways the bill status field alone cannot express. Today, every `PASSED` bill in the export is a potential lie until the vetoes are applied.

### IF 4 — Approp Classifier Beyond Title-String

**IF** classification draws on the LSO bill page (and its "Relates to the appropriation to X for fiscal year(s) Y") instead of the minidata title alone, then **split-FY bills like S1433 stop getting miscategorized**, and the Trailer bucket (policy-bill pay-fors) can be populated without manual curation. Minidata title is a cheap heuristic; the LSO page is the ground truth. LSO blocks scraping, so this IF requires either a cached LSO snapshot layer or a human-in-the-loop transcription pass.

### IF 5 — Agency Reduction Plans as a Structured Source

**IF** the DFM Agency Reduction Plans PDF is parsed once into a structured agency×FY×amount table, then **S1331's 108-row expansion becomes reproducible and auditable** instead of a one-shot hand-transcription whose provenance nobody can reconstruct six months from now. Same pattern applies to any future reduction bill.

### IF 6 — Dashboard Delivery as First-Class Infrastructure

**IF** the Flourish delivery mechanism (manual upload vs live connection) is documented in `CLAUDE.md` / `AGENTS.md` / wherever agents actually read, then **agents stop having to ask Logan at the worst moment** ("dashboard needs update NOW" → "first, how does the dashboard work?"). Today this knowledge lives only in Logan's head and in a `README-CSV-EXPORT.md` that describes a broken workflow.

### IF 7 — The Verify-Before-Plan Discipline

**IF** every plan that hardcodes a string, prefix, field name, or path has a verification step against the actual source file **before** ExitPlanMode, then **I stop confabulating plausible-sounding conventions** like "Supp approp," / "Trustee,". This is already written into `feedback_verify_conventions.md`. Surfacing it here in the ledger so the discipline survives this window's archival.

---

## Findings (terse)

- **F1:** `Approp,` title prefix is the only appropriations signal in LSO minidata. Everything else is confabulation.
- **F2:** openpyxl `data_only=True` silently returns `None` for uncalculated formulas — never trust the display columns as a safe read surface; go to the source columns.
- **F3:** `update_budget_tracker_from_minidata.py` passes its own checks while destroying manual work. Check success ≠ operational safety.
- **F4:** The workbook is the integration point for at least four data sources (LSO minidata, DFM plans, news, governor's office). Minidata is one signal, not ground truth.
- **F5:** S1331's 108 rows are the DFM Agency Reduction Plans rendered as per-agency impact lines. This is architecture, not bloat.
- **F6:** S1433 (H&W Medicaid) covers both FY26 and FY27. Single-FY classification by minidata title alone is unsafe for any split-FY bill.
- **F7:** Logan has been manually advancing workbook status from non-minidata sources. Those manual updates are AHEAD of the stale minidata snapshot, which is why the April 3→April 9 sync would regress every bill.
- **F8:** Column AB is a formula; column BB is the writable override slot; column E is plain text written directly by the sync script. Three different kinds of status live in the same workbook.
- **F9:** The governor issued line-item vetoes after session sine die. None of them are in the vault as of this filing.
- **F10:** The LSO scraper path is blocked; minidata arrives by email as `.msg` attachments. The `budget-tracker-csv-export.yml` workflow is broken by design, not accident.

---

## Snapshots (pointers, not copies)

- **Workbook:** `!_2026_BUDGETS.xlsx` (Apr 9 15:41 save, gitignored)
- **Export:** `!_2026_BUDGETS_flourish_export_2026-04-10.csv` (Apr 10, 351 rows, gitignored alongside workbook)
- **Handoff note:** `DASHBOARD-HANDOFF-2026-04-10.md` (vault root)
- **Fresh-ish minidata:** `minidata-2026-04-01.csv` / April 3 snapshot (vault root; email-sourced)
- **Sync script:** `.github/scripts/update_budget_tracker_from_minidata.py` (Approp filter LIVE, regression bug LIVE)
- **Timeline script:** `.github/scripts/minidata_appropriations_timeline.py` (hardcoded TRACKED_BILLS; 14 entries; all audited Approp-valid)
- **Broken workflow:** `.github/workflows/budget-tracker-csv-export.yml` + `README-CSV-EXPORT.md`
- **Plan artifact:** `C:\Users\loganf\.claude\plans\quiet-hugging-simon.md` (approved 2026-04-10, Approp-only filter plan)
- **Feedback memory:** `feedback_verify_conventions.md` (created 2026-04-10 after confabulation incident)
- **Conversation transcript:** `C:\Users\loganf\.claude\projects\C--Users-loganf-Documents-IDAHO-VAULT\675b2557-7e98-4a6c-9795-be2262cc9825.jsonl`

---

## Orientation Notes for the Next Claude

If a future Claude picks up this thread after the window is archived:

1. **Read this file first, then `DASHBOARD-HANDOFF-2026-04-10.md`, then `feedback_verify_conventions.md`.** Those three reconstruct most of the session.
2. **Do not run `update_budget_tracker_from_minidata.py` against stale minidata.** Fix the regression bug first (IF 1) or require Logan's explicit "go" per run.
3. **Treat minidata as one signal among several, not as ground truth.** Logan has been manually updating the workbook from news and governor's office.
4. **The Approp-only filter is LIVE and working.** Do not re-implement it. Do not widen it. 83 Approp bills is the correct load count.
5. **Do not touch columns A–D in the workbook** — they're TEXTJOIN formulas. Source columns are G/J/N/R/V/X; override slot is BB; plain-text simplified status is E.
6. **Before writing any plan that hardcodes a convention, grep the source.** Empty grep means "doesn't exist," not "pre-build for later."
7. **Vetoes are the unknown unknown.** Until the governor's transmittal letter is in the vault, every `PASSED` bill is provisional.

---

*Filed by Claude (The Abhorsen) · branch `codex/live-state-snapshot` · 2026-04-11 · pre-archive*
