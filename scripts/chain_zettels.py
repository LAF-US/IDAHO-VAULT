#!/usr/bin/env python3
"""
chain_zettels.py — nondestructively add a decomposed-spelling wikilink chain as
the FIRST LINE AFTER FRONTMATTER of every address-space coordinate note.

Spec (Logan): for each coordinate file (stem = pure [A-Za-z0-9], length >= 2),
insert the per-character chain  ABC -> [[A]][[B]][[C]]  as the first body line,
*regardless of whether the file is empty or already has content*. Nondestructive
means: insert one line in the right place; never delete or replace existing
content or frontmatter.

Safety / correctness:
  - Pure insertion. Existing frontmatter and body are preserved byte-for-byte
    (read/write use newline="" so CRLF files round-trip unchanged); the chain
    is placed immediately after the closing frontmatter fence (or at the top
    if there is no frontmatter), followed by exactly one newline, then the
    original body untouched.
  - Atomic per-file write. --apply writes each file's new content to a
    sibling temp file, fsyncs it, then os.replace()s it over the original —
    never truncates the original in place. An interruption or disk-full
    error mid-write leaves the source note exactly as it was, not empty or
    partial.
  - Idempotent by position, not substring. A file is only treated as already
    chained if the chain is exactly the literal first body line -- a leading
    blank line before an otherwise-correct chain does NOT count as placed,
    it's reported MISPLACED, same as a chain appended at EOF by an earlier,
    buggy run. MISPLACED files are left alone rather than silently
    re-inserted (which would duplicate the chain) or auto-relocated (which
    would no longer be pure insertion).
  - No filename-based exclusion list. An earlier version of this script hard-
    coded a growing EXCLUDE_STEMS blocklist of root governance files
    (CLAUDE, CONSTITUTION, the LEVELSET protocol names, etc.) that happened
    to match the coordinate-stem pattern. Logan's own direct instruction on
    PR #572 (2026-08-11): that's disallowed, and unnecessary -- the whole
    point of nondestructive insertion is that it's safe to run on ANY
    matching file, governance included, because nothing is ever deleted or
    replaced. Trust the insertion contract instead of hand-maintaining a
    list of exceptions to it.
  - Full compare-and-swap for cooperating writers; no protection at all
    against non-cooperating ones. apply_one() takes a sidecar lockfile
    (atomic O_CREAT|O_EXCL) around the re-read/compare/replace, so two runs
    of this script -- or anything else that adopts the same lock convention
    -- genuinely serialize rather than racing; that risk (two automated
    writers) is fully closed, not just narrowed. What's NOT closed, and
    CANNOT be by any locking scheme added here: a human editing the file
    directly in Obsidian, which will never check for or honor this lock.
    That part of the risk is procedural -- keep the vault quiescent during
    any --apply run -- not a code gap this script can close by itself.
  - Root-only by default (the address grid lives at the vault root); does NOT
    recurse into subdirectories. (#572's rglob walk was over-broad, and is
    also why this file's own path — scripts/chain_zettels.py — was never at
    risk of self-matching.)
  - Dry-run by default. Writes nothing until --apply. --samples shows real
    before/after previews so the insertion can be inspected before any write.

This supersedes an earlier same-named script that already lived at this path
on main: PR #573, "Add idempotent Zettel component link chainer script" —
opened the same day as this PR (2026-06-19) and merged ~15 minutes later, a
parallel attempt at the same feature that landed first. Never wired into any
workflow, unguarded `rglob` + unconditional write, no dry-run — and never
actually run against the vault (no coordinate file on `main` carries a
chain, checked directly). That version is replaced here rather than kept
alongside it.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile

STEM_RE = re.compile(r"^[A-Za-z0-9]+$")


def chain_for(stem: str) -> str:
    """Return the per-character wikilink chain for a filename stem, e.g. "AB" -> "[[A]][[B]]"."""
    return "".join(f"[[{ch}]]" for ch in stem)


def split_frontmatter(content: str):
    """Return (prefix, body) where prefix is the frontmatter block including its
    closing fence and trailing newline; or (None, content) if no frontmatter."""
    if content.startswith("---\n") or content.startswith("---\r\n"):
        lines = content.splitlines(keepends=True)
        for i in range(1, len(lines)):
            if lines[i].rstrip("\r\n") == "---":
                return "".join(lines[: i + 1]), "".join(lines[i + 1:])
    return None, content


def chain_status(content: str, links: str) -> str:
    """Classify a file's relationship to its chain: 'placed' (correct, the
    literal first body line, no leading blank line tolerated), 'missing'
    (absent as a standalone line), or 'misplaced' (present as a standalone
    line somewhere else in the body -- e.g. a leading blank line pushed it
    down, or an earlier buggy run appended it at EOF)."""
    _, body = split_frontmatter(content)
    lines = body.splitlines()
    if lines and lines[0] == links:
        return "placed"
    if links in lines:
        return "misplaced"
    return "missing"


def transform(content: str, links: str):
    """Return new content with the chain inserted as the first body line.
    Caller must only call this when chain_status(content, links) == 'missing'.
    The newly-inserted line ends with whatever line-ending style the file
    already uses (CRLF if any \\r\\n is present, else LF), so a CRLF note
    doesn't end up with one stray LF line mixed into otherwise-CRLF content."""
    nl = "\r\n" if "\r\n" in content else "\n"
    prefix, body = split_frontmatter(content)
    if prefix is not None:
        if not prefix.endswith("\n"):  # covers both "\n" and "\r\n" terminators
            prefix += nl                # defensive: fence line had no trailing newline at all
        return prefix + links + nl + body
    return links + nl + content


