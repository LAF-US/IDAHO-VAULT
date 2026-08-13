authority: LOGAN
related:
  - GITHOOKS
  - Git
  - runtime
---
<<<<<<< HEAD
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

Without it, git reads `.git/hooks/` and **none of these gates run**. That is the
only per-machine wiring required — the `pre-push` trufflehog leg runs in
**filesystem mode** (scans the changed files directly), so it needs no clone,
no `core.longpaths`, and no LFS smudge.

## What runs here

| hook | job |
|---|---|
| `pre-commit` | gitleaks scan of the staged set — secrets never enter a commit. Fails closed if gitleaks is missing. |
| `pre-push` | per-ref, in order: **(0) size gate** — blocks files GitHub would reject (non-LFS >100 MiB, LFS >2 GiB on Free/Pro; warns >50 MiB), scoped to the range's new objects; **(1) gitleaks** scans the full outgoing commit range (offline); **(2) trufflehog** scans the range's changed files in filesystem mode (verified, gates on verified+unknown); then chains `git lfs pre-push`. Fails closed on oversized file, missing engine, or scan error. |
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
=======

**.githooks** — Git hook runtime persona.

Tracked anchor for VAULT hook files and hook-adjacent notes.

This anchor is not a setup contract. It does not declare coordination state,
office, checkout activation, or operational status.

Read the hook files themselves for implementation details.
>>>>>>> 684896b8a3040118f438cf44b6f39191676d9845
