---
title: "GitHub Automation Audit — 2026-04-03"
updated: 2026-04-03
status: active
authority: "Logan Finney"
authored-by: "Claude Code (The Sentry 🧿)"
for: "GitHub Copilot (VSCode Agent)"
tags:
  - administration/audit
  - administration/github
---

# GITHUB AUTOMATION AUDIT — 2026-04-03

**For:** GitHub Copilot (VSCode Agent) — action required items flagged ⚠️
**From:** Claude Code (The Sentry 🧿)
**Branch:** `claude/friendly-cartwright` — this report travels with the branch fix

---

## EXECUTIVE SUMMARY

The entire GitHub Actions automation stack was dark. **18 workflow files + 1 composite action** referenced non-existent action versions (`@v6`, `@v7`, `@v8`). Every push, schedule, and event trigger was crashing within 5–8 seconds. This branch carries the fix. **Nothing restores until this branch merges to main.**

---

## I. THE FIX (already in this branch)

### Broken → Correct Action Versions

| Action | Was | Now |
|---|---|---|
| `actions/checkout` | `@v6` ❌ | `@v4` ✅ |
| `actions/setup-python` | `@v6` ❌ | `@v5` ✅ |
| `actions/upload-artifact` | `@v7` ❌ | `@v4` ✅ |
| `peter-evans/create-pull-request` | `@v8` ❌ | `@v7` ✅ |

**Files patched (18 workflows + 1 composite action):**
- `.github/actions/setup-vault/action.yml` ← **missed by initial grep; fixed separately**
- All `.github/workflows/*.yml` except `1password-secret-template.yml` and `pr-linear-sync.yml` (those were already correct)

**Copilot action:** Merge `claude/friendly-cartwright` to unblock everything. See history divergence issue in Section VI.

---

## II. FULL WORKFLOW INVENTORY

### Scheduled Automations ("The Chores")

| Workflow | Schedule | Purpose | Status |
|---|---|---|---|
| `idaho-leg-scraper.yml` | Daily 6:00 AM MT | Scrapes Idaho Legislature bill data | 🔴 Was dark → fixed |
| `budget-tracker-csv-export.yml` | Daily 6:30 AM MT | Exports bill data to CSV for Flourish | 🔴 Was dark → fixed |
| `vault-ingest.yml` | Daily 12:00 UTC | Ingest pipeline stub | 🔴 Was dark → fixed ⚠️ stub only |
| `daily-rollover.yml` | Daily 4:00 AM MT | Rolls incomplete to-dos forward | 🔴 Was dark → fixed |
| `sort-audit.yml` | Monday 6:00 AM UTC | Audits vault file structure | 🔴 Was dark → fixed |
| `vault-propose-moves.yml` | Monday 7:00 AM UTC | Proposes file reorganization | 🔴 Was dark → fixed |
| `wayback-audit.yml` | Monday 8:00 AM UTC | Audits URL preservation status | 🔴 Was dark → fixed |
| `branch-cleanup.yml` | Monday 9:00 AM UTC | Prunes merged/closed agent branches | 🔴 Was dark → fixed |

### Event-Driven Automations (PR Lifecycle)

| Workflow | Trigger | Purpose | Status |
|---|---|---|---|
| `auto-pr.yml` | Push to `claude/*`, `codex/*`, `gemini/*`, `copilot/*`, `perplexity/*`, `grok/*` | Create PR, classify risk, label | 🔴 Was dark → fixed |
| `auto-merge.yml` | PR labeled `auto-merge` | Enable squash auto-merge if low-risk | 🔴 Was dark → fixed |
| `review-response.yml` | PR review submitted (changes_requested or commented) | Pause auto-merge, add `review-required` label, post acknowledgment comment | 🔴 Was dark → fixed |
| `branch-cleanup.yml` | PR closed against main | Delete agent branch immediately | 🔴 Was dark → fixed |
| `linear-pr-sync.yml` | PR opened/reopened/ready/closed | Sync PR state to Linear | 🔴 Was dark → fixed |
| `levelset-closure-notify.yml` | Push touching `!/LEVELSET-*.md` | Notify when LEVELSET files ready for closure | 🔴 Was dark → fixed |
| `wayback-preserve.yml` | Push to main touching `SOURCES/`, `GOVERNMENTS/`, `TOPICS/` | Submit new URLs to Wayback Machine | 🔴 Was dark → fixed ⚠️ path issue |
| `janitor-sweep.yml` | `daily-rollover.yml` fails | Post failure alert to Linear LAF-23 + Slack | 🔴 Was dark → fixed |

### Infrastructure / Webhook

