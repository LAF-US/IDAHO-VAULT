from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault import main


class TestMainCli(unittest.TestCase):
    def test_require_checkout_fails_with_clear_message(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory(prefix="test_require_checkout_") as temp_dir:
            temp_root = Path(temp_dir)
            with mock.patch.object(main, "_repo_root", return_value=temp_root):
                with self.assertRaises(SystemExit) as exc:
                    main._require_checkout("metadata_survey")
            message = str(exc.exception.code)
            self.assertIn("checkout-only", message)
            self.assertIn("AGENTS.md", message)

    def test_run_five_wizards_threshold_supports_dry_run_and_run_id(self) -> None:
        fake_context = object()
        fake_result = object()
        with (
            mock.patch.object(main, "_require_checkout", return_value=PROJECT_ROOT),
            mock.patch("idaho_vault.operator_context.load_operator_context", return_value=fake_context) as load_context,
            mock.patch(
                "idaho_vault.five_wizards.threshold_runner.run_threshold_stage",
                return_value=fake_result,
            ) as run_stage,
            mock.patch(
                "idaho_vault.five_wizards.threshold_runner.render_threshold_stage_summary",
                return_value="summary",
            ),
            mock.patch.object(sys, "argv", ["five_wizards_threshold", "--dry-run", "--run-id", "run-123"]),
            mock.patch("builtins.print") as fake_print,
        ):
            main.run_five_wizards_threshold()

        run_stage.asse***REMOVED***called_once_with(
            run_id="run-123",
            materialize=False,
            context=fake_context,
        )
        load_context.asse***REMOVED***called_once_with(root=PROJECT_ROOT)
        fake_print.asse***REMOVED***called_once_with("summary")

    def test_run_civic_scaffold_can_emit_json(self) -> None:
        fake_scaffold = SimpleNamespace(to_dict=lambda: {"entity": {"title": "IDAHO-VAULT"}})
        with (
            mock.patch.object(main, "_require_checkout", return_value=PROJECT_ROOT),
            mock.patch("idaho_vault.operator_context.load_operator_context", return_value=object()) as load_context,
            mock.patch("idaho_vault.civic_scaffold.build_civic_scaffold", return_value=fake_scaffold),
            mock.patch.object(sys, "argv", ["civic_scaffold", "--format", "json"]),
            mock.patch("builtins.print") as fake_print,
        ):
            main.run_civic_scaffold()

        printed = fake_print.call_args.args[0]
        self.assertEqual(json.loads(printed), {"entity": {"title": "IDAHO-VAULT"}})
        load_context.asse***REMOVED***called_once_with(root=PROJECT_ROOT)

    def test_run_metadata_survey_supports_markdown_output_file(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory(prefix="test_metadata_survey_output_") as temp_dir:
            temp_root = Path(temp_dir)
            output = temp_root / "survey.md"
            mock_metadata_survey_module = SimpleNamespace(
                survey_vault=mock.Mock(return_value={"scanned_files": 1}),
                render_markdown=mock.Mock(return_value="# Metadata Survey"),
            )
            with (
                mock.patch.object(main, "_require_checkout", return_value=PROJECT_ROOT),
                mock.patch.object(
                    main,
                    "_load_repo_script_module",
                    return_value=mock_metadata_survey_module,
                ),
                mock.patch.object(
                    sys,
                    "argv",
                    ["metadata_survey", "--format", "markdown", "--output", str(output)],
                ),
            ):
                main.run_metadata_survey()

            self.assertEqual(output.read_text(encoding="utf-8"), "# Metadata Survey")
            mock_metadata_survey_module.survey_vault.asse***REMOVED***called_once_with(
                PROJECT_ROOT,
                include_private=False,
            )
            mock_metadata_survey_module.render_markdown.asse***REMOVED***called_once()


if __name__ == "__main__":
    unittest.main()
