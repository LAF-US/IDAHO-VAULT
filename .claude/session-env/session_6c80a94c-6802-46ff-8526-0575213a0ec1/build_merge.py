#!/usr/bin/env python3
"""Build the Mac<->Windows reunification merge commit in a temp index.

Never touches the working tree or any ref. Output: a commit object SHA
(printed and written to merge-commit.txt). Ref choreography happens
outside this script, after review.

Policies (approved by Logan):
  - keep-both for byte-identical duplicates under different names
  - keep-both with " (WIN)" suffix where same-name content differs
    (under .github/workflows/ the WIN copy gets .yml.txt so Actions
    never executes a forked workflow)
  - modify/delete + rename/delete: surviving content kept
  - invalid-UTF-8 filenames sanitized; APFS/NTFS case- and
    normalization-collisions resolved via NETWEB '_' prefix
  - hard lossless gate before committing
"""
import os
import subprocess
import sys
import unicodedata

REPO = "/Users/logan/IDAHO-VAULT"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
OURS = "526b97570581ca445f2106f011437a33e3c395da"       # logan/obsidian (Mac)
THEIRS = "6b6ce4541eeeeedb15a92f06d39362d5b838825f"     # origin/logan/obsidian (Win)
BASE = "709965f1"                                        # merge-base 2026-05-26
MANIFEST_NAME = b"MERGE-MANIFEST-2026-08-12.md"
TMP_INDEX = os.path.join(SCRATCH, "merge-index")


def git(*args, input=None):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, input=input)
    if r.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed: {r.stderr[:800]}")
    return r.stdout


