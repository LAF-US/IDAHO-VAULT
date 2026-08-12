---
title: GITHOOKS
authority: LOGAN
related:
  - GIT-CONTROL-SURFACES-2026-05-17
  - .gitattributes
  - .gitignore
---

# .githooks — enforcement backstop

Hooks are per-machine wiring: `core.hooksPath` cannot be committed. On every
machine / fresh clone, bootstrap once (idempotent):

```
git config core.hooksPath .githooks
```

Without it, git reads `.git/hooks/` and **none of these gates run**.

The `pre-push` trufflehog leg full-clones the repo to a temp dir; on this vault
(84k files, ~200-char filenames) that checkout fails without long-path support.
Enable it once, per machine:

```
git config --global core.longpaths true
```

Without it the clone errors and `pre-push` **fails closed** (blocks the push) —
safe, but every push is blocked until this is set. (The hook itself already
sets `GIT_LFS_SKIP_SMUDGE=1` so the clone copies LFS pointers, not 13 GB of
media.)

## What runs here

| hook | job |
|---|---|
| `pre-commit` | gitleaks scan of the staged set — secrets never enter a commit. Fails closed if gitleaks is missing. |
| `pre-push` | per-ref outgoing-range scan: gitleaks (offline backstop) + trufflehog (verified mode, gates on verified+unknown), then chains `git lfs pre-push`. Fails closed on missing engine or scan error. |
| `post-checkout` / `post-commit` / `post-merge` | stock Git LFS shims (smudge/maintenance). |
| `*.sample` | git's stock templates, kept deliberately as inert reference seeds. |

Engines are per-machine dependencies (`scoop install gitleaks trufflehog` here;
brew/apt elsewhere). Absence BLOCKS — a silently-skipped secret gate is worse
than no gate at all.

## Git LFS coexistence (verified against git-lfs 3.6.1)

Plain `git lfs install` / `git lfs update` silently upgrades hook files whose
content it *recognizes* (the stock shims) and **refuses — errors, does not
overwrite —** on content it doesn't recognize, such as our custom `pre-push`.
That error is expected and safe. Answer it with:

- `git lfs install --skip-repo` — (re)asserts the `filter.lfs.*` config without
  touching any hook file, or
- `git lfs update --manual` — prints instructions, writes nothing.

**Never run `git lfs install --force` or `git lfs update --force` in this
repo.** That is the only path that silently replaces the pre-push secret gate
with the stock shim.

## Positive controls — a gate is believed only after it blocks

Wiring: `git config core.hooksPath` → must print `.githooks`.

pre-commit (expect BLOCKED, then clean up):

```
printf 'aws_access_key_id = AKIAQZKPXVJWMNBTUCRD\n' > CANARY-DELETE-ME.txt  # gitleaks:allow (doc canary)
git add CANARY-DELETE-ME.txt && git commit -m canary
git restore --staged CANARY-DELETE-ME.txt && rm CANARY-DELETE-ME.txt
```

(Random canary on purpose — AWS's documented example key may be allowlisted by
default configs.)

pre-push (expect BLOCKED before any transfer; fixture built with plumbing so
no gate is bypassed constructing it):

```
blob=$(printf 'id=AKIAQZKPXVJWMNBTUCRD\n' | git hash-object -w --stdin)  # gitleaks:allow (doc canary)
tree=$(printf '100644 blob %s\tCANARY.txt\n' "$blob" | git mktree)
c=$(git commit-tree "$tree" -p HEAD -m 'canary: secret-gate positive control - never merge')
git branch tmp/secret-canary "$c"
git push origin tmp/secret-canary:refs/heads/tmp/secret-canary
git branch -D tmp/secret-canary
```

Per `GIT-CONTROL-SURFACES-2026-05-17.md`: these are guardrails. Do not bypass
them to make a blocked operation succeed.

# ---------------------------------------------------------------
# THE WORLD IS QUIET HERE．ESTO PERPETUA!
# ---------------------------------------------------------------
