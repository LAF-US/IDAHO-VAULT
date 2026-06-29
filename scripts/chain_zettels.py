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
  - Pure insertion. Existing frontmatter and body are preserved byte-for-byte;
    the chain is placed immediately after the closing frontmatter fence (or at
    the top if there is no frontmatter).
  - Idempotent. If the file already contains its chain, it is left unchanged.
  - Root-only by default (the address grid lives at the vault root); does NOT
    recurse into subdirectories. (#572's rglob walk was over-broad.)
  - Dry-run by default. Writes nothing until --apply. --samples shows real
    before/after previews so the insertion can be inspected before any write.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

STEM_RE = re.compile(r"^[A-Za-z0-9]+$")


def chain_for(stem: str) -> str:
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


def transform(content: str, links: str):
    """Return new content with the chain inserted, or None if no change needed."""
    if links in content:                       # idempotent: already chained
        return None
    prefix, body = split_frontmatter(content)
    if prefix is not None:
        if not prefix.endswith("\n"):
            prefix += "\n"
        return prefix + links + ("\n\n" + body if body.strip() else "\n")
    return links + ("\n\n" + content if content.strip() else "\n")


def coordinate_files(root: str):
    for entry in os.scandir(root):
        if entry.is_file() and entry.name.endswith(".md"):
            stem = entry.name[:-3]
            if STEM_RE.match(stem) and len(stem) >= 2:
                yield entry.name, stem


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true",
                    help="actually write (default: dry-run, writes nothing)")
    ap.add_argument("--samples", type=int, default=3,
                    help="before/after previews to print (default 3)")
    args = ap.parse_args(argv)

    to_change, already, previews = [], 0, []
    for name, stem in sorted(coordinate_files(args.root)):
        path = os.path.join(args.root, name)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        new = transform(content, chain_for(stem))
        if new is None:
            already += 1
            continue
        to_change.append((name, new))
        if len(previews) < args.samples:
            previews.append((name, content, new))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] root={os.path.abspath(args.root)}")
    print(f"  coordinate files needing the chain : {len(to_change)}")
    print(f"  already chained (skipped, idempotent): {already}")
    for name, before, after in previews:
        print(f"\n  --- {name} (BEFORE, first 5 lines) ---")
        for ln in before.splitlines()[:5] or ["(empty)"]:
            print(f"    | {ln}")
        print(f"  --- {name} (AFTER, first 5 lines) ---")
        for ln in after.splitlines()[:5]:
            print(f"    | {ln}")

    if not args.apply:
        print("\n  (dry-run: no files written. Re-run with --apply to write.)")
        return 0

    written = 0
    for name, new in to_change:
        with open(os.path.join(args.root, name), "w", encoding="utf-8") as fh:
            fh.write(new)
        written += 1
    print(f"\n  WROTE {written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
