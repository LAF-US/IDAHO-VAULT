from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent


def _load_resolver():
    script_path = PROJECT_ROOT / "!" / "resolve_openrouter_secret.py"
    spec = importlib.util.spec_from_file_location("openrouter_secret_resolver_test_module", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load test module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_op_reference() -> str:
    return "op:" + "//vault/openrouter/credential"


resolver = _load_resolver()


class OpenRouterSecretResolverTest(unittest.TestCase):
    def test_materialize_writes_runtime_aliases_with_private_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            env_file = Path(temporary_directory) / ".op" / "openrouter.env"
            reference = test_op_reference()
            with (
                patch.object(resolver, "ENV_FILE", env_file),
                patch.dict(os.environ, {"OPENROUTER_API_KEY": reference}, clear=True),
            ):
                output_path = resolver.materialize_runtime_env()

            content = output_path.read_text(encoding="utf-8")
            self.assertEqual(output_path, env_file)
            self.assertIn(f"OPENROUTER_API_KEY={reference}", content)
            self.assertIn(f"OPENAI_API_KEY={reference}", content)
            self.assertIn(f"ANTHROPIC_AUTH_TOKEN={reference}", content)
            self.assertIn(f"ANTHROPIC_API_KEY={reference}", content)
            self.assertEqual(stat.S_IMODE(output_path.parent.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(output_path.stat().st_mode), 0o600)

    def test_main_never_prints_validated_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            env_file = Path(temporary_directory) / ".op" / "openrouter.env"
            reference = test_op_reference()
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(resolver, "ENV_FILE", env_file),
                patch.dict(os.environ, {"OPENROUTER_API_KEY": reference}, clear=True),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                result = resolver.main()

            self.assertEqual(result, 0)
            self.assertIn("Materialized OpenRouter runtime environment", stdout.getvalue())
            self.assertNotIn(reference, stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(env_file.read_text(encoding="utf-8").count(reference), 4)

    def test_rejects_invalid_source_without_echoing_it(self) -> None:
        invalid_source = "not-a-valid-reference"
        stderr = io.StringIO()
        with (
            patch.dict(os.environ, {"OPENROUTER_API_KEY": invalid_source}, clear=True),
            contextlib.redirect_stderr(stderr),
        ):
            result = resolver.main()

        self.assertEqual(result, 1)
        self.assertIn("must be a valid 1Password op:// reference", stderr.getvalue())
        self.assertNotIn(invalid_source, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
