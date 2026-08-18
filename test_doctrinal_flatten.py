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

    def test_inbox_plan_renames_case_and_unicode_equivalent_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            destination_dir = repo_root / "!" / "INBOX"
            destination_dir.mkdir(parents=True)
            (destination_dir / "RÉSUMÉ.md").write_text("incumbent", encoding="utf-8")
            source_dir = repo_root / "INBOX"
            source_dir.mkdir()
            source = source_dir / "re\u0301sume\u0301.MD"
            source.write_text("incoming", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "rehomed_inbox_renamed")
        self.assertEqual(plans[0]["collision"], "inbox_existing")
        self.assertNotEqual(
            doctrinal_flatten.filesystem_key(str(plans[0]["destination"])),
            doctrinal_flatten.filesystem_key("!/INBOX/RÉSUMÉ.md"),
        )

    def test_inbox_plan_distinguishes_backslash_name_from_nested_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            destination_dir = repo_root / "!" / "INBOX"
            destination_dir.mkdir(parents=True)
            (destination_dir / r"a\b.md").write_text("literal backslash", encoding="utf-8")
            source_dir = repo_root / "INBOX" / "a"
            source_dir.mkdir(parents=True)
            (source_dir / "b.md").write_text("nested path", encoding="utf-8")

            candidates, _ = doctrinal_flatten.collect_candidates(repo_root)
            plans = doctrinal_flatten.plan_moves(repo_root, candidates)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["action"], "rehomed_inbox")
        self.assertIsNone(plans[0]["collision"])
        self.assertEqual(plans[0]["destination"], "!/INBOX/a/b.md")


if __name__ == "__main__":
    unittest.main()
