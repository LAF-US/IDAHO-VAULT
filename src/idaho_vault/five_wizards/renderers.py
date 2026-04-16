"""Canonical JSON and Markdown renderers for 5Wizards artifacts."""

from __future__ import annotations

import json

from pydantic import BaseModel

from idaho_vault.five_wizards.enums import CouncilDomain, FamiliarId, FamiliarMode, LaneDomain, familiar_label
from idaho_vault.five_wizards.lane_runner import LaneRunArtifacts
from idaho_vault.five_wizards.models import (
    Claim,
    CouncilReport,
    CouncilSession,
    FamiliarGaggleNote,
    GateReport,
    Objection,
    PersonalNote,
    ValidationVerdict,
)
from idaho_vault.five_wizards.workflow import FiveWizardsWorkflowArtifacts


def to_canonical_json(model: BaseModel) -> str:
    """Serialize a model to stable, human-readable JSON."""

    return json.dumps(model.model_dump(mode="json"), indent=2, sort_keys=True)


def lane_artifact_group(domain: LaneDomain) -> str:
    """Return the reserved lane artifact group for a domain."""

    return f"lane/{domain.value.lower()}"


def council_artifact_group() -> str:
    """Return the reserved council artifact group for HOW."""

    return f"council/{CouncilDomain.HOW.value.lower()}"


def artifact_filename(run_id: str, stem: str, extension: str) -> str:
    """Build a stable artifact filename without writing it anywhere."""

    return f"{run_id}__{stem}.{extension.lstrip('.')}"


def _render_refs(refs: list[str]) -> str:
    return ", ".join(refs) if refs else "None"


def _render_familiar(familiar: FamiliarId, familiar_mode: FamiliarMode | None) -> str:
    return familiar_label(familiar, familiar_mode)


def render_personal_note_markdown(note: PersonalNote) -> str:
    lines = [
        f"# Personal Note `{note.note_id}`",
        "",
        f"- Run ID: `{note.run_id}`",
        f"- Domain: `{note.domain.value}`",
        f"- Author Kind: `{note.author_kind.value}`",
        f"- Character: `{note.character.value}`",
        f"- Character Mode: `{note.character_mode.value}`",
        f"- Familiar: `{_render_familiar(note.familiar, note.familiar_mode)}`",
        f"- Visibility: `{note.visibility.value}`",
        f"- Include In Final Report: `{'true' if note.include_in_final_report else 'false'}`",
        f"- Evidence Refs: {_render_refs(note.evidence_refs)}",
        "",
        "## Inquiry Question",
        "",
        note.inquiry_question,
        "",
        "## Note Text",
        "",
        note.text,
    ]
    if note.recurring_questions:
        lines.extend(["", "## Recurring Questions", ""])
        lines.extend(f"- {question}" for question in note.recurring_questions)
    if note.cautions:
        lines.extend(["", "## Cautions", ""])
        lines.extend(f"- {caution}" for caution in note.cautions)
    if note.unresolved_tensions:
        lines.extend(["", "## Unresolved Tensions", ""])
        lines.extend(f"- {tension}" for tension in note.unresolved_tensions)
    return "\n".join(lines)


def render_objection_markdown(objection: Objection) -> str:
    lines = [
        f"# Objection `{objection.objection_id}`",
        "",
        f"- Run ID: `{objection.run_id}`",
        f"- Target Claim: `{objection.target_claim_id}`",
        f"- Scope: `{objection.scope.value}`",
    ]
    if objection.lane_domain is not None:
        lines.append(f"- Lane Domain: `{objection.lane_domain.value}`")
    if objection.council_domain is not None:
        lines.append(f"- Council Domain: `{objection.council_domain.value}`")
    lines.extend(
        [
            f"- Character: `{objection.character.value}`",
            f"- Character Mode: `{objection.character_mode.value}`",
            f"- Familiar: `{_render_familiar(objection.familiar, objection.familiar_mode)}`",
            f"- Severity: `{objection.severity.value}`",
            f"- Status: `{objection.status.value}`",
            f"- Category: `{objection.category.value}`",
            f"- Evidence Refs: {_render_refs(objection.evidence_refs)}",
            "",
            "## Text",
            "",
            objection.text,
        ]
    )
    if objection.resolution_note:
        lines.extend(["", "## Resolution Note", "", objection.resolution_note])
    return "\n".join(lines)


