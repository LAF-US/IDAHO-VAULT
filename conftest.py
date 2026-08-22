import os
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "tests"


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Fail loudly, with an actionable message, if the cache directory is unwritable.

    pytest's own cacheprovider handles this silently: Cache.set()/mkdir() catch
    OSError and only emit a PytestCacheWarning, so a broken cache directory is
    easy to miss in CI output instead of loudly breaking --lf/--ff and the
    cache fixture. (There's no tempfile *retry* loop on this path -- that
    10-attempt retry mechanism belongs to a different, unrelated directory:
    the tmp_path/tmpdir fixture's system-temp base dir in _pytest/tmpdir.py.)
    """
    if not config.pluginmanager.hasplugin("cacheprovider"):
        return

    cache_dir = Path(config.getini("cache_dir"))
    if not cache_dir.is_absolute():
        cache_dir = config.rootpath / cache_dir
    probe = cache_dir.parent / f".pytest-cache-write-probe-{os.getpid()}-{time.monotonic_ns()}"

    try:
        cache_dir.parent.mkdir(parents=True, exist_ok=True)
        probe.mkdir()
        probe.rmdir()
    except OSError as exc:
        raise pytest.UsageError(
            f"pytest cache parent is not writable: {cache_dir.parent}. "
            "Fix the directory permissions or explicitly run pytest with "
            "'-p no:cacheprovider'."
        ) from exc


@pytest.hookimpl(tryfirst=True)
def pytest_ignore_collect(
    collection_path: Path, config: pytest.Config
) -> bool | None:
    """Keep pytest from probing every top-level vault chamber during collection.

    Root holds two different kinds of top-level entries: vault content chambers
    (not test-bearing) and the vault's actual test modules, which live directly
    at root rather than under ``tests/`` (which is empty -- that convention, not
    this file, is canonical). Test modules at root use either ``test_*.py``
    (e.g. ``test_doctrinal_flatten.py``) or the ten ``tests-test_*.py`` files.
    Excluding everything at root except the empty `tests/` dir silently dropped
    all of them from collection.
    """
    del config
    if collection_path.parent != ROOT:
        return None
    if collection_path == TESTS:
        return None
    if collection_path.suffix == ".py" and collection_path.name.startswith(
        ("test_", "tests-test_")
    ):
        return None
    return True
