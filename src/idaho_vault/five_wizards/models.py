"""Pydantic models for the 5Wizards schema foundation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.enums import (
    AnchorType,
    CharacterId,
    CharacterMode,
    ClaimConfidence,
    ClaimStatus,
    CouncilDomain,
    CouncilReportStatus,
    CouncilSessionStatus,
    FamiliarId,
    FamiliarMode,
    GateState,
    LaneDomain,
    NoteAuthorKind,
    NoteVisibility,
    ObjectionScope,
    ObjectionSeverity,
    ObjectionStatus,
    MirageCategory,
    LANE_TO_ANCHOR,
    LANE_TO_CHARACTER,
    LANE_TO_FAMILIAR,
    LANE_TO_FAMILIAR_MODE,
    LANE_TO_INQUIRY_PROMPT,
    COUNCIL_INQUIRY_PROMPT,
    COUNCIL_ANCHOR,
    COUNCIL_CHARACTER,
    COUNCIL_CHARACTER_MODE,
    COUNCIL_FAMILIAR,
    COUNCIL_FAMILIAR_MODE,
)


class WizardBaseModel(BaseModel):
    """Common base model with strict fields."""

    model_config = ConfigDict(extra="forbid")


class PersonalNote(WizardBaseModel):
    note_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    domain: LaneDomain
    author_kind: NoteAuthorKind
    character: CharacterId
    character_mode: CharacterMode
    familiar: FamiliarId
    familiar_mode: FamiliarMode | None = None
    text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    inquiry_question: str = Field(min_length=1)
    recurring_questions: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    unresolved_tensions: list[str] = Field(default_factory=list)
    visibility: NoteVisibility = NoteVisibility.PAIR_PRIVATE
    include_in_final_report: bool = True

    @model_validator(mode="after")
    def validate_note_mapping(self) -> "PersonalNote":
        if self.character is not LANE_TO_CHARACTER[self.domain]:
            raise ValueError("Personal note character does not match lane domain mapping.")
        if self.character_mode is not CharacterMode.LANE:
            raise ValueError("Personal notes must use `character_mode=LANE`.")
        if self.familiar is not LANE_TO_FAMILIAR[self.domain]:
            raise ValueError("Personal note familiar does not match lane domain mapping.")
        if self.familiar_mode != LANE_TO_FAMILIAR_MODE[self.domain]:
            raise ValueError("Personal note familiar mode does not match lane domain mapping.")
        if not self.inquiry_question.strip():
            raise ValueError("Personal notes require a current inquiry question.")
        return self


class Objection(WizardBaseModel):
    objection_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    target_claim_id: str = Field(min_length=1)
    scope: ObjectionScope
    lane_domain: LaneDomain | None = None
    council_domain: CouncilDomain | None = None
    character: CharacterId
    character_mode: CharacterMode
    familiar: FamiliarId
    familiar_mode: FamiliarMode | None = None
    severity: ObjectionSeverity
    category: MirageCategory
    text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    status: ObjectionStatus
    resolution_note: str | None = None

    @model_validator(mode="after")
    def validate_scope_mapping(self) -> "Objection":
        if self.scope is ObjectionScope.LANE:
            if self.lane_domain is None or self.council_domain is not None:
                raise ValueError("Lane objections require `lane_domain` and forbid `council_domain`.")
            if self.character is not LANE_TO_CHARACTER[self.lane_domain]:
                raise ValueError("Lane objection character does not match domain mapping.")
            if self.character_mode is not CharacterMode.LANE:
                raise ValueError("Lane objections require `character_mode=LANE`.")
            if self.familiar is not LANE_TO_FAMILIAR[self.lane_domain]:
                raise ValueError("Lane objection familiar does not match domain mapping.")
            if self.familiar_mode != LANE_TO_FAMILIAR_MODE[self.lane_domain]:
                raise ValueError("Lane objection familiar mode does not match domain mapping.")
        else:
            if self.council_domain is None or self.lane_domain is not None:
                raise ValueError("Council objections require `council_domain` and forbid `lane_domain`.")
            if self.council_domain is not CouncilDomain.HOW:
                raise ValueError("Council objections currently support only `HOW`.")
            if self.character is not COUNCIL_CHARACTER or self.character_mode is not COUNCIL_CHARACTER_MODE:
                raise ValueError("Council objections must use WHY_HOW in COUNCIL mode.")
            if self.familiar is not COUNCIL_FAMILIAR or self.familiar_mode is not COUNCIL_FAMILIAR_MODE:
                raise ValueError("Council objections must use THY_THE in THE mode.")
        return self


class Claim(WizardBaseModel):
    claim_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    domain: LaneDomain
    character: CharacterId
    character_mode: CharacterMode
    wizard_role: str = Field(min_length=1)
    familiar: FamiliarId
    familiar_mode: FamiliarMode | None = None
    text: str = Field(min_length=1)
    anchor_type: AnchorType
    anchor_value: str
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: ClaimConfidence
    status: ClaimStatus = ClaimStatus.PROPOSED
    objections: list[Objection] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_lane_mapping(self) -> "Claim":
        if self.character is not LANE_TO_CHARACTER[self.domain]:
            raise ValueError("Claim character does not match lane domain mapping.")
        if self.character_mode is not CharacterMode.LANE:
            raise ValueError("Claims must use `character_mode=LANE`.")
        if self.familiar is not LANE_TO_FAMILIAR[self.domain]:
            raise ValueError("Claim familiar does not match lane domain mapping.")
        if self.familiar_mode != LANE_TO_FAMILIAR_MODE[self.domain]:
            raise ValueError("Claim familiar mode does not match lane domain mapping.")
        if self.anchor_type is not LANE_TO_ANCHOR[self.domain]:
            raise ValueError("Claim anchor type does not match lane domain mapping.")
        for objection in self.objections:
            if objection.target_claim_id != self.claim_id:
                raise ValueError("Attached objections must target the current claim id.")
        return self


class CouncilReport(WizardBaseModel):
    report_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    domain: LaneDomain
    character: CharacterId
    character_mode: CharacterMode
    wizard_role: str = Field(min_length=1)
    familiar: FamiliarId
    familiar_mode: FamiliarMode | None = None
    status: CouncilReportStatus
    personal_note_ids: list[str] = Field(default_factory=list)
    challenge_objection_ids: list[str] = Field(default_factory=list)
    inquiry_question: str = Field(min_length=1)
    unresolved_questions: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    council_text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_report_mapping(self) -> "CouncilReport":
        if self.character is not LANE_TO_CHARACTER[self.domain]:
            raise ValueError("Council report character does not match lane domain mapping.")
        if self.character_mode is not CharacterMode.LANE:
            raise ValueError("Council reports remain wizard-owned lane artifacts.")
        if self.familiar is not LANE_TO_FAMILIAR[self.domain]:
            raise ValueError("Council report familiar does not match lane domain mapping.")
        if self.familiar_mode != LANE_TO_FAMILIAR_MODE[self.domain]:
            raise ValueError("Council report familiar mode does not match lane domain mapping.")
        if not self.inquiry_question.strip():
            raise ValueError("Council reports require a current inquiry question.")
        return self


class FamiliarGaggleNote(WizardBaseModel):
    note_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    council_domain: CouncilDomain
    host_character: CharacterId
    host_character_mode: CharacterMode
    host_familiar: FamiliarId
    host_familiar_mode: FamiliarMode
    participant_familiars: list[FamiliarId]
    participant_modes: list[FamiliarMode | None]
    watched_report_ids: list[str] = Field(default_factory=list)
    gossip_text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    include_in_final_report: bool = True

    @model_validator(mode="after")
    def validate_gaggle(self) -> "FamiliarGaggleNote":
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Familiar gaggle notes currently belong to the HOW council domain.")
        if self.host_character is not COUNCIL_CHARACTER or self.host_character_mode is not COUNCIL_CHARACTER_MODE:
            raise ValueError("Familiar gaggle notes must be hosted by WHY_HOW in COUNCIL mode.")
        if self.host_familiar is not COUNCIL_FAMILIAR or self.host_familiar_mode is not COUNCIL_FAMILIAR_MODE:
            raise ValueError("Familiar gaggle notes must use THY_THE in THE mode as host.")
        if len(self.participant_familiars) != len(self.participant_modes):
            raise ValueError("Participant familiars and modes must have the same length.")
        return self


class CouncilSession(WizardBaseModel):
    session_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    council_domain: CouncilDomain
    convener_character: CharacterId
    convener_character_mode: CharacterMode
    convener_familiar: FamiliarId
    convener_familiar_mode: FamiliarMode
    status: CouncilSessionStatus
    council_report_ids: list[str] = Field(default_factory=list)
    familiar_gaggle_note_ids: list[str] = Field(default_factory=list)
    inquiry_question: str = Field(min_length=1)
    debate_threads: list[str] = Field(default_factory=list)
    method_warnings: list[str] = Field(default_factory=list)
    debate_summary: str = Field(min_length=1)
    outcome_summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_session(self) -> "CouncilSession":
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Council sessions currently belong to the HOW council domain.")
        if self.convener_character is not COUNCIL_CHARACTER or self.convener_character_mode is not COUNCIL_CHARACTER_MODE:
            raise ValueError("Council sessions must be convened by WHY_HOW in COUNCIL mode.")
        if self.convener_familiar is not COUNCIL_FAMILIAR or self.convener_familiar_mode is not COUNCIL_FAMILIAR_MODE:
            raise ValueError("Council sessions must use THY_THE in THE mode as familiar host.")
        if not self.inquiry_question.strip():
            raise ValueError("Council sessions require the HOW inquiry question.")
        return self


class ValidationVerdict(WizardBaseModel):
    claim_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    domain: LaneDomain
    character: CharacterId
    character_mode: CharacterMode
    status: ClaimStatus
    reason: str = Field(min_length=1)
    mirage_categories: list[MirageCategory] = Field(default_factory=list)
    blocking_objection_ids: list[str] = Field(default_factory=list)
    accepted_evidence_refs: list[str] = Field(default_factory=list)
    validator: str = Field(min_length=1)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_verdict_mapping(self) -> "ValidationVerdict":
        if self.character is not LANE_TO_CHARACTER[self.domain]:
            raise ValueError("Validation verdict character does not match lane mapping.")
        if self.character_mode is not CharacterMode.LANE:
            raise ValueError("Validation verdicts must use `character_mode=LANE`.")
        return self


class GateReport(WizardBaseModel):
    run_id: str = Field(min_length=1)
    overall_state: GateState
    lane_states: dict[LaneDomain, GateState]
    council_character: CharacterId
    council_domain: CouncilDomain
    council_ready: bool
    claim_counts: dict[ClaimStatus, int]
    blocking_domains: list[LaneDomain] = Field(default_factory=list)
    blocking_claim_ids: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_gate_report(self) -> "GateReport":
        if self.council_character is not COUNCIL_CHARACTER:
            raise ValueError("Gate reports must use WHY_HOW as the council character.")
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Gate reports must use HOW as the council domain.")
        if set(self.lane_states) != set(LaneDomain):
            raise ValueError("Gate reports must contain all five lane states.")
        return self
