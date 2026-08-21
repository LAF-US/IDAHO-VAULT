"""Tests for the dotfolder tri-anchor guard (check_dotfolder_anchors).

Covers the discrimination the guard exists to make: a chamber that carries a
real payload versus one that is declared vacant by a `stub.txt` sentinel.

The case that matters is the BYTE comparison. `STUB-PERSONAFOLDERS-2026-05-03`
fixes the sentinel at `¿!?` and the guard compares `read_bytes()` against
`STUB_CONTENT` exactly. The module's own note records why: 306 of the vault's
stubs were already those four bytes and 18 carried a stray trailing newline, so
an `endswith` or `strip()` comparison would have ratified the drift instead of
catching it. A test that only checks "a stub exists" would pass against either
comparison and so would not defend the rule at all — the trailing-newline case
below is the one that separates them.

The fixtures build a whole throwaway repository and run the script inside it.
`ROOT` is derived from the script's own location (`parents[2]`), so copying the
script into `<tmp>/.github/scripts/` makes `<tmp>` the repository under test —
no monkeypatching of module state, and `main()` runs end to end including the
`git ls-tree HEAD` enumeration and the exit code. The enumeration is why each
fixture is a real git repo with a real commit: an untracked dotfolder is
invisible to the guard, which is itself part of the contract.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_dotfolder_anchors as guard  # noqa: E402

SCRIPT = Path(__file__).with_name("check_dotfolder_anchors.py")


class ExpectedAnchorNameTest(unittest.TestCase):
    """`.foo` -> `FOO.md`, stripping exactly one leading dot."""

    def test_single_leading_dot_is_stripped(self):
        self.assertEqual(guard.expected_anchor_name(".claude"), "CLAUDE.md")
        self.assertEqual(guard.expected_anchor_name(".circleci"), "CIRCLECI.md")

    def test_further_dots_stay_significant(self):
        # Only the first dot is the dotfolder marker; the rest belong to the
        # name and must survive into the anchor, or two distinct chambers
        # could collapse onto one expected anchor.
        self.assertEqual(guard.expected_anchor_name(".well.known"), "WELL.KNOWN.md")


class StubSentinelContractTest(unittest.TestCase):
    """The sentinel is four exact bytes — not 'starts with', not 'stripped'."""

    def test_sentinel_is_exactly_the_four_bytes(self):
        self.assertEqual(guard.STUB_CONTENT, b"\xc2\xbf\x21\x3f")
        self.assertEqual(len(guard.STUB_CONTENT), 4)
        self.assertEqual(guard.STUB_CONTENT.decode("utf-8"), "¿!?")

    def test_trailing_newline_is_not_the_sentinel(self):
        # The precise drift the guard was written to reject. Asserted here as
        # a bare inequality so it holds regardless of how main() reports it.
        self.assertNotEqual(guard.STUB_CONTENT + b"\n", guard.STUB_CONTENT)


class GuardFixture(unittest.TestCase):
    """A temporary git repository containing a copy of the guard."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="anchorguard-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / ".github" / "scripts").mkdir(parents=True)
        shutil.copy(SCRIPT, self.root / ".github" / "scripts" / SCRIPT.name)
        # `.github` is itself a tracked top-level dotfolder, so the guard holds
        # it to the same tri-anchor rule as any chamber. Anchor it here so each
        # test asserts against the chamber it actually built, not against the
        # harness's own scaffolding.
        self.chamber(".github")

    def write(self, rel: str, data: bytes) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def chamber(self, name: str, *, anchor=True, stub=b"\xc2\xbf\x21\x3f", root_anchor=True):
        """Build one dotfolder chamber. `stub=None` omits the sentinel."""
        expected = guard.expected_anchor_name(name)
        if anchor:
            self.write(f"{name}/{expected}", b"---\ntitle: fixture\n---\n")
        else:
            # The chamber must still exist in the tree to be enumerated.
            self.write(f"{name}/placeholder.md", b"fixture\n")
        if stub is not None:
            self.write(f"{name}/stub.txt", stub)
        if root_anchor:
            self.write(expected, b"---\ntitle: fixture root anchor\n---\n")

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=self.root, check=True,
            capture_output=True, text=True, timeout=60,
        )

    def commit(self) -> None:
        self._git("init", "-q")
        self._git("add", "-A")
        self._git(
            "-c", "user.email=fixture@example.invalid", "-c", "user.name=fixture",
            "commit", "-q", "-m", "fixture",
        )

    def run_guard(self) -> tuple[int, str]:
        """(exit code, the whole stderr). stderr is returned intact, never
        filtered: selecting only lines that match an expected shape would let a
        traceback register as 'no findings' — output silently reclassified as
        safe because a pattern did not match it."""
        result = subprocess.run(
            [sys.executable, str(self.root / ".github" / "scripts" / SCRIPT.name)],
            cwd=self.root, capture_output=True, text=True, timeout=60, check=False,
        )
        return result.returncode, result.stdout + result.stderr


class VacancySentinelTest(GuardFixture):
    """ENTITY-RUNTIME payload vs. the stub.txt vacancy sentinel."""

    def test_conforming_chamber_passes(self):
        self.chamber(".fixture")
        self.commit()
        code, out = self.run_guard()
        self.assertEqual(code, 0, out)

    def test_missing_sentinel_fails(self):
        # A chamber with an anchor but no sentinel is neither occupied-and-
        # declared nor declared-vacant; the guard must not pass it.
        self.chamber(".fixture", stub=None)
        self.commit()
        code, out = self.run_guard()
        self.assertEqual(code, 1, out)
        self.assertIn("stub.txt", out)

    def test_sentinel_with_trailing_newline_fails(self):
        # THE case. An `endswith`/`strip()` comparison would pass this and
        # ratify the 18 drifted stubs the module note records.
        self.chamber(".fixture", stub=b"\xc2\xbf\x21\x3f\n")
        self.commit()
        code, out = self.run_guard()
        self.assertEqual(code, 1, out)

    def test_empty_sentinel_fails(self):
        self.chamber(".fixture", stub=b"")
        self.commit()
        code, out = self.run_guard()
        self.assertEqual(code, 1, out)

    def test_missing_chamber_anchor_fails(self):
        self.chamber(".fixture", anchor=False)
        self.commit()
        code, out = self.run_guard()
        self.assertEqual(code, 1, out)

    def test_untracked_chamber_is_not_enumerated(self):
        # Enumeration is `git ls-tree HEAD`, so an uncommitted chamber is
        # invisible. Pinned deliberately: it is the contract that lets a
        # working tree hold scratch dotfolders without failing the guard.
        self.chamber(".tracked")
        self.commit()
        self.chamber(".untracked", stub=b"wrong bytes")
        code, out = self.run_guard()
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
