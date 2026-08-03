from __future__ import annotations

import importlib.util
import unittest
import unittest.mock
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_root_conftest():
    spec = importlib.util.spec_from_file_location("root_conftest", ROOT / "conftest.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load root conftest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PytestCollectionGuardTest(unittest.TestCase):
    def test_ignores_non_test_entries_at_repository_root(self) -> None:
        conftest = load_root_conftest()

        self.assertTrue(
            conftest.pytest_ignore_collect(ROOT / "!", config=None)
        )

    def test_allows_tests_directory_and_its_contents(self) -> None:
        conftest = load_root_conftest()

        self.assertIsNone(
            conftest.pytest_ignore_collect(ROOT / "tests", config=None)
        )
        self.assertIsNone(
            conftest.pytest_ignore_collect(
                ROOT / "tests" / "test_live_startup_contract.py", config=None
            )
        )

    def test_fails_fast_when_cache_parent_is_not_writable(self) -> None:
        conftest = load_root_conftest()
        pluginmanager = unittest.mock.Mock()
        pluginmanager.hasplugin.return_value = True
        config = unittest.mock.Mock()
        config.rootpath = ROOT
        config.getini.return_value = ".pytest_cache"
        config.pluginmanager = pluginmanager

        with unittest.mock.patch.object(
            conftest.Path,
            "mkdir",
            side_effect=PermissionError("read-only test workspace"),
        ):
            with self.assertRaisesRegex(
                pytest.UsageError,
                "Fix the directory permissions or explicitly run pytest with "
                "'-p no:cacheprovider'",
            ):
                conftest.pytest_configure(config)

        pluginmanager.unregister.assert_not_called()

    def test_fails_fast_on_read_only_filesystem_generic_oserror(self) -> None:
        """
        EROFS (read-only filesystem) raises plain OSError, not PermissionError.

        The probe must not let that propagate as an unhandled traceback.
        """
        conftest = load_root_conftest()
        pluginmanager = unittest.mock.Mock()
        pluginmanager.hasplugin.return_value = True
        config = unittest.mock.Mock()
        config.rootpath = ROOT
        config.getini.return_value = ".pytest_cache"
        config.pluginmanager = pluginmanager

        with unittest.mock.patch.object(
            conftest.Path,
            "mkdir",
            side_effect=OSError(30, "Read-only file system"),
        ):
            with self.assertRaisesRegex(
                pytest.UsageError,
                "Fix the directory permissions or explicitly run pytest with "
                "'-p no:cacheprovider'",
            ):
                conftest.pytest_configure(config)

        pluginmanager.unregister.assert_not_called()

    def test_keeps_cache_plugin_when_cache_parent_is_writable(self) -> None:
        conftest = load_root_conftest()
        pluginmanager = unittest.mock.Mock()
        pluginmanager.hasplugin.return_value = True
        config = unittest.mock.Mock()
        config.rootpath = ROOT
        config.getini.return_value = ".pytest_cache"
        config.pluginmanager = pluginmanager

        with (
            unittest.mock.patch.object(conftest.Path, "mkdir") as mkdir,
            unittest.mock.patch.object(conftest.Path, "rmdir") as rmdir,
        ):
            conftest.pytest_configure(config)

        self.assertEqual(mkdir.call_count, 2)
        rmdir.assert_called_once_with()
        pluginmanager.unregister.assert_not_called()

    def test_skips_cache_probe_when_operator_disables_cache_plugin(self) -> None:
        conftest = load_root_conftest()
        pluginmanager = unittest.mock.Mock()
        pluginmanager.hasplugin.return_value = False
        config = unittest.mock.Mock()
        config.pluginmanager = pluginmanager

        with unittest.mock.patch.object(conftest.Path, "mkdir") as mkdir:
            conftest.pytest_configure(config)

        mkdir.assert_not_called()

    def test_pinned_runtime_contains_bounded_windows_tempfile_retries(self) -> None:
        self.assertEqual((ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13.5")


if __name__ == "__main__":
    unittest.main()
