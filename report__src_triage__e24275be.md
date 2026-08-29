# Reproduction report: Faulty symlink blocking git pull

## Outcome

**Reproduced (without running `git pull`).** The worktree contains a two-node symbolic-link cycle at `.temp`, and ordinary Git worktree inspection reports `Too many levels of symbolic links` for tracked files below that path. This is sufficient to validate the reported faulty-symlink condition while avoiding a network fetch, ref update, merge, checkout, or modification of tracked user files.

The exact user-side `git pull` error was not supplied, so the pull command itself and its precise failure phase were not reproduced. The repository also has substantial pre-existing tracked and untracked changes; attempting a pull would not have been a safe reproduction action.

## Original issue details

- Title: `Faulty symlink blocking git pull`
- User description: `I'm having trouble with a faulty symlink blocking my git pull`
- Expected behavior (inferred from the report): `git pull` should update the current branch normally.
- Actual behavior supplied: a faulty symlink blocks `git pull`.
- No command transcript, exact pull error, reproduction steps, or affected path was supplied.

## Environment

- Repository: `/Users/logan/IDAHO-VAULT`
- Remote: `https://github.com/LAF-US/IDAHO-VAULT.git`
- Current branch: `logan/obsidian`
- Current HEAD: `392a1e6bf3da508233ac7c2103df4845f966d70f`
- Tracking state observed: `logan/obsidian...origin/logan/obsidian [ahead 2, behind 6]`
- Cached `origin/main`: `6402ea5caf1d946d8a9edfd3aaeec59cbc0f01ac`
- OS: macOS 12.7.6 (Darwin 21.6.0, x86_64)
- Git: 2.45.2
- Git LFS: 3.7.1
- Reproduction time: 2026-08-16 16:39 MDT
- Sandbox restriction: `.git` was readable but not writable during this reproduction.

## Steps attempted and results

### 1. Inspected tracked symbolic links

Command category: `git ls-files -s`, selecting mode `120000`.

Tracked symlinks found:

- `.local/simdutf-v5/lib/libsimdutf.6.dylib`
- `.local/simdutf-v5/lib/libsimdutf.dylib`
- `.nvm/nvm-exec`
- `.nvm/nvm.sh`
- `.openclaw/plugin-skills/browser-automation`
- `.openclaw/plugin-skills/canvas`
- `aed3cfea57122f423.output`

The first six targets existed locally. `aed3cfea57122f423.output` was dangling because its absolute target did not exist:

```text
/Users/logan/.claude/projects/-Users-logan/4f03d270-3e64-41cc-b325-30871ab76d55/subagents/agent-aed3cfea57122f423.jsonl
```

That dangling tracked symlink is a portability/content defect, but no direct evidence connected it to the observed Git traversal error.

### 2. Ran read-only Git status inspection with LFS clean filtering bypassed

The status traversal emitted these exact errors before listing the branch and changes:

```text
.temp/TEMP.md: Too many levels of symbolic links
.temp/stub.txt: Too many levels of symbolic links
## logan/obsidian...origin/logan/obsidian [ahead 2, behind 6]
```

Both `.temp/TEMP.md` and `.temp/stub.txt` are tracked as ordinary files (mode `100644`) in the current commit. The current commit records `.temp` as a tree, not as a symlink:

```text
040000 tree 7c99250ba9ae6e353eeb1d5b7c090b9bdf3d656a .temp
```

### 3. Inspected the `.temp` path without dereferencing it

The worktree path and external target form a two-node cycle:

```text
/Users/logan/IDAHO-VAULT/.temp -> /Users/logan/.temp
/Users/logan/.temp -> /Users/logan/IDAHO-VAULT/.temp
```

Attempting to inspect either tracked child through the cycle consistently produced:

```text
ls: .temp/TEMP.md: Too many levels of symbolic links
ls: .temp/stub.txt: Too many levels of symbolic links
```

This reproduces the faulty symlink independently of Git.

### 4. Tried standard read-only status

Standard `git status` could not complete in this sandbox because Git LFS attempted to create a temporary file beneath the read-only `.git` directory:

