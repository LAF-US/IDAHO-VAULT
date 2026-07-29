#!/usr/bin/env python3
"""Sync only *paired* Jupyter notebooks with their twins, failing loudly on a real sync error.

A notebook is "paired" iff it declares ``metadata.jupytext.formats`` (the explicit, per-notebook
opt-in this repo requires — see ``NOTEBOOKS.md``). Only those are synced here. Notebooks that are
unpaired, or whose JSON cannot even be parsed (a corrupt stray), are skipped entirely: they are
never synced (the footgun guard against a stale twin overwriting code) and never fail the run
(unparseable strays are listed on stderr for observability).

This replaces the earlier ``jupytext --sync "$nb" || true`` one-liners in the CI check and the
pre-commit hook, which swallowed *every* failure — including a paired notebook that genuinely
failed to sync — and could therefore pass green while drift slipped through.

Usage::

    jupytext_sync_paired.py [notebook.ipynb ...]

With no arguments it operates on every tracked ``*.ipynb``. For each paired notebook it runs
``jupytext --sync`` and, on success, prints the existing twin path(s) the notebook's declared
formats imply (one per line, whether or not this run actually modified them) so a git hook can
re-stage them. Exit status is non-zero iff a *paired* notebook failed to sync.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys


def tracked_notebooks() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.ipynb"], capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line]


def read_notebook(path: str) -> tuple[dict | None, Exception | None]:
    """Parse a notebook's JSON. Returns ``(data, error)``; ``error`` is non-None iff the file
    could not be parsed (a corrupt stray)."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle), None
    except (OSError, ValueError) as exc:
        return None, exc


def declared_formats(notebook: dict) -> str | None:
    """The declared jupytext formats string, or None if the notebook is unpaired."""
    return notebook.get("metadata", {}).get("jupytext", {}).get("formats") or None


def twin_paths(notebook: str, formats: str) -> list[str]:
    """Twin file paths implied by a formats string (every non-ipynb format)."""
    stem, _ = os.path.splitext(notebook)
    twins = []
    for fmt in formats.split(","):
        extension = fmt.strip().split(":")[0]
        if extension and extension != "ipynb":
            twins.append(f"{stem}.{extension}")
    return twins


def main(argv: list[str]) -> int:
    notebooks = argv[1:] or tracked_notebooks()
    failed: list[str] = []
    implied_twins: list[str] = []
    unparseable: list[str] = []
    for notebook in notebooks:
        data, error = read_notebook(notebook)
        if error is not None:
            unparseable.append(notebook)
            continue  # corrupt stray: never sync, never fail — but surfaced on stderr below
        formats = declared_formats(data)
        if not formats:
            continue  # genuinely unpaired: a no-op
        # Capture jupytext's own output: it must NOT reach this script's stdout, which is a
        # strict one-twin-path-per-line contract the pre-commit hook word-splits into `git add`.
        # jupytext chatter on our stdout would be handed to `git add` as bogus paths.
        proc = subprocess.run(
            ["jupytext", "--sync", "--", notebook], capture_output=True, text=True, check=False)
        if proc.stderr:
            sys.stderr.write(proc.stderr)
        if proc.returncode != 0:
            if proc.stdout:  # only on failure, and only to stderr — never our stdout
                sys.stderr.write(proc.stdout)
            failed.append(notebook)
            continue
        implied_twins.extend(twin for twin in twin_paths(notebook, formats) if os.path.exists(twin))
    # Emit each twin once, in first-seen order. The pre-commit hook word-splits this stdout into
    # `git add`, so a duplicate (e.g. a notebook declaring the same non-ipynb format twice) would
    # only pad the argument list; dedupe keeps the one-path-per-line contract deterministic.
    seen: set[str] = set()
    for twin in implied_twins:
        if twin not in seen:
            seen.add(twin)
            print(twin)
    if unparseable:
        sys.stderr.write(
            "note: skipped unparseable notebook(s) — not synced (observability, not a failure): "
            + ", ".join(unparseable) + "\n"
        )
    if failed:
        sys.stderr.write(
            "jupytext --sync failed for paired notebook(s): " + ", ".join(failed) + "\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
