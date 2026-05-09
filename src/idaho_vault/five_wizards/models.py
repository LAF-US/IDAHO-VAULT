"""Pydantic models for the 5Wizards schema foundation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.enums import (
    AnchorType,
    ClaimConfidence,
    ClaimStatus,
    COUNCIL_ENTITY,
    COUNCIL_FAMILIAR,
    COUNCIL_FAMILIAR_MODE,
    COUNCIL_PERSONALITY,
    COUNCIL_SURFACE_MODE,
    CouncilDomain,
    CouncilReportStatus,
    CouncilSessionStatus,
    FamiliarId,
    FamiliarMode,
    GateState,
    InstitutionId,
    LaneDomain,
    LANE_TO_ANCHOR,
    LANE_TO_ENTITY,
    LANE_TO_FAMILIAR,
    LANE_TO_FAMILIAR_MODE,
    LANE_TO_PERSONALITY,
    MirageCategory,
    NoteAuthorKind,
    NoteVisibility,
    ObjectionScope,
    ObjectionSeverity,
    ObjectionStatus,
    SurfaceMode,
    WizardEntityId,
    WizardPersonalityId,
)


class WizardBaseModel(BaseModel):
    """Common base model with strict fields."""

    model_config = ConfigDict(extra="forbid")


class PersonalNote(WizardBaseModel):
    note_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    domain: LaneDomain
    author_kind: NoteAuthorKind
    entity: WizardEntityId
    personality: WizardPersonalityId
    surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Personal notes currently belong only to the FIVE_WIZARDS institution.")
        if self.entity is not LANE_TO_ENTITY[self.domain]:
            raise ValueError("Personal note entity does not match lane domain mapping.")
        if self.personality is not LANE_TO_PERSONALITY[self.domain]:
            raise ValueError("Personal note personality does not match lane domain mapping.")
        if self.surface_mode is not SurfaceMode.LANE:
            raise ValueError("Personal notes must use `surface_mode=LANE`.")
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
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    target_claim_id: str = Field(min_length=1)
    scope: ObjectionScope
    lane_domain: LaneDomain | None = None
    council_domain: CouncilDomain | None = None
    entity: WizardEntityId
    personality: WizardPersonalityId
    surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Objections currently belong only to the FIVE_WIZARDS institution.")
        if self.scope is ObjectionScope.LANE:
            if self.lane_domain is None or self.council_domain is not None:
                raise ValueError("Lane objections require `lane_domain` and forbid `council_domain`.")
            if self.entity is not LANE_TO_ENTITY[self.lane_domain]:
                raise ValueError("Lane objection entity does not match domain mapping.")
            if self.personality is not LANE_TO_PERSONALITY[self.lane_domain]:
                raise ValueError("Lane objection personality does not match domain mapping.")
            if self.surface_mode is not SurfaceMode.LANE:
                raise ValueError("Lane objections require `surface_mode=LANE`.")
            if self.familiar is not LANE_TO_FAMILIAR[self.lane_domain]:
                raise ValueError("Lane objection familiar does not match domain mapping.")
            if self.familiar_mode != LANE_TO_FAMILIAR_MODE[self.lane_domain]:
                raise ValueError("Lane objection familiar mode does not match domain mapping.")
        else:
            if self.council_domain is None or self.lane_domain is not None:
                raise ValueError("Council objections require `council_domain` and forbid `lane_domain`.")
            if self.council_domain is not CouncilDomain.HOW:
                raise ValueError("Council objections currently support only `HOW`.")
            if self.entity is not COUNCIL_ENTITY:
                raise ValueError("Council objections must use WHY as the council entity.")
            if self.personality is not COUNCIL_PERSONALITY:
                raise ValueError("Council objections must use HOW as the council personality.")
            if self.surface_mode is not COUNCIL_SURFACE_MODE:
                raise ValueError("Council objections must use `surface_mode=COUNCIL`.")
            if self.familiar is not COUNCIL_FAMILIAR or self.familiar_mode is not COUNCIL_FAMILIAR_MODE:
                raise ValueError("Council objections must use THY_THE in THE mode.")
        return self


class Claim(WizardBaseModel):
    claim_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    domain: LaneDomain
    entity: WizardEntityId
    personality: WizardPersonalityId
    surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Claims currently belong only to the FIVE_WIZARDS institution.")
        if self.entity is not LANE_TO_ENTITY[self.domain]:
            raise ValueError("Claim entity does not match lane domain mapping.")
        if self.personality is not LANE_TO_PERSONALITY[self.domain]:
            raise ValueError("Claim personality does not match lane domain mapping.")
        if self.surface_mode is not SurfaceMode.LANE:
            raise ValueError("Claims must use `surface_mode=LANE`.")
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
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    domain: LaneDomain
    entity: WizardEntityId
    personality: WizardPersonalityId
    surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Council reports currently belong only to the FIVE_WIZARDS institution.")
        if self.entity is not LANE_TO_ENTITY[self.domain]:
            raise ValueError("Council report entity does not match lane domain mapping.")
        if self.personality is not LANE_TO_PERSONALITY[self.domain]:
            raise ValueError("Council report personality does not match lane domain mapping.")
        if self.surface_mode is not SurfaceMode.LANE:
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
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    council_domain: CouncilDomain
    host_entity: WizardEntityId
    host_personality: WizardPersonalityId
    host_surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Familiar gaggle notes currently belong only to the FIVE_WIZARDS institution.")
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Familiar gaggle notes currently belong to the HOW council domain.")
        if self.host_entity is not COUNCIL_ENTITY:
            raise ValueError("Familiar gaggle notes must use WHY as the host entity.")
        if self.host_personality is not COUNCIL_PERSONALITY:
            raise ValueError("Familiar gaggle notes must use HOW as the host personality.")
        if self.host_surface_mode is not COUNCIL_SURFACE_MODE:
            raise ValueError("Familiar gaggle notes must use `host_surface_mode=COUNCIL`.")
        if self.host_familiar is not COUNCIL_FAMILIAR or self.host_familiar_mode is not COUNCIL_FAMILIAR_MODE:
            raise ValueError("Familiar gaggle notes must use THY_THE in THE mode as host.")
        if len(self.participant_familiars) != len(self.participant_modes):
            raise ValueError("Participant familiars and modes must have the same length.")
        return self


class CouncilSession(WizardBaseModel):
    session_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    council_domain: CouncilDomain
    convener_entity: WizardEntityId
    convener_personality: WizardPersonalityId
    convener_surface_mode: SurfaceMode
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
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Council sessions currently belong only to the FIVE_WIZARDS institution.")
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Council sessions currently belong to the HOW council domain.")
        if self.convener_entity is not COUNCIL_ENTITY:
            raise ValueError("Council sessions must use WHY as the convener entity.")
        if self.convener_personality is not COUNCIL_PERSONALITY:
            raise ValueError("Council sessions must use HOW as the convener personality.")
        if self.convener_surface_mode is not COUNCIL_SURFACE_MODE:
            raise ValueError("Council sessions must use `convener_surface_mode=COUNCIL`.")
        if self.convener_familiar is not COUNCIL_FAMILIAR or self.convener_familiar_mode is not COUNCIL_FAMILIAR_MODE:
            raise ValueError("Council sessions must use THY_THE in THE mode as familiar host.")
        if not self.inquiry_question.strip():
            raise ValueError("Council sessions require the HOW inquiry question.")
        return self


class ValidationVerdict(WizardBaseModel):
    claim_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    domain: LaneDomain
    entity: WizardEntityId
    personality: WizardPersonalityId
    surface_mode: SurfaceMode
    status: ClaimStatus
    reason: str = Field(min_length=1)
    mirage_categories: list[MirageCategory] = Field(default_factory=list)
    blocking_objection_ids: list[str] = Field(default_factory=list)
    accepted_evidence_refs: list[str] = Field(default_factory=list)
    validator: str = Field(min_length=1)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_verdict_mapping(self) -> "ValidationVerdict":
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Validation verdicts currently belong only to the FIVE_WIZARDS institution.")
        if self.entity is not LANE_TO_ENTITY[self.domain]:
            raise ValueError("Validation verdict entity does not match lane mapping.")
        if self.personality is not LANE_TO_PERSONALITY[self.domain]:
            raise ValueError("Validation verdict personality does not match lane mapping.")
        if self.surface_mode is not SurfaceMode.LANE:
            raise ValueError("Validation verdicts must use `surface_mode=LANE`.")
        return self


class GateReport(WizardBaseModel):
    run_id: str = Field(min_length=1)
    institution: InstitutionId = InstitutionId.FIVE_WIZARDS
    overall_state: GateState
    lane_states: dict[LaneDomain, GateState]
    council_entity: WizardEntityId
    council_personality: WizardPersonalityId
    council_surface_mode: SurfaceMode
    council_domain: CouncilDomain
    council_ready: bool
    claim_counts: dict[ClaimStatus, int]
    blocking_domains: list[LaneDomain] = Field(default_factory=list)
    blocking_claim_ids: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_gate_report(self) -> "GateReport":
        if self.institution is not InstitutionId.FIVE_WIZARDS:
            raise ValueError("Gate reports currently belong only to the FIVE_WIZARDS institution.")
        if self.council_entity is not COUNCIL_ENTITY:
            raise ValueError("Gate reports must use WHY as the council entity.")
        if self.council_personality is not COUNCIL_PERSONALITY:
            raise ValueError("Gate reports must use HOW as the council personality.")
        if self.council_surface_mode is not COUNCIL_SURFACE_MODE:
            raise ValueError("Gate reports must use `council_surface_mode=COUNCIL`.")
        if self.council_domain is not CouncilDomain.HOW:
            raise ValueError("Gate reports must use HOW as the council domain.")
        if set(self.lane_states) != set(LaneDomain):
            raise ValueError("Gate reports must contain all five lane states.")
        return self
