from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_redaction_damage.py"
    spec = importlib.util.spec_from_file_location("redaction_damage_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()

MARKER = "*" * 3 + "REMOVED" + "*" * 3


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )


def _init_repo(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")


class RedactionDamageCheckerTest(unittest.TestCase):
    def test_touching_marker_in_added_line_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_repo(repo)
            (repo / "f.py").write_text("line1\nline2\n", encoding="utf-8")
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "base")
            base = _git(repo, "rev-parse", "HEAD").stdout.strip()

            (repo / "f.py").write_text(
                f"line1\nline2\nsta{MARKER}time = 1\n", encoding="utf-8"
            )
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "head")
            head = _git(repo, "rev-parse", "HEAD").stdout.strip()

            by_file = checker.added_lines_by_file_at(repo, base, head)
            findings = checker.findings_for_added_lines(by_file)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].path, "f.py")
            self.assertEqual(findings[0].line, 3)

    def test_standalone_marker_is_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_repo(repo)
            (repo / "f.py").write_text("line1\n", encoding="utf-8")
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "base")
            base = _git(repo, "rev-parse", "HEAD").stdout.strip()

            (repo / "f.py").write_text(
                f"line1\nGenuine notice: [{MARKER}] applied here.\n", encoding="utf-8"
            )
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "head")
            head = _git(repo, "rev-parse", "HEAD").stdout.strip()

            by_file = checker.added_lines_by_file_at(repo, base, head)
            findings = checker.findings_for_added_lines(by_file)
            self.assertEqual(findings, [])

    def test_preexisting_damage_untouched_by_diff_is_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_repo(repo)
            (repo / "f.py").write_text(
                f"line1\nsta{MARKER}time = 1\nline3\n", encoding="utf-8"
            )
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "base with pre-existing damage")
            base = _git(repo, "rev-parse", "HEAD").stdout.strip()

            (repo / "f.py").write_text(
                f"line1\nsta{MARKER}time = 1\nline3\nline4 unrelated\n", encoding="utf-8"
            )
            _git(repo, "add", "f.py")
            _git(repo, "commit", "-q", "-m", "unrelated addition")
            head = _git(repo, "rev-parse", "HEAD").stdout.strip()

            by_file = checker.added_lines_by_file_at(repo, base, head)
            findings = checker.findings_for_added_lines(by_file)
            self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
