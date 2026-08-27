---
title: CI Failure Sweep — 2026-08-18
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, ~2026-08-16T17:00Z to 2026-08-18T17:00Z (per-workflow coverage varies — see Big IF)
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-18

## 5W Summary

| | |
|---|---|
| **Who** | Scheduled Claude Code CI-review routine, acting for Logan Finney, against all ~69 registered workflows (`list_workflows`) on `laf-us/idaho-vault`. Two root causes fixed in this same PR (#998); two more flagged, deliberately not fixed. |
| **What** | (1) `.github/workflows/sync-plugin-registry.yml` never installed `pygit2` before running a script that imports it at module level — `ModuleNotFoundError` on every push touching Obsidian plugin config. (2) Root file `"consistent with" ≠ evidence.md` carried literal `"` characters, illegal on NTFS — broke `git checkout` on every Windows CI runner for nearly every open PR regardless of what it touched. |
| **When** | Both confirmed still firing at sweep time. (1): 18 failures in-window across 18 branches (workflow id 283254968). (2): reproduced on ≥8 unrelated PR branches between 11:22Z and 14:07Z today; the offending file predates this sweep and has no discoverable introduction date within the window checked. `main` HEAD (`ad09929d`, PR #961, 11:42Z today) was unchanged throughout the sweep. |
| **Where** | `.github/workflows/sync-plugin-registry.yml` (both `check-plugin-registry` and `self-heal-plugin-registry` jobs); root-level filename; `manifest.json`/`swarm.json` (stale count, surfaced as a side effect of fix #1); `.triagebot/stub.txt` (separate, smaller fix — see Findings). |
| **Why** | Neither was a defect in the code under test — both were gaps in the CI plumbing itself: a missing dependency-install line, and a pre-existing tracked file whose name only breaks one platform's checkout. Both were repo-wide, not scoped to whatever a given PR touched. |
| **How** | GitHub Actions REST API (workflow-run listing across all registered workflows, job-log pulls on failures) for detection; local reproduction against current `main` HEAD (import failure, `git checkout` failure, running the repo's own guard scripts) before writing any fix; cross-checked against existing open PRs/issues (#966, #859, #984, #962) before acting, to avoid duplicating in-flight work. |

## Findings

### Incident A — `sync-plugin-registry.yml` missing `pygit2` install — Code, **fixed in this PR**

`.github/scripts/sync_obsidian_plugin_registry.py` does `import pygit2` at module level (used to read tracked plugin manifests via libgit2 rather than shelling out to `git`, see #514). Neither `check-plugin-registry` nor `self-heal-plugin-registry` in `sync-plugin-registry.yml` ever installed it — both jobs only ran `actions/checkout` + `actions/setup-python`. Every run failed with `ModuleNotFoundError: No module named 'pygit2'`. Confirmed by direct API query: 18 failures on 18 different branches in this 48h window alone (`push` events, workflow id 283254968), plus reproduced locally (`python3 -c "import pygit2"` fails in a bare env, succeeds after `pip install`).

Fixed by adding `pip install "pygit2>=1.18.2"` to both jobs — matches the repo's existing single-package convention (`pip install pyyaml` in `metadata-survey.yml` and `validate-agent-content.yml`; `pip install --quiet jupytext` in `check-notebooks-paired.yml`). With the import fixed, `--check` immediately surfaced a second, real problem: `manifest.json`/`swarm.json` had a stale `installed_community_count`/`dormant_installed_count` (75/31 vs. the actual 74/30 tracked manifests) — the counts field had drifted out of sync with the actual `installed_community_plugins` array length, independent of anything this sweep touched. Regenerated both files via the now-working `--write` and included the correction in this PR.

### Incident B — root file with an NTFS-illegal filename — Code, **fixed in this PR**

Root file `"consistent with" ≠ evidence.md` contained two literal `"` characters — one of the six characters (`<>:"|?*`) `.github/scripts/check_portable_paths.py` itself treats as illegal, per the repo's own NETWEB standard (`VAULT-CONVENTIONS.md` § "Portable Path Standard"). Confirmed via job logs on `Cross-Platform Smoke`'s `windows-latest` legs: `git checkout --progress --force refs/remotes/pull/NNN/merge` failed with `error: invalid path '"consistent with" ≠ evidence.md'`, exit 128 — on at least 8 unrelated branches (`codex/phone-link-explicit-vault-root`, `claude/rework-census-doctrine-463-4033po` ×4, `claude/practical-cerf-rylptz`, `claude/elegant-archimedes-0zqhsc` ×2), none of which touched this file. Because the file is tracked on `main`, every Windows checkout of any branch built on current `main` inherited the failure — this was not "some PRs are broken," it was "every Windows smoke test is broken, regardless of PR content."

Fixed by renaming to `consistent with ≠ evidence.md`: dropped only the two illegal quote characters, kept `≠` (not in the illegal set) and all file content unchanged. Added an `aliases:` frontmatter entry with the original quoted title so existing Obsidian references/search still resolve. Verified clean against `check_portable_paths.py` itself post-rename, and confirmed via a full tracked-tree scan that no other file carries an NTFS-illegal character.

`NETWEB Path Portability Check` (`check-portable-paths.yml`) never caught this because it only checks the *changed paths in a PR's diff* — this file predates the check or simply hasn't been touched by any PR since, so it never re-triggered the gate. The principle (per VAULT-CONVENTIONS.md) still applies retroactively regardless of gate coverage; noting the gap rather than claiming the gate would have caught it.

### Incident C — `.triagebot/` dotfolder incomplete — half-fixed, half-flagged

`.triagebot/` (added by #941, "feat: implement triagebot-action for automated issue triage", merged today 11:37Z) has its chamber anchor (`.triagebot/TRIAGEBOT.md`) but shipped without two things `check_dotfolder_anchors.py` requires of every tracked dotfolder:

- **`.triagebot/stub.txt`** (the STUB-PERSONAFOLDERS vacancy sentinel, exact bytes `¿!?`) — missing. **Fixed in this PR**: mechanical, no judgment call, added the required 4 bytes.
- **Root-level `TRIAGEBOT.md`** — missing, and this pushes the script's own root-anchor ratchet from 293 to 294, which the script hard-fails on (`check_dotfolder_anchors.py`'s own docstring: "Effect: existing debt warns; ANY increase fails"). **Not fixed here.** The script's docstring is explicit that a root anchor is "an authored persona note (frontmatter, `related` edges, the chamber's own lines), not a sentinel," and that generating one unprompted would be "an agent writing vault canon it was never asked to write." Confirmed this reproduces identically against current `main` (not introduced by this PR) — `check-dotfolder-anchors` is red on every push/PR against `main` right now until either `TRIAGEBOT.md` is authored or the ratchet ceiling is deliberately raised. Left for Logan.

### Incident D — `Codacy Security Scan` failing on `main` — not a defect, already tracked elsewhere

Run `32133055147` (push, merge of PR #961, 11:42Z today) failed on `main` itself. Root-caused via job log: the SARIF-null-`rules` repair that *was* a real defect (fixed via PR #962, merged 2026-08-16) is running clean — log shows `repaired: runs[0].tool.driver.rules was NoneType, coerced to []` executing without error. The actual failure is downstream, on the `upload-sarif` step: `API rate limit exceeded for installation`. This is the same GitHub API installation-wide rate-limit exhaustion already root-caused and being fixed in open PR #984 ("Fix review-bot comment storm exhausting GitHub API rate limit," see LAF-80, 2026-08-16 sweep) — not a new bug, not duplicated here.

### Pre-existing audit-PR pile — not added to, one redundancy found

Per this routine's own instruction not to stack another unaddressed report on the pile: #966 ("CI failure audit — 48h rolling review (2026-08-12)") is still open, `mergeable_state: blocked`, 6 days old, 49 mostly-bot comments, auto-merge-enabled. Logan's own comment on it (today, 11:54Z) already correctly diagnosed both of its blocking checks as the exact same pre-existing `main`-branch debt documented above (Incident C's stub.txt/ratchet, and the pygit2 gap) — PR #998 is the actual fix for that debt, not a third report on top.

**New finding this sweep:** #966's core deliverable — `!/AUDIT-CI-FAILURE-SWEEP-2026-08-12.md` — already exists on `main`, landed via the separately-merged PR #962 (commit `91eecee1`, part of merge `6402ea5c`). #966 is therefore attempting to re-add/modify a file that already shipped through a different PR; it is not merely stale, it is now substantively redundant. Flagging for Logan rather than closing it myself. #859 ("CI failure sweep report for 2026-07-21") is also still open and stale (~4 weeks) — flagged, not touched.

## Big IF

- **The recurring shape of this sweep series continues: silent-until-triggered CI-plumbing gaps, not code-under-test defects.** Same pattern as the 2026-08-12 sweep's invalid-`permissions`-key finding and the 2026-08-16 sweep's rate-limit-storm finding (LAF-78, LAF-80): neither of this sweep's two fixes would show up reading any single PR's diff. Both needed a job-log read plus a local reproduction against current `main` to distinguish "real, fixable, currently-blocking defect" from the swarm's very high background noise floor (several workflows here logged 1,000–12,500+ lifetime runs; `Agent Review Response` alone had 4,170).
- **Coverage is honest, not exhaustive, by necessity.** Queried run-level data for all 69 registered workflows' most recent ~30 runs each. For the handful of hyper-frequent ones (`Agent Review Response`, `CodeQL`, `Check Dotfolder Anchors`, `Cross-Platform Smoke`, `opencode`, `PR-Agent`, `Codacy Security Scan`, `Verify Arbiter Approvals`, and others — 14 total), that most-recent-30 slice did not reach back the full 48h window; each such case is labeled with its actual retrieved time range above/in the PR, not silently presented as full coverage. Did not attempt full pagination on those (would run into the thousands of API calls for some), consistent with the 2026-08-12 sweep's finding that this repo's write throughput makes naive full-window pagination unreliable at the boundary anyway.
- **The audit-PR pile still didn't shrink, and now has a redundancy inside it.** #966 and #859 remain open; #966's report content already landed via a different PR (#962), which nobody had previously connected. This sweep continued the established instruction (bundle report with real fix, don't file report-only), and surfaced the redundancy rather than silently reconciling it — that's Logan's call, not this routine's, per its own scope limits.

---
Cross-posted: GitHub PR #998 (this PR) + comment on #998 re: check-dotfolder-anchors, Linear LAF-81, Slack #all-logan-finney, Discord #ledger (via Zapier).
