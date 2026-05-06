#!/usr/bin/env python3
"""Sync Obsidian plugin registry state from tracked Obsidian config.

The source of truth is the Obsidian interface state:

- .obsidian/community-plugins.json
- .obsidian/core-plugins.json
- .obsidian/plugins/*/manifest.json

This script updates the machine registries that agents read. It intentionally
does not parse or rewrite the long-form human doctrine in !-PLUGIN-REGISTRY.md;
that document can explain policy, while these generated blocks keep counts and
plugin lists aligned with Git-tracked config.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
OBSIDIAN_DIR = REPO_ROOT / ".obsidian"
COMMUNITY_CONFIG = OBSIDIAN_DIR / "community-plugins.json"
CORE_CONFIG = OBSIDIAN_DIR / "core-plugins.json"
PLUGIN_DIR = OBSIDIAN_DIR / "plugins"
MANIFEST_PATH = REPO_ROOT / "manifest.json"
SWARM_PATH = REPO_ROOT / "swarm.json"

PLUGIN_REGISTRY_CANDIDATES = (
    "!-PLUGIN-REGISTRY.md",
    "!/PLUGIN-REGISTRY.md",
)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def plugin_registry_path() -> str:
    for candidate in PLUGIN_REGISTRY_CANDIDATES:
        if (REPO_ROOT / candidate).exists():
            return candidate
    return PLUGIN_REGISTRY_CANDIDATES[0]


def read_enabled(path: Path) -> list[str]:
    data = load_json(path, [])
    if isinstance(data, list):
        return [str(item) for item in data]
    if isinstance(data, dict):
        return [str(key) for key, enabled in data.items() if enabled is True]
    raise ValueError(f"{repo_rel(path)} must contain a JSON array or object")


def read_plugin_manifests() -> dict[str, dict[str, Any]]:
    installed: dict[str, dict[str, Any]] = {}
    if not PLUGIN_DIR.exists():
        return installed

    for manifest_path in sorted(PLUGIN_DIR.glob("*/manifest.json")):
        data = load_json(manifest_path, {})
        plugin_id = str(data.get("id") or manifest_path.parent.name)
        installed[plugin_id] = {
            "id": plugin_id,
            "name": str(data.get("name") or plugin_id),
            "version": str(data.get("version") or ""),
            "path": repo_rel(manifest_path),
        }
    return installed


def build_state() -> dict[str, Any]:
    enabled_community = read_enabled(COMMUNITY_CONFIG)
    enabled_core = read_enabled(CORE_CONFIG)
    installed = read_plugin_manifests()

    installed_ids = sorted(installed)
    dormant = [plugin_id for plugin_id in installed_ids if plugin_id not in enabled_community]
    missing_enabled = [plugin_id for plugin_id in enabled_community if plugin_id not in installed]

    return {
        "manifest_doc": plugin_registry_path(),
        "status": "active",
        "source_of_truth": "tracked_obsidian_config",
        "generated_by": ".github/scripts/sync_obsidian_plugin_registry.py",
        "authority_boundary": (
            "Obsidian config files define interface state; the plugin registry "
            "document defines doctrine and promotion rules."
        ),
        "current_state": {
            "enabled_community_count": len(enabled_community),
            "enabled_core_count": len(enabled_core),
            "installed_community_count": len(installed_ids),
            "dormant_installed_count": len(dormant),
            "enabled_missing_manifest_count": len(missing_enabled),
        },
        "entrypoints": [
            {
                "id": "plugin-manifest",
                "path": plugin_registry_path(),
                "role": "plugin doctrine and promotion rules",
            },
            {
                "id": "community-plugins",
                "path": repo_rel(COMMUNITY_CONFIG),
                "role": "enabled community-plugin interface state",
            },
            {
                "id": "core-plugins",
                "path": repo_rel(CORE_CONFIG),
                "role": "enabled core-plugin interface state",
            },
            {
                "id": "plugin-payloads",
                "path": repo_rel(PLUGIN_DIR) + "/",
                "role": "installed community-plugin manifests and payloads",
            },
        ],
        "enabled_community_plugins": enabled_community,
        "enabled_core_plugins": enabled_core,
        "installed_community_plugins": [installed[plugin_id] for plugin_id in installed_ids],
        "dormant_installed_plugins": dormant,
        "enabled_plugins_missing_manifest": missing_enabled,
        "promotion_rule": (
            "Any committed Obsidian plugin config change must be accompanied by "
            "synced manifest.json and swarm.json plugin_layer blocks."
        ),
    }


def update_manifest_plugin_layer(manifest: dict[str, Any], state: dict[str, Any]) -> None:
    prior = manifest.get("plugin_layer", {})
    next_layer = copy.deepcopy(prior) if isinstance(prior, dict) else {}
    next_layer.update(copy.deepcopy(state))
    manifest["plugin_layer"] = next_layer


def update_swarm_plugin_layer(swarm: dict[str, Any], state: dict[str, Any]) -> None:
    prior = swarm.get("plugin_layer", {})
    next_layer = copy.deepcopy(prior) if isinstance(prior, dict) else {}
    next_layer.update(copy.deepcopy(state))

    counts = next_layer.setdefault("counts", {})
    counts["enabled_community"] = state["current_state"]["enabled_community_count"]
    counts["enabled_core"] = state["current_state"]["enabled_core_count"]
    counts["installed_total"] = state["current_state"]["installed_community_count"]
    counts["dormant_installed"] = state["current_state"]["dormant_installed_count"]
    counts["enabled_missing_manifest"] = state["current_state"]["enabled_missing_manifest_count"]

    swarm["plugin_layer"] = next_layer


def synced_documents() -> tuple[dict[str, Any], dict[str, Any]]:
    state = build_state()
    manifest = load_json(MANIFEST_PATH, {})
    swarm = load_json(SWARM_PATH, {})
    update_manifest_plugin_layer(manifest, state)
    update_swarm_plugin_layer(swarm, state)
    return manifest, swarm


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write synced registry state")
    mode.add_argument("--check", action="store_true", help="fail if registry state is out of sync")
    args = parser.parse_args()

    expected_manifest, expected_swarm = synced_documents()
    current_manifest = load_json(MANIFEST_PATH, {})
    current_swarm = load_json(SWARM_PATH, {})

    if args.write:
        if current_manifest != expected_manifest:
            write_json(MANIFEST_PATH, expected_manifest)
            print(f"updated {repo_rel(MANIFEST_PATH)}")
        if current_swarm != expected_swarm:
            write_json(SWARM_PATH, expected_swarm)
            print(f"updated {repo_rel(SWARM_PATH)}")
        return 0

    drifted = []
    if current_manifest != expected_manifest:
        drifted.append(repo_rel(MANIFEST_PATH))
    if current_swarm != expected_swarm:
        drifted.append(repo_rel(SWARM_PATH))

    if drifted:
        print("Obsidian plugin registry drift detected:", file=sys.stderr)
        for path in drifted:
            print(f"  {path}", file=sys.stderr)
        print(
            "Run: python .github/scripts/sync_obsidian_plugin_registry.py --write",
            file=sys.stderr,
        )
        return 1

    print("Obsidian plugin registry is in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
