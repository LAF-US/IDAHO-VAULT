from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SKIP_BASENAMES = {"Thumbs.db", "desktop.ini", ".DS_Store"}
SKIP_PREFIXES = ("._",)
# Opaque packages: a directory with one of these suffixes is a single artifact
# (macOS bundle, Xcode container, Premiere template). Its internals are never
# flatten candidates -- moving one file out breaks the whole package. This is
# a class rule on the directory name; it enumerates no paths.
GIT_DIR = ".git"
PACKAGE_SUFFIXES = (
    ".app", ".framework", ".bundle", ".plugin", ".kext", ".appex", ".xpc",
    ".xcodeproj", ".xcworkspace", ".playground", ".mogrt", ".lproj",
)


@dataclass(frozen=True)
class Candidate:
    top_level: str
    source: Path
    relative_source: str
    relative_within_top: str
    basename: str
    stem: str
    suffix: str


def is_protected_dir(name: str) -> bool:
    return name == "!" or name.startswith(".")


def is_machine_junk(name: str) -> bool:
    return name in SKIP_BASENAMES or any(name.startswith(prefix) for prefix in SKIP_PREFIXES)


def is_package_dir(name: str) -> bool:
    return name.lower().endswith(PACKAGE_SUFFIXES)


def inside_package(rel_within_top: str, top_level: str) -> bool:
    """True if the file lives under any package directory or nested git repo.

    A nested ``.git`` is another repository's internals, not vault content;
    hoisting its HEAD/config/packed-refs to the root collides with this repo's
    own names. Class rule on the directory name; it enumerates no paths.
    """
    if is_package_dir(top_level) or top_level == GIT_DIR:
        return True
    return any(
        is_package_dir(part) or part == GIT_DIR
        for part in rel_within_top.split("/")[:-1]
    )


def slugify(value: str) -> str:
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return slug or "misc"


def hash8(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def filesystem_key(value: str) -> str:
    """Return a canonical caseless filename key for macOS collision planning.

    Default macOS volumes are commonly case-insensitive and
    normalization-insensitive. Use Unicode canonical caseless matching—NFD,
    case-fold, then NFD again—so a case fold cannot leave combining marks outside
    canonical order before planning reaches ``shutil.move``.
    """
    normalized = unicodedata.normalize("NFD", value)
    return unicodedata.normalize("NFD", normalized.casefold())


def unique_root_name(
    source_rel: str,
    top_level: str,
    stem: str,
    suffix: str,
    reserved: set[str],
) -> str:
    safe_stem = stem or "file"
    base = f"{safe_stem}__src_{slugify(top_level)}__{hash8(source_rel)}"
    candidate = f"{base}{suffix}"
    counter = 2
    while filesystem_key(candidate) in reserved:
        candidate = f"{base}__n{counter}{suffix}"
        counter += 1
    reserved.add(filesystem_key(candidate))
    return candidate


def iter_top_level_dirs(repo_root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in repo_root.iterdir()
            if path.is_dir() and not is_protected_dir(path.name) and os.access(path, os.W_OK)
        ],
        key=lambda path: (filesystem_key(path.name), path.name),
    )


def collect_candidates(repo_root: Path) -> tuple[list[Candidate], list[dict[str, object]]]:
    candidates: list[Candidate] = []
    manifest_entries: list[dict[str, object]] = []

    for top_dir in iter_top_level_dirs(repo_root):
        for source in sorted(
            [path for path in top_dir.rglob("*") if path.is_file()],
            key=lambda path, parent=top_dir: (
                filesystem_key(path.relative_to(parent).as_posix()),
                path.as_posix(),
            ),
        ):
            rel_source = source.relative_to(repo_root).as_posix()
            rel_within_top = source.relative_to(top_dir).as_posix()
            skip_action = None
            if is_machine_junk(source.name):
                skip_action = "skipped_machine_state"
            elif inside_package(rel_within_top, top_dir.name):
                skip_action = "skipped_package_internal"
            elif not (os.access(source, os.W_OK) and os.access(source.parent, os.W_OK)):
                # Unwritable file or unwritable parent directory (can't unlink
                # even if the file itself is readable): not ours to move.
                skip_action = "skipped_unwritable"
            if skip_action:
                manifest_entries.append(
                    {
                        "action": skip_action,
                        "source": rel_source,
                        "destination": None,
                        "top_level": top_dir.name,
                        "relative_within_top": rel_within_top,
                        "collision": None,
                    }
                )
                continue

            candidates.append(
                Candidate(
                    top_level=top_dir.name,
                    source=source,
                    relative_source=rel_source,
                    relative_within_top=rel_within_top,
                    basename=source.name,
                    stem=source.stem,
                    suffix=source.suffix,
                )
            )

    return candidates, manifest_entries


