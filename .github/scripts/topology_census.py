#!/usr/bin/env python3
"""Doctrine-first topology census for root folders, dotfolders, and the Nest.

This tool is intentionally diagnostic. It inventories topology, authority
signals, and git-state evidence without proposing moves or mutating repo
tracked structure.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "!"
LIVE_DOCTRINE_PATHS = (
    "CONSTITUTION.md",
    "VAULT-CONVENTIONS.md",
    "!/WAKEUP.md",
    "!/README.md",
    "!/AGENTS.md",
)
ROOT_EXCLUDED_NAME = "!"
GOVERNING_FILENAMES = (
    "README.md",
    "AGENTS.md",
    "MANIFEST.md",
    "DOCKET.md",
)
NEST_STATUS_LIVE_HINTS = (
    "status: active",
    "current truth",
    "is the live",
    "live staging",
    "durable async bus",
    "intake automation layer",
    "file drop zone",
    "swarmic nest",
)
NEST_STATUS_HISTORICAL_HINTS = (
    "historical",
    "superseded",
    "retired",
    "archive only",
    "preserved",
)
TOP_LEVEL_SUMMARY_LIMIT = 12
CHILD_SAMPLE_LIMIT = 8
RUN_ID_FORMAT = "%Y%m%dT%H%M%SZ"


def _normalize(path: Path | str) -> str:
    return Path(path).as_posix()


def _relpath(path: Path, root: Path) -> str:
    return _normalize(path.relative_to(root))


def _run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stdout


def _git_repo_available(root: Path) -> bool:
    try:
        _run_git(root, "rev-parse", "--is-inside-work-tree")
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def _git_tracked_files(root: Path) -> set[str]:
    if not _git_repo_available(root):
        return set()
    return {line for line in _run_git(root, "ls-files").splitlines() if line}


def _git_path_is_ignored(root: Path, relpath: str) -> bool:
    if not _git_repo_available(root):
        return False
    result = subprocess.run(
        ["git", "-C", str(root), "check-ignore", relpath],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


def _git_status_lines(root: Path, relpath: str) -> list[str]:
    if not _git_repo_available(root):
        return []
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--short", "--ignored", "--", relpath],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def _tracked_prefix_exists(relpath: str, tracked_files: set[str]) -> bool:
    prefix = f"{relpath}/"
    return any(path == relpath or path.startswith(prefix) for path in tracked_files)


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def _load_live_doctrine(root: Path) -> dict[str, list[str]]:
    doctrine: dict[str, list[str]] = {}
    for relpath in LIVE_DOCTRINE_PATHS:
        path = root / Path(relpath)
        doctrine[relpath] = _load_text(path).splitlines()
    return doctrine


def _find_heading_range(lines: list[str], heading: str) -> tuple[int, int] | None:
    start = None
    level = None
    pattern = re.compile(r"^(#+)\s+(.*)$")
    for idx, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        hashes, title = match.groups()
        if start is None and title.strip() == heading:
            start = idx
            level = len(hashes)
            continue
        if start is not None and len(hashes) <= level:
            return (start, idx)
    if start is None:
        return None
    return (start, len(lines))


def _sample_children(path: Path) -> tuple[dict[str, object], list[str]]:
    try:
        children = sorted(path.iterdir(), key=lambda child: (not child.is_dir(), child.name.lower()))
    except OSError as exc:
        return (
            {
                "accessible": False,
                "dir_count": None,
                "file_count": None,
                "sample_children": [],
            },
            [str(exc)],
        )

    dir_count = sum(1 for child in children if child.is_dir())
    file_count = sum(1 for child in children if child.is_file())
    sample = [
        f"{'DIR' if child.is_dir() else 'FILE'} {child.name}"
        for child in children[:CHILD_SAMPLE_LIMIT]
    ]
    if len(children) > CHILD_SAMPLE_LIMIT:
        sample.append(f"... +{len(children) - CHILD_SAMPLE_LIMIT} more")
    return (
        {
            "accessible": True,
            "dir_count": dir_count,
            "file_count": file_count,
            "sample_children": sample,
        },
        [],
    )


def _make_citation(relpath: str, line_number: int, line: str) -> dict[str, object]:
    return {
        "path": relpath,
        "line": line_number,
        "excerpt": line.strip(),
    }


def _find_citations(
    doctrine_lines: dict[str, list[str]],
    *,
    exact_tokens: list[str],
    loose_tokens: list[str] | None = None,
    limit: int = 8,
) -> list[dict[str, object]]:
    citations: list[dict[str, object]] = []
    normalized_loose = [token.casefold() for token in (loose_tokens or []) if token]
    for relpath, lines in doctrine_lines.items():
        for idx, line in enumerate(lines, start=1):
            line_casefold = line.casefold()
            if any(token in line for token in exact_tokens if token):
                citations.append(_make_citation(relpath, idx, line))
            elif any(token in line_casefold for token in normalized_loose):
                citations.append(_make_citation(relpath, idx, line))
            if len(citations) >= limit:
                return citations
    return citations


def _find_local_governing_surface(path: Path) -> Path | None:
    for name in GOVERNING_FILENAMES:
        candidate = path / name
        if candidate.exists():
            return candidate
    return None


def _governing_surface_summary(root: Path, path: Path) -> dict[str, object] | None:
    local_surface = _find_local_governing_surface(path)
    if local_surface is None:
        return None
    relpath = _relpath(local_surface, root)
    text = _load_text(local_surface)
    lines = text.splitlines()
    citations = [
        _make_citation(relpath, idx, line)
        for idx, line in enumerate(lines, start=1)
        if idx <= 12 and line.strip()
    ][:4]
    return {
        "path": relpath,
        "citations": citations,
    }


def _authority_state(
    *,
    doctrine_citations: list[dict[str, object]],
    local_governing_surface: dict[str, object] | None,
    conflict_signal: bool = False,
) -> str:
    if conflict_signal:
        return "conflicting_signals"
    if doctrine_citations:
        return "explicit_live_authority"
    if local_governing_surface is not None:
        return "implied_by_local_documentation"
    return "no_discernible_authority"


def _obvious_authority_label(
    *,
    doctrine_citations: list[dict[str, object]],
    local_governing_surface: dict[str, object] | None,
    ignored: bool,
) -> str:
    if doctrine_citations:
        return "live doctrine"
    if local_governing_surface is not None:
        return f"local governing surface ({local_governing_surface['path']})"
    if ignored:
        return "ignore rules only"
    return "none found"


def _root_folder_citations(name: str, doctrine_lines: dict[str, list[str]]) -> list[dict[str, object]]:
    return _find_citations(
        doctrine_lines,
        exact_tokens=[f"`{name}/`", f"`{name}`"],
        loose_tokens=[f"{name}/", name],
    )


def _dotfolder_citations(name: str, doctrine_lines: dict[str, list[str]]) -> list[dict[str, object]]:
    return _find_citations(
        doctrine_lines,
        exact_tokens=[f"`{name}/`", f"`{name}`"],
        loose_tokens=[f"{name}/", name],
    )


def _dotfolder_roster_signals(root: Path, dotfolder: str) -> dict[str, object]:
    agents_path = root / "!" / "AGENTS.md"
    lines = _load_text(agents_path).splitlines()
    roster_range = _find_heading_range(lines, "Direct-Write Agents (Autoloaded)")
    advisory_range = _find_heading_range(lines, "Advisory & Specialized Agents")
    recovery_range = _find_heading_range(lines, "Narrative Recovery Layer")

    live_roster_citations: list[dict[str, object]] = []
    recovery_citations: list[dict[str, object]] = []

    live_ranges = [section for section in (roster_range, advisory_range) if section is not None]
    for start, end in live_ranges:
        for idx in range(start, end):
            if dotfolder in lines[idx]:
                live_roster_citations.append(_make_citation("!/AGENTS.md", idx + 1, lines[idx]))

    if recovery_range is not None:
        start, end = recovery_range
        for idx in range(start, end):
            if dotfolder in lines[idx]:
                recovery_citations.append(_make_citation("!/AGENTS.md", idx + 1, lines[idx]))

    return {
        "appears_in_live_roster": bool(live_roster_citations),
        "appears_in_recovery_layer": bool(recovery_citations),
        "live_roster_citations": live_roster_citations[:6],
        "recovery_citations": recovery_citations[:6],
    }


def _dotfolder_surface_signals(path: Path) -> dict[str, list[str]]:
    owner_paths: list[str] = []
    shared_paths: list[str] = []
    archive_paths: list[str] = []
    try:
        children = sorted(path.iterdir(), key=lambda child: child.name.lower())
    except OSError:
        return {
            "owner_signal_paths": owner_paths,
            "shared_signal_paths": shared_paths,
            "archive_signal_paths": archive_paths,
        }

    for child in children:
        name = child.name
        if name in {"MEMORY", "memories", "archive", "archives"}:
            archive_paths.append(name)
        elif name in {"README.md", "AGENTS.md", "copilot-instructions.md", "config.toml"}:
            shared_paths.append(name)
        elif child.is_file() and name.endswith(".md") and name.upper() == name:
            shared_paths.append(name)
        elif name in {"logs", "history"}:
            archive_paths.append(name)
        elif name not in {"__pycache__", "cache", "tmp"}:
            owner_paths.append(name)

    return {
        "owner_signal_paths": owner_paths[:TOP_LEVEL_SUMMARY_LIMIT],
        "shared_signal_paths": shared_paths[:TOP_LEVEL_SUMMARY_LIMIT],
        "archive_signal_paths": archive_paths[:TOP_LEVEL_SUMMARY_LIMIT],
    }


def _dotfolder_memory_state(root: Path, dotfolder: str, tracked_files: set[str]) -> dict[str, object]:
    memory_rel = f"{dotfolder}/MEMORY"
    memory_path = root / Path(memory_rel)
    tracked_memory = any(path.startswith(f"{memory_rel}/") for path in tracked_files)
    return {
        "memory_dir_exists": memory_path.exists(),
        "memory_dir_tracked": tracked_memory,
    }


def _nest_duplicate_key(name: str) -> str:
    return re.sub(r"\s+\d+$", "", name.strip().casefold())


def _compute_nest_conflicts(root: Path) -> dict[str, list[str]]:
    conflicts: dict[str, list[str]] = defaultdict(list)
    for parent in [root / "!"]:
        if not parent.exists():
            continue
        try:
            children = [child for child in parent.iterdir() if child.is_dir()]
        except OSError:
            continue
        groups: dict[str, list[str]] = defaultdict(list)
        for child in children:
            groups[_nest_duplicate_key(child.name)].append(_relpath(child, root))
        for paths in groups.values():
            if len(paths) > 1:
                for path in paths:
                    conflicts[path] = [other for other in paths if other != path]
    return conflicts


def _nest_room_status(
    *,
    text: str,
    duplicate_conflicts: list[str],
    structure_sample: dict[str, object],
) -> str:
    if duplicate_conflicts:
        return "ambiguous"

    lowered = text.casefold()
    has_live = any(token in lowered for token in NEST_STATUS_LIVE_HINTS)
    has_historical = any(token in lowered for token in NEST_STATUS_HISTORICAL_HINTS)
    if has_live and has_historical:
        return "mixed"
    if has_historical:
        return "historical"
    if has_live:
        return "live"

    sample = " ".join(structure_sample.get("sample_children", [])).casefold()
    if "handoff" in sample or "audit" in sample or "levelset" in sample or "report" in sample:
        return "historical"
    return "ambiguous"


def _gather_root_entries(root: Path, doctrine_lines: dict[str, list[str]], tracked_files: set[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(
        (
            child
            for child in root.iterdir()
            if child.is_dir() and child.name != ROOT_EXCLUDED_NAME and not child.name.startswith(".")
        ),
        key=lambda item: item.name.lower(),
    ):
        relpath = _relpath(path, root)
        structure, access_errors = _sample_children(path)
        ignored = _git_path_is_ignored(root, relpath)
        status_lines = _git_status_lines(root, relpath)
        tracked = _tracked_prefix_exists(relpath, tracked_files)
        doctrine_citations = _root_folder_citations(path.name, doctrine_lines)
        local_governing_surface = _governing_surface_summary(root, path)
        entry = {
            "scope": "root",
            "path": relpath,
            "name": path.name,
            "git_state": {
                "tracked_prefix": tracked,
                "ignored": ignored,
                "status_lines": status_lines,
            },
            "structure": structure,
            "access_errors": access_errors,
            "appears_in_live_doctrine": bool(doctrine_citations),
            "appears_in_ignore_rules": ignored,
            "local_governing_surface": local_governing_surface,
            "authority_state": _authority_state(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
            ),
            "obvious_authority": _obvious_authority_label(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
                ignored=ignored,
            ),
            "authority_citations": doctrine_citations[:6],
            "notes": [],
        }
        if ignored and doctrine_citations:
            entry["notes"].append("Folder appears in live doctrine and also has ignore-based local signals.")
        if access_errors:
            entry["notes"].append("Folder could not be fully inspected.")
        entries.append(entry)
    return entries


def _gather_dotfolder_entries(root: Path, doctrine_lines: dict[str, list[str]], tracked_files: set[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(
        (child for child in root.iterdir() if child.is_dir() and child.name.startswith(".")),
        key=lambda item: item.name.lower(),
    ):
        relpath = _relpath(path, root)
        structure, access_errors = _sample_children(path)
        ignored = _git_path_is_ignored(root, relpath)
        status_lines = _git_status_lines(root, relpath)
        tracked = _tracked_prefix_exists(relpath, tracked_files)
        doctrine_citations = _dotfolder_citations(path.name, doctrine_lines)
        local_governing_surface = _governing_surface_summary(root, path)
        roster = _dotfolder_roster_signals(root, path.name)
        memory = _dotfolder_memory_state(root, path.name, tracked_files)
        surface_signals = _dotfolder_surface_signals(path)
        entry = {
            "scope": "dotfolders",
            "path": relpath,
            "name": path.name,
            "git_state": {
                "tracked_prefix": tracked,
                "ignored": ignored,
                "status_lines": status_lines,
            },
            "structure": structure,
            "access_errors": access_errors,
            "appears_in_live_doctrine": bool(doctrine_citations),
            "local_governing_surface": local_governing_surface,
            "authority_state": _authority_state(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
            ),
            "obvious_authority": _obvious_authority_label(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
                ignored=ignored,
            ),
            "authority_citations": doctrine_citations[:6],
            "live_roster": roster["appears_in_live_roster"],
            "historical_recovery": roster["appears_in_recovery_layer"],
            "live_roster_citations": roster["live_roster_citations"],
            "historical_recovery_citations": roster["recovery_citations"],
            "surface_signals": surface_signals,
            "memory_state": memory,
            "notes": [],
        }
        if access_errors:
            entry["notes"].append("Dotfolder could not be fully inspected.")
        if not roster["appears_in_live_roster"] and not roster["appears_in_recovery_layer"]:
            entry["notes"].append("Dotfolder does not appear in the live roster or recovery layer.")
        entries.append(entry)
    return entries


def _walk_nest_rooms(root: Path) -> list[Path]:
    nest_root = root / "!"
    rooms: list[Path] = []
    if not nest_root.exists():
        return rooms
    for path in sorted(nest_root.rglob("*"), key=lambda item: _normalize(item.relative_to(root)).lower()):
        if path.is_dir():
            rooms.append(path)
    return rooms


def _gather_nest_entries(root: Path, doctrine_lines: dict[str, list[str]], tracked_files: set[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    duplicate_conflicts = _compute_nest_conflicts(root)
    for path in _walk_nest_rooms(root):
        relpath = _relpath(path, root)
        structure, access_errors = _sample_children(path)
        ignored = _git_path_is_ignored(root, relpath)
        status_lines = _git_status_lines(root, relpath)
        tracked = _tracked_prefix_exists(relpath, tracked_files)
        doctrine_citations = _find_citations(
            doctrine_lines,
            exact_tokens=[f"`{relpath}`", f"`{relpath}/`"],
            loose_tokens=[relpath],
        )
        local_governing_surface = _governing_surface_summary(root, path)
        local_text = ""
        if local_governing_surface is not None:
            local_text = _load_text(root / Path(local_governing_surface["path"]))
        duplicate_paths = duplicate_conflicts.get(relpath, [])
        room_status = _nest_room_status(
            text=local_text,
            duplicate_conflicts=duplicate_paths,
            structure_sample=structure,
        )
        entry = {
            "scope": "nest",
            "path": relpath,
            "name": path.name,
            "depth": len(path.relative_to(root / "!").parts),
            "git_state": {
                "tracked_prefix": tracked,
                "ignored": ignored,
                "status_lines": status_lines,
            },
            "structure": structure,
            "access_errors": access_errors,
            "local_governing_surface": local_governing_surface,
            "authority_state": _authority_state(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
                conflict_signal=bool(duplicate_paths),
            ),
            "obvious_authority": _obvious_authority_label(
                doctrine_citations=doctrine_citations,
                local_governing_surface=local_governing_surface,
                ignored=ignored,
            ),
            "authority_citations": doctrine_citations[:6],
            "room_status": room_status,
            "duplicate_conflicts": duplicate_paths,
            "notes": [],
        }
        if duplicate_paths:
            entry["notes"].append(
                "Room has a competing sibling path with the same normalized key."
            )
        if access_errors:
            entry["notes"].append("Room could not be fully inspected.")
        entries.append(entry)
    return entries


def _scope_summary(scope: str, entries: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {
        "entry_count": len(entries),
        "authority_state_counts": dict(Counter(entry["authority_state"] for entry in entries)),
    }
    if scope == "root":
        summary["appears_in_live_doctrine_count"] = sum(
            1 for entry in entries if entry["appears_in_live_doctrine"]
        )
        summary["appears_in_ignore_rules_count"] = sum(
            1 for entry in entries if entry["appears_in_ignore_rules"]
        )
    elif scope == "dotfolders":
        summary["live_roster_count"] = sum(1 for entry in entries if entry["live_roster"])
        summary["historical_recovery_count"] = sum(
            1 for entry in entries if entry["historical_recovery"]
        )
        summary["tracked_memory_count"] = sum(
            1 for entry in entries if entry["memory_state"]["memory_dir_tracked"]
        )
    elif scope == "nest":
        summary["room_status_counts"] = dict(Counter(entry["room_status"] for entry in entries))
        summary["duplicate_conflict_count"] = sum(
            1 for entry in entries if entry["duplicate_conflicts"]
        )
    return summary


def build_scope_report(root: Path, scope: str) -> dict[str, object]:
    doctrine_lines = _load_live_doctrine(root)
    tracked_files = _git_tracked_files(root)
    if scope == "root":
        entries = _gather_root_entries(root, doctrine_lines, tracked_files)
    elif scope == "dotfolders":
        entries = _gather_dotfolder_entries(root, doctrine_lines, tracked_files)
    elif scope == "nest":
        entries = _gather_nest_entries(root, doctrine_lines, tracked_files)
    else:
        raise ValueError(f"Unsupported scope: {scope}")

    return {
        "scope": scope,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo_root": str(root),
        "doctrine_sources": list(LIVE_DOCTRINE_PATHS),
        "summary": _scope_summary(scope, entries),
        "entries": entries,
    }


def _render_git_state(git_state: dict[str, object]) -> str:
    pieces = [
        f"tracked={'yes' if git_state['tracked_prefix'] else 'no'}",
        f"ignored={'yes' if git_state['ignored'] else 'no'}",
    ]
    status_lines = git_state.get("status_lines") or []
    if status_lines:
        pieces.append("status=" + "; ".join(status_lines[:3]))
    return ", ".join(pieces)


def _render_citations(citations: list[dict[str, object]]) -> list[str]:
    return [
        f"- `{citation['path']}:{citation['line']}` — {citation['excerpt']}"
        for citation in citations
    ]


def render_scope_markdown(report: dict[str, object]) -> str:
    scope = report["scope"]
    summary = report["summary"]
    lines = [
        f"# Topology Census — {scope}",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Repo root: `{report['repo_root']}`",
        f"- Entries: `{summary['entry_count']}`",
        "",
        "## Summary",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in summary.items():
        if isinstance(value, dict):
            continue
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    for key, mapping in summary.items():
        if not isinstance(mapping, dict):
            continue
        lines.extend(
            [
                "",
                f"### {key.replace('_', ' ')}",
                "",
                "| Value | Count |",
                "|---|---:|",
            ]
        )
        for subkey, count in sorted(mapping.items()):
            lines.append(f"| `{subkey}` | {count} |")

    lines.extend(["", "## Entries", ""])
    for entry in report["entries"]:
        lines.append(f"### `{entry['path']}`")
        lines.append("")
        lines.append(f"- Authority state: `{entry['authority_state']}`")
        if scope == "nest":
            lines.append(f"- Room status: `{entry['room_status']}`")
        lines.append(f"- Obvious authority: {entry['obvious_authority']}")
        lines.append(f"- Git state: {_render_git_state(entry['git_state'])}")
        structure = entry["structure"]
        if structure["accessible"]:
            lines.append(
                f"- Structure: `{structure['dir_count']}` dirs, `{structure['file_count']}` files"
            )
            if structure["sample_children"]:
                lines.append(
                    "- Sample children: " + "; ".join(structure["sample_children"])
                )
        else:
            lines.append("- Structure: inaccessible during census")
        if scope == "root":
            lines.append(
                f"- Live doctrine mention: `{'yes' if entry['appears_in_live_doctrine'] else 'no'}`"
            )
            lines.append(
                f"- Ignore-rule signal: `{'yes' if entry['appears_in_ignore_rules'] else 'no'}`"
            )
        elif scope == "dotfolders":
            lines.append(f"- Live roster: `{'yes' if entry['live_roster'] else 'no'}`")
            lines.append(
                f"- Historical recovery layer: `{'yes' if entry['historical_recovery'] else 'no'}`"
            )
            lines.append(
                f"- Tracked MEMORY: `{'yes' if entry['memory_state']['memory_dir_tracked'] else 'no'}`"
            )
            surface_signals = entry["surface_signals"]
            lines.append(
                "- Surface signals: "
                f"OWNER={surface_signals['owner_signal_paths'] or []}; "
                f"SHARED={surface_signals['shared_signal_paths'] or []}; "
                f"ARCHIVE={surface_signals['archive_signal_paths'] or []}"
            )
        elif scope == "nest" and entry["duplicate_conflicts"]:
            lines.append(
                "- Duplicate conflicts: " + ", ".join(f"`{path}`" for path in entry["duplicate_conflicts"])
            )
        if entry["local_governing_surface"] is not None:
            lines.append(
                f"- Local governing surface: `{entry['local_governing_surface']['path']}`"
            )
        if entry["notes"]:
            lines.append("- Notes:")
            for note in entry["notes"]:
                lines.append(f"  - {note}")
        if entry["authority_citations"]:
            lines.append("- Authority citations:")
            lines.extend(f"  {line}" for line in _render_citations(entry["authority_citations"]))
        if scope == "dotfolders" and entry["live_roster_citations"]:
            lines.append("- Live roster citations:")
            lines.extend(f"  {line}" for line in _render_citations(entry["live_roster_citations"]))
        if scope == "dotfolders" and entry["historical_recovery_citations"]:
            lines.append("- Recovery-layer citations:")
            lines.extend(
                f"  {line}" for line in _render_citations(entry["historical_recovery_citations"])
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _artifact_paths(output_dir: Path, scope: str, run_id: str) -> tuple[Path, Path]:
    prefix = f"TOPOLOGY-CENSUS-{scope}-{run_id}"
    return (
        output_dir / f"{prefix}.md",
        output_dir / f"{prefix}.json",
    )


def render_index_markdown(run_id: str, generated: list[dict[str, str]]) -> str:
    lines = [
        f"# Topology Census Index — {run_id}",
        "",
        "## Generated Artifacts",
        "",
        "| Scope | Markdown | JSON |",
        "|---|---|---|",
    ]
    for row in generated:
        lines.append(
            f"| `{row['scope']}` | `{row['markdown']}` | `{row['json']}` |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_scope_reports(
    *,
    root: Path,
    output_dir: Path,
    scopes: list[str],
) -> dict[str, object]:
    run_id = datetime.now(timezone.utc).strftime(RUN_ID_FORMAT)
    generated: list[dict[str, str]] = []
    scope_reports: dict[str, dict[str, object]] = {}

    for scope in scopes:
        report = build_scope_report(root, scope)
        markdown_path, json_path = _artifact_paths(output_dir, scope, run_id)
        _write_text(markdown_path, render_scope_markdown(report))
        _write_text(json_path, json.dumps(report, indent=2) + "\n")
        scope_reports[scope] = report
        generated.append(
            {
                "scope": scope,
                "markdown": _normalize(markdown_path.relative_to(root)),
                "json": _normalize(json_path.relative_to(root)),
            }
        )

    index_path = output_dir / f"TOPOLOGY-CENSUS-INDEX-{run_id}.md"
    _write_text(index_path, render_index_markdown(run_id, generated))
    return {
        "run_id": run_id,
        "generated": generated,
        "index": _normalize(index_path.relative_to(root)),
        "reports": scope_reports,
    }


def _resolve_scopes(scope: str) -> list[str]:
    if scope == "all":
        return ["root", "dotfolders", "nest"]
    return [scope]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("root", "dotfolders", "nest", "all"),
        default="all",
        help="Which topology scope to census.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory for durable report output. Defaults to !/ under the repo root.",
    )
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir

    result = write_scope_reports(
        root=REPO_ROOT,
        output_dir=output_dir,
        scopes=_resolve_scopes(args.scope),
    )
    sys.stdout.write(json.dumps(
        {
            "run_id": result["run_id"],
            "index": result["index"],
            "generated": result["generated"],
        },
        indent=2,
    ) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
