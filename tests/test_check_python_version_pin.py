from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_python_version_pin.py"
    spec = importlib.util.spec_from_file_location("python_version_pin_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


class PythonVersionPinCheckerTest(unittest.TestCase):
    def test_pin_within_range_is_satisfied(self) -> None:
        pinned = checker.parse_version("3.13.3")
        self.assertEqual(checker.unsatisfied_clauses(pinned, ">=3.10,<3.14"), [])

    def test_pin_above_upper_bound_is_unsatisfied(self) -> None:
        pinned = checker.parse_version("3.14.0")
        self.assertEqual(checker.unsatisfied_clauses(pinned, ">=3.10,<3.14"), ["<3.14"])

    def test_pin_below_lower_bound_is_unsatisfied(self) -> None:
        pinned = checker.parse_version("3.9.0")
        self.assertEqual(checker.unsatisfied_clauses(pinned, ">=3.10,<3.14"), [">=3.10"])

    def test_two_component_pin_compares_against_three_component_bound(self) -> None:
        pinned = checker.parse_version("3.10")
        self.assertEqual(checker.unsatisfied_clauses(pinned, ">=3.10.1"), [">=3.10.1"])

    def test_compatible_release_operator(self) -> None:
        # ~=3.10 means >=3.10, ==3.* (the release segment before the last stays fixed).
        self.assertTrue(checker.compare(checker.parse_version("3.10.9"), "~=", checker.parse_version("3.10")))
        self.assertTrue(checker.compare(checker.parse_version("3.11.0"), "~=", checker.parse_version("3.10")))
        self.assertFalse(checker.compare(checker.parse_version("4.0.0"), "~=", checker.parse_version("3.10")))
        self.assertFalse(checker.compare(checker.parse_version("3.9.0"), "~=", checker.parse_version("3.10")))

    def test_unsupported_clause_raises(self) -> None:
        with self.assertRaises(RuntimeError):
            checker.unsatisfied_clauses(checker.parse_version("3.13.3"), "compatible with 3.13")

    def test_missing_requires_python_raises(self) -> None:
        with self.assertRaises(RuntimeError):
            checker.read_requires_python('name = "idaho-vault"\nversion = "0.1.0"\n')

    def test_non_numeric_version_raises(self) -> None:
        with self.assertRaises(ValueError):
            checker.parse_version("3.13.3-rc1")


if __name__ == "__main__":
    unittest.main()
