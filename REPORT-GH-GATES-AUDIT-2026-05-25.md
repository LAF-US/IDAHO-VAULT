---
title: GitHub Gates and Checks Audit — 2026-05-25
updated: 2026-05-25
status: active
authority: Logan Finney
authored-by: Claude Code
related:
- CLAUDE
- GitHub
- AGENTS
- REPORT-GH-AUTOMATION-TRIAGE-2026-05-25
- REPORT-GH-AUTOMATION-AUDIT-2026-04-03
---
# GITHUB GATES AND CHECKS AUDIT — 2026-05-25

**From:** Claude Code (Windows session)
**Branch:** `agent/triage-scripts-2026-05-25`
**Companion:** `REPORT-GH-AUTOMATION-TRIAGE-2026-05-25.md` (scripts/workflows triage)
**Feeds into:** Claude–Codex Security Collaboration Proposal (same session)

---

## I. CONFIRMED STATE

```
gh api graphql branchProtectionRules → nodes: []
```

Zero branch protection rules on `main`. Repository-level settings:

| Setting | Value |
| --- | --- |
| `allow_auto_merge` | `true` |
| `delete_branch_on_merge` | `true` |
| `allow_squash_merge` | `true` |
| `allow_merge_commit` | `true` |
| `allow_rebase_merge` | `true` |

Auto-merge is enabled as a repository feature. Without required checks configured, `gh pr merge --auto` fires as soon as it is called — there is nothing for it to wait on.

---

## II. WHAT "GATES" ACTUALLY MEANS IN THIS REPO

There are two categories of gate in this vault. Understanding the distinction is essential before any remediation:

**Advisory gates** — run and report; pass or fail visibly; cannot block a merge. All current gates are advisory.

**Enforced gates** — required status checks that GitHub refuses to bypass. Currently: none.

The entire review/merge/risk-classification pipeline is advisory. It functions as a social coordination system: agents follow the rules because the rules exist, not because GitHub enforces them.

---

## III. THE PR LIFECYCLE — HOW IT WORKS

### For agent branches (`claude/*`, `codex/*`, `gemini/*`, `copilot/*`, `perplexity/*`, `grok/*`, `serena/*`)

```
1. Agent pushes to qualifying branch prefix
        │
        ▼
2. agent-auto-pr.yml fires (trigger: on: create)
   ├── classify_paths.py reads changed files vs origin/main
   │     risk/low  → label: risk/low + review/pending
   │     risk/high → label: risk/high  (no auto-merge path)
   └── Creates PR; logs "30-minute grace period"
        │
        ▼
3. agent-review-gate.yml (schedule: every 4 hours)
   ├── review_feedback_loop.py reconcile-open-prs
   │     For each open low-risk PR:
   │       - Grace period elapsed? (default 30 min)
   │       - No blocking review labels?
   │       - No open threads?
   │       → promote: remove review/pending, add merge/auto
   │
   ├── pr_loop_watchdog.py — generates findings report
   └── issue_reconciler.py — syncs findings to a recurring GitHub Issue
        │
        ▼
4. auto-merge.yml fires (trigger: PR labeled merge/auto)
   └── review_feedback_loop.py enable-auto-merge
         ├── Final derived-state check
         └── gh pr merge --auto --squash --delete-branch
              (fires immediately — no required checks to wait for)
        │
        ▼
5. review-response.yml (trigger: pull_request_review submitted)
   └── review_feedback_loop.py review-submitted
         ├── Non-author changes_requested → add review/required
         │   remove merge/auto, block merge path
         └── Approved → recompute, may re-promote

6. review-feedback-loop.yml (trigger: issue_comment, PR events)
   ├── acknowledge-apply: "@copilot apply changes" → add merge/copilot-apply-pending
   ├── sweep-review-threads: after PR update, auto-resolve outdated advisory threads
   └── verify-claim: IF 7 — if an agent says "ready to merge" in a comment,
         compare claim against actual GitHub state (mergeable, mergeStateStatus,
         draft, check rollup); post divergence note if claim is wrong
```

