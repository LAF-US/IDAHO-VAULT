"""Bare-bones civic-fantasy scaffold built from live operator machinery."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

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


PACKET_REFS = (
    "!/STUDIO-PACKET-SYNTHESIS-CIVIC-FANTASY-2026-04-17.md",
    "!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md",
    "!/HUB-WORLD-ROUTE-MAP-2026-04-17.md",
    "!/CIVIC-LAW-AND-VAULTED-SYNTAX-2026-04-17.md",
)

LOCAL_MACHINERY_REFS = (
    "src/idaho_vault/operator_context.py",
    "src/idaho_vault/bootstrap_contract.py",
    "src/idaho_vault/five_wizards/workflow.py",
    "src/idaho_vault/five_wizards/threshold_runner.py",
)

COMMON_LOOP = (
    "awakening at root -> orientation through live surfaces -> entry into a district -> "
    "threshold trial -> truthful artifact -> return to center -> Logan decides "
    "promotion, staging, deferment, burial, or merge"
)

STAGING_SURFACE = "!/CREWAI/"


@dataclass(frozen=True)
class RouteDistrict:
    """One district in the bare-bones hub-world scaffold."""

    district_id: DistrictId
    title: str
    readiness: DistrictReadiness
    lesson: str
    artifact: str
    return_condition: str
    surfaces: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the district."""

        return {
            "district_id": self.district_id.value,
            "title": self.title,
            "readiness": self.readiness.value,
            "lesson": self.lesson,
            "artifact": self.artifact,
            "return_condition": self.return_condition,
            "surfaces": list(self.surfaces),
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class CivicScaffold:
    """Machine-readable civic-fantasy scaffold derived from current repo truth."""

    root: Path
    current_rank: StandingRank
    boot_chain_ok: bool
    operator_front_door_ok: bool
    staging_surface: str
    common_loop: str
    packet_refs: tuple[str, ...]
    local_machinery_refs: tuple[str, ...]
    districts: tuple[RouteDistrict, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation of the scaffold."""

        return {
            "root": str(self.root),
            "current_rank": self.current_rank.value,
            "boot_chain_ok": self.boot_chain_ok,
            "operator_front_door_ok": self.operator_front_door_ok,
            "staging_surface": self.staging_surface,
            "common_loop": self.common_loop,
            "packet_refs": list(self.packet_refs),
            "local_machinery_refs": list(self.local_machinery_refs),
            "districts": [district.to_dict() for district in self.districts],
        }

    def to_markdown(self) -> str:
        """Render a concise human-readable summary of the scaffold."""

        lines = [
            "# Civic Scaffold",
            "",
            f"- Current rank: `{self.current_rank.value}`",
            f"- Boot chain ok: `{'yes' if self.boot_chain_ok else 'no'}`",
            f"- Operator front door ok: `{'yes' if self.operator_front_door_ok else 'no'}`",
            f"- Staging surface: `{self.staging_surface}`",
            "",
            "## Common Loop",
            "",
            self.common_loop,
            "",
            "## Districts",
            "",
        ]

        for district in self.districts:
            lines.extend(
                [
                    f"### {district.title}",
                    "",
                    f"- Readiness: `{district.readiness.value}`",
                    f"- Lesson: {district.lesson}",
                    f"- Artifact: {district.artifact}",
                    f"- Return condition: {district.return_condition}",
                    f"- Surfaces: {', '.join(f'`{surface}`' for surface in district.surfaces)}",
                ]
            )
            if district.notes:
                lines.append(f"- Notes: {' '.join(district.notes)}")
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


def _missing_clause(prefix: str, missing: tuple[str, ...]) -> str:
    if not missing:
        return prefix
    return f"{prefix} Missing: {', '.join(missing)}."


def _build_districts(context: OperatorContext) -> tuple[RouteDistrict, ...]:
    return (
        RouteDistrict(
            district_id=DistrictId.ROOT_AWAKENING,
            title="Spawn / Root Awakening",
            readiness=_readiness_for_boot(context),
            lesson="You wake with little legitimacy and must identify the live boot chain.",
            artifact="first witness",
            return_condition="Identify live startup surfaces instead of following noise.",
            surfaces=BOOT_CHAIN_SURFACES,
            notes=(
                _missing_clause(
                    "This district is grounded in the canonical boot chain.",
                    context.missing_boot_chain,
                ),
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.ORIENTATION_HALL,
            title="Orientation Hall",
            readiness=_readiness_for_front_door(context),
            lesson="Surfaces are not equal; doctrine, front door, staging, and residue differ.",
            artifact="classified hall read",
            return_condition="Name what is live, what is staged, and what merely shouts.",
            surfaces=(*OPERATOR_FRONT_DOOR_SURFACES, context.daily_note_path),
            notes=(
                _missing_clause(
                    "This district depends on the operator front door staying truthful.",
                    context.missing_operator_front_door,
                ),
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.FORGE,
            title="Forge",
            readiness=_readiness_for_front_door(context),
            lesson="Transport is not promotion; branching and staging still return for judgment.",
            artifact="lawful PR-ready seam",
            return_condition="Stage work and return without self-merging in spirit.",
            surfaces=(
                ".github/workflows/",
                "src/idaho_vault/five_wizards/threshold_runner.py",
                STAGING_SURFACE,
            ),
            notes=(
                "Uses existing repo automation and the singular `!/CREWAI/` staging surface.",
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.DOCKET,
            title="Docket",
            readiness=DistrictReadiness.DECLARED,
            lesson="Work has status, queue, precedence, and unresolved consequence.",
            artifact="issue state witness",
            return_condition="Report state truthfully instead of overstating closure.",
            surfaces=("Linear",),
            notes=(
                "Declared as a district by the packet, but not claimed as locally executable by this scaffold.",
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.POST_ROOM,
            title="Post Room",
            readiness=DistrictReadiness.DECLARED,
            lesson="Not all incoming signal deserves inward consequence; triage matters.",
            artifact="intake brief",
            return_condition="Separate urgency from mere loudness.",
            surfaces=("Gmail",),
            notes=(
                "Declared as a district by the packet, but not claimed as locally executable by this scaffold.",
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.SCRIBES_CHAMBER,
            title="Scribe's Chamber",
            readiness=_readiness_for_front_door(context),
            lesson="Witness belongs beside the record; adjacency is part of truthfulness.",
            artifact="witness note",
            return_condition="Write clearly without collapsing source and interpretation.",
            surfaces=("!/README.md", "!/AGENTS.md", "TO DO LIST.md", context.daily_note_path),
            notes=(
                "This district is already supported by the live root and operator-note surfaces.",
            ),
        ),
        RouteDistrict(
            district_id=DistrictId.MACHINERY_FLOOR,
            title="Workshop / Machinery Floor",
            readiness=_readiness_for_boot(context),
            lesson="Procedural fluency is not sanction; machinery must remain bounded by doctrine.",
            artifact="machine-readable report",
            return_condition="Stop before consecration and hand off a legible mechanism.",
            surfaces=LOCAL_MACHINERY_REFS,
            notes=(
                "This is the first truthful implementation seam for the packet.",
            ),
        ),
    )


def build_civic_scaffold(
    context: OperatorContext | None = None,
) -> CivicScaffold:
    """Build a thin civic-fantasy scaffold from the current operator context."""

    resolved_context = context or load_operator_context()
    current_rank = (
        StandingRank.WITNESS if resolved_context.operator_front_door_ok else StandingRank.NOVICE
    )

    return CivicScaffold(
        root=resolved_context.root,
        current_rank=current_rank,
        boot_chain_ok=resolved_context.boot_chain_ok,
        operator_front_door_ok=resolved_context.operator_front_door_ok,
        staging_surface=STAGING_SURFACE,
        common_loop=COMMON_LOOP,
        packet_refs=PACKET_REFS,
        local_machinery_refs=LOCAL_MACHINERY_REFS,
        districts=_build_districts(resolved_context),
    )


def render_civic_scaffold_markdown(scaffold: CivicScaffold) -> str:
    """Render a scaffold as markdown."""

    return scaffold.to_markdown()
