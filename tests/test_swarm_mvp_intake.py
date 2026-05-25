from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


swarm_mvp_intake = _load_module("swarm_mvp_intake_test_module", ".github/scripts/swarm_mvp_intake.py")
update_manifest = _load_module("update_manifest_test_module", ".github/scripts/update_manifest.py")


class _Workspace:
    def __init__(self) -> None:
        self.original = Path.cwd()
        self.path = PROJECT_ROOT / ".test-tmp" / uuid.uuid4().hex

    def __enter__(self) -> Path:
        self.path.mkdir(parents=True, exist_ok=False)
        os.chdir(self.path)
        return self.path

    def __exit__(self, *_exc: object) -> None:
        os.chdir(self.original)
        shutil.rmtree(self.path, ignore_errors=True)


class SwarmMvpIntakeTest(unittest.TestCase):
    def test_rejects_unsupported_command(self) -> None:
        with _Workspace():
            with self.assertRaisesRegex(ValueError, "Unsupported command"):
                swarm_mvp_intake.create_intake_artifact(
                    command="process galaxy",
                    payload="payload",
                    run_id="123",
                    run_at="2026-05-22T17:00:00Z",
                    agent_id="github-actions[bot]",
                    manifest="manifest.json",
                    output_root="INBOX/SWARM-MVP",
                )

    def test_writes_safe_incrementing_output_paths(self) -> None:
        with _Workspace():
            first = swarm_mvp_intake.create_intake_artifact(
                command="process document",
                payload="payload",
                run_id="run 123",
                run_at="2026-05-22T17:00:00Z",
                agent_id="github-actions[bot]",
                manifest="manifest.json",
                output_root="INBOX/SWARM-MVP",
            )
            second = swarm_mvp_intake.create_intake_artifact(
                command="process document",
                payload="payload",
                run_id="run 123",
                run_at="2026-05-22T17:00:00Z",
                agent_id="github-actions[bot]",
                manifest="manifest.json",
                output_root="INBOX/SWARM-MVP",
            )

            self.assertEqual(
                first.relative_output_path,
                "INBOX/SWARM-MVP/process-document-run-123-1.md",
            )
            self.assertEqual(
                second.relative_output_path,
                "INBOX/SWARM-MVP/process-document-run-123-2.md",
            )

    def test_restricts_output_root_to_swarm_mvp_inbox(self) -> None:
        with self.assertRaisesRegex(ValueError, "output_root must be"):
            swarm_mvp_intake.validate_output_root("INBOX/OTHER")
        with self.assertRaisesRegex(ValueError, "repo-relative"):
            swarm_mvp_intake.validate_output_root(Path.cwd())
        with self.assertRaisesRegex(ValueError, "must not contain"):
            swarm_mvp_intake.validate_output_root("INBOX/../SWARM-MVP")

    def test_frontmatter_and_body_include_routing_context(self) -> None:
        with _Workspace():
            result = swarm_mvp_intake.create_intake_artifact(
                command="process document",
                payload="Line one\nLine two",
                run_id="456",
                run_at="2026-05-22T17:00:00Z",
                agent_id="github-actions[bot]",
                manifest="manifest.json",
                output_root="INBOX/SWARM-MVP",
                github_issue="355",
                linear_ref="LAF-99",
            )

            content = result.output_path.read_text(encoding="utf-8")
            self.assertIn('status: "staged"', content)
            self.assertIn('authority: "github-actions[bot]"', content)
            self.assertIn('source_command: "process document"', content)
            self.assertIn('github_run_id: "456"', content)
            self.assertIn('github_issue: "355"', content)
            self.assertIn('linear_ref: "LAF-99"', content)
            self.assertIn("    Line one\n    Line two", content)
            self.assertIn("- control_plane: github", content)

    def test_manifest_entry_creation_with_skip_swarm_sync(self) -> None:
        with _Workspace():
            Path("manifest.json").write_text(
                json.dumps({"manifest_version": "1.0.0", "locks": [], "entries": {}}),
                encoding="utf-8",
            )
            Path("swarm.json").write_text('{"template_tracking":"do-not-touch"}\n', encoding="utf-8")
            result = swarm_mvp_intake.create_intake_artifact(
                command="process document",
                payload="payload",
                run_id="789",
                run_at="2026-05-22T17:00:00Z",
                agent_id="github-actions[bot]",
                manifest="manifest.json",
                output_root="INBOX/SWARM-MVP",
            )

            manifest_path = Path("manifest.json")
            manifest = update_manifest.load_manifest(manifest_path)
            update_manifest.normalize_manifest(manifest, Path("."), skip_swarm_sync=True)
            now = datetime(2026, 5, 22, 17, 0, tzinfo=timezone.utc)
            lock = update_manifest.acquire_lock(
                manifest,
                result.relative_output_path,
                "github-actions[bot]",
                now,
                15,
            )
            update_manifest.update_entry(
                manifest,
                result.relative_output_path,
                Path(result.relative_output_path),
                "github-actions[bot]",
                lock["lock_id"],
                now,
            )
            lock["state"] = "released"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            reloaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            entry = reloaded["entries"][result.relative_output_path]
            self.assertEqual(entry["last_writer"], "github-actions[bot]")
            self.assertEqual(entry["version"], 1)
            self.assertEqual(entry["lock_id"], lock["lock_id"])
            self.assertTrue(entry["content_hash"].startswith("sha256:"))
            self.assertEqual(
                Path("swarm.json").read_text(encoding="utf-8"),
                '{"template_tracking":"do-not-touch"}\n',
            )


if __name__ == "__main__":
    unittest.main()
