#!/usr/bin/env python3
"""
metadata_survey.py - survey markdown metadata/frontmatter health for IDAHO-VAULT.

Purpose:
  - measure frontmatter coverage and parse health
  - identify drift in required baseline metadata fields
  - separate daily-note metadata shape from non-daily note metadata shape
  - produce machine-readable output agents can consume before proposing repairs

Usage:
  python .github/scripts/metadata_survey.py
  python .github/scripts/metadata_survey.py --format markdown
  python .github/scripts/metadata_survey.py --include-private --output !/metadata-survey.md --format markdown
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


VAULT_ROOT = Path(__file__).resolve().parents[2]
FRONTMATTER_RE = re.compile(
    r"\A---(?:\r?\n)(?P<frontmatter>.*?)(?:\r?\n)---(?:\r?\n|$)",
    re.DOTALL,
)
DAILY_NOTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
DEFAULT_REQUIRED_FIELDS = ("title", "updated", "status", "authority")
DAILY_EXPECTED_FIELDS = (
    "title",
    "aliases",
    "linter-yaml-title-alias",
    "yesterday",
    "tomorrow",
    "weekday",
)
TEMPLATE_FIELDS = ("doc_class", "template_id", "template_version")
EXAMPLE_LIMIT = 10
SKIP_DIRS = {
    ".git",
    ".venv",
    ".uv-cache",
    ".smart-env",
    "__pycache__",
    "node_modules",
}
SKIP_GLOBS = (
    "_tmp*",
    "pytest-cache-files-*",
    "tmp*",
)


@dataclass(frozen=True)
class FrontmatterResult:
    state: str
    data: dict[str, Any] | None
    error: str | None = None


def _matches_skip_glob(name: str) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in SKIP_GLOBS)


def _should_skip_dir(path: Path, root: Path, include_private: bool) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return True

    if not rel_parts:
        return False

    first = rel_parts[0]
    if first in SKIP_DIRS:
        return True
    if first == "_private" and not include_private:
        return True
    if first == ".obsidian" and len(rel_parts) > 1 and rel_parts[1] == "plugins":
        return True
    return any(_matches_skip_glob(part) for part in rel_parts)


def iter_markdown_files(root: Path, include_private: bool = False) -> list[Path]:
    results: list[Path] = []
    for path in root.rglob("*.md"):
        if _should_skip_dir(path.parent, root, include_private):
            continue
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if any(part == "_private" for part in rel_parts) and not include_private:
            continue
        if ".obsidian" in rel_parts:
            obsidian_index = rel_parts.index(".obsidian")
            if len(rel_parts) > obsidian_index + 1 and rel_parts[obsidian_index + 1] == "plugins":
                continue
        if any(_matches_skip_glob(part) for part in rel_parts):
            continue
        results.append(path)
    return sorted(results)


def parse_frontmatter(text: str) -> FrontmatterResult:
    if not text.startswith("---"):
        return FrontmatterResult(state="missing", data=None)

    match = FRONTMATTER_RE.match(text)
    if not match:
        return FrontmatterResult(state="malformed", data=None, error="missing closing frontmatter fence")

    raw_frontmatter = match.group("frontmatter")
    try:
        loaded = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as exc:
        return FrontmatterResult(state="malformed", data=None, error=str(exc))

    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        return FrontmatterResult(state="malformed", data=None, error="frontmatter must parse to a mapping")

    return FrontmatterResult(state="valid", data=loaded)


def _append_example(bucket: list[str], relpath: str) -> None:
    if len(bucket) < EXAMPLE_LIMIT and relpath not in bucket:
        bucket.append(relpath)


def _increment_missing_fields(
    data: dict[str, Any],
    required_fields: tuple[str, ...],
    counter: Counter[str],
    examples: dict[str, list[str]],
    relpath: str,
) -> None:
    for key in required_fields:
        if key not in data:
            counter[key] += 1
            _append_example(examples[key], relpath)


def survey_vault(root: Path, include_private: bool = False) -> dict[str, Any]:
    files = iter_markdown_files(root, include_private=include_private)

    summary: dict[str, Any] = {
        "root": str(root),
        "include_private": include_private,
        "scanned_files": len(files),
        "frontmatter": {
            "valid": 0,
            "missing": 0,
            "malformed": 0,
        },
        "daily_notes": {
            "count": 0,
            "valid_frontmatter": 0,
            "missing_expected_fields": {},
            "legacy_field_usage": {},
        },
        "non_daily_notes": {
            "count": 0,
            "valid_frontmatter": 0,
            "missing_required_fields": {},
            "with_related": 0,
            "with_tags": 0,
            "with_aliases": 0,
            "with_template_fields": {
                "doc_class": 0,
                "template_id": 0,
                "template_version": 0,
            },
            "status_values": {},
            "authority_values": {},
            "doc_class_values": {},
        },
        "key_frequency": {},
        "examples": {
            "missing_frontmatter": [],
            "malformed_frontmatter": [],
            "daily_missing_expected_fields": {},
            "non_daily_missing_required_fields": {},
        },
    }

    key_frequency: Counter[str] = Counter()
    daily_missing: Counter[str] = Counter()
    daily_legacy: Counter[str] = Counter()
    governed_missing: Counter[str] = Counter()
    status_values: Counter[str] = Counter()
    authority_values: Counter[str] = Counter()
    doc_class_values: Counter[str] = Counter()
    daily_missing_examples: dict[str, list[str]] = defaultdict(list)
    governed_missing_examples: dict[str, list[str]] = defaultdict(list)

    for path in files:
        relpath = path.relative_to(root).as_posix()
        parsed = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        summary["frontmatter"][parsed.state] += 1

        if parsed.state == "missing":
            _append_example(summary["examples"]["missing_frontmatter"], relpath)
        elif parsed.state == "malformed":
            _append_example(summary["examples"]["malformed_frontmatter"], relpath)

        is_daily = DAILY_NOTE_RE.match(path.name) is not None
        bucket = summary["daily_notes"] if is_daily else summary["non_daily_notes"]
        bucket["count"] += 1

        if parsed.state != "valid" or parsed.data is None:
            continue

        bucket["valid_frontmatter"] += 1
        data = parsed.data
        key_frequency.update(data.keys())

        if is_daily:
            _increment_missing_fields(
                data,
                DAILY_EXPECTED_FIELDS,
                daily_missing,
                daily_missing_examples,
                relpath,
            )
            for legacy_key in ("date created", "date modified", "created", "updated", "status", "authority"):
                if legacy_key in data:
                    daily_legacy[legacy_key] += 1
            continue

        _increment_missing_fields(
            data,
            DEFAULT_REQUIRED_FIELDS,
            governed_missing,
            governed_missing_examples,
            relpath,
        )

        if "related" in data:
            summary["non_daily_notes"]["with_related"] += 1
        if "tags" in data:
            summary["non_daily_notes"]["with_tags"] += 1
        if "aliases" in data:
            summary["non_daily_notes"]["with_aliases"] += 1

        for field in TEMPLATE_FIELDS:
            if field in data:
                summary["non_daily_notes"]["with_template_fields"][field] += 1

        if "status" in data:
            status_values[str(data["status"])] += 1
        if "authority" in data:
            authority_values[str(data["authority"])] += 1
        if "doc_class" in data:
            doc_class_values[str(data["doc_class"])] += 1

    summary["daily_notes"]["missing_expected_fields"] = dict(sorted(daily_missing.items()))
    summary["daily_notes"]["legacy_field_usage"] = dict(sorted(daily_legacy.items()))
    summary["non_daily_notes"]["missing_required_fields"] = dict(sorted(governed_missing.items()))
    summary["non_daily_notes"]["status_values"] = dict(sorted(status_values.items()))
    summary["non_daily_notes"]["authority_values"] = dict(sorted(authority_values.items()))
    summary["non_daily_notes"]["doc_class_values"] = dict(sorted(doc_class_values.items()))
    summary["key_frequency"] = dict(key_frequency.most_common())
    summary["examples"]["daily_missing_expected_fields"] = dict(sorted(daily_missing_examples.items()))
    summary["examples"]["non_daily_missing_required_fields"] = dict(sorted(governed_missing_examples.items()))

    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Metadata Survey",
        "",
        f"- Root: `{summary['root']}`",
        f"- Scanned markdown files: `{summary['scanned_files']}`",
        f"- Included `_private`: `{summary['include_private']}`",
        "",
        "## Frontmatter Health",
        "",
        f"- Valid: `{summary['frontmatter']['valid']}`",
        f"- Missing: `{summary['frontmatter']['missing']}`",
        f"- Malformed: `{summary['frontmatter']['malformed']}`",
        "",
        "## Daily Notes",
        "",
        f"- Daily note files: `{summary['daily_notes']['count']}`",
        f"- Daily notes with valid frontmatter: `{summary['daily_notes']['valid_frontmatter']}`",
    ]

    daily_missing = summary["daily_notes"]["missing_expected_fields"]
    if daily_missing:
        lines.extend(["", "### Daily Missing Expected Fields", ""])
        for key, count in daily_missing.items():
            lines.append(f"- `{key}`: `{count}`")

    daily_legacy = summary["daily_notes"]["legacy_field_usage"]
    if daily_legacy:
        lines.extend(["", "### Daily Legacy / Drift Fields", ""])
        for key, count in daily_legacy.items():
            lines.append(f"- `{key}`: `{count}`")

    governed = summary["non_daily_notes"]
    lines.extend(
        [
            "",
            "## Non-Daily Notes",
            "",
            f"- Non-daily note files: `{governed['count']}`",
            f"- Non-daily notes with valid frontmatter: `{governed['valid_frontmatter']}`",
            f"- With `related`: `{governed['with_related']}`",
            f"- With `tags`: `{governed['with_tags']}`",
            f"- With `aliases`: `{governed['with_aliases']}`",
        ]
    )

    missing_required = governed["missing_required_fields"]
    if missing_required:
        lines.extend(["", "### Non-Daily Missing Required Fields", ""])
        for key, count in missing_required.items():
            lines.append(f"- `{key}`: `{count}`")

    with_template_fields = governed["with_template_fields"]
    lines.extend(["", "### Template Field Coverage", ""])
    for key, count in with_template_fields.items():
        lines.append(f"- `{key}`: `{count}`")

    status_values = governed["status_values"]
    if status_values:
        lines.extend(["", "### Status Values", ""])
        for key, count in status_values.items():
            lines.append(f"- `{key}`: `{count}`")

    authority_values = governed["authority_values"]
    if authority_values:
        lines.extend(["", "### Authority Values", ""])
        for key, count in authority_values.items():
            lines.append(f"- `{key}`: `{count}`")

    doc_class_values = governed["doc_class_values"]
    if doc_class_values:
        lines.extend(["", "### Document Classes", ""])
        for key, count in doc_class_values.items():
            lines.append(f"- `{key}`: `{count}`")

    examples = summary["examples"]
    if examples["missing_frontmatter"]:
        lines.extend(["", "## Example Files Missing Frontmatter", ""])
        for relpath in examples["missing_frontmatter"]:
            lines.append(f"- `{relpath}`")

    if examples["malformed_frontmatter"]:
        lines.extend(["", "## Example Files With Malformed Frontmatter", ""])
        for relpath in examples["malformed_frontmatter"]:
            lines.append(f"- `{relpath}`")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Survey markdown metadata/frontmatter health")
    parser.add_argument("--root", default=str(VAULT_ROOT), help="Vault root to scan")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include _private/ historical work areas in the survey",
    )
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    summary = survey_vault(root=root, include_private=args.include_private)
    rendered = (
        json.dumps(summary, indent=2, sort_keys=True)
        if args.format == "json"
        else render_markdown(summary)
    )

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
