from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def load_reconciler():
    module_path = Path(__file__).resolve().parents[1] / "dotfolder_reconcile.py"
    spec = importlib.util.spec_from_file_location("dotfolder_reconcile_test_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reconciler = load_reconciler()


def test_plain_apply_requires_explicit_mode(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_root.mkdir()
    vault_root.mkdir()

    with pytest.raises(SystemExit, match="--snapshot or --retire"):
        reconciler.main(
            [
                "demo",
                "--home-root",
                str(home_root),
                "--vault-root",
                str(vault_root),
                "--cache-path",
                str(tmp_path / "cache.json"),
                "--apply",
                "--quiet",
            ]
        )


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
        snapshot=True,
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
            "--snapshot",
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


def test_snapshot_apply_copies_unique_home_files_without_removing_home(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "config.txt").write_text("home", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--snapshot",
            "--apply",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert (vault_root / ".demo" / "config.txt").read_text(encoding="utf-8") == "home"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"


def test_snapshot_apply_preserves_conflicts_without_overwriting(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    (vault_dir / "config.txt").write_text("vault", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--snapshot",
            "--apply",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "config.txt.home").read_text(encoding="utf-8") == "home"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"


def test_retire_apply_moves_unique_home_files_into_vault(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "config.txt").write_text("home", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--retire",
            "--apply",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert (vault_root / ".demo" / "config.txt").read_text(encoding="utf-8") == "home"
    assert not (home_dir / "config.txt").exists()


def test_retire_apply_deletes_identical_home_files(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("same", encoding="utf-8")
    (vault_dir / "config.txt").write_text("same", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--retire",
            "--apply",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "same"
    assert not (home_dir / "config.txt").exists()


def test_snapshot_apply_is_idempotent(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    args = [
        "demo",
        "--snapshot",
        "--apply",
        "--home-root",
        str(home_root),
        "--vault-root",
        str(vault_root),
        "--cache-path",
        str(tmp_path / "cache.json"),
        "--quiet",
    ]

    assert reconciler.main(args) == 0
    assert reconciler.main(args) == 0

    assert (vault_root / ".demo" / "config.txt").read_text(encoding="utf-8") == "home"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"


def test_retire_conflict_is_idempotent(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    (vault_dir / "config.txt").write_text("vault", encoding="utf-8")
    args = [
        "demo",
        "--retire",
        "--apply",
        "--home-root",
        str(home_root),
        "--vault-root",
        str(vault_root),
        "--cache-path",
        str(tmp_path / "cache.json"),
        "--quiet",
    ]

    assert reconciler.main(args) == 0
    assert reconciler.main(args) == 0

    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "config.txt.home").read_text(encoding="utf-8") == "home"
    assert not (home_dir / "config.txt").exists()


def test_non_identical_existing_preservation_target_is_refused(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    (vault_dir / "config.txt").write_text("vault", encoding="utf-8")
    (vault_dir / "config.txt.home").write_text("different", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--snapshot",
            "--apply",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 1

    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "config.txt.home").read_text(encoding="utf-8") == "different"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"

def test_retire_dry_run_prints_explicit_retire_hint(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "config.txt").write_text("home", encoding="utf-8")

    assert reconciler.main(
        [
            "demo",
            "--retire",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert "--retire --apply" in capsys.readouterr().out


def test_reference_denied_page_id_routing_test_path() -> None:
    assert reconciler.is_secret_path("src/page_id_routing_test.ts")
