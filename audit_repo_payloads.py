#!/usr/bin/env python3
"""Classify tracked binary/media payloads for repo-slimming work.

This is a non-destructive audit tool. It inventories large tracked payloads,
classifies them into repo-slimming categories, and can optionally enforce a
staged-file guardrail for future additions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]

PAYLOAD_SUFFIXES = {
    ".m4a",
    ".mp3",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".heic",
    ".heif",
    ".svg",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".geojson",
    ".kml",
    ".kmz",
    ".shp",
    ".gpx",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
    ".dmg",
    ".exe",
    ".bin",
    ".db",
    ".sqlite",
    ".sqlite3",
}

PLUGIN_RUNTIME_FILENAMES = {"main.js", "styles.css", "manifest.json"}
MIN_SIZE_BYTES = 128 * 1024

TEMP_TOOL_PREFIXES = (
    ".codex/tmp/",
    "tmp-minidata-msg/",
    "tmp-msg-extract/",
)

PROTECTED_PREFIXES = (
    ".claude/",
    ".gemini/",
    ".codex/",
    ".grok/",
    ".deepseek/",
    ".perplexity/",
    ".microsoft/",
    ".google/",
    ".meta/",
    ".slack/",
    ".bartimaeus/",
    ".zagreus/",
    ".persephone/",
    ".github/",
    "!/",
)

PROTECTED_EXCEPTIONS = (
    ".codex/tmp/",
)

HUMAN_INTERFACE_PREFIXES = (
    ".obsidian/",
)

ACTIVE_WORKFLOW_EXACT = {
    "!_2026_BUDGETS.xlsx",
    "!_2026_BUDGETS_2026-04-01.xlsx",
    "!_2026_BUDGETS_2026-04-02.xlsx",
}

MOVE_TO_ANNEX_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".heic",
    ".heif",
    ".svg",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".m4a",
    ".mp3",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".geojson",
    ".kml",
    ".kmz",
    ".shp",
    ".gpx",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stdout


def git_ls_files() -> list[str]:
    return [line for line in run_git("ls-files").splitlines() if line]


def git_staged_files() -> list[str]:
    return [
        line
        for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        if line
    ]


def git_lfs_oid_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    try:
        output = run_git("lfs", "ls-files", "-l")
    except subprocess.CalledProcessError:
        return mapping

    for line in output.splitlines():
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            oid, _, path = parts
            mapping[path] = oid
    return mapping


def git_count_objects() -> dict[str, str]:
    data: dict[str, str] = {}
    for line in run_git("count-objects", "-vH").splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        data[key] = value
    return data


def is_protected_path(rel_path: str) -> bool:
    if any(rel_path.startswith(prefix) for prefix in PROTECTED_EXCEPTIONS):
        return False
    return any(rel_path.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def is_candidate(rel_path: str, size_bytes: int) -> bool:
    path = Path(rel_path)
    suffix = path.suffix.lower()
    if path.name.startswith("~$"):
        return True
    if rel_path.startswith(".obsidian/plugins/") and path.name in PLUGIN_RUNTIME_FILENAMES:
        return True
    return suffix in PAYLOAD_SUFFIXES and size_bytes >= MIN_SIZE_BYTES


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_markdown_files() -> list[str]:
    return [path for path in git_ls_files() if path.lower().endswith(".md")]


def find_note_links(rel_path: str, markdown_files: Iterable[str]) -> list[str]:
    path = Path(rel_path)
    rel_lower = rel_path.casefold().replace("\\", "/")
    name_lower = path.name.casefold()
    stem_lower = path.stem.casefold()
    patterns = {
        rel_lower,
        name_lower,
        f"[[{stem_lower}]]",
        f"![[{stem_lower}]]",
        f"[[{name_lower}]]",
        f"![[{name_lower}]]",
    }

    matches: list[str] = []
    for md_path in markdown_files:
        abs_path = REPO_ROOT / md_path
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace").casefold()
        except OSError:
            continue
        if any(pattern in text for pattern in patterns):
            matches.append(md_path)
            if len(matches) >= 5:
                break
    return matches


def classify_candidate(
    rel_path: str,
    note_links: list[str],
    protected_path: bool,
    human_interface_path: bool,
) -> tuple[str, str]:
    path = Path(rel_path)
    suffix = path.suffix.lower()

    if path.name.startswith("~$") or any(rel_path.startswith(prefix) for prefix in TEMP_TOOL_PREFIXES):
        return ("temp_tool_trash", "purge_as_trash")

    if human_interface_path:
        return ("plugin_runtime_payload", "manual_review")

    if protected_path:
        return ("operational_runtime_asset", "keep_in_root")

    if rel_path in ACTIVE_WORKFLOW_EXACT:
        return ("operational_runtime_asset", "manual_review")

    if note_links or suffix in MOVE_TO_ANNEX_SUFFIXES:
        if suffix in {".xls", ".xlsx"}:
            return ("vault_evidence_reference_asset", "manual_review")
        return ("vault_evidence_reference_asset", "move_to_annex")

    return ("unknown_review", "manual_review")


def build_inventory(paths: Iterable[str]) -> dict:
    lfs_map = git_lfs_oid_map()
    markdown_files = load_markdown_files()
    count_objects = git_count_objects()

    inventory: list[dict] = []
    duplicate_groups: defaultdict[str, list[str]] = defaultdict(list)

    for rel_path in paths:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.exists() or not abs_path.is_file():
            continue

        size_bytes = abs_path.stat().st_size
        if not is_candidate(rel_path, size_bytes):
            continue

        note_links = find_note_links(rel_path, markdown_files)
        protected_path = is_protected_path(rel_path)
        human_interface_path = any(rel_path.startswith(prefix) for prefix in HUMAN_INTERFACE_PREFIXES)
        under_lfs = rel_path in lfs_map
        content_id = f"lfs:{lfs_map[rel_path]}" if under_lfs else f"sha256:{sha256_file(abs_path)}"
        duplicate_groups[content_id].append(rel_path)
        category, recommendation = classify_candidate(
            rel_path,
            note_links,
            protected_path,
            human_interface_path,
        )

        inventory.append(
            {
                "path": rel_path,
                "size_bytes": size_bytes,
                "suffix": Path(rel_path).suffix.lower(),
                "category": category,
                "recommended_action": recommendation,
                "under_lfs": under_lfs,
                "linked_from_notes": bool(note_links),
                "note_link_examples": note_links,
                "protected_path": protected_path,
                "human_interface_path": human_interface_path,
                "sensitive_path": protected_path or human_interface_path,
                "content_id": content_id,
                "duplicate_paths": [],
            }
        )

    for row in inventory:
        siblings = duplicate_groups[row["content_id"]]
        if len(siblings) > 1:
            row["duplicate_paths"] = [path for path in siblings if path != row["path"]]

    inventory.sort(key=lambda row: row["size_bytes"], reverse=True)

    category_counts = Counter(row["category"] for row in inventory)
    recommendation_counts = Counter(row["recommended_action"] for row in inventory)
    linked_count = sum(1 for row in inventory if row["linked_from_notes"])
    duplicate_count = sum(1 for row in inventory if row["duplicate_paths"])

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo_root": str(REPO_ROOT),
        "pack_stats": count_objects,
        "summary": {
            "candidate_count": len(inventory),
            "linked_from_notes_count": linked_count,
            "duplicate_entry_count": duplicate_count,
            "category_counts": dict(category_counts),
            "recommended_action_counts": dict(recommendation_counts),
        },
        "inventory": inventory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("tracked", "staged"),
        default="tracked",
        help="Inspect all tracked files or only staged additions/modifications.",
    )
    parser.add_argument(
        "--json-out",
        help="Write the JSON inventory to this file path.",
    )
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Exit non-zero if staged payloads need annex/review/purge.",
    )
    args = parser.parse_args()

    paths = git_ls_files() if args.mode == "tracked" else git_staged_files()
    report = build_inventory(paths)
    rendered = json.dumps(report, indent=2) + "\n"

    if args.json_out:
        output_path = Path(args.json_out)
        if not output_path.is_absolute():
            output_path = REPO_ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    if args.enforce:
        flagged = [
            row
            for row in report["inventory"]
            if row["recommended_action"] != "keep_in_root"
        ]
        if flagged:
            print(
                f"audit_repo_payloads: {len(flagged)} staged payload(s) need review or purge.",
                file=sys.stderr,
            )
            for row in flagged[:20]:
                print(
                    f"  {row['recommended_action']}: {row['path']}",
                    file=sys.stderr,
                )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
