"""Generic executable lane runner for the 5Wizards workflow."""

from __future__ import annotations

from collections import Counter

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.enums import (
    CharacterMode,
    ClaimConfidence,
    ClaimStatus,
    GateState,
    LaneDomain,
    MirageCategory,
    NoteAuthorKind,
    NoteVisibility,
    ObjectionScope,
    ObjectionSeverity,
    ObjectionStatus,
    familiar_label,
    lane_anchor_type,
    lane_character,
    lane_familiar,
    lane_familiar_mode,
)
from idaho_vault.five_wizards.models import (
    Claim,
    CouncilReport,
    Objection,
    PersonalNote,
    ValidationVerdict,
)
from idaho_vault.five_wizards.pipelines import (
    challenge_council_report,
    create_personal_note,
    draft_council_report,
    finalize_council_report,
)
from idaho_vault.five_wizards.validators import adjudicate_claim


DEFAULT_WIZARD_ROLE_BY_LANE: dict[LaneDomain, str] = {
    LaneDomain.WHO: "identity scholar",
    LaneDomain.WHAT: "content scholar",
    LaneDomain.WHEN: "temporal scholar",
    LaneDomain.WHERE: "spatial scholar",
    LaneDomain.WHY: "meaning scholar",
}


class LaneRunnerBaseModel(BaseModel):
    """Strict base model for reusable lane runner types."""

    model_config = ConfigDict(extra="forbid")


class LaneClaimChallengeInput(LaneRunnerBaseModel):
    objection_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    category: MirageCategory
    severity: ObjectionSeverity = ObjectionSeverity.CONCERN
    evidence_refs: list[str] = Field(default_factory=list)
    status: ObjectionStatus = ObjectionStatus.OPEN
    resolution_note: str | None = None


class LaneClaimInput(LaneRunnerBaseModel):
    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    anchor_value: str
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: ClaimConfidence = ClaimConfidence.GROUNDED
    challenges: list[LaneClaimChallengeInput] = Field(default_factory=list)


class LaneNoteInput(LaneRunnerBaseModel):
    note_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    inquiry_question: str | None = None
    recurring_questions: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    unresolved_tensions: list[str] = Field(default_factory=list)
    visibility: NoteVisibility = NoteVisibility.PAIR_PRIVATE
    include_in_final_report: bool = True


class LaneRunInput(LaneRunnerBaseModel):
    lane_domain: LaneDomain
    run_id: str = Field(min_length=1)
    report_id: str = Field(min_length=1)
    claims: list[LaneClaimInput]
    wizard_note: LaneNoteInput
    familiar_note: LaneNoteInput
    wizard_role: str | None = None
    draft_council_text: str | None = None
    challenged_council_text: str | None = None
    final_council_text: str | None = None

    @model_validator(mode="after")
    def validate_claims(self) -> "LaneRunInput":
        if not self.claims:
            raise ValueError(f"{self.lane_domain.value} lane execution requires at least one claim.")
        return self


class LaneRunArtifacts(LaneRunnerBaseModel):
    run_id: str = Field(min_length=1)
    lane_domain: LaneDomain
    wizard_note: PersonalNote
    familiar_note: PersonalNote
    claims: list[Claim]
    objections: list[Objection]
    verdicts: list[ValidationVerdict]
    draft_report: CouncilReport
    challenged_report: CouncilReport
    finalized_report: CouncilReport | None = None
    lane_state: GateState
    council_ready: bool
    blocking_claim_ids: list[str] = Field(default_factory=list)
    blocking_objection_ids: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_bundle(self) -> "LaneRunArtifacts":
        for note in (self.wizard_note, self.familiar_note):
            if note.run_id != self.run_id or note.domain is not self.lane_domain:
                raise ValueError("Lane notes must belong to the lane run.")
        for claim in self.claims:
            if claim.run_id != self.run_id or claim.domain is not self.lane_domain:
                raise ValueError("Lane claims must belong to the lane run.")
        for objection in self.objections:
            if objection.run_id != self.run_id or objection.lane_domain is not self.lane_domain:
                raise ValueError("Lane objections must belong to the lane run.")
        for verdict in self.verdicts:
            if verdict.run_id != self.run_id or verdict.domain is not self.lane_domain:
                raise ValueError("Lane verdicts must belong to the lane run.")
        for report in (self.draft_report, self.challenged_report, self.finalized_report):
            if report is None:
                continue
            if report.run_id != self.run_id or report.domain is not self.lane_domain:
                raise ValueError("Lane reports must belong to the lane run.")
        if self.council_ready and self.finalized_report is None:
            raise ValueError("Council-ready lane bundles require a finalized report.")
        return self


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _lane_state(verdicts: list[ValidationVerdict]) -> GateState:
    statuses = {verdict.status for verdict in verdicts}
    if ClaimStatus.FAIL in statuses or ClaimStatus.BLOCKED in statuses:
        return GateState.RED
    if ClaimStatus.DISPUTED in statuses:
        return GateState.YELLOW
    return GateState.GREEN


