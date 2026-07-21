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

`.githooks/` is the tracked source for IDAHO-VAULT repository hook policy.

This is a tooling dotfolder, not an agent persona chamber.

Git decides the active hook runtime from local configuration:

- If `git config --local --get core.hooksPath` prints `.githooks`, these
  tracked hook files are active for this checkout.
- If `core.hooksPath` is unset, Git uses `.git/hooks/`. In that state,
  `.git/hooks/` should contain generated local runtime hooks only, normally
  the stock hooks installed by `git lfs install --local`.

Do not maintain two competing policy surfaces. The rule is:

- repository policy lives in `.githooks/` and canonical guard scripts such as
  `.github/scripts/`
- `.git/hooks/` is local generated runtime state, not a place for custom vault
  policy
- do not copy or hand-edit alternate versions of these hooks under `.git/hooks/`

Git LFS is not custom vault policy. GitHub Desktop includes Git LFS, but a
repository still needs Git LFS configured so a pre-push hook uploads referenced
objects before GitHub accepts the Git push. The tracked `pre-push` hook delegates
that upload to the stock `git lfs pre-push` command instead of reimplementing
LFS upload behavior.

No hook fix requires editing GitHub Desktop application files or administrator
rights.
