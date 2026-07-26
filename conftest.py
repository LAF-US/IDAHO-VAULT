import os
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).parent
TESTS = ROOT / "tests"


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    """Fail before pytest enters tempfile retries against an unwritable cache."""
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
    """Keep pytest from probing every top-level vault chamber during collection."""
    del config
    if collection_path.parent == ROOT and collection_path != TESTS:
        return True
    return None
