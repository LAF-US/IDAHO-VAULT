from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_character_conformity.py"
    spec = importlib.util.spec_from_file_location("character_conformity_test_module", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()

TEXT = {"text": "set"}


class GateClassificationTest(unittest.TestCase):
    def test_lfs_filtered_file_is_binary(self) -> None:
        self.assertEqual(checker.classify({"text": "unspecified", "filter": "lfs"}, b"data"), "binary")

    def test_text_unset_is_binary(self) -> None:
        # `*.csv -text` in .gitattributes is a deliberate not-text declaration.
        self.assertEqual(checker.classify({"text": "unset", "filter": "unspecified"}, b"a,b\n"), "binary")

    def test_unspecified_extension_is_undeclared_not_judged(self) -> None:
        self.assertEqual(checker.classify({"text": "unspecified", "filter": "unspecified"}, b"\x97"), "undeclared")

    def test_declared_text_with_nul_is_ambiguous(self) -> None:
        self.assertEqual(checker.classify(TEXT, b"looks like text\x00but has NUL"), "ambiguous")

    def test_utf16_bom_is_text_in_wrong_encoding_not_ambiguous(self) -> None:
        # NUL bytes are what UTF-16 looks like; the BOM declares the charset.
        data = b"\xff\xfe" + "Rollover".encode("utf-16-le")
        self.assertEqual(checker.classify(TEXT, data), "text")

    def test_nul_beyond_probe_window_stays_text(self) -> None:
        data = b"a" * checker.NUL_PROBE_BYTES + b"\x00"
        self.assertEqual(checker.classify(TEXT, data), "text")

    def test_declared_text_without_nul_is_text(self) -> None:
        self.assertEqual(checker.classify(TEXT, "plain — prose".encode("utf-8")), "text")


class PathContainmentTest(unittest.TestCase):
    def test_repo_relative_path_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "note.md").write_bytes(b"x")
            self.assertEqual(checker.contained_path(root, "note.md"), root / "note.md")

    def test_traversal_and_absolute_paths_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.assertIsNone(checker.contained_path(root, "../outside.md"))
            self.assertIsNone(checker.contained_path(root, "/etc/hostname"))
            self.assertIsNone(checker.contained_path(root, "a/../../outside.md"))

    def test_symlink_escaping_root_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            root = Path(tmp).resolve()
            outside = Path(other).resolve() / "target.md"
            outside.write_bytes(b"x")
            (root / "link.md").symlink_to(outside)
            self.assertIsNone(checker.contained_path(root, "link.md"))


class EncodingFindingsTest(unittest.TestCase):
    def test_valid_utf8_typography_is_clean(self) -> None:
        # The vault's style is em-dash-heavy; as UTF-8 codepoints they conform.
        data = "em-dash — curly ‘quotes’ ¿inverted?".encode("utf-8")
        self.assertEqual(checker.encoding_findings("note.md", data), [])

    def test_leading_bom_is_tolerated_not_flagged(self) -> None:
        # N1 is "BOM-aware UTF-8": a single leading BOM is recognized, not an offense.
        data = checker.UTF8_BOM + "hello".encode("utf-8")
        self.assertEqual(checker.encoding_findings("note.md", data), [])

    def test_cp1252_em_dash_byte_is_flagged_with_gloss(self) -> None:
        # The CHAMBER.md fingerprint: cp1252 0x97 where UTF-8 E2 80 94 was meant.
        findings = checker.encoding_findings("CHAMBER.md", b"anchor \x97 voice")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].kind, "encoding")
        self.assertIn("97", findings[0].detail)
        self.assertIn("—", findings[0].detail)

    def test_utf16le_bom_file_is_flagged_as_wrong_encoding(self) -> None:
        data = b"\xff\xfe" + "log line".encode("utf-16-le")
        findings = checker.encoding_findings("SyncLog.txt", data)
        self.assertEqual(len(findings), 1)
        self.assertIn("UTF-16LE", findings[0].detail)

    def test_latin1_inverted_question_byte_is_flagged(self) -> None:
        # The stub.txt fingerprint: a leading 0xBF (¿) byte.
        findings = checker.encoding_findings("stub.txt", b"\xbfwildcard?")
        self.assertEqual(len(findings), 1)
        self.assertIn("bf", findings[0].detail)


def _garble(text: str) -> str:
    """Produce the double-decode artifact of text (UTF-8 bytes read as cp1252)."""
    return text.encode("utf-8").decode("cp1252")


