from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def _load_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_character_conformity.py"
    spec = importlib.util.spec_from_file_location("character_conformity_test_module", script_path)
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


if __name__ == "__main__":
    unittest.main()
