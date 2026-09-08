---
title: PR Loop Audit — 2026-04-19
type: audit
status: draft
authority: CLAUDE (Abhorsen audit)
scope: GitHub Actions agent-PR lifecycle + related schedule ecosystem
owner: Logan Finney
---

# PR Loop Audit — 2026-04-19

## Context

Audit of the agent-PR lifecycle end-to-end: branch push → auto-PR creation → bot review triggers → review-gate promotion → auto-merge → branch cleanup. Triggered by observed wonkiness (title amputation, body churn, four `422 already exists` races in one session). Grounded in a full sweep of all 30 workflows, 16 scripts, 13 scheduled triggers, and the full label vocabulary.

Not a remediation plan — a reference punch list. Each finding cites `file:line` evidence; none prescribes code. Fix ordering and scope are Logan's call.

---

## Findings (ranked by pain, not by severity)

### 1. Title amputation

**Evidence:** `.github/workflows/auto-pr.yml:104`

```bash
TITLE=$(echo "$BRANCH" | sed 's|^[^/]*/||' | sed 's|-[a-zA-Z0-9]*$||' | tr '-' ' ')
```

The second `sed` assumes every agent branch ends with a random session token (e.g. `U4XDk`). Real branches without a suffix lose their last real word:

- `claude/serena-voice-bleed-purge` → "serena voice bleed" (lost `purge`)
- `claude/todoist-probe` → "todoist" (lost `probe`)
- `claude/cleanup-mcp-connectors` → "cleanup mcp" (lost `connectors`)

No fallback: workflow does not read the last commit subject, a PR template, or any file in the branch (confirmed by sweep §7). Fix direction: detect session-suffix shape (contains digit OR uppercase) before stripping, or prefer `git log -1 --format=%s HEAD` when it looks like a conventional commit.

---

### 2. Body/risk-tier churn invalidates the gate parser

**Evidence:** `.github/workflows/auto-pr.yml:119-127` (body generation) + `.github/scripts/review_feedback_loop.py:216-222` (`_risk_tier_for_pr`)

The auto-body encodes the canonical risk tier as a `**Risk tier:** low` marker. `_risk_tier_for_pr()` parses that marker back out of the body to decide auto-merge eligibility.

But agents (me included) overwrite the body with a real description immediately after the auto-PR lands — which destroys the marker. Parser falls back to checking the `agent-review-pending` label (fine, mostly), but the invariant that "body is the source of truth for risk tier" is broken on every PR.

Blast radius: today the fallback saves us. Tomorrow, if the label gets removed by review activity before promotion, the parse returns `"unknown"` → `low_risk = False` → PR stuck in staged forever.

Fix direction: move risk tier to the label as primary (`risk/low`, `risk/high`) and stop parsing body markers. Or: auto-pr uses PR comments or a hidden HTML marker that agents are trained to preserve.

---

### 3. Lifecycle vocabulary has 5 dead-letter states

**Evidence:** `.github/scripts/pr_lifecycle.py:14-23` (8 states defined) vs. sweep §5 (3 reachable).

| State | Reachable? | Setter |
|---|---|---|
| `staged` | ✅ | `auto-pr.yml:155` |
| `merged` | ✅ | `branch-cleanup.yml:89` (on `pull_request.closed` when `merged == true`) |
| `abandoned` | ✅ | `branch-cleanup.yml:89` (on `pull_request.closed` when `merged == false`) |
| `live` | ❌ | none |
| `superseded` | ❌ | none |
| `dormant` | ❌ | none |
| `reactivated` | ❌ | none |
| `archived` | ❌ | none |

No workflow transitions `staged` → `live`. "Live" appears to be an intended human-curated state (e.g., "in production") with no automation hook. Either (a) build the transitions, (b) prune the vocabulary to the reachable three, or (c) document the five as human-only.

---

### 4. Two label vocabularies with inconsistent namespacing

**Evidence:** `pr_lifecycle.py:14-23` (lifecycle namespaced) vs. `review_feedback_loop.py:39-60` (review flat).

| Namespace style | Labels |
|---|---|
| `lifecycle/<state>` | staged, merged, abandoned, live, superseded, dormant, reactivated, archived |
| flat | `auto-merge`, `agent-review-pending`, `review-required`, `review-threads-open`, `copilot-apply-pending` |

The two scripts don't know about each other's labels. Fix direction: pick one convention (e.g., `review/pending`, `review/required`, `review/threads-open`, `merge/auto`, `merge/copilot-apply-pending`) and migrate, or accept the split and document it in one place.

---

### 5. Up to 60-minute latency for low-risk auto-merge

**Evidence:** `auto-pr.yml` (stamps at T=0) + `review_feedback_loop.py:31,260-262` (30-min body-age grace) + `agent-review-gate.yml:8-9` (`*/30 * * * *` cron).

Worst case: PR created 29 minutes before grace window elapses, then waits another 30 min for the next cron tick. Total 59 minutes before the `auto-merge` label gets added. Then `auto-merge.yml` fires on the label event and arms GitHub auto-merge, which itself waits for required checks.

Fix direction: drop cron to `*/5` or `*/10`, or trigger `promote-ready` from `pull_request` events so the grace check happens the moment the window elapses (still cron-backed as a safety net).

---

### 6. Review-trigger blast is unconditional

**Evidence:** `auto-pr.yml:170-174`

Every new agent PR gets three bot-review triggers posted as comments regardless of whether the apps are installed, under quota, or relevant to the changed files:

