from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def _load_doctrinal_flatten_module():
    project_root = Path(__file__).resolve().parent
    script_path = project_root / "doctrinal_flatten.py"
    spec = importlib.util.spec_from_file_location(
        "doctrinal_flatten_test_module",
        script_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return module


doctrinal_flatten = _load_doctrinal_flatten_module()


class DoctrinalFlattenTest(unittest.TestCase):
    def test_filesystem_key_matches_case_and_canonical_unicode_variants(self) -> None:
        self.assertEqual(
            doctrinal_flatten.filesystem_key("RÉSUMÉ.md"),
            doctrinal_flatten.filesystem_key("re\u0301sume\u0301.MD"),
        )
        self.assertNotEqual(
            doctrinal_flatten.filesystem_key(r"a\b.md"),
            doctrinal_flatten.filesystem_key("a/b.md"),
        )

    def test_root_plan_renames_case_and_unicode_equivalent_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            (repo_root / "RÉSUMÉ.md").write_text("incumbent", encoding="utf-8")
            source_dir = repo_root / "Reports"
            source_dir.mkdir()
            source = source_dir / "re\u0301sume\u0301.MD"
            source.write_text("incoming", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "moved_root_renamed")
        self.assertEqual(plans[0]["collision"], "root_existing")
        self.assertNotEqual(
            doctrinal_flatten.filesystem_key(str(plans[0]["destination"])),
            doctrinal_flatten.filesystem_key("RÉSUMÉ.md"),
        )

    def test_inbox_plan_uses_root_collision_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            (repo_root / "RÉSUMÉ.md").write_text("incumbent", encoding="utf-8")
            source_dir = repo_root / "INBOX"
            source_dir.mkdir()
            source = source_dir / "re\u0301sume\u0301.MD"
            source.write_text("incoming", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "moved_root_renamed")
        self.assertEqual(plans[0]["collision"], "root_existing")
        self.assertNotEqual(
            doctrinal_flatten.filesystem_key(str(plans[0]["destination"])),
            doctrinal_flatten.filesystem_key("RÉSUMÉ.md"),
        )

    def test_root_directory_name_is_an_incoming_file_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            (repo_root / "photo.png").mkdir()
            source_dir = repo_root / "INBOX"
            source_dir.mkdir()
            (source_dir / "photo.png").write_text("incoming", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "moved_root_renamed")
        self.assertEqual(plans[0]["collision"], "root_existing")
        self.assertNotEqual(plans[0]["destination"], "photo.png")

    def test_inbox_nested_file_flattens_to_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            source_dir = repo_root / "INBOX" / "PHONE-LINK"
            source_dir.mkdir(parents=True)
            (source_dir / "photo.png").write_text("incoming", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "moved_root")
        self.assertIsNone(plans[0]["collision"])
        self.assertEqual(plans[0]["destination"], "photo.png")

    def test_underscore_directory_flattens_while_bang_and_dotfolders_remain_protected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            source_dir = repo_root / "_agent"
            source_dir.mkdir()
            (source_dir / "collected.md").write_text("incoming", encoding="utf-8")
            protected_bang = repo_root / "!"
            protected_bang.mkdir()
            (protected_bang / "protected.md").write_text("protected", encoding="utf-8")
            protected_dotfolder = repo_root / ".agent"
            protected_dotfolder.mkdir()
            (protected_dotfolder / "hidden.md").write_text("protected", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual([candidate.relative_source for candidate in candidates], ["_agent/collected.md"])
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "moved_root")
        self.assertEqual(plans[0]["destination"], "collected.md")


if __name__ == "__main__":
    unittest.main()
