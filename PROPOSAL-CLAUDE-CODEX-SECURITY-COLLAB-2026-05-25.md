---
title: Claude–Codex Security Collaboration Proposal — 2026-05-25
updated: 2026-05-25
status: proposal
authority: Logan Finney
authored-by: Claude Code
related:
- CLAUDE
- AGENTS
- GitHub
- REPORT-GH-GATES-AUDIT-2026-05-25
- REPORT-GH-AUTOMATION-TRIAGE-2026-05-25
- REPORT-GH-AUTOMATION-AUDIT-2026-04-03
---
# CLAUDE–CODEX SECURITY COLLABORATION PROPOSAL

## Restoring Branch Protection Without Re-Creating the Softlock

**Proposed:** 2026-05-25
**Status:** Awaiting Logan's authorization
**Context:** Codex is performing a repository-wide security scan (concurrent). Claude has completed a scripts/workflows triage and a gates/checks audit (this session).

---

## I. WHAT EACH AGENT HAS DONE

### Claude (this session)

- Catalogued all 39 scripts in `.github/scripts/` — what each claims vs. what it actually does
- Applied idempotency as a governance filter
- Deleted 7 non-idempotent or superseded scripts + 1 dead workflow (1,642 lines removed)
- Fixed a two-layer trigger bug in `levelset-closure-notify.yml`
- Wired 3 previously orphaned scripts to new CI workflows
- Audited all gate/check workflows — PR lifecycle, label taxonomy, risk classification, auto-merge mechanics
- Confirmed: zero branch protection rules; CODEOWNERS is decorative; all gates are advisory
- Documented the softlock history and why "just turn protection back on" is the re-softlock path
- **Reports on file:** `REPORT-GH-AUTOMATION-TRIAGE-2026-05-25.md`, `REPORT-GH-GATES-AUDIT-2026-05-25.md`
- **Branch:** `agent/triage-scripts-2026-05-25` (awaiting PR merge)

### Codex (concurrent)

- Performing a repository-wide security scan
- Scope: TBD pending Codex's own report

---

## II. THE SHARED PROBLEM

Branch protection has been off since a softlock: agents kept adding required checks without reading what was already required. The check queue broke. PRs couldn't pass. Logan disabled protection to escape.

The result:

- CODEOWNERS is decorative — `.github/workflows/`, `CONSTITUTION.md`, `CLAUDE.md`, `!/` are listed as requiring Logan's review; GitHub will not enforce this
- CodeQL findings are visible but not blocking
- Secret scan, large-file check can fail and PRs still merge
- The `sync-dependencies.yml` workflow commits directly to `main` as an emergency bypass that was never cleaned up

The solution is not simply "turn protection back on." The solution is a verified minimal required-check set, implemented carefully enough that it doesn't re-create the problem it's solving.

---

## III. PROPOSED DIVISION OF LABOR

### Phase 1 — Codex: Reliability Audit (read-only)

Codex's security-scan posture makes it well-suited to this phase. The question to answer: **Which checks pass reliably on clean pushes?**

**Tasks:**

1. Pull recent run history for each candidate check workflow (last 30 runs minimum)
2. For each: calculate pass rate, identify any flapping, identify false-positive patterns
3. Cross-reference with `KNOWN_NOISE_CHECKS` in `review_feedback_loop.py` — confirm those exclusions are still correct and complete
4. Identify any checks that are currently silently broken (run but always pass vacuously)
5. Review `classify_paths.py` — does the HIGH_RISK_EXACT set match the current CODEOWNERS? Are there paths that should be high-risk but aren't?
6. Review the `sync-dependencies.yml` direct-main corridor — assess the security exposure of a workflow that bypasses PR review
7. Deliver: a reliability report for each candidate required check, with a recommended required-set

