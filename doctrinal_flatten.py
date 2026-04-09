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


@dataclass(frozen=True)
class Candidate:
    top_level: str
    source: Path
    relative_source: str
    relative_within_top: str
    basename: str
    stem: str
    suffix: str
    inbox: bool


def is_protected_dir(name: str) -> bool:
    return name == "!" or name.startswith(".") or name.startswith("_")


def is_machine_junk(name: str) -> bool:
    return name in SKIP_BASENAMES or any(name.startswith(prefix) for prefix in SKIP_PREFIXES)


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
    while candidate.lower() in reserved:
        candidate = f"{base}__n{counter}{suffix}"
        counter += 1
    reserved.add(candidate.lower())
    return candidate


def unique_inbox_path(
    dest: Path,
    source_rel: str,
    reserved: set[str],
) -> Path:
    key = str(dest).lower()
    if key not in reserved:
        reserved.add(key)
        return dest

    stem = dest.stem or "file"
    suffix = dest.suffix
    base = f"{stem}__src_inbox__{hash8(source_rel)}"
    candidate = dest.with_name(f"{base}{suffix}")
    counter = 2
    while str(candidate).lower() in reserved:
        candidate = dest.with_name(f"{base}__n{counter}{suffix}")
        counter += 1
    reserved.add(str(candidate).lower())
    return candidate


def iter_top_level_dirs(repo_root: Path) -> list[Path]:
    return sorted(
        [path for path in repo_root.iterdir() if path.is_dir() and not is_protected_dir(path.name)],
        key=lambda path: path.name.lower(),
    )


def collect_candidates(repo_root: Path) -> tuple[list[Candidate], list[dict[str, object]]]:
    candidates: list[Candidate] = []
    manifest_entries: list[dict[str, object]] = []

    for top_dir in iter_top_level_dirs(repo_root):
        for source in sorted([path for path in top_dir.rglob("*") if path.is_file()], key=lambda p: p.as_posix().lower()):
            rel_source = source.relative_to(repo_root).as_posix()
            rel_within_top = source.relative_to(top_dir).as_posix()
            if is_machine_junk(source.name):
                manifest_entries.append(
                    {
                        "action": "skipped_machine_state",
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
                    inbox=top_dir.name == "INBOX",
                )
            )

    return candidates, manifest_entries


def plan_moves(repo_root: Path, candidates: list[Candidate]) -> list[dict[str, object]]:
    root_reserved = {
        path.name.lower()
        for path in repo_root.iterdir()
        if path.is_file()
    }
    inbox_reserved = {
        str(path).lower()
        for path in (repo_root / "!" / "INBOX").rglob("*")
        if path.exists()
    } if (repo_root / "!" / "INBOX").exists() else set()

    plans: list[dict[str, object]] = []

    root_candidates = [candidate for candidate in candidates if not candidate.inbox]
    inbox_candidates = [candidate for candidate in candidates if candidate.inbox]

    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in root_candidates:
        grouped[candidate.basename.lower()].append(candidate)

    for basename_key in sorted(grouped.keys()):
        group = sorted(grouped[basename_key], key=lambda item: item.relative_source.lower())
        root_has_incumbent = basename_key in root_reserved

        winner_rel: str | None = None
        if not root_has_incumbent:
            winner_rel = group[0].relative_source
            root_reserved.add(group[0].basename.lower())

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

    for candidate in sorted(inbox_candidates, key=lambda item: item.relative_source.lower()):
        tentative = repo_root / "!" / "INBOX" / Path(candidate.relative_within_top)
        dest_path = unique_inbox_path(tentative, candidate.relative_source, inbox_reserved)
        collision = None if dest_path == tentative else "inbox_existing"
        action = "rehomed_inbox" if collision is None else "rehomed_inbox_renamed"
        plans.append(
            {
                "action": action,
                "source": candidate.relative_source,
                "destination": dest_path.relative_to(repo_root).as_posix(),
                "top_level": candidate.top_level,
                "relative_within_top": candidate.relative_within_top,
                "collision": collision,
            }
        )

    return sorted(plans, key=lambda item: str(item["source"]).lower())


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the doctrinal vault flatten with a manifest-first move plan.")
    parser.add_argument("--repo-root", default=".", help="Path to the vault root")
    parser.add_argument(
        "--manifest",
        default=f"!/RESTRUCTURE-MANIFEST-{date.today().isoformat()}.jsonl",
        help="Manifest path relative to repo root",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest).resolve()

    candidates, manifest_entries = collect_candidates(repo_root)
    plans = plan_moves(repo_root, candidates)
    manifest_entries.extend(plans)
    write_manifest(manifest_path, manifest_entries)
    execute_plans(repo_root, plans)
    remove_empty_directories(repo_root)

    summary = summarize(manifest_entries)
    print(json.dumps({"manifest": str(manifest_path.relative_to(repo_root)), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