def _verdict_rollup(verdicts: list[ValidationVerdict]) -> str:
    return "; ".join(f"{verdict.claim_id}={verdict.status.value}" for verdict in verdicts)


def _lane_familiar_label(domain: LaneDomain) -> str:
    return familiar_label(lane_familiar(domain), lane_familiar_mode(domain))


def _wizard_role_for_lane(request: LaneRunInput) -> str:
    return request.wizard_role or DEFAULT_WIZARD_ROLE_BY_LANE[request.lane_domain]


def _draft_report_text(request: LaneRunInput) -> str:
    if request.draft_council_text:
        return request.draft_council_text
    claim_ids = ", ".join(f"`{claim.claim_id}`" for claim in request.claims)
    return (
        f"{request.lane_domain.value} assembled {len(request.claims)} lane claims for review: {claim_ids}. "
        f"This draft stays close to the evidentiary record before {_lane_familiar_label(request.lane_domain)} "
        "applies challenge pressure."
    )


def _challenged_report_text(
    request: LaneRunInput,
    objections: list[Objection],
    verdicts: list[ValidationVerdict],
) -> str:
    if request.challenged_council_text:
        return request.challenged_council_text
    if objections:
        return (
            f"{_lane_familiar_label(request.lane_domain)} challenged the draft across "
            f"{len(objections)} recorded objections. Current verdicts: {_verdict_rollup(verdicts)}."
        )
    return (
        f"{_lane_familiar_label(request.lane_domain)} pressure-tested the draft and recorded no "
        f"formal objections. Current verdicts: {_verdict_rollup(verdicts)}."
    )


def _final_report_text(
    request: LaneRunInput,
    lane_state: GateState,
    verdicts: list[ValidationVerdict],
) -> str:
    if request.final_council_text:
        return request.final_council_text
    return (
        f"{request.lane_domain.value} finalized its council report after "
        f"{_lane_familiar_label(request.lane_domain)}'s review. "
        f"Lane state: {lane_state.value}. Claim verdicts: {_verdict_rollup(verdicts)}."
    )


def _build_note(
    lane_domain: LaneDomain,
    run_id: str,
    author_kind: NoteAuthorKind,
    note_input: LaneNoteInput,
) -> PersonalNote:
    return create_personal_note(
        note_id=note_input.note_id,
        run_id=run_id,
        domain=lane_domain,
        author_kind=author_kind,
        text=note_input.text,
        evidence_refs=note_input.evidence_refs,
        inquiry_question=note_input.inquiry_question,
        recurring_questions=note_input.recurring_questions,
        cautions=note_input.cautions,
        unresolved_tensions=note_input.unresolved_tensions,
        visibility=note_input.visibility,
        include_in_final_report=note_input.include_in_final_report,
    )


def _build_claim(
    lane_domain: LaneDomain,
    run_id: str,
    wizard_role: str,
    claim_input: LaneClaimInput,
) -> Claim:
    objections = [
        Objection(
            objection_id=challenge.objection_id,
            run_id=run_id,
            target_claim_id=claim_input.claim_id,
            scope=ObjectionScope.LANE,
            lane_domain=lane_domain,
            council_domain=None,
            character=lane_character(lane_domain),
            character_mode=CharacterMode.LANE,
            familiar=lane_familiar(lane_domain),
            familiar_mode=lane_familiar_mode(lane_domain),
            severity=challenge.severity,
            category=challenge.category,
            text=challenge.text,
            evidence_refs=challenge.evidence_refs,
            status=challenge.status,
            resolution_note=challenge.resolution_note,
        )
        for challenge in claim_input.challenges
    ]
    return Claim(
        claim_id=claim_input.claim_id,
        run_id=run_id,
        domain=lane_domain,
        character=lane_character(lane_domain),
        character_mode=CharacterMode.LANE,
        wizard_role=wizard_role,
        familiar=lane_familiar(lane_domain),
        familiar_mode=lane_familiar_mode(lane_domain),
        text=claim_input.text,
        anchor_type=lane_anchor_type(lane_domain),
        anchor_value=claim_input.anchor_value,
        evidence_refs=claim_input.evidence_refs,
        confidence=claim_input.confidence,
        status=ClaimStatus.PROPOSED,
        objections=objections,
    )


