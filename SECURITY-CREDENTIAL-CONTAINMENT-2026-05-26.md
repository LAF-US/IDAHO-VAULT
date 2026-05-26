---
title: OpenClaw Gateway Credential Containment - 2026-05-26
updated: 2026-05-26
status: rotation-required
authority: LOGAN
---

# OpenClaw Gateway Credential Containment

A literal OpenClaw gateway authentication token was found in tracked
configuration introduced on April 24, 2026. Its value is intentionally omitted
from this record.

## Containment

- The current tracked configuration now uses a runtime secret reference only.
- Secret-scanning coverage now includes quoted JSON credential assignments and
  previously skipped NUL-containing or large content.
- The unreviewed root MCP bridge, exported assistant session residue, local
  machine configuration artifacts, and tracked OpenClaw launcher helper are
  removed from the proposed live tip.
- GitHub ruleset `16864823` now requires an approving review for changes to
  `main` and blocks deletion and force-push while containment remains open.
- Unattended direct-write, broad auto-merge, unsafe cleanup, and retired
  notification workflow registrations were manually suspended on May 26.
- A read-only local status check confirmed that an OpenClaw gateway was
  running on loopback with token authentication and an enabled Discord
  channel. It was stopped and uninstalled; generated startup/backup residue
  was removed, stored gateway and Discord credential fields were replaced with
  environment-backed references, and Discord policy is set to `allowlist`.
- Public git history is not rewritten by this remediation.

## Required Before Restart Or Redeployment

The local running gateway has been contained, but the former credential may
remain valid in git history, copied state, or another installation. Revoke or
rotate it in the authoritative runtime or secret provider before any OpenClaw
restart or redeployment, then confirm the runtime resolves the replacement
reference without committing any secret value. Landing this remediation
removes the literal credential from the current repository tip and should not
be delayed by that out-of-band rotation.
