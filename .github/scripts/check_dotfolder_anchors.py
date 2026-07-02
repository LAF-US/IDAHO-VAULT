#!/usr/bin/env python3
"""Enforce the dotfolder anchor FORMAT, not a hand-coded folder list.

Per STUB-PERSONAFOLDERS-2026-05-03.md and CONSTITUTION § I, every top-level
dotfolder is a persona/infrastructure chamber whose canonical anchor note is
`.<name>/<NAME>.md` — the folder name minus its leading dot, uppercased,
hyphens and underscores preserved (`.claude/CLAUDE.md`, `.amun-ra/AMUN-RA.md`).

The previous version of this check enforced a hand-coded 22-folder allowlist
that had drifted from both the intent and the vault: by 2026-07-02 roughly
300 tracked dotfolders satisfied the format — including every "exception" the
list encoded (`.github/GITHUB.md`, `.crewai/CREWAI.md`, `.abhorsen/ABHORSEN.md`,
`.dionysus/DIONYSUS.md` all exist) — so the list was simultaneously too small
and wrong. This version derives the requirement from the format itself:

- every TRACKED top-level dotfolder must contain its `<NAME>.md` anchor;
- a new dotfolder cannot land without one;
- known pre-existing debt (below) warns instead of failing until anchored.

Folders are enumerated from `git ls-tree HEAD` (tracked trees only), so local
untracked runtime dirs (.venv, caches) never false-fail a local run.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

# Pre-existing nonconforming dotfolders, inventoried 2026-07-02. These WARN
# rather than fail so the format rule can land without blocking main; each
# should gain its <NAME>.md anchor (per the stub standard's required minimum)
# and then be removed from this set. Do not add new entries — a new dotfolder
# must ship its anchor in the same PR.
GRANDFATHERED_MISSING_ANCHORS = {
    ".blue",
    ".copilot",
    ".gitbook",
    ".gordian",
    ".gordon",
    ".green",
    ".indigo",
    ".openclaw",
    ".orange",
    ".red",
    ".violet",
    ".vscode",
    ".yellow",
}


def expected_anchor_name(dotfolder: str) -> str:
    return dotfolder.lstrip(".").upper() + ".md"


def tracked_top_level_dotfolders() -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-tree HEAD failed")

    folders: list[str] = []
    for line in result.stdout.splitlines():
        # format: <mode> <type> <object>\t<name>
        meta, _, name = line.partition("\t")
        if not name or not name.startswith("."):
            continue
        if meta.split()[1] != "tree":
            continue
        folders.append(name)
    return sorted(folders)


def main() -> int:
    try:
        dotfolders = tracked_top_level_dotfolders()
    except RuntimeError as error:
        print(f"dotfolder-anchor guard: cannot enumerate tracked tree: {error}", file=sys.stderr)
        return 1

    missing: list[str] = []
    grandfathered: list[str] = []
    healed: list[str] = []

    for dotfolder in dotfolders:
        anchor = f"{dotfolder}/{expected_anchor_name(dotfolder)}"
        anchored = (ROOT / anchor).is_file()
        if anchored:
            if dotfolder in GRANDFATHERED_MISSING_ANCHORS:
                healed.append(dotfolder)
            continue
        if dotfolder in GRANDFATHERED_MISSING_ANCHORS:
            grandfathered.append(anchor)
        else:
            missing.append(anchor)

    if healed:
        print("dotfolder-anchor guard: these folders gained their anchor —")
        print("remove them from GRANDFATHERED_MISSING_ANCHORS:")
        for item in healed:
            print(f" - {item}")

    if grandfathered:
        print("dotfolder-anchor guard: pre-existing anchor debt (warn-only):", file=sys.stderr)
        for item in grandfathered:
            print(f" - {item}", file=sys.stderr)

    if missing:
        print("dotfolder-anchor guard: dotfolders missing their <NAME>.md anchor:", file=sys.stderr)
        for item in missing:
            print(f" - {item}", file=sys.stderr)
        print(
            "Every top-level dotfolder ships its anchor note in the same PR "
            "(see STUB-PERSONAFOLDERS-2026-05-03.md).",
            file=sys.stderr,
        )
        return 1

    print(f"dotfolder-anchor guard: {len(dotfolders)} tracked dotfolders conform to the anchor format.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
