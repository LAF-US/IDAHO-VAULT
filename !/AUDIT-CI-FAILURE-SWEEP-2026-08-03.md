---
title: CI Failure Sweep — 2026-08-03
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-08-02T07:00Z to 2026-08-03T07:30Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-03

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (64 workflows per `list_workflows`). No new human-caused breakage. One genuinely new, fixable workflow bug found and fixed in this same PR (Incident D below); everything else is either benign (gate-holds), transient (self-healed credential blip), already-tracked (Codacy), or branch-local drift on PRs already flagged in prior sweeps. |
| **What** | Swept all 64 workflows individually (not a single all-workflows call — that call's payload is too large to read reliably at this run volume). Found 7 distinct incidents, detailed below; the "unclear" item from the raw sweep was tracked down to a specific, verified root cause (see Incident H). |
| **When** | 2026-08-02T07:00Z – 2026-08-03T07:30Z. |
| **Where** | Zero failures on `main` itself. Everything is confined to: a single dependency-sync PR (gate-hold), three automation workflows during one ~5.5h credential blip, PR #470's stale branch (`test/subtle-alien-landing`), PR #894's active branch (`claude/smoke-guards-qzt7le`), and two branches with real, working-as-intended drift-detector hits. |
| **Why** | See per-incident root cause below — each is evidence-based (job logs read directly), not inferred. |
| **How** | Category breakdown: Configuration (4), Transient (1), Code (1, fixed in this PR), Code/branch-drift (1, not this PR's to fix). See below. |

## Findings

### Incident A — `automation/sync-dependencies` PR held at `action_required` across 13 workflows — Configuration, non-blocking

All 13 required-check workflows fanned out to `action_required` simultaneously at 2026-08-03T03:49:34Z on one PR event (branch `automation/sync-dependencies`). Verified directly: pulled job logs for one of them (NETWEB Path Portability Check, run [30782759958](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30782759958)) — **0 jobs ever ran**. This is GitHub's own "needs approval to run workflows" gate on a first-time/low-trust actor, not a code or infra failure. Nothing to fix; it clears on manual approval.

### Incident B — Intermittent `gh`/`gh api` 401 "Bad credentials", ~2026-08-02T22:12Z–2026-08-03T03:47Z, self-resolved — Transient

Confirmed with actual log text on 3 separate workflows/~20 runs, all the same signature:

- Agent Review Response — run [30782407999](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30782407999) (PR #892): `gh label create` → `HTTP 401: Bad credentials`.
- Auto-merge on PR events — run [30771226003](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30771226003) (PR #854): `gh api graphql` → `Bad credentials (HTTP 401)`.
- Enqueue on checks complete — run [30782636840](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30782636840) (`main`, PR #562) and ~14 more runs (run_numbers 1368–1387) across the same window, interleaved with successful runs (not a hard outage).

Every run on these three workflows from ~03:47Z onward succeeded — the token issue cleared on its own before this sweep started. **Owner: Logan, if it recurs.** Not fixable from a code change; flagging because it hit 3 separate automation paths, not just one.

### Incident C — Windows `UnicodeDecodeError` in Cross-Platform Smoke — Code, but not this PR's to touch

Verified via job logs (run [30788030341](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30788030341)): `meshnetweb_portability_check.py`'s `tracked_files()` reads `git ls-files -z` output via `subprocess.run(..., text=True)` with no explicit encoding, so Windows runners decode with `cp1252` and crash on byte `0x9d`. Root-caused precisely, **but this is on `claude/smoke-guards-qzt7le` (PR #894, "Fix CI on logan/obsidian... make the surface check path-tolerant"), which was pushed to as recently as this morning (2026-08-03T06:02Z) — i.e. someone is actively iterating on this exact file right now.** Not touching it: this session's operating instructions are explicit that other agents' in-progress branches aren't mine to push to, and PR #894's own title suggests this may already be what it's mid-fixing.

### Incident D — Auto PR for Agent Branches attempted `gh pr create` against GitHub's own merge-queue branches — Code, **fixed in this PR**

Verified via job logs across 7 runs (e.g. run [30782704220](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30782704220), branch `gh-readonly-queue/main/pr-562-...`): `pull request create failed: GraphQL: Head sha can't be blank ... Head must not be a merge queue branch`.

Root cause: `.github/workflows/agent-auto-pr.yml`'s branch gate is intentionally prefix-agnostic — any slash-namespaced branch (`<namespace>/<desc>`) is treated as agent work and gets a PR. GitHub's merge queue creates its own ephemeral branches in exactly that shape (`gh-readonly-queue/<base>/pr-<n>-<sha>`), so they slipped through the same gate and hit `gh pr create`, which rejects merge-queue heads outright.

**Fix:** added an explicit `gh-readonly-queue/*` case to the gate's branch-name `case` statement, ordered before the generic `*/*` match (bash `case` takes the first match), so these branches are skipped the same way dash-prefixed ephemeral artifacts already are. Added a regression test (`tests/test_workflow_security_invariants.py::test_merge_queue_branches_are_excluded_from_auto_pr`) asserting the exclusion exists and is ordered correctly. Verified locally: ran the extracted gate logic against `gh-readonly-queue/main/pr-562-...` (now skips), `claude/practical-cerf-eaj0xt` (still creates a PR), `dependabot/github_actions/foo` (still creates a PR), and `main` (still skips) — the fix doesn't change behavior for any branch shape other than the one it targets.

### Incident E — `Sync Plugin Registry` / `check-notebooks-paired` drift detectors firing correctly — Configuration, working as intended

- `Sync Plugin Registry`, run [30775233178](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30775233178): `Obsidian plugin registry drift detected: manifest.json, swarm.json` — this is the #514 pattern; PR #891 (still open, 2026-08-02) already lands the git-tracked-manifest fix for it.
- `check-notebooks-paired`, runs [30776339184](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30776339184) / [30775232760](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30775232760): "A notebook twin is out of sync" (jupytext) — content out of sync with its generator, not a broken check.

### Incident F — Secret Pattern Policy flagged real secret-shaped strings in committed daily notes — Configuration, needs Logan's eyes on content, not a workflow bug

Runs [30786957468](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30786957468) / 30775233189 (branches `claude/smoke-guards-qzt7le`, `claude/poka-yoke-player-qzt7le`): scanner found `google_api_key`/`openai_key`/`generic_secret_assignment`-shaped strings in several daily-note `.md` files and one `session-join-pattern` file. Exits 1 by design — not something to silently work around from a CI-sweep session. Flagging so it doesn't get read as "just noise."

### Incident G — Codacy Coverage Reporter — Configuration, already tracked (#822 / LAF-72)

Runs [30773666793](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30773666793) / 30769052661: `Invalid configuration: Empty argument for --project-token`. Different literal message than the "Could not get remote project configuration" text from earlier sweeps, but same underlying class (token/project-association). Not a new problem. Separately, 6 `Codacy Security Scan` runs showed `conclusion: cancelled` in this window — verified these are concurrency-group cancellations (superseded by a newer push to the same PR), not the tracked Codacy failure; not counted as failures.

### Incident H — Python Test Suite failure on PR #470's branch, root cause now confirmed — Code/branch-drift, not this PR's to fix

Run [30769052696](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/30769052696), branch `test/subtle-alien-landing` (PR #470): pulled the full log rather than leaving this as "unverified" the way the raw sweep first found it. The actual failure is `test_dependabot_auto_merge_requires_verified_low_risk_updates_and_gates` in `tests/test_workflow_security_invariants.py`, asserting a `!contains(github.event.pull_request.labels.*.name, 'risk/high')` string that isn't present in that branch's copy of the dependabot-auto-merge eligibility logic — i.e. that branch's workflow/test pair predates a change that later landed on `main`. Consistent with (and now confirms, rather than just repeats) the 2026-07-31 sweep's flag of unresolved content drift on PR #470. Not fixing on that branch — it's a 9,357-line, 86-commit, actively-commented PR (`mergeable_state: dirty`) that is not mine to rewrite mid-review.

## Big IF

- **The "unclear, needs a fuller log" habit from prior sweeps is worth breaking deliberately.** Last sweep's raw data would have left Incident H as "root cause unverified from available logs." Pulling the full (not tail-truncated) log took one extra tool call and turned a guess into a citation. Doing this by default, not just when convenient, is what keeps this report out of the "possibly/likely" failure mode the routine exists to catch.
- **This is the second sweep in a row to find a real, fixable workflow bug (Incident D) rather than only re-describing known issues** — same pattern as 2026-08-02's #514 fix. Two data points isn't a trend, but it suggests actually reading job logs closely each day surfaces real things, not just repeats.
- **The audit-PR pile grew, not shrank, since yesterday.** Of 12 daily sweep PRs filed since this thread opened 2026-07-08, only 3 have ever landed on `main` (07-08, 07-09, 07-20); 9 remain open/unmerged (#838, #859, #861, #862, #866, #878, #882, #884, and now #891 from yesterday). This sweep follows the same instruction as yesterday's — bundling the report with a real fix (Incident D) instead of filing a report-only PR — but that alone doesn't clear the backlog; only merging (or deliberately closing) the existing 9 does. Worth a batch pass on Logan's end: they're pure-documentation + already-verified-safe fixes, not big asks individually.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
