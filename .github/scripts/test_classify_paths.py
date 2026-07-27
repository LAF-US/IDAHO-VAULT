"""Tests for the two-paired-flag risk classifier (classify_paths)."""

import json
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import classify_paths as cp

SCRIPT = Path(__file__).with_name("classify_paths.py")


class ClassifyFileTest(unittest.TestCase):
    def test_natural_language_prose_is_none(self):
        # Blueprint (2026-06-22): Natural Language in the maze -> `—` (None) on BOTH axes,
        # i.e. the `—/—` clear cell. NL no longer collapses to `low` (this is the step).
        self.assertEqual(cp.classify_file("Brad Little.md"), (None, None))
        self.assertEqual(cp.classify_file("WITNESS-THE-KEYS-2026-06-21.md"), (None, None))
        self.assertEqual(cp.classify_file("(2026) House Bill 24.md"), (None, None))
        self.assertEqual(cp.classify_file("notes/draft.txt"), (None, None))

    def test_machine_documentation_is_low(self):
        # Machine Documentation stays `low` — its distinction from prose is the point of the step.
        self.assertEqual(cp.classify_file("data/index.json"), ("low", None))
        self.assertEqual(cp.classify_file("config.yaml"), ("low", None))

    def test_computer_code_in_maze_is_med(self):
        self.assertEqual(cp.classify_file("scripts/scrape.py"), ("med", None))
        self.assertEqual(cp.classify_file("tools/run.sh"), ("med", None))
        self.assertEqual(cp.classify_file("LLM-Router.ipynb"), ("med", None))  # missing middle

    def test_unknown_type_is_conservative_med(self):
        self.assertEqual(cp.classify_file("mystery.q3z"), ("med", None))

    def test_nest_is_depth_high(self):
        # Inside the ! Nest -> placement high. The filetype axis scores INDEPENDENTLY
        # (two parallel analyses, Logan 2026-07-06): prose stays `—`, code carries med.
        self.assertEqual(cp.classify_file("!/AGENTS.md"), (None, "high"))
        self.assertEqual(cp.classify_file("! README.md"), (None, "high"))
        self.assertEqual(cp.classify_file("!-!-__!__-reflection_essay.md"), (None, "high"))
        self.assertEqual(cp.classify_file("!/swarm/tools/state_manager.py"), ("med", "high"))

    def test_still_point_is_nope(self):
        self.assertEqual(
            cp.classify_file("!/!/__!__/!/! The world is quiet here/Esto Perpetua!/README.md"),
            (None, "nope"),
        )
        # flattened alias of the canon core
        self.assertEqual(
            cp.classify_file("!-!-__!__-!-! The world is quiet here-Esto Perpetua!-!README.md"),
            (None, "nope"),
        )

    def test_still_point_substring_outside_nest_is_not_nope(self):
        # Copilot #2: a maze note merely *named* with the text must NOT be nope.
        # (It is prose -> `—/—` clear, the same as any other maze .md.)
        self.assertEqual(cp.classify_file("My Esto Perpetua! manifesto.md"), (None, None))
        self.assertFalse(cp.is_still_point("notes/Esto Perpetua! draft.md"))
        # A Nest file that is not the still-point segment stays high, not nope.
        self.assertEqual(cp.classify_file("!/ARBORSCAPING-REPORT-2026-04-16.md"), (None, "high"))

    def test_protected_surfaces_pinned_high(self):
        # Placement pins high; the filetype axis still speaks for itself (yml=low, py=med).
        self.assertEqual(cp.classify_file(".github/workflows/auto-merge-rhythm.yml"), ("low", "high"))
        self.assertEqual(cp.classify_file(".github/scripts/classify_paths.py"), ("med", "high"))
        self.assertEqual(cp.classify_file("CONSTITUTION.md"), (None, "high"))
        self.assertEqual(cp.classify_file("AGENTS.md"), (None, "high"))

    def test_dotfolder_surfaces_pinned_high(self):
        # Persona/config dotfolders must be pinned high regardless of filetype.
        # Editing .claude/ or .gemini/ is not a low-risk change.
        self.assertEqual(cp.classify_file(".claude/CLAUDE.md"), (None, "high"))
        self.assertEqual(cp.classify_file(".gemini/GEMINI.md"), (None, "high"))
        self.assertEqual(cp.classify_file(".codex/CODEX.md"), (None, "high"))
        self.assertEqual(cp.classify_file(".op/secrets.template.md"), (None, "high"))
        self.assertEqual(cp.classify_file(".perplexity/PERPLEXITY.md"), (None, "high"))

    def test_probe_carveout_low(self):
        # Probe sandboxes are a PLACEMENT carve-out (not a protected pin); the filetype
        # axis scores honestly: a probe .yml is machine-doc low, a probe .py is code med
        # (the old single pass hard-coded probe files to low — med is the fail-safe fix).
        self.assertEqual(cp.classify_file(".github/workflows/probe-smoke.yml"), ("low", None))
        self.assertEqual(cp.classify_file(".github/scripts/probe-runner.py"), ("med", None))

    def test_two_axes_are_independent(self):
        # The architecture bearing (#626, 2026-06-22; Logan 2026-07-06): filetype and
        # placement are two parallel analyses, each scoring EVERY file — placement never
        # suppresses filetype. The four corners of the composition:
        self.assertEqual(cp.classify_file("essay.md"), (None, None))                  # —/—
        self.assertEqual(cp.classify_file("tools/run.sh"), ("med", None))             # med/—
        self.assertEqual(cp.classify_file("!/essay.md"), (None, "high"))              # —/high
        self.assertEqual(cp.classify_file("!/swarm/run.sh"), ("med", "high"))         # med/high
        # And placement outranks filetype in the combined verdict, so tier4 is unchanged
        # by the split (a Nest .py was high before and is high now).
        self.assertEqual(cp.combine("med", "high"), "high")

    def test_retired_rhythm_glob_surfaces_all_pinned_high(self):
        # K1/K2 (#627/#628) equivalence guard: auto-merge-rhythm.yml retired its hand-
        # maintained protected-path glob and now defers to this classifier's placement axis
        # (`depth`), NOT `tier` — `tier` folds in filetype, so a med maze file like uv.lock
        # reads tier=high but depth=None and must stay eligible; keying on tier would
        # reintroduce the fail-closed-on-lockfiles bug. Every surface that glob protected MUST
        # still score a protected placement here, or the collapse would open auto-merge on a
        # formerly-protected path. One representative per retired glob entry; this fails loud
        # if the single source ever stops covering one of them.
        retired_glob_representatives = [
            ".github/workflows/deploy.yml",   # .github/workflows/*
            ".github/scripts/tool.py",        # .github/scripts/*
            ".codex/CODEX.md",                # .codex/*
            ".openclaw/config.yml",           # .openclaw/*
            "AGENTS.md",                      # AGENTS.md
            "CONSTITUTION.md",                # CONSTITUTION.md
            "DECISIONS.md",                   # DECISIONS.md
            "VAULT-CONVENTIONS.md",           # VAULT-CONVENTIONS.md
            "swarm.json",                     # swarm.json
            "!/anything.md",                  # !/*
        ]
        # The workflow keys on the placement axis firing at all (depth in {high, nope}) —
        # NOT tier — so a med-filetype maze file (uv.lock) stays eligible. Assert the exact
        # predicate the workflow reads.
        for path in retired_glob_representatives:
            with self.subTest(path=path):
                _filetype, depth = cp.classify_file(path)
                self.assertIn(depth, ("high", "nope"),
                              f"{path} must stay a protected placement (depth high/nope)")

    def test_dep_sync_lockfiles_stay_eligible_placement_clear(self):
        # Guard the K1/K2 collapse against the fail-open twin: the sync-bot's own dependency
        # files must NOT read as a protected placement, or the rhythm bot would never arm its
        # own PRs. uv.lock is filetype=med (unknown .lock), but placement is clear (depth None).
        for path in ("requirements.txt", "uv.lock"):
            with self.subTest(path=path):
                _filetype, depth = cp.classify_file(path)
                self.assertIsNone(depth, f"{path} must have no placement flag (stays eligible)")


