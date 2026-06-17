#!/usr/bin/env python3
"""Sync only *paired* Jupyter notebooks with their twins, failing loudly on a real sync error.

A notebook is "paired" iff it declares ``metadata.jupytext.formats`` (the explicit, per-notebook
opt-in this repo requires — see ``NOTEBOOKS.md``). Only those are synced here. Notebooks that are
unpaired, or whose JSON cannot even be parsed (a corrupt stray), are skipped entirely: they are
never synced (the footgun guard against a stale twin overwriting code) and never fail the run.

This replaces the earlier ``jupytext --sync "$nb" || true`` one-liners in the CI check and the
pre-commit hook, which swallowed *every* failure — including a paired notebook that genuinely
failed to sync — and could therefore pass green while drift slipped through.

Usage::

    jupytext_sync_paired.py [notebook.ipynb ...]

With no arguments it operates on every tracked ``*.ipynb``. For each paired notebook it runs
``jupytext --sync`` and, on success, prints the twin path(s) it touched (one per line) so a git
hook can re-stage them. Exit status is non-zero iff a *paired* notebook failed to sync.
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


def paired_formats(path: str) -> str | None:
    """Return the declared jupytext formats string, or None if unpaired/unparseable."""
    try:
        with open(path, encoding="utf-8") as handle:
            notebook = json.load(handle)
    except (OSError, ValueError):
        return None
    formats = notebook.get("metadata", {}).get("jupytext", {}).get("formats")
    return formats or None


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
    touched: list[str] = []
    for notebook in notebooks:
        formats = paired_formats(notebook)
        if not formats:
            continue  # unpaired or unparseable: never sync, never fail the run
        if subprocess.run(["jupytext", "--sync", notebook]).returncode != 0:
            failed.append(notebook)
            continue
        touched.extend(twin for twin in twin_paths(notebook, formats) if os.path.exists(twin))
    for twin in touched:
        print(twin)
    if failed:
        sys.stderr.write(
            "jupytext --sync failed for paired notebook(s): " + ", ".join(failed) + "\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
