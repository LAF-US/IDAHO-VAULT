# Reunify Mac ↔ Windows vault histories (`logan/obsidian`)

## Context

Since **May 26** (merge-base `709965f1`), the home MacBook and work Windows machine have committed independently to `logan/obsidian`: local is **ahead 1,919** commits (tip `526b9757`), remote **ahead 2,028** (tip `6b6ce454`). Both lines contain valuable work; Logan has decided to **merge, preserving everything**, with these policies already chosen:

- **Byte-identical duplicates under different names → keep both copies.**
- **Same-name files with differing content → keep both, Windows copy suffixed** (e.g. `NOTE.md` + `NOTE (WIN).md`).

### Relationship to `main` (measured, not assumed)

Both lines also differ from `main`, but **asymmetrically**:

- **Windows line** (`origin/logan/obsidian`) is main-tracked: merge-base with `origin/main` is **Aug 4** (`0bce7237`); today it is only **78 ahead / 288 behind** `origin/main`.
- **Mac line** has been isolated from *everything* since **May 26**: same stale merge-base (`709965f1`) against both the Windows line and `origin/main`; it is 1,919 ahead / **2,238 behind** `origin/main`. (No local `main` branch exists on this Mac at all.)

Consequence: reunifying the two `logan/obsidian` lines **implicitly absorbs main through Aug 4**. After this merge, catching up with `origin/main` is an ordinary ~288-commit merge — a separate, later, much smaller step (Phase 4 follow-up), not a second monster.

A conventional working-tree merge is a dead end, proven empirically this session:

1. **Illegal filenames**: ≥28 remote-side paths contain byte sequences APFS rejects (`Illegal byte sequence`) — checkout can never succeed on this Mac until they're renamed.
2. **Scale**: checkout of ~36k files exceeded the 10-minute command limit and was killed mid-flight, leaving the worktree damaged (see "Current damage").
3. **Ref ambiguity footgun**: a tracked file literally named `HEAD` exists at repo root on both branches, so `git reset --hard HEAD` fails. All commands must use explicit refs (`refs/heads/…`).
4. This is Logan's **live Obsidian vault** — large working-tree churn while Obsidian runs is risky.

**Strategy: build the merge commit entirely in a temporary index — never touching the working tree** — then verify it via a throwaway `git worktree` checkout before anything touches the live vault.

### Facts established (this session, read-only trial merge)

`git merge-tree --write-tree` succeeds (tree `dadd5028`), with **1,156 conflicts over ~1,690 paths**:

| Type | Count | Resolution per policy |
|---|---|---|
| add/add | 555 | keep both: path = Mac blob, ` (WIN)` suffix = Windows blob |
| rename/rename | 525 (487 identical, 38 differ) | both names already land in merged tree — keep both (verify) |
| content (both edited) | 18 | keep both, suffixed; **special-case `.github/workflows/`** (see below) |
| modify/delete | 22 | keep the modified version (preservation) |
| rename/delete | 7 | keep the renamed version |
| file location | 26 | accept ort's auto-placement |
| implicit dir rename | 3 | informational only |

### Current damage to repair first

The killed merge left (vs. branch tip): **1,173 tracked files deleted**, **7,057 tracked files modified**, **36,637 untracked** (pre-existing junk *plus* merge debris written from remote blobs). Index is clean (0 unmerged). HEAD is on new branch `claude/reunify-mac-win-6c80a94c` (== `logan/obsidian` tip). 8 untracked artifacts (5 `.pyc`, 1 log, 2 ollama manifests) already moved to scratchpad `displaced-untracked/`.

Disk: 194 GB free; `.git` = 10 GB → scratch worktree for verification is feasible.

---

## Execution plan

All scripts are written to the session scratchpad as reviewable files **before** running, use git plumbing only, and every destructive step runs **dry-run first** with a printed summary.

### Phase 0 — Safety net (cheap, reversible)

1. Logan quits Obsidian on this Mac (or disables the obsidian-git plugin) for the duration — prevents auto-commits/indexing racing us.
2. Snapshot all refs: `git for-each-ref > scratchpad/refs-before.txt`.
3. Backup branch: `git branch backup/logan-obsidian-pre-reunify-20260812 refs/heads/logan/obsidian`.

### Phase 1 — Repair the working tree

