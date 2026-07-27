from __future__ import annotations

import hashlib
import json
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import importlib.util
import sys
from pathlib import Path

import pytest


def load_reconciler():
    module_path = Path(__file__).resolve().parents[1] / "dotfolder_reconcile.py"
    spec = importlib.util.spec_from_file_location("dotfolder_reconcile_test_module", module_path)
    assert spec is not None
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


def test_snapshot_apply_copies_sensitive_unique_home_file(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "auth.json").write_text('{"token":"home"}', encoding="utf-8")

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

    assert (vault_root / ".demo" / "auth.json").read_text(encoding="utf-8") == '{"token":"home"}'
    assert (home_dir / "auth.json").exists()


def test_snapshot_apply_preserves_sensitive_conflict_as_home_copy(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "auth.json").write_text("home", encoding="utf-8")
    (vault_dir / "auth.json").write_text("vault", encoding="utf-8")

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

    assert (vault_dir / "auth.json").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "auth.json.home").read_text(encoding="utf-8") == "home"
    assert (home_dir / "auth.json").exists()


def test_retire_apply_moves_sensitive_unique_home_file_into_vault(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "auth.json").write_text("home", encoding="utf-8")

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

    assert (vault_root / ".demo" / "auth.json").read_text(encoding="utf-8") == "home"
    assert not (home_dir / "auth.json").exists()


def test_retire_apply_deletes_identical_sensitive_home_file(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "auth.json").write_text("same", encoding="utf-8")
    (vault_dir / "auth.json").write_text("same", encoding="utf-8")

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

    assert (vault_dir / "auth.json").read_text(encoding="utf-8") == "same"
    assert not (home_dir / "auth.json").exists()

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



def test_dry_run_snapshot_runs_containment_without_writing_manifest_or_cache(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("same", encoding="utf-8")
    (vault_dir / "config.txt").write_text("same", encoding="utf-8")
    cache_path = tmp_path / "cache.json"
    manifest_path = reconciler.default_containment_manifest_path(vault_root)

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

    assert "DOTFOLDER CONTAINMENT REPORT" in capsys.readouterr().out
    assert not cache_path.exists()
    assert not manifest_path.exists()


def test_snapshot_apply_writes_default_containment_manifest(tmp_path: Path) -> None:
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

    manifest_path = reconciler.default_containment_manifest_path(vault_root)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "generated_at" not in manifest
    paths = {entry["path"] for entry in manifest["entries"]}
    assert ".demo/config.txt" in paths
    assert ".tmp" not in paths
    config_entry = next(entry for entry in manifest["entries"] if entry["path"] == ".demo/config.txt")
    assert config_entry == {
        "path": ".demo/config.txt",
        "dotfolder": ".demo",
        "classification": "publishable",
        "rules": [],
        "size": 4,
    }


def test_snapshot_apply_containment_manifest_is_idempotent(tmp_path: Path) -> None:
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
    manifest_path = reconciler.default_containment_manifest_path(vault_root)
    first_manifest = manifest_path.read_text(encoding="utf-8")
    assert reconciler.main(args) == 0

    assert manifest_path.read_text(encoding="utf-8") == first_manifest


def test_retire_apply_writes_default_containment_manifest_after_cleanup(tmp_path: Path) -> None:
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

    manifest = json.loads(
        reconciler.default_containment_manifest_path(vault_root).read_text(encoding="utf-8")
    )
    assert ".demo/config.txt" in {entry["path"] for entry in manifest["entries"]}
    assert not (home_dir / "config.txt").exists()


def test_no_containment_suppresses_automatic_report_and_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
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
            "--no-containment",
            "--home-root",
            str(home_root),
            "--vault-root",
            str(vault_root),
            "--cache-path",
            str(tmp_path / "cache.json"),
            "--quiet",
        ]
    ) == 0

    assert "DOTFOLDER CONTAINMENT REPORT" not in capsys.readouterr().out
    assert not reconciler.default_containment_manifest_path(vault_root).exists()