class MojibakeRepairTest(unittest.TestCase):
    def test_em_dash_artifact_is_repaired(self) -> None:
        fixed, count = checker.apply_mojibake_repairs(f"before {_garble('—')} after")
        self.assertEqual(fixed, "before — after")
        self.assertEqual(count, 1)

    def test_e_acute_artifact_is_repaired(self) -> None:
        fixed, count = checker.apply_mojibake_repairs(f"caf{_garble('é')} bar")
        self.assertEqual(fixed, "café bar")
        self.assertEqual(count, 1)

    def test_nbsp_artifact_is_repaired(self) -> None:
        fixed, count = checker.apply_mojibake_repairs(f"x{_garble(' ')}y")
        self.assertEqual(fixed, "x y")
        self.assertEqual(count, 1)

    def test_legitimate_accented_text_is_untouched(self) -> None:
        text = "café — déjà vu, naïve ¿verdad?"
        fixed, count = checker.apply_mojibake_repairs(text)
        self.assertEqual(fixed, text)
        self.assertEqual(count, 0)

    def test_partial_image_is_not_repaired(self) -> None:
        # 'â€"' with a plain ASCII quote is NOT a decodable byte image
        # (E2 80 22 is invalid UTF-8) — must be left alone, never guessed.
        text = 'broken â€" thing'
        fixed, count = checker.apply_mojibake_repairs(text)
        self.assertEqual(fixed, text)
        self.assertEqual(count, 0)

    def test_multi_generation_garble_is_fully_flattened(self) -> None:
        # Garbled twice (the Wikipedia Mojibake article's own demonstration:
        # £ -> its cp1252 image -> that image's image). One run must repair
        # all the way down, not leave a layer. Note not every character CAN
        # double-garble — an em-dash's second generation needs byte 9D,
        # undefined in cp1252 — which is why the fixture uses £ and é.
        twice = _garble(_garble("£ and é"))
        fixed, count = checker.apply_mojibake_repairs(twice)
        self.assertEqual(fixed, "£ and é")
        self.assertGreater(count, 0)

    def test_repair_is_idempotent(self) -> None:
        once, _ = checker.apply_mojibake_repairs(f"a {_garble('—')} b {_garble('é')} c")
        twice, count = checker.apply_mojibake_repairs(once)
        self.assertEqual(twice, once)
        self.assertEqual(count, 0)

    def test_every_repair_satisfies_roundtrip_proof(self) -> None:
        # Note: only artifacts that can exist are testable — e.g. '”' (U+201D,
        # UTF-8 ...9D) can never double-decode via cp1252 because byte 9D is
        # undefined there; a cp1252 writer would have crashed, not garbled.
        text = f"mix {_garble('“quoted')} and {_garble('…')} ends {_garble('naïve')}"
        for _s, _e, observed, repaired in checker.find_mojibake_repairs(text):
            self.assertEqual(repaired.encode("utf-8").decode("cp1252"), observed)


class HomoglyphRepairTest(unittest.TestCase):
    # Mixed-script specimens are built from escapes, never written literally:
    # a literal specimen in this file would be "repaired" by the very sweep
    # under test (it was, once) — the same self-reference rule as the program
    # document's byte-named examples.

    def test_cyrillic_e_inside_latin_word_is_repaired(self) -> None:
        # The #638 case: Cyrillic е (U+0435) posing as Latin e in a Latin word.
        specimen = "pr\u0435ss"
        repairs, flags = checker.find_homoglyph_repairs(f"the {specimen} release")
        self.assertEqual([(r[1], r[2]) for r in repairs], [(specimen, "press")])
        self.assertEqual(flags, [])

    def test_genuine_russian_text_is_untouched(self) -> None:
        # The vault is not English-only: single-script foreign words are
        # never candidates, whole sentences included.
        repairs, flags = checker.find_homoglyph_repairs("привет мир, это тест")
        self.assertEqual(repairs, [])
        self.assertEqual(flags, [])

    def test_latin_letter_inside_cyrillic_word_is_repaired_symmetrically(self) -> None:
        # Latin 'e' (U+0065) hiding inside an otherwise-Cyrillic word:
        # normalized toward Cyrillic, not toward Latin.
        specimen = "прив\u0065т"
        repairs, _flags = checker.find_homoglyph_repairs(f"он сказал {specimen} всем")
        self.assertEqual([(r[1], r[2]) for r in repairs], [(specimen, "привет")])

    def test_greek_prose_is_untouched(self) -> None:
        repairs, flags = checker.find_homoglyph_repairs("και το όνομα αυτής")
        self.assertEqual(repairs, [])
        self.assertEqual(flags, [])

    def test_mixed_but_unmappable_word_is_flagged_not_guessed(self) -> None:
        # Cyrillic ж (U+0436) has no Latin look-alike: a mixed-script word
        # that cannot be normalized to one script is flagged for human eyes.
        repairs, flags = checker.find_homoglyph_repairs("word\u0436")
        self.assertEqual(repairs, [])
        self.assertEqual(len(flags), 1)

    def test_correction_table_guard_pattern(self) -> None:
        # A dictionary row mapping a look-alike misspelling to its correction
        # must keep its key: the guard pattern in run_homoglyph_sweep matches
        # `| observed | repaired |` rows. Verified here at the pattern level.
        import re as _re
        specimen = "\u0441ontain"  # Cyrillic es + Latin tail, built from escape
        line = f"| {specimen} | contain |"
        self.assertTrue(
            _re.search(r"\|\s*" + _re.escape(specimen) + r"\s*\|\s*contain\s*\|", line)
        )
        prose = f"we {specimen} multitudes"
        self.assertFalse(
            _re.search(r"\|\s*" + _re.escape(specimen) + r"\s*\|\s*contain\s*\|", prose)
        )

    def test_repaired_word_is_single_script(self) -> None:
        repairs, _ = checker.find_homoglyph_repairs("t\u0435st \u0441\u0430se")
        self.assertTrue(repairs)
        for _off, _obs, fixed in repairs:
            scripts = {checker._script(c) for c in fixed}
            self.assertEqual(len(scripts), 1)


