"""Vault-local runtime containment for the CrewAI bootstrap shard."""

from __future__ import annotations

import os
from pathlib import Path


def _set_runtime_path(name: str, path: Path) -> None:
    """Point an environment variable at a vault-local directory."""
    path.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(path)


def configure_vault_runtime() -> dict[str, str]:
    """Keep CrewAI runtime state inside the vault.

    CrewAI uses appdirs-backed storage for kickoff SQLite databases and related
    runtime files. In sandboxed or shared environments, the default user-level
    AppData targets can fail or drift outside the vault. This function redirects
    the relevant paths into repo-local runtime directories before CrewAI starts.
    """

    vault_root = Path(__file__).resolve().parents[2]
    runtime_root = vault_root / ".agent-home" / "crewai"

    path_map = {
        "APPDATA": runtime_root / "AppData" / "Roaming",
        "LOCALAPPDATA": runtime_root / "AppData" / "Local",
        "HOME": runtime_root,
        "USERPROFILE": runtime_root,
        "TMP": vault_root / ".tmp",
        "TEMP": vault_root / ".tmp",
        "TMPDIR": vault_root / ".tmp",
        "XDG_CACHE_HOME": vault_root / ".cache",
        "XDG_STATE_HOME": vault_root / ".state",
        "XDG_DATA_HOME": vault_root / ".state",
    }

    for name, path in path_map.items():
        _set_runtime_path(name, path)

    os.environ.setdefault("CREWAI_STORAGE_DIR", vault_root.name)

    drive = runtime_root.drive or Path.cwd().drive
    if drive:
        os.environ["HOMEDRIVE"] = drive
        os.environ["HOMEPATH"] = str(runtime_root).replace(drive, "", 1)

    return {name: os.environ[name] for name in sorted(path_map)}
