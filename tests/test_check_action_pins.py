from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_action_pins.py"
    spec = importlib.util.spec_from_file_location("action_pins_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def _write(tmp: Path, text: str) -> Path:
    path = tmp / "workflow.yml"
    path.write_text(text, encoding="utf-8")
    return path


class ActionPinCheckerTest(unittest.TestCase):
    def test_full_sha_pin_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: actions/checkout@" + "a" * 40 + " # v7.0.0\n")
            self.assertEqual(checker.unpinned_refs(path), [])

    def test_floating_tag_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: actions/checkout@v4\n")
            findings = checker.unpinned_refs(path)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0][1], "actions/checkout@v4")

    def test_missing_ref_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: actions/checkout\n")
            self.assertEqual(len(checker.unpinned_refs(path)), 1)

    def test_local_composite_action_is_exempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: ./.github/actions/setup-vault\n")
            self.assertEqual(checker.unpinned_refs(path), [])

    def test_docker_action_is_exempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: docker://alpine:3.19\n")
            self.assertEqual(checker.unpinned_refs(path), [])

    def test_short_sha_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), "      - uses: actions/checkout@9c091bb\n")
            self.assertEqual(len(checker.unpinned_refs(path)), 1)


if __name__ == "__main__":
    unittest.main()
