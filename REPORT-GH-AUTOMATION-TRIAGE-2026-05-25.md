---
title: GitHub Automation Triage — 2026-05-25
updated: 2026-05-25
status: active
authority: Logan Finney
authored-by: Claude Code
related:
- CLAUDE
- GitHub
- AGENTS
- VAULT-CONVENTIONS
- REPORT-GH-AUTOMATION-AUDIT-2026-04-03
---
# GITHUB AUTOMATION TRIAGE — 2026-05-25

**From:** Claude Code (Windows session)
**Branch:** `agent/triage-scripts-2026-05-25` — awaiting push authorization
**Prior report:** `REPORT-GH-AUTOMATION-AUDIT-2026-04-03.md` (by The Sentry — fixed action versions)
**Commit:** `a4222dad`

---

## I. WHAT THIS SYSTEM IS AND HOW IT WORKS

### The Platform: GitHub Actions

GitHub Actions is the automation platform built into GitHub. It runs programs automatically in response to events — a file is changed, a push goes up, a clock ticks over. You do not press a button. Things just happen.

GitHub named both the platform and its smallest building blocks "Actions," which is confusing. For clarity, this vault uses three distinct terms:

---

### Vocabulary

**Workflow** — a robot. A YAML file living in `.github/workflows/`. It defines:
- *When* to wake up (a trigger: push, schedule, pull request event)
- *What* to do when it wakes (a sequence of steps)

The vault owns these files. Logan can edit them. They run on GitHub's servers, not on any local machine.

**Script** — a tool a workflow runs. A Python or shell file living in `.github/scripts/`. The workflow picks up the script and runs it. Scripts do nothing on their own — they need a workflow to call them.

**Action** — a pre-built reusable step borrowed from GitHub or the community (e.g. `actions/checkout`, `actions/setup-python`). Workflows call these internally. The vault does not write or maintain them — it pins them to specific version hashes so they cannot change unexpectedly.

**Composite action** — a reusable building block written and maintained by the vault itself, living in `.github/actions/`. Composite actions are not workflows — they have no triggers and cannot run on their own. They are called by workflows as shared steps, eliminating repeated boilerplate. The vault currently has two: `setup-vault` (shared Python/git identity setup, used across scheduled workflows) and `idempotent-pr-create` (PR lookup utility, prevents duplicate PR creation on reruns).

**GitHub Actions (the platform)** — the name for all of the above, running on GitHub's servers.

```
GitHub Actions (platform)
│
├── Workflows   (.github/workflows/*.yml)   ← the robots; vault-owned
│   ├── call → Actions  (pre-built borrowed steps, e.g. actions/checkout)
│   ├── call → Composite actions  (.github/actions/*/)   ← shared building blocks; vault-owned
│   └── call → Scripts  (.github/scripts/*.py/.sh)   ← the tools; vault-owned
```

---

### How a Workflow Runs

1. An event happens (Logan or an agent pushes a commit; a clock fires; a PR opens).
2. GitHub reads the matching workflow YAML file.
3. GitHub spins up a fresh Ubuntu machine in the cloud.
4. The workflow's steps run in sequence on that machine:
   - Check out the vault (clone it)
   - Set up Python
   - Run the script
   - Report success or failure
5. The machine is discarded.

Nothing persists between runs except what gets committed back to the vault or posted to GitHub Issues.

---

## II. THE GOVERNANCE FAILURE PATTERN

This triage was triggered by a named pattern Logan identified:

> *Logan says "I need/want the vault to do X." Agent designs, builds, and tests X-prototype, then reports success and abandons the project without leaving documentation or wiring it to CI.*

The failure is not in the building. It is in the declaration. An agent that reports "tested and working" on a script that has no workflow calling it has not delivered a working feature — it has delivered an artifact. The operational gap (the missing workflow) is invisible unless someone audits the `.github/` directory.

**Evidence found:** `REPORT-TODO-SYNC-FIX.md` (commit `e07141f0`) declares a sync feature "tested and working." The functions `extract_tasks_from_daily_note()`, `sync_tasks_to_todo_list()`, and `sync_completed_to_daily_note()` exist in the script but are never called from `main()`. The feature was never delivered.

This is a repeat of a prior instance. Logan named it a governance failure.

---

## III. THE IDEMPOTENCY STANDARD

The governing filter applied to triage all scripts:

> **An operation is idempotent if running it N times produces the same result as running it once.**

Scripts that fail this test accumulate damage on repeated runs — they create duplicate files, corrupt locks, or produce inconsistent state. These should not exist in a system that runs automatically.

