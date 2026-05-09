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
    CIVIC_ENTITY_AUTHORITY,
    CIVIC_ENTITY_ID,
    CIVIC_ENTITY_TITLE,
    FIVE_WIZARDS_TITLE,
    GOVERNANCE_SURFACES,
    STAGING_SURFACE,
    DistrictId,
    DistrictKind,
    DistrictReadiness,
    InstitutionKind,
    StandingRank,
    build_civic_scaffold,
    render_civic_scaffold_markdown,
)
from idaho_vault.five_wizards.enums import CouncilDomain, InstitutionId as RuntimeInstitutionId
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
        institution_map = {
            institution.institution_id: institution for institution in scaffold.institutions
        }

        self.assertEqual(scaffold.entity.entity_id, CIVIC_ENTITY_ID)
        self.assertEqual(scaffold.entity.title, CIVIC_ENTITY_TITLE)
        self.assertEqual(scaffold.entity.authority, CIVIC_ENTITY_AUTHORITY)
        self.assertEqual(scaffold.entity.current_rank, StandingRank.WITNESS)
        self.assertTrue(scaffold.entity.boot_chain_ok)
        self.assertTrue(scaffold.entity.operator_front_door_ok)
        self.assertEqual(scaffold.entity.governance_surfaces, GOVERNANCE_SURFACES)
        self.assertEqual(scaffold.entity.staging_surface, STAGING_SURFACE)
        self.assertEqual(
            institution_map[RuntimeInstitutionId.FIVE_WIZARDS.value].title,
            FIVE_WIZARDS_TITLE,
        )
        self.assertEqual(
            institution_map[RuntimeInstitutionId.FIVE_WIZARDS.value].kind,
            InstitutionKind.COUNCIL,
        )
        self.assertEqual(
            institution_map[RuntimeInstitutionId.FIVE_WIZARDS.value].council_domains,
            (CouncilDomain.HOW.value,),
        )
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
        self.assertEqual(
            district_map[DistrictId.FORGE].kind,
            DistrictKind.TRANSPORT,
        )
        self.assertFalse(district_map[DistrictId.DOCKET].locally_executable)
        self.assertIn("2026-04-17.md", district_map[DistrictId.ORIENTATION_HALL].surfaces)
        self.assertEqual(
            district_map[DistrictId.FORGE].institutions,
            (RuntimeInstitutionId.FIVE_WIZARDS.value,),
        )
        self.assertEqual(
            district_map[DistrictId.ORIENTATION_HALL].missing_requirements,
            (),
        )

        markdown = render_civic_scaffold_markdown(scaffold)
        self.assertIn("# Civic Scaffold", markdown)
        self.assertIn("## Civic Entity", markdown)
        self.assertIn("## Institutions", markdown)
        self.assertIn(CIVIC_ENTITY_TITLE, markdown)
        self.assertIn(FIVE_WIZARDS_TITLE, markdown)
        self.assertIn(STAGING_SURFACE, markdown)
        self.assertIn("Root Awakening", markdown)
        self.assertIn("- Kind: `transport`", markdown)
        self.assertNotIn("- Lesson:", markdown)

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
        institution_map = {
            institution.institution_id: institution for institution in scaffold.institutions
        }

        self.assertEqual(scaffold.entity.current_rank, StandingRank.NOVICE)
        self.assertTrue(scaffold.entity.boot_chain_ok)
        self.assertFalse(scaffold.entity.operator_front_door_ok)
        self.assertEqual(
            institution_map[RuntimeInstitutionId.FIVE_WIZARDS.value].readiness,
            DistrictReadiness.BLOCKED,
        )
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
        self.assertIn("2026-04-17.md", district_map[DistrictId.FORGE].missing_requirements)


if __name__ == "__main__":
    unittest.main()
