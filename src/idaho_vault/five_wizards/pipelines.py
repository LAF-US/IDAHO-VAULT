"""Pure-Python pipeline helpers for the 5Wizards reporting flow."""

from __future__ import annotations

from collections.abc import Sequence

from idaho_vault.five_wizards.enums import (
    COUNCIL_CHARACTER,
    COUNCIL_CHARACTER_MODE,
    COUNCIL_FAMILIAR,
    COUNCIL_FAMILIAR_MODE,
    COUNCIL_INQUIRY_PROMPT,
    CharacterMode,
    CouncilDomain,
    CouncilReportStatus,
    CouncilSessionStatus,
    LaneDomain,
    NoteAuthorKind,
    NoteVisibility,
    ObjectionScope,
    ObjectionSeverity,
    ObjectionStatus,
    lane_character,
    lane_familiar,
    lane_familiar_mode,
    lane_inquiry_prompt,
)
from idaho_vault.five_wizards.models import (
    CouncilReport,
    CouncilSession,
    FamiliarGaggleNote,
    Objection,
    PersonalNote,
)


def _dedupe(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _merge_text_items(existing: Sequence[str], extra: Sequence[str] | None) -> list[str]:
    if extra is None:
        return list(existing)
    return _dedupe([*existing, *extra])


def _assert_same_run(expected_run_id: str, actual_run_id: str, artifact_label: str) -> None:
    if actual_run_id != expected_run_id:
        raise ValueError(
            f"{artifact_label} run id `{actual_run_id}` does not match expected run `{expected_run_id}`."
        )


def _assert_lane_notes(run_id: str, domain: LaneDomain, notes: Sequence[PersonalNote]) -> None:
    if not notes:
        raise ValueError("Drafting a council report requires at least one personal note.")
    for note in notes:
        _assert_same_run(run_id, note.run_id, "Personal note")
        if note.domain is not domain:
            raise ValueError("All personal notes must belong to the same lane domain as the council report.")


def _assert_lane_objections(run_id: str, domain: LaneDomain, objections: Sequence[Objection]) -> None:
    for objection in objections:
        _assert_same_run(run_id, objection.run_id, "Objection")
        if objection.scope is not ObjectionScope.LANE:
            raise ValueError("Council report challenges must be expressed as lane objections.")
        if objection.lane_domain is not domain:
            raise ValueError("Challenge objections must stay inside the council report's lane domain.")


def _ordered_reports(
    run_id: str,
    reports: Sequence[CouncilReport],
    *,
    require_all_lanes: bool,
) -> list[CouncilReport]:
    if not reports:
        raise ValueError("Council work requires at least one council report.")

    report_by_domain: dict[LaneDomain, CouncilReport] = {}
    for report in reports:
        _assert_same_run(run_id, report.run_id, "Council report")
        if report.status is not CouncilReportStatus.FINALIZED:
            raise ValueError("Council reports must be finalized before council-side use.")
        if report.domain in report_by_domain:
            raise ValueError("Only one council report may be supplied per lane domain.")
        report_by_domain[report.domain] = report

    if require_all_lanes and set(report_by_domain) != set(LaneDomain):
        raise ValueError("Convening the council requires one finalized report from each of the five lanes.")

    return [report_by_domain[domain] for domain in LaneDomain if domain in report_by_domain]


def create_personal_note(
    *,
    note_id: str,
    run_id: str,
    domain: LaneDomain,
    author_kind: NoteAuthorKind,
    text: str,
    evidence_refs: Sequence[str] = (),
    inquiry_question: str | None = None,
    recurring_questions: Sequence[str] = (),
    cautions: Sequence[str] = (),
    unresolved_tensions: Sequence[str] = (),
    visibility: NoteVisibility = NoteVisibility.PAIR_PRIVATE,
    include_in_final_report: bool = True,
) -> PersonalNote:
    """Create one pair-private note with the canonical lane mapping pre-filled."""

    resolved_inquiry = inquiry_question or lane_inquiry_prompt(domain)
    resolved_recurring = list(recurring_questions) or [resolved_inquiry]

    return PersonalNote(
        note_id=note_id,
        run_id=run_id,
        domain=domain,
        author_kind=author_kind,
        character=lane_character(domain),
        character_mode=CharacterMode.LANE,
        familiar=lane_familiar(domain),
        familiar_mode=lane_familiar_mode(domain),
        text=text,
        evidence_refs=list(evidence_refs),
        inquiry_question=resolved_inquiry,
        recurring_questions=resolved_recurring,
        cautions=list(cautions),
        unresolved_tensions=list(unresolved_tensions),
        visibility=visibility,
        include_in_final_report=include_in_final_report,
    )


def draft_council_report(
    *,
    report_id: str,
    run_id: str,
    domain: LaneDomain,
    wizard_role: str,
    council_text: str,
    personal_notes: Sequence[PersonalNote],
    unresolved_questions: Sequence[str] | None = None,
    cautions: Sequence[str] | None = None,
    evidence_refs: Sequence[str] | None = None,
) -> CouncilReport:
    """Draft a wizard's council report from the pair's private notes."""

    _assert_lane_notes(run_id, domain, personal_notes)

    inferred_evidence = _dedupe(
        list(evidence_refs)
        if evidence_refs is not None
        else [ref for note in personal_notes for ref in note.evidence_refs]
    )
    inferred_unresolved = (
        list(unresolved_questions)
        if unresolved_questions is not None
        else _dedupe([item for note in personal_notes for item in note.unresolved_tensions])
    )
    inferred_cautions = (
        list(cautions)
        if cautions is not None
        else _dedupe([item for note in personal_notes for item in note.cautions])
    )

    return CouncilReport(
        report_id=report_id,
        run_id=run_id,
        domain=domain,
        character=lane_character(domain),
        character_mode=CharacterMode.LANE,
        wizard_role=wizard_role,
        familiar=lane_familiar(domain),
        familiar_mode=lane_familiar_mode(domain),
        status=CouncilReportStatus.DRAFT,
        personal_note_ids=[note.note_id for note in personal_notes],
        challenge_objection_ids=[],
        inquiry_question=lane_inquiry_prompt(domain),
        unresolved_questions=inferred_unresolved,
        cautions=inferred_cautions,
        council_text=council_text,
        evidence_refs=inferred_evidence,
    )


def challenge_council_report(
    report: CouncilReport,
    objections: Sequence[Objection],
    *,
    revised_council_text: str | None = None,
    unresolved_questions: Sequence[str] | None = None,
    cautions: Sequence[str] | None = None,
) -> CouncilReport:
    """Record familiar challenges against a wizard's draft council report."""

    if report.status not in {CouncilReportStatus.DRAFT, CouncilReportStatus.CHALLENGED}:
        raise ValueError("Only draft or already challenged reports may enter the challenge stage.")
    _assert_lane_objections(report.run_id, report.domain, objections)
    challenge_ids = _dedupe([*report.challenge_objection_ids, *(obj.objection_id for obj in objections)])

    return report.model_copy(
        update={
            "status": CouncilReportStatus.CHALLENGED,
            "challenge_objection_ids": challenge_ids,
            "council_text": revised_council_text if revised_council_text is not None else report.council_text,
            "unresolved_questions": _merge_text_items(report.unresolved_questions, unresolved_questions),
            "cautions": _merge_text_items(report.cautions, cautions),
        }
    )


def finalize_council_report(
    report: CouncilReport,
    objections: Sequence[Objection] = (),
    *,
    final_council_text: str | None = None,
    unresolved_questions: Sequence[str] | None = None,
    cautions: Sequence[str] | None = None,
    evidence_refs: Sequence[str] | None = None,
) -> CouncilReport:
    """Finalize a wizard's council report after challenge review."""

    if report.status not in {CouncilReportStatus.DRAFT, CouncilReportStatus.CHALLENGED}:
        raise ValueError("Only draft or challenged reports may be finalized.")
    _assert_lane_objections(report.run_id, report.domain, objections)

    objection_ids = {objection.objection_id for objection in objections}
    missing_challenges = [
        objection_id
        for objection_id in report.challenge_objection_ids
        if objection_id not in objection_ids
    ]
    if missing_challenges:
        raise ValueError("Finalizing a challenged report requires the full challenge objection set.")

    fatal_open = [
        objection.objection_id
        for objection in objections
        if objection.severity is ObjectionSeverity.FATAL and objection.status is ObjectionStatus.OPEN
    ]
    if fatal_open:
        raise ValueError("Cannot finalize a council report while fatal challenge objections remain open.")

    resolved_evidence = (
        list(report.evidence_refs)
        if evidence_refs is None
        else _dedupe([*report.evidence_refs, *evidence_refs])
    )

    return report.model_copy(
        update={
            "status": CouncilReportStatus.FINALIZED,
            "challenge_objection_ids": _dedupe(
                [*report.challenge_objection_ids, *(obj.objection_id for obj in objections)]
            ),
            "council_text": final_council_text if final_council_text is not None else report.council_text,
            "unresolved_questions": _merge_text_items(report.unresolved_questions, unresolved_questions),
            "cautions": _merge_text_items(report.cautions, cautions),
            "evidence_refs": resolved_evidence,
        }
    )


def record_familiar_gaggle(
    *,
    note_id: str,
    run_id: str,
    council_reports: Sequence[CouncilReport],
    gossip_text: str,
    evidence_refs: Sequence[str] | None = None,
    include_in_final_report: bool = True,
) -> FamiliarGaggleNote:
    """Record the familiar-side council observation layer."""

    ordered_reports = _ordered_reports(run_id, council_reports, require_all_lanes=False)
    resolved_evidence = _dedupe(
        list(evidence_refs)
        if evidence_refs is not None
        else [ref for report in ordered_reports for ref in report.evidence_refs]
    )

    return FamiliarGaggleNote(
        note_id=note_id,
        run_id=run_id,
        council_domain=CouncilDomain.HOW,
        host_character=COUNCIL_CHARACTER,
        host_character_mode=COUNCIL_CHARACTER_MODE,
        host_familiar=COUNCIL_FAMILIAR,
        host_familiar_mode=COUNCIL_FAMILIAR_MODE,
        participant_familiars=[report.familiar for report in ordered_reports],
        participant_modes=[report.familiar_mode for report in ordered_reports],
        watched_report_ids=[report.report_id for report in ordered_reports],
        gossip_text=gossip_text,
        evidence_refs=resolved_evidence,
        include_in_final_report=include_in_final_report,
    )


def awaken_council(
    *,
    session_id: str,
    run_id: str,
    debate_threads: Sequence[str] = (),
    method_warnings: Sequence[str] = (),
    debate_summary: str = "HOW awakened the council and called the five lanes into relation.",
    outcome_summary: str = "The council stands awake, awaiting finalized reports from every lane.",
) -> CouncilSession:
    """Create the initial HOW-side council session before the full debate begins."""

    return CouncilSession(
        session_id=session_id,
        run_id=run_id,
        council_domain=CouncilDomain.HOW,
        convener_character=COUNCIL_CHARACTER,
        convener_character_mode=COUNCIL_CHARACTER_MODE,
        convener_familiar=COUNCIL_FAMILIAR,
        convener_familiar_mode=COUNCIL_FAMILIAR_MODE,
        status=CouncilSessionStatus.AWAKENED,
        council_report_ids=[],
        familiar_gaggle_note_ids=[],
        inquiry_question=COUNCIL_INQUIRY_PROMPT,
        debate_threads=list(debate_threads),
        method_warnings=list(method_warnings),
        debate_summary=debate_summary,
        outcome_summary=outcome_summary,
    )


def convene_council(
    session: CouncilSession,
    *,
    council_reports: Sequence[CouncilReport],
    familiar_gaggle_notes: Sequence[FamiliarGaggleNote] = (),
    debate_threads: Sequence[str] = (),
    method_warnings: Sequence[str] = (),
    debate_summary: str = "HOW convened the five finalized reports for council debate.",
    outcome_summary: str = "The council is convened and ready to deliberate across the full record.",
) -> CouncilSession:
    """Move an awakened HOW-side session into the convened council state."""

    if session.status is not CouncilSessionStatus.AWAKENED:
        raise ValueError("Only an awakened council session may be convened.")
    ordered_reports = _ordered_reports(session.run_id, council_reports, require_all_lanes=True)
    for gaggle_note in familiar_gaggle_notes:
        _assert_same_run(session.run_id, gaggle_note.run_id, "Familiar gaggle note")
        if gaggle_note.council_domain is not CouncilDomain.HOW:
            raise ValueError("Council gaggle notes must belong to HOW.")

    return session.model_copy(
        update={
            "status": CouncilSessionStatus.CONVENED,
            "council_report_ids": [report.report_id for report in ordered_reports],
            "familiar_gaggle_note_ids": [note.note_id for note in familiar_gaggle_notes],
            "debate_threads": list(debate_threads),
            "method_warnings": list(method_warnings),
            "debate_summary": debate_summary,
            "outcome_summary": outcome_summary,
        }
    )