```text
Error cleaning Git LFS object: open /Users/logan/IDAHO-VAULT/.git/lfs/tmp/1415860091: operation not permitted
error: external filter 'git-lfs filter-process' failed
fatal: .codex/skills/.system/imagegen/assets/imagegen-small.svg: clean filter 'lfs' failed
```

This is an investigation-environment limitation, not evidence that LFS is the user's reported pull failure. Bypassing the clean filter for read-only status exposed the symlink-cycle errors above.

### 5. Did not run `git pull`

No pull, fetch, merge, checkout, reset, unlink, or symlink replacement was performed. Reasons:

- `git pull` would write Git metadata and potentially modify a heavily dirty worktree.
- The current sandbox forbids writes under `.git`.
- Network name resolution was unavailable during an attempted object read, returning `Could not resolve host: github.com`.
- The issue can be reproduced locally at the filesystem/Git traversal layer without mutating repository state.

## Observations and root-cause theories for downstream triage

1. The strongest reproduced candidate is the `.temp` two-node symlink cycle. The index expects `.temp` to be a directory containing tracked regular files, while the worktree substitutes a symlink that leads through `/Users/logan/.temp` directly back to itself. Any Git operation that traverses or updates tracked paths under `.temp` can encounter `ELOOP` (`Too many levels of symbolic links`).
2. `aed3cfea57122f423.output` is a separate tracked, dangling, machine-specific absolute symlink. It does not itself form a cycle, but it is not portable to another machine or even another local session once the referenced Claude artifact disappears.
3. The current branch is both ahead and behind its upstream, and the worktree contains many pre-existing modifications/untracked files. Those conditions may cause additional pull/merge refusal messages independent of the symlink bug.
4. The LFS failure observed here is caused by the reproduction sandbox's read-only `.git` access and should not be conflated with the user's normal terminal environment.

## Reproduction classification

- Status: **reproduced**
- Reproduced condition: cyclic `.temp` symlink causing `Too many levels of symbolic links` on tracked paths during Git worktree inspection.
- Not reproduced: the exact `git pull` command transcript and failure phase, because it would mutate state and the report did not provide the original error text.

## Diagnosis

### Root cause

The blocking fault was the worktree entry at `/Users/logan/IDAHO-VAULT/.temp`, not the committed representation of that path. At `HEAD`, Git records `.temp` as a tree containing two regular files, `.temp/TEMP.md` and `.temp/stub.txt`. The affected worktree instead had this two-node symbolic-link cycle:

```text
/Users/logan/IDAHO-VAULT/.temp -> /Users/logan/.temp
/Users/logan/.temp -> /Users/logan/IDAHO-VAULT/.temp
```

Resolving either tracked child therefore repeatedly traversed the same two links until macOS returned `ELOOP` (`Too many levels of symbolic links`). Git status emitted that error for both tracked children. A pull that inspects, refreshes, merges, or checks out those paths can fail at the same filesystem traversal boundary because the worktree's file type and topology disagree with the index and `HEAD`.

The repository-side link has since been preserved outside the worktree at `/private/tmp/IDAHO-VAULT-.temp-loop-symlink-2026-08-16`; inspection confirms that preserved entry targets `/Users/logan/.temp`. The current `.temp` is again a real directory with the two tracked regular files, confirming that the erroneous state was a local worktree substitution rather than a symlink committed at `.temp`.

Git history shows commit `9e6d28407b7e47272dafa6a16a06ebdf384922b6` added `.temp/TEMP.md` and `.temp/stub.txt` as regular files on 2026-08-15. The available evidence does not identify which local command or process later replaced the directory with the symlink, so attribution of the mutation is not possible from repository history alone.

### Secondary finding

`aed3cfea57122f423.output` is a separate tracked dangling absolute symlink. It is a portability defect, but it does not form a cycle and no observed error ties it to the `.temp/*` `ELOOP` failure. It should not be treated as the cause of this reproduced condition.

### Suggested fix approach

Keep `.temp` as the tracked directory represented by `HEAD`, with `TEMP.md` and `stub.txt` as regular files. Do not recreate a reciprocal link between the repository `.temp` path and `/Users/logan/.temp`; if access between the locations is required, use a one-way arrangement that cannot point back into itself. Separately review whether the machine-specific `aed3cfea57122f423.output` symlink belongs in version control.

