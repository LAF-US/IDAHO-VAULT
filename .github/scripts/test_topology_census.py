"""Tests for the topology census scope contract (topology_census).

Covers the second half of the census requirement: that the census emits the
scopes its doctrine mandates, in a deterministic order.

Order is the part worth pinning. Every scope report is written to a file and
indexed, so a non-deterministic scope order produces a different index on every
run for an unchanged tree — which turns a census, whose whole purpose is to be
diffable against the last one, into noise. `_resolve_scopes` is the single
place that order is decided, so it is asserted here as an ordered list rather
than a set: a set comparison would pass while the order drifted, which is
exactly the failure this is meant to catch.

The tests are deliberately unit-level against the scope contract and do not run
a full census. Building real reports would need doctrine files, a git tree, and
disk writes, and would assert the gatherers' output rather than the scope
contract — a slower test of a different thing.

KNOWN DIVERGENCE, recorded rather than hidden: CENSUS.md's scope table mandates
FOUR scopes and the implementation resolves THREE. `Git refs` has no gatherer.
That gap is pinned below as an expected failure, so it is visible in the run
instead of living only in prose, and so that implementing it reports an
unexpected success and prompts removal of the marker.
"""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# topology_census.py lives in scripts_scripts/, not beside this file. Search both
# so the test follows the module rather than pinning one layout: a stale
# .github/scripts/__pycache__/topology_census.*.pyc will satisfy a bare import
# locally long after the source moved, which hides exactly this breakage until CI
# runs on a clean checkout.
for _candidate in (REPO_ROOT / "scripts_scripts", Path(__file__).resolve().parent):
    if (_candidate / "topology_census.py").is_file():
        sys.path.insert(0, str(_candidate))
        break
else:  # pragma: no cover - only when the module is deleted outright
    raise ModuleNotFoundError(
        "topology_census.py not found in scripts_scripts/ or beside this test"
    )

import topology_census as census  # noqa: E402
CENSUS_DOCTRINE = REPO_ROOT / "CENSUS.md"

# The scope keys the tool implements, in the order `--scope all` emits them.
MANDATED_ORDER = ["root", "dotfolders", "nest"]

# Doctrine label -> implementation scope key. `None` means doctrine names the
# scope but no gatherer implements it.
DOCTRINE_TO_SCOPE = {
    "Nest": "nest",
    "Persona chambers": "dotfolders",
    "Root": "root",
    "Git refs": None,
}


def _doctrine_scope_labels() -> list[str]:
    """The Scope column of CENSUS.md's scope table, in document order.

    Parsed from the committed doctrine rather than restated here, so the test
    fails when doctrine and implementation drift apart instead of agreeing with
    a copy of doctrine that has itself gone stale.
    """
    labels: list[str] = []
    in_table = False
    for line in CENSUS_DOCTRINE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Scope "):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cell = line.split("|")[1].strip()
            if set(cell) <= {"-", " "}:  # the header separator row
                continue
            # Drop the parenthetical path hint: "Nest (`!/`)" -> "Nest".
            labels.append(re.sub(r"\s*\(.*\)\s*$", "", cell))
    return labels


class ScopeOrderTest(unittest.TestCase):
    def test_all_resolves_to_a_fixed_order(self):
        # Ordered comparison on purpose — see the module docstring.
        self.assertEqual(census._resolve_scopes("all"), MANDATED_ORDER)

    def test_order_is_stable_across_calls(self):
        self.assertEqual(census._resolve_scopes("all"), census._resolve_scopes("all"))

    def test_single_scope_resolves_to_itself(self):
        for scope in MANDATED_ORDER:
            with self.subTest(scope=scope):
                self.assertEqual(census._resolve_scopes(scope), [scope])

    def test_no_scope_is_emitted_twice(self):
        scopes = census._resolve_scopes("all")
        self.assertEqual(len(scopes), len(set(scopes)))


class UnsupportedScopeTest(unittest.TestCase):
    def test_unknown_scope_fails_loudly(self):
        # Must raise, not return an empty report: a census that silently emits
        # nothing for a scope reads downstream as "this scope is empty" —
        # indistinguishable from a real finding of zero bodies.
        with self.assertRaises(ValueError):
            census.build_scope_report(REPO_ROOT, "refs")

    def test_cli_rejects_an_unknown_scope(self):
        # argparse prints its usage to stderr on rejection; captured so an
        # intentional failure does not look like a broken run in CI logs.
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                census.main(["--scope", "refs"])
        self.assertEqual(raised.exception.code, 2)


class DoctrineAgreementTest(unittest.TestCase):
    """The implemented scopes must be ones doctrine actually names."""

    def test_doctrine_table_is_parseable(self):
        self.assertTrue(CENSUS_DOCTRINE.is_file(), f"missing {CENSUS_DOCTRINE}")
        self.assertEqual(_doctrine_scope_labels(), list(DOCTRINE_TO_SCOPE))

    def test_every_implemented_scope_is_named_in_doctrine(self):
        # Catches drift in the tool-ahead-of-doctrine direction: a scope added
        # to the census without a corresponding row in CENSUS.md.
        named = {DOCTRINE_TO_SCOPE[label] for label in _doctrine_scope_labels()}
        for scope in census._resolve_scopes("all"):
            with self.subTest(scope=scope):
                self.assertIn(scope, named)

    @unittest.expectedFailure
    def test_every_mandated_scope_is_implemented(self):
        # KNOWN DIVERGENCE. CENSUS.md mandates `Git refs` (named branches, PR
        # refs, orphan lineages); topology_census has no gatherer for it, so
        # `--scope all` covers three of the four mandated scopes.
        #
        # Marked expectedFailure rather than deleted or softened: the
        # requirement is real and belongs in the suite, and when the gatherer
        # lands this reports an UNEXPECTED SUCCESS, which is the signal to drop
        # this decorator instead of leaving a passing test mislabelled.
        implemented = set(census._resolve_scopes("all"))
        unimplemented = [
            label for label in _doctrine_scope_labels()
            if DOCTRINE_TO_SCOPE[label] not in implemented
        ]
        self.assertEqual(unimplemented, [], f"doctrine mandates but census omits: {unimplemented}")


if __name__ == "__main__":
    unittest.main()
