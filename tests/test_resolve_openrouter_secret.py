from __future__ import annotations

import importlib.util
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import unittest
from unittest.mock import patch
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    script_path = PROJECT_ROOT / "!-resolve_openrouter_secret.py"
    spec = importlib.util.spec_from_file_location("resolve_openrouter_secret_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver = _load_module()


class RenderOpEnvFileTest(unittest.TestCase):
    def test_all_keys_reference_the_same_1password_item(self) -> None:
        rendered = resolver.render_op_env_file("op://Vault/OpenRouter API Key/credential")
        lines = rendered.split("\r\n")
        self.assertIn("OPENROUTER_API_KEY=op://Vault/OpenRouter API Key/credential", lines)
        self.assertIn("ANTHROPIC_API_KEY=op://Vault/OpenRouter API Key/credential", lines)
        self.assertIn("OPENAI_BASE_URL=https://openrouter.ai/api/v1", lines)


class FindOpReferenceTest(unittest.TestCase):
    def test_returns_first_candidate_that_resolves(self) -> None:
        readable = "op://MyVault/openrouter/credential"
        with patch.object(resolver, "can_read_secret", side_effect=lambda ref: ref == readable):
            found = resolver.find_op_reference("MyVault")
        self.assertEqual(found, readable)

    def test_raises_when_no_candidate_resolves(self) -> None:
        with patch.object(resolver, "can_read_secret", return_value=False):
            with self.assertRaises(SystemExit) as exc:
                resolver.find_op_reference("MyVault")
        self.assertIn("Could not resolve", str(exc.exception))


class OpCliFailClosedTest(unittest.TestCase):
    def test_ensure_op_signed_in_fails_closed_when_op_could_not_run(self) -> None:
        with patch.object(resolver.subprocess, "run", side_effect=OSError("permission denied")):
            with self.assertRaises(SystemExit) as exc:
                resolver.ensure_op_signed_in()
        self.assertIn("could not run", str(exc.exception))

    def test_ensure_op_signed_in_fails_closed_on_timeout(self) -> None:
        with patch.object(
            resolver.subprocess, "run", side_effect=subprocess.TimeoutExpired(cmd="op", timeout=15)
        ):
            with self.assertRaises(SystemExit) as exc:
                resolver.ensure_op_signed_in()
        self.assertIn("timed out", str(exc.exception))

    def test_can_read_secret_fails_closed_when_op_could_not_run(self) -> None:
        with patch.object(resolver.subprocess, "run", side_effect=OSError("no such file")):
            with self.assertRaises(SystemExit) as exc:
                resolver.can_read_secret("op://Vault/OpenRouter API Key/credential")
        self.assertIn("could not run", str(exc.exception))

    def test_can_read_secret_fails_closed_on_timeout(self) -> None:
        with patch.object(
            resolver.subprocess, "run", side_effect=subprocess.TimeoutExpired(cmd="op", timeout=15)
        ):
            with self.assertRaises(SystemExit) as exc:
                resolver.can_read_secret("op://Vault/OpenRouter API Key/credential")
        self.assertIn("timed out", str(exc.exception))


class OutFileLocationTest(unittest.TestCase):
    def test_destination_is_fixed_under_the_vault_root_not_argv_derived(self) -> None:
        # The destination is a literal expression (repo_root / ".op" / "openrouter.env")
        # with no CLI flag feeding it -- confirms the input class CodeQL flagged
        # (an arbitrary --out-file reaching open()/write_text()) no longer exists.
        source = (PROJECT_ROOT / "!-resolve_openrouter_secret.py").read_text(encoding="utf-8")
        self.assertNotIn("--out-file", source)
        self.assertIn('out_file = repo_root / ".op" / "openrouter.env"', source)


if __name__ == "__main__":
    unittest.main()
