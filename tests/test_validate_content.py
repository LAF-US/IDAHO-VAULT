from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_validate_content_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "validate_content.py"
    spec = importlib.util.spec_from_file_location("validate_content_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_content = _load_validate_content_module()


class ValidateContentTest(unittest.TestCase):
    def test_admin_scope_requires_governed_frontmatter(self) -> None:
        target = Path("!/wayback-audit-2026-04-22.md")
        errors = validate_content.validate_governed_metadata(target, None, "admin")
        self.assertEqual(errors, [f"{target}: Governed note missing YAML frontmatter"])

    def test_admin_scope_requires_baseline_fields(self) -> None:
        target = Path("!/TOPOLOGY-CENSUS-root-20260422-000000.md")
        errors = validate_content.validate_governed_metadata(
            target,
            {"title": "Topology Census — root", "status": "draft"},
            "admin",
        )
        self.assertEqual(
            errors,
            [f"{target}: Governed note missing required frontmatter field(s): updated, authority"],
        )

    def test_admin_scope_accepts_baseline_fields(self) -> None:
        target = Path("!/wayback-audit-2026-04-22.md")
        errors = validate_content.validate_governed_metadata(
            target,
            {
                "title": "Wayback Audit — 2026-04-22",
                "updated": "2026-04-22",
                "status": "draft",
                "authority": "github-actions",
            },
            "admin",
        )
        self.assertEqual(errors, [])

    def test_bills_scope_does_not_enforce_governed_baseline(self) -> None:
        errors = validate_content.validate_governed_metadata(
            Path("GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/example.md"),
            None,
            "bills",
        )
        self.assertEqual(errors, [])

    def test_inbox_scope_accepts_inbox_markdown(self) -> None:
        errors = validate_content.validate_directory(
            Path("INBOX/SWARM-MVP/process-document-123-1.md"),
            "inbox",
        )
        self.assertEqual(errors, [])

    def test_inbox_scope_rejects_non_inbox_markdown(self) -> None:
        target = Path("!/SWARM-MVP/process-document-123-1.md")
        errors = validate_content.validate_directory(target, "inbox")
        self.assertEqual(
            errors,
            [f"{target}: File outside allowed directories for scope 'inbox': ['INBOX/']"],
        )

    def test_deletion_of_live_governance_requires_human_review(self) -> None:
        target = Path("!/WAKEUP.md")
        errors = validate_content.validate_deleted_path(target, "all")
        self.assertEqual(
            errors,
            [f"{target}: Deletion of governed content requires explicit human review"],
        )

    def test_non_governed_deletion_is_not_blocked(self) -> None:
        self.assertEqual(validate_content.validate_deleted_path(Path("draft.md"), "all"), [])

    def test_run_git_fails_closed_when_git_missing(self) -> None:
        with patch.object(
            validate_content.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(RuntimeError) as exc:
                validate_content._run_git(["git", "diff"])

        self.assertIn("could not run", str(exc.exception))

    def test_has_parent_commit_fails_closed_when_git_missing(self) -> None:
        with patch.object(
            validate_content.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(RuntimeError) as exc:
                validate_content._has_parent_commit()

        self.assertIn("could not run", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
