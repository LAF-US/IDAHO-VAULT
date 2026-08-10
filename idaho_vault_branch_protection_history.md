---
name: idaho_vault-branch-protection-history
description: Why branch protection is off on IDAHO-VAULT main — softlock history and remediation constraints
metadata: 
  node_type: memory
  type: project
  originSessionId: 7016a42c-36e8-4e7e-8823-72c9034d2389
---

Branch protection on `main` was disabled as a **forced necessity**, not a preference. Logan wants protection ON, but on a reliable foundation. The softlock was caused by agents repeatedly adding workflows and required checks without reading what already existed. The required-check queue became broken or contradictory, PRs couldn't pass, nothing could merge — so Logan removed protection to unblock work.

**2026-05-26 update:** CODEX's hardening sweep added ruleset `Containment: gated PRs to main (2026-05-26)` (id 16864823). It re-enabled protection but did the very thing this memory warns against: required `submit-pypi` (known-noise, always fails — see [[idaho_vault_submit_pypi_noise]]) and set `current_user_can_bypass: never`. Result: another softlock. CODEX was *supposed* to deliver a working protected-main state; it didn't.

The emergency exit: `sync-dependencies.yml` contains a "temporary direct-main emergency corridor" comment documenting this. It writes directly to main without a PR. It has not been removed because the underlying problem was never addressed.

**Why protection is still off:** Turning it back on blindly re-creates the softlock. Remediation requires:
1. Audit which checks pass reliably on clean pushes (no flapping)
2. Designate a minimal required set — only load-bearing, consistently-green checks
3. Re-enable protection with only those checks
4. Remove the direct-main corridor in sync-dependencies.yml
5. Decide agent/* prefix policy (currently not covered by auto-PR trigger)

**The pattern:** Same as the orphaned-scripts governance failure — agents optimize for building (demonstrable) not for integration (requires reading the existing system). At the workflow level this created check-queue bloat that deadlocked the repo.

**Do NOT:** propose "just turn protection back on" without first verifying which checks pass consistently. That's the re-softlock path.

Related: [[feedback_no_demiurging]], [[idaho_vault_race_conditions]]
