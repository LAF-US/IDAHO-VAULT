---
created: 2026-03-24
source: commit
status: draft
verified-through: 2026-03-24
related:
- '2026-03-24'
- '2026-03-25'
- '226'
- '228'
- '726'
- '740'
- '752'
- CAN
- CSV
- ChatGPT
- Copilot
- FINDINGS
- Idaho
- Idaho Legislature
- LEFT
- LOGAN
- LSO
- Legislative Services Office
- M365
- README
- THE
- VAULT-CONVENTIONS
- budget
- website
authority: LOGAN
---
# HANDOFF: LSO Minidata Ingest Transition (2026-03-24)

**Author:** ChatGPT Codex  
**Audience:** Future repo-aware agents working under LOGAN  
**Purpose:** Preserve the verified intake contract, CSV findings, M365 automation direction, and open implementation tasks for the Idaho Legislature ingest transition.

---

## 1. VERIFIED INTAKE CONTRACT

The Idaho Legislature bill data source is now a daily email attachment from the Legislative Services Office.

- Sender: `gems@lso.idaho.gov`
- Attachment name: `minidata.csv`
- Delivery pattern: one automated email per day
- User evidence: Outlook screenshot supplied by Logan on 2026-03-24 showed messages for March 23, March 24, and March 25, 2026 with `minidata.csv` attached.

This means the repo should treat the emailed attachment as the authoritative daily input, not as a fallback export and not as a secondary artifact from a website scrape.

---

## 2. VERIFIED SAMPLE FILE FINDINGS

Three local sample files were inspected:

- `c:\Users\loganf\Downloads\minidata.csv`
- `c:\Users\loganf\Downloads\minidata (1).csv`
- `c:\Users\loganf\Downloads\minidata (2).csv`

Observed properties:

- Encoding: `cp1252` worked; `utf-8` did not.
- Header row: none.
- Logical columns: 4.
  - `bill_id`
  - `title`
  - `status`
  - `vote_result`
- Cleanup rules needed:
  - ignore one blank line per file
  - collapse 5-column rows where the fifth field is only a trailing empty string
- Bill IDs are unique per file.
- These are full snapshots, not deltas.

Snapshot counts after cleanup:

- `minidata.csv`: 726 bill rows
- `minidata (1).csv`: 740 bill rows
- `minidata (2).csv`: 752 bill rows

Delta behavior:

- March 20 -> March 23, 2026: 14 added bill IDs, 226 changed rows, 0 removals
- March 23 -> March 24, 2026: 12 added bill IDs, 228 changed rows, 0 removals

Practical conclusion:

- Ingest should treat each `minidata.csv` as the current authoritative session snapshot keyed by `bill_id`.
- Do not build the pipeline as append-only event ingestion.

---

## 3. WHAT THE FILE CAN AND CANNOT SUPPORT

The LSO minidata attachment is sufficient for:

- bill identity
- bill title
- current status / last action
- vote or result string when present
- stable daily full-session refresh

The attachment is not sufficient by itself for:

- sponsor lists
- committee history
- full action history
- rich bill-page prose

Future agents should not fabricate those missing fields. If a note already contains richer metadata from older work, preserve it. Minidata-only ingest should update the current status fields without destroying richer existing content.

---

## 4. REPO STATE AND MISMATCHES FOUND

### Old pipeline assumptions

The old implementation still assumes scrape-first:

- `.github/scripts/idaho_leg_scraper.py`
- `.github/workflows/idaho-leg-scraper.yml`
- `.github/workflows/budget-tracker-csv-export.yml`
- `.github/scripts/README-CSV-EXPORT.md`

### Path mismatch

The documented and scripted bill location is:

- `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/`

But at least some existing bill note examples currently live at vault root, for example:

- `(2023) House Bill 24.md`

This mismatch was not resolved in this session. Future agents must either:

1. confirm the canonical target is the documented `GOVERNMENTS/.../BILLS/` path and write new 2026 notes there, or
2. preserve/update legacy root-level bill notes when they already exist by exact filename.

### Digest dependency

`post_digest.py` expects bill notes to expose `last_action` in frontmatter or body-readable status text. Any replacement ingest should preserve the `last_action` field so digest generation does not break.

---

## 5. RECOMMENDED M365 AUTOMATION DIRECTION

Recommended Microsoft-side automation:

1. Outlook rule or Outlook folder routing for the LSO message.
2. Power Automate cloud flow triggered by the incoming email.
3. Save attachment to OneDrive or SharePoint intake folder with a date-stamped filename such as `minidata-2026-03-25.csv`.
4. Let OneDrive sync surface that file locally to the Windows machine.
5. Run the vault ingest script against the newest file in that intake folder.

Reasoning:

- Copilot can help create the rule and the flow.
- Power Automate should execute the actual automation.
- OneDrive sync is more robust than trying to make Outlook or Copilot write directly into the local vault path.

Do not block the repo-side ingest on Outlook automation. The first supported contract should simply be: "given a locally saved `minidata.csv`, ingest it."

---

## 6. RECOMMENDED INGEST BEHAVIOR

Future agents should build a new standalone script, for example:

- `.github/scripts/ingest_leg_csv.py`

Minimum behavior:

- accept a local CSV path
- decode with `utf-8` / `utf-8-sig` fallback and then `cp1252`
- ignore blank lines
- normalize away the trailing empty fifth column when present
- treat the file as a full current snapshot
- support `--dry-run`
- support idempotent reruns

Recommended note-writing behavior:

- create new notes for unseen bill IDs
- update existing notes conservatively
- preserve richer existing frontmatter keys like `sponsor` or `cmte` if present
- preserve rich existing body/history if present
- update at least:
  - `aliases`
  - `URL`
  - `last_action`
  - vote/result field if used
  - an ingest timestamp field

Recommended generated content for minidata-only notes:

- title as first substantive body line
- a small clearly labeled current-status block
- no invented sponsor or history data

---

## 7. OPEN TASKS LEFT UNFINISHED

No code changes were made for this transition during this session. The following work remains open:

1. Build the new CSV ingest script.
2. Decide the canonical output directory for bill notes.
3. Update or retire the old scrape-derived CSV export documentation.
4. Remove or disable obsolete automation that still re-scrapes the legislature site.
5. Decide whether `idaho_leg_scraper.py` remains as manual backfill only, or is fully retired after CSV ingest is stable.
6. Rework the Wayback path separately as an archive-preservation tool for saved article and webpage notes with `URL:` fields.

Likely delete or retire:

- `.github/workflows/budget-tracker-csv-export.yml`
- `.github/workflows/vault-ingest.yml`

Likely keep but demote to manual/backfill:

- `.github/scripts/idaho_leg_scraper.py`
- `.github/workflows/idaho-leg-scraper.yml`

---

## 8. SUGGESTED NEXT IMPLEMENTATION ORDER

1. Build `ingest_leg_csv.py` and verify it against the inspected sample files.
2. Choose and document the canonical bill-note output path.
3. Run the ingest in dry-run mode and verify creation/update counts.
4. Update docs in `VAULT-CONVENTIONS.md` and replace scrape-export guidance in `README-CSV-EXPORT.md`.
5. Remove or disable obsolete workflows.
6. Add a second-step automation later for OneDrive intake folder discovery or scheduled local ingest.

---

## 9. BOTTOM LINE

The important state change is this:

The Idaho Legislature ingest path is no longer "scrape website -> export CSV." It is now "receive authoritative LSO `minidata.csv` attachment -> date and store it -> ingest into bill notes."

Any future implementation should start from that assumption.
