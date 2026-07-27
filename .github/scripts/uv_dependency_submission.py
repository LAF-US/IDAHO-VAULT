#!/usr/bin/env python3
"""Build a GitHub Dependency-Submission snapshot from uv.lock.

WHY THIS EXISTS
---------------
This project is resolved by **uv**, which writes a *universal* lock (`uv.lock`,
exported to `requirements.txt`) carrying Python-version-forked pins — the same
package can appear at two versions, e.g. `numpy==2.2.6 ; python<3.11` AND
`numpy==2.4.6 ; python>=3.11` (same for `onnxruntime`, `sympy`, …).

GitHub's built-in **Automatic Dependency Submission (Python)** re-resolves the
project from scratch with its `component-detection` engine (pip's resolver
underneath). That resolver cannot represent uv's forked universal pins, so it
dies with `pip ... DistributionNotFound: ResolutionImpossible` on every run —
the constantly-red `submit-pypi` / "Automatic Dependency Submission (Python)"
check. (Parked in review_feedback_loop.KNOWN_NOISE_CHECKS.)

This script reads the already-resolved `uv.lock` and emits a snapshot for
GitHub's Dependency Submission API directly — no re-resolution, so it succeeds.
The companion workflow (`.github/workflows/dependency-submission-uv.yml`)
submits the JSON via `gh api`. Replace the built-in feature by setting
Settings -> Code security -> "Automatic dependency submission" to **Disabled**.

DESIGN
------
- stdlib only (`tomllib` needs Python >= 3.11; the workflow pins setup-python 3.12).
- `build_snapshot(...)` is pure and offline (no network), so it is unit-tested
  against the real lockfile in tests/test_uv_dependency_submission.py.
- The `resolved` map is keyed by **purl** (`pkg:pypi/<name>@<version>`), NOT by
  name, so packages locked at multiple versions (numpy, onnxruntime) are both
  kept rather than colliding.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from datetime import datetime, timezone

_NAME_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_PEP503 = re.compile(r"[-_.]+")


def normalize(name: str) -> str:
    """PEP 503 normalization: lowercase, runs of -_. collapse to a single -."""
    return _PEP503.sub("-", name).lower()


def _declared_names(pyproject: dict, table: str) -> set[str]:
    """Normalized leading names from a PEP 621 requirement list.

    `table` is the literal string ``"project.dependencies"`` (PEP 621 runtime
    deps) or the name of a group under ``[dependency-groups]`` (e.g. ``"dev"``).
    Version specifiers, extras, and markers are stripped — only the distribution
    name is kept.
    """
    if table == "project.dependencies":
        specs = pyproject.get("project", {}).get("dependencies", [])
    else:  # a [dependency-groups] group name, e.g. "dev"
        specs = pyproject.get("dependency-groups", {}).get(table, [])
    names: set[str] = set()
    for spec in specs:
        if not isinstance(spec, str):
            continue  # skip {include-group = ...} and other non-string entries
        m = _NAME_TOKEN.match(spec.strip())
        if m:
            names.add(normalize(m.group(0)))
    return names


def build_snapshot(
    lock_path: str,
    pyproject_path: str,
    *,
    repo: str,
    sha: str,
    ref: str,
    run_id: str,
    scanned: str | None = None,
) -> dict:
    """Parse uv.lock + pyproject.toml into a GitHub dependency snapshot dict.

    Pure and offline — no network, no env reads. Submission is the workflow's
    job (`gh api .../dependency-graph/snapshots`).
    """
    with open(lock_path, "rb") as fh:
        lock = tomllib.load(fh)

    lock_version = lock.get("version")
    if lock_version != 1:
        raise ValueError(
            f"Unsupported uv.lock format version {lock_version!r} (expected 1). "
            "Update this script after reviewing the new schema."
        )

    with open(pyproject_path, "rb") as fh:
        pyproject = tomllib.load(fh)

    direct = _declared_names(pyproject, "project.dependencies")
    packages = lock.get("package", [])

    # Scope by reachability, not by direct-name membership: a package is
    # `development` only if it is NOT reachable from any runtime root. Runtime
    # roots are the project's declared `[project.dependencies]`; we BFS over each
    # locked package's `dependencies` edges. Anything not runtime-reachable is
    # reachable only through dev roots (pytest/ruff *and* their exclusive
    # transitives like iniconfig/pluggy), so it is dev-scoped.
    edges: dict[str, set[str]] = {}
    for pkg in packages:
        pname = pkg.get("name")
        if not pname:
            continue
        edges.setdefault(normalize(pname), set()).update(
            normalize(dep["name"])
            for dep in pkg.get("dependencies", [])
            if isinstance(dep, dict) and dep.get("name")
        )
    runtime_reachable: set[str] = set()
    stack = list(direct)
    while stack:
        node = stack.pop()
        if node in runtime_reachable:
            continue
        runtime_reachable.add(node)
        stack.extend(edges.get(node, ()))

    resolved: dict[str, dict] = {}
    for pkg in packages:
        source = pkg.get("source", {})
        # Only registry-backed packages map to a pkg:pypi purl. This also
        # excludes the editable local project and any git/url/path sources,
        # which must not be mislabeled as PyPI distributions.
        if "registry" not in source:
            continue
        name = pkg.get("name")
        version = pkg.get("version")
        if not name or not version:
            continue
        norm = normalize(name)
        purl = f"pkg:pypi/{norm}@{version}"
        relationship = "direct" if norm in direct else "indirect"
        scope = "runtime" if norm in runtime_reachable else "development"
        # Keyed by purl so multi-version packages (numpy, onnxruntime) coexist.
        resolved[purl] = {
            "package_url": purl,
            "relationship": relationship,
            "scope": scope,
        }

    return {
        "version": 0,
        "job": {"id": str(run_id), "correlator": "dependency-submission-uv"},
        "sha": sha,
        "ref": ref,
        "detector": {
            "name": "idaho-vault-uv-dependency-submission",
            "version": "1.0.0",
            "url": f"https://github.com/{repo}",
        },
        "scanned": scanned or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "manifests": {
            "uv.lock": {
                "name": "uv.lock",
                "file": {"source_location": lock_path},
                "resolved": resolved,
            }
        },
    }


def main() -> int:
    """Read GitHub Actions env vars, build the snapshot, and write it to stdout.

    The workflow submits the emitted JSON via `gh api`; keeping submission out of
    this script is what lets `build_snapshot()` stay pure and offline-testable.
    """
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    sha = os.environ.get("GITHUB_SHA", "")
    ref = os.environ.get("GITHUB_REF", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "0")
    if not (repo and sha and ref):
        print(
            "::error::GITHUB_REPOSITORY, GITHUB_SHA and GITHUB_REF must be set.",
            file=sys.stderr,
        )
        return 1
    try:
        snapshot = build_snapshot(
            "uv.lock", "pyproject.toml", repo=repo, sha=sha, ref=ref, run_id=run_id
        )
    except (ValueError, OSError, tomllib.TOMLDecodeError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 1
    json.dump(snapshot, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
