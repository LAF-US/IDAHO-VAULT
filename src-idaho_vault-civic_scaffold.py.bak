"""Bare-bones civic scaffold built from live operator machinery."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from idaho_vault.five_wizards.enums import (
    CouncilDomain,
    InstitutionId as RuntimeInstitutionId,
    LaneDomain,
)
from idaho_vault.operator_context import (
    BOOT_CHAIN_SURFACES,
    OPERATOR_FRONT_DOOR_SURFACES,
    OperatorContext,
    load_operator_context,
)


class StringEnum(str, Enum):
    """Compatibility helper for string-valued enums."""

    def __str__(self) -> str:
        return self.value


class StandingRank(StringEnum):
    """Conservative standing ranks for the first scaffold."""

    NOVICE = "novice"
    WITNESS = "witness"


class DistrictReadiness(StringEnum):
    """How honestly executable a district currently is."""

    DECLARED = "declared"
    SCAFFOLDED = "scaffolded"
    BLOCKED = "blocked"


class DistrictId(StringEnum):
    """Canonical hub-world districts for the first scaffold."""

    ROOT_AWAKENING = "root-awakening"
    ORIENTATION_HALL = "orientation-hall"
    FORGE = "forge"
    DOCKET = "docket"
    POST_ROOM = "post-room"
    SCRIBES_CHAMBER = "scribes-chamber"
    MACHINERY_FLOOR = "machinery-floor"


class DistrictKind(StringEnum):
    """Neutral district classification for the scaffold."""

    BOOT = "boot"
    ORIENTATION = "orientation"
    TRANSPORT = "transport"
    CASEWORK = "casework"
    INTAKE = "intake"
    RECORD = "record"
    MACHINERY = "machinery"

CIVIC_ENTITY_ID = "idaho-vault"
CIVIC_ENTITY_TITLE = "IDAHO-VAULT"
CIVIC_ENTITY_AUTHORITY = "LOGAN"
GOVERNANCE_SURFACES = ("CONSTITUTION.md", "DECISIONS.md", "VAULT-CONVENTIONS.md")
LOCAL_MACHINERY_REFS = (
    "src/idaho_vault/operator_context.py",
    "src/idaho_vault/bootstrap_contract.py",
    "src/idaho_vault/five_wizards/workflow.py",
    "src/idaho_vault/five_wizards/threshold_runner.py",
)
FIVE_WIZARDS_TITLE = "5Wizards' Council of Journalistic Inquiries"
FIVE_WIZARDS_RUNTIME_SURFACES = (
    "src/idaho_vault/five_wizards/workflow.py",
    "src/idaho_vault/five_wizards/service.py",
    "src/idaho_vault/five_wizards/staging.py",
    "src/idaho_vault/five_wizards/threshold_runner.py",
)

STAGING_SURFACE = "!/CREWAI/"


@dataclass(frozen=True)
class RouteDistrict:
    """One district in the bare-bones hub-world scaffold."""

    district_id: DistrictId
    title: str
    kind: DistrictKind
    readiness: DistrictReadiness
    locally_executable: bool
    surfaces: tuple[str, ...]
    institutions: tuple[str, ...] = ()
    requirements: tuple[str, ...] = ()
    missing_requirements: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the district."""

        return {
            "district_id": self.district_id.value,
            "title": self.title,
            "kind": self.kind.value,
            "readiness": self.readiness.value,
            "locally_executable": self.locally_executable,
            "surfaces": list(self.surfaces),
            "institutions": list(self.institutions),
            "requirements": list(self.requirements),
            "missing_requirements": list(self.missing_requirements),
        }


@dataclass(frozen=True)
class CivicEntitySetup:
    """Top-level civic entity contract for the scaffold."""

    entity_id: str
    title: str
    authority: str
    current_rank: StandingRank
    boot_chain_ok: bool
    operator_front_door_ok: bool
    governance_surfaces: tuple[str, ...]
    boot_chain_surfaces: tuple[str, ...]
    operator_front_door_surfaces: tuple[str, ...]
    staging_surface: str

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the civic entity setup."""

        return {
            "entity_id": self.entity_id,
            "title": self.title,
            "authority": self.authority,
            "current_rank": self.current_rank.value,
            "boot_chain_ok": self.boot_chain_ok,
            "operator_front_door_ok": self.operator_front_door_ok,
            "governance_surfaces": list(self.governance_surfaces),
            "boot_chain_surfaces": list(self.boot_chain_surfaces),
            "operator_front_door_surfaces": list(self.operator_front_door_surfaces),
            "staging_surface": self.staging_surface,
        }


class InstitutionKind(StringEnum):
    """High-level institution type mounted inside the civic entity."""

    COUNCIL = "council"


@dataclass(frozen=True)
class ResidentInstitution:
    """A concrete institution mounted inside the civic entity."""

    institution_id: str
    title: str
    kind: InstitutionKind
    readiness: DistrictReadiness
    locally_executable: bool
    authority: str
    home_districts: tuple[DistrictId, ...]
    runtime_surfaces: tuple[str, ...]
    lane_domains: tuple[str, ...] = ()
    council_domains: tuple[str, ...] = ()
    staging_surface: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the institution."""

        return {
            "institution_id": self.institution_id,
            "title": self.title,
            "kind": self.kind.value,
            "readiness": self.readiness.value,
            "locally_executable": self.locally_executable,
            "authority": self.authority,
            "home_districts": [district.value for district in self.home_districts],
            "runtime_surfaces": list(self.runtime_surfaces),
            "lane_domains": list(self.lane_domains),
            "council_domains": list(self.council_domains),
            "staging_surface": self.staging_surface,
        }