def render_claim_markdown(claim: Claim) -> str:
    lines = [
        f"# Claim `{claim.claim_id}`",
        "",
        f"- Run ID: `{claim.run_id}`",
        f"- Domain: `{claim.domain.value}`",
        f"- Character: `{claim.character.value}`",
        f"- Character Mode: `{claim.character_mode.value}`",
        f"- Familiar: `{_render_familiar(claim.familiar, claim.familiar_mode)}`",
        f"- Status: `{claim.status.value}`",
        f"- Confidence: `{claim.confidence.value}`",
        f"- Anchor: `{claim.anchor_type.value}` -> `{claim.anchor_value}`",
        f"- Evidence Refs: {_render_refs(claim.evidence_refs)}",
        "",
        "## Claim Text",
        "",
        claim.text,
    ]
    if claim.objections:
        lines.extend(["", "## Objections", ""])
        for objection in claim.objections:
            lines.append(
                f"- `{objection.objection_id}` [{objection.scope.value}] "
                f"`{objection.severity.value}` / `{objection.status.value}`"
            )
    else:
        lines.extend(["", "## Objections", "", "- None"])
    return "\n".join(lines)


def render_council_report_markdown(report: CouncilReport) -> str:
    lines = [
        f"# Council Report `{report.report_id}`",
        "",
        f"- Run ID: `{report.run_id}`",
        f"- Domain: `{report.domain.value}`",
        f"- Character: `{report.character.value}`",
        f"- Character Mode: `{report.character_mode.value}`",
        f"- Familiar: `{_render_familiar(report.familiar, report.familiar_mode)}`",
        f"- Status: `{report.status.value}`",
        f"- Personal Notes: {', '.join(f'`{note_id}`' for note_id in report.personal_note_ids) or 'None'}",
        f"- Challenge Objections: {', '.join(f'`{obj}`' for obj in report.challenge_objection_ids) or 'None'}",
        f"- Evidence Refs: {_render_refs(report.evidence_refs)}",
        "",
        "## Inquiry Question",
        "",
        report.inquiry_question,
        "",
        "## Council Text",
        "",
        report.council_text,
    ]
    if report.unresolved_questions:
        lines.extend(["", "## Unresolved Questions", ""])
        lines.extend(f"- {question}" for question in report.unresolved_questions)
    if report.cautions:
        lines.extend(["", "## Cautions", ""])
        lines.extend(f"- {caution}" for caution in report.cautions)
    return "\n".join(lines)


def render_familiar_gaggle_markdown(note: FamiliarGaggleNote) -> str:
    participants = ", ".join(
        f"`{_render_familiar(familiar, mode)}`"
        for familiar, mode in zip(note.participant_familiars, note.participant_modes)
    ) or "None"
    watched = ", ".join(f"`{report_id}`" for report_id in note.watched_report_ids) or "None"
    return "\n".join(
        [
            f"# Familiar Gaggle Note `{note.note_id}`",
            "",
            f"- Run ID: `{note.run_id}`",
            f"- Council Domain: `{note.council_domain.value}`",
            f"- Host Character: `{note.host_character.value}`",
            f"- Host Familiar: `{_render_familiar(note.host_familiar, note.host_familiar_mode)}`",
            f"- Participants: {participants}",
            f"- Watched Reports: {watched}",
            f"- Include In Final Report: `{'true' if note.include_in_final_report else 'false'}`",
            f"- Evidence Refs: {_render_refs(note.evidence_refs)}",
            "",
            "## Gossip Text",
            "",
            note.gossip_text,
        ]
    )


def render_council_session_markdown(session: CouncilSession) -> str:
    reports = ", ".join(f"`{report_id}`" for report_id in session.council_report_ids) or "None"
    gaggle = ", ".join(f"`{note_id}`" for note_id in session.familiar_gaggle_note_ids) or "None"
    lines = [
        f"# Council Session `{session.session_id}`",
        "",
        f"- Run ID: `{session.run_id}`",
        f"- Council Domain: `{session.council_domain.value}`",
        f"- Convener Character: `{session.convener_character.value}`",
        f"- Convener Familiar: `{_render_familiar(session.convener_familiar, session.convener_familiar_mode)}`",
        f"- Status: `{session.status.value}`",
        f"- Council Reports: {reports}",
        f"- Familiar Gaggle Notes: {gaggle}",
        "",
        "## Inquiry Question",
        "",
        session.inquiry_question,
    ]
    if session.debate_threads:
        lines.extend(["", "## Debate Threads", ""])
        lines.extend(f"- {thread}" for thread in session.debate_threads)
    if session.method_warnings:
        lines.extend(["", "## Method Warnings", ""])
        lines.extend(f"- {warning}" for warning in session.method_warnings)
    lines.extend(
        [
            "",
            "## Debate Summary",
            "",
            session.debate_summary,
            "",
            "## Outcome Summary",
            "",
            session.outcome_summary,
        ]
    )
    return "\n".join(lines)


