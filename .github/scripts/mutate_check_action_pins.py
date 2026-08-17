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

Deliberately NOT named `test_*.py`: this is a manual verification tool, not
part of the CI suite, because each entry quotes a line of the guard verbatim
and will need updating when that line legitimately changes. A `PATTERN MISSING`
result means exactly that -- the guard moved out from under a mutation, and
this file needs attention. It counts as a survivor, never as a pass.

    python3 .github/scripts/mutate_check_action_pins.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
GUARD = SCRIPTS / "check_action_pins.py"
SUITE = SCRIPTS / "test_check_action_pins.py"


def mutations(guard: str) -> dict[str, tuple[str, str]]:
    """Each historical defect, as (what the guard says now, the broken form)."""
    runs_pattern = re.search(r"RUNS_PATTERN = re\.compile\(.*?\)\n", guard, re.S)
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
            "return sorted(dict.fromkeys(paths))",
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


def main() -> int:
    guard = GUARD.read_text(encoding="utf-8")
    survivors: list[str] = []

    for label, (original, broken) in mutations(guard).items():
        if not original or original not in guard:
            print(f"{'PATTERN MISSING':17}{label}")
            survivors.append(label)
            continue

        workspace = Path(tempfile.mkdtemp(prefix="mutant-"))
        try:
            (workspace / "scripts").mkdir()
            (workspace / "scripts" / GUARD.name).write_text(
                guard.replace(original, broken, 1), encoding="utf-8"
            )
            shutil.copy(SUITE, workspace / "scripts" / SUITE.name)
            result = subprocess.run(
                [sys.executable, str(workspace / "scripts" / SUITE.name)],
                capture_output=True,
                text=True,
                timeout=600,
            )
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

        killed_by = sorted(
            set(re.findall(r"^(?:FAIL|ERROR): (\w+)", result.stderr, re.M))
        )
        if killed_by:
            print(f"{'killed':17}{label}\n{'':17}  by {', '.join(killed_by[:3])}")
        else:
            print(f"{'*** SURVIVED ***':17}{label}")
            survivors.append(label)

    total = len(mutations(guard))
    print(f"\n{total - len(survivors)}/{total} mutants killed")
    if survivors:
        print("survivors (the suite cannot see these):")
        for label in survivors:
            print(f"  {label}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