def plan_moves(repo_root: Path, candidates: list[Candidate]) -> list[dict[str, object]]:
    root_reserved = {filesystem_key(path.name) for path in repo_root.iterdir()}
    plans: list[dict[str, object]] = []

    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[filesystem_key(candidate.basename)].append(candidate)

    for basename_key in sorted(grouped.keys()):
        group = sorted(
            grouped[basename_key],
            key=lambda item: (
                filesystem_key(item.relative_source),
                item.relative_source,
            ),
        )
        root_has_incumbent = basename_key in root_reserved

        winner_rel: str | None = None
        if not root_has_incumbent:
            winner_rel = group[0].relative_source
            root_reserved.add(filesystem_key(group[0].basename))

        for candidate in group:
            if not root_has_incumbent and candidate.relative_source == winner_rel:
                dest_name = candidate.basename
                collision = None
                action = "moved_root"
            else:
                dest_name = unique_root_name(
                    source_rel=candidate.relative_source,
                    top_level=candidate.top_level,
                    stem=candidate.stem,
                    suffix=candidate.suffix,
                    reserved=root_reserved,
                )
                collision = "root_existing" if root_has_incumbent else "incoming_duplicate"
                action = "moved_root_renamed"

            plans.append(
                {
                    "action": action,
                    "source": candidate.relative_source,
                    "destination": dest_name,
                    "top_level": candidate.top_level,
                    "relative_within_top": candidate.relative_within_top,
                    "collision": collision,
                }
            )

    return sorted(
        plans,
        key=lambda item: (filesystem_key(str(item["source"])), str(item["source"])),
    )


def write_manifest(manifest_path: Path, entries: list[dict[str, object]]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute_plans(repo_root: Path, plans: list[dict[str, object]]) -> None:
    for plan in plans:
        source = repo_root / str(plan["source"])
        destination = repo_root / str(plan["destination"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))


def remove_empty_directories(repo_root: Path) -> None:
    for top_dir in reversed(iter_top_level_dirs(repo_root)):
        nested_dirs = sorted(
            [path for path in top_dir.rglob("*") if path.is_dir()],
            key=lambda path: len(path.parts),
            reverse=True,
        )
        for path in nested_dirs:
            try:
                path.rmdir()
            except OSError:
                pass
        try:
            top_dir.rmdir()
        except OSError:
            pass


def summarize(entries: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        counts[str(entry["action"])] += 1
    return dict(sorted(counts.items()))


def display_manifest_path(repo_root: Path, manifest_path: Path) -> str:
    try:
        return str(manifest_path.relative_to(repo_root))
    except ValueError:
        return str(manifest_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the doctrinal vault flatten with a manifest-first move plan.")
    parser.add_argument("--repo-root", default=".", help="Path to the vault root")
    parser.add_argument(
        "--manifest",
        default=f"!/RESTRUCTURE-MANIFEST-{date.today().isoformat()}.jsonl",
        help="Manifest path relative to repo root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan and write the manifest, but move nothing and remove no directories",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest).resolve()

    candidates, manifest_entries = collect_candidates(repo_root)
    plans = plan_moves(repo_root, candidates)
    manifest_entries.extend(plans)
    write_manifest(manifest_path, manifest_entries)
    if not args.dry_run:
        execute_plans(repo_root, plans)
        remove_empty_directories(repo_root)

    summary = summarize(manifest_entries)
    print(
        json.dumps(
            {
                "manifest": display_manifest_path(repo_root, manifest_path),
                "dry_run": args.dry_run,
                "summary": summary,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
