"""Python adjudicators and gate builders for the 5Wizards schema foundation."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from idaho_vault.five_wizards.enums import (
    ClaimStatus,
    COUNCIL_ENTITY,
    COUNCIL_PERSONALITY,
    COUNCIL_SURFACE_MODE,
    CouncilDomain,
    GateState,
    InstitutionId,
    LaneDomain,
    LANE_TO_ANCHOR,
    LANE_TO_ENTITY,
    LANE_TO_FAMILIAR,
    LANE_TO_FAMILIAR_MODE,
    LANE_TO_PERSONALITY,
    MirageCategory,
    ObjectionSeverity,
    ObjectionStatus,
    SurfaceMode,
)
from idaho_vault.five_wizards.models import Claim, GateReport, ValidationVerdict


VALIDATOR_NAME = "idaho_vault.five_wizards.validators.adjudicate_claim"


def _mapping_violation_reason(claim: Claim) -> str | None:
    if claim.institution is not InstitutionId.FIVE_WIZARDS:
        return "claim must stay inside the FIVE_WIZARDS institution"
    if claim.entity is not LANE_TO_ENTITY[claim.domain]:
        return "entity mismatch for lane domain"
    if claim.personality is not LANE_TO_PERSONALITY[claim.domain]:
        return "personality mismatch for lane domain"
    if claim.surface_mode is not SurfaceMode.LANE:
        return "claims must use LANE surface mode"
    if claim.familiar is not LANE_TO_FAMILIAR[claim.domain]:
        return "familiar mismatch for lane domain"
    if claim.familiar_mode != LANE_TO_FAMILIAR_MODE[claim.domain]:
        return "familiar mode mismatch for lane domain"
    if claim.anchor_type is not LANE_TO_ANCHOR[claim.domain]:
        return "anchor type mismatch for lane domain"
    return None


def adjudicate_claim(claim: Claim, *, validator: str = VALIDATOR_NAME) -> ValidationVerdict:
    """Return the canonical verdict for one lane claim."""

    if not claim.anchor_value.strip():
        return ValidationVerdict(
            claim_id=claim.claim_id,
            run_id=claim.run_id,
            institution=claim.institution,
            domain=claim.domain,
            entity=claim.entity,
            personality=claim.personality,
            surface_mode=claim.surface_mode,
            status=ClaimStatus.FAIL,
            reason="missing_anchor",
            mirage_categories=[MirageCategory.MISSING_ANCHOR],
            blocking_objection_ids=[],
            accepted_evidence_refs=[],
            validator=validator,
            notes="Claims require a non-empty anchor value.",
        )

    if not claim.evidence_refs:
        return ValidationVerdict(
            claim_id=claim.claim_id,
            run_id=claim.run_id,
            institution=claim.institution,
            domain=claim.domain,
            entity=claim.entity,
            personality=claim.personality,
            surface_mode=claim.surface_mode,
            status=ClaimStatus.FAIL,
            reason="missing_evidence",
            mirage_categories=[MirageCategory.MISSING_EVIDENCE],
            blocking_objection_ids=[],
            accepted_evidence_refs=[],
            validator=validator,
            notes="Claims require at least one evidence reference.",
        )

    mapping_violation = _mapping_violation_reason(claim)
    if mapping_violation is not None:
        return ValidationVerdict(
            claim_id=claim.claim_id,
            run_id=claim.run_id,
            institution=InstitutionId.FIVE_WIZARDS,
            domain=claim.domain,
            entity=LANE_TO_ENTITY[claim.domain],
            personality=LANE_TO_PERSONALITY[claim.domain],
            surface_mode=SurfaceMode.LANE,
            status=ClaimStatus.BLOCKED,
            reason="invalid_mapping",
            mirage_categories=[],
            blocking_objection_ids=[],
            accepted_evidence_refs=claim.evidence_refs,
            validator=validator,
            notes=mapping_violation,
        )

    fatal_open_objections = [
        objection.objection_id
        for objection in claim.objections
        if objection.severity is ObjectionSeverity.FATAL and objection.status is ObjectionStatus.OPEN
    ]
    if fatal_open_objections:
        return ValidationVerdict(
            claim_id=claim.claim_id,
            run_id=claim.run_id,
            institution=claim.institution,
            domain=claim.domain,
            entity=claim.entity,
            personality=claim.personality,
            surface_mode=claim.surface_mode,
            status=ClaimStatus.DISPUTED,
            reason="fatal_objection",
            mirage_categories=[],
            blocking_objection_ids=fatal_open_objections,
            accepted_evidence_refs=claim.evidence_refs,
            validator=validator,
            notes="At least one fatal objection remains open.",
        )

    return ValidationVerdict(
        claim_id=claim.claim_id,
        run_id=claim.run_id,
        institution=claim.institution,
        domain=claim.domain,
        entity=claim.entity,
        personality=claim.personality,
        surface_mode=claim.surface_mode,
        status=ClaimStatus.PASS,
        reason="grounded_for_current_scope",
        mirage_categories=[],
        blocking_objection_ids=[],
        accepted_evidence_refs=claim.evidence_refs,
        validator=validator,
        notes="Claim passed current scope adjudication.",
    )


def _aggregate_lane_state(verdicts: list[ValidationVerdict]) -> GateState:
    if not verdicts:
        return GateState.RED
    statuses = {verdict.status for verdict in verdicts}
    if ClaimStatus.FAIL in statuses or ClaimStatus.BLOCKED in statuses:
        return GateState.RED
    if ClaimStatus.DISPUTED in statuses:
        return GateState.YELLOW
    return GateState.GREEN


def build_gate_report(verdicts: Iterable[ValidationVerdict]) -> GateReport:
    """Aggregate lane verdicts into a run-level gate report."""

    verdict_list = list(verdicts)
    if not verdict_list:
        raise ValueError("Cannot build a gate report without at least one verdict.")

    run_ids = {verdict.run_id for verdict in verdict_list}
    if len(run_ids) != 1:
        raise ValueError("Gate reports require verdicts from exactly one run id.")
    run_id = verdict_list[0].run_id

    grouped: dict[LaneDomain, list[ValidationVerdict]] = defaultdict(list)
    for verdict in verdict_list:
        grouped[verdict.domain].append(verdict)

    lane_states = {domain: _aggregate_lane_state(grouped[domain]) for domain in LaneDomain}
    overall_state = GateState.GREEN
    if any(state is GateState.RED for state in lane_states.values()):
        overall_state = GateState.RED
    elif any(state is GateState.YELLOW for state in lane_states.values()):
        overall_state = GateState.YELLOW

    claim_counts = {status: 0 for status in ClaimStatus}
    for verdict in verdict_list:
        claim_counts[verdict.status] += 1

    blocking_domains = [domain for domain, state in lane_states.items() if state is GateState.RED]
    blocking_claim_ids = [
        verdict.claim_id
        for verdict in verdict_list
        if verdict.status in {ClaimStatus.FAIL, ClaimStatus.BLOCKED}
    ]
    council_ready = overall_state is GateState.GREEN
    summary = (
        f"Run {run_id} is {overall_state.value}. "
        f"Council ready: {'yes' if council_ready else 'no'}."
    )

    return GateReport(
        run_id=run_id,
        institution=InstitutionId.FIVE_WIZARDS,
        overall_state=overall_state,
        lane_states=lane_states,
        council_entity=COUNCIL_ENTITY,
        council_personality=COUNCIL_PERSONALITY,
        council_surface_mode=COUNCIL_SURFACE_MODE,
        council_domain=CouncilDomain.HOW,
        council_ready=council_ready,
        claim_counts=claim_counts,
        blocking_domains=blocking_domains,
        blocking_claim_ids=blocking_claim_ids,
        summary=summary,
    )
