"""Tests for the two-axis risk classifier (classify_paths)."""

import json
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import classify_paths as cp

SCRIPT = Path(__file__).with_name("classify_paths.py")


class FiletypeTest(unittest.TestCase):
    def test_natural_language_is_none(self):
        self.assertEqual(cp.classify_file("Brad Little.md"), (None, None))
        self.assertEqual(cp.classify_file("notes/draft.txt"), (None, None))
        self.assertEqual(cp.classify_file("(2026) House Bill 24.md"), (None, None))

    def test_machine_documentation_is_low(self):
        self.assertEqual(cp.classify_file("data/index.json"), ("low", None))
        self.assertEqual(cp.classify_file("config.yaml"), ("low", None))

    def test_computer_code_is_med(self):
        self.assertEqual(cp.classify_file("scripts/scrape.py"), ("med", None))
        self.assertEqual(cp.classify_file("tools/run.sh"), ("med", None))
        self.assertEqual(cp.classify_file("LLM-Router.ipynb"), ("med", None))

    def test_unknown_type_is_conservative_med(self):
        self.assertEqual(cp.classify_file("mystery.q3z"), ("med", None))


class PlacementTest(unittest.TestCase):
    def test_root_is_none(self):
        # A path under neither prefix scores None -- including flattened "!-…" root files,
        # which physically sit at repo root (their "-"-encoded name is not a directory path).
        self.assertIsNone(cp.placement_flag("essay.md"))
        self.assertIsNone(cp.placement_flag("! README.md"))
        self.assertIsNone(cp.placement_flag("!README.md"))
        self.assertIsNone(cp.placement_flag("!-!-__!__-reflection_essay.md"))
        self.assertIsNone(
            cp.placement_flag("!-!-__!__-!-! The world is quiet here-Esto Perpetua!-!README.md")
        )

    def test_inside_nest_is_high(self):
        # Inside "!/", above the inner prefix.
        self.assertEqual(cp.placement_flag("!/AGENTS.md"), "high")
        self.assertEqual(cp.placement_flag("!/!/README.md"), "high")
        self.assertEqual(cp.placement_flag("!/!/__!__/report.md"), "high")
        self.assertEqual(cp.placement_flag("!/swarm/tools/state_manager.py"), "high")

    def test_inner_and_below_is_nope(self):
        # The inner prefix "!/!/__!__/!/" and everything below it.
        self.assertEqual(cp.placement_flag("!/!/__!__/!/x.md"), "nope")
        self.assertEqual(
            cp.placement_flag("!/!/__!__/!/! The world is quiet here/y.md"), "nope"
        )
        self.assertEqual(
            cp.placement_flag(
                "!/!/__!__/!/! The world is quiet here/Esto Perpetua!/README.md"
            ),
            "nope",
        )

    def test_file_named_bang_inside_region_four_stays_high(self):
        # A file "!README.md" inside "!/!/__!__/" is not the "!/" directory below it; the
        # trailing slash in NOPE_PREFIX keeps it "high", not "nope".
        self.assertEqual(cp.placement_flag("!/!/__!__/!README.md"), "high")

    def test_dotfolders_and_governance_score_none(self):
        # No file or folder is special-cased on placement. Dotfolders (".github" is a
        # dotfolder like the rest) and root governance files are not under "!/" -> None.
        self.assertIsNone(cp.placement_flag(".github/workflows/deploy.yml"))
        self.assertIsNone(cp.placement_flag(".github/scripts/tool.py"))
        self.assertIsNone(cp.placement_flag(".claude/CLAUDE.md"))
        self.assertIsNone(cp.placement_flag(".op/secrets.template.md"))
        self.assertIsNone(cp.placement_flag("CONSTITUTION.md"))
        self.assertIsNone(cp.placement_flag("swarm.json"))

    def test_axes_are_independent(self):
        # filetype and placement score separately; a code file in the nest carries both.
        self.assertEqual(cp.classify_file("!/swarm/run.sh"), ("med", "high"))
        self.assertEqual(cp.classify_file("!/essay.md"), (None, "high"))
        self.assertEqual(cp.classify_file(".github/workflows/deploy.yml"), ("low", None))
        self.assertEqual(cp.classify_file(".github/scripts/tool.py"), ("med", None))

    def test_lockfiles_are_placement_clear(self):
        for path in ("requirements.txt", "uv.lock"):
            with self.subTest(path=path):
                self.assertIsNone(cp.placement_flag(path))

    def test_windows_separators_are_normalized(self):
        # classify_file normalizes '\\' to '/' so placement prefixes match regardless of
        # separator style (git/gh emit '/', but local/tooling input may use '\\').
        self.assertEqual(cp.classify_file("!\\AGENTS.md"), (None, "high"))
        self.assertEqual(cp.classify_file("!\\!\\__!__\\!\\x.md"), (None, "nope"))
        self.assertEqual(cp.classify_file("!\\swarm\\run.sh"), ("med", "high"))


