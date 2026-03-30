#!/usr/bin/env python3
"""Update manifest.json with a soft-lock lifecycle and entry metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_TTL_MINUTES = 15


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def parse_iso(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "manifest_version": "1.0.0",
        "generated_at": iso_z(utc_now()),
        "authority": {
            "canonical_system": "github",
            "interface_system": "obsidian",
            "fallback_mode": "filesystem",
        },
        "sync": {
            "primary_dataset": "vault",
            "sync_unit": ["file", "manifest_entry"],
            "trigger_model": "event_based_write_read_cycle",
        },
        "mcp": {
            "enabled": False,
            "mode": "transport_only",
            "server": None,
            "notes": "Enable after Obsidian MCP Tools endpoint and write controls are validated.",
        },
        "locks": [],
        "entries": {},
    }


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

    now = utc_now()
    manifest = load_manifest(manifest_path)
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