| Workflow | Trigger | Purpose | Status |
|---|---|---|---|
| `linear-webhook.yml` | `repository_dispatch: linear-webhook` | Route Linear webhook events to vault scripts | 🔴 Was dark → fixed ⚠️ gateway missing |
| `pr-linear-sync.yml` | `workflow_call` / `workflow_dispatch` only | Secondary Linear PR sync (1Password path) | ⚠️ Disabled as direct trigger; requires `OP_SERVICE_ACCOUNT_TOKEN` |
| `review-response.yml` | PR review | (see above) | — |

### Dependabot

| Ecosystem | Schedule | Relevant? |
|---|---|---|
| `github-actions` | Daily | ✅ Should catch version drift (didn't catch `@v6` — investigate) |
| `pip` | Weekly | ✅ Valid — Python scripts present |
| `npm` | Daily | ⚠️ No `package.json` — dead weight |
| `maven` | Weekly | ❌ No Java files — dead weight |

**Copilot action:** Trim `npm` and `maven` from `dependabot.yml`.

---

## III. ORDER OF AGENTIC OPERATIONS

### Standard PR Lifecycle (agent branch → main)

```
1. AGENT pushes to claude/* (or codex/*, copilot/*, etc.)
        │
        ▼
2. auto-pr.yml fires
   ├── git diff vs origin/main
   ├── classify_paths.py → risk tier (low / high)
   ├── Check for existing PR (skip if already open)
   ├── Create PR with label:
   │     low risk  → label: auto-merge
   │     high risk → label: review-required
   └── If low risk: enable auto-merge immediately
        │
        ▼
3. linear-pr-sync.yml fires (PR opened)
   └── Syncs PR state to Linear matching issue
        │
        ▼
4. CodeRabbit reviews (passive, triggers automatically on PR open)
        │
        ├── If CodeRabbit posts changes_requested / comment:
        │         ▼
        │   review-response.yml fires
        │   ├── Disable auto-merge
        │   ├── Remove label: auto-merge
        │   ├── Add label: review-required
        │   └── Post acknowledgment comment on PR
        │
        ├── If auto-merge label present + no review-required:
        │         ▼
        │   auto-merge.yml fires
        │   └── gh pr merge --squash --delete-branch --auto
        │         (waits for required checks to pass)
        │
        └── If CODEOWNERS paths touched (see Section IV):
                  ▼
            Logan's explicit approval REQUIRED before merge
```

### After PR Merge / Close

```
5. PR closed
        │
        ├── branch-cleanup.yml fires immediately → deletes agent branch
        │
        └── linear-pr-sync.yml fires (closed) → syncs closed state to Linear
```

### Daily / Weekly Background

```
Every day:
  04:00 MT → daily-rollover.yml → rolls to-dos forward
               │
               └── if FAILS → janitor-sweep.yml → alert to Linear LAF-23 + Slack
  06:00 MT → idaho-leg-scraper.yml → scrapes bills, commits minidata CSV
  06:30 MT → budget-tracker-csv-export.yml → exports CSV for Flourish
  12:00 UTC → vault-ingest.yml → ingest stub (currently placeholder)

Every Monday:
  06:00 UTC → sort-audit.yml → vault structure audit
  07:00 UTC → vault-propose-moves.yml → proposes file moves
  08:00 UTC → wayback-audit.yml → checks URL preservation
  09:00 UTC → branch-cleanup.yml (full sweep) → prunes all stale agent branches
```

---

## IV. MANUAL REVIEW CHECKPOINTS (HARD GATES)

These require **Logan's explicit action** — no automation can clear them.

### CODEOWNERS Gates (enforced if branch protection is active)

```
CLAUDE.md               → @loganfinney27 must approve
/!/                     → @loganfinney27 must approve
/.github/workflows/     → @loganfinney27 must approve  ← THIS BRANCH touches this
/.github/scripts/       → @loganfinney27 must approve
```

**Note:** `claude/friendly-cartwright` modifies `.github/workflows/` and `!/GRIMOIRE/` — both CODEOWNERS-gated. Logan's review approval is a hard requirement before merge if branch protection is active.

### PR Label Gates

| Label | Effect |
|---|---|
| `auto-merge` | Auto-merge enabled on passing checks |
| `review-required` | Auto-merge disabled; Logan must review |

`review-response.yml` automatically escalates to `review-required` when CodeRabbit requests changes.

### Publication Hard Gates (not GitHub automation — vault governance)

- JFAC audio verification: 5 quotes + speaker IDs — **Logan only**
- DECISIONS 18–21: auto-generated, require Logan confirmation
- Decision 21 (Agent Behavioral Model): ⚠️ CODE AUTHORITY review required

---

## V. ISSUES FOUND (beyond the action version fix)

### ⚠️ 1. Composite Action Missed by Initial Grep
`.github/actions/setup-vault/action.yml` still had `actions/setup-python@v6`. Used by `sort-audit.yml`, `wayback-preserve.yml`, `janitor-sweep.yml`, `linear-webhook.yml`. **Fixed in this branch.**

### ⚠️ 2. Dual Linear Sync — Collision Risk (LAF-14 known)
`linear-pr-sync.yml` and `pr-linear-sync.yml` both sync PR → Linear. The second is disabled as a direct trigger to prevent collision. But they use different secret paths:
- `linear-pr-sync.yml` → `secrets.LINEAR_API_KEY` (direct)
- `pr-linear-sync.yml` → 1Password via `OP_SERVICE_ACCOUNT_TOKEN`

`pr-linear-sync.yml` is effectively dormant until `OP_SERVICE_ACCOUNT_TOKEN` is provisioned. **Only `linear-pr-sync.yml` is doing live Linear syncs.**

### ⚠️ 3. `vault-ingest.yml` is a Stub
Hardcoded: `SOURCE=system-test`, `CONTENT=Vault ingest pipeline initialized.` This is a placeholder, not a real ingest pipeline. It runs daily, creates an `!/ingest-*.md` file with boilerplate, and commits it. **Not harmful but not useful either.**

### ⚠️ 4. Linear Webhook Gateway Not Built
`linear-webhook.yml` is ready. The gateway (Cloud Function or similar) that forwards Linear webhooks to GitHub `repository_dispatch` **does not exist**. The workflow will never fire until the gateway is built. This is part of GCP/`affable-bastion` Phase III work.

### ⚠️ 5. `wayback-preserve.yml` Path Triggers May Never Fire
Triggers only on `SOURCES/`, `GOVERNMENTS/`, `TOPICS/` directory changes. These directories may not exist or may not be actively used. Verify they exist on main.

### ⚠️ 6. Dependabot Noise (npm + maven)
No `package.json` or Maven files in this vault. Dependabot is scanning two dead ecosystems daily/weekly. Minor but clean-up worthy.

### ⚠️ 7. Branch Protection Status Unknown
CODEOWNERS is configured but only enforced if branch protection rules are active on `main`. If protection is off, CODEOWNERS is decorative. Verify in GitHub Settings → Branches → `main`.

### ⚠️ 8. History Divergence — This Branch
`claude/friendly-cartwright` has no common ancestor with remote `main` via `gh pr create`. The worktree was spawned from a diverged base. **You (Copilot) need to resolve this before a PR can be opened.** Options:
- Rebase onto current `origin/main` (preferred)
- Cherry-pick the commits onto a fresh branch from main
- Force-push with Logan's approval

**Do not merge without Logan's review.** CODEOWNERS gating applies.

---

## VI. RECOMMENDED COPILOT ACTIONS (priority order)

| # | Action | Priority |
|---|---|---|
| 1 | Resolve history divergence on `claude/friendly-cartwright` | 🔴 Urgent — blocks everything |
| 2 | Open PR for `claude/friendly-cartwright` → `main` | 🔴 Urgent — fixes all automation |
| 3 | Request Logan's review approval (CODEOWNERS) | 🔴 Urgent — required for merge |
| 4 | After merge: verify workflows resume in GitHub Actions tab | 🟡 High |
| 5 | Trim `npm` + `maven` from `dependabot.yml` | 🟢 Low — separate PR |
| 6 | Investigate why Dependabot didn't catch the `@v6` version drift | 🟢 Low |
| 7 | Verify `wayback-preserve.yml` path triggers against actual vault structure | 🟢 Low |
| 8 | Verify branch protection is active on `main` (CODEOWNERS enforcement) | 🟡 High |

---

## VII. WHAT IS WORKING (no changes needed)

- `1password-secret-template.yml` — already on correct versions ✅
- `pr-linear-sync.yml` — already on correct versions ✅ (but dormant pending 1Password setup)
- `auto-pr.yml` risk classification logic — `classify_paths.py` appears sound
- `branch-cleanup.yml` agent prefix list — matches `auto-pr.yml` branch triggers ✅
- `review-response.yml` logic — correctly pauses auto-merge on CodeRabbit feedback ✅
- `janitor-sweep.yml` → Linear LAF-23 + Slack alert chain — correct dependency on rollover failure ✅

---

*Report filed: 2026-04-03 by Claude Code (The Sentry 🧿), on Logan's direction.*
*Branch: `claude/friendly-cartwright` — travels with the workflow fix commits.*
*Linear: LAF-30*

###### [["The world is quiet here."]]
