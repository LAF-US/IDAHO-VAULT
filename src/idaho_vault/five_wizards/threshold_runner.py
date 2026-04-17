"""Root-first threshold runner for one local 5Wizards staging loop."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from idaho_vault.five_wizards.enums import LaneDomain
from idaho_vault.five_wizards.lane_runner import (
    LaneClaimInput,
    LaneNoteInput,
    LaneRunInput,
)
from idaho_vault.five_wizards.service import (
    FiveWizardsStageRequest,
    FiveWizardsStageResult,
    run_and_stage_five_wizards,
)
from idaho_vault.five_wizards.workflow import FiveWizardsWorkflowInput

ROOT_ORIENTATION_SURFACES = (
    "AGENTS.md",
    "!/WAKEUP.md",
    "!/README.md",
    "!/AGENTS.md",
    "CONSTITUTION.md",
    "swarm.json",
)


def repo_root() -> Path:
    """Return the repository root for vault-local staging."""

    return Path(__file__).resolve().parents[3]


def threshold_stage_root() -> Path:
    """Return the one declared staging surface for the threshold run."""

    return repo_root() / "!" / "CREWAI"


def _timestamped_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"five-wizards-threshold-{stamp}"


def _lane_spec(domain: LaneDomain) -> dict[str, object]:
    if domain is LaneDomain.WHO:
        return {
            "claim_text": "Logan remains the authority who decides whether staged output is promoted.",
            "anchor_value": "LOGAN",
            "evidence_refs": ["AGENTS.md", "!/WAKEUP.md", "CONSTITUTION.md"],
            "wizard_note_text": (
                "Root-first orientation makes Logan's authority explicit before any "
                "candidate mistakes local success for sanction."
            ),
            "familiar_note_text": (
                "Do not let startup fluency masquerade as permission to promote."
            ),
        }
    if domain is LaneDomain.WHAT:
        return {
            "claim_text": "This threshold slice stages output to !/CREWAI/ and leaves it on-record but non-canonical.",
            "anchor_value": "staged threshold slice",
            "evidence_refs": [".crewai/MANIFEST.md", "!/CREWAI/README.md"],
            "wizard_note_text": (
                "The first loop handles claims, objections, and staging without pretending "
                "that staged output has become canon."
            ),
            "familiar_note_text": (
                "Challenge any wording that implies the run self-promotes."
            ),
        }
    if domain is LaneDomain.WHEN:
        return {
            "claim_text": "This loop resolves only after staging and Logan's explicit decision, not at first execution success.",
            "anchor_value": "after staging and review",
            "evidence_refs": ["!/README.md", "CONSTITUTION.md"],
            "wizard_note_text": (
                "The candidate's clock does not stop at execution; the lawful ending comes "
                "only after explicit review and named state transition."
            ),
            "familiar_note_text": (
                "Do not collapse handling, staging, and promotion into the same moment."
            ),
        }
    if domain is LaneDomain.WHERE:
        return {
            "claim_text": "The live staging surface for this run is !/CREWAI/.",
            "anchor_value": "!/CREWAI/",
            "evidence_refs": [".crewai/MANIFEST.md", "!/CREWAI/README.md"],
            "wizard_note_text": (
                "Threshold competence includes knowing which room is staging and which "
                "room is canon."
            ),
            "familiar_note_text": (
                "If a second staging destination appears, treat it as drift until Logan says otherwise."
            ),
        }
    if domain is LaneDomain.WHY:
        return {
            "claim_text": "The loop stops before consecration so the candidate does not lie about permissions.",
            "anchor_value": "truthful threshold conduct",
            "evidence_refs": [
                "!/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md",
                "!/README.md",
            ],
            "wizard_note_text": (
                "The playable lesson is not inward access; it is truthful handling at the threshold."
            ),
            "familiar_note_text": (
                "Keep wonder, but refuse the temptation to confuse adjacency with authority."
            ),
        }
    raise AssertionError(f"Unsupported lane domain: {domain}")


def build_threshold_workflow_input(
    *,
    run_id: str | None = None,
    session_id: str | None = None,
) -> FiveWizardsWorkflowInput:
    """Build one fixed, root-first workflow input for the threshold slice."""

    resolved_run_id = run_id or _timestamped_run_id()
    resolved_session_id = session_id or f"{resolved_run_id}-session"

    lane_runs: list[LaneRunInput] = []
    for domain in LaneDomain:
        spec = _lane_spec(domain)
        lane_stub = domain.value.lower()
        evidence_refs = list(spec["evidence_refs"])
        lane_runs.append(
            LaneRunInput(
                lane_domain=domain,
                run_id=resolved_run_id,
                report_id=f"{lane_stub}-threshold-report",
                claims=[
                    LaneClaimInput(
                        claim_id=f"{lane_stub}-threshold-claim",
                        text=str(spec["claim_text"]),
                        anchor_value=str(spec["anchor_value"]),
                        evidence_refs=evidence_refs,
                    )
                ],
                wizard_note=LaneNoteInput(
                    note_id=f"{lane_stub}-threshold-wizard-note",
                    text=str(spec["wizard_note_text"]),
                    evidence_refs=evidence_refs,
                    recurring_questions=[
                        "What is live here, and what is only staged or historical?",
                    ],
                    cautions=[
                        "Witness before declaration.",
                        "Handling before consecration.",
                    ],
                    unresolved_tensions=[
                        "A candidate can understand the machinery without claiming the altar."
                    ],
                ),
                familiar_note=LaneNoteInput(
                    note_id=f"{lane_stub}-threshold-familiar-note",
                    text=str(spec["familiar_note_text"]),
                    evidence_refs=evidence_refs,
                    recurring_questions=[
                        "Where must the loop stop and ask Logan?",
                    ],
                    cautions=[
                        "Adjacency is not authority.",
                    ],
                    unresolved_tensions=[
                        "The loop must stay legible to the next novice who wakes here."
                    ],
                ),
            )
        )

    return FiveWizardsWorkflowInput(
        run_id=resolved_run_id,
        session_id=resolved_session_id,
        lane_runs=lane_runs,
        awaken_debate_threads=[
            "Root/startup orientation precedes local lane execution.",
            "Staged work remains non-canonical until Logan decides promotion.",
        ],
        awaken_method_warnings=[
            "Do not confuse architectural understanding with sanction.",
        ],
        convene_debate_threads=[
            "All lanes remained local and staged only to !/CREWAI/.",
            "The run stopped before consecration and left canon untouched.",
        ],
        convene_method_warnings=[
            "Promotion is not part of this executable slice.",
        ],
        gaggle_text=(
            "The familiars agreed that the threshold run stayed root-first, staged "
            "only to !/CREWAI/, and did not pretend to self-promote."
        ),
        gaggle_evidence_refs=[
            "AGENTS.md",
            "!/README.md",
            ".crewai/MANIFEST.md",
        ],
    )


def run_threshold_stage(
    *,
    run_id: str | None = None,
    materialize: bool = True,
) -> FiveWizardsStageResult:
    """Execute the fixed threshold slice and stage it to !/CREWAI/ only."""

    workflow = build_threshold_workflow_input(run_id=run_id)
    request = FiveWizardsStageRequest(
        workflow=workflow,
        stage_root=str(threshold_stage_root()),
        materialize=materialize,
    )
    return run_and_stage_five_wizards(request)


def render_threshold_stage_summary(result: FiveWizardsStageResult) -> str:
    """Render a short console summary for the threshold slice."""

    orientation = " -> ".join(ROOT_ORIENTATION_SURFACES)
    stage_root = Path(result.stage_root) if result.stage_root is not None else threshold_stage_root()
    pack_root = result.pack_root or str(stage_root / result.run_id)
    return "\n".join(
        [
            f"5Wizards threshold run `{result.run_id}`",
            f"- Root orientation: {orientation}",
            f"- Gate state: {result.workflow.gate_report.overall_state.value}",
            f"- Council ready: {'yes' if result.workflow.gate_report.council_ready else 'no'}",
            f"- Staging surface: {stage_root}",
            f"- Pack root: {pack_root}",
            "- Promotion: Logan approval is still required before anything staged becomes canon.",
        ]
    )
