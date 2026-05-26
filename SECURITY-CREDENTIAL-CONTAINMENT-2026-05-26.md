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
- Public git history is not rewritten by this remediation.

## Required Before Merge

The former credential could not be safely proven obsolete from this repository
checkout. Revoke or rotate the gateway credential in the authoritative runtime
or secret provider, then confirm the runtime resolves the replacement reference
without committing any secret value.