def test_snapshot_apply_salvages_secret_and_reports_without_failing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    secret_value = "ghp_" + "a" * 36
    (home_dir / "auth.json").write_text(f"token={secret_value}\n", encoding="utf-8")

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

    assert (vault_root / ".demo" / "auth.json").exists()
    assert "[WARN] containment found 1 secret-classified file(s)" in capsys.readouterr().out
    manifest_text = reconciler.default_containment_manifest_path(vault_root).read_text(
        encoding="utf-8"
    )
    assert secret_value not in manifest_text
    manifest = json.loads(manifest_text)
    assert "generated_at" not in manifest
    assert manifest["summary"]["by_class"]["secret"] == 1
    assert ".demo/auth.json" in {entry["path"] for entry in manifest["entries"]}

def test_non_identical_existing_preservation_target_gets_hash_suffix(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "config.txt").write_text("home", encoding="utf-8")
    (vault_dir / "config.txt").write_text("vault", encoding="utf-8")
    (vault_dir / "config.txt.home").write_text("different", encoding="utf-8")
    suffix = hashlib.sha256(b"home").hexdigest()[:12]

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

    assert (vault_dir / "config.txt").read_text(encoding="utf-8") == "vault"
    assert (vault_dir / "config.txt.home").read_text(encoding="utf-8") == "different"
    assert (vault_dir / f"config.txt.home.{suffix}").read_text(encoding="utf-8") == "home"
    assert (home_dir / "config.txt").read_text(encoding="utf-8") == "home"


def test_unreadable_file_is_reported_without_aborting_dotfolder(tmp_path: Path) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    (home_dir / "lock").write_text("aaaa", encoding="utf-8")
    (vault_dir / "lock").write_text("bbbb", encoding="utf-8")

    class UnreadableCache(reconciler.HashCache):
        def sha256(self, path: Path, key: str) -> str:
            if key == "home/demo/lock":
                raise PermissionError("locked")
            return super().sha256(path, key)

    result = reconciler.reconcile_dot(
        "demo",
        home_root=home_root,
        vault_root=vault_root,
        cache=UnreadableCache(tmp_path / "cache.json", disabled=True),
        apply=False,
        snapshot=True,
        prune=False,
        stub=False,
        force=True,
        quiet=True,
    )

    assert result.error is None
    assert result.unavailable_paths == 1
    assert result.conflicts == 0


def test_scanner_unavailable_file_does_not_abort_dotfolder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_root.mkdir()
    (home_dir / "available.txt").write_text("home", encoding="utf-8")
    locked_path = home_dir / "locked.db"
    locked_path.write_text("locked", encoding="utf-8")
    original_is_file = Path.is_file

    def flaky_is_file(path: Path) -> bool:
        if path == locked_path:
            raise PermissionError("locked")
        return original_is_file(path)

    monkeypatch.setattr(Path, "is_file", flaky_is_file)

    result = reconciler.reconcile_dot(
        "demo",
        home_root=home_root,
        vault_root=vault_root,
        cache=reconciler.HashCache(tmp_path / "cache.json", disabled=True),
        apply=False,
        snapshot=True,
        prune=False,
        stub=False,
        force=True,
        quiet=True,
    )

    assert result.error is None
    assert result.files_home == 1
    assert result.unique_to_home == 1
    assert result.unavailable_paths == 1


