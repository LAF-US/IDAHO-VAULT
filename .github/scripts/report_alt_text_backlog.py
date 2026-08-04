#!/usr/bin/env python3
"""Report images still carrying the placeholder alt text.

`alt text needed` is not alt text. It exists so MD045 has something to see,
because the automated "quick fix" for an empty `![]()` is to delete the image
line -- 98 such deletions were proposed in the codacy patch this repo declined.
The placeholder keeps the image and makes the omission countable.

This is a REPORT, not a gate: it exits 0 no matter how large the backlog is.
Pass --strict to fail instead, which is only useful once the backlog is small.

Empty `![]()` is reported separately, because that is a regression rather than
backlog -- every one in tracked markdown was filled, so a new one means an
image arrived without passing through here.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

PLACEHOLDER = "alt text needed"
_PLACEHOLDER_RE = re.compile(r"!\[" + re.escape(PLACEHOLDER) + r"\]\(")
_EMPTY_RE = re.compile(r"!\[\]\(")
_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def _markdown_files(root: Path):
    for path in root.rglob("*.md"):
        if _SKIP_DIRS.isdisjoint(part for part in path.parts):
            yield path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="repo root (default: cwd)")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any placeholder remains")
    ap.add_argument("--top", type=int, default=10, help="how many files to list (default 10)")
    args = ap.parse_args()

    placeholders: Counter[str] = Counter()
    empties: Counter[str] = Counter()
    for path in _markdown_files(args.root):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = path.relative_to(args.root).as_posix()
        if n := len(_PLACEHOLDER_RE.findall(text)):
            placeholders[rel] = n
        if n := len(_EMPTY_RE.findall(text)):
            empties[rel] = n

    total = sum(placeholders.values())
    print(f"images awaiting alt text: {total} across {len(placeholders)} files")
    for rel, n in placeholders.most_common(args.top):
        print(f"  {n:4d}  {rel}")
    if len(placeholders) > args.top:
        print(f"  ... and {len(placeholders) - args.top} more files")

    if empties:
        print(
            f"\nREGRESSION: {sum(empties.values())} image(s) with empty alt text "
            f"in {len(empties)} file(s) -- these will be deleted by an MD045 autofix:",
            file=sys.stderr,
        )
        for rel, n in empties.most_common(args.top):
            print(f"  {n:4d}  {rel}", file=sys.stderr)
        return 1

    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())