**Candidate checks to evaluate (from Claude's audit):**

Strong candidates for required:

- `secret-pattern-policy` — Secret Pattern Policy
- `large-file-policy` — Large File Policy
- `check-portable-paths` — NETWEB Path Portability

Conditional (verify history):

- `codeql` — CodeQL Advanced
- `validate-daily-notes` — Daily Notes Placeholder Check
- `check-dotfolder-anchors` — Dotfolder Anchor Check

Do not require (known noise):

- `submit-pypi`, `Automatic Dependency Submission` — already excluded from check rollup; should remain excluded from required checks

**Codex deliverable:** A written reliability report + a recommended minimal required-check set, with pass rates and reasoning. Post to GitHub Issue (see Section V).

---

### Phase 2 — Claude: Implementation

Once Logan approves a required-check set and Codex has confirmed reliability:

**Tasks:**

1. Remove the direct-main write from `sync-dependencies.yml` — route through a PR like everything else
2. Standardize `actions/checkout` hash across all workflows (`11bd71901bbe5b1630ceea73d27597364c9af683 # v4`)
3. Standardize `setup-python` version — pick v5 or v6; update all workflows consistently
4. Decide `agent/*` prefix policy with Logan; update `agent-auto-pr.yml` if warranted
5. Configure branch protection rules via `gh api` or GitHub UI per Logan's decision:
   - Required status checks: Codex's recommended minimal set
   - Require 1 approving review (CODEOWNERS enforcement)
   - Dismiss stale reviews on new commits
   - Do NOT require administrators — Logan needs an escape hatch if something breaks again

**Claude does NOT configure branch protection unilaterally.** The required-check set is Logan's decision after reviewing Codex's reliability report.

---

## IV. WHAT CODEX NEEDS TO READ

Before beginning Phase 1, Codex should read these files in order:

| File | Why |
| --- | --- |
| `.github/CODEOWNERS` | Which paths require Logan's review |
| `.github/scripts/classify_paths.py` | Risk classification logic |
| `.github/scripts/review_feedback_loop.py` | PR state machine; `KNOWN_NOISE_CHECKS` |
| `.github/workflows/agent-auto-pr.yml` | PR creation + classification trigger |
| `.github/workflows/agent-review-gate.yml` | Grace period + reconciliation logic |
| `.github/workflows/auto-merge.yml` | Auto-merge arm logic |
| `.github/workflows/sync-dependencies.yml` | The direct-main corridor |
| `REPORT-GH-GATES-AUDIT-2026-05-25.md` | Claude's full audit (this session) |
| `REPORT-GH-AUTOMATION-TRIAGE-2026-05-25.md` | Scripts triage + softlock history |

---

## V. COORDINATION MECHANISM

**GitHub Issue** — open one issue for the collaboration; both agents comment on it.

Suggested title: `[Security] Restore branch protection — Claude/Codex collaboration`

Suggested labels: `agent:claude-code`, `agent:codex`, `security`

**Workflow:**

1. Logan opens the issue (or authorizes Claude to open it)
2. Claude posts a link to the three vault documents (triage report, gates audit, this proposal)
3. Codex posts its security scan findings and reliability report as comments
4. Logan reviews both, designates the required-check set
5. Claude implements Phase 2 on a branch; opens PR for Logan's review
6. Logan merges; branch protection is re-enabled

---

## VI. CONSTRAINTS AND GUARDRAILS

- **Branch protection configuration is Logan's decision.** Neither agent configures it without explicit authorization.
- **No agent opens this PR.** `agent-auto-pr.yml` would classify `.github/workflows/` changes as high-risk, producing a manual-review PR. That is correct. Logan merges.
- **The direct-main corridor stays until protection is re-enabled.** Removing it before protection is stable would break the dependency lane again.
- **The remediation must be atomic from a protection standpoint.** Don't enable protection with a partial required-check set that causes immediate failures. Test each required check manually before adding it.
- **Codex's security scan findings supersede Claude's audit where they conflict.** Codex has broader access to run history and security context. Claude's audit is a starting point.

---

## VII. RISKS

| Risk | Mitigation |
| --- | --- |
| Re-softlock if a required check flaps | Codex's reliability audit; minimal required set; Logan keeps admin override |
| Agent adds more workflows before protection is re-enabled | This proposal is contingent on the triage branch merging first; no new automation added until protection is stable |
| Codex security scan finds issues beyond branch protection scope | Address those separately; don't block this proposal on unrelated findings |
| `sync-dependencies.yml` removal breaks the dependency lane | Test pip-compile manually on a branch before removing the corridor |

---

## VIII. GITHUB ISSUE DRAFT

*Logan can copy this to open the coordination issue.*

---

**Title:** `[Security] Restore branch protection — Claude/Codex collaboration 2026-05-25`

**Body:**

Branch protection on `main` has been off since a softlock caused by agents adding required checks without reading what was already required. This issue tracks restoring it correctly.

**Context documents (in vault, on `agent/triage-scripts-2026-05-25`):**

- `REPORT-GH-AUTOMATION-TRIAGE-2026-05-25.md` — scripts triage, softlock history
- `REPORT-GH-GATES-AUDIT-2026-05-25.md` — per-workflow gate analysis, candidate required checks
- `PROPOSAL-CLAUDE-CODEX-SECURITY-COLLAB-2026-05-25.md` — this proposal

**Phase 1 (Codex):** Reliability audit of candidate required checks. See proposal Section III.
**Phase 2 (Claude):** Implementation once Logan approves the required-check set.

**Logan's decision required:** Which checks to require; whether to require 1 approving review; admin enforcement.

**Do not merge this PR or re-enable protection until Codex's reliability report is posted here.**

---

*Proposal filed: 2026-05-25 by Claude Code (Windows session), on Logan's direction.*

---

```
The world is quiet here．Esto Perpetua!
```
