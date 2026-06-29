#!/usr/bin/env python3
"""
chain_address_space.py — nondestructively fill EMPTY address-space coordinate
stubs with their per-character wikilink chain.

Assignment (Logan): insert [[*]][[*]][[*]] links nondestructively into the
A-ZZZZ (and numeric) address spaces.

Safety contract — what this tool will NOT do:
  - It NEVER creates a file. It only fills coordinate files that already exist.
    (Fixes the "agent hand-wrote individual cards" failure.)
  - It NEVER replaces or deletes existing content or frontmatter. It writes
    ONLY into files that are empty (0 bytes / whitespace-only).
    (Fixes the "destructive overwrite of DECISIONS.md / neurons" failure.)
  - Default mode is DRY-RUN: it writes nothing until you pass --apply.
  - It is idempotent: once a stub is filled it is no longer empty, so a second
    run skips it.

A "coordinate stub" is an existing root-level .md whose stem is a pure address
token — all letters (A..ZZZZ) or, with --numeric, all digits (0..999...).
"ABC.md" -> [[A]][[B]][[C]] ; "302.md" -> [[3]][[0]][[2]].
"""
from __future__ import annotations

import argparse
import os
import re
import sys

LETTER_RE = re.compile(r"^[A-Za-z]+$")
DIGIT_RE = re.compile(r"^[0-9]+$")


def chain_for(stem: str) -> str:
    """Per-character wikilink chain, e.g. 'ABC' -> '[[A]][[B]][[C]]'."""
    return "".join(f"[[{ch}]]" for ch in stem)


def is_empty(path: str) -> bool:
    """True if the file is empty or whitespace-only."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip() == ""
    except (OSError, UnicodeDecodeError):
        return False


def coordinate_stubs(root: str, include_numeric: bool):
    """Yield (filename, stem) for root-level .md files whose stem is a pure
    address token. Does not recurse; the address grid lives at the root."""
    for entry in os.scandir(root):
        if not entry.is_file() or not entry.name.endswith(".md"):
            continue
        stem = entry.name[:-3]
        if LETTER_RE.match(stem) or (include_numeric and DIGIT_RE.match(stem)):
            yield entry.name, stem


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="vault root (default: cwd)")
    ap.add_argument("--numeric", action="store_true",
                    help="also fill numeric coordinate stubs (0..999...)")
    ap.add_argument("--apply", action="store_true",
                    help="actually write (default is dry-run, writes nothing)")
    ap.add_argument("--samples", type=int, default=8,
                    help="how many would-fill examples to print (default 8)")
    args = ap.parse_args(argv)

    would_fill, skipped_nonempty = [], 0
    for name, stem in sorted(coordinate_stubs(args.root, args.numeric)):
        if is_empty(os.path.join(args.root, name)):
            would_fill.append((name, stem))
        else:
            skipped_nonempty += 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] root={os.path.abspath(args.root)}  "
          f"numeric={'on' if args.numeric else 'off'}")
    print(f"  empty coordinate stubs to fill : {len(would_fill)}")
    print(f"  non-empty files skipped (safe) : {skipped_nonempty}")
    for name, stem in would_fill[: args.samples]:
        print(f"    {name:>10}  ->  {chain_for(stem)}")
    if len(would_fill) > args.samples:
        print(f"    ... and {len(would_fill) - args.samples} more")

    if not args.apply:
        print("  (dry-run: no files written. Re-run with --apply to write.)")
        return 0

    written = 0
    for name, stem in would_fill:
        path = os.path.join(args.root, name)
        if not is_empty(path):           # re-check at write time (TOCTOU guard)
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(chain_for(stem) + "\n")
        written += 1
    print(f"  WROTE {written} coordinate stub(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
