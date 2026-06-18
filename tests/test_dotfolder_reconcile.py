from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_reconciler():
    module_path = Path(__file__).resolve().parents[1] / "dotfolder_reconcile.py"
    spec = importlib.util.spec_from_file_location("dotfolder_reconcile_test_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reconciler = load_reconciler()


def test_stub_dry_run_does_not_write_vault_files(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_root.mkdir()
    vault_root.mkdir()

    result = reconciler.reconcile_dot(
        "demo",
        home_root=home_root,
        vault_root=vault_root,
        cache=reconciler.HashCache(tmp_path / "cache.json", disabled=True),
        apply=False,
        snapshot=False,
        prune=False,
        stub=True,
        force=False,
        quiet=True,
    )

    assert result.error is None
    assert not (vault_root / ".demo").exists()


def test_dry_run_does_not_write_hash_cache(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("same", encoding="utf-8")
    (vault_dir / "config.txt").write_text("same", encoding="utf-8")
    cache_path = tmp_path / "cache.json"

    assert reconciler.main(
        [
            "demo",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(cache_path),
            "--quiet",
        ]
    ) == 0

    assert not cache_path.exists()


def test_apply_stub_is_idempotent(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_root.mkdir()
    vault_root.mkdir()

    args = [
        "demo",
        "--home-root",
        str(home_root),
        "--vault-root",
        str(vault_root),
        "--cache-path",
        str(tmp_path / "cache.json"),
        "--stub",
        "--apply",
        "--quiet",
    ]

    assert reconciler.main(args) == 0
    first_stub = (vault_root / ".demo" / "stub.txt").read_text(encoding="utf-8")
    assert reconciler.main(args) == 0

    assert (vault_root / ".demo" / "stub.txt").read_text(encoding="utf-8") == first_stub


def test_snapshot_conflict_keeps_vault_file_in_place(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    (vault_dir / "config.txt").write_text("vault", encoding="utf-8")

    result = reconciler.reconcile_dot(
        "demo",
        home_root=home_root,
        vault_root=vault_root,
        cache=reconciler.HashCache(tmp_path / "cache.json", disabled=True),
        apply=True,
        snapshot=True,
        prune=False,
        stub=False,
        force=False,
        quiet=True,
    )

    assert result.conflicts == 1
    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "config.txt.home").read_text(encoding="utf-8") == "home"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"
