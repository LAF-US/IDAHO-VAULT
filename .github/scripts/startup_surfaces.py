#!/usr/bin/env python3
"""Resolve vault startup/doctrine surfaces to wherever they currently live.

A surface's *path* is not part of its identity. `!/WAKEUP.md` may sit at its
canonical path, at its NETWEB `_PREFIX` alias (`!-WAKEUP.md`, see
VAULT-CONVENTIONS § Portable Path Standard), or somewhere else entirely
because the Architect moved it. None of those is a defect.

Before this module, five places hard-coded `"!/WAKEUP.md"` independently:

    .github/workflows/cross-platform-smoke.yml
    .github/scripts/meshnetweb_portability_check.py   (must-find list)
    .github/scripts/topology_census.py                (doctrine paths)
    .github/scripts/generate_agents_bootstrap.py      (optional context)
    .github/scripts/validate_content.py               (protection list)

Moving the file broke the first three loudly and the fourth *silently* — a
protection list keyed to a stale path simply stops protecting anything, and
nothing fails to tell you. Ask this module instead of naming a path.

Two different questions, two different functions:

    resolve()     "where is this surface right now?"  -> one Path, or None
    candidates()  "every path this surface may occupy" -> all of them

Guard and protection lists want `candidates()`: covering a path that does not
currently exist costs nothing and keeps the guard correct across a move in
either direction. Readers want `resolve()`.
"""

from __future__ import annotations

from pathlib import Path

# Logical name -> candidate relative paths, most canonical first.
SURFACES: dict[str, tuple[str, ...]] = {
    "AGENTS": ("AGENTS.md",),
    "CONSTITUTION": ("CONSTITUTION.md",),
    "DECISIONS": ("DECISIONS.md",),
    "VAULT_CONVENTIONS": ("VAULT-CONVENTIONS.md",),
    "LEVELSET": ("LEVELSET.md",),
    "SWARM": ("swarm.json",),
    # NEST surfaces: canonical `!/` path, NETWEB `_PREFIX` alias, then the
    # flattened root form that a move or a copy can leave behind.
    "WAKEUP": ("!/WAKEUP.md", "!-WAKEUP.md", "WAKEUP.md"),
    "NEST_README": ("!/README.md", "!-README.md", "!README.md"),
    "NEST_AGENTS": ("!/AGENTS.md", "!-AGENTS.md"),
}


def repo_root() -> Path:
    """Repository root, derived from this file's location."""
    return Path(__file__).resolve().parents[2]


def candidates(name: str) -> tuple[str, ...]:
    """Every relative path `name` may legitimately occupy.

    Raises KeyError for an unknown surface — a typo should fail loudly here
    rather than quietly resolve to nothing downstream.
    """
    return SURFACES[name]


def resolve(name: str, root: Path | None = None) -> Path | None:
    """Absolute path to `name` where it actually is, or None if nowhere."""
    base = repo_root() if root is None else root
    for rel in candidates(name):
        path = base / rel
        if path.exists():
            return path
    return None


def resolve_rel(name: str, root: Path | None = None) -> str | None:
    """As `resolve`, but returns the repo-relative path that matched."""
    base = repo_root() if root is None else root
    for rel in candidates(name):
        if (base / rel).exists():
            return rel
    return None


def missing(names: list[str], root: Path | None = None) -> list[str]:
    """Names that cannot be found at any of their candidate paths."""
    return [n for n in names if resolve(n, root) is None]


def describe(names: list[str], root: Path | None = None) -> str:
    """Human-readable resolution table, for CI logs."""
    lines = []
    for name in names:
        rel = resolve_rel(name, root)
        if rel is None:
            lines.append(
                f"  MISSING  {name:<18}   looked for: "
                + ", ".join(candidates(name))
            )
        else:
            lines.append(f"  ok       {name:<18} -> {rel}")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Startup surfaces:")
    print(describe(list(SURFACES)))
