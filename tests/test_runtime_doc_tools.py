from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib import error


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


health_monitor = _load_module("health_monitor_test_module", "scripts/health_monitor.py")
validate_openrouter = _load_module("validate_openrouter_test_module", "scripts/validate_openrouter.py")
sys.modules.setdefault("health_monitor", health_monitor)
sys.modules.setdefault("validate_openrouter", validate_openrouter)
validate_services = _load_module("validate_services_test_module", "scripts/validate_services.py")


class RuntimeDocToolsTest(unittest.TestCase):
    def test_health_monitor_treats_http_404_as_reachable(self) -> None:
        service = health_monitor.ServiceSpec(name="Example", url="https://example.com")
        http_error = error.HTTPError(service.url, 404, "Not Found", hdrs=None, fp=None)
        with patch.object(health_monitor.request, "urlopen", side_effect=http_error):
            result = health_monitor.check_service(service)

        self.assertTrue(result.ok)
        self.assertEqual(result.status_code, 404)

    def test_health_monitor_reports_url_errors_as_failures(self) -> None:
        service = health_monitor.ServiceSpec(name="Example", url="https://example.com")
        with patch.object(health_monitor.request, "urlopen", side_effect=error.URLError("dns failed")):
            result = health_monitor.check_service(service)

        self.assertFalse(result.ok)
        self.assertIn("dns failed", result.detail)

    def test_validate_openrouter_flags_missing_required_keys(self) -> None:
        env_values = {"OPENAI_BASE_URL": "https://openrouter.ai/api/v1"}
        with patch.object(validate_openrouter, "parse_env_file", return_value=env_values):
            results = validate_openrouter.validate_openrouter_env()

        missing_key_results = [result for result in results if result.name == "Env key `OPENROUTER_API_KEY`"]
        self.assertEqual(len(missing_key_results), 1)
        self.assertFalse(missing_key_results[0].ok)

    def test_validate_openrouter_warns_on_plaintext_keys(self) -> None:
        env_values = {
            "OPENROUTER_API_KEY": "sk-test",
            "OPENAI_API_KEY": "sk-test",
            "OPENAI_BASE_URL": "https://openrouter.ai/api/v1",
            "ANTHROPIC_AUTH_TOKEN": "sk-test",
            "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
            "ANTHROPIC_API_KEY": "sk-test",
        }
        with patch.object(validate_openrouter, "parse_env_file", return_value=env_values):
            results = validate_openrouter.validate_openrouter_env()

        style_results = [result for result in results if result.name == "Secret style `OPENROUTER_API_KEY`"]
        self.assertEqual(len(style_results), 1)
        self.assertFalse(style_results[0].ok)
        self.assertEqual(style_results[0].severity, "warn")

    def test_validate_services_renders_scope_notes_into_matrix(self) -> None:
        local_results = [validate_services.ServiceValidation(name="Local", ok=True, detail="present")]
        openrouter_results = [
            validate_openrouter.ValidationResult(name="Env", ok=True, severity="info", detail="good"),
        ]

        markdown = validate_services.build_compatibility_markdown(local_results, openrouter_results)

        self.assertIn("1Password SSH agent guidance is separate", markdown)
        self.assertIn("OpenRouter Contract", markdown)

    def test_validate_services_json_is_serializable(self) -> None:
        local_results = [validate_services.ServiceValidation(name="Local", ok=True, detail="present")]
        openrouter_results = [
            validate_openrouter.ValidationResult(name="Env", ok=True, severity="info", detail="good"),
        ]
        payload = {
            "local_results": [local_results[0].__dict__],
            "openrouter_results": [openrouter_results[0].__dict__],
            "health_results": [],
        }

        rendered = json.dumps(payload, indent=2)

        self.assertIn('"local_results"', rendered)


if __name__ == "__main__":
    unittest.main()