class SweepTest(unittest.TestCase):
    def test_pure_cp1252_file_is_reencoded_with_roundtrip_proof(self) -> None:
        original = b"dash \x97 ellipsis \x85 quote \x92"
        result, new = checker.sweep_file("CHAMBER.md", original)
        self.assertEqual(result.action, "reencoded")
        assert new is not None
        # The repaired bytes are valid UTF-8 and read as the intended text.
        self.assertEqual(new.decode("utf-8"), "dash — ellipsis … quote ’")
        # Reversibility: the repair is exactly the cp1252 reading, re-encoded.
        self.assertEqual(new.decode("utf-8").encode("cp1252"), original)

    def test_clean_utf8_file_is_left_alone(self) -> None:
        result, new = checker.sweep_file("note.md", "already — clean".encode("utf-8"))
        self.assertEqual(result.action, "skipped-clean")
        self.assertIsNone(new)

    def test_mixed_encoding_file_is_refused_not_guessed(self) -> None:
        # Valid UTF-8 em-dash AND a stray cp1252 byte: whole-file cp1252 decode
        # would mojibake the healthy sequence, so the sweeper must refuse.
        mixed = "healthy — text ".encode("utf-8") + b"\x97 stray"
        result, new = checker.sweep_file("mixed.md", mixed)
        self.assertEqual(result.action, "refused-mixed")
        self.assertIsNone(new)

    def test_byte_undefined_in_cp1252_is_refused(self) -> None:
        result, new = checker.sweep_file("odd.md", b"broken \x81 byte")
        self.assertEqual(result.action, "refused-undecodable")
        self.assertIsNone(new)

    def test_utf16le_bom_file_is_converted_with_roundtrip_proof(self) -> None:
        text = "Rollover report\r\nline two — done\r\n"
        original = b"\xff\xfe" + text.encode("utf-16-le")
        result, new = checker.sweep_file("dry_run.txt", original)
        self.assertEqual(result.action, "reencoded")
        assert new is not None
        self.assertEqual(new.decode("utf-8"), text)
        self.assertFalse(new.startswith(checker.UTF8_BOM))

    def test_truncated_utf16_is_refused(self) -> None:
        # Odd byte count after the BOM: strict decode fails; never guess.
        original = b"\xff\xfe" + "abc".encode("utf-16-le") + b"\x41"
        result, new = checker.sweep_file("bad.txt", original)
        self.assertEqual(result.action, "refused-undecodable")
        self.assertIsNone(new)

    def test_sweep_never_adds_a_bom(self) -> None:
        _, new = checker.sweep_file("note.md", b"\x97")
        assert new is not None
        self.assertFalse(new.startswith(checker.UTF8_BOM))


class RepoRootFailClosedTest(unittest.TestCase):
    def test_fails_closed_on_timeout(self) -> None:
        with patch.object(
            checker.subprocess, "run", side_effect=subprocess.TimeoutExpired(cmd="git", timeout=30)
        ):
            with self.assertRaises(SystemExit) as exc:
                checker.repo_root()
        self.assertIn("timed out", str(exc.exception))

    def test_fails_closed_when_git_missing(self) -> None:
        with patch.object(checker.subprocess, "run", side_effect=FileNotFoundError("git")):
            with self.assertRaises(SystemExit) as exc:
                checker.repo_root()
        self.assertIn("could not run", str(exc.exception))

    def test_fails_closed_on_nonzero_exit(self) -> None:
        error = subprocess.CalledProcessError(128, ["git", "rev-parse"], stderr="not a git repository")
        with patch.object(checker.subprocess, "run", side_effect=error):
            with self.assertRaises(SystemExit) as exc:
                checker.repo_root()
        self.assertIn("not a git repository", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
