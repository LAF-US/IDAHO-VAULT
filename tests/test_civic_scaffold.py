from __future__ import annotations

from datetime import date
import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.civic_scaffold import (
    COMMON_LOOP,
    PACKET_REFS,
    STAGING_SURFACE,
    DistrictId,
    DistrictReadiness,
    StandingRank,
    build_civic_scaffold,
    render_civic_scaffold_markdown,
)
from idaho_vault.operator_context import (
    BOOT_CHAIN_SURFACES,
    OPERATOR_FRONT_DOOR_SURFACES,
    load_operator_context,
)


class CivicScaffoldTest(unittest.TestCase):
    def _write_surface(self, root: Path, relpath: str) -> None:
        path = root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".json":
            if path.name == "daily-notes.json":
                path.write_text(
                    '{"template":"DAILY NOTE TEMPLATE","folder":""}',
                    encoding="utf-8",
                )
            elif path.name == "data.json":
                path.write_text(
                    (
                        '{"daily":{"format":"YYYY-MM-DD","template":"DAILY NOTE TEMPLATE",'
                        '"folder":"","enabled":true}}'
                    ),
                    encoding="utf-8",
                )
            else:
                path.write_text("{}", encoding="utf-8")
        else:
            path.write_text("placeholder", encoding="utf-8")

    def test_build_civic_scaffold_marks_local_districts_truthfully(self) -> None:
        root = PROJECT_ROOT / "tests" / "_tmp_civic_scaffold_case"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True, exist_ok=True)
        try:
            for relpath in (*BOOT_CHAIN_SURFACES, *OPERATOR_FRONT_DOOR_SURFACES):
                self._write_surface(root, relpath)

            (root / "2026-04-17.md").write_text("# daily note", encoding="utf-8")

            context = load_operator_context(root=root, target_date=date(2026, 4, 17))
            scaffold = build_civic_scaffold(context)
        finally:
            shutil.rmtree(root, ignore_errors=True)

        district_map = {district.district_id: district for district in scaffold.districts}

        self.assertEqual(scaffold.current_rank, StandingRank.WITNESS)
        self.assertTrue(scaffold.boot_chain_ok)
        self.assertTrue(scaffold.operator_front_door_ok)
        self.assertEqual(scaffold.staging_surface, STAGING_SURFACE)
        self.assertEqual(scaffold.common_loop, COMMON_LOOP)
        self.assertEqual(scaffold.packet_refs, PACKET_REFS)
        self.assertEqual(
            district_map[DistrictId.ROOT_AWAKENING].readiness,
            DistrictReadiness.SCAFFOLDED,
        )
        self.assertEqual(
            district_map[DistrictId.ORIENTATION_HALL].readiness,
            DistrictReadiness.SCAFFOLDED,
        )
        self.assertEqual(
            district_map[DistrictId.FORGE].readiness,
            DistrictReadiness.SCAFFOLDED,
        )
        self.assertEqual(
            district_map[DistrictId.DOCKET].readiness,
            DistrictReadiness.DECLARED,
        )
        self.assertEqual(
            district_map[DistrictId.POST_ROOM].readiness,
            DistrictReadiness.DECLARED,
        )
        self.assertIn("2026-04-17.md", district_map[DistrictId.ORIENTATION_HALL].surfaces)

        markdown = render_civic_scaffold_markdown(scaffold)
        self.assertIn("# Civic Scaffold", markdown)
        self.assertIn(STAGING_SURFACE, markdown)
        self.assertIn("Spawn / Root Awakening", markdown)

    def test_build_civic_scaffold_blocks_front_door_when_surfaces_are_missing(self) -> None:
        root = PROJECT_ROOT / "tests" / "_tmp_civic_scaffold_missing"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True, exist_ok=True)
        try:
            for relpath in BOOT_CHAIN_SURFACES:
                self._write_surface(root, relpath)

            context = load_operator_context(root=root, target_date=date(2026, 4, 17))
            scaffold = build_civic_scaffold(context)
        finally:
            shutil.rmtree(root, ignore_errors=True)

        district_map = {district.district_id: district for district in scaffold.districts}

        self.assertEqual(scaffold.current_rank, StandingRank.NOVICE)
        self.assertTrue(scaffold.boot_chain_ok)
        self.assertFalse(scaffold.operator_front_door_ok)
        self.assertEqual(
            district_map[DistrictId.ORIENTATION_HALL].readiness,
            DistrictReadiness.BLOCKED,
        )
        self.assertEqual(
            district_map[DistrictId.FORGE].readiness,
            DistrictReadiness.BLOCKED,
        )
        self.assertEqual(
            district_map[DistrictId.MACHINERY_FLOOR].readiness,
            DistrictReadiness.SCAFFOLDED,
        )


if __name__ == "__main__":
    unittest.main()
