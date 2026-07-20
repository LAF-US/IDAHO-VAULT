---
title: "GITHOOKS"
updated: 2026-07-20
status: active
authority: LOGAN
related:
  - GIT
  - GITHOOKS
  - GIT-LFS
  - GITHUB-DESKTOP
tags:
  - tooling/git/hooks
  - runtime/git
---

# GITHOOKS

`.githooks/` is the tracked Git hook runtime for IDAHO-VAULT.

This is a tooling dotfolder, not an agent persona chamber. Its live authority is
the repository Git configuration: `core.hooksPath=.githooks`.

Files under `.git/hooks/` are local Git installation residue unless
`core.hooksPath` is changed. They must not be treated as separate hook policy.

Keep hook behavior in one of two places:

- the live tracked hook files under `.githooks/`
- the canonical guard scripts those hooks call, such as `.github/scripts/`

Do not maintain parallel local hook copies.