1. `git reset --hard refs/heads/claude/reunify-mac-win-6c80a94c` — **explicit ref** (the `HEAD`-file ambiguity). Restores the 1,173 deleted + 7,057 modified tracked files. Backgrounded if slow.
2. **Debris sweep** (`scratchpad/sweep_debris.py`): delete an untracked file **only if** its content hash exactly equals the blob at the same path in `origin/logan/obsidian` (provably re-creatable from git objects). Mechanism: `git ls-files --others --exclude-standard -z` → `git hash-object --stdin-paths` → compare against `git ls-tree -r -z origin/logan/obsidian` map. Dry-run prints counts + samples for review before the deleting pass. Pre-existing junk (`.cargo/`, `.codex/`, caches) doesn't match remote blobs and is untouched. Prune only directories the sweep emptied.

### Phase 2 — Build the merge commit in a temp index (worktree untouched)

Script `scratchpad/build_merge.py`, operating with `GIT_INDEX_FILE=<scratchpad>/merge-index`:

1. Re-run `git merge-tree --write-tree -z` for NUL-delimited, machine-parseable conflict records (filenames here contain spaces/emoji/parens — never parse the human format).
2. `git read-tree <merged-tree>` into the temp index.
3. Apply policy fixups via `git update-index --index-info` (batch, NUL-safe):
   - **add/add + content conflicts**: replace ort's conflict-marker blob: path ← `logan/obsidian:path` blob; `name (WIN).ext` ← `origin/logan/obsidian:path` blob. Under `.github/workflows/`, the WIN copy is named `name (WIN).yml.txt` so GitHub Actions never executes a forked workflow.
   - **rename/rename & modify/delete & rename/delete**: verify expected survivors are present in the tree (no action expected; assert).
   - **Invalid-UTF-8 path scan** over the *entire* merged tree: rename offending index entries (invalid bytes → `_`), consistent with the NETWEB portable-path standard. Record every mapping.
   - **Case-insensitive collision scan** (APFS/NTFS would silently clobber): resolve with NETWEB `_`-prefix aliasing; report count.
   - Write `MERGE-MANIFEST-2026-08-12.md` (list of every suffixed, sanitized, or aliased path + policy statement) and add it to the commit's tree.
4. **Lossless assertion (hard gate)**: every blob reachable in *either* parent tree must be reachable in the merged tree (at its path or its mapped path). Script aborts before committing if any blob is lost.
5. `git write-tree` → `git commit-tree <tree> -p 526b9757 -p 6b6ce454` with a message documenting the policies, plus trailers:
   - `Claude-Session: https://claude.ai/code/session_6c80a94c-6802-46ff-8526-0575213a0ec1`
   - `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
6. Ref choreography (ordering matters): first `git switch logan/obsidian` (no-op checkout, identical tree — moves HEAD off the reunify branch), **then** `git update-ref refs/heads/claude/reunify-mac-win-6c80a94c <merge-commit>`. The live vault never sees a checkout.

### Phase 3 — Verification

1. **Scratch worktree proof**: `git worktree add --no-checkout <scratchpad>/verify-checkout claude/reunify-mac-win-6c80a94c` + background checkout. Proves APFS accepts every filename post-sanitization and measures real checkout time. Then `git worktree remove`.
2. `git ls-files -u` (temp index) == 0; `git log -1 --stat` sanity; spot-check one sample from each conflict class (identical-pair kept twice, add/add pair split, workflow special-case, sanitized filename).
3. Diff-stat merged tree vs. each parent; confirm counts line up with the conflict census.

### Phase 4 — Handoff (requires Logan's explicit go; not executed by default)

- Push `claude/reunify-mac-win-6c80a94c` to origin and open a PR per vault convention (**ask first** — outward-facing), or
- Locally fast-forward `logan/obsidian` to the merge commit and run the (backgrounded) live-vault checkout, then Windows pulls.
- **Follow-up (separate task): catch up with `origin/main`** — after reunification this is an ordinary merge (~288 commits behind / 78+1,919 ahead), reviewed on its own.

## Rollback

- `logan/obsidian` and origin are never modified by Phases 0–3.
- Backup branch pins the pre-merge tip; `refs-before.txt` snapshots everything else.
- All Phase-2 work is new objects + one branch ref move; deleting the branch fully undoes it.
- The only worktree mutations are Phase 1's repair (restoring files the killed merge damaged) and the hash-verified debris sweep.

## Files/scripts

- `scratchpad/sweep_debris.py` — new, dry-run-first, hash-verified deletion only.
- `scratchpad/build_merge.py` — new, plumbing-only, temp index, hard lossless gate.
- `MERGE-MANIFEST-2026-08-12.md` — new vault file inside the merge commit.
- No existing vault files are edited by hand.

## Note

The designated plan path `~/.claude/plans/` was unwritable: `~/.claude` carries the macOS `uchg` (user-immutable) flag, set Jul 8 — presumed deliberate agent containment; not overridden.
