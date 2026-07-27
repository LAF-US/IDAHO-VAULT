from __future__ import annotations

import importlib.util
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import tempfile
import unittest
from pathlib import Path


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_redaction_damage.py"
    spec = importlib.util.spec_from_file_location("redaction_damage_test_module", script_path)
    assert spec is not None
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
        timeout=30,
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

    def test_carried_damage_on_reencoded_line_is_suppressed(self) -> None:
        # A mechanical rewrite (e.g. the NORMALIZATION encoding sweep) re-adds
        # a line whose damage fragment already exists in the same file's base:
        # carried, not new (Logan's 2026-07-08 "known rt_ garble (tracked)").
        damaged = f"serena.cli:sta{MARKER}mcp_server:301 - Star"
        by_file = {"log.txt": [(1, damaged)]}
        findings = checker.findings_for_added_lines(by_file, lambda path: damaged + "\n")
        self.assertEqual(findings, [])

    def test_new_damage_still_flags_with_base_loader(self) -> None:
        damaged = f"sta{MARKER}time"
        by_file = {"f.py": [(1, damaged)]}
        findings = checker.findings_for_added_lines(by_file, lambda path: "clean base\n")
        self.assertEqual(len(findings), 1)

    def test_propagated_damage_to_other_file_still_flags(self) -> None:
        # The fragment exists in SOME file's base, but not this one's: flag.
        damaged = f"sta{MARKER}mcp_server"
        by_file = {"new-home.md": [(1, damaged)]}
        findings = checker.findings_for_added_lines(
            by_file, lambda path: None if path == "new-home.md" else damaged
        )
        self.assertEqual(len(findings), 1)

    def test_two_markers_on_one_line_produce_one_finding(self) -> None:
        # Same per-line semantics as the pre-refinement guard (which searched
        # once per line): the line is flagged, exactly one Finding results.
        damaged = f"sta{MARKER}time and sta{MARKER}again"
        findings = checker.findings_for_added_lines(
            {"f.py": [(1, damaged)]}, lambda path: "clean base\n"
        )
        self.assertEqual(len(findings), 1)

    def test_carried_first_match_does_not_mask_new_second_match(self) -> None:
        # First fragment is carried from base, second is new: the line flags.
        carried = f"sta{MARKER}mcp_server"
        line = f"{carried} plus sta{MARKER}fresh"
        findings = checker.findings_for_added_lines(
            {"log.txt": [(1, line)]}, lambda path: carried + "\n"
        )
        self.assertEqual(len(findings), 1)

    def test_no_base_loader_keeps_strict_behavior(self) -> None:
        damaged = f"sta{MARKER}time"
        findings = checker.findings_for_added_lines({"f.py": [(1, damaged)]})
        self.assertEqual(len(findings), 1)

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
