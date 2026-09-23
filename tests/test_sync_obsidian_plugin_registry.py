from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest import mock


def _load_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "sync_obsidian_plugin_registry.py"
    spec = importlib.util.spec_from_file_location(
        "sync_obsidian_plugin_registry_test_module",
        script_path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


registry = _load_module()


def test_manifest_discovery_uses_git_index_and_excludes_ambient_files(tmp_path: Path) -> None:
    tracked = tmp_path / ".obsidian" / "plugins" / "tracked" / "manifest.json"
    ignored = tmp_path / ".obsidian" / "plugins" / "ignored" / "manifest.json"
    tracked.parent.mkdir(parents=True)
    ignored.parent.mkdir(parents=True)
    tracked.write_text('{"id": "tracked"}', encoding="utf-8")
    ignored.write_text('{"id": "ignored"}', encoding="utf-8")
    result = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=".obsidian/plugins/tracked/manifest.json\0",
        stderr="",
    )

    with mock.patch.object(registry, "REPO_ROOT", tmp_path), mock.patch.object(
        registry.subprocess,
        "run",
        return_value=result,
    ):
        paths = registry.tracked_plugin_manifest_paths()

    assert paths == [tracked]


def test_openclaw_manifest_is_part_of_committed_inventory() -> None:
    manifest_path = (
        Path(__file__).resolve().parents[1]
        / ".obsidian"
        / "plugins"
        / "obsidianclaw"
        / "manifest.json"
    )
    plugins = registry.read_plugin_manifests([manifest_path])

    assert plugins["openclaw"]["version"] == "0.41.1"
    assert plugins["openclaw"]["path"] == ".obsidian/plugins/obsidianclaw/manifest.json"


def test_generated_state_disclaims_runtime_presence() -> None:
    with mock.patch.object(registry, "read_enabled", side_effect=[["openclaw"], []]), mock.patch.object(
        registry,
        "read_plugin_manifests",
        return_value={
            "openclaw": {
                "id": "openclaw",
                "name": "OpenClaw",
                "version": "0.41.1",
                "path": ".obsidian/plugins/obsidianclaw/manifest.json",
            }
        },
    ):
        state = registry.build_state()

    assert state["inventory_scope"] == "git_index"
    assert state["runtime_claim"] == "none"
    assert "device-local runtime presence" in state["authority_boundary"]


def test_precommit_hook_checks_registry_without_rewriting_or_staging() -> None:
    hook = (
        Path(__file__).resolve().parents[1] / ".githooks" / "pre-commit"
    ).read_text(encoding="utf-8")

    assert "sync_obsidian_plugin_registry.py --check" in hook
    assert "sync_obsidian_plugin_registry.py --write" not in hook
    assert "git add manifest.json swarm.json" not in hook
