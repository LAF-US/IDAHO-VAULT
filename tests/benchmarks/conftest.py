"""Import wiring and shared corpora for the benchmark suite.

The automation guards under `.github/scripts/` are not an importable package
(they are run as standalone scripts by the policy workflows), so the benchmark
modules reach them the same way `.github/scripts/test_classify_paths.py` does:
by putting the script directory on `sys.path`.

The corpora below are deterministic — seeded once, built once per session — so
a benchmark measures the guard, never the fixture.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / ".github" / "scripts"
SCRIPTS_SCRIPTS_DIR = REPO_ROOT / "scripts_scripts"
SRC_DIR = REPO_ROOT / "src"

for _candidate in (SRC_DIR, SCRIPTS_DIR, SCRIPTS_SCRIPTS_DIR):
    _entry = str(_candidate)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)


CORPUS_SEED = 20260419

# Extensions in roughly the proportion the vault actually carries: mostly
# Markdown notes, a long tail of automation and captured assets.
_EXTENSIONS = (
    *([".md"] * 12),
    ".txt",
    ".json",
    ".yml",
    ".toml",
    ".csv",
    ".py",
    ".sh",
    ".ps1",
    ".ts",
    ".ipynb",
    ".pdf",
    ".jpeg",
    ".q3z",
)

# Directory prefixes spanning both filedepth axes the classifier scores.
_PREFIXES = (
    "",
    "",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/",
    ".github/scripts/",
    ".github/workflows/",
    "src/idaho_vault/",
    "!/",
    "!/!/",
    "!/!/__!__/!/",
)

_NAME_WORDS = (
    "Borah",
    "House Bill",
    "Senate Joint Memorial",
    "levelset",
    "handoff",
    "arborscaping",
    "census",
    "wayback",
    "rollover",
    "operator context",
    "swarm",
    "docket",
)


def _build_paths(count: int) -> list[str]:
    rng = random.Random(CORPUS_SEED)
    paths: list[str] = []
    for index in range(count):
        prefix = rng.choice(_PREFIXES)
        word = rng.choice(_NAME_WORDS)
        extension = rng.choice(_EXTENSIONS)
        paths.append(f"{prefix}{2026 - index % 40}-{index:05d} - {word}{extension}")
    # A handful of genuinely awkward names, because the guards' slow branches
    # are the ones that fire: reserved device names, trailing dots, Windows
    # separators, case-only collisions, and an over-long path.
    paths.extend(
        [
            "GOVERNMENTS/IDAHO - EXECUTIVE/AUX.md",
            "GOVERNMENTS/IDAHO - EXECUTIVE/aux.md",
            "!/COM1.txt",
            "!/trailing period.",
            "captures\\windows\\note (2).md",
            "captures/windows/note (2).md",
            f"!/!/__!__/!/{'deeply nested chamber/' * 12}note.md",
        ]
    )
    return paths


@pytest.fixture(scope="session")
def vault_paths() -> list[str]:
    """A changeset-shaped path corpus (~4k entries) for the path guards."""
    return _build_paths(4000)


@pytest.fixture(scope="session")
def small_vault_paths(vault_paths: list[str]) -> list[str]:
    """A smaller slice, for guards that run many regexes per path."""
    return vault_paths[:1500]


def _build_note(sections: int) -> str:
    rng = random.Random(CORPUS_SEED + 1)
    lines = [
        "---",
        "title: 'Operator handoff'",
        "status: active",
        "authority: LOGAN",
        "tags:",
        "  - Governments/Idaho",
        "  - governments/idaho",
        "  - '#Projects/Vault'",
        "  - dailynote",
        "  - category/legacy",
        "related:",
        "  - CONSTITUTION",
        "  - PROTOCOLS",
        "---",
        "",
        "# Operator handoff",
        "",
    ]
    for section in range(sections):
        lines.append(f"## Section {section}")
        lines.append("")
        for _ in range(6):
            lines.append(" ".join(rng.choice(_NAME_WORDS) for _ in range(9)))
        lines.append("")
        lines.append(f"#projects/section-{section}")
        lines.append("")
        lines.append(f"- [ ] follow up on section {section}")
        lines.append(f"- [x] archived item {section}")
        lines.append("")
    return "\n".join(lines)


@pytest.fixture(scope="session")
def vault_note() -> str:
    """A frontmattered Markdown note with inline tag lines and a long body."""
    return _build_note(60)


@pytest.fixture(scope="session")
def vault_note_bytes(vault_note: str) -> bytes:
    return vault_note.encode("utf-8")
