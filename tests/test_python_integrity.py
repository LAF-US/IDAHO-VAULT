from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_checker():
    script_path = ROOT / ".github" / "scripts" / "check_python_integrity.py"
    spec = importlib.util.spec_from_file_location("check_python_integrity_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def test_rejects_purge_markers_and_syntax_errors(tmp_path: Path) -> None:
    marker = "***" + "REMOVED" + "***"
    path = tmp_path / "broken.py"
    path.write_text(f"{marker}\ndef nope(:\n", encoding="utf-8")

    findings = checker.python_file_findings(path)

    assert any("contains purge marker" in finding for finding in findings)
    assert any("syntax error" in finding for finding in findings)


def test_invalid_utf8_is_flagged_not_silently_replaced(tmp_path: Path) -> None:
    path = tmp_path / "bad_encoding.py"
    # A lone continuation byte (0x80) is never valid UTF-8 on its own.
    path.write_bytes(b"VALUE = 1\n\x80\n")

    findings = checker.python_file_findings(path)

    assert any("not valid UTF-8" in finding for finding in findings)


def test_unreadable_file_is_flagged_not_a_crash(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "unreadable.py"
    path.write_text("VALUE = 1\n", encoding="utf-8")

    def _raise_permission_error(self, encoding=None):
        raise PermissionError("Permission denied")

    monkeypatch.setattr(checker.Path, "read_text", _raise_permission_error)

    findings = checker.python_file_findings(path)

    assert any("could not read file" in finding for finding in findings)


def test_active_subprocess_requires_timeout(tmp_path: Path) -> None:
    path = tmp_path / "runner.py"
    path.write_text(
        "import subprocess\nsubprocess.run(['git', 'status'])\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert any("subprocess call missing timeout" in finding for finding in findings)


def test_interactive_subprocess_can_be_explicitly_exempted(tmp_path: Path) -> None:
    path = tmp_path / "interactive.py"
    path.write_text(
        "import subprocess\n"
        "# timeout: interactive\n"
        "subprocess.run(['agent', 'serve'])\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert findings == []


def test_aliased_subprocess_import_is_flagged(tmp_path: Path) -> None:
    path = tmp_path / "aliased.py"
    path.write_text(
        "import subprocess as sp\nsp.run(['git', 'status'], timeout=30)\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert any("aliased subprocess import" in finding for finding in findings)


def test_from_import_of_gated_callable_is_flagged(tmp_path: Path) -> None:
    path = tmp_path / "from_import.py"
    path.write_text(
        "from subprocess import run\nrun(['git', 'status'], timeout=30)\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert any("'from subprocess import run'" in finding for finding in findings)


def test_wildcard_subprocess_import_is_flagged(tmp_path: Path) -> None:
    path = tmp_path / "wildcard_import.py"
    path.write_text(
        "from subprocess import *\nrun(['git', 'status'], timeout=30)\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert any("'from subprocess import *'" in finding for finding in findings)


def test_from_import_of_non_spawning_names_is_allowed(tmp_path: Path) -> None:
    path = tmp_path / "types_only.py"
    path.write_text(
        "from subprocess import PIPE, CompletedProcess, TimeoutExpired\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert findings == []


def test_obvious_flattened_duplicate_is_reported(tmp_path: Path) -> None:
    canonical = tmp_path / "src" / "pkg" / "module.py"
    canonical.parent.mkdir(parents=True)
    canonical.write_text("VALUE = 1\n", encoding="utf-8")
    flattened = tmp_path / "src-pkg-module.py"
    flattened.write_text("VALUE = 1\n", encoding="utf-8")

    findings = checker.flattened_duplicate_findings(tmp_path, [canonical, flattened])

    assert any(
        path == flattened and "byte-identical flattened duplicate" in message
        for path, message in findings
    )


def _init_git_repo_with_violation(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, timeout=10)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=root,
        check=True,
        capture_output=True,
        timeout=10,
    )
    subprocess.run(
        ["git", "config", "user.name", "Integrity Test"],
        cwd=root,
        check=True,
        capture_output=True,
        timeout=10,
    )
    (root / "clean.py").write_text("import subprocess\nsubprocess.run(['x'], timeout=5)\n", encoding="utf-8")
    (root / "violator.py").write_text("import subprocess\nsubprocess.run(['x'])\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True, timeout=10)


def test_paths_from_stdin_gates_only_changed_files(tmp_path: Path, monkeypatch) -> None:
    """A pre-existing violation outside the changed set must warn, not fail —
    the whole-repo scan this guards against would block every future PR."""
    _init_git_repo_with_violation(tmp_path)

    monkeypatch.setattr(sys, "stdin", io.StringIO("clean.py\n"))
    exit_code = checker.main(["--root", str(tmp_path), "--paths-from-stdin"])
    assert exit_code == 0

    monkeypatch.setattr(sys, "stdin", io.StringIO("violator.py\n"))
    exit_code = checker.main(["--root", str(tmp_path), "--paths-from-stdin"])
    assert exit_code == 1


def test_paths_from_stdin_strips_incidental_whitespace(tmp_path: Path, monkeypatch) -> None:
    """Trailing padding on a stdin line (not removed by splitlines(), which
    only strips line terminators) must not desync it from the exact posix
    path string, or the gate silently stops matching that file."""
    _init_git_repo_with_violation(tmp_path)

    monkeypatch.setattr(sys, "stdin", io.StringIO("violator.py \n"))
    exit_code = checker.main(["--root", str(tmp_path), "--paths-from-stdin"])
    assert exit_code == 1
