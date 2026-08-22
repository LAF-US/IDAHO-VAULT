"""Benchmarks for the NETWEB path portability guard.

`check_portable_paths.py` gates changed paths and additionally sweeps the whole
tracked tree for case-insensitive collisions, which in this repository means
tens of thousands of paths on every run.
"""

from __future__ import annotations

import check_portable_paths as cpp


def test_path_violations_over_changeset(benchmark, vault_paths):
    """Per-path portability scan: reserved names, illegal characters, length."""
    findings = benchmark(
        lambda: [finding for path in vault_paths for finding in cpp.path_violations(path)]
    )

    assert any("RESERVED NAME" in finding for finding in findings)


def test_case_collisions_over_tree(benchmark, vault_paths):
    """Whole-tree sweep for paths that differ only by case."""
    collisions = benchmark(lambda: cpp.case_collisions(vault_paths))

    assert collisions


def test_normalize_paths(benchmark, vault_paths):
    """The comparison-key fold that the collision sweep calls once per path."""
    keys = benchmark(lambda: [cpp.normalize(path) for path in vault_paths])

    assert len(keys) == len(vault_paths)
