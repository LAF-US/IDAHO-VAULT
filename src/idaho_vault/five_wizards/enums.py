"""Enums and canonical mappings for the 5Wizards schema foundation."""

from __future__ import annotations

from enum import Enum


class StringEnum(str, Enum):
    """Compatibility helper for string-valued enums."""

    def __str__(self) -> str:
        return self.value


class LaneDomain(StringEnum):
    WHO = "WHO"
    WHAT = "WHAT"
    WHEN = "WHEN"
    WHERE = "WHERE"
    WHY = "WHY"


class CouncilDomain(StringEnum):
    HOW = "HOW"


class CharacterId(StringEnum):
    WHO = "WHO"
    WHAT = "WHAT"
    WHEN = "WHEN"
    WHERE = "WHERE"
    WHY_HOW = "WHY_HOW"


class CharacterMode(StringEnum):
    LANE = "LANE"
    COUNCIL = "COUNCIL"


class FamiliarId(StringEnum):
    THOU = "THOU"
    THAT = "THAT"
    THEN = "THEN"
    THERE = "THERE"
    THY_THE = "THY_THE"


class FamiliarMode(StringEnum):
    THY = "THY"
    THE = "THE"


class AnchorType(StringEnum):
    THOU = "THOU"
    THAT = "THAT"
    THEN = "THEN"
    THERE = "THERE"
    THY = "THY"
    THE = "THE"


class ClaimConfidence(StringEnum):
    GROUNDED = "grounded"
    PROBABLE = "probable"
    TENTATIVE = "tentative"


class ClaimStatus(StringEnum):
    PROPOSED = "proposed"
    PASS = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"
    DISPUTED = "disputed"


class ObjectionSeverity(StringEnum):
    NOTE = "note"
    CONCERN = "concern"
    FATAL = "fatal"


class ObjectionStatus(StringEnum):
    OPEN = "open"
    ADDRESSED = "addressed"
    UPHELD = "upheld"
    OVERRULED = "overruled"


class ObjectionScope(StringEnum):
    LANE = "lane"
    COUNCIL = "council"


class MirageCategory(StringEnum):
    MISSING_ANCHOR = "missing-anchor"
    MISSING_EVIDENCE = "missing-evidence"
    CONTRADICTORY_EVIDENCE = "contradictory-evidence"
    OVERREACH = "overreach"
    FABRICATED_ENTITY = "fabricated-entity"
    FABRICATED_CAUSATION = "fabricated-causation"
    FABRICATED_PROCESS = "fabricated-process"
    TEMPORAL_IMPRECISION = "temporal-imprecision"
    SPATIAL_IMPRECISION = "spatial-imprecision"


class GateState(StringEnum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class NoteAuthorKind(StringEnum):
    WIZARD = "wizard"
    FAMILIAR = "familiar"


class NoteVisibility(StringEnum):
    PAIR_PRIVATE = "pair-private"
    INCLUDED_IN_FINAL = "included-in-final"


class CouncilReportStatus(StringEnum):
    DRAFT = "draft"
    CHALLENGED = "challenged"
    FINALIZED = "finalized"


class CouncilSessionStatus(StringEnum):
    AWAKENED = "awakened"
    CONVENED = "convened"
    DEBATING = "debating"
    ADJOURNED = "adjourned"


LANE_TO_CHARACTER: dict[LaneDomain, CharacterId] = {
    LaneDomain.WHO: CharacterId.WHO,
    LaneDomain.WHAT: CharacterId.WHAT,
    LaneDomain.WHEN: CharacterId.WHEN,
    LaneDomain.WHERE: CharacterId.WHERE,
    LaneDomain.WHY: CharacterId.WHY_HOW,
}

LANE_TO_FAMILIAR: dict[LaneDomain, FamiliarId] = {
    LaneDomain.WHO: FamiliarId.THOU,
    LaneDomain.WHAT: FamiliarId.THAT,
    LaneDomain.WHEN: FamiliarId.THEN,
    LaneDomain.WHERE: FamiliarId.THERE,
    LaneDomain.WHY: FamiliarId.THY_THE,
}

LANE_TO_FAMILIAR_MODE: dict[LaneDomain, FamiliarMode | None] = {
    LaneDomain.WHO: None,
    LaneDomain.WHAT: None,
    LaneDomain.WHEN: None,
    LaneDomain.WHERE: None,
    LaneDomain.WHY: FamiliarMode.THY,
}

LANE_TO_ANCHOR: dict[LaneDomain, AnchorType] = {
    LaneDomain.WHO: AnchorType.THOU,
    LaneDomain.WHAT: AnchorType.THAT,
    LaneDomain.WHEN: AnchorType.THEN,
    LaneDomain.WHERE: AnchorType.THERE,
    LaneDomain.WHY: AnchorType.THY,
}

COUNCIL_CHARACTER = CharacterId.WHY_HOW
COUNCIL_CHARACTER_MODE = CharacterMode.COUNCIL
COUNCIL_FAMILIAR = FamiliarId.THY_THE
COUNCIL_FAMILIAR_MODE = FamiliarMode.THE
COUNCIL_ANCHOR = AnchorType.THE

LANE_TO_INQUIRY_PROMPT: dict[LaneDomain, str] = {
    LaneDomain.WHO: "Who is present, absent, acting, named, or still unresolved here?",
    LaneDomain.WHAT: "What is being claimed, described, built, changed, or evidenced here?",
    LaneDomain.WHEN: "When does this happen, in what sequence, and with what temporal uncertainty?",
    LaneDomain.WHERE: "Where is this situated, crossed, routed, or left indeterminate?",
    LaneDomain.WHY: "Why does this matter, what motive or rationale is evidenced, and what remains unclear?",
}

COUNCIL_INQUIRY_PROMPT = (
    "How should the council hold method, caution, and relation together before finalizing?"
)


def lane_character(domain: LaneDomain) -> CharacterId:
    return LANE_TO_CHARACTER[domain]


def lane_familiar(domain: LaneDomain) -> FamiliarId:
    return LANE_TO_FAMILIAR[domain]


def lane_familiar_mode(domain: LaneDomain) -> FamiliarMode | None:
    return LANE_TO_FAMILIAR_MODE[domain]


def lane_anchor_type(domain: LaneDomain) -> AnchorType:
    return LANE_TO_ANCHOR[domain]


def familiar_label(familiar: FamiliarId, familiar_mode: FamiliarMode | None = None) -> str:
    if familiar is FamiliarId.THY_THE and familiar_mode is not None:
        return f"{familiar.value}[{familiar_mode.value}]"
    return familiar.value


def lane_inquiry_prompt(domain: LaneDomain) -> str:
    return LANE_TO_INQUIRY_PROMPT[domain]
