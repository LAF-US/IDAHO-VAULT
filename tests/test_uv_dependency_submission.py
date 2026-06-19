from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "uv_dependency_submission.py"

# Load the script as a module (it lives under .github/scripts, not on sys.path).
_spec = importlib.util.spec_from_file_location("uv_dependency_submission", SCRIPT)
assert _spec and _spec.loader
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
        ):
            match = [v for k, v in self.resolved.items() if k.startswith(purl)]
            self.assertTrue(match, f"missing direct dependency {purl}")
            self.assertEqual(match[0]["relationship"], "direct")

    def test_multi_version_packages_are_both_kept(self) -> None:
        # uv's universal lock pins numpy and onnxruntime at two versions each
        # (the exact case pip-compile cannot resolve). Keying by purl keeps both.
        numpy = sorted(k for k in self.resolved if k.startswith("pkg:pypi/numpy@"))
        onnx = sorted(k for k in self.resolved if k.startswith("pkg:pypi/onnxruntime@"))
        self.assertEqual(len(numpy), 2, numpy)
        self.assertEqual(len(onnx), 2, onnx)

    def test_resolved_count_matches_non_local_versioned_packages(self) -> None:
        # 149 [[package]] entries in uv.lock, minus the single editable local
        # project, all registry packages versioned -> 148 distinct purls.
        self.assertEqual(len(self.resolved), 148)


if __name__ == "__main__":
    unittest.main()
