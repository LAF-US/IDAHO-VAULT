"""Benchmarks for the two-axis risk classifier.

`classify_paths.py` runs on every pull request in `agent-auto-pr.yml` and
`review_feedback_loop.py`, once per changed file, so its per-path cost is
multiplied by the size of the changeset.
"""

from __future__ import annotations

import contextlib
import io
from unittest.mock import patch

import classify_paths as cp


def test_classify_file_over_changeset(benchmark, vault_paths):
    """Score both axes for every path in a large changeset."""
    scored = benchmark(lambda: [cp.classify_file(path) for path in vault_paths])

    assert len(scored) == len(vault_paths)


def test_riskiest_aggregation(benchmark, vault_paths):
    """Fold one axis down to the riskiest reach across the changeset."""
    filetypes = [cp.classify_file(path)[0] for path in vault_paths]

    result = benchmark(lambda: cp.riskiest(*filetypes))

    assert result in cp.TIER_PRECEDENCE


def test_classify_paths_cli(benchmark, vault_paths):
    """End-to-end entry point: read paths from stdin, emit the JSON verdict."""
    payload = "\n".join(vault_paths) + "\n"
    def run() -> None:
        with patch("sys.stdin", io.StringIO(payload)):
            with contextlib.redirect_stdout(io.StringIO()):
                cp.main()

    benchmark(run)
