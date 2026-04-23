from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import unittest
from pathlib import Path
from unittest import mock


def _load_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / "doctrinal_flatten.py"
    spec = importlib.util.spec_from_file_location("doctrinal_flatten_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


doctrinal_flatten = _load_module()


class DoctrinalFlattenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.root = self.project_root / "tests" / "_tmp_doctrinal_flatten_case"
        shutil.rmtree(self.root, ignore_errors=True)
        self.root.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def test_main_reports_absolute_manifest_path_when_manifest_is_outside_repo(self) -> None:
        source_dir = self.root / "Folder A"
        source_dir.mkdir()
        (source_dir / "note.md").write_text("body\n", encoding="utf-8")

        external_manifest = self.root.parent / "_tmp_doctrinal_flatten_manifest.jsonl"
        if external_manifest.exists():
            external_manifest.unlink()

        try:
            with mock.patch.object(
                sys,
                "argv",
                [
                    "doctrinal_flatten.py",
                    "--repo-root",
                    str(self.root),
                    "--manifest",
                    str(external_manifest),
                ],
            ), mock.patch("builtins.print") as mock_print:
                result = doctrinal_flatten.main()

            self.assertEqual(result, 0)
            printed = json.loads(mock_print.call_args.args[0])
            self.assertEqual(printed["manifest"], str(external_manifest))
            self.assertTrue(external_manifest.exists())
            self.assertFalse(source_dir.exists())
            self.assertTrue((self.root / "note.md").exists())
        finally:
            external_manifest.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
