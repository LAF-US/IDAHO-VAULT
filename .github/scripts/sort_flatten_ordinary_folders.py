#!/usr/bin/env python3
"""Flatten ordinary Vault folders upward one level per pass.

This is a SORT operation for the IDAHO-VAULT root.

The rule implemented here is intentionally plain:

* The repository root folder named ``!`` is protected.
* Repository root folders whose names begin with ``.`` are protected roots.
* Every other repository root folder is ordinary.
* Files inside ordinary root folders move up exactly one directory level per
  pass until they reach the repository root.
* A nested folder that contains a dot in its name, such as ``hr.lproj``, is
  still an ordinary nested folder. Only root-level dotfolders are protected.
* Existing filenames are preserved with Windows-style "Keep Both" names:
  ``name.ext``, ``name (2).ext``, ``name (3).ext``.
* The ugly repeated collision names are evidence. Do not normalize them.
* ``.gitignore`` is not consulted. Ignored files are still filesystem reality.
* The script does not create directories.
* Empty ordinary folders may be removed after the move when explicitly asked.

Why this exists:

Prior agents and tools created ordinary folder structures at the Vault root
where the Constitution allows only the shared ``!`` layer and root-level
PERSONAE dotfolders, plus whatever Logan explicitly approves. Git is used for
version tracking and blame. Hiding or smoothing the mess destroys provenance.

This script therefore surfaces files instead of hiding them. The result may be
visibly ugly. That is part of the point: the resulting names show the collision
damage caused by earlier automation.

Examples:

    python .github/scripts/sort_flatten_ordinary_folders.py --dry-run
    python .github/scripts/sort_flatten_ordinary_folders.py --execute
    python .github/scripts/sort_flatten_ordinary_folders.py --execute --remove-empty-folders

Run from the repository root, or pass ``--root`` explicitly.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


PROTECTED_LITERAL_ROOTS = {"!"}


@dataclass(frozen=True)
class MovePlan:
    """One planned one-level file move."""

    source: Path
    destination: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "SORT operation: flatten files from ordinary root folders upward "
            "one level per pass while preserving Keep Both filename conflicts."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Vault repository root. Defaults to the current working directory.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned passes without changing files. This is the default.",
    )
    mode.add_argument(
        "--execute",
        action="store_true",
        help="Actually move files. Required for filesystem changes.",
    )
    parser.add_argument(
        "--remove-empty-folders",
        action="store_true",
        help=(
            "After executing moves, remove empty directories under ordinary "
            "root folders, deepest first. This never removes protected root "
            "folders and never removes a directory that still contains files."
        ),
    )
    parser.add_argument(
        "--max-print",
        type=int,
        default=40,
        help="Maximum individual moves to print per pass.",
    )
    return parser.parse_args()


def resolve_root(root_arg: Path) -> Path:
    root = root_arg.resolve()
    if not root.is_dir():
        raise SystemExit(f"Vault root is not a directory: {root}")
    return root


def is_protected_root(path: Path, root: Path) -> bool:
    if path.parent != root:
        return False
    return path.name in PROTECTED_LITERAL_ROOTS or path.name.startswith(".")


def ordinary_root_folders(root: Path) -> list[Path]:
    folders = []
    for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if child.is_dir() and not is_protected_root(child, root):
            folders.append(child)
    return folders


def assert_inside_root(path: Path, root: Path) -> None:
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"Refusing path outside Vault root: {resolved}") from exc


def keep_both_destination(destination: Path, reserved: set[Path], root: Path) -> Path:
    """Return a collision-safe destination using Windows Keep Both naming."""

    assert_inside_root(destination, root)
    if not destination.exists() and destination not in reserved:
        reserved.add(destination)
        return destination

    suffix_index = 2
    while True:
        candidate = destination.with_name(
            f"{destination.stem} ({suffix_index}){destination.suffix}"
        )
        assert_inside_root(candidate, root)
        if not candidate.exists() and candidate not in reserved:
            reserved.add(candidate)
            return candidate
        suffix_index += 1


def collect_initial_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for folder in ordinary_root_folders(root):
        files.extend(path for path in folder.rglob("*") if path.is_file())
    return sorted(files, key=lambda path: str(path.relative_to(root)).lower())


def plan_pass(current_files: list[Path], root: Path) -> tuple[list[MovePlan], list[Path]]:
    """Plan one upward pass.

    Files already at the repository root are carried forward unchanged.
    Every other file moves to its immediate grandparent directory.
    """

    reserved_destinations: set[Path] = set()
    moves: list[MovePlan] = []
    next_files: list[Path] = []

    # Reverse lexical order is intentional: it matches the first production run
    # and avoids moving a parent-visible file before deeper siblings.
    for source in sorted(
        current_files, key=lambda path: str(path.relative_to(root)).lower(), reverse=True
    ):
        assert_inside_root(source, root)
        relative = source.relative_to(root)
        if len(relative.parts) <= 1:
            next_files.append(source)
            continue

        destination = keep_both_destination(source.parent.parent / source.name, reserved_destinations, root)
        moves.append(MovePlan(source=source, destination=destination))
        next_files.append(destination)

    return moves, next_files


def print_pass(pass_number: int, moves: list[MovePlan], root: Path, max_print: int) -> None:
    collision_count = sum(1 for move in moves if move.source.name != move.destination.name)
    print(f"PASS {pass_number}: moves={len(moves)} collisions={collision_count}")
    for move in moves[:max_print]:
        print(f"  {move.source.relative_to(root)} -> {move.destination.relative_to(root)}")
    if len(moves) > max_print:
        print(f"  ... {len(moves) - max_print} more")


def execute_moves(moves: list[MovePlan], root: Path) -> None:
    for move in moves:
        assert_inside_root(move.source, root)
        assert_inside_root(move.destination, root)
        if not move.source.exists():
            raise FileNotFoundError(f"Missing source before move: {move.source}")
        move.source.rename(move.destination)


def remove_empty_ordinary_folders(root: Path, execute: bool) -> int:
    """Remove empty directories under ordinary roots, deepest first."""

    removed = 0
    for folder in ordinary_root_folders(root):
        candidates = sorted(
            (path for path in folder.rglob("*") if path.is_dir()),
            key=lambda path: len(path.relative_to(root).parts),
            reverse=True,
        )
        candidates.append(folder)
        for candidate in candidates:
            assert_inside_root(candidate, root)
            if is_protected_root(candidate, root):
                continue
            try:
                next(candidate.iterdir())
            except StopIteration:
                print(f"REMOVE EMPTY FOLDER: {candidate.relative_to(root)}")
                if execute:
                    candidate.rmdir()
                removed += 1
    return removed


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    execute = bool(args.execute)

    folders = ordinary_root_folders(root)
    print("ordinary_root_dirs=" + ", ".join(folder.name for folder in folders))
    current_files = collect_initial_files(root)
    print(f"initial_file_count={len(current_files)}")

    pass_number = 0
    total_moves = 0
    while True:
        moves, next_files = plan_pass(current_files, root)
        if not moves:
            break
        pass_number += 1
        print_pass(pass_number, moves, root, args.max_print)
        if execute:
            execute_moves(moves, root)
        total_moves += len(moves)
        current_files = next_files

    final_root_files = sum(1 for path in current_files if len(path.relative_to(root).parts) == 1)
    print(
        f"DONE passes={pass_number} total_moves={total_moves} "
        f"final_root_files={final_root_files}"
    )

    if args.remove_empty_folders:
        removed = remove_empty_ordinary_folders(root, execute)
        action = "removed" if execute else "would_remove"
        print(f"EMPTY FOLDERS {action}={removed}")

    if not execute:
        print("DRY RUN ONLY: no files or directories changed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
