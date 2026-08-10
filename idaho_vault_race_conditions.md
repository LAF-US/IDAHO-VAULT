---
name: idaho-vault-race-conditions
description: "IDAHO-VAULT GitHub automation has recurring race conditions when batched events land simultaneously (Dependabot PR storms, parallel workflow runs). Check for races first when \"stuck\" PRs / jobs appear."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4ebcc146-08af-4d98-8ba6-b8b3b366018d
---

IDAHO-VAULT automation suffers recurring race conditions when multiple events land near-simultaneously. Dependabot PR storms are the canonical case: 8 PRs opening in 30 seconds, each triggering its own `pull_request_target` workflow run that races to merge `main`.

**Why:** Workflows like [[dependabot-rhythm]] do an immediate `gh pr merge --auto --squash` rather than just enabling auto-merge and stepping back. When the first PR wins, the rest die with `GraphQL: Base branch was modified. Review and try the merge again.` — and they die *before* auto-merge is registered, so they sit OPEN with no mechanism to retry.

**How to apply:**
- When stuck/failed GitHub automation is reported (especially "stuck Dependabot PRs," "auto-merge didn't work," "this PR should have merged"), check for race condition before assuming logic bug or permissions issue.
- Diagnostic signature: `gh run view <id> --log-failed` showing `Base branch was modified` or similar GraphQL conflict errors near the end of an otherwise-successful job.
- Durable fixes follow a pattern: (a) enable auto-merge before attempting immediate merge, (b) treat base-modified errors as non-fatal, (c) add a periodic reaper/cron workflow to re-enable auto-merge on stragglers.
- Suspect the same pattern in other batched IDAHO-VAULT automations (branch cleanup, sort-audit, daily-rollover) when they misbehave.