def load_tree(treeish):
    """path(bytes) -> (mode(bytes), sha(str))"""
    out = git("ls-tree", "-r", "-z", treeish)
    tree = {}
    for rec in out.split(b"\x00"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, _type, sha = meta.split(b" ")
        tree[path] = (mode, sha.decode())
    return tree


def apfs_key(path_bytes):
    """Collision key approximating APFS/NTFS semantics: case- and
    Unicode-normalization-insensitive."""
    s = path_bytes.decode("utf-8", "replace")
    return unicodedata.normalize("NFC", s).casefold()


def win_suffix(path_bytes):
    d = path_bytes.decode("utf-8", "surrogateescape")
    dirname, _, fname = d.rpartition("/")
    prefix = dirname + "/" if dirname else ""
    if dirname.startswith(".github/workflows"):
        stem = fname[:-4] if fname.endswith((".yml",)) else fname
        cand = f"{prefix}{stem} (WIN).yml.txt"
    else:
        stem, dot, ext = fname.rpartition(".")
        if dot and stem:
            cand = f"{prefix}{stem} (WIN).{ext}"
        else:
            cand = f"{prefix}{fname} (WIN)"
    return cand.encode("utf-8", "surrogateescape")


def side_suffix(path_bytes, tag):
    d = path_bytes.decode("utf-8", "surrogateescape")
    dirname, _, fname = d.rpartition("/")
    prefix = dirname + "/" if dirname else ""
    stem, dot, ext = fname.rpartition(".")
    if dot and stem:
        cand = f"{prefix}{stem} ({tag}).{ext}"
    else:
        cand = f"{prefix}{fname} ({tag})"
    return cand.encode("utf-8", "surrogateescape")


FS_TEST_DIR = os.path.join(SCRATCH, "fs-name-test")


def fs_creatable(name_bytes):
    """Empirically test whether this filesystem accepts the name."""
    if name_bytes in (b".", b"..") or b"/" in name_bytes:
        return False
    p = os.path.join(FS_TEST_DIR.encode(), name_bytes)
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        os.unlink(p)
        return True
    except OSError:
        return False


def fs_sanitize_component(comp_bytes):
    """Replace exactly the characters the filesystem rejects with '_'."""
    s = comp_bytes.decode("utf-8", "surrogateescape")
    out = []
    for ch in s:
        probe = ("t" + ch).encode("utf-8", "surrogateescape")
        out.append(ch if fs_creatable(probe) else f"U+{ord(ch):04X}")
    return "".join(out).encode("utf-8", "surrogateescape")


def main():
    # ---- 1. parse merge-tree -z output --------------------------------
    raw = open(os.path.join(SCRATCH, "merge-tree-z.bin"), "rb").read()
    toks = raw.split(b"\x00")
    merged_tree_oid = toks[0].decode()
    entries = []
    for t in toks[1:]:
        if t == b"":
            break  # end of conflicted-file-info section
        meta, path = t.split(b"\t", 1)
        mode, sha, stage = meta.split(b" ")
        entries.append((path, int(stage), mode, sha.decode()))
    print(f"merged tree {merged_tree_oid}, {len(entries)} conflict stage entries")

    # ---- 2. load all four trees ---------------------------------------
    merged = load_tree(merged_tree_oid)
    ours = load_tree(OURS)
    theirs = load_tree(THEIRS)
    base = load_tree(BASE)
    print(f"tree sizes: merged={len(merged)} ours={len(ours)} theirs={len(theirs)} base={len(base)}")

    # ---- 3. group conflict entries by path ----------------------------
    groups = {}
    for path, stage, mode, sha in entries:
        groups.setdefault(path, {})[stage] = (mode, sha)

    taken_keys = {apfs_key(p) for p in merged}

    def claim(path_bytes):
        """Unique-ify against both byte-space and APFS key-space."""
        cand = path_bytes
        n = 2
        while cand in merged or apfs_key(cand) in taken_keys:
            d = cand.decode("utf-8", "surrogateescape")
            dirname, _, fname = d.rpartition("/")
            prefix = dirname + "/" if dirname else ""
            cand = f"{prefix}{n} {fname}".encode("utf-8", "surrogateescape")
            n += 1
        taken_keys.add(apfs_key(cand))
        return cand

    win_pairs, anomalies = [], []
    for path, g in sorted(groups.items()):
        if 2 in g and 3 in g:
            m2, s2 = g[2]
            m3, s3 = g[3]
            if s2 == s3:
                merged[path] = (m2, s2)
                continue
            merged[path] = (m2, s2)                      # Mac version at path
            win = claim(win_suffix(path))
            merged[win] = (m3, s3)                       # Windows version
            win_pairs.append((path, win))
        elif 2 in g:
            merged[path] = g[2]
        elif 3 in g:
            merged[path] = g[3]
        else:  # stage 1 only: both sides moved/deleted it
            if path in merged:
                anomalies.append(path)
    print(f"WIN-suffixed pairs: {len(win_pairs)}  stage1-only anomalies: {len(anomalies)}")
    for p in anomalies[:10]:
        print("  anomaly:", p.decode("utf-8", "replace"))

    # ---- 3b. lossless gate with restoration ---------------------------
    merged_blobs = {sha for _, sha in merged.values()}

    def gate_violations(tip, other, label):
        out = []
        for path, (mode, sha) in tip.items():
            if sha in merged_blobs:
                continue
            if base.get(path, (None, None))[1] == sha:
                continue  # side never touched it; superseded content is in history
            if path in other and other[path][1] != sha and path in merged:
                continue  # clean 3-way auto-merge produced a combined blob at path
            out.append((path, mode, sha))
        print(f"lossless gate [{label}]: {len(out)} violations")
        return out

    gate_restored = []
    for tip, other, label, tag in ((ours, theirs, "Mac", "MAC"),
                                   (theirs, ours, "Windows", "WIN")):
        for path, mode, sha in gate_violations(tip, other, label):
            target = path
            if target in merged or apfs_key(target) in taken_keys:
                target = claim(side_suffix(path, tag))
            else:
                taken_keys.add(apfs_key(target))
            merged[target] = (mode, sha)
            merged_blobs.add(sha)
            gate_restored.append((path, target, label))
            print(f"  restored [{label}]: {path.decode('utf-8','replace')}"
                  + (f" -> {target.decode('utf-8','replace')}" if target != path else ""))
    # re-assert: gate must now be clean on both sides
    if gate_violations(ours, theirs, "Mac/recheck") or \
       gate_violations(theirs, ours, "Windows/recheck"):
        print("ABORTING: lossless gate still failing after restoration.")
        sys.exit(1)

    # ---- 4. invalid-UTF-8 filename sanitization ----------------------
    sanitized = []
    for path in sorted(list(merged)):
        try:
            path.decode("utf-8", "strict")
        except UnicodeDecodeError:
            clean = path.decode("utf-8", "replace").replace("�", "_").encode()
            new = claim(clean)
            merged[new] = merged.pop(path)
            sanitized.append((path, new))
    print(f"invalid-UTF-8 paths sanitized: {len(sanitized)}")

    # ---- 5. APFS/NTFS collision resolution ----------------------------
    by_key = {}
    for path in merged:
        by_key.setdefault(apfs_key(path), []).append(path)
    pre_existing = 0
    aliased = []
    for key, paths in sorted(by_key.items()):
        if len(paths) < 2:
            continue
        both_in_ours = [p for p in paths if p in ours]
        if len(both_in_ours) == len(paths):
            pre_existing += 1  # collision already existed on Mac line; report only
            continue
        # keep the Mac-side representation if present, else first sorted
        paths.sort(key=lambda p: (p not in ours, p))
        for loser in paths[1:]:
            d = loser.decode("utf-8", "surrogateescape")
            dirname, _, fname = d.rpartition("/")
            prefix = dirname + "/" if dirname else ""
            cand = f"{prefix}_{fname}".encode("utf-8", "surrogateescape")
            new = claim(cand)
            merged[new] = merged.pop(loser)
            aliased.append((loser, new))
    print(f"case/normalization collisions aliased: {len(aliased)}  pre-existing (report-only): {pre_existing}")

    # ---- 6. empirical filesystem-name test (APFS rejects some names) --
    os.makedirs(FS_TEST_DIR, exist_ok=True)
    components = set()
    for path in merged:
        components.update(path.split(b"/"))
    bad = {c for c in components if not fs_creatable(c)}
    print(f"unique path components: {len(components)}  fs-rejected: {len(bad)}")
    fs_renamed = []
    if bad:
        comp_map = {c: fs_sanitize_component(c) for c in sorted(bad)}
        for c, n in comp_map.items():
            print(f"  fs-rename component: {c.decode('utf-8','replace')} -> {n.decode('utf-8','replace')}")
        for path in sorted(list(merged)):
            parts = path.split(b"/")
            if any(p in comp_map for p in parts):
                newp = b"/".join(comp_map.get(p, p) for p in parts)
                newp = claim(newp)
                merged[newp] = merged.pop(path)
                fs_renamed.append((path, newp))
    print(f"paths renamed for filesystem compatibility: {len(fs_renamed)}")

    # ---- 7. manifest ---------------------------------------------------
    def fmt(b):
        return b.decode("utf-8", "backslashreplace")

    lines = [
        "# MERGE MANIFEST — 2026-08-12 Mac/Windows reunification",
        "",
        "Merge of `origin/logan/obsidian` (Windows line, main-tracked) into",
        "`logan/obsidian` (MacBook line), diverged since merge-base `709965f1`",
        "(2026-05-26). Policy: preserve everything from both sides.",
        "",
        f"- Parents: Mac `{OURS[:8]}`, Windows `{THEIRS[:8]}`",
        f"- Same-name/different-content pairs split (Windows copy suffixed): {len(win_pairs)}",
        f"- Invalid-UTF-8 filenames sanitized: {len(sanitized)}",
        f"- Case/normalization collisions aliased (NETWEB `_` prefix): {len(aliased)}",
        f"- Pre-existing Mac-line case collisions (untouched, flagged): {pre_existing}",
        f"- Lossless-gate restorations (content ort would have dropped): {len(gate_restored)}",
        f"- Paths renamed for filesystem compatibility (APFS-rejected names): {len(fs_renamed)}",
        "",
        "## Split pairs (Mac version at original path)",
        "",
    ]
    lines += [f"- `{fmt(a)}` → WIN copy `{fmt(b)}`" for a, b in win_pairs]
    lines += ["", "## Sanitized filenames", ""]
    lines += [f"- `{fmt(a)}` → `{fmt(b)}`" for a, b in sanitized]
    lines += ["", "## Case-collision aliases", ""]
    lines += [f"- `{fmt(a)}` → `{fmt(b)}`" for a, b in aliased]
    lines += ["", "## Lossless-gate restorations", ""]
    lines += [f"- [{side}] `{fmt(a)}`" + (f" → `{fmt(b)}`" if a != b else " (restored in place)")
              for a, b, side in gate_restored]
    lines += ["", "## Filesystem-compatibility renames", ""]
    lines += [f"- `{fmt(a)}` → `{fmt(b)}`" for a, b in fs_renamed]
    lines += [
        "",
        "---",
        "Claude-Session: https://claude.ai/code/session_6c80a94c-6802-46ff-8526-0575213a0ec1",
        "",
    ]
    manifest_sha = git("hash-object", "-w", "--stdin",
                       input="\n".join(lines).encode()).decode().strip()
    merged[claim(MANIFEST_NAME)] = (b"100644", manifest_sha)

    # ---- 8. materialize index, write tree, commit ----------------------
    if os.path.exists(TMP_INDEX):
        os.unlink(TMP_INDEX)
    env = {**os.environ, "GIT_INDEX_FILE": TMP_INDEX}
    payload = b"\x00".join(
        mode + b" " + sha.encode() + b" 0\t" + path
        for path, (mode, sha) in sorted(merged.items())
    ) + b"\x00"
    r = subprocess.run(["git", "-C", REPO, "update-index", "-z", "--index-info"],
                       input=payload, capture_output=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:800])
    tree = subprocess.run(["git", "-C", REPO, "write-tree"], capture_output=True,
                          env=env).stdout.decode().strip()
    print(f"final tree: {tree}  entries: {len(merged)}")

    msg = os.path.join(SCRATCH, "merge-msg.txt")
    commit = git("commit-tree", tree, "-p", OURS, "-p", THEIRS, "-F", msg).decode().strip()
    print(f"MERGE COMMIT: {commit}")
    open(os.path.join(SCRATCH, "merge-commit.txt"), "w").write(commit + "\n")


if __name__ == "__main__":
    main()