def render_validation_verdict_markdown(verdict: ValidationVerdict) -> str:
    lines = [
        f"# Validation Verdict `{verdict.claim_id}`",
        "",
        f"- Run ID: `{verdict.run_id}`",
        f"- Domain: `{verdict.domain.value}`",
        f"- Character: `{verdict.character.value}`",
        f"- Character Mode: `{verdict.character_mode.value}`",
        f"- Status: `{verdict.status.value}`",
        f"- Reason: `{verdict.reason}`",
        f"- Validator: `{verdict.validator}`",
        f"- Evidence Refs: {_render_refs(verdict.accepted_evidence_refs)}",
    ]
    if verdict.mirage_categories:
        lines.append(
            "- Mirage Categories: "
            + ", ".join(f"`{category.value}`" for category in verdict.mirage_categories)
        )
    else:
        lines.append("- Mirage Categories: None")
    if verdict.blocking_objection_ids:
        lines.append(
            "- Blocking Objections: "
            + ", ".join(f"`{objection_id}`" for objection_id in verdict.blocking_objection_ids)
        )
    else:
        lines.append("- Blocking Objections: None")
    if verdict.notes:
        lines.extend(["", "## Notes", "", verdict.notes])
    return "\n".join(lines)


def render_gate_report_markdown(report: GateReport) -> str:
    lines = [
        f"# Gate Report `{report.run_id}`",
        "",
        f"- Overall State: `{report.overall_state.value}`",
        f"- Council Character: `{report.council_character.value}`",
        f"- Council Domain: `{report.council_domain.value}`",
        f"- Council Ready: `{'true' if report.council_ready else 'false'}`",
        "",
        "## Lane States",
        "",
    ]
    for domain in LaneDomain:
        lines.append(f"- `{domain.value}`: `{report.lane_states[domain].value}`")

    lines.extend(["", "## Claim Counts", ""])
    for status, count in report.claim_counts.items():
        lines.append(f"- `{status.value}`: {count}")

    lines.extend(
        [
            "",
            "## Blocking Domains",
            "",
            ", ".join(f"`{domain.value}`" for domain in report.blocking_domains) or "None",
            "",
            "## Blocking Claims",
            "",
            ", ".join(f"`{claim_id}`" for claim_id in report.blocking_claim_ids) or "None",
            "",
            "## Summary",
            "",
            report.summary,
        ]
    )
    return "\n".join(lines)


def render_lane_run_markdown(lane_run: LaneRunArtifacts) -> str:
    claims = ", ".join(f"`{claim.claim_id}`" for claim in lane_run.claims) or "None"
    blocking_claims = ", ".join(f"`{claim_id}`" for claim_id in lane_run.blocking_claim_ids) or "None"
    blocking_objections = (
        ", ".join(f"`{objection_id}`" for objection_id in lane_run.blocking_objection_ids) or "None"
    )
    finalized_status = (
        f"`{lane_run.finalized_report.status.value}`"
        if lane_run.finalized_report is not None
        else "None"
    )
    return "\n".join(
        [
            f"# Lane Run `{lane_run.run_id}` / `{lane_run.lane_domain.value}`",
            "",
            f"- Lane State: `{lane_run.lane_state.value}`",
            f"- Council Ready: `{'true' if lane_run.council_ready else 'false'}`",
            f"- Claims: {claims}",
            f"- Finalized Report: {finalized_status}",
            f"- Wizard Note: `{lane_run.wizard_note.note_id}`",
            f"- Familiar Note: `{lane_run.familiar_note.note_id}`",
            "",
            "## Blocking Claims",
            "",
            blocking_claims,
            "",
            "## Blocking Objections",
            "",
            blocking_objections,
            "",
            "## Summary",
            "",
            lane_run.summary,
        ]
    )


def render_workflow_markdown(workflow: FiveWizardsWorkflowArtifacts) -> str:
    lines = [
        f"# Workflow Run `{workflow.run_id}`",
        "",
        f"- Awakened Session: `{workflow.awakened_session.session_id}` / `{workflow.awakened_session.status.value}`",
        f"- Gate State: `{workflow.gate_report.overall_state.value}`",
        f"- Council Ready: `{'true' if workflow.gate_report.council_ready else 'false'}`",
        f"- Familiar Gaggle Note: `{workflow.familiar_gaggle_note.note_id}`"
        if workflow.familiar_gaggle_note is not None
        else "- Familiar Gaggle Note: None",
        f"- Convened Session: `{workflow.convened_session.session_id}` / `{workflow.convened_session.status.value}`"
        if workflow.convened_session is not None
        else "- Convened Session: None",
        "",
        "## Lane Results",
        "",
    ]
    for lane_result in workflow.lane_results:
        lines.append(
            f"- `{lane_result.lane_domain.value}`: `{lane_result.lane_state.value}` / "
            f"council_ready=`{'true' if lane_result.council_ready else 'false'}`"
        )
    lines.extend(["", "## Summary", "", workflow.summary])
    return "\n".join(lines)
