#!/usr/bin/env python3
"""Update manifest.json with a soft-lock lifecycle and execution-state metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DEFAULT_TTL_MINUTES = 15
DEFAULT_AUTHORITY = {
    "canonical_system": "vault",
    "execution_system": "github",
    "interface_system": "obsidian",
    "fallback_mode": "filesystem",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def parse_iso(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def obsidian_note_to_path(note_name: str) -> str | None:
    cleaned = note_name.strip().replace("\\", "/").strip("/")
    if not cleaned:
        return None
    if not cleaned.lower().endswith(".md"):
        cleaned = f"{cleaned}.md"
    return cleaned


def build_obsidian_template_inventory(repo_root: Path) -> dict:
    obsidian_dir = repo_root / ".obsidian"
    daily_notes = load_json(obsidian_dir / "daily-notes.json", {})
    templates = load_json(obsidian_dir / "templates.json", {})
    community_plugins = load_json(obsidian_dir / "community-plugins.json", [])

    concrete_bindings = []
    folder_bindings = []
    untracked_plugins = []

    daily_template = obsidian_note_to_path(str(daily_notes.get("template", "")))
    if daily_template:
        concrete_bindings.append(
            {
                "client": "obsidian",
                "plugin": "core/daily-notes",
                "config_path": ".obsidian/daily-notes.json",
                "template_path": daily_template,
                "mode": "daily_note",
                "status": "active",
                "note_folder": str(daily_notes.get("folder", "")),
            }
        )

    if isinstance(templates, dict):
        folder_bindings.append(
            {
                "client": "obsidian",
                "plugin": "core/templates",
                "config_path": ".obsidian/templates.json",
                "folder": str(templates.get("folder", "")),
                "date_format": str(templates.get("dateFormat", "")),
                "time_format": str(templates.get("timeFormat", "")),
                "status": "folder_only",
                "note": "Tracked config exposes a template pool, not concrete template file bindings.",
            }
        )

    if "templater-obsidian" in community_plugins:
        untracked_plugins.append(
            {
                "client": "obsidian",
                "plugin": "templater-obsidian",
                "status": "installed_untracked_config",
                "config_path": ".obsidian/plugins/templater-obsidian/data.json",
                "note": "Plugin settings are intentionally private via Obsidian Sync and are not read into swarm tracking.",
            }
        )

    return {
        "source_of_truth": "tracked_obsidian_config",
        "concrete_bindings": concrete_bindings,
        "folder_bindings": folder_bindings,
        "untracked_plugins": untracked_plugins,
    }


def build_swarm_template_tracking(template_inventory: dict) -> dict:
    concrete_bindings = [
        {
            "client": binding["client"],
            "plugin": binding["plugin"],
            "config_path": binding["config_path"],
            "template_path": binding["template_path"],
            "mode": binding["mode"],
            "status": binding["status"],
        }
        for binding in template_inventory.get("concrete_bindings", [])
    ]

    folder_bindings = [
        {
            "client": binding["client"],
            "plugin": binding["plugin"],
            "config_path": binding["config_path"],
            "folder": binding["folder"],
            "status": binding["status"],
            "note": binding["note"],
        }
        for binding in template_inventory.get("folder_bindings", [])
    ]

    untracked_plugins = [
        {
            "client": plugin["client"],
            "plugin": plugin["plugin"],
            "status": plugin["status"],
            "config_path": plugin["config_path"],
            "note": plugin["note"],
        }
        for plugin in template_inventory.get("untracked_plugins", [])
    ]

    return {
        "source_of_truth": "tracked_obsidian_config",
        "registry_files": ["manifest.json", "swarm.json"],
        "policy": (
            "Concrete Obsidian template files named by tracked client config "
            "must be mirrored here and in manifest.json. Folder-only plugin "
            "scopes and private plugin settings must be declared explicitly "
            "instead of guessed."
        ),
        "concrete_bindings": concrete_bindings,
        "folder_bindings": folder_bindings,
        "untracked_plugins": untracked_plugins,
    }


def sync_swarm_template_tracking(repo_root: Path, template_inventory: dict) -> None:
    swarm_path = repo_root / "swarm.json"
    if not swarm_path.exists():
        return

    swarm = load_json(swarm_path, {})
    tracking = build_swarm_template_tracking(template_inventory)
    if swarm.get("template_tracking") == tracking:
        return

    swarm["template_tracking"] = tracking
    swarm_path.write_text(json.dumps(swarm, indent=2) + "\n", encoding="utf-8")


def load_manifest(path: Path) -> dict:
    repo_root = path.parent
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "manifest_version": "1.0.0",
        "generated_at": iso_z(utc_now()),
        "authority": DEFAULT_AUTHORITY.copy(),
        "sync": {
            "primary_dataset": "vault",
            "sync_unit": ["file", "manifest_entry"],
            "trigger_model": "event_based_write_read_cycle",
        },
        "mcp": {
            "enabled": False,
            "mode": "transpo***REMOVED***only",
            "server": None,
            "notes": "Enable after Obsidian MCP Tools endpoint and write controls are validated.",
        },
        "obsidian_templates": build_obsidian_template_inventory(repo_root),
        "locks": [],
        "entries": {},
    }


def normalize_manifest(manifest: dict, repo_root: Path) -> None:
    """Keep the authority block aligned with the current transport model."""
    manifest["authority"] = DEFAULT_AUTHORITY.copy()
    template_inventory = build_obsidian_template_inventory(repo_root)
    manifest["obsidian_templates"] = template_inventory
    sync_swarm_template_tracking(repo_root, template_inventory)


def expire_stale_locks(manifest: dict, now: datetime) -> None:
    for lock in manifest.get("locks", []):
        if lock.get("state") != "active":
            continue
        if parse_iso(lock["expires_at"]) <= now:
            lock["state"] = "expired"


def acquire_lock(manifest: dict, file_path: str, agent_id: str, now: datetime, ttl_minutes: int) -> dict:
    for lock in manifest.get("locks", []):
        if lock.get("file_path") != file_path:
            continue
        if lock.get("state") != "active":
            continue
        if lock.get("agent_id") == agent_id:
            return lock
        raise RuntimeError(f"active lock conflict for {file_path} (holder={lock.get('agent_id')})")

    lock = {
        "lock_id": str(uuid.uuid4()),
        "file_path": file_path,
        "agent_id": agent_id,
        "created_at": iso_z(now),
        "expires_at": iso_z(now + timedelta(minutes=ttl_minutes)),
        "state": "active",
    }
    manifest.setdefault("locks", []).append(lock)
    return lock


def update_entry(manifest: dict, file_path: str, file_abs: Path, agent_id: str, lock_id: str, now: datetime) -> None:
    entries = manifest.setdefault("entries", {})
    prior = entries.get(file_path)
    version = 1 if prior is None else int(prior.get("version", 0)) + 1

    entries[file_path] = {
        "content_hash": sha256_file(file_abs),
        "last_writer": agent_id,
        "last_write_at": iso_z(now),
        "last_read_at": iso_z(now),
        "status": "active",
        "lock_id": lock_id,
        "version": version,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="manifest.json", help="Path to manifest file")
    parser.add_argument("--file", required=True, help="Repo-relative file path being written")
    parser.add_argument("--agent-id", required=True, help="Agent identity for lock/entry metadata")
    parser.add_argument("--ttl-minutes", type=int, default=DEFAULT_TTL_MINUTES)
    parser.add_argument(
        "--phase",
        choices=["acquire", "release"],
        default=None,
        help=(
            "Two-phase lock protocol: "
            "'acquire' records an active lock BEFORE the file is written; "
            "'release' updates the entry and releases the lock AFTER the file is written. "
            "Omitting --phase runs the legacy single-step mode (acquire + release in one call, "
            "file must already exist)."
        ),
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    file_path = args.file
    file_abs = Path(file_path)
    repo_root = manifest_path.parent

    now = utc_now()
    manifest = load_manifest(manifest_path)
    normalize_manifest(manifest, repo_root)
    expire_stale_locks(manifest, now)

    if args.phase == "acquire":
        # Phase 1: record an active lock before the file is written.
        # The file does not need to exist yet.
        lock = acquire_lock(manifest, file_path, args.agent_id, now, args.ttl_minutes)
        manifest["generated_at"] = iso_z(now)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"lock acquired for {file_path}: {lock['lock_id']} (expires {lock['expires_at']})")
        return 0

    if args.phase == "release":
        # Phase 2: update the manifest entry and release the lock after the file was written.
        if not file_abs.exists():
            raise FileNotFoundError(f"target file not found: {file_path} (did the write step succeed?)")
        lock = acquire_lock(manifest, file_path, args.agent_id, now, args.ttl_minutes)
        update_entry(manifest, file_path, file_abs, args.agent_id, lock["lock_id"], now)
        lock["state"] = "released"
        manifest["generated_at"] = iso_z(now)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"manifest updated for {file_path} with lock {lock['lock_id']} (released)")
        return 0

    # Legacy single-step mode: file must already exist.
    if not file_abs.exists():
        raise FileNotFoundError(f"target file not found: {file_path}")

    lock = acquire_lock(manifest, file_path, args.agent_id, now, args.ttl_minutes)
    update_entry(manifest, file_path, file_abs, args.agent_id, lock["lock_id"], now)
    lock["state"] = "released"
    manifest["generated_at"] = iso_z(now)

    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"manifest updated for {file_path} with lock {lock['lock_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
