#!/usr/bin/env python3
"""Enforce the dotfolder anchor FORMAT, not a hand-coded folder list.

Per STUB-PERSONAFOLDERS-2026-05-03.md and CONSTITUTION § I, every top-level
dotfolder is a persona/infrastructure chamber whose canonical anchor note is
`.<name>/<NAME>.md` — the folder name minus its leading dot, uppercased,
hyphens and underscores preserved (`.claude/CLAUDE.md`, `.amun-ra/AMUN-RA.md`).

Three prongs, all derived from the folder name. For a vault holding `.foo`
and `.bar`:

    exists            .foo/FOO.md     .bar/BAR.md      (chamber anchor)
    exists            FOO.md          BAR.md           (vault-root anchor)
    exists + bytes    .foo/stub.txt   .bar/stub.txt    (vacancy sentinel)

The sentinel's content is fixed at `¿!?` (c2 bf 21 3f, four bytes, no
trailing newline). Every dotfolder carries one — there is no exempt class.
STUB-PERSONAFOLDERS § 3 appears to carve out "software-imported persona
chambers" as stub-optional; per Logan that distinction was glossed on by an
agent and is not doctrine, so it is not honoured here.

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

# Pre-existing nonconforming dotfolders, inventoried 2026-07-02, all healed
# 2026-07-04 (.blue, .copilot, .gitbook, .gordian, .gordon, .green, .indigo,
# .openclaw, .orange, .red, .violet, .vscode, .yellow each gained their
# <NAME>.md anchor). Kept as an empty set rather than deleted so the
# grandfathering machinery below stays in place, even though it is
# currently inactive with nothing left to warn about: do not add new
# entries — a new dotfolder must ship its anchor in the same PR that
# introduces it.
GRANDFATHERED_MISSING_ANCHORS: set[str] = set()


def expected_anchor_name(dotfolder: str) -> str:
    # Strip exactly one leading dot; any further dots stay significant.
    return dotfolder[1:].upper() + ".md"


def tracked_top_level_dotfolders() -> list[str]:
    result = subprocess.run(
        # quotePath=false: git's default quoting wraps non-ASCII names in
        # "..." with octal escapes, which would fail startswith(".") and
        # silently exempt such a dotfolder from enforcement.
        ["git", "-c", "core.quotePath=false", "ls-tree", "HEAD"],
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
    missing_stub: list[str] = []
    wrong_stub: list[str] = []
    missing_root: list[str] = []

    for dotfolder in dotfolders:
        name = expected_anchor_name(dotfolder)

        # Prong 1 — the chamber anchor.
        anchor = f"{dotfolder}/{name}"
        anchored = (ROOT / anchor).is_file()
        if anchored:
            if dotfolder in GRANDFATHERED_MISSING_ANCHORS:
                healed.append(dotfolder)
        elif dotfolder in GRANDFATHERED_MISSING_ANCHORS:
            grandfathered.append(anchor)
        else:
            missing.append(anchor)

        # Prong 2 — the vacancy sentinel, existence AND bytes.
        stub = ROOT / dotfolder / STUB_FILENAME
        if not stub.is_file():
            missing_stub.append(f"{dotfolder}/{STUB_FILENAME}")
        else:
            try:
                found = stub.read_bytes()
            except OSError as error:
                wrong_stub.append(f"{dotfolder}/{STUB_FILENAME} (unreadable: {error})")
            else:
                if found != STUB_CONTENT:
                    wrong_stub.append(
                        f"{dotfolder}/{STUB_FILENAME} contains {found!r}, expected {STUB_CONTENT!r}"
                    )

        # Prong 3 — the vault-root anchor (ratcheted; see MAX_MISSING_ROOT_ANCHORS).
        if not (ROOT / name).is_file():
            missing_root.append(name)

    if healed:
        print("dotfolder-anchor guard: these folders gained their anchor —")
        print("remove them from GRANDFATHERED_MISSING_ANCHORS:")
        for item in healed:
            print(f" - {item}")

    if grandfathered:
        print("dotfolder-anchor guard: pre-existing anchor debt (warn-only):", file=sys.stderr)
        for item in grandfathered:
            print(f" - {item}", file=sys.stderr)

    failed = False

    if missing:
        print("dotfolder-anchor guard: dotfolders missing their <NAME>.md anchor:", file=sys.stderr)
        for item in missing:
            print(f" - {item}", file=sys.stderr)
        failed = True

    if missing_stub:
        print("dotfolder-anchor guard: dotfolders missing their stub.txt sentinel:", file=sys.stderr)
        for item in missing_stub:
            print(f" - {item}", file=sys.stderr)
        failed = True

    if wrong_stub:
        print("dotfolder-anchor guard: stub.txt sentinels with the wrong bytes:", file=sys.stderr)
        for item in wrong_stub:
            print(f" - {item}", file=sys.stderr)
        failed = True

    # Warn-and-ratchet, never a list. Debt at or below the mark reports and
    # passes; any increase is a new dotfolder that skipped its root anchor.
    if missing_root:
        over = len(missing_root) - MAX_MISSING_ROOT_ANCHORS
        if over > 0:
            print(
                f"dotfolder-anchor guard: {len(missing_root)} dotfolders have no vault-root "
                f"<NAME>.md, above the ratchet of {MAX_MISSING_ROOT_ANCHORS}. A new dotfolder "
                "ships its root anchor in the same PR:",
                file=sys.stderr,
            )
            for item in missing_root:
                print(f" - {item}", file=sys.stderr)
            failed = True
        else:
            print(
                f"dotfolder-anchor guard: {len(missing_root)} of {len(dotfolders)} dotfolders "
                f"have no vault-root <NAME>.md (ratchet {MAX_MISSING_ROOT_ANCHORS}, warn-only). "
                "Authored notes, not sentinels — write them, then lower the ratchet."
            )
            if len(missing_root) < MAX_MISSING_ROOT_ANCHORS:
                print(
                    f"  debt fell below the ratchet — lower MAX_MISSING_ROOT_ANCHORS to "
                    f"{len(missing_root)}."
                )

    if failed:
        print(
            "Every top-level dotfolder ships its anchor note and its stub.txt in the same PR "
            "(see STUB-PERSONAFOLDERS-2026-05-03.md).",
            file=sys.stderr,
        )
        return 1

    conforming = len(dotfolders) - len(grandfathered)
    summary = (
        f"dotfolder-anchor guard: {conforming} of {len(dotfolders)} tracked dotfolders carry "
        f"their <NAME>.md anchor and a correct stub.txt"
    )
    if grandfathered:
        summary += f" ({len(grandfathered)} grandfathered, warn-only)"
    print(summary + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
