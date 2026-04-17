"""Shared executable view of the live startup and operator front door."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import subprocess
from typing import Iterable


BOOT_CHAIN_SURFACES = (
    "AGENTS.md",
    "!/WAKEUP.md",
    "!/README.md",
    "!/AGENTS.md",
    "CONSTITUTION.md",
    "swarm.json",
)

OPERATOR_FRONT_DOOR_SURFACES = (
    "DAILY NOTE TEMPLATE.md",
    ".obsidian/daily-notes.json",
    ".obsidian/plugins/periodic-notes/data.json",
    ".github/scripts/daily_rollover.py",
    "TO DO LIST.md",
)


@dataclass(frozen=True)
class SurfaceStatus:
    relpath: str
    exists: bool
    tracked: bool | None = None


@dataclass(frozen=True)
class EvidenceStatus:
    ref: str
    relpath: str
    exists: bool
    tracked: bool | None = None


@dataclass(frozen=True)
class OperatorContext:
    root: Path
    target_date: date
    boot_chain_checks: tuple[SurfaceStatus, ...]
    front_door_checks: tuple[SurfaceStatus, ...]
    daily_note_path: str
    daily_note_exists: bool
    daily_note_tracked: bool | None
    daily_note_folder: str
    daily_note_format: str
    active_backlog_lines: tuple[str, ...]

    @property
    def boot_chain_ok(self) -> bool:
        return all(check.exists for check in self.boot_chain_checks)

    @property
    def front_door_ok(self) -> bool:
        return all(check.exists for check in self.front_door_checks)

    @property
    def current_daily_note_ok(self) -> bool:
        return self.daily_note_exists

    @property
    def operator_front_door_ok(self) -> bool:
        return self.front_door_ok and self.current_daily_note_ok

    @property
    def missing_boot_chain(self) -> tuple[str, ...]:
        return tuple(check.relpath for check in self.boot_chain_checks if not check.exists)

    @property
    def missing_front_door(self) -> tuple[str, ...]:
        return tuple(check.relpath for check in self.front_door_checks if not check.exists)

    @property
    def missing_operator_front_door(self) -> tuple[str, ...]:
        if self.current_daily_note_ok:
            return self.missing_front_door
        return (*self.missing_front_door, self.daily_note_path)

    @property
    def live_boot_chain_refs(self) -> tuple[str, ...]:
        return tuple(
            check.relpath
            for check in self.boot_chain_checks
            if check.exists and check.tracked is not False
        )

    @property
    def live_front_door_refs(self) -> tuple[str, ...]:
        refs = [
            check.relpath
            for check in self.front_door_checks
            if check.exists and check.tracked is not False
        ]
        if self.daily_note_exists and self.daily_note_tracked is not False:
            refs.append(self.daily_note_path)
        return tuple(refs)

    @property
    def open_backlog_items(self) -> tuple[str, ...]:
        items: list[str] = []
        for line in self.active_backlog_lines:
            stripped = line.strip()
            if not stripped.startswith("- [ ]"):
                continue
            if stripped in {"- [ ]", "- []"}:
                continue
            items.append(stripped)
        return tuple(items)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _normalize_relpath(relpath: str) -> str:
    return Path(relpath).as_posix()


def _tracked_files(root: Path) -> set[str] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return {_normalize_relpath(line) for line in result.stdout.splitlines() if line.strip()}


def _surface_status(root: Path, relpath: str, tracked_files: set[str] | None) -> SurfaceStatus:
    normalized = _normalize_relpath(relpath)
    path = root / Path(normalized)
    tracked = None if tracked_files is None else normalized in tracked_files
    return SurfaceStatus(relpath=normalized, exists=path.exists(), tracked=tracked)


def _load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _daily_note_settings(root: Path) -> tuple[str, str]:
    periodic_path = root / ".obsidian" / "plugins" / "periodic-notes" / "data.json"
    periodic = _load_json(periodic_path)
    if isinstance(periodic, dict):
        daily = periodic.get("daily")
        if isinstance(daily, dict) and daily.get("enabled", True):
            folder = str(daily.get("folder", "") or "")
            format_string = str(daily.get("format", "YYYY-MM-DD") or "YYYY-MM-DD")
            return folder, format_string

    legacy = _load_json(root / ".obsidian" / "daily-notes.json")
    folder = ""
    if isinstance(legacy, dict):
        folder = str(legacy.get("folder", "") or "")
    return folder, "YYYY-MM-DD"


def _render_obsidian_date(target_date: date, format_string: str) -> str:
    iso = target_date.isocalendar()
    replacements = {
        "GGGG": f"{iso.year:04d}",
        "YYYY": f"{target_date.year:04d}",
        "WW": f"{iso.week:02d}",
        "MM": f"{target_date.month:02d}",
        "DD": f"{target_date.day:02d}",
        "Q": str(((target_date.month - 1) // 3) + 1),
    }
    rendered = format_string
    for token in sorted(replacements, key=len, reverse=True):
        rendered = rendered.replace(token, replacements[token])
    return rendered.replace("[", "").replace("]", "")


def _extract_active_section(content: str) -> tuple[str, ...]:
    lines = content.splitlines()
    in_active = False
    active_lines: list[str] = []

    for line in lines:
        if line.strip() == "## Active":
            in_active = True
            continue

        if in_active:
            if line.startswith("## "):
                break
            active_lines.append(line)

    return tuple(active_lines)


def load_operator_context(
    *,
    root: Path | None = None,
    target_date: date | None = None,
) -> OperatorContext:
    """Resolve the live startup and operator front door surfaces for the repo."""

    root_path = root or _repo_root()
    resolved_date = target_date or date.today()
    tracked_files = _tracked_files(root_path)

    boot_checks = tuple(
        _surface_status(root_path, relpath, tracked_files) for relpath in BOOT_CHAIN_SURFACES
    )
    front_door_checks = tuple(
        _surface_status(root_path, relpath, tracked_files)
        for relpath in OPERATOR_FRONT_DOOR_SURFACES
    )

    daily_note_folder, daily_note_format = _daily_note_settings(root_path)
    rendered_name = f"{_render_obsidian_date(resolved_date, daily_note_format)}.md"
    daily_note_relpath = (
        _normalize_relpath(str(Path(daily_note_folder) / rendered_name))
        if daily_note_folder
        else rendered_name
    )
    daily_note_abs = root_path / Path(daily_note_relpath)
    daily_note_tracked = None if tracked_files is None else daily_note_relpath in tracked_files

    todo_path = root_path / "TO DO LIST.md"
    active_backlog_lines = ()
    if todo_path.exists():
        active_backlog_lines = _extract_active_section(todo_path.read_text(encoding="utf-8"))

    return OperatorContext(
        root=root_path,
        target_date=resolved_date,
        boot_chain_checks=boot_checks,
        front_door_checks=front_door_checks,
        daily_note_path=daily_note_relpath,
        daily_note_exists=daily_note_abs.exists(),
        daily_note_tracked=daily_note_tracked,
        daily_note_folder=daily_note_folder,
        daily_note_format=daily_note_format,
        active_backlog_lines=active_backlog_lines,
    )


def evaluate_evidence_refs(
    refs: Iterable[str],
    *,
    root: Path | None = None,
    tracked_files: set[str] | None = None,
) -> tuple[EvidenceStatus, ...]:
    """Resolve evidence refs against the repo root and report existence/tracked status."""

    root_path = root or _repo_root()
    resolved_tracked = tracked_files if tracked_files is not None else _tracked_files(root_path)

    seen: set[str] = set()
    results: list[EvidenceStatus] = []
    for ref in refs:
        if not ref:
            continue
        relpath = _normalize_relpath(ref.split("#", 1)[0])
        if relpath in seen:
            continue
        seen.add(relpath)
        path = root_path / Path(relpath)
        tracked = None if resolved_tracked is None else relpath in resolved_tracked
        results.append(
            EvidenceStatus(
                ref=ref,
                relpath=relpath,
                exists=path.exists(),
                tracked=tracked,
            )
        )

    return tuple(results)
