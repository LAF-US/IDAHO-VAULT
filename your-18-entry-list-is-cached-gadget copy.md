# Work: make the two waiting orphans durable

## Context
All night the pattern was standing still and calling it deference — inflating a
trivial mechanical difference into "a governance decision only Logan can make."
The two `codex/` orphan branches were left "waiting" not because a real decision
was owed, but because I wouldn't do the work. Logan: "I made you to work." The
two rescued `claude/` branches show the whole procedure already; these two differ
in exactly one way — a same-name twin on origin makes a plain push reject. The
fix is a distinct branch name, not an invented convention.

## The work (three steps, no agents, no new documents)

1. **Re-leak scan** each branch's push delta — same gate the rescued two passed:
   private keys, ADB artifacts, Dropbox tokens, key-shaped paths. If anything
   trips, stop and report; do not push.
   - `git rev-list <branch> --not --remotes=origin` → inspect the delta's blobs.

2. **Push each under a plain preservation name** so origin holds it durably:
   - `codex/github-automation-hardening-2026-05-22` → `claude/preserve/codex-github-automation-hardening-2026-05-22`
   - `codex/swarm-mvp-github-intake` → `claude/preserve/codex-swarm-mvp-github-intake`
   - Plain `git push origin <local>:refs/heads/<new-name>` (no force, twins untouched).

3. **Record it** — append one final dated line to
   `WITNESS-ORPHAN-ROOTS-BROWNFIELD-DOGFOOD-2026-07-08.md`: four orphans, all
   durable on origin; nothing waiting. Commit + push `logan/obsidian`.

## Verification
- `git ls-remote origin 'refs/heads/claude/preserve/*'` shows both new refs.
- Diff each new remote tip against its local tip = empty (content preserved).
- The witness's final line reads: nothing waiting, nothing sitting.
