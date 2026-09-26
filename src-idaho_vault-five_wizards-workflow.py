"""Pure-Python workflow orchestration for the five lane runners and council."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.enums import GateState, LaneDomain
from idaho_vault.five_wizards.lane_runner import LaneRunArtifacts, LaneRunInput, run_lane
from idaho_vault.five_wizards.models import CouncilSession, FamiliarGaggleNote, GateReport
from idaho_vault.five_wizards.pipelines import (
    awaken_council,
    convene_council,
    record_familiar_gaggle,
)
from idaho_vault.five_wizards.validators import build_gate_report


class WorkflowBaseModel(BaseModel):
    """Strict base model for full 5Wizards workflow orchestration."""

    model_config = ConfigDict(extra="forbid")


class FiveWizardsWorkflowInput(WorkflowBaseModel):
    run_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    lane_runs: list[LaneRunInput]
    familiar_gaggle_note_id: str | None = None
    awaken_debate_threads: list[str] = Field(default_factory=list)
    awaken_method_warnings: list[str] = Field(default_factory=list)
    awaken_debate_summary: str = (
        "HOW awakened the council and sent the five wizards back to their domains."
    )
    awaken_outcome_summary: str = (
        "The five wizards withdrew to prepare private notes and council reports."
    )
    gaggle_text: str | None = None
    gaggle_evidence_refs: list[str] = Field(default_factory=list)
    convene_debate_threads: list[str] = Field(default_factory=list)
    convene_method_warnings: list[str] = Field(default_factory=list)
    convene_debate_summary: str = (
        "HOW convened the council after the five lane reports returned."
    )
    convene_outcome_summary: str = (
        "The council entered formal debate while the familiars gathered in observation."
    )

    @model_validator(mode="after")
    def validate_lane_runs(self) -> "FiveWizardsWorkflowInput":
        if not self.lane_runs:
            raise ValueError("The workflow requires lane inputs for all five canonical lanes.")
        lane_map: dict[LaneDomain, LaneRunInput] = {}
        for lane_run in self.lane_runs:
            if lane_run.run_id != self.run_id:
                raise ValueError("All lane runs in the workflow must share the workflow run id.")
            if lane_run.lane_domain in lane_map:
                raise ValueError("The workflow accepts only one lane run per canonical lane.")
            lane_map[lane_run.lane_domain] = lane_run
        if set(lane_map) != set(LaneDomain):
            raise ValueError("The workflow requires WHO, WHAT, WHEN, WHERE, and WHY lane runs.")
        return self


class FiveWizardsWorkflowArtifacts(WorkflowBaseModel):
    run_id: str = Field(min_length=1)
    awakened_session: CouncilSession
    lane_results: list[LaneRunArtifacts]
    gate_report: GateReport
    familiar_gaggle_note: FamiliarGaggleNote | None = None
    convened_session: CouncilSession | None = None
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_workflow(self) -> "FiveWizardsWorkflowArtifacts":
        if self.awakened_session.run_id != self.run_id:
            raise ValueError("Awakened council session must belong to the workflow run id.")
        lane_map: dict[LaneDomain, LaneRunArtifacts] = {}
        for lane_result in self.lane_results:
            if lane_result.run_id != self.run_id:
                raise ValueError("All lane results must belong to the workflow run id.")
            if lane_result.lane_domain in lane_map:
                raise ValueError("The workflow accepts only one lane result per canonical lane.")
            lane_map[lane_result.lane_domain] = lane_result
        if set(lane_map) != set(LaneDomain):
            raise ValueError("Workflow artifacts must include all five canonical lane results.")
        if self.gate_report.run_id != self.run_id:
            raise ValueError("Gate report must belong to the workflow run id.")
        if self.familiar_gaggle_note is not None and self.familiar_gaggle_note.run_id != self.run_id:
            raise ValueError("Familiar gaggle note must belong to the workflow run id.")
        if self.convened_session is not None and self.convened_session.run_id != self.run_id:
            raise ValueError("Convened council session must belong to the workflow run id.")
        if self.gate_report.council_ready:
            if self.familiar_gaggle_note is None or self.convened_session is None:
                raise ValueError("Green workflow runs must produce a gaggle note and a convened session.")
        else:
            if self.familiar_gaggle_note is not None:
                raise ValueError("Non-green workflow runs must not produce a gaggle note.")
            if self.convened_session is not None:
                raise ValueError("Non-green workflow runs must not produce a convened session.")
        return self


def _ordered_lane_runs(lane_runs: list[LaneRunInput]) -> list[LaneRunInput]:
    lane_map = {lane_run.lane_domain: lane_run for lane_run in lane_runs}
    return [lane_map[domain] for domain in LaneDomain]


def _ordered_lane_results(lane_results: list[LaneRunArtifacts]) -> list[LaneRunArtifacts]:
    lane_map = {lane_result.lane_domain: lane_result for lane_result in lane_results}
    return [lane_map[domain] for domain in LaneDomain]


def _default_gaggle_text() -> str:
    return (
        "The familiars watched the five reports return, compared skepticism, and kept score "
        "before the council debate."
    )


def run_five_wizards_workflow(request: FiveWizardsWorkflowInput) -> FiveWizardsWorkflowArtifacts:
    """Awaken the council, run all five lanes, gate the record, and convene when green."""

    awakened_session = awaken_council(
        session_id=request.session_id,
        run_id=request.run_id,
        debate_threads=request.awaken_debate_threads,
        method_warnings=request.awaken_method_warnings,
        debate_summary=request.awaken_debate_summary,
        outcome_summary=request.awaken_outcome_summary,
    )

    lane_results = [run_lane(lane_run) for lane_run in _ordered_lane_runs(request.lane_runs)]
    ordered_results = _ordered_lane_results(lane_results)
    verdicts = [verdict for lane_result in ordered_results for verdict in lane_result.verdicts]
    gate_report = build_gate_report(verdicts)

    familiar_gaggle_note: FamiliarGaggleNote | None = None
    convened_session: CouncilSession | None = None
    if gate_report.council_ready:
        finalized_reports = [
            lane_result.finalized_report for lane_result in ordered_results if lane_result.finalized_report is not None
        ]
        familiar_gaggle_note = record_familiar_gaggle(
            note_id=request.familiar_gaggle_note_id or f"{request.run_id}-familiar-gaggle",
            run_id=request.run_id,
            council_reports=finalized_reports,
            gossip_text=request.gaggle_text or _default_gaggle_text(),
            evidence_refs=request.gaggle_evidence_refs or None,
        )
        convened_session = convene_council(
            awakened_session,
            council_reports=finalized_reports,
            familiar_gaggle_notes=[familiar_gaggle_note],
            debate_threads=request.convene_debate_threads,
            method_warnings=request.convene_method_warnings,
            debate_summary=request.convene_debate_summary,
            outcome_summary=request.convene_outcome_summary,
        )

    blocking = ", ".join(domain.value for domain in gate_report.blocking_domains) or "none"
    summary = (
        f"Workflow run {request.run_id}: gate={gate_report.overall_state.value}; "
        f"council_ready={'yes' if gate_report.council_ready else 'no'}; "
        f"blocking_domains={blocking}."
    )

    return FiveWizardsWorkflowArtifacts(
        run_id=request.run_id,
        awakened_session=awakened_session,
        lane_results=ordered_results,
        gate_report=gate_report,
        familiar_gaggle_note=familiar_gaggle_note,
        convened_session=convened_session,
        summary=summary,
    )