### For `agent/*` branches (current Claude Code convention)

`agent-auto-pr.yml` branch pattern does not include `agent/*`. These branches receive no auto-PR. PRs must be opened manually. This is either intentional (Logan opens PRs for Claude's work after review) or an oversight from before `agent/` was adopted as a naming convention.

### For Dependabot PRs

```
1. Dependabot opens PR for pip or github-actions ecosystem
        │
        ▼
2. dependabot-rhythm.yml (trigger: pull_request_target opened)
   ├── dependabot/fetch-metadata → reads update-type, package-ecosystem
   ├── If pip/uv/github-actions AND semver-patch/minor:
   │     gh pr review --approve
   │     add label: dependabot/low-risk-auto  ← proof label
   │     gh pr merge --auto --squash --delete-branch
   └── Else: no action (waits for manual handling)
        │
        ▼
3. dependabot-reaper.yml (schedule: every 2 hours)
   └── Re-arms auto-merge for any qualifying PR that was missed
         (batch-event race condition mitigation — see idaho-vault-race-conditions)
```

---

## IV. LABEL TAXONOMY

The gate system uses a coherent label vocabulary. All labels are created by `review_feedback_loop.py ensure-labels`.

| Label | Color | Meaning |
| --- | --- | --- |
| `risk/low` | Green | Only low-risk paths changed |
| `risk/high` | Red-pink | At least one high-risk path changed |
| `review/pending` | Light blue | Low-risk PR in grace period; not yet eligible for auto-merge |
| `review/required` | Red | Blocking review state; auto-merge paused |
| `review/threads-open` | Yellow | Unresolved review threads |
| `merge/auto` | Green | Grace period elapsed; armed for auto-merge |
| `merge/copilot-apply-pending` | Purple | Waiting on Copilot follow-up push |
| `dependabot/low-risk-auto` | Dark green | Dependabot metadata proved patch/minor eligibility |

---

## V. RISK CLASSIFICATION — `classify_paths.py`

The classifier is the heart of the gate system. It reads changed file paths from stdin and outputs a JSON tier decision.

**Rule:** If ANY file is high-risk, the entire PR is high-risk.

**High-risk exact matches:**

```
AGENTS.md, CLAUDE.md, CONSTITUTION.md, DECISIONS.md, LEVELSET.md,
VAULT-CONVENTIONS.md, swarm.json, .gitignore, .github/CODEOWNERS,
.github/copilot-instructions.md
```

**High-risk prefixes:**

```
!/          .github/workflows/          .github/scripts/
```

**Low-risk prefixes:**

```
SOURCES/    TOPICS/     PEOPLE/     PLACES/
ORGANIZATIONS/  GOVERNMENTS/    ATTACHMENTS/
.github/swarm/  !/swarm/
```

**Probe/example override (low regardless):**

```
.github/workflows/probe-*   .github/workflows/example-*
.github/scripts/probe-*     .github/scripts/example-*
```

**Default for unknown paths: high-risk (fail-safe)**

**Implications:**

- Daily notes (`2026-05-25.md` at repo root) → unknown → high-risk → manual review required
- The `!/` prefix covers all NEST files — any change to `!/` is high-risk
- The high-risk default means agents touching anything outside the listed low-risk prefixes always produce manual-review PRs
- This is intentional: the vault's content surfaces are not low-risk by default

---

## VI. PER-WORKFLOW FINDINGS

### `agent-auto-pr.yml` — Auto PR for Agent Branches

**Status:** Working correctly for covered prefixes.
**Finding:** `agent/*` not in pattern. Branches named `agent/` get no auto-PR.
**Script deps:** `classify_paths.py`, `review_feedback_loop.py ensure-labels`, `pr_lifecycle.py`

---

### `agent-review-gate.yml` — PR Review Gate (scheduled reconciler)

**Status:** Working correctly.
**Runs:** Every 4 hours + `workflow_dispatch`.
**Finding:** Grace period is 30 minutes by default but the reconciler only runs every 4 hours. A PR that passes its grace period at minute 31 may wait up to 4 hours before being promoted. This is known and acceptable — the gate is conservative by design.
**Script deps:** `review_feedback_loop.py reconcile-open-prs`, `pr_loop_watchdog.py`, `issue_reconciler.py`
**Notable:** The `action_required` sweep (IF 8 from ARBORSCAPE) appends to the watchdog report rather than creating a separate issue — correct pattern.

---

### `auto-merge.yml` — Auto Merge on Label

**Status:** Working correctly given current repo settings.
**Finding:** With no required checks, `gh pr merge --auto` fires immediately. The merge is instant, not gated on check completion. This is the intended behavior for low-risk PRs under the current (unprotected) configuration. Under branch protection, `--auto` would wait for required checks.
**Trigger:** `pull_request_target` — correct for elevated-permission workflows.

---

### `review-response.yml` — Agent Review Response

**Status:** Working correctly.
**Finding:** None. Correctly delegates to `review_feedback_loop.py review-submitted`, which only pauses auto-merge when a *non-author* submits changes_requested — author self-review doesn't block.

---

### `review-feedback-loop.yml` — Review Feedback Loop

**Status:** Working correctly.
**Notable features:**

- `verify-claim` (IF 7): watches PR comments for agent completion claims (`"ready to merge"`, `"CLAUDE COMPLETE"`, etc.); compares against GitHub institutional state; posts divergence note if claim is wrong. Addresses brass-mouth reliability per ARBORSCAPE.
- `KNOWN_NOISE_CHECKS`: `submit-pypi` and `Automatic Dependency Submission (Python)` excluded from check rollup — correct, these are GitHub auto-generated noise not related to vault logic.
- `VERIFY_CLAIM_MARKER = "<!-- verify-claim:1 -->"` prevents recursive re-posting on its own divergence comments.

---

### `secret-pattern-policy.yml` — Secret Pattern Policy (per-push)

**Status:** Working correctly.
**Trigger:** PR + push to main.
**Finding:** Correctly uses `trusted-main` checkout pattern — reads the validator from the base branch, not the agent branch, preventing a compromised agent branch from disabling its own check.
**Hash note:** Uses standard `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4`.

---

### `secret-pattern-full-scan.yml` — Secret Pattern Full Scan (weekly)

**Status:** Working correctly; one inconsistency.
**Finding:** Uses `actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5` — no version comment, different hash from the vault standard (`11bd71901bbe5b1630ceea73d27597364c9af683 # v4`). Likely a Dependabot update that hit only this file. Functionally harmless; inconsistent with the pinning standard.

---

### `large-file-policy.yml` — Large File Policy (per-push)

**Status:** Working correctly.
**Trigger:** PR + push to main.
**Finding:** Same trusted-main checkout pattern as secret-policy. Correct.

---

### `large-file-watchdog.yml` — Large File Watchdog (weekly)

**Status:** Working correctly; one inconsistency.
**Finding:** Uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6` (newer) vs. the vault's established `@a26af69be951a213d495a4c3e4e4022e16d87065 # v5` standard. From a partial Dependabot update.

---

### `check-portable-paths.yml` — NETWEB Path Portability

**Status:** Working correctly.
**Finding:** Uses `set +H` to disable bash history expansion — important because vault paths contain `!`. Correct. Trusted-main checkout pattern. Correct.

---

### `check-dotfolder-anchors.yml` — Dotfolder Anchor Check

**Status:** Working correctly.
**Finding:** Uses `setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6` — same version inconsistency as large-file-watchdog.

---

### `validate-daily-notes.yml` — Daily Notes Placeholder Check

**Status:** Working correctly.
**Finding:** Inline bash; no Python dependency; checks only `YYYY-MM-DD.md` at repo root and `TO DO LIST.md`. Complementary to (not redundant with) `validate_content.py` which now runs on agent branches via `validate-agent-content.yml`.

---

### `codeql.yml` — CodeQL Advanced

**Status:** Working correctly.
**Scans:** `actions` (workflow YAML) + `python` (scripts).
**Finding:** Has `concurrency` group to prevent duplicate runs on the same SHA — correct. Runs on push to main, PRs targeting main, and weekly schedule. Security scan results post to GitHub Security tab. Without branch protection, CodeQL findings are visible but not blocking.

---

### `dependabot-rhythm.yml` + `dependabot-reaper.yml`

**Status:** Working correctly as a pair.
**Finding:** The proof-label pattern (`dependabot/low-risk-auto` applied by rhythm, checked by reaper) is the correct solution to the batch-event race condition. `dependabot.yml` correctly limits to `pip` (weekly) and `github-actions` (daily) — npm and maven removed per prior audit.

---

### `sync-dependencies.yml` — Direct-Main Write

**Status:** Functioning; architecturally problematic.
**Finding:** Commits `requirements.txt` directly to `main` without a PR. Comment documents this as a temporary emergency corridor post-softlock. Should be routed through a PR once branch protection is stable.

---

### `stale-bot-prs.yml` — Stale Bot PR Cleanup

**Status:** Working correctly.
**Trigger:** Daily 13:00 UTC.
**Finding:** Closes Dependabot/bot PRs older than 5 days with `--apply`. Uses `setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6` — same version inconsistency.

---

### `opencode.yml` — OpenCode Agent Dispatch

**Status:** Working correctly.
**Trigger:** Any issue comment or PR review comment containing `/oc` or `/opencode`.
**Finding:** Third-party agent (`anomalyco/opencode`) using `OPENCODE_API_KEY` secret. Pinned to `d74d166acf40e51146f8547216913a4e787a4bc1 # v1.15.10`. No security concerns in the wiring; the agent itself is a separate trust surface.

---

### `1password-secret-template.yml` — 1Password Secret Injection Template

**Status:** Working correctly; reference template only.
**Trigger:** `workflow_dispatch` — never auto-fires.
**Finding:** Reference template demonstrating 1Password secret injection via `1password/load-secrets-action@v4`. Not part of the active gate or review pipeline. `OP_SERVICE_ACCOUNT_TOKEN` is the only credential stored directly in GitHub Secrets; all other secrets are fetched from 1Password at runtime.
**Script deps:** None.

---

### `janitor-sweep.yml` — Daily Rollover Failure Alerter

**Status:** Working correctly.
**Trigger:** `workflow_run` on "Daily To-Do Rollover" completion — fires only on failure.
**Finding:** Slack alert workflow; posts to `SWARM_SLACK_WEBHOOK_URL` when `daily-rollover.yml` fails. Uses `setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6` — same v6 inconsistency noted elsewhere. Reactive monitor, not a gate.
**Script deps:** `janitor_sweep.py`

---

### `laf-usb-manifest-policy.yml` — LAF-USB Object Manifest Policy

**Status:** Working correctly; security posture note.
**Trigger:** PR + push to main on `LAF-USB-OBJECT-MANIFEST*.json` or script/workflow changes.
**Finding:** Validates LAF-USB object manifests using `laf_usb_manifest.py`. Uses checkout@v4 + setup-python@v5 (standard single-checkout pattern). **Does NOT use the trusted-main dual-checkout pattern** used by `secret-pattern-policy.yml`, `large-file-policy.yml`, and `check-portable-paths.yml`. For structured JSON validation this is lower risk than secret or path validation — but is an inconsistency in the policy workflow tier.
**Script deps:** `laf_usb_manifest.py`

---

### `daily-rollover.yml` — Daily To-Do Rollover

**Status:** Working correctly.
**Trigger:** Schedule 10:00 UTC daily + `workflow_dispatch`.
**Finding:** Rolls incomplete to-do items forward daily. Parent workflow monitored by `janitor-sweep.yml` (which fires on failure). No gate or merge-path involvement.

---

### `wayback-audit.yml` — Wayback Machine URL Audit

**Status:** Working correctly.
**Trigger:** Schedule Monday 08:00 UTC + `workflow_dispatch` (with optional `limit` and `save` inputs).
**Finding:** Runs `wayback_audit.py`; if changes are produced, commits them to a timestamped branch and creates a PR via `gh pr create`. Uses `idempotent-pr-create` to skip PR creation if one already exists for that branch. Also calls `.github/actions/setup-vault` with `pip-packages: "PyYAML>=6.0"` (no `python-version`). Not a policy gate — it does not block merges — but it is not advisory-only: it produces commits and PRs when the audit finds changes.
**Composite actions used:** `.github/actions/setup-vault`, `.github/actions/idempotent-pr-create`

---

### `wayback-preserve.yml` — Wayback Machine URL Submission

**Status:** Working correctly.
**Trigger:** Push to main on `SOURCES/**`, `GOVERNMENTS/**`, `TOPICS/**`.
**Finding:** Submits new source URLs to the Wayback Machine when source documents are added or modified. If changes are logged, commits to a timestamped branch and creates a PR via `gh pr create`; uses `idempotent-pr-create` to prevent duplicate PRs on rerun. Calls `.github/actions/setup-vault` with no inputs (git identity only; no Python setup). Content-surface trigger (low-risk paths). Not a gate; cannot block merges.
**Composite actions used:** `.github/actions/setup-vault`, `.github/actions/idempotent-pr-create`

---

### `sort-audit.yml` — Vault Topology Census

**Status:** Working correctly.
**Trigger:** Schedule Monday 06:00 UTC + `workflow_dispatch`.
**Finding:** Runs `topology_census.py --scope all` (not `sort_audit.py`, which was deleted this session as superseded). Creates a PR via `peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1 # v8`, which handles idempotency natively (updates an existing branch PR rather than creating a duplicate — `idempotent-pr-create` is NOT used here). Calls `./.github/actions/setup-vault` with `pip-packages: "PyYAML>=6.0"` but no `python-version` — setup-python is skipped, but `pip install PyYAML` still runs against the runner's system Python. `topology_census.py` imports only stdlib so the PyYAML install is redundant but harmless.
**Composite action used:** `.github/actions/setup-vault`

---

### `branch-garden-report.yml`, `metadata-survey.yml`, `branch-cleanup.yml`, etc

**Status:** Working correctly. Covered in the companion triage report.

---

## VI-B. COMPOSITE ACTIONS (.github/actions/)

The vault owns two composite actions — vault-maintained reusable steps that live in `.github/actions/`. They have no triggers and cannot run independently; they are called by workflows as shared steps. Neither was inventoried in any prior audit report.

### `setup-vault` — Shared Vault Environment Setup

**Location:** `.github/actions/setup-vault/action.yml`
**Called by:** `sort-audit.yml`, `wayback-audit.yml`, `wayback-preserve.yml` (confirmed); likely other scheduled workflows.
**Function:** Configures git bot identity (`github-actions[bot]`) and optionally sets up Python + pip packages.
**Inputs:** `python-version` (optional), `pip-packages` (optional), `requirements-file` (optional).
**Finding:** If `python-version` is not passed, the setup-python step is skipped; if `pip-packages` is non-empty, pip install still runs against the runner's system Python. Internally uses `setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5` when Python is requested — adds another surface to the v5/v6 inconsistency finding. Any future caller that expects v6 behavior but routes through this composite without explicit `python-version` will silently get v5.

---

### `idempotent-pr-create` — PR Idempotency Lookup

**Location:** `.github/actions/idempotent-pr-create/action.yml`
**Called by:** `wayback-audit.yml`, `wayback-preserve.yml` (confirmed by file inspection).
**Function:** Checks whether an open PR already exists for a given branch before creating a new one. Prevents duplicate PR creation on workflow reruns.
**Inputs:** `branch` (required), `gh-token` (required).
**Outputs:** `pr_exists` ('true'/'false'), `pr_number` (number or empty string).
**Finding:** Correct idempotency primitive used by both Wayback workflows. Uses `gh pr list --head "$BRANCH_NAME" --state open --json number --jq` — reads only, no write side effects. Note: `sort-audit.yml` uses `peter-evans/create-pull-request` instead, which handles idempotency via branch reuse natively.

---

## VII. CONSOLIDATED FINDINGS

| # | Finding | Severity | Affected |
| --- | --- | --- | --- |
| 1 | Zero branch protection rules — all gates advisory | 🔴 Critical | All workflows |
| 2 | CODEOWNERS has no enforcement power | 🔴 Critical | Governance files, `!/`, `.github/` |
| 3 | `agent/*` branches not in auto-PR trigger | 🟡 Gap | `agent-auto-pr.yml` |
| 4 | `sync-dependencies.yml` direct-main write | 🟡 Temp debt | `sync-dependencies.yml` |
| 5 | `secret-pattern-full-scan.yml` non-standard checkout hash | 🟢 Inconsistency | `secret-pattern-full-scan.yml` |
| 6 | Mixed setup-python v5/v6 (partial Dependabot updates) | 🟢 Inconsistency | `large-file-watchdog.yml`, `check-dotfolder-anchors.yml`, `stale-bot-prs.yml`, `branch-garden-report.yml`, `metadata-survey.yml` |
| 7 | Composite action layer (`.github/actions/`) not previously inventoried; `setup-vault` uses v5 internally, adding a silent surface to the v5/v6 inconsistency | 🟢 Inventory gap | `setup-vault`, `idempotent-pr-create` |
| 8 | `laf-usb-manifest-policy.yml` does not use trusted-main dual-checkout pattern (unlike other policy workflows) | 🟢 Informational | `laf-usb-manifest-policy.yml` |

---

## VIII. CANDIDATE REQUIRED CHECKS FOR BRANCH PROTECTION

When Logan decides to re-enable branch protection, the minimal required set should consist only of checks that:

- Pass reliably on every clean push (no flapping)
- Are genuinely load-bearing (catching real problems, not noise)
- Have no known false-positive patterns

**Strong candidates:**

| Check | Workflow | Rationale |
| --- | --- | --- |
| Secret Pattern Policy | `secret-pattern-policy.yml` | Has never false-fired on clean vault content; fast; catches real secrets |
| Large File Policy | `large-file-policy.yml` | Deterministic; fast; prevents LFS budget blowout |
| NETWEB Path Portability | `check-portable-paths.yml` | Deterministic; catches real cross-platform issues |

**Conditional candidates (verify history first):**

| Check | Workflow | Concern |
| --- | --- | --- |
| CodeQL | `codeql.yml` | Can be slow; check if it has ever produced false positives on vault Python |
| Daily Notes Placeholder | `validate-daily-notes.yml` | Fast; verify it never fires on clean agent pushes |
| Dotfolder Anchors | `check-dotfolder-anchors.yml` | Verify consistent pass rate |

**Do not require (known noise or advisory-only):**

| Check | Reason |
| --- | --- |
| `submit-pypi` | GitHub auto-generated noise; always fails; already in KNOWN_NOISE_CHECKS |
| `Automatic Dependency Submission` | Same |
| Metadata Survey | Documented as persistent visibility surface, not pass/fail |
| Branch Garden | Advisory reporting only |

---

*Report filed: 2026-05-25 by Claude Code (Windows session), on Logan's direction.*
*Feeds into: Claude–Codex Security Collaboration Proposal (same session).*

The world is quiet here．Esto Perpetua!
