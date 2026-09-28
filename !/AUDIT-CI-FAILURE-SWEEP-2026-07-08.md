---
title: CI Failure Sweep — 2026-07-08
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-07T09:00Z to 2026-07-08T09:15Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-08

## Context

Scheduled 24-hour review of failing GitHub Actions runs across `laf-us/idaho-vault`. The repo runs ~48 workflows; most of the run volume is per-PR bot automation (review/merge-queue/arbiter bots) that was clean throughout the window. Six workflows had genuine `conclusion: "failure"` runs. Root-caused each from job logs rather than reporting them unread.

One finding (PR #463's CENSUS doctrine + unresolved review threads) was carried to completion rather than just logged — see [[#Action taken this run]] below — because a fresh look turned up a fixable, non-architectural blocker.

---

## 5W Summary

| | |
| --- | --- |
| **Who** | No human-caused breakage. Failures are: 1 third-party GitHub Action bug (Codacy), 2 doctrine-drift checks on Logan's own `logan/obsidian` live-edit branch, 1 file-size policy hit on an in-progress agent branch, 1 unpinned-action lint hit on draft PR #450 (already a known TODO there), 1 known corruption-signature hit on a Codex branch (issue #739 pattern). |
| **What** | 35 failing runs across 6 workflows: Codacy Security Scan (29), Sync Plugin Registry (9, pre-existing — not counted in the 35), Sync Agent Discovery Index (2), Validate Agent Content (1), Action Pin Policy (1), Redaction Damage Policy (1), plus one anomalous `claude-sign.yml` failure with no retrievable job logs. |
| **When** | 2026-07-07T09:00Z – 2026-07-08T09:15Z (rolling 24h). Sync Plugin Registry has been failing since at least 2026-07-03 — a 5-day-old unaddressed chronic failure. |
| **Where** | Codacy: every push/PR/merge_group targeting `main`. Sync Plugin Registry + Sync Agent Discovery Index: pushes to `logan/obsidian`. Others: isolated to their own feature branches (`agent/adr-canon-core-portability`, `claude/draft-signing-via-action-2026-06-01`, `codex/triage-idaho-vault-repository-issues`). |
| **Why** | See per-item root cause below — ranges from a third-party CLI bug, to doctrine-drift checks with no auto-fix step, to real policy violations (oversized file, unpinned action, redaction-corruption signature). |
| **How** (next step) | See per-item recommendation below. Nothing in this sweep is a "here's a report, good luck" — each item has an owner-actionable next step, not just a restated symptom. |

---

## Findings, prioritized by blocking impact

### 1. Codacy Security Scan — 29/30 runs failed — BLOCKING, repo-wide

**Category:** Infrastructure (third-party action bug)

Every push/PR/merge_group against `main` in the window failed identically. Root cause is not the repo's code — `max-allowed-issues: 2147483647` in `.github/workflows/codacy.yml` already forces the analysis step itself to exit 0 regardless of findings. The crash happens *after* analysis, while `codacy/codacy-analysis-cli-action` builds the SARIF report:

```text
Exception in thread "main" java.nio.charset.MalformedInputException: Input length = 1
    at ... better.files.File.lines(File.scala:282)
    at com.codacy.analysis.cli.formatter.Sarif.$anonfun$createResults$3(Sarif.scala:146)
##[error]Process completed with exit code 1.
```

One sub-tool's intermediate results file contains a non-UTF-8 byte sequence; the Sarif formatter's line reader chokes on it. (Separately, `pmd`/`pmd-legacy` log "No rules found" but that's non-fatal — the encoding crash is what kills the job.) Representative run: id 28926865837 (2026-07-08T07:55:30Z, `main`, push).

**Update (same day, on PR #821):** actually fixed, in three steps, not just diagnosed:

1. Ran a full-repo blob scan (`git cat-file --batch` over all 38,458 tracked blobs) to find every non-UTF-8 tracked file rather than guess — 21 total (photos/scans, a Publisher draft, an `.rtfd`, a database/pickle file, a WhatsApp `.crypt14` backup, several cp1252 `minidata*.csv` exports). Excluded them in `.codacy.yml`.
2. That alone didn't fully land — Codacy's exclude-path glob dialect turned out to require a bare `*.ext` pattern in addition to `**/*.ext` for root-level files (10 of the 21 live at repo root); added both forms.
3. A *second*, independent bug then surfaced in the same formatter (`IndexOutOfBoundsException` at `Sarif.generatePrimaryLocationHash`, unrelated to encoding): the pinned action commit (`d840f886`, tagged `1.1.0`) resolves to `codacy-analysis-cli` **4.0.0**, whose hash function only guards the lower bound on a tool-reported line number (`fileContents(Math.max(0, issue.location.line - 1))`) — any issue reporting a line past the file's actual length crashes the job. Confirmed via the CLI's own source at each version; the fix (`fileContents.applyOrElse(...)`) landed by CLI ~7.x. Re-pinned to `v4.0.2` (`f38648320929161d81646834fbee4d75f6502aea`) — the oldest tagged action release with the fix, chosen over newer tags (v4.4.0+) because those reference an unpinned `actions/setup-go@v3` internally, which this repo's action-pin policy rejects outright regardless of runtime conditionals.

Both SARIF crashes are now gone (confirmed: no `Exception in thread` anywhere in the v4.0.2 run's log). What's left is a **third, unrelated blocker**: `CODACY_PROJECT_TOKEN` — never listed in `.op/secrets.template.md`'s secrets inventory, so it was likely never actually provisioned — causing `Could not get remote project configuration: No credentials found.` once the analysis gets far enough to need it. Every prior run's SARIF crash was masking this.

**Suggested next step:** needs Logan — either provision a real `CODACY_PROJECT_TOKEN` (1Password + repo secret, same pattern as `OP_SERVICE_ACCOUNT_TOKEN`), or decide whether to keep the Codacy workflow at all given it's likely never had working credentials. Not fixable from a code change; no access to repo secrets or the Codacy dashboard from this session.

### 2. Sync Plugin Registry — 9 failures in-window, chronic since ≥2026-07-03

**Category:** Configuration/Process

`.github/workflows/sync-plugin-registry.yml` runs `sync_obsidian_plugin_registry.py --check` on every push touching `.obsidian/*` config or `manifest.json`/`swarm.json`, and fails closed on drift. Every failure in the window is the same message:

```text
Obsidian plugin registry drift detected:
  manifest.json
  swarm.json
Run: python .github/scripts/sync_obsidian_plugin_registry.py --write
```

All 9 are pushes to `logan/obsidian` — this is Logan's live-edit branch (presumably synced from the Obsidian desktop app), and nothing in that path runs the generator's `--write` mode before committing, so the check fails every single time plugin config changes, indefinitely.

**Suggested next step:** Fix, not just retry. Either (a) wire `--write` into whatever process commits from the Obsidian desktop app before it pushes, or (b) convert this from a fail-closed *check* into a self-healing workflow that runs `--write` and commits the corrected `manifest.json`/`swarm.json` back to `logan/obsidian` automatically. Given this has been red for 5+ days without anyone acting on it, a self-healing workflow is probably the more durable fix than relying on discipline at commit time.

### 3. Sync Agent Discovery Index — 2 failures, same pattern as #2

**Category:** Configuration/Process

Same shape as Sync Plugin Registry, different generator: `.github/scripts/generate_agents_bootstrap.py --check` fails closed on `logan/obsidian` pushes (runs 28907512777, 28903779527). Likely fixable by the same remediation as #2 — worth doing both together since they're the same root pattern (fail-closed drift check with no upstream auto-fix step, on a branch that gets pushed to directly and often).

### 4. Validate Agent Content — 1 failure

**Category:** Configuration (policy violation, real)

`agent/adr-canon-core-portability` branch: `!/TOPOLOGY-CENSUS-dotfolders-20260706T100744Z.md` is 177.5 KB against a 50 KB limit. This is a generated topology-census artifact, not hand-authored content — the branch likely needs to either exclude generated census output from this check's scope, or that file shouldn't have been committed to that branch in the first place.

**Suggested next step:** Investigate on that branch specifically — outside this sweep's scope to fix blind, since it's an in-progress agent branch I don't have context on.

### 5. Action Pin Policy — 1 failure

**Category:** Code (policy violation, trivial fix, but not mine to make)

`claude/draft-signing-via-action-2026-06-01` (PR #450): `.github/workflows/claude-sign.yml:90` uses `anthropics/claude-code-action@main` instead of a pinned 40-char SHA. This is a known, already-tracked gap — PR #450's own body lists "Pin `claude-code-action@main` to a tagged release" as open item #5, and that PR is explicitly a draft held under Logan's gate pending his answers to its other open architecture questions. Not fixing it here since the PR is intentionally not being advanced without Logan's input.

### 6. Redaction Damage Policy — 1 failure

**Category:** Code (known corruption pattern, per issue #739)

`codex/triage-idaho-vault-repository-issues` branch: redaction-damage guard caught a marker glued to a letter/digit on both sides in `.claude/plugins/.install-manifests/*.json` (e.g. `chrome-devtools-mcp@claude-plugins-official.json:179`), matching the known corruption shape from issue #739.

**Suggested next step:** Flag to whoever's driving that Codex branch — this is a recognized bug pattern, not a new one, so the fix should already be documented against #739.

### 7. `claude-sign.yml` — 1 anomalous failure, no logs

**Category:** Infrastructure (unclear — needs manual look)

Run 28919974166 (`claude/draft-signing-via-action-2026-06-01`, push, 2026-07-08T05:32:08Z) is recorded with `conclusion: "failure"`, but both job-logs and job-listing queries return zero jobs for this run. Can't diagnose from the API. Worth a look in the GitHub Actions UI directly.

---

## Action taken this run

Rather than only filing this report, picked up PR #463 (`loganfinney27/templates`, the second-oldest open PR, open since 2026-06-03 with 9 unresolved automated-review threads) and drove it toward merge:

- Addressed all 9 outstanding review findings on #463 directly (status enum, Tri-Anchor wording, dead-pointer findings that main had already resolved independently, etc.) and resolved each thread.
- Discovered #463's branch predates this repo's "Clean history - secrets purged" rewrite and now has **no common ancestor with `main`** (`git merge` refuses it; GitHub reports `mergeable_state: dirty`) — the same failure mode PR #450 already named and worked around ("reworked in place ... on current main").
- Opened #821, rebuilding the still-relevant content (the `CENSUS.md` doctrine seed, four reference docs not yet on `main`, and a properly-rendered `2026-06-03.md`) fresh on top of current `main`, dropping the `backup-compare-temp/` scratch tree and stale `.gitignore`/issue-template edits that `main` had already superseded.
- Commented on #463 pointing to #821 and recommending it close as superseded once #821 merges (left the close itself to Logan).

This is the same "unrelated histories" defect that presumably explains why several other stale open PRs in this repo (predating the purge) haven't been mergeable via the normal GitHub merge button — worth keeping in mind if more of the backlog gets worked.

---

## Big IFs (Insights and Findings)

- **The repo has a systemic pre-purge/post-purge branch-compatibility break.** Any open PR whose branch was created before the "Clean history - secrets purged" rewrite cannot be merged via a normal `git merge` — GitHub will report `mergeable_state: dirty` no matter how clean the content diff looks, because the histories are literally unrelated. PR #450 already discovered and worked around this once; #463/#821 is the second confirmed instance. Worth an inventory pass over the rest of the stale-PR backlog to see how many others are silently blocked the same way — that would explain a lot of the "opened-then-unaddressed" pile as a structural cause rather than neglect.
- **Two workflows (Sync Plugin Registry, Sync Agent Discovery Index) are fail-closed checks with no corresponding auto-fix step**, both aimed at the one branch (`logan/obsidian`) that gets pushed to most often and most directly. As written, they can only ever go red and stay red until someone manually runs the `--write` counterpart — which nobody has, for at least 5 days on the plugin registry. A self-healing variant (run `--write`, commit back) would convert chronic red into an occasional bot commit.
- **Codacy blocking every push/PR to `main`** for reasons unrelated to actual code findings is a visibility problem: it trains everyone to ignore the Codacy check as "always red," which is exactly the condition under which a real Codacy finding would also get ignored.
