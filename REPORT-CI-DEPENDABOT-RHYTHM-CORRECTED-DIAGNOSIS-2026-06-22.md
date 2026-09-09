---
title: "Corrected Diagnosis — Dependabot Rhythm startup_failure"
updated: 2026-06-22
status: active
authority: LOGAN
related:
  - GitHub Actions
  - CI
  - dependabot
  - pull_request_target
  - startup_failure
  - LAF-53
---

# Corrected Diagnosis — Dependabot Rhythm `startup_failure`

**Issued by:** GitHub Copilot
**Date:** 2026-06-22
**Related issues:** #595 (LAF-53), #633
**File repaired:** `.github/workflows/dependabot-rhythm.yml`

---

## Original (Incomplete) Diagnosis

Issue #595 / LAF-53 (filed 2026-06-20) listed two root-cause candidates for
`startup_failure` on `.github/workflows/dependabot-rhythm.yml`:

1. **Org-level `pull_request_target` permission policy** — org policy blocking
   the `contents: write` elevation on bot-actor PRs.
2. **Stale action SHA** — `dependabot/fetch-metadata@25dd0e34f…` no longer
   resolvable upstream.

The report also elevated the issue from P3 to P1 when the workflow began
failing on a **real Dependabot PR** (#589), not just on non-Dependabot
agent branches.

## Corrected Diagnosis

Issue #633 (CI Health Report, 2026-06-22) refined the root cause:

**The workflow declares `permissions: contents: write, pull-requests: write`
at the workflow level.** GitHub's security model for `pull_request_target`
blocks workflow _startup_ for non-Dependabot actors when elevated write
permissions are declared at the workflow level — the `if:` guard on the job
(`github.event.pull_request.user.login == 'dependabot[bot]'`) is never
reached because the workflow never starts.

This is distinct from both original candidates:

- Not an org policy issue — it is GitHub's built-in fork-PR privilege
  escalation prevention on `pull_request_target` + write permissions.
- Not a stale SHA — the action reference is intact.

The fix is to move `permissions` from the workflow level to the individual
job level. This allows the workflow to start for any actor (minimal default
permissions), while only the jobs that actually run (after the Dependabot
actor check) carry elevated permissions.

## Repair Applied

Moved `permissions: contents: write, pull-requests: write` from the
workflow level to each of the two jobs (`auto-merge-low-risk` and
`disable-high-risk-auto-merge`). The actor/bot `if:` conditions on both
jobs remain unchanged.

**Noise eliminated:** `startup_failure` on every non-Dependabot PR push
that previously triggered two noisy failed runs per push event.

---

_Filed by GitHub Copilot · 2026-06-22_
_See also: Issue #595 (LAF-53), Issue #633_
