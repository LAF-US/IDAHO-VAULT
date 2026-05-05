from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


validate_bootstrap = _load_module("validate_bootstrap_test_module", "scripts/validate_bootstrap.py")


class ValidateBootstrapTest(unittest.TestCase):
    def test_validate_bootstrap_reports_missing_repo_entrypoint_import_as_error(self) -> None:
        with patch.object(
            validate_bootstrap.importlib,
            "import_module",
            side_effect=[object(), RuntimeError("broken import")],
        ):
            contract = {"ok": True, "checks": []}
            validations = validate_bootstrap.validate_bootstrap()[1]

        result = [item for item in validations if item.name == "Repo entrypoint import"]
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].ok)
        self.assertEqual(result[0].severity, "error")

    def test_render_markdown_includes_scope_notes(self) -> None:
        contract = {"ok": True, "checks": [{"name": "lockfile", "ok": True, "detail": "present"}]}
        validations = [
            validate_bootstrap.BootstrapValidation(
                name="uv CLI",
                ok=True,
                severity="info",
                detail="available",
            )
        ]

        markdown = validate_bootstrap.render_markdown(contract, validations)

        self.assertIn("checkout-bound and vault-local", markdown)
        self.assertIn("install_dependencies.sh", markdown)

    def test_json_payload_is_serializable(self) -> None:
        contract = {"ok": True, "checks": [{"name": "lockfile", "ok": True, "detail": "present"}]}
        validations = [
            validate_bootstrap.BootstrapValidation(
                name="uv CLI",
                ok=True,
                severity="info",
                detail="available",
            )
        ]
        payload = {
            "contract": contract,
            "validations": [validate_bootstrap.asdict(validations[0])],
        }

        rendered = json.dumps(payload, indent=2)

        self.assertIn('"contract"', rendered)


if __name__ == "__main__":
    unittest.main()
