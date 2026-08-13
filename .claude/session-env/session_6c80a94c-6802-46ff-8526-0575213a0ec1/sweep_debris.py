#!/usr/bin/env python3
"""Hash-verified debris sweep (Phase 1.2 of reunify plan).

Deletes an untracked file ONLY if its content hash exactly equals the blob
recorded at the same path in origin/logan/obsidian — i.e. it is provably a
byproduct of the killed merge checkout and fully re-creatable from git
objects. Everything else is left untouched.

Usage:
    python3 sweep_debris.py            # dry run (default): report only
    python3 sweep_debris.py --execute  # delete after re-verifying each hash
"""
import os
import subprocess
import sys

REPO = "/Users/logan/IDAHO-VAULT"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
REMOTE_REF = "origin/logan/obsidian"
EXECUTE = "--execute" in sys.argv


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}... failed: {r.stderr[:500]}")
    return r.stdout if binary else r.stdout.decode("utf-8", "surrogateescape")


def main():
    # 1. Paths tracked in the CURRENT branch's index (never touched).
    ours_tracked = set(git("ls-files", "-z", binary=True).split(b"\x00"))
    ours_tracked.discard(b"")

    # 2. Full path -> (mode, sha) map of the remote tree.
    origin_map = {}
    out = git("ls-tree", "-r", "-z", REMOTE_REF, binary=True)
    for rec in out.split(b"\x00"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, otype, sha = meta.split(b" ")
        if otype == b"blob":
            origin_map[path] = (mode, sha.decode())

    # 3. Candidates: origin-tracked paths that exist on disk but are NOT
    #    tracked locally (== written by the killed merge, or pre-existing).
    candidates, skipped_symlinks = [], []
    for path, (mode, sha) in origin_map.items():
        if path in ours_tracked:
            continue
        fs = os.path.join(REPO, os.fsdecode(path))
        if not os.path.lexists(fs):
            continue
        if os.path.islink(fs) or mode == b"120000":
            skipped_symlinks.append(path)
            continue
        candidates.append((path, sha, fs))

    print(f"origin-tracked paths: {len(origin_map)}")
    print(f"candidates on disk (untracked locally): {len(candidates)}")
    print(f"symlinks skipped: {len(skipped_symlinks)}")

    # 4. Hash every candidate in one batch. --stdin-paths is LF-delimited
    #    (no -z in git 2.45), so paths containing a newline are skipped.
    if not candidates:
        print("nothing to do")
        return
    nl_paths = [c for c in candidates if b"\n" in c[0]]
    if nl_paths:
        print(f"paths containing newline skipped: {len(nl_paths)}")
        candidates = [c for c in candidates if b"\n" not in c[0]]
    proc = subprocess.run(
        ["git", "-C", REPO, "hash-object", "--stdin-paths"],
        input=b"\n".join(fs.encode() for _, _, fs in candidates) + b"\n",
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[:500])
    hashes = proc.stdout.decode().split()
    assert len(hashes) == len(candidates), "hash count mismatch"

    matches, mismatches = [], []
    for (path, sha, fs), actual in zip(candidates, hashes):
        (matches if actual == sha else mismatches).append((path, fs, sha, actual))

    print(f"MATCH  (hash == origin blob, safe to delete): {len(matches)}")
    print(f"DIFFER (kept — content is not origin's):      {len(mismatches)}")

    with open(os.path.join(SCRATCH, "sweep-plan.txt"), "wb") as f:
        for path, *_ in matches:
            f.write(path + b"\n")
    with open(os.path.join(SCRATCH, "sweep-kept.txt"), "wb") as f:
        for path, *_ in mismatches:
            f.write(path + b"\n")
    print(f"full lists: {SCRATCH}/sweep-plan.txt, sweep-kept.txt")

    for label, rows in (("sample deletions", matches[:8]), ("sample kept", mismatches[:8])):
        print(f"--- {label} ---")
        for path, *_ in rows:
            print("  " + os.fsdecode(path))

    if not EXECUTE:
        print("\nDRY RUN — nothing deleted. Re-run with --execute to sweep.")
        return

    # 5. Delete, re-verifying each hash immediately before unlink.
    deleted, raced, dirs = 0, 0, set()
    for path, fs, sha, _ in matches:
        p = subprocess.run(
            ["git", "-C", REPO, "hash-object", "--", fs], capture_output=True
        )
        if p.returncode != 0 or p.stdout.decode().strip() != sha:
            raced += 1
            continue
        os.unlink(fs)
        deleted += 1
        dirs.add(os.path.dirname(fs))

    # 6. Prune only directories the sweep emptied (walk upward).
    pruned = 0
    for d in sorted(dirs, key=len, reverse=True):
        while d.startswith(REPO) and d != REPO:
            try:
                os.rmdir(d)  # fails unless empty — that's the guard
                pruned += 1
                d = os.path.dirname(d)
            except OSError:
                break

    print(f"\ndeleted: {deleted}  changed-since-scan (kept): {raced}  dirs pruned: {pruned}")


if __name__ == "__main__":
    main()