def apply_one(root: str, name: str, original: str, new: str):
    """Write one file's new content atomically, guarding against a change since
    the scan that produced `original`. Returns None on success, or a string
    reason if skipped (locked by a concurrent run, unreadable at write time,
    or changed on disk).

    Holds a sidecar lockfile (atomic O_CREAT|O_EXCL, portable) across the
    re-read, comparison, and replace, so two runs of this script -- or any
    other writer that adopts the same `.{name}.lock` convention -- serialize
    instead of racing. This is a real compare-and-swap for COOPERATING
    writers, not a partial one: whichever process wins the lock has the only
    correct view of "did this change since scan" for the full critical
    section, not just up to the moment it starts writing.

    It does NOT and CANNOT protect against a non-cooperating writer (Obsidian
    desktop, a human editing the file directly) -- no lock this script takes
    is one Obsidian will ever check for, so there is no locking scheme,
    heavy or light, that closes that specific gap. That part of the risk is
    procedural, not fixable in code here: keep the vault quiescent (no
    Obsidian, no un-lock-aware writers) during any --apply run."""
    path = os.path.join(root, name)
    lock_path = os.path.join(root, f".{name}.lock")
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return "locked by a concurrent run of this script; skipped"

    try:
        # TOCTOU guard, now covering the FULL critical section under the
        # lock: re-read right before writing and refuse to clobber a change
        # that was never inspected.
        try:
            with open(path, "r", encoding="utf-8", newline="") as fh:
                current = fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            return f"unreadable at write time: {exc}"
        if current != original:
            return "changed on disk since scan; skipped, not overwritten"

        try:
            file_mode = os.stat(path).st_mode & 0o777
        except FileNotFoundError:
            file_mode = None  # new file: keep mkstemp's default (umask-restricted) mode
        fd, tmp_path = tempfile.mkstemp(dir=root, prefix=f".{name}.", suffix=".tmp")
        try:
            if file_mode is not None:
                os.chmod(tmp_path, file_mode)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, path)
        except BaseException:
            os.unlink(tmp_path)
            raise
        return None
    finally:
        os.close(lock_fd)
        os.unlink(lock_path)


def coordinate_files(root: str):
    """Yield (filename, stem) for each root-level .md file eligible as a coordinate
    note: pure-alphanumeric stem, length >= 2. Non-recursive."""
    for entry in os.scandir(root):
        if entry.is_file() and entry.name.endswith(".md"):
            stem = entry.name[:-3]
            if STEM_RE.match(stem) and len(stem) >= 2:
                yield entry.name, stem


def main(argv=None) -> int:
    """CLI entry point: scan --root for coordinate files, report their chain status,
    and (only with --apply) write the missing ones atomically. See module docstring."""
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true",
                    help="actually write (default: dry-run, writes nothing)")
    ap.add_argument("--samples", type=int, default=3,
                    help="before/after previews to print (default 3)")
    args = ap.parse_args(argv)

    to_change, already, misplaced, previews, failed = [], 0, [], [], []
    for name, stem in sorted(coordinate_files(args.root)):
        path = os.path.join(args.root, name)
        try:
            with open(path, "r", encoding="utf-8", newline="") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            failed.append((name, str(exc)))
            continue
        links = chain_for(stem)
        status = chain_status(content, links)
        if status == "placed":
            already += 1
            continue
        if status == "misplaced":
            misplaced.append(name)
            continue
        new = transform(content, links)
        to_change.append((name, content, new))
        if len(previews) < args.samples:
            previews.append((name, content, new))

    run_mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{run_mode}] root={os.path.abspath(args.root)}")
    print(f"  coordinate files needing the chain   : {len(to_change)}")
    print(f"  already chained, correctly placed    : {already}")
    print(f"  chain present but MISPLACED (skipped): {len(misplaced)}")
    for name in misplaced:
        print(f"    ! {name}")
    print(f"  unreadable / not valid UTF-8 (skipped, NOT scanned): {len(failed)}")
    for name, err in failed:
        print(f"    ! {name}: {err}")
    for name, before, after in previews:
        print(f"\n  --- {name} (BEFORE, first 5 lines) ---")
        for ln in before.splitlines()[:5] or ["(empty)"]:
            print(f"    | {ln}")
        print(f"  --- {name} (AFTER, first 5 lines) ---")
        for ln in after.splitlines()[:5]:
            print(f"    | {ln}")

    if not args.apply:
        print("\n  (dry-run: no files written. Re-run with --apply to write.)")
        return 1 if failed else 0

    written, conflicts = 0, []
    for name, original, new in to_change:
        reason = apply_one(args.root, name, original, new)
        if reason is not None:
            conflicts.append((name, reason))
            continue
        written += 1
    print(f"\n  WROTE {written} file(s).")
    if conflicts:
        print(f"  SKIPPED {len(conflicts)} file(s) that changed since scan:")
        for name, reason in conflicts:
            print(f"    ! {name}: {reason}")
    return 1 if (failed or conflicts) else 0


if __name__ == "__main__":
    sys.exit(main())