def test_retire_delete_unavailable_identical_file_does_not_abort(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home_root = tmp_path / "home"
    vault_root = tmp_path / "vault"
    home_dir = home_root / ".demo"
    vault_dir = vault_root / ".demo"
    home_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    home_file = home_dir / "config.txt"
    home_file.write_text("same", encoding="utf-8")
    (vault_dir / "config.txt").write_text("same", encoding="utf-8")
    original_unlink = Path.unlink

    def flaky_unlink(path: Path, *args: object, **kwargs: object) -> None:
        if path == home_file:
            raise PermissionError("locked")
        original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", flaky_unlink)

    result = reconciler.reconcile_dot(
        "demo",
        home_root=home_root,
        vault_root=vault_root,
        cache=reconciler.HashCache(tmp_path / "cache.json", disabled=True),
        apply=True,
        snapshot=False,
        prune=False,
        stub=False,
        force=True,
        quiet=True,
    )

    assert result.error is None
    assert result.identical == 1
    assert result.unavailable_paths == 1
    assert home_file.exists()

def test_retire_dry_run_prints_explicit_retire_hint(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
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


def test_containment_classifies_secret_path(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    secret_path = vault_root / ".codex" / "auth.json"
    secret_path.parent.mkdir(parents=True)
    secret_path.write_text('{"token":"redacted"}', encoding="utf-8")

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert len(report.entries) == 1
    assert report.entries[0].classification == "secret"
    assert "secret_path" in report.entries[0].rules


def test_containment_include_ignored_scans_gitignored_auth_json(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    vault_root.mkdir()
    (vault_root / ".gitignore").write_text(".codex/\n", encoding="utf-8")
    subprocess.run(
        ["git", "-c", "init.defaultBranch=main", "init", "--quiet"],
        cwd=vault_root,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    secret_path = vault_root / ".codex" / "auth.json"
    secret_path.parent.mkdir(parents=True)
    secret_path.write_text('{"token":"redacted"}', encoding="utf-8")

    excluded_report = reconciler.build_containment_report(vault_root, include_ignored=False)
    included_report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert excluded_report.entries == ()
    assert len(included_report.entries) == 1
    assert included_report.entries[0].classification == "secret"

def test_containment_classifies_runtime_cache(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    runtime_path = vault_root / ".codex" / "sessions" / "session.jsonl"
    runtime_path.parent.mkdir(parents=True)
    runtime_path.write_text("ordinary session text", encoding="utf-8")

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert report.entries[0].classification == "runtime/cache"


def test_containment_runtime_dotfolder_root_is_summarized(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vault_root = tmp_path / "vault"
    runtime_path = vault_root / ".vscode" / "extensions" / "plugin" / "state.txt"
    runtime_path.parent.mkdir(parents=True)
    runtime_path.write_text("token = ghp_" + ("a" * 36), encoding="utf-8")

    def fail_content_scan(path: Path) -> tuple[str, ...]:
        raise AssertionError(f"runtime root should not be content-scanned: {path}")

    monkeypatch.setattr(reconciler, "content_secret_rules", fail_content_scan)

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert len(report.entries) == 1
    assert report.entries[0].path == ".vscode"
    assert report.entries[0].classification == "runtime/cache"

def test_containment_runtime_subtree_is_summarized(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vault_root = tmp_path / "vault"
    runtime_path = vault_root / ".codex" / "plugins" / "plugin" / "state.txt"
    runtime_path.parent.mkdir(parents=True)
    runtime_path.write_text("token = ghp_" + ("a" * 36), encoding="utf-8")

    def fail_content_scan(path: Path) -> tuple[str, ...]:
        raise AssertionError(f"runtime subtree should not be content-scanned: {path}")

    monkeypatch.setattr(reconciler, "content_secret_rules", fail_content_scan)

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert len(report.entries) == 1
    assert report.entries[0].path == ".codex/plugins"
    assert report.entries[0].classification == "runtime/cache"


def test_containment_runtime_root_skips_content_scan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vault_root = tmp_path / "vault"
    runtime_path = vault_root / ".ollama" / "models" / "blobs" / "sha256-deadbeef"
    runtime_path.parent.mkdir(parents=True)
    runtime_path.write_bytes(b"token = ghp_" + (b"a" * 36))

    def fail_content_scan(path: Path) -> tuple[str, ...]:
        raise AssertionError(f"runtime path should not be content-scanned: {path}")

    monkeypatch.setattr(reconciler, "content_secret_rules", fail_content_scan)

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert len(report.entries) == 1
    assert report.entries[0].classification == "runtime/cache"
    assert report.entries[0].rules == ()

def test_containment_classifies_publishable_anchor(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    anchor_path = vault_root / ".codex" / "CODEX.md"
    anchor_path.parent.mkdir(parents=True)
    anchor_path.write_text("# Codex\n", encoding="utf-8")

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert report.entries[0].classification == "publishable"


def test_containment_classifies_private_preserve(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    private_path = vault_root / ".codex" / "config.toml"
    private_path.parent.mkdir(parents=True)
    private_path.write_text("model = 'example'\n", encoding="utf-8")

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert report.entries[0].classification == "private-preserve"


def test_containment_large_private_file_is_not_content_scanned(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    large_path = vault_root / ".config" / "large-state.txt"
    large_path.parent.mkdir(parents=True)
    large_path.write_bytes(b"x" * (reconciler.MAX_CONTENT_SCAN_BYTES + 1))

    report = reconciler.build_containment_report(vault_root, include_ignored=True)

    assert len(report.entries) == 1
    assert report.entries[0].classification == "private-preserve"
    assert report.entries[0].rules == ()

def test_manifest_requires_containment_report(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    vault_root.mkdir()

    with pytest.raises(SystemExit) as excinfo:
        reconciler.main(
            [
                "--manifest",
                str(vault_root / "dotfolder-manifest.json"),
                "--vault-root",
                str(vault_root),
            ]
        )

    assert excinfo.value.code == "--manifest requires --containment-report"


def test_containment_report_cannot_be_combined_with_apply(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    vault_root.mkdir()

    with pytest.raises(SystemExit) as excinfo:
        reconciler.main(
            [
                "--containment-report",
                "--apply",
                "--vault-root",
                str(vault_root),
            ]
        )

    assert (
        excinfo.value.code
        == "--containment-report is non-mutating and cannot be combined with --apply"
    )

def test_containment_report_writes_nothing_without_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    vault_root = tmp_path / "vault"
    anchor_path = vault_root / ".codex" / "CODEX.md"
    anchor_path.parent.mkdir(parents=True)
    anchor_path.write_text("# Codex\n", encoding="utf-8")

    before = sorted(path.relative_to(vault_root).as_posix() for path in vault_root.rglob("*"))

    assert reconciler.main(["--containment-report", "--vault-root", str(vault_root)]) == 0

    after = sorted(path.relative_to(vault_root).as_posix() for path in vault_root.rglob("*"))
    assert before == after
    assert "DOTFOLDER CONTAINMENT REPORT" in capsys.readouterr().out


def test_containment_manifest_is_sanitized(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    secret_value = "ghp_" + "a" * 36
    secret_path = vault_root / ".codex" / "history.jsonl"
    manifest_path = tmp_path / "manifest.json"
    secret_path.parent.mkdir(parents=True)
    secret_path.write_text(f"token={secret_value}\n", encoding="utf-8")

    assert (
        reconciler.main(
            [
                "--containment-report",
                "--include-ignored",
                "--vault-root",
                str(vault_root),
                "--manifest",
                str(manifest_path),
            ]
        )
        == 1
    )

    manifest_text = manifest_path.read_text(encoding="utf-8")
    assert secret_value not in manifest_text
    manifest = json.loads(manifest_text)
    assert "generated_at" not in manifest
    assert manifest["summary"]["by_class"]["secret"] == 1
    assert set(manifest["entries"][0]["rules"]) == {"generic_secret_assignment", "github_token"}


def test_containment_report_exits_nonzero_when_secret_present(tmp_path: Path) -> None:
    vault_root = tmp_path / "vault"
    key_path = vault_root / ".claude" / "id_ed25519"
    key_path.parent.mkdir(parents=True)
    key_path.write_text("not a real key", encoding="utf-8")

    assert reconciler.main(["--containment-report", "--vault-root", str(vault_root)]) == 1
