from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "uv_dependency_submission.py"

# Load the script as a module (it lives under .github/scripts, not on sys.path).
_spec = importlib.util.spec_from_file_location("uv_dependency_submission", SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"could not create an import spec/loader for {SCRIPT}")
uds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uds)

_PURL = re.compile(r"^pkg:pypi/[a-z0-9.-]+@.+$")
# PEP 508: the name runs until the first version/marker/extra punctuation.
_REQ_NAME = re.compile(r"^\s*([A-Za-z0-9._-]+)")


def _req_name(spec: str) -> str:
    """Pull the bare distribution name out of a dependency specifier."""
    match = _REQ_NAME.match(spec)
    if match is None:
        raise ValueError(f"unparseable dependency specifier: {spec!r}")
    return match.group(1)


class UvDependencySubmissionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot = uds.build_snapshot(
            str(ROOT / "uv.lock"),
            str(ROOT / "pyproject.toml"),
            repo="LAF-US/IDAHO-VAULT",
            sha="0" * 40,
            ref="refs/heads/main",
            run_id="123",
            scanned="2026-06-19T00:00:00Z",
        )
        cls.resolved = cls.snapshot["manifests"]["uv.lock"]["resolved"]
        # Derived, never hardcoded. Every assertion below reads its expectation
        # out of uv.lock / pyproject.toml at run time, because the dependency
        # set is a decision that changes and a test that pins yesterday's set
        # fails for the one reason that is never a defect: the manifest moved.
        with open(ROOT / "uv.lock", "rb") as fh:
            cls.lock = tomllib.load(fh)
        with open(ROOT / "pyproject.toml", "rb") as fh:
            cls.pyproject = tomllib.load(fh)
        cls.registry_packages = [
            pkg for pkg in cls.lock["package"] if "registry" in pkg.get("source", {})
        ]
        cls.declared_runtime = [
            uds.normalize(_req_name(spec))
            for spec in cls.pyproject["project"].get("dependencies", [])
        ]
        cls.declared_dev = [
            uds.normalize(_req_name(spec))
            for spec in cls.pyproject.get("dependency-groups", {}).get("dev", [])
        ]

    def test_unsupported_lock_version_raises_valueerror(self) -> None:
        # build_snapshot is a reusable, pure function: it raises a normal
        # exception (not SystemExit) so callers can handle the error path.
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / "uv.lock"
            lock.write_text('version = 2\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                uds.build_snapshot(
                    str(lock),
                    str(ROOT / "pyproject.toml"),
                    repo="LAF-US/IDAHO-VAULT",
                    sha="0" * 40,
                    ref="refs/heads/main",
                    run_id="123",
                )

    def test_snapshot_envelope(self) -> None:
        s = self.snapshot
        self.assertEqual(s["version"], 0)
        self.assertEqual(s["job"]["correlator"], "dependency-submission-uv")
        self.assertEqual(s["ref"], "refs/heads/main")
        self.assertIn("uv.lock", s["manifests"])
        self.assertEqual(s["manifests"]["uv.lock"]["name"], "uv.lock")
        self.assertEqual(
            s["detector"]["name"], "idaho-vault-uv-dependency-submission"
        )

    def test_every_purl_is_well_formed(self) -> None:
        for key, entry in self.resolved.items():
            self.assertEqual(key, entry["package_url"])
            self.assertRegex(entry["package_url"], _PURL)
            self.assertIn(entry["relationship"], ("direct", "indirect"))
            self.assertIn(entry["scope"], ("runtime", "development"))

    def test_local_project_is_excluded(self) -> None:
        # The editable repo itself (idaho-vault) is not a submittable dependency.
        self.assertFalse(any("idaho-vault" in key for key in self.resolved))

    def test_declared_dependencies_are_marked_direct(self) -> None:
        # The property: whatever `[project.dependencies]` declares is `direct`.
        # The list comes from the manifest, so adding or dropping a dependency
        # changes what is checked without editing this test.
        self.assertTrue(self.declared_runtime, "no runtime dependencies declared")
        for name in self.declared_runtime:
            purl = f"pkg:pypi/{name}@"
            match = [v for k, v in self.resolved.items() if k.startswith(purl)]
            self.assertTrue(match, f"missing direct dependency {purl}")
            # Every locked version of a declared dep must be direct, not just the first.
            self.assertTrue(
                all(v["relationship"] == "direct" for v in match),
                f"non-direct entry found for {purl}",
            )

    def test_scope_is_runtime_reachability_based(self) -> None:
        # Scope is reachability, not direct-name membership. Both root sets and
        # the edges come from the lock, so this states the rule rather than a
        # census of which packages happened to be installed the day it was written.
        # MERGE, do not overwrite. A dict comprehension keyed on the normalized name
        # keeps only the LAST record for a package the lock pins at several versions
        # (pygit2 today), silently dropping the earlier version's edges — and a
        # dependency reachable only through the dropped record then falls out of both
        # root sets and has its scope silently unchecked below. `build_snapshot`
        # accumulates with setdefault().update(); this has to match, or the
        # independent re-derivation is re-deriving something else.
        edges: dict[str, set[str]] = {}
        for pkg in self.lock["package"]:
            if not pkg.get("name"):
                continue
            edges.setdefault(uds.normalize(pkg["name"]), set()).update(
                uds.normalize(dep["name"])
                for dep in pkg.get("dependencies", [])
                if isinstance(dep, dict) and dep.get("name")
            )

        def reachable_from(roots: list[str]) -> set[str]:
            seen: set[str] = set()
            stack = list(roots)
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.add(node)
                stack.extend(edges.get(node, ()))
            return seen

        runtime = reachable_from(self.declared_runtime)
        dev_only = reachable_from(self.declared_dev) - runtime
        self.assertTrue(runtime, "no runtime-reachable packages")
        self.assertTrue(dev_only, "no dev-exclusive packages")

        for purl, entry in self.resolved.items():
            name = purl.removeprefix("pkg:pypi/").rsplit("@", 1)[0]
            if name in runtime:
                # Shared transitives (reachable from BOTH root sets) stay runtime.
                self.assertEqual(entry["scope"], "runtime", purl)
            elif name in dev_only:
                self.assertEqual(entry["scope"], "development", purl)

    def test_multi_version_packages_are_both_kept(self) -> None:
        # uv's universal lock can pin one package at several versions across the
        # requires-python range — the exact case pip-compile cannot resolve.
        # Keying `resolved` by purl instead of by name is what preserves them.
        # Which package splits is a function of the manifest (dropping
        # requires-python collapses every split), so the split is found rather
        # than named.
        counts: dict[str, int] = {}
        for pkg in self.registry_packages:
            counts[uds.normalize(pkg["name"])] = counts.get(uds.normalize(pkg["name"]), 0) + 1
        split = {name: n for name, n in counts.items() if n > 1}
        self.assertTrue(
            split,
            "uv.lock has no multi-version package, so this property is untested — "
            "check requires-python still spans more than one minor version",
        )
        for name, expected in split.items():
            kept = [k for k in self.resolved if k.startswith(f"pkg:pypi/{name}@")]
            self.assertEqual(len(kept), expected, sorted(kept))

    def test_resolved_matches_non_local_versioned_packages(self) -> None:
        # Every registry-backed [[package]] becomes exactly one purl; the editable
        # local project and any git/url/path sources become none. Derived from the
        # lock, which is what the previous hardcoded 164 was a snapshot of.
        #
        # Identities, not just cardinality: equal counts also hold if a registry
        # package went missing and a git/url/path source was mislabeled as PyPI in
        # its place, which is the substitution this test exists to catch. The count
        # assertion stays alongside it — a set comparison cannot see duplicate
        # resolved records, since a set collapses them.
        expected = {
            f"pkg:pypi/{uds.normalize(pkg['name'])}@{pkg['version']}"
            for pkg in self.registry_packages
        }
        self.assertTrue(self.registry_packages, "uv.lock has no registry packages")
        self.assertEqual(set(self.resolved), expected)
        self.assertEqual(len(self.resolved), len(self.registry_packages))


if __name__ == "__main__":
    unittest.main()
