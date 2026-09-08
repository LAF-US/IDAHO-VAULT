# ARBORSCAPING REPORT — 2026-05-25

**Conducted by:** Bellhop (Claude Code, MacBook)
**Date:** 2026-05-25
**Scope:** Mac-side local branch census + open PR audit
**Protocol:** SALVAGE → CHERRY-PICK → PRUNE (trunk-directed convergence)

---

## Context: The Orphan History Problem

All 7 local branches are **orphan history branches** — artifacts from before the vault's
April 2026 history rewrite. They share no merge base with `origin/main`. This means:

- `git branch --merged origin/main` gives **misleading results** (some show as "merged" but
  have no actual merge base)
- `git diff origin/main...branch` fails with "fatal: no merge base"
- Correct classification requires reading **tip-commit file content** and comparing against
  trunk via `git show branch:path`

All content assessments below are provenance-grounded via direct file reads.

---

## Branch Census

### 1. `bot/daily-rollover-2026-04-24`

**Tip payload:** Adds `2026-04-24.md` (daily note rollover for April 24)
**Trunk status:** `2026-04-24.md` **IS IN TRUNK** — confirmed via `ls`
**Classification: 🟢 PRUNE candidate**
Tip payload already landed in trunk. No unique content to rescue.

---

### 2. `bot/daily-rollover-2026-04-25`

**Tip payload:** Adds `2026-04-25.md` (daily note rollover for April 25)
**Trunk status:** `2026-04-25.md` **NOT IN TRUNK**
**Classification: 🟡 SALVAGE — cherry-pick pending approval**

Content of missing note:

```markdown
- WORK: [ ] FMLA PAPERWORK
- VAULT: [ ] FIX DAILY NOTE SYNCING / CARRYFORWARD (4 sub-tasks)
```

This is a real daily note with uncompleted tasks that never reached trunk.

---

### 3. `codex/example-high-risk-pr-flow-2026-04-23`

**Tip payload:** Adds `automation-high-risk-probe-2026-04-23.md` (root level)
**Trunk status:** File **IS IN TRUNK** — confirmed via `ls`
**Classification: 🟢 PRUNE candidate**
Probe document already in trunk.

---

### 4. `codex/example-low-risk-pr-flow-2026-04-23`

**Tip payload:** Adds `.github/swarm/automation-probe-low-risk-2026-04-23.md`
**Trunk status:** File **IS IN TRUNK** — confirmed via `git show main:.github/swarm/...`
**Classification: 🟢 PRUNE candidate**
Probe document already in trunk.

---

### 5. `copilot/filter-secret-scanning-alerts`

**Tip payload:** 6 files changed — 4 workflow permission fixes, 2 Python security patches
**Trunk status:** MIXED

| File | Status |
| --- | --- |
| `.github/workflows/1password-secret-template.yml` | ✅ Permissions fix already in trunk |
| `.github/workflows/check-dotfolder-anchors.yml` | ✅ Permissions fix already in trunk |
| `.github/workflows/check-portable-paths.yml` | ✅ Permissions fix already in trunk |
| `.github/workflows/vault-propose-moves.yml` | ⬛ File removed from trunk (superseded) |
| `!/resolve_openrouter_secret.py` | ⬛ Trunk has newer version — copilot version superseded |
| `.github/scripts/wayback_audit.py` | 🟡 **UNIQUE FIX** — see below |

**The `wayback_audit.py` fix is not in trunk:**

- Trunk (line 112): `if "web.archive.org" in url:` — incomplete URL check (CodeQL alert)
- Copilot branch (lines 124–125): `parsed = urllib.parse.urlparse(url)` + exact hostname
  membership check — fixes CWE-20 py/incomplete-url-substring-sanitization

**Classification: 🟡 PARTIAL SALVAGE — cherry-pick `wayback_audit.py` fix pending approval**

---

### 6. `ingest-2026-04-24T130510Z`

**Tip payload:** Adds `!/ingest-2026-04-24T130510Z.md` + `manifest.json` update
**Trunk status:** Stub **NOT IN TRUNK** — trunk ingest stubs top out at `ingest-2026-04-23T130830Z.md`
**Classification: 🟡 SALVAGE — cherry-pick pending approval**

Content: standard system-test pipeline init stub (timestamp + source metadata).

---

### 7. `ingest-2026-04-25T124501Z`

**Tip payload:** Adds `!/ingest-2026-04-25T124501Z.md` + `manifest.json` update
**Trunk status:** Stub **NOT IN TRUNK** — same gap as above
**Classification: 🟡 SALVAGE — cherry-pick pending approval**

Content: standard system-test pipeline init stub.

---

## Open PRs (Remote)

| # | Branch | Status | Notes |
| --- | --- | --- | --- |
| #356 | `swarm-mvp-github-intake` | Open | Swarm MVP GitHub intake pipeline |
| #355 | `automation-hardening` | Open | Automation hardening |
| #354 | `update-claude-files` | Open | Claude instruction updates |
| #352 | `dependabot/...` | Open | Dependabot dependency update |

All 4 PRs are on `origin` — not touched locally. Awaiting Logan's review.

---

## Recommended Actions (Pending Approval)

### Phase 1: CHERRY-PICK (salvage unique content)

1. **`2026-04-25.md`** from `bot/daily-rollover-2026-04-25` → trunk
   - Real daily note with uncompleted tasks; absent from trunk
2. **`wayback_audit.py` urlparse fix** from `copilot/filter-secret-scanning-alerts` → trunk
   - Active CodeQL security alert (CWE-20); 3 lines affected
3. **`!/ingest-2026-04-24T130510Z.md`** from `ingest-2026-04-24T130510Z` → trunk
   - Ingest pipeline stub; sequence gap in vault record
4. **`!/ingest-2026-04-25T124501Z.md`** from `ingest-2026-04-25T124501Z` → trunk
   - Same; `manifest.json` also needs sync if applicable

### Phase 2: PRUNE (after cherry-picks confirmed)

- `bot/daily-rollover-2026-04-24` — tip payload in trunk ✅
- `codex/example-high-risk-pr-flow-2026-04-23` — tip payload in trunk ✅
- `codex/example-low-risk-pr-flow-2026-04-23` — tip payload in trunk ✅
- `bot/daily-rollover-2026-04-25` — after `2026-04-25.md` lands in trunk
- `copilot/filter-secret-scanning-alerts` — after wayback fix lands in trunk
- `ingest-2026-04-24T130510Z` — after stub lands in trunk
- `ingest-2026-04-25T124501Z` — after stub lands in trunk

**No branch deletions until Logan approves Phase 2.**

---

## Manifest / `manifest.json` Note

The ingest branches modify `manifest.json`. The trunk `manifest.json` may be out of sync
with these two ingest events. The cherry-pick of the file stubs should be paired with a
`manifest.json` reconciliation to avoid sequence gaps in the vault record.

---

*All classifications grounded in direct file reads via `git show`. No training-data inference.*
