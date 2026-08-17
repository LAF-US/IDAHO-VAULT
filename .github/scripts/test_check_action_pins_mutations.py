#!/usr/bin/env python3
"""Break the action-pin guard on purpose and check that its tests notice.

A passing test suite proves nothing on its own. `test_check_action_pins.py`
guards a script whose failure mode is silence -- it prints OK and exits 0
whether or not it read the container it was asked about -- so the suite has to
be shown capable of going red for each defence it claims to cover, not merely
observed to be green.

This reintroduces each historical defect one at a time into a throwaway copy
and runs the suite against it. Every mutant must be killed. Three of these
survived the first draft of the tests and sent real cases back for rewriting:
the BOM mutant survived because that test asserted a decode error a BOM does
not actually cause, and the scoping mutant survived because its fixture did
not contain the text the scoping decision turns on.

It is a test module, discovered by CI like any other, but its one case skips
unless `RUN_MUTATION_TESTS` is set. Skipped rather than run because each entry
quotes a line of the guard verbatim: a legitimate refactor of that line makes
this fail with `PATTERN MISSING`, which is worth a person's attention on the
pull request that caused it and is not worth blocking an unrelated one. The
skip is printed on every CI run, so the tool announces itself instead of
sitting in the tree waiting to be remembered. `PATTERN MISSING` counts as a
survivor and fails, never as a pass -- a mutation that no longer applies has
stopped testing anything.

(It was first written as `mutate_check_action_pins.py`, kept out of discovery
by its name. That was worse on both counts: invisible in CI, and classified as
runtime code by the repository's scanners, which flag `subprocess` there and
suppress it in test files. It is test code; the name now says so.)

    RUN_MUTATION_TESTS=1 python3 -m unittest discover -s .github/scripts
    python3 .github/scripts/test_check_action_pins_mutations.py   # always runs
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
GUARD = SCRIPTS / "check_action_pins.py"
SUITE = SCRIPTS / "test_check_action_pins.py"


def mutations(guard: str) -> dict[str, tuple[str, str]]:
    """Each historical defect, as (what the guard says now, the broken form)."""
    runs_pattern = re.search(r"RUNS_PATTERN = re\.compile\(.*?\)\n", guard, re.DOTALL)
    strip_line = next(
        (
            f"{line}\n"
            for line in guard.splitlines()
            if "without_strings = re.sub(" in line
        ),
        "",
    )
    comment_line = next(
        (
            f"{line}\n"
            for line in guard.splitlines()
            if "return re.split(r" in line and "#" in line
        ),
        "",
    )
    return {
        # Discovery
        "recursive glob instead of a no-follow walk": (
            '    actions_root = REPO_ROOT / ".github" / "actions"',
            '    paths.extend(sorted(REPO_ROOT.glob(".github/actions/**/action.yml")))\n'
            '    actions_root = REPO_ROOT / "nonexistent-disabled"',
        ),
        "duplicate targets returned": (
            "return sorted(set(paths))",
            "return sorted(paths)",
        ),
        "symlinks resolved instead of refused": (
            '    if candidate.is_symlink():\n        return None, "symlink; not read"',
            '    if False:\n        return None, "symlink; not read"',
        ),
        "containment check removed": (
            "        candidate.relative_to(REPO_ROOT)",
            "        pass",
        ),
        # Reading
        "plain utf-8 read (BOM intolerant)": (
            'return path.read_text(encoding="utf-8-sig"), ""',
            'return path.read_text(encoding="utf-8"), ""',
        ),
        "no UnicodeDecodeError handler": (
            "    except UnicodeDecodeError:\n"
            '        return None, "not valid UTF-8; cannot verify pins"\n',
            "",
        ),
        # `uses:`
        "flow-form uses: treated as safe": (
            "            if FLOW_USES_PATTERN.search(_outside_strings(line)):",
            "            if False and FLOW_USES_PATTERN.search(_outside_strings(line)):",
        ),
        "quoted keys stripped too (flow hole reopens)": (
            strip_line,
            strip_line.replace(r"(?!\s*:)", ""),
        ),
        "comment stripping removed (false positives)": (
            comment_line,
            "    return without_strings\n",
        ),
        "expression refs treated as safe": (
            "        if EXPRESSION_PATTERN.search(ref):",
            "        if False:",
        ),
        # Container actions
        "image: not held to a digest": (
            "        if not IMAGE_DIGEST_PATTERN.search(image):\n"
            '            findings.append((lineno, f"{image} (image needs @sha256:<64 hex>)"))',
            "        if False:\n            pass",
        ),
        "runs: anchored at column 0": (
            runs_pattern.group(0) if runs_pattern else "",
            runs_pattern.group(0).replace(r"^(\s*)", "^()") if runs_pattern else "",
        ),
        "root-indent scoping disabled": (
            "        if not match or (root is not None and match.group(1) != root):",
            "        if not match:",
        ),
        "flow-form runs: treated as safe": (
            "        if FLOW_RUNS_PATTERN.search(_outside_strings(line)):",
            "        if False and FLOW_RUNS_PATTERN.search(_outside_strings(line)):",
        ),
        "block scoping removed (a decoy image vouches)": (
            "        block = _block_at(lines, lineno, match.group(1))",
            "        block = lines",
        ),
        "workflow container/services unchecked": (
            "        *_workflow_inline_image_findings(path, lines),",
            "",
        ),
        # Dockerfiles
        "Dockerfile FROM lines unchecked": (
            "            findings.extend(_unpinned_from_lines(path, image, lineno))",
            "            pass",
        ),
        "physical Dockerfile lines (no continuation join)": (
            "    lines = text.splitlines()\n    escape = _escape_char(lines)",
            "    return list(enumerate(text.splitlines(), start=1))\n"
            "    lines = text.splitlines()\n    escape = _escape_char(lines)",
        ),
        "a stage may exempt itself": (
            '        exempt = base.lower() == "scratch" or base.lower() in stages',
            '        exempt = base.lower() == "scratch" or '
            "(stages.add(stage.lower()) if stage else None) or base.lower() in stages",
        ),
        # Reporting
        "empty repository passes instead of erroring": (
            "        return 2",
            "        return 0",
        ),
        "a warning on the clean path goes unnoticed": (
            '    print("action-pin guard: OK")',
            '    print("action-pin guard: some files skipped", file=sys.stderr)\n'
            '    print("action-pin guard: OK")',
        ),
    }


def _run_suite(scripts: Path) -> subprocess.CompletedProcess[str]:
    """Run a copy of the suite against whatever guard sits beside it."""
    return subprocess.run(
        # A list, never a string, and never `shell=True`: the arguments are
        # `sys.executable` and a path this module just made under the system
        # temporary directory. Nothing is parsed by a shell and nothing comes
        # from outside the repository, which is why the audit-grade "subprocess
        # without a static string" warning finds no injection to report. The
        # child process IS the measurement: the mutant has to be loaded fresh,
        # and importing a second copy of the guard here would not do that.
        [sys.executable, str(scripts / SUITE.name)],
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )


def _failures(result: subprocess.CompletedProcess[str]) -> list[str]:
    """What noticed, in one run. Empty only when the suite actually passed.

    The exit code is the authority, not the parsed names. A mutant that breaks
    the module badly enough to die before unittest prints any `FAIL:`/`ERROR:`
    header — an import error, a syntax error, an interpreter crash — produced
    no names to find, and the run was then labelled a SURVIVOR: the suite was
    screaming and this read it as silence. That erred safe (a false survivor
    fails the sweep, it does not hide a regression) but it named the wrong
    thing, which is its own defect in a tool whose whole job is to report
    honestly what a test run did.

    Calling a non-zero exit a kill is only sound because the baseline ran
    first: the suite is known to pass unmutated, so a failure under mutation
    is attributable to the mutation and not to a broken suite.
    """
    if result.returncode == 0:
        return []
    named = sorted(
        set(re.findall(r"^(?:FAIL|ERROR): (\w+)", result.stderr, re.MULTILINE))
    )
    return named or [f"(no named failure; exit {result.returncode})"]


def surviving_mutants(report=print) -> list[str]:
    """Every mutation the suite failed to notice. Empty is the only pass.

    The baseline goes first. Grading mutants against a suite that is already
    failing reports every one of them killed -- a green 21/21 that measures
    nothing, which is the exact false confidence this tool exists to deny the
    guard. So the untouched suite runs once, and a dirty baseline stops the run
    rather than being averaged into it.
    """
    guard = GUARD.read_text(encoding="utf-8")
    survivors: list[str] = []

    baseline = _run_suite(SCRIPTS)
    if baseline.returncode != 0:
        report("BASELINE DIRTY   the suite does not pass unmutated; nothing to grade")
        for name in _failures(baseline):
            report(f"{'':17}  {name}")
        report(baseline.stderr[-2000:])
        return ["baseline"]

    for label, (original, broken) in mutations(guard).items():
        if not original or original not in guard:
            report(f"{'PATTERN MISSING':17}{label}")
            survivors.append(label)
            continue

        workspace = Path(tempfile.mkdtemp(prefix="mutant-"))
        try:
            (workspace / "scripts").mkdir()
            (workspace / "scripts" / GUARD.name).write_text(
                guard.replace(original, broken, 1), encoding="utf-8"
            )
            shutil.copy(SUITE, workspace / "scripts" / SUITE.name)
            result = _run_suite(workspace / "scripts")
        except BaseException:
            shutil.rmtree(workspace, ignore_errors=True)
            raise

        killed_by = _failures(result)
        if killed_by:
            report(f"{'killed':17}{label}\n{'':17}  by {', '.join(killed_by[:3])}")
            shutil.rmtree(workspace, ignore_errors=True)
        else:
            # Kept, not cleaned. A survivor is the one case where someone needs
            # to look at the mutant and ask why the suite could not see it --
            # which is how three of these were turned into real test cases
            # rather than dismissed.
            report(f"{'*** SURVIVED ***':17}{label}\n{'':17}  kept at {workspace}")
            survivors.append(label)

    total = len(mutations(guard))
    report(f"\n{total - len(survivors)}/{total} mutants killed")
    return survivors


class MutationTest(unittest.TestCase):
    """The suite must be able to go red for every defence it claims."""

    @unittest.skipUnless(
        os.environ.get("RUN_MUTATION_TESTS"),
        "set RUN_MUTATION_TESTS=1 to break the guard on purpose (~1 min)",
    )
    def test_every_mutant_is_killed(self):
        self.assertEqual(
            surviving_mutants(), [], "the suite cannot see these regressions"
        )


def main() -> int:
    survivors = surviving_mutants()
    if survivors:
        print("survivors (the suite cannot see these):")
        for label in survivors:
            print(f"  {label}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