class RiskiestTest(unittest.TestCase):
    def test_riskiest_picks_by_precedence(self):
        self.assertEqual(cp.riskiest("low", "med"), "med")
        self.assertEqual(cp.riskiest(None, "high"), "high")
        self.assertEqual(cp.riskiest("low", None), "low")
        self.assertEqual(cp.riskiest("med", "nope"), "nope")
        self.assertIsNone(cp.riskiest(None, None))


class CombineTest(unittest.TestCase):
    def test_ordering(self):
        self.assertEqual(cp.combine("low", "nope"), "nope")
        self.assertEqual(cp.combine("med", "high"), "high")
        self.assertEqual(cp.combine("med", None), "med")
        self.assertEqual(cp.combine("low", None), "low")
        self.assertEqual(cp.combine(None, None), "clear")


class ChangesetTest(unittest.TestCase):
    def _run(self, paths):
        out = subprocess.run([sys.executable, str(SCRIPT)], input="\n".join(paths),
                             capture_output=True, text=True, check=True, timeout=30)
        return json.loads(out.stdout)

    def test_prose_only_pr_is_clear(self):
        r = self._run(["research-a.md", "research-b.md"])
        self.assertEqual(r["tier4"], "clear")
        self.assertIsNone(r["filetype"])
        self.assertIsNone(r["depth"])
        self.assertEqual(r["tier"], "low")
        self.assertIsNone(r["subtier"])

    def test_machine_doc_only_pr_is_low(self):
        r = self._run(["data/index.json", "config.yaml"])
        self.assertEqual(r["tier4"], "low")
        self.assertEqual(r["filetype"], "low")
        self.assertEqual(r["tier"], "low")

    def test_code_only_pr_is_med_binary_high(self):
        r = self._run(["scripts/helper.py", "tools/run.sh"])
        self.assertEqual(r["tier4"], "med")
        self.assertEqual(r["tier"], "high")
        self.assertEqual(r["filetype"], "med")
        self.assertIsNone(r["depth"])

    def test_mixed_pr_carries_both_flags(self):
        r = self._run(["note.md", "scripts/x.py", "!/DOCKET.md"])
        self.assertEqual(r["filetype"], "med")
        self.assertEqual(r["depth"], "high")
        self.assertEqual(r["tier"], "high")
        self.assertEqual(r["tier4"], "high")

    def test_inner_pr_is_nope(self):
        r = self._run(["!/!/__!__/!/! The world is quiet here/Esto Perpetua!/x.md"])
        self.assertEqual(r["tier4"], "nope")
        self.assertEqual(r["tier"], "high")

    def test_empty_is_clear(self):
        r = self._run([])
        self.assertEqual(r["tier4"], "clear")
        self.assertEqual(r["tier"], "low")


if __name__ == "__main__":
    unittest.main()
