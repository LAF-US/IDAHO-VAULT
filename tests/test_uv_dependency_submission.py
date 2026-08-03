from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "uv_dependency_submission.py"

# Load the script as a module (it lives under .github/scripts, not on sys.path).
_spec = importlib.util.spec_from_file_location("uv_dependency_submission", SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"could not create an import spec/loader for {SCRIPT}")
uds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uds)

_PURL = re.compile(r"^pkg:pypi/[a-z0-9.-]+@.+$")


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
        for purl in (
            "pkg:pypi/crewai@",
            "pkg:pypi/flask@",
            "pkg:pypi/pydantic@",
            "pkg:pypi/huggingface-hub@",
            "pkg:pypi/requests-oauthlib@",
            "pkg:pypi/honcho-ai@",
            "pkg:pypi/pygit2@",
        ):
            match = [v for k, v in self.resolved.items() if k.startswith(purl)]
            self.assertTrue(match, f"missing direct dependency {purl}")
            # Every locked version of a declared dep must be direct, not just the first.
            self.assertTrue(
                all(v["relationship"] == "direct" for v in match),
                f"non-direct entry found for {purl}",
            )

    def test_scope_is_runtime_reachability_based(self) -> None:
        # Scope is derived from runtime reachability, not direct-name membership.
        # Dev tools AND their exclusive transitives are development-scoped...
        for name in ("pytest", "ruff", "iniconfig", "pluggy"):
            match = [v for k, v in self.resolved.items() if k.startswith(f"pkg:pypi/{name}@")]
            self.assertTrue(match, f"missing {name}")
            self.assertTrue(
                all(v["scope"] == "development" for v in match),
                f"{name} should be development-scoped: {match}",
            )
        # ...while transitives reachable from runtime roots stay runtime-scoped,
        # including ones shared with dev tools (e.g. packaging via both).
        for name in ("flask", "crewai", "packaging", "click"):
            match = [v for k, v in self.resolved.items() if k.startswith(f"pkg:pypi/{name}@")]
            self.assertTrue(match, f"missing {name}")
            self.assertTrue(
                all(v["scope"] == "runtime" for v in match),
                f"{name} should be runtime-scoped: {match}",
            )

    def test_multi_version_packages_are_both_kept(self) -> None:
        # uv's universal lock pins numpy at three versions and onnxruntime at two
        # (the exact case pip-compile cannot resolve). Keying by purl keeps all.
        numpy = sorted(k for k in self.resolved if k.startswith("pkg:pypi/numpy@"))
        onnx = sorted(k for k in self.resolved if k.startswith("pkg:pypi/onnxruntime@"))
        self.assertEqual(len(numpy), 3, numpy)
        self.assertEqual(len(onnx), 2, onnx)

    def test_resolved_count_matches_non_local_versioned_packages(self) -> None:
        # 165 [[package]] entries in uv.lock (163 + pygit2, added in #891 to
        # read Git's tracked index directly via libgit2 bindings instead of
        # shelling out to the git binary; pygit2 appears as two version-split
        # entries -- 1.18.2 for Python 3.10, 1.19.3 for 3.11+ -- the same
        # multi-version pattern as numpy/onnxruntime below), minus the single
        # editable local project, all registry packages versioned -> 164
        # distinct purls.
        self.assertEqual(len(self.resolved), 164)


if __name__ == "__main__":
    unittest.main()