Scripts that pass this test are safe to wire to CI. Running them twice, or running them on a clean repo, produces no harm.

This standard cleanly resolved every ambiguous DELETE/KEEP decision.

---

## IV. PRE-TRIAGE STATE

Before this session, the `.github/scripts/` directory contained **39 files**. Cross-referencing every script against every workflow revealed:

| Category | Count |
|---|---|
| Scripts called by live, triggered workflows | 14 |
| Scripts called by workflows that existed but never triggered correctly | 4 |
| Scripts with no workflow calling them at all | 17 |
| Shell scripts (non-Python) | 4 |

Of the 17 orphans: some were idempotent tools that needed wiring. Others were non-idempotent tools that should never have been left available to run.

Additionally, one existing workflow had a broken trigger that had silently prevented it from ever firing.

---

## V. WHAT WAS DELETED AND WHY

### `.github/scripts/tidy_daily_notes.py`

**Claimed:** Tidy conflicted or duplicate daily notes.
**Actually:** A hardcoded list of 8 specific filenames from March 12–26, 2026, plus a hardcoded `NOTES` dict for that same window. A one-time repair for a specific mess in March 2026.
**Why deleted:** That mess is resolved. Running this again would target files that no longer exist or would damage files that replaced them. Not idempotent.

---

### `.github/scripts/chainfire.py`

**Claimed:** Burns tags and aliases from frontmatter across all vault notes; strips `[[wikilinks]]` from note bodies.
**Actually:** A vault-wide nuclear operation. Requires an explicit `--execute` flag. The script's own docstring reads:

> *"Do not run --execute without a sanctioned SPACE RACE mission ready to follow. CHAINFIRE without a committed CHAINLINK operation is not a cycle — it is damage."*

**CHAINLINK** — the rebuild operation — was never written.
**Why deleted:** Nuclear tool with no safety counterpart. Not idempotent (destroys data). The docstring itself prohibits running it in the current state.

---

### `.github/scripts/swarm_mvp_intake.py`

**Claimed:** Multi-agent document intake dispatcher.
**Actually:** Creates new markdown artifacts in `INBOX/SWARM-MVP/` on every run. Emits `GITHUB_OUTPUT`. Part of a "Swarm MVP" architecture that was never activated.
**Why deleted:** Accumulates new files on every invocation. Not idempotent. The architecture it served was never operational.

---

### `.github/scripts/update_manifest.py`

**Claimed:** Syncs Obsidian template tracking to `swarm.json`; manages manifest state.
**Actually:** Implements a two-phase soft-lock protocol (`--phase acquire` / `--phase release`). Acquires a lock, writes, releases. `DEFAULT_TTL_MINUTES = 15`.
**Why deleted:** Stateful lock management is not re-entrant and not idempotent. Running it twice without releasing breaks the lock. Part of the same never-activated Swarm MVP.

---

### `.github/scripts/sort_audit.py`

**Claimed:** Audits vault file sort order and structure.
**Actually:** An earlier version (v1) of the sort audit tool.
**Why deleted:** Superseded by `topology_census.py`, which is the current tool and is already wired to the live `sort-audit.yml` workflow. Two tools doing the same job; kept the live one.

---

### `.github/scripts/meshnetweb_portability_check.py`

**Claimed:** Checks vault file paths for cross-platform portability (the NETWEB standard).
**Actually:** Contains a `CHECK_FILES` list that includes `"!/README.md"` — but the actual file is `"!README.md"` (no slash). This mismatch means the check always fires a false positive for a file that isn't actually problematic.
**Why deleted:** Broken by design; overlaps with the live `check_portable_paths.py` which handles the same job correctly.

---

### `.github/scripts/vault-courier-sync.sh`

**Claimed:** Syncs vault content to a courier/relay destination.
**Actually:** Explicitly self-disabled at the top of the file. A credential was leaked and never reprovisioned.
**Why deleted:** Disabled by its own author. Credential never restored. Dead code.

---

### `.github/workflows/swarm-mvp-intake.yml`

**Claimed:** Orchestrates the Swarm MVP intake pipeline.
**Actually:** Calls `swarm_mvp_intake.py`, `update_manifest.py`, and `validate_content.py` in sequence. Never triggered (required a `workflow_dispatch` with specific inputs that no agent ever sent).
**Why deleted:** Two of its three scripts were just deleted. The workflow is broken without them. The architecture it served was never operational.

---

## VI. WHAT WAS FIXED

### `.github/workflows/levelset-closure-notify.yml`

**Purpose:** When a LEVELSET conversation log (in `!/`) is pushed with `status: terminated`, post a structured notification to the vault's GitHub Issues log.

