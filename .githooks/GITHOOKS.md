---
title: GITHOOKS
related:
  - .gitattributes
  - .gitboss
  - .gitconfig
  - .gitignore
  - .gitkeep
  - .githooks
  - .gitlight
  - .gitmodules
---

# Git Hooks

`core.hooksPath` points to this tracked directory. Hooks are composed here;
running an installer with `--force` must never replace them.

## Storage composition

- `pre-commit` lets git-annex finalize explicitly attributed pointers when
  annex is initialized, validates the Git/LFS/annex ownership boundary, then
  runs the secret gate.
- `pre-push` validates committed ownership before delegating the untouched
  push-ref stream to `git lfs pre-push`.
- `post-checkout` and `post-merge` run Git LFS first, then refresh unlocked
  annex content when the clone is annex-enabled.
- `post-commit` remains the Git LFS hook; git-annex records its own metadata
  through `git annex pre-commit` and the `git-annex` branch.

The annex bootstrap diverts annex's generated hooks into a temporary private
directory during initialization. This prevents `git annex init` from replacing
these composed tracked hooks.
