from __future__ import annotations

import base64
import importlib.util
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path


def _load_version_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_version_transitions.py"
    spec = importlib.util.spec_from_file_location("version_checker_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


version_checker = _load_version_checker()


class VersionTransitionCheckerTest(unittest.TestCase):
    def test_runtime_python_change_requires_transition_record(self) -> None:
        findings = version_checker.findings_for_patches(
            {".python-version": "@@\n-3.13.8\n+3.13.3\n"},
            actor="codex",
        )
        self.assertEqual(findings, [".python-version"])

    def test_dependency_source_constraint_requires_transition_record(self) -> None:
        findings = version_checker.findings_for_patches(
            {
                "pyproject.toml": (
                    "@@\n"
                    '-    "crewai>=1.9.3",\n'
                    '+    "crewai>=1.14.5",\n'
                )
            },
            actor="codex",
        )
        self.assertEqual(findings, ["pyproject.toml"])

    def test_versioned_registry_field_requires_transition_record(self) -> None:
        findings = version_checker.findings_for_patches(
            {'swarm.json': '@@\n-  "registry_version": "a",\n+  "registry_version": "b",\n'},
            actor="codex",
        )
        self.assertEqual(findings, ["swarm.json"])

    def test_workflow_runtime_version_requires_transition_record(self) -> None:
        findings = version_checker.findings_for_patches(
            {
                ".github/workflows/example.yml": (
                    "@@\n"
                    '-          python-version: "3.11"\n'
                    '+          python-version: "3.13"\n'
                )
            },
            actor="codex",
        )
        self.assertEqual(findings, [".github/workflows/example.yml"])

    def test_record_row_allows_recorded_transition(self) -> None:
        findings = version_checker.findings_for_patches(
            {
                ".python-version": "@@\n-3.13.8\n+3.13.3\n",
                "VERSION-TRANSITIONS.md": (
                    "@@\n"
                    "+| 2026-05-26 | Python runtime | 3.13.8 -> 3.13.3 | "
                    "CI compatibility | verified | Logan |\n"
                ),
            },
            actor="codex",
        )
        self.assertEqual(findings, [])

    def test_authenticated_dependabot_lock_only_update_is_pr_audited_exception(self) -> None:
        findings = version_checker.findings_for_patches(
            {"requirements.txt": "@@\n-click==8.1.8\n+click==8.1.9\n"},
            actor="dependabot[bot]",
        )
        self.assertEqual(findings, [])

    def test_dependabot_source_change_is_not_lock_only_exception(self) -> None:
        findings = version_checker.findings_for_patches(
            {"pyproject.toml": '@@\n-    "click>=8.1",\n+    "click>=8.2",\n'},
            actor="dependabot[bot]",
        )
        self.assertEqual(findings, ["pyproject.toml"])

    def test_manual_lock_edit_requires_transition_record(self) -> None:
        findings = version_checker.findings_for_patches(
            {"requirements.txt": "@@\n-click==8.1.8\n+click==8.1.9\n"},
            actor="github-actions[bot]",
        )
        self.assertEqual(findings, ["requirements.txt"])

    def test_unrelated_document_change_is_not_a_version_transition(self) -> None:
        findings = version_checker.findings_for_patches(
            {"README.md": "@@\n-old explanation\n+new explanation\n"},
            actor="codex",
        )
        self.assertEqual(findings, [])

    def test_git_diff_enumerates_deleted_version_surfaces(self) -> None:
        with unittest.mock.patch.object(
            version_checker,
            "run_git",
            side_effect=[
                subprocess.CompletedProcess([], 0, ".python-version\0", ""),
                subprocess.CompletedProcess([], 0, "@@\n-3.13.3\n", ""),
            ],
        ) as run_git:
            patches = version_checker.diff_patches("a" * 40, "b" * 40)

        self.assertIn(".python-version", patches)
        self.assertIn("--diff-filter=ACMRD", run_git.call_args_list[0].args[0])

    def test_github_api_mode_compares_governed_file_contents(self) -> None:
        def content(text: str) -> dict[str, str]:
            return {
                "encoding": "base64",
                "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
            }

        with unittest.mock.patch.object(
            version_checker,
            "github_api_json",
            side_effect=[
                [{"filename": ".python-version", "status": "modified"}],
                content("3.13.8\n"),
                content("3.13.3\n"),
            ],
        ):
            patches = version_checker.github_pr_patches(
                "LAF-US/IDAHO-VAULT",
                374,
                "a" * 40,
                "b" * 40,
                token="read-only-token",
            )

        findings = version_checker.findings_for_patches(patches, actor="codex")
        self.assertEqual(findings, [".python-version"])

    def test_github_api_mode_preserves_non_lock_changes_for_dependabot_scope(self) -> None:
        def content(text: str) -> dict[str, str]:
            return {
                "encoding": "base64",
                "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
            }

        with unittest.mock.patch.object(
            version_checker,
            "github_api_json",
            side_effect=[
                [
                    {"filename": "requirements.txt", "status": "modified"},
                    {"filename": "README.md", "status": "modified"},
                ],
                content("click==8.1.8\n"),
                content("click==8.1.9\n"),
            ],
        ):
            patches = version_checker.github_pr_patches(
                "LAF-US/IDAHO-VAULT",
                360,
                "a" * 40,
                "b" * 40,
                token="read-only-token",
            )

        findings = version_checker.findings_for_patches(patches, actor="dependabot[bot]")
        self.assertEqual(findings, ["requirements.txt"])


if __name__ == "__main__":
    unittest.main()