```
@coderabbitai review
@Qodo /review
@gemini-code-assist review
```

Noise per PR: 3 comments. Noise per week at current velocity: ~60 comments. Fix direction: make the roster conditional on an installed-apps check, or move to a repo-level setting with per-PR opt-in.

---

### 7. Creation race mitigated in ONE place, not SIX

**Evidence:** Sweep §6, §8.4.

`auto-pr.yml:70-84` has an idempotency guard: it lists open PRs for the branch before calling `gh pr create` and skips if one exists. This prevents the workflow from racing itself.

But it does NOT prevent `auto-pr` from racing an agent's own `gh pr create` (or MCP `create_pull_request`) call — I hit this four times this session, getting `422 already exists` every time.

AND five OTHER branch-creating workflows have no idempotency guard at all:

| Workflow | File | Creates PR without check |
|---|---|---|
| `daily-rollover.yml` | partial check at :121-131 | — |
| `linear-brief.yml` | — | ✅ |
| `vault-ingest.yml` | — | ✅ |
| `idaho-leg-scraper.yml` | — | ✅ |
| `wayback-preserve.yml` | — | ✅ |

Fix direction: extract the check-for-existing-PR pattern into a shared composite action (`./.github/actions/idempotent-pr-create`). Or document the observed agent-side pattern: "agents must never call `gh pr create` on agent-prefixed branches — always push and let `auto-pr.yml` own creation, then use `update_pull_request` to set title/body."

---

### 8. All `.github/workflows/` + `.github/scripts/` are classified high-risk

**Evidence:** `.github/scripts/classify_paths.py:13-17`

```python
HIGH_RISK_PREFIXES = (
    "!/",
    ".github/workflows/",
    ".github/scripts/",
)
```

Any workflow or script change is high-risk → no `agent-review-pending` label → cannot be auto-merged. That's correct-by-design for most changes, but it means:

- PR #263 (Todoist probe — additive, new file, no existing-workflow edits) requires manual review to merge
- Follow-up probes will have the same friction
- The fix PRs for items 1–7 above will all require manual merge

Fix direction: either accept the friction (maybe correct!), or carve out a narrow "additive workflow" rule (e.g., net-new file under `.github/workflows/` matching a probe/example prefix) that classifies as low-risk.

---

## Surprises from the sweep (out of the 8-point scope)

These were flagged by the Explore agent and are worth naming even though they don't fit the agent-PR loop proper:

- **S1. Dependabot is MORE permissive than agent PRs.** `.github/workflows/dependabot-rhythm.yml` auto-approves patch/minor pip + actions updates with no grace window. Inverse of the rigor applied to human-directed agent work.
- **S2. `stale-bot-prs.yml` hard-closes at 2 days with no warning.** Legit PRs waiting on review feedback or a dependent workflow could be eaten.
- **S3. The 30-min grace window is a Python-side convention.** No branch-protection rule enforces it — if `review_feedback_loop.py` has a bug or is bypassed, PRs can arm earlier than intended.
- **S4. No documentation explains any of this.** No runbook, no architecture doc, no agent guidance about the race surface. The audit *is* the documentation.

---

## Appendix A: Schedule ecosystem at a glance

| Cron | UTC time | Workflow | Commits? |
|---|---|---|---|
| `*/30 * * * *` | every 30 min | agent-review-gate | no |
| `0 10 * * *` | daily 10:00 | daily-rollover | yes |
| `0 12 * * *` | daily 12:00 | vault-ingest | yes |
| `0 13 * * *` | daily 13:00 | stale-bot-prs | no |
| `30 13 * * *` | daily 13:30 | budget-tracker-csv-export | no |
| `0 6 * * 1` | Monday 06:00 | sort-audit | sometimes |
| `0 8 * * 1` | Monday 08:00 | wayback-audit | sometimes |
| `0 9 * * 1` | Monday 09:00 | branch-cleanup | no |
| `0 10 * * 1` | Monday 10:00 | branch-garden-report | no |
| `0 11 * * 1` | Monday 11:00 | large-file-watchdog | no |
| `33 13 * * 6` | Saturday 13:33 | codeql | no |
| `0 13 * * *` | DISABLED | idaho-leg-scraper | — |

Peak concurrency: Monday 10:00 UTC has two workflows scheduled back-to-back (daily-rollover + branch-garden-report). No observed conflicts.

---

## Appendix B: Recommended fix ordering (suggestion only)

If Logan wants a single remediation PR, the minimal high-leverage bundle is **(1) + (2) + (7)**:

1. **Title amputation** — one regex line in `auto-pr.yml`.
2. **Risk tier as label, not body marker** — move the canonical location, update `_risk_tier_for_pr()` to read the label. Removes the body-churn brittleness.
3. **Idempotent PR creation helper** — shared composite action, replaces the inline check-pr step, gets adopted by the other 5 workflows over time.

(3) + (5) + (6) would be a second tier (clean up lifecycle vocabulary, cut auto-merge latency, tame review trigger noise). (8) is a scope call, not a fix.

---

## Status

**Not committed.** Reference document for discussion. Next action: Logan reviews, decides scope for remediation PR(s), or directs further investigation on specific findings.

**Audit artifacts:** Explore-agent sweep report attached to conversation at `/tmp/claude-0/-home-user-IDAHO-VAULT/feb07931-08a9-4bb3-970a-65a51fb728a8/tasks/ae88f020f2af69ae1.output` (ephemeral; capture inline above if needed).