class RiskiestTest(unittest.TestCase):
    def test_riskiest_picks_by_precedence(self):
        # The single ordering primitive: riskiest (earliest in TIER_PRECEDENCE) wins;
        # None flags are ignored; all-None -> None (the —/— clear case).
        self.assertEqual(cp.riskiest("low", "med"), "med")
        self.assertEqual(cp.riskiest(None, "high"), "high")
        self.assertEqual(cp.riskiest("low", None), "low")
        self.assertEqual(cp.riskiest("med", "nope"), "nope")
        self.assertIsNone(cp.riskiest(None, None))


class CombineTest(unittest.TestCase):
    def test_ordering_nope_high_med_low_clear(self):
        self.assertEqual(cp.combine("low", "nope"), "nope")
        self.assertEqual(cp.combine("med", "high"), "high")
        self.assertEqual(cp.combine("med", None), "med")
        self.assertEqual(cp.combine("low", None), "low")
        # —/— : neither sorter fired -> `clear`, kept DISTINCT from `low`.
        self.assertEqual(cp.combine(None, None), "clear")


class ChangesetTest(unittest.TestCase):
    def _run(self, paths):
        out = subprocess.run([sys.executable, str(SCRIPT)], input="\n".join(paths),
                             capture_output=True, text=True, check=True, timeout=30)
        return json.loads(out.stdout)

    def test_prose_only_pr_is_clear(self):
        # The #597 case: additive root-level prose research docs -> `—/—` clear (tier4),
        # the blueprint's auto-merge cell. Binary `tier` is UNCHANGED ("low") — clear folds
        # into low for the legacy label, so this step makes no live behavior change.
        r = self._run(["REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20.md",
                       "LOOKER-LANE-CLASSIFIER-BEHAVIORAL-MAP-2026-06-21.md"])
        self.assertEqual(r["tier4"], "clear")
        self.assertIsNone(r["filetype"])
        self.assertIsNone(r["depth"])
        self.assertEqual(r["tier"], "low")        # binary preserved: clear -> low
        self.assertIsNone(r["subtier"])           # subtiers TBD — next version

    def test_machine_doc_only_pr_is_low_not_clear(self):
        # Machine Documentation is a flag (`low`), DISTINCT from prose (`clear`) — the
        # whole point of the step. Binary tier is still "low" for both, so no live change.
        r = self._run(["data/index.json", "config.yaml"])
        self.assertEqual(r["tier4"], "low")
        self.assertEqual(r["filetype"], "low")
        self.assertEqual(r["tier"], "low")

    def test_code_only_pr_is_med_collapses_to_high(self):
        # Code files outside the Nest -> tier4=med, but binary tier collapses to high
        # (tier = "low" only when tier4 == "low"; everything above low is "high").
        r = self._run(["scripts/helper.py", "tools/run.sh"])
        self.assertEqual(r["tier4"], "med")
        self.assertEqual(r["tier"], "high")  # binary collapse: med -> high
        self.assertEqual(r["filetype"], "med")
        self.assertIsNone(r["depth"])
        self.assertIsNone(r["subtier"])

    def test_mixed_pr_carries_both_flags(self):
        r = self._run(["note.md", "scripts/x.py", "!/DOCKET.md"])
        self.assertEqual(r["filetype"], "med")   # the .py
        self.assertEqual(r["depth"], "high")     # the Nest file
        self.assertEqual(r["tier"], "high")
        self.assertEqual(r["tier4"], "high")

    def test_still_point_pr_is_nope(self):
        r = self._run(["!/!/__!__/!/! The world is quiet here/Esto Perpetua!/x.md"])
        self.assertEqual(r["tier4"], "nope")   # four-valued
        self.assertEqual(r["tier"], "high")    # binary legacy label

    def test_empty_is_clear(self):
        # No files touched -> `—/—` clear; binary tier folds to low.
        r = self._run([])
        self.assertEqual(r["tier4"], "clear")
        self.assertEqual(r["tier"], "low")


if __name__ == "__main__":
    unittest.main()
