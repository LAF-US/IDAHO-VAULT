from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "codex_work_guard.py"
SPEC = importlib.util.spec_from_file_location("codex_work_guard", MODULE_PATH)
assert SPEC is not None
codex_work_guard = importlib.util.module_from_spec(SPEC)
sys.modules["codex_work_guard"] = codex_work_guard
assert SPEC.loader is not None
SPEC.loader.exec_module(codex_work_guard)


def test_forbidden_work_root_matches_temp_descendant(tmp_path: Path) -> None:
    forbidden = tmp_path / "tmp"
    checkout = forbidden / "IDAHO-VAULT-work"
    checkout.mkdir(parents=True)

    assert codex_work_guard.is_forbidden_work_root(checkout, [forbidden])


def test_forbidden_work_root_matches_forbidden_dir_name_tmp_path_segment(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "work" / "tmp" / "IDAHO-VAULT"
    unrelated_forbidden = tmp_path / "elsewhere"
    checkout.mkdir(parents=True)

    assert codex_work_guard.is_forbidden_work_root(checkout, [unrelated_forbidden])


def test_forbidden_work_root_allows_repo_surface(tmp_path: Path) -> None:
    forbidden = tmp_path / "tmp"
    vault = Path("/") / "vaults" / "IDAHO-VAULT"

    assert not codex_work_guard.is_forbidden_work_root(vault, [forbidden])


def test_audit_forbidden_roots_finds_codex_residue(tmp_path: Path) -> None:
    residue = tmp_path / "dotfolder-reconcile-smoke-deadbeef"
    residue.mkdir()

    findings = codex_work_guard.audit_forbidden_roots([tmp_path])

    assert len(findings) == 1
    assert findings[0].code == "forbidden_residue"
    assert findings[0].path == str(residue)


def test_audit_forbidden_roots_finds_codex_residue_by_marker_name(tmp_path: Path) -> None:
    residue = tmp_path / "IDAHO-VAULT-scratch"
    residue.mkdir()

    findings = codex_work_guard.audit_forbidden_roots([tmp_path])

    assert len(findings) == 1
    assert findings[0].code == "forbidden_residue"
    assert findings[0].path == str(residue)


def test_audit_forbidden_roots_finds_codex_residue_by_git_dir(tmp_path: Path) -> None:
    repo = tmp_path / "worktree"
    (repo / ".git").mkdir(parents=True)

    findings = codex_work_guard.audit_forbidden_roots([tmp_path])

    assert len(findings) == 1
    assert findings[0].code == "forbidden_residue"
    assert findings[0].path == str(repo)


def test_audit_forbidden_roots_ignores_unrelated_dirs(tmp_path: Path) -> None:
    unrelated = tmp_path / "ordinary-folder"
    unrelated.mkdir()

    assert codex_work_guard.audit_forbidden_roots([tmp_path]) == []


def test_main_no_findings_exits_zero(monkeypatch, capsys) -> None:
    monkeypatch.setattr(codex_work_guard, "default_forbidden_roots", lambda: [])
    monkeypatch.setattr(codex_work_guard, "audit_current_root", lambda cwd, forbidden_roots: [])

    exit_code = codex_work_guard.main([])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "codex-work guard: OK"
    assert captured.err == ""


def test_main_with_findings_exits_nonzero_and_writes_stderr(monkeypatch, capsys) -> None:
    finding = codex_work_guard.Finding(
        severity="error",
        code="forbidden_checkout_root",
        path="/tmp/IDAHO-VAULT",
        message="bad root",
    )
    monkeypatch.setattr(codex_work_guard, "default_forbidden_roots", lambda: [])
    monkeypatch.setattr(codex_work_guard, "audit_current_root", lambda cwd, forbidden_roots: [finding])

    exit_code = codex_work_guard.main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "forbidden_checkout_root" in captured.err
    assert "/tmp/IDAHO-VAULT" in captured.err


def test_main_json_output_structure_with_finding(monkeypatch, capsys) -> None:
    finding = codex_work_guard.Finding(
        severity="error",
        code="forbidden_checkout_root",
        path="/tmp/IDAHO-VAULT",
        message="bad root",
    )
    monkeypatch.setattr(codex_work_guard, "default_forbidden_roots", lambda: [])
    monkeypatch.setattr(codex_work_guard, "audit_current_root", lambda cwd, forbidden_roots: [finding])

    exit_code = codex_work_guard.main(["--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert exit_code == 1
    assert data == {"findings": [codex_work_guard.finding_to_dict(finding)]}
    assert captured.err == ""
