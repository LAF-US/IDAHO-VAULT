from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
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

        parsed = openrouter_runtime.parse_env_content(content)

        self.assertEqual(
            parsed,
            {
                "OPENAI_API_KEY": "op://vault/item/credential",
                "OPENAI_BASE_URL": "https://openrouter.ai/api/v1",
            },
        )

    def test_ensure_env_file_refreshes_when_required_value_is_blank(self) -> None:
        env_file = PROJECT_ROOT / ".tmp" / "test-openrouter.env"
        with (
            patch.object(openrouter_runtime, "ENV_FILE", env_file),
            patch.object(openrouter_runtime.shutil, "which", return_value="op"),
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
        run.assert_called_once_with([openrouter_runtime.sys.executable, str(openrouter_runtime.RESOLVER)], check=True)

    def test_help_requests_bypass_1password_preflight(self) -> None:
        with (
            patch.object(openrouter_runtime, "exec_agent", return_value=0) as exec_agent,
            patch.object(openrouter_runtime, "ensure_op_available") as ensure_op_available,
            patch.object(openrouter_runtime, "ensure_op_signed_in") as ensure_op_signed_in,
            patch.object(openrouter_runtime, "ensure_env_file") as ensure_env_file,
        ):
            status = openrouter_runtime.launch_agent("claude", "claude", ["--help"])

        self.assertEqual(status, 0)
        exec_agent.assert_called_once_with("claude", "claude", ["--help"])
        ensure_op_available.assert_not_called()
        ensure_op_signed_in.assert_not_called()
        ensure_env_file.assert_not_called()

    def test_exec_agent_resolves_full_cli_path(self) -> None:
        with (
            patch.object(openrouter_runtime, "apply_runtime_env", return_value={"PATH": r"C:\mock\bin"}),
            patch.object(openrouter_runtime.shutil, "which", return_value=r"C:\mock\bin\codex.cmd") as which,
            patch.object(openrouter_runtime.subprocess, "run") as run,
        ):
            openrouter_runtime.exec_agent("codex", "codex", ["--help"])

        which.assert_called_once_with("codex", path=r"C:\mock\bin")
        run.assert_called_once_with([r"C:\mock\bin\codex.cmd", "--help"], env={"PATH": r"C:\mock\bin"}, check=False)

    def test_exec_agent_raises_clear_error_when_cli_is_missing(self) -> None:
        with (
            patch.object(openrouter_runtime, "apply_runtime_env", return_value={"PATH": r"C:\mock\bin"}),
            patch.object(openrouter_runtime.shutil, "which", return_value=None),
        ):
            with self.assertRaises(SystemExit) as exc:
                openrouter_runtime.exec_agent("codex", "codex", ["--help"])

        self.assertEqual(str(exc.exception), "Could not find 'codex' on PATH.")


if __name__ == "__main__":
    unittest.main()