def _collect_objection_insights(objections: list[Objection]) -> tuple[list[str], list[str]]:
    unresolved = [
        objection.text for objection in objections if objection.status is ObjectionStatus.OPEN
    ]
    cautions = [
        f"{objection.category.value}: {objection.text}"
        for objection in objections
        if objection.severity in {ObjectionSeverity.CONCERN, ObjectionSeverity.FATAL}
    ]
    return _dedupe(unresolved), _dedupe(cautions)


def _report_evidence(
    wizard_note: PersonalNote,
    familiar_note: PersonalNote,
    claims: list[Claim],
    objections: list[Objection],
) -> list[str]:
    values = [
        *wizard_note.evidence_refs,
        *familiar_note.evidence_refs,
        *(ref for claim in claims for ref in claim.evidence_refs),
        *(ref for objection in objections for ref in objection.evidence_refs),
    ]
    return _dedupe(values)


def run_lane(request: LaneRunInput) -> LaneRunArtifacts:
    """Execute the pure-Python lane workflow for any canonical lane domain."""

    wizard_note = _build_note(request.lane_domain, request.run_id, NoteAuthorKind.WIZARD, request.wizard_note)
    familiar_note = _build_note(
        request.lane_domain,
        request.run_id,
        NoteAuthorKind.FAMILIAR,
        request.familiar_note,
    )

    wizard_role = _wizard_role_for_lane(request)
    claims = [
        _build_claim(request.lane_domain, request.run_id, wizard_role, claim_input)
        for claim_input in request.claims
    ]
    objections = [objection for claim in claims for objection in claim.objections]
    verdicts = [adjudicate_claim(claim) for claim in claims]
    lane_state = _lane_state(verdicts)
    unresolved_questions, caution_additions = _collect_objection_insights(objections)
    shared_evidence_refs = _report_evidence(wizard_note, familiar_note, claims, objections)

    draft_report = draft_council_report(
        report_id=request.report_id,
        run_id=request.run_id,
        domain=request.lane_domain,
        wizard_role=wizard_role,
        council_text=_draft_report_text(request),
        personal_notes=[wizard_note, familiar_note],
        evidence_refs=shared_evidence_refs,
    )
    challenged_report = challenge_council_report(
        draft_report,
        objections,
        revised_council_text=_challenged_report_text(request, objections, verdicts),
        unresolved_questions=unresolved_questions,
        cautions=caution_additions,
    )

    finalized_report: CouncilReport | None = None
    finalization_error: str | None = None
    try:
        finalized_report = finalize_council_report(
            challenged_report,
            objections,
            final_council_text=_final_report_text(request, lane_state, verdicts),
            evidence_refs=shared_evidence_refs,
        )
    except ValueError as exc:
        finalization_error = str(exc)

    blocking_claim_ids = [verdict.claim_id for verdict in verdicts if verdict.status is not ClaimStatus.PASS]
    blocking_objection_ids = _dedupe(
        [objection_id for verdict in verdicts for objection_id in verdict.blocking_objection_ids]
    )
    council_ready = lane_state is GateState.GREEN and finalized_report is not None

    counts = Counter(verdict.status for verdict in verdicts)
    summary_parts = [
        f"{request.lane_domain.value} lane produced {len(claims)} claims",
        f"state={lane_state.value}",
        f"passes={counts.get(ClaimStatus.PASS, 0)}",
        f"disputed={counts.get(ClaimStatus.DISPUTED, 0)}",
        f"failed={counts.get(ClaimStatus.FAIL, 0)}",
        f"blocked={counts.get(ClaimStatus.BLOCKED, 0)}",
        f"council_ready={'yes' if council_ready else 'no'}",
    ]
    if finalization_error:
        summary_parts.append(f"finalization_withheld={finalization_error}")

    return LaneRunArtifacts(
        run_id=request.run_id,
        lane_domain=request.lane_domain,
        wizard_note=wizard_note,
        familiar_note=familiar_note,
        claims=claims,
        objections=objections,
        verdicts=verdicts,
        draft_report=draft_report,
        challenged_report=challenged_report,
        finalized_report=finalized_report,
        lane_state=lane_state,
        council_ready=council_ready,
        blocking_claim_ids=blocking_claim_ids,
        blocking_objection_ids=blocking_objection_ids,
        summary="; ".join(summary_parts),
    )