@dataclass(frozen=True)
class CivicScaffold:
    """Machine-readable civic scaffold derived from current repo truth."""

    root: Path
    entity: CivicEntitySetup
    institutions: tuple[ResidentInstitution, ...]
    districts: tuple[RouteDistrict, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the scaffold."""

        return {
            "root": str(self.root),
            "entity": self.entity.to_dict(),
            "institutions": [institution.to_dict() for institution in self.institutions],
            "districts": [district.to_dict() for district in self.districts],
        }

    def to_markdown(self) -> str:
        """Render a concise human-readable summary of the scaffold."""

        lines = [
            "# Civic Scaffold",
            "",
            "## Civic Entity",
            "",
            f"- Id: `{self.entity.entity_id}`",
            f"- Title: `{self.entity.title}`",
            f"- Authority: `{self.entity.authority}`",
            f"- Current rank: `{self.entity.current_rank.value}`",
            f"- Boot chain ok: `{'yes' if self.entity.boot_chain_ok else 'no'}`",
            (
                "- Operator front door ok: "
                f"`{'yes' if self.entity.operator_front_door_ok else 'no'}`"
            ),
            "- Governance surfaces: "
            + ", ".join(f"`{surface}`" for surface in self.entity.governance_surfaces),
            "- Staging surface: "
            + f"`{self.entity.staging_surface}`",
            "",
            "## Institutions",
            "",
        ]

        for institution in self.institutions:
            lines.extend(
                [
                    f"### {institution.title}",
                    "",
                    f"- Id: `{institution.institution_id}`",
                    f"- Kind: `{institution.kind.value}`",
                    f"- Readiness: `{institution.readiness.value}`",
                    f"- Local execution: `{'yes' if institution.locally_executable else 'no'}`",
                    f"- Authority: `{institution.authority}`",
                    "- Home districts: "
                    + ", ".join(f"`{district.value}`" for district in institution.home_districts),
                    "- Runtime surfaces: "
                    + ", ".join(f"`{surface}`" for surface in institution.runtime_surfaces),
                ]
            )
            if institution.lane_domains:
                lines.append(
                    "- Lane domains: "
                    + ", ".join(f"`{domain}`" for domain in institution.lane_domains)
                )
            if institution.council_domains:
                lines.append(
                    "- Council domains: "
                    + ", ".join(f"`{domain}`" for domain in institution.council_domains)
                )
            if institution.staging_surface is not None:
                lines.append(f"- Staging surface: `{institution.staging_surface}`")
            lines.extend(
                [
                    "",
                ]
            )

        lines.extend(
            [
                "",
                "## Districts",
                "",
            ]
        )

        for district in self.districts:
            lines.extend(
                [
                    f"### {district.title}",
                    "",
                    f"- Kind: `{district.kind.value}`",
                    f"- Readiness: `{district.readiness.value}`",
                    f"- Local execution: `{'yes' if district.locally_executable else 'no'}`",
                    f"- Surfaces: {', '.join(f'`{surface}`' for surface in district.surfaces)}",
                ]
            )
            if district.institutions:
                lines.append(
                    "- Institutions: "
                    + ", ".join(f"`{institution}`" for institution in district.institutions)
                )
            if district.requirements:
                lines.append(
                    "- Requirements: "
                    + ", ".join(f"`{surface}`" for surface in district.requirements)
                )
            if district.missing_requirements:
                lines.append(
                    "- Missing requirements: "
                    + ", ".join(f"`{surface}`" for surface in district.missing_requirements)
                )
            lines.append("")

        return "\n".join(lines).strip()


def _readiness_for_boot(context: OperatorContext) -> DistrictReadiness:
    return DistrictReadiness.SCAFFOLDED if context.boot_chain_ok else DistrictReadiness.BLOCKED


def _readiness_for_front_door(context: OperatorContext) -> DistrictReadiness:
    return (
        DistrictReadiness.SCAFFOLDED
        if context.operator_front_door_ok
        else DistrictReadiness.BLOCKED
    )


def _front_door_requirements(context: OperatorContext) -> tuple[str, ...]:
    return (*OPERATOR_FRONT_DOOR_SURFACES, context.daily_note_path)


def _readiness_for_local_institution(context: OperatorContext) -> DistrictReadiness:
    if context.boot_chain_ok and context.operator_front_door_ok:
        return DistrictReadiness.SCAFFOLDED
    return DistrictReadiness.BLOCKED


def _build_districts(context: OperatorContext) -> tuple[RouteDistrict, ...]:
    return (
        RouteDistrict(
            district_id=DistrictId.ROOT_AWAKENING,
            title="Root Awakening",
            kind=DistrictKind.BOOT,
            readiness=_readiness_for_boot(context),
            locally_executable=True,
            surfaces=BOOT_CHAIN_SURFACES,
            requirements=BOOT_CHAIN_SURFACES,
            missing_requirements=context.missing_boot_chain,
        ),
        RouteDistrict(
            district_id=DistrictId.ORIENTATION_HALL,
            title="Orientation Hall",
            kind=DistrictKind.ORIENTATION,
            readiness=_readiness_for_front_door(context),
            locally_executable=True,
            surfaces=_front_door_requirements(context),
            requirements=_front_door_requirements(context),
            missing_requirements=context.missing_operator_front_door,
        ),
        RouteDistrict(
            district_id=DistrictId.FORGE,
            title="Forge",
            kind=DistrictKind.TRANSPORT,
            readiness=_readiness_for_front_door(context),
            locally_executable=True,
            surfaces=(
                ".github/workflows/",
                "src/idaho_vault/five_wizards/threshold_runner.py",
                STAGING_SURFACE,
            ),
            institutions=(RuntimeInstitutionId.FIVE_WIZARDS.value,),
            requirements=_front_door_requirements(context),
            missing_requirements=context.missing_operator_front_door,
        ),
        RouteDistrict(
            district_id=DistrictId.DOCKET,
            title="Docket",
            kind=DistrictKind.CASEWORK,
            readiness=DistrictReadiness.DECLARED,
            locally_executable=False,
            surfaces=("Linear",),
        ),
        RouteDistrict(
            district_id=DistrictId.POST_ROOM,
            title="Post Room",
            kind=DistrictKind.INTAKE,
            readiness=DistrictReadiness.DECLARED,
            locally_executable=False,
            surfaces=("Gmail",),
        ),
        RouteDistrict(
            district_id=DistrictId.SCRIBES_CHAMBER,
            title="Scribe's Chamber",
            kind=DistrictKind.RECORD,
            readiness=_readiness_for_front_door(context),
            locally_executable=True,
            surfaces=("!/README.md", "!/AGENTS.md", "TO DO LIST.md", context.daily_note_path),
            institutions=(RuntimeInstitutionId.FIVE_WIZARDS.value,),
            requirements=_front_door_requirements(context),
            missing_requirements=context.missing_operator_front_door,
        ),
        RouteDistrict(
            district_id=DistrictId.MACHINERY_FLOOR,
            title="Machinery Floor",
            kind=DistrictKind.MACHINERY,
            readiness=_readiness_for_boot(context),
            locally_executable=True,
            surfaces=LOCAL_MACHINERY_REFS,
            institutions=(RuntimeInstitutionId.FIVE_WIZARDS.value,),
            requirements=BOOT_CHAIN_SURFACES,
            missing_requirements=context.missing_boot_chain,
        ),
    )


def _build_entity_setup(context: OperatorContext) -> CivicEntitySetup:
    current_rank = (
        StandingRank.WITNESS if context.operator_front_door_ok else StandingRank.NOVICE
    )
    return CivicEntitySetup(
        entity_id=CIVIC_ENTITY_ID,
        title=CIVIC_ENTITY_TITLE,
        authority=CIVIC_ENTITY_AUTHORITY,
        current_rank=current_rank,
        boot_chain_ok=context.boot_chain_ok,
        operator_front_door_ok=context.operator_front_door_ok,
        governance_surfaces=GOVERNANCE_SURFACES,
        boot_chain_surfaces=BOOT_CHAIN_SURFACES,
        operator_front_door_surfaces=_front_door_requirements(context),
        staging_surface=STAGING_SURFACE,
    )


def _build_institutions(context: OperatorContext) -> tuple[ResidentInstitution, ...]:
    return (
        ResidentInstitution(
            institution_id=RuntimeInstitutionId.FIVE_WIZARDS.value,
            title=FIVE_WIZARDS_TITLE,
            kind=InstitutionKind.COUNCIL,
            readiness=_readiness_for_local_institution(context),
            locally_executable=True,
            authority=CIVIC_ENTITY_AUTHORITY,
            home_districts=(
                DistrictId.FORGE,
                DistrictId.SCRIBES_CHAMBER,
                DistrictId.MACHINERY_FLOOR,
            ),
            runtime_surfaces=FIVE_WIZARDS_RUNTIME_SURFACES,
            lane_domains=tuple(domain.value for domain in LaneDomain),
            council_domains=(CouncilDomain.HOW.value,),
            staging_surface=STAGING_SURFACE,
        ),
    )


def build_civic_scaffold(
    context: OperatorContext | None = None,
) -> CivicScaffold:
    """Build a thin civic scaffold from the current operator context."""

    resolved_context = context or load_operator_context()

    return CivicScaffold(
        root=resolved_context.root,
        entity=_build_entity_setup(resolved_context),
        institutions=_build_institutions(resolved_context),
        districts=_build_districts(resolved_context),
    )


def render_civic_scaffold_markdown(scaffold: CivicScaffold) -> str:
    """Render a scaffold as markdown."""

    return scaffold.to_markdown()