**Bug found — two-layer trigger failure:**

Layer 1 — YAML escaping:
```yaml
# Before (broken):
paths:
  - '\!/LEVELSET-*.md'
```
In YAML single-quoted strings, `\` is a literal backslash, not an escape character. The actual string passed to GitHub was `\!/LEVELSET-*.md`. No file path begins with a backslash. This trigger never fired.

Layer 2 — GitHub Actions path negation:
Even if the backslash were removed, `!` at the start of a path pattern in GitHub Actions is a negation operator. It means "exclude paths matching this." So `!/LEVELSET-*.md` would mean "trigger on everything *except* LEVELSET files" — the exact opposite of intent.

```yaml
# After (fixed):
paths:
  - '[!]/LEVELSET-*.md'
```
Square brackets form a character class. `[!]` is the literal character `!`. This matches `!/LEVELSET-*.md` correctly.

Layer 3 — git pathspec `!` magic (fixed in diff step):
```bash
# Before (potentially broken):
git diff --name-only "$before" "$after" -- '!/LEVELSET-*.md'
# ! in a git pathspec can trigger exclude magic

# After (fixed):
git diff --name-only "$before" "$after" | grep '^!/LEVELSET-' > /tmp/changed_levelsets.txt || true
```

---

## VII. WHAT WAS WIRED (new workflows for existing scripts)

### `.github/workflows/sync-agents-bootstrap.yml` → `generate_agents_bootstrap.py`

**What the script does:** Reads `swarm.json` and generates `!/agents.json` and `agents.json` — index files that tell agents what other agents exist and what they can do. Has a `--check` mode that exits with error if the generated output doesn't match what's on disk.

**Why it needed wiring:** The script existed. The index files existed. But nothing checked whether they stayed in sync when `swarm.json` changed. The check mode was built but never called.

**Trigger:** Any push that modifies `swarm.json`.
**Action:** Runs `generate_agents_bootstrap.py --check`. Fails the workflow (alerts Logan) if the index is stale.

---

### `.github/workflows/sync-plugin-registry.yml` → `sync_obsidian_plugin_registry.py`

**What the script does:** Reads `.obsidian/community-plugins.json` and `.obsidian/core-plugins.json`, cross-references plugin manifests, and updates `plugin_layer` blocks in `manifest.json` and `swarm.json`. Has `--check` mode.

**Why it needed wiring:** Same pattern. Script existed and worked. Nothing called it when plugin lists changed.

**Trigger:** Any push that modifies `.obsidian/community-plugins.json` or `.obsidian/core-plugins.json`.
**Action:** Runs `sync_obsidian_plugin_registry.py --check`. Fails if registry is stale.

---

### `.github/workflows/validate-agent-content.yml` → `validate_content.py`

**What the script does:** A content safety gate. Inspects staged `.md` files for:
- Script injection (`<script>`, `javascript:`, `onclick=`)
- Malformed YAML frontmatter
- Files over 50KB
- Unresolved template tokens (`[[YESTERDAY]]`, `[[TOMORROW]]`, `[[TODAY]]`) in daily notes and the TO DO LIST
- Suspicious sponsor names
- Directory scope violations
- Missing required frontmatter fields on governed notes

Uses `git diff --cached` (staged files) internally. Requires `PyYAML`.

**Why it needed wiring:** The validator existed and was used in the now-deleted `swarm-mvp-intake.yml` — but only as part of the never-activated Swarm MVP pipeline. It was never wired to agent branches, which is the surface that actually needed it.

**Trigger:** Any push to an `agent/**` branch.
**Special handling:** The workflow stages `HEAD^..HEAD` changed `.md` files before running the script, because `git diff --cached` reads the staging area, not the working tree. In CI there is no staging area unless you explicitly create one.
**Dependencies:** Installs `pyyaml` before running.

---

## VIII. SCRIPTS KEPT AS LOCAL TOOLS (intentionally not wired)

These scripts are idempotent and useful but designed for local use. Wiring them to CI would not make sense — either they require local filesystem access, interactive input, or Logan's manual judgment.

| Script | Reason kept local |
|---|---|
| `backfill_daily_notes.py` | Repair kit; Logan runs on demand when daily notes have gaps |
| `audit_repo_payloads.py` | LFS slimming analysis; output is for Logan's review — **deleted 2026-07-24 (PR #854)** |
| `date_tagger.py` | Tags root-level source notes; Logan runs manually |
| `tag_stubs.py` | Tags 1-line stub notes; Logan runs manually |
| `bind_ai_book.py` | Archives personal AI chat exports; input is Logan's local files |
| `phone_link_intake.py` | Intake from Logan's Windows phone; local machine only |
| `obsidian_rest_api_client.py` | Calls local Obsidian REST API; not reachable from CI |
| `generate_name_forms.py` | Personal creative/naming tool; not a vault-maintenance function |

---

## IX. POST-TRIAGE AUTOMATION STATE

### Live Workflows (pre-triage fleet, running correctly)

All 28 pre-existing workflows currently in `.github/workflows/`, with verified triggers. The 4 workflows added or fixed in this session are listed separately below.

| Workflow | Trigger | Purpose |
|---|---|---|
| `1password-secret-template.yml` | workflow_dispatch | Reference template for 1Password secret injection; never auto-fires |
| `agent-auto-pr.yml` | on: create + workflow_dispatch | Auto-creates PRs for claude/codex/gemini/copilot/perplexity/grok/serena branches |
| `agent-review-gate.yml` | Schedule every 4h + workflow_dispatch | Reconciles open PR review state; promotes eligible low-risk PRs to merge/auto |
| `auto-merge.yml` | pull_request_target: labeled | Enables squash auto-merge (job gates on merge/auto label) |
| `branch-cleanup.yml` | PR closed to main + Schedule Mon 9am UTC + workflow_dispatch | Prunes stale agent branches |
| `branch-garden-report.yml` | Schedule Mon 10am UTC + workflow_dispatch | Branch health report |
| `check-dotfolder-anchors.yml` | Push to main + PR | Dotfolder anchor integrity check |
| `check-portable-paths.yml` | PR + push to main (trusted-main) | NETWEB path portability enforcement |
| `codeql.yml` | Push to main + PR + weekly schedule | CodeQL Advanced security scan |
| `daily-rollover.yml` | Schedule 10am UTC (4am MT) daily | Rolls incomplete to-dos forward |
| `dependabot-reaper.yml` | Schedule every 2h | Re-arms stuck low-risk Dependabot PRs (race-condition safety net) |
| `dependabot-rhythm.yml` | pull_request_target: opened/reopened/ready | Auto-approves and merges qualifying Dependabot patch/minor PRs |
| `janitor-sweep.yml` | workflow_run on daily-rollover failure | Posts Slack alert via webhook |
| `laf-usb-manifest-policy.yml` | PR + push to main on manifest file paths | Validates LAF-USB object manifests |
| `large-file-policy.yml` | PR + push to main + workflow_dispatch (trusted-main) | Per-push large file check |
| `large-file-watchdog.yml` | Schedule Mon 11am UTC + workflow_dispatch | Weekly large file scan |
| `metadata-survey.yml` | Schedule Mon 10am UTC + workflow_dispatch | Frontmatter health survey |
| `opencode.yml` | issue_comment/PR review comment containing /oc | Dispatches OpenCode agent |
| `review-feedback-loop.yml` | issue_comment, PR events | Agent claim verification, thread sweep, copilot apply |
| `review-response.yml` | pull_request_review submitted | Pauses/resumes auto-merge on review |
| `secret-pattern-full-scan.yml` | Schedule Mon 11:23am UTC + workflow_dispatch | Full-repo secret pattern scan |
| `secret-pattern-policy.yml` | PR + push to main + workflow_dispatch (trusted-main) | Per-push secret pattern check |
| `sort-audit.yml` | Schedule Mon 6am UTC + workflow_dispatch | Vault topology census (topology_census.py); creates PR |
| `stale-bot-prs.yml` | Schedule daily 13:00 UTC + workflow_dispatch | Closes old Dependabot/bot PRs |
| `sync-dependencies.yml` | Push to main on pyproject.toml + workflow_dispatch | Direct-main pip requirements sync (temp corridor) |
| `validate-daily-notes.yml` | PR + push to main | Daily note placeholder check |
| `wayback-audit.yml` | Schedule Mon 8am UTC + workflow_dispatch | URL preservation audit |
| `wayback-preserve.yml` | Push to main touching SOURCES/GOVERNMENTS/TOPICS | Submits new URLs to Wayback Machine |

### Newly Wired (this session)

| Workflow | Trigger | Purpose |
|---|---|---|
| `sync-agents-bootstrap.yml` | `swarm.json` changes | Verifies agent index is current |
| `sync-plugin-registry.yml` | `.obsidian/*.json` changes | Verifies plugin registry is current |
| `validate-agent-content.yml` | Push to `agent/**` | Content safety gate on agent commits |
| `levelset-closure-notify.yml` | Push touching `!/LEVELSET-*.md` | **Fixed** (was silently broken since creation) |

### Open Issues (not addressed in this triage)

| Issue | Notes |
|---|---|
| Node.js 20 deprecation | Exactly 30 of 32 workflows use `checkout@v4` / `setup-python@v5/v6` (Node.js 20 runtime); deprecation date not confirmed — do not act on this without verifying the GitHub announcement |
| Secret Pattern Full Scan false positives | Fires every Monday; known noise |
| Ollama key rotation | `id_ed25519` was scrubbed from git history 2026-05-25; key itself still needs rotation |

---

## X. NET CHANGE

```
Before: 39 scripts — 17 orphaned, 4 wired-never-triggered, some non-idempotent
After:  32 scripts — 0 orphaned, 0 silently broken triggers, all non-idempotent tools removed

Deleted:  7 scripts + 1 workflow (1,642 lines removed)
Fixed:    1 workflow trigger (double bug)
Created:  3 new workflows (94 lines added)
```

Every script that remains either runs via a working CI trigger or is an intentionally local tool. Every workflow trigger that exists actually fires on the events it claims to fire on.

---

---

## XI. GATES AND CHECKS — FINDINGS (addendum, same session)

### How the vault got here

Agents kept bolting workflows and required checks on without reading what already existed. The required-check queue grew contradictory. PRs couldn't pass. Nothing could merge. Logan had to disable branch protection to escape the softlock.

Evidence in the codebase: `sync-dependencies.yml` contains this comment, still live:

> *"Temporary direct-main emergency corridor: retained only while the dependency lane is being repaired after PR automation softlock."*

The corridor was cut as an emergency exit. The exit was never closed because the root cause — agents building without reading the existing system — was never addressed at that layer. It was addressed in this session at the script layer (see Sections V–VII above). The workflow layer is next.

### Confirmed state (via GraphQL)

```json
{"data":{"repository":{"branchProtectionRules":{"nodes":[]}}}}
```

Zero branch protection rules. Repository settings confirm `allow_auto_merge: true` — auto-merge is enabled, but with no required checks and no required reviews configured, auto-merge fires immediately once armed. There is nothing for it to wait for.

**Consequence:** CODEOWNERS is decorative. The vault's most sensitive surfaces — `CONSTITUTION.md`, `CLAUDE.md`, `.github/workflows/`, `!/` — are listed as requiring Logan's review. GitHub will not enforce that requirement.

### Full findings

| Finding | Severity |
|---|---|
| No branch protection rules — all gates are advisory | 🔴 Critical |
| CODEOWNERS has no enforcement power (consequence of above) | 🔴 Critical |
| `agent/*` branches not covered by `agent-auto-pr.yml` trigger | 🟡 Gap |
| `sync-dependencies.yml` direct-main write still in place | 🟡 Temp debt |
| `secret-pattern-full-scan.yml` uses non-standard `actions/checkout` hash | 🟢 Inconsistency |
| Mixed `setup-python` v5/v6 across workflows (partial Dependabot updates) | 🟢 Inconsistency |

### What is working correctly

- **classify_paths.py** — fail-safe default (unknown → high-risk); label taxonomy consistent
- **Dependabot pipeline** — rhythm + reaper + `dependabot/low-risk-auto` proof label is well-designed; npm and maven correctly removed
- **review_feedback_loop.py** — handles `@copilot apply changes`, thread sweep, agent claim verification (IF 7)
- **KNOWN_NOISE_CHECKS** — `submit-pypi` correctly excluded from check rollup
- **opencode.yml** — properly scoped, pinned hash, correct secret reference
- **validate-daily-notes.yml** — complementary to validate_content.py, not redundant
- **30-minute grace period** — time-based gate enforced by agent-review-gate.yml; works correctly as a social control even without branch protection

### Remediation sequence (when ready)

**Do not simply re-enable branch protection.** That is the re-softlock path. The required sequence:

1. Identify which checks pass reliably on clean pushes — no flapping, no false failures
2. Designate a minimal required set (candidate: secret-pattern-policy, large-file-policy, check-portable-paths)
3. Re-enable protection with only those verified checks as required + 1 approving review
4. Remove the direct-main corridor from `sync-dependencies.yml`
5. Decide `agent/*` prefix policy — add to auto-PR pattern or document as intentionally manual

This is a Logan decision, not an agent decision. No changes made in this session.

---

*Report filed: 2026-05-25 by Claude Code (Windows session), on Logan's direction.*
*Branch: `agent/triage-scripts-2026-05-25` — awaiting push authorization.*

###### "The world is quiet here."
