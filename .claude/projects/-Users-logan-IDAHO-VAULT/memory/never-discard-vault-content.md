---
name: never-discard-vault-content
description: "Standing rule: never delete anything from IDAHO-VAULT — preserve, relocate, or ignore, but do not discard"
metadata:
  type: feedback
---

Logan's standing instruction (2026-08-21): **"Do not discard ANYTHING."** Applies
to vault content without exception — including material that looks like pure
debris: `.trash/` collision artifacts (`! copy 10.md.md`, `(WIN)` suffixes,
`(2)`/`(3)` duplicates), `node_modules`, caches, agent state, orphaned commits.

**Why:** This vault has lost material repeatedly — two secret purges that severed
history, dropped stashes, a flatten that had to be reversed twice, 139 GB rescued
back out of the Trash by an agent. "Obviously junk" has been wrong here before;
`.trash/` turned out to hold mangled copies of real documents, not unrelated
garbage. Logan is the only one who decides what stops existing.

**How to apply:** The available moves are **preserve in place**, **relocate**
(e.g. `mv` out of the repo — instant on the same APFS volume, frees no space but
removes it from git's reach), or **gitignore** (stops tracking, keeps the file).
Never `rm`, never `git gc --prune`, never `git lfs prune`, never accept a
duplicate-finder's or cleaner's selection. If disk space is the pressure, the
answer is copying to external media, not deletion. Propose; do not execute.
See [[macbook-is-transitional-vault-host]], [[vault-history-grafts]].
