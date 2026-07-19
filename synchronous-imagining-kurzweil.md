# Plan: DOCKET.md LAF-16 edit + session commit

## Context

Previous session (GUI Claude, retiring 2026-03-29) prepared ~23 staged files on `claude/resolve-pr-conflicts` but did not commit before retiring. Gemini attempted to update DOCKET.md (change LAF-16 status from "Handoff" → "Blocked") but the edit failed. Logan handed off to this session to make that edit cleanly and close out the branch.

## Scope

1. **Edit DOCKET.md** — two changes:
   - In the `ACTIVE WORK / PROJECT-SCOPED WORK ITEMS` table: change LAF-16 status from `Handoff` → `Blocked`
   - In the `BLOCKED / PENDING LOGAN` table: add LAF-16 row

2. **Re-stage `linear-brief.yml`** — status is `MM` (staged version is partial; disk version is hardened with payload scrubbing, size limits, HMAC validation). Stage the full disk version.

3. **Un-stage conflicted-copy daily notes** — do NOT commit:
   - `2026-03-28 (Conflicted copy Laptop (IdahoPTV) 202603291001).md`
   - `2026-03-29 (Conflicted copy Laptop (IdahoPTV) 202603291001).md`

4. **Commit A — LAF-16 state + artifacts:**
   - `!/!/!/! The world is quiet here/DOCKET.md`
   - `!/!/SESSION-2026-03-29-artifacts/` (all session artifacts)
   - `!/!/SESSION-2026-03-29.md`
   - `.github/scripts/normalize_budget_data.py`
   - `deliverables.md`
   - `2026-03-29.md`, `2026-03-30.md`

5. **Commit B — workflow / guardrail / config changes:**
   - `.github/workflows/linear-brief.yml` (guardrails + security hardening)
   - `.github/workflows/vault-ingest.yml` (python → python3)
   - `.claude/settings.json` (hook fix — DECISIONS.md label)
   - `.gemini/GEMINI.md` (Linear Access Guardrail)

6. **Push branch** — `git push origin claude/resolve-pr-conflicts`

**Not in scope:** PR creation (Copilot owns PR lane per memory), merging, touching PRs #96/#102/#103.

---

## Critical file

- [!/!/!/! The world is quiet here/DOCKET.md](!/!/!/! The world is quiet here/DOCKET.md)

---

## DOCKET edits (exact)

**Change 1 — ACTIVE WORK table row:**
```
| Budget Bill Tracker Normalization    | Gemini CLI   | Handoff     | LAF-16   | First-pass normalization script + deliverables doc ready for PR. Blocked on scraper mods. |
```
→
```
| Budget Bill Tracker Normalization    | Gemini CLI   | Blocked     | LAF-16   | First-pass normalization script + deliverables doc ready for PR. Blocked on scraper mods (LAF-16). |
```

**Change 2 — BLOCKED / PENDING LOGAN table, add row:**
```
| LAF-16 — Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on wrong branch (`claude/resolve-pr-conflicts`); scraper mods needed before merge | Logan / Copilot |
```

---

## Verification

- `git diff HEAD -- "!/!/!/! The world is quiet here/DOCKET.md"` shows LAF-16 changes
- `git log --oneline -3` shows new commit on top of `190f55d`
- `git push` exits 0