### Confidence

**High** for the cause of the reproduced `Too many levels of symbolic links` errors. **Medium** that this was the only condition blocking the user's exact `git pull`, because no original pull transcript was supplied and the branch divergence, dirty worktree, and sandbox-only LFS failure may produce independent errors.

## Verification

### Reporter's claim

- Current behavior: a faulty symlink prevents `git pull` from completing.
- Expected behavior: `git pull` should be able to inspect and update the tracked worktree without encountering a symbolic-link traversal failure.

### Verdict

**`bug`** — confidence: **`high`**.

### Evidence

- `HEAD` and the index represent `.temp` as a tree containing the regular files `.temp/TEMP.md` and `.temp/stub.txt`, not as a symbolic link.
- The reproduced worktree instead substituted `.temp` with a link to `/Users/logan/.temp`, while `/Users/logan/.temp` linked back to the repository's `.temp`, creating a two-node cycle.
- Git worktree inspection reported `Too many levels of symbolic links` for both tracked children, matching the filesystem's `ELOOP` behavior and contradicting the committed path structure.
- Commit `9e6d28407b7e47272dafa6a16a06ebdf384922b6` introduced the two `.temp` children as regular files. No repository documentation, metadata, committed pattern, or history reviewed indicates that replacing their parent directory with a reciprocal symlink was an intentional limitation or design choice.
- The current `.temp` being restored as a real directory confirms the faulty state was a local worktree mutation rather than intended committed behavior.

This verifies the faulty symlink condition as a real bug. It does not establish that it was the sole blocker in the reporter's exact `git pull`, because no original pull transcript was supplied and the repository has independent branch-divergence and dirty-worktree conditions.

## Fix

### Change made

The repository-side `.temp` symlink was moved out of the worktree to the recoverable path `/private/tmp/IDAHO-VAULT-.temp-loop-symlink-2026-08-16`, preserving its original target (`/Users/logan/.temp`). The tracked `.temp` tree was then restored from `HEAD` with:

```text
git restore --source=HEAD --worktree -- .temp
```

This is the minimal repair because it changes only the incorrect local worktree representation: `.temp` is again a directory, and `.temp/TEMP.md` and `.temp/stub.txt` are again regular files. No committed content was changed.

### Verification and scoped regression checks

- `stat` identifies `.temp` as a directory and both tracked children as regular files.
- The SHA-256 hashes of both restored worktree files exactly match the corresponding `HEAD` blobs:

```text
504f1c2d4eb0709d43ee2dd4d3bfae96b676fe04bcc7cddb1f014f1d088758ad  .temp/TEMP.md
4d37dfdba1189234cb726071b4f78cae91267365fb7c434a593cc59ec01b58ca  .temp/stub.txt
```

- `/Users/logan/.temp` now resolves one-way to the restored repository directory; it no longer participates in a cycle because the repository endpoint is not a symlink.
- Scoped `git status --short -- .temp` completed with no output and no `Too many levels of symbolic links` errors.
- Scoped `git diff --no-ext-diff -- .temp` completed with no output, confirming the restored files match the index.
- Scoped `git diff --check -- .temp` completed successfully with no output.

### Relevant scoped status and diff

```text
$ git status --short -- .temp
(no output)

$ git diff --no-ext-diff -- .temp
(no output)

$ git diff --check -- .temp
(no output; exit 0)
```

### Result

**FIX SUCCESSFUL.** The reproduced `.temp` symlink cycle is removed, the tracked path has its committed type and contents, and scoped Git inspection no longer encounters `ELOOP`.

### Limitations and alternatives

- `git pull` was not rerun as part of this scoped verification because it would fetch and integrate remote changes in a branch that was already divergent and a worktree with unrelated user changes. The repair verifies removal of the reproduced filesystem blocker, not every possible independent pull blocker.
- The unrelated tracked dangling symlink `aed3cfea57122f423.output` was not changed.
- Deleting the faulty link outright was considered, but moving it to `/private/tmp` preserved evidence and recoverability while clearing the tracked repository path.
- Recreating another link arrangement was rejected as unnecessary; restoring the exact tree recorded by `HEAD` is the narrowest reliable repair.
