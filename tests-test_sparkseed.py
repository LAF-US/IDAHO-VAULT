from __future__ import annotations

import sys
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault import sparkseed


class TestSparkseed(unittest.TestCase):
    def test_build_secret_env_reads_required_fields(self) -> None:
        responses = {
            ("op", "whoami"): CompletedProcess(["op", "whoami"], 0, stdout="logan\n", stderr=""),
            (
                "op",
                "item",
                "get",
                "OpenClaw Gateway Token",
                "--field",
                "token",
            ): CompletedProcess([], 0, stdout="gateway-token\n", stderr=""),
            (
                "op",
                "item",
                "get",
                "OpenClaw Discord Bot",
                "--field",
                "token",
            ): CompletedProcess([], 0, stdout="discord-token\n", stderr=""),
            (
                "op",
                "item",
                "get",
                "OpenClaw Discord Bot",
                "--field",
                "applicationId",
            ): CompletedProcess([], 0, stdout="discord-app\n", stderr=""),
            (
                "op",
                "item",
                "get",
                "OpenClaw Signal Account",
                "--field",
                "number",
            ): CompletedProcess([], 0, stdout="+12085551212\n", stderr=""),
        }

        def fake_run(command: list[str], **_: object) -> CompletedProcess[str]:
            return responses[tuple(command)]

        with (
            mock.patch("idaho_vault.sparkseed.shutil.which", return_value="present"),
            mock.patch("idaho_vault.sparkseed.subprocess.run", side_effect=fake_run),
        ):
            resolved = sparkseed.build_secret_env()

        self.assertEqual(
            resolved,
            {
                "GATEWAY_TOKEN": "gateway-token",
                "DISCORD_BOT_TOKEN": "discord-token",
                "DISCORD_APP_ID": "discord-app",
                "SIGNAL_NUMBER": "+12085551212",
            },
        )

    def test_run_sparkseed_runs_openclaw_sequence_with_secret_env(self) -> None:
        streamed_calls: list[tuple[list[str], dict[str, str]]] = []

        def fake_run(command: list[str], **kwargs: object) -> CompletedProcess[str]:
            env = kwargs.get("env")
            if env is not None:
                streamed_calls.append((command, dict(env)))
            return CompletedProcess(command, 0, stdout="", stderr="")

        with (
            mock.patch("idaho_vault.sparkseed._require_command"),
            mock.patch(
                "idaho_vault.sparkseed.build_secret_env",
                return_value={
                    "GATEWAY_TOKEN": "gateway-token",
                    "DISCORD_BOT_TOKEN": "discord-token",
                    "DISCORD_APP_ID": "discord-app",
                    "SIGNAL_NUMBER": "+12085551212",
                },
            ),
            mock.patch("idaho_vault.sparkseed.subprocess.run", side_effect=fake_run),
            mock.patch("builtins.print"),
        ):
            sparkseed.run_sparkseed()

        self.assertEqual(
            [command for command, _ in streamed_calls],
            [
                ["openclaw", "gateway", "start"],
                ["openclaw", "secrets", "reload"],
                ["openclaw", "secrets", "audit"],
            ],
        )
        for _, env in streamed_calls:
            self.assertEqual(env["GATEWAY_TOKEN"], "gateway-token")
            self.assertEqual(env["DISCORD_BOT_TOKEN"], "discord-token")
            self.assertEqual(env["DISCORD_APP_ID"], "discord-app")
            self.assertEqual(env["SIGNAL_NUMBER"], "+12085551212")
