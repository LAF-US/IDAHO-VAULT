from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load test module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


openrouter_runtime = _load_module(
    "openrouter_runtime_test_module",
    "scripts/openrouter_runtime.py",
)


class OpenRouterRuntimeTest(unittest.TestCase):
    def test_parse_env_content_ignores_comments_and_blank_lines(self) -> None:
        content = """
        # comment
        OPENAI_API_KEY=op://vault/item/credential

        OPENAI_BASE_URL=https://openrouter.ai/api/v1
        """

        self.assertEqual(
            openrouter_runtime.parse_env_content(content),
            {
                "OPENAI_API_KEY": "op://vault/item/credential",
                "OPENAI_BASE_URL": "https://openrouter.ai/api/v1",
            },
        )

    def test_ensure_env_file_refreshes_when_required_value_is_blank(self) -> None:
        env_file = PROJECT_ROOT / ".tmp" / "test-openrouter.env"
        with (
            patch.object(openrouter_runtime, "ENV_FILE", env_file),
            patch.object(openrouter_runtime.subprocess, "run") as run,
        ):
            env_file.parent.mkdir(parents=True, exist_ok=True)
            env_file.write_text(
                "ANTHROPIC_AUTH_TOKEN=op://vault/item/credential\n"
                "ANTHROPIC_BASE_URL=https://openrouter.ai/api\n"
                "ANTHROPIC_API_KEY=\n",
                encoding="utf-8",
            )

            resolved_env_file = openrouter_runtime.ensure_env_file("claude")

        self.assertEqual(resolved_env_file, env_file)
        run.assert_called_once_with(
            [openrouter_runtime.sys.executable, str(openrouter_runtime.RESOLVER)],
            check=True,
            timeout=60,
        )

    def test_approved_agent_returns_only_fixed_literals(self) -> None:
        self.assertEqual(openrouter_runtime.approved_agent("codex"), "codex")
        self.assertEqual(openrouter_runtime.approved_agent("claude"), "claude")
        with self.assertRaises(SystemExit) as exc:
            openrouter_runtime.approved_agent("untrusted")
        self.assertIn("Unsupported OpenRouter agent", str(exc.exception))

    def test_launcher_rejects_command_arguments_before_preflight(self) -> None:
        with (
            patch.object(openrouter_runtime, "ensure_op_available") as ensure_op_available,
            patch.object(openrouter_runtime, "ensure_op_signed_in") as ensure_op_signed_in,
            patch.object(openrouter_runtime, "ensure_env_file") as ensure_env_file,
        ):
            with self.assertRaises(SystemExit) as exc:
                openrouter_runtime.launch_agent("claude", ["--help"])

        self.assertIn("do not accept command arguments", str(exc.exception))
        ensure_op_available.assert_not_called()
        ensure_op_signed_in.assert_not_called()
        ensure_env_file.assert_not_called()

    def test_codex_launcher_uses_the_fixed_op_run_command(self) -> None:
        env_file = PROJECT_ROOT / ".op" / "openrouter.env"
        runtime_env = {"CODEX_HOME": "/mock/codex"}
        with (
            patch.object(openrouter_runtime, "ensure_op_available"),
            patch.object(openrouter_runtime, "ensure_op_signed_in"),
            patch.object(openrouter_runtime, "ensure_env_file", return_value=env_file),
            patch.object(openrouter_runtime, "apply_runtime_env", return_value=runtime_env),
            patch.object(openrouter_runtime.subprocess, "run") as run,
        ):
            run.return_value.returncode = 0
            result = openrouter_runtime.launch_agent("codex", [])

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            ["op", "run", f"--env-file={env_file}", "--", "codex"],
            env=runtime_env,
            check=False,
        )

    def test_claude_launcher_uses_the_fixed_op_run_command(self) -> None:
        env_file = PROJECT_ROOT / ".op" / "openrouter.env"
        runtime_env = {"APPDATA": "/mock/claude"}
        with (
            patch.object(openrouter_runtime, "ensure_op_available"),
            patch.object(openrouter_runtime, "ensure_op_signed_in"),
            patch.object(openrouter_runtime, "ensure_env_file", return_value=env_file),
            patch.object(openrouter_runtime, "apply_runtime_env", return_value=runtime_env),
            patch.object(openrouter_runtime.subprocess, "run") as run,
        ):
            run.return_value.returncode = 17
            result = openrouter_runtime.launch_agent("claude", [])

        self.assertEqual(result, 17)
        run.assert_called_once_with(
            ["op", "run", f"--env-file={env_file}", "--", "claude"],
            env=runtime_env,
            check=False,
        )

    def test_runtime_does_not_use_direct_execution_functions(self) -> None:
        source = (PROJECT_ROOT / "scripts" / "openrouter_runtime.py").read_text(encoding="utf-8")

        self.assertNotIn("os.exec", source)
        self.assertNotIn("cli_name", source)
        self.assertNotIn("--exec", source)

    def test_windows_launcher_uses_a_fixed_agent_command_map_without_args(self) -> None:
        launcher = (PROJECT_ROOT / "scripts" / "Use-OpenRouterEnv.ps1").read_text(encoding="utf-8")

        self.assertNotIn("[string]$CliName", launcher)
        self.assertNotIn("ValueFromRemainingArguments", launcher)
        self.assertIn('$cliName = switch ($Agent)', launcher)
        self.assertIn('$command = @("op", "run", $envArg, "--", $cliName)', launcher)


if __name__ == "__main__":
    unittest.main()
