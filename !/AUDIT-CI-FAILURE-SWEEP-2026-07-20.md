---
title: CI Failure Sweep — 2026-07-20
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-19T04:53Z to 2026-07-20T04:53Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-20

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (63 workflows per the Actions API's `list_workflows`, which also counts platform-registered dynamic workflows like Dependabot Updates/CodeQL default setup/Copilot cloud agent; 49 are `.yml` files under `.github/workflows/`); Claude Code (this session, scheduled). No new human-caused breakage. |
| **What** | 28 `Codacy Security Scan` failures + 2 `action_required`; 11 `Codacy Coverage Reporter` failures + 1 `action_required` (new workflow, 100% failure rate since it merged yesterday); 8-run `Agent Review Response`/`Review Feedback Loop` cluster (transient); 1 `CodeQL` failure on PR #450 (root cause not visible). `opencode.yml`/`Dependabot Rhythm` — 30/30 `skipped`, the 2026-07-02 fix (PR #737) still holds, no `startup_failure`. `cloud-run-deploy.yml` (PULLMAN)/`janitor-sweep.yml` — zero runs in-window, nothing to report. |
| **When** | 2026-07-19T04:53Z – 2026-07-20T04:53Z. Codacy failures spread across the full window, before and after 16:34Z. The Review-Response cluster is isolated to 2026-07-20T00:00–00:02Z. |
| **Where** | `.github/workflows/codacy.yml` + `codacy-coverage-reporter.yml` — `main` and nearly every open branch/PR. Review-Response cluster — PR #450 only. CodeQL failure — PR #450 only. |
| **Why** | See "Blocking / repeated" below — this is the substantive change from every prior sweep in this thread. |
| **How** | Category: Codacy/Coverage Reporter = **Configuration**, but a *different* configuration problem than the one tracked since 2026-07-08 (see below). Review-Response cluster = **Transient** (GitHub API 503, self-resolved). CodeQL = **Unknown** — job logs 404, not diagnosable from here. |

## Blocking / repeated

- **Codacy is still red, but not for the reason tracked in #822 since 2026-07-08.** You commented `CODACY_PROJECT_TOKEN provisioned` on #822 at 2026-07-19T16:34:40Z. Confirmed directly by diffing job logs from before and after that timestamp on the same workflow:
  - Before (run 29686696981, 2026-07-19T12:17:35Z): `Could not get remote project configuration: No credentials found.`
  - After (run 29717811744, 2026-07-20T04:51:26Z — this morning, 12+ hours post-provisioning): `Could not get remote project configuration: Error: getting Project Configuration : not found`
  The token is now being read (the error changed), but Codacy's API can't locate a project to associate it with. This reads as `idaho-vault` not actually being set up/synced as a project in the Codacy web dashboard yet, or the token belonging to a different project than this repo — not a workflow-file or secret-wiring bug (`project-token: ${{ secrets.CODACY_PROJECT_TOKEN }}` in both `codacy.yml` and `codacy-coverage-reporter.yml` is wired correctly). This needs a look at the Codacy dashboard directly, not another token provision — flagging distinctly rather than repeating "still needs your provision-vs-retire call," which would now be stale and wrong.
  - Secondary, identical on every single run regardless of before/after: `Failed to fetch patterns for Biome from API: ... High not a member of Level: DownField(level),DownArray,DownField(data)`. Reads as a Codacy-service-side schema issue, not something in this repo's config — plausibly downstream of the same missing project association, not independently diagnosed further.
  - **Correction, added after this PR's own checks surfaced it:** `mergefreeze` staying green is not the whole picture. This PR's own `mergeable_state` came back `blocked`, with `coverage` and `Codacy Security Scan` as failing *required* status checks — `mergefreeze` and GitHub's native required-status-checks are two separate gates, and one being green doesn't mean the other is. So this item is blocking for at least some PRs (this one included) via branch protection, even though `mergefreeze` itself isn't the thing enforcing it. Don't repeat the flat "non-blocking for merges" claim from the 2026-07-11 correction without checking each PR's own `mergeable_state`.
  - **Owner:** Logan. **Next action:** in the Codacy web dashboard, confirm `idaho-vault` is listed as a project, and confirm the value stored in `CODACY_PROJECT_TOKEN` was generated from that project's own token page (not an account/org-level token — those use a different secret, `CODACY_API_TOKEN`, per `codacy-analysis-cli-action`'s README). **Done when:** a `Codacy Security Scan` run on a fresh push returns `success` (or a real lint/security finding) instead of the `Project Configuration : not found` error.
- **`codacy-coverage-reporter.yml`** (new, merged 2026-07-18 via PR #850/#855) has never once succeeded since it started running (2026-07-19T19:48Z) — same root cause as above. Expected to clear once the Codacy project association is fixed; not a separate bug in the new workflow file.
- **Sync Plugin Registry / Sync Agent Discovery Index (PR #831 / #834) — still unmerged, still not actually fixed on `main`.** Zero failures this window only because `logan/obsidian` hasn't pushed plugin/agent config since 2026-07-14 — verified directly by reading current `main`'s `.github/workflows/sync-plugin-registry.yml` and `sync-agents-bootstrap.yml` just now: neither has the self-heal job from #834, only the original fail-closed `--check`. The tested fix has sat ready since 2026-07-09/10, explicitly parked pending your direction (your 2026-07-10 comment on #822). Re-flagging once, plainly, so "no failures today" doesn't get read as "resolved."

## New findings

None beyond the Codacy diagnosis update above — no new workflow, branch, or failure signature outside what's covered there.

## Big IF

- **A "still needs your call" diagnosis can go stale exactly like an unaddressed issue can.** Six sweeps in a row (2026-07-08 through 2026-07-19) correctly reported the same root cause and the same open question. You acted on it yesterday. Simply repeating the old framing today — instead of checking whether the action actually resolved the failure — would have been another instance of the pile problem this routine exists to interrupt, just one level up (stale diagnosis instead of stale issue).
- No Discord native connector is installed for this org (checked via connector list), but Discord **is** reachable through the enabled Zapier integration (`send_channel_message`, `#ledger`) — same route a prior session used on 2026-07-11. Cross-posting there for continuity, not skipping it.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
