from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


phone_link_intake = _load_module(
    "phone_link_intake_test_module",
    ".github/scripts/phone_link_intake.py",
)


class PhoneLinkIntakeTest(unittest.TestCase):
    def test_main_skips_identical_duplicate_at_vault_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phone_link_source_") as source_dir, tempfile.TemporaryDirectory(
            prefix="phone_link_vault_"
        ) as vault_dir:
            source = Path(source_dir)
            vault_root = Path(vault_dir)
            existing = vault_root / "IMG_1234.jpg"
            existing.write_bytes(b"same-photo")
            incoming = source / "IMG_1234.jpg"
            incoming.write_bytes(b"same-photo")

            with mock.patch.object(phone_link_intake, "get_vault_root", return_value=vault_root):
                status = phone_link_intake.main(["--source", str(source)])

            self.assertEqual(status, 0)
            self.assertEqual(existing.read_bytes(), b"same-photo")
            self.assertFalse(any(vault_root.glob("IMG_1234-*.jpg")))
            self.assertTrue(incoming.exists())

    def test_main_moves_files_directly_to_vault_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phone_link_source_") as source_dir, tempfile.TemporaryDirectory(
            prefix="phone_link_vault_"
        ) as vault_dir:
            source = Path(source_dir)
            vault_root = Path(vault_dir)
            incoming = source / "IMG_1234.jpg"
            incoming.write_bytes(b"photo-bytes")

            with mock.patch.object(phone_link_intake, "get_vault_root", return_value=vault_root):
                status = phone_link_intake.main(["--source", str(source)])

            self.assertEqual(status, 0)
            self.assertFalse(incoming.exists())
            self.assertEqual((vault_root / "IMG_1234.jpg").read_bytes(), b"photo-bytes")
            self.assertFalse((vault_root / "INBOX").exists())

    def test_main_appends_suffix_on_name_collision(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phone_link_source_") as source_dir, tempfile.TemporaryDirectory(
            prefix="phone_link_vault_"
        ) as vault_dir:
            source = Path(source_dir)
            vault_root = Path(vault_dir)
            (vault_root / "IMG_1234.jpg").write_bytes(b"existing-photo")
            incoming = source / "IMG_1234.jpg"
            incoming.write_bytes(b"new-photo")

            with mock.patch.object(phone_link_intake, "get_vault_root", return_value=vault_root):
                status = phone_link_intake.main(["--source", str(source)])

            self.assertEqual(status, 0)
            self.assertEqual((vault_root / "IMG_1234.jpg").read_bytes(), b"existing-photo")
            collisions = sorted(vault_root.glob("IMG_1234-*.jpg"))
            self.assertEqual(len(collisions), 1)
            self.assertEqual(collisions[0].read_bytes(), b"new-photo")

    def test_git_add_stages_only_ingested_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phone_link_source_") as source_dir, tempfile.TemporaryDirectory(
            prefix="phone_link_vault_"
        ) as vault_dir:
            source = Path(source_dir)
            vault_root = Path(vault_dir)
            incoming = source / "voice-note.m4a"
            incoming.write_bytes(b"audio-bytes")

            with (
                mock.patch.object(phone_link_intake, "get_vault_root", return_value=vault_root),
                mock.patch.object(
                    phone_link_intake.subprocess,
                    "run",
                    return_value=mock.Mock(returncode=0, stderr=""),
                ) as mock_run,
            ):
                status = phone_link_intake.main(["--source", str(source), "--git-add"])

            self.assertEqual(status, 0)
            mock_run.assert_called_once_with(
                ["git", "add", str(vault_root / "voice-note.m4a")],
                cwd=str(vault_root),
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
