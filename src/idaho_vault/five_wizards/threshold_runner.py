"""Root-first threshold runner for one local 5Wizards staging loop."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from idaho_vault.bootstrap_contract import build_contract_report_for_root
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
from idaho_vault.operator_context import (
    BOOT_CHAIN_SURFACES,
    OPERATOR_FRONT_DOOR_SURFACES,
    OperatorContext,
    evaluate_evidence_refs,
    load_operator_context,
)

ROOT_ORIENTATION_SURFACES = BOOT_CHAIN_SURFACES


class ThresholdContractError(RuntimeError):
    """Raised when the threshold runner cannot honestly claim its startup contract."""


def repo_root() -> Path:
    """Return the repository root for vault-local staging."""

    return Path(__file__).resolve().parents[3]


def threshold_stage_root(root: Path | None = None) -> Path:
    """Return the one declared staging surface for the threshold run."""

    return (root or repo_root()) / "!" / "CREWAI"


def _timestamped_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"five-wizards-threshold-{stamp}"


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _tracked_daily_note_ref(context: OperatorContext) -> str | None:
    if context.daily_note_exists and context.daily_note_tracked is not False:
        return context.daily_note_path
    return None


def _backlog_preview(context: OperatorContext, limit: int = 2) -> str:
    items = []
    for line in context.open_backlog_items[:limit]:
        item = line.removeprefix("- [ ] ").strip()
        if item:
            items.append(item)
    if not items:
        return "No open backlog items are currently recorded in TO DO LIST.md."
    return "; ".join(items)


def _lane_spec(domain: LaneDomain, context: OperatorContext) -> dict[str, object]:
    current_note_ref = _tracked_daily_note_ref(context)
    backlog_refs = ["TO DO LIST.md"]
    if current_note_ref is not None:
        backlog_refs.append(current_note_ref)
    backlog_preview = _backlog_preview(context)

    if domain is LaneDomain.WHO:
        return {
            "claim_text": "Logan remains the authority who decides whether staged output is promoted.",
            "anchor_value": "LOGAN",
            "evidence_refs": ["AGENTS.md", "!/WAKEUP.md", "CONSTITUTION.md", "swarm.json"],
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
            "claim_text": (
                "This threshold slice stages output to !/CREWAI/, leaves it on-record but "
                "non-canonical, and reads from the active operator backlog rather than a "
                "self-authored queue."
            ),
            "anchor_value": "staged threshold slice",
            "evidence_refs": [".crewai/MANIFEST.md", "!/CREWAI/README.md", *backlog_refs],
            "wizard_note_text": (
                "The first loop handles claims, objections, and staging without pretending "
                f"that staged output has become canon. Backlog preview: {backlog_preview}"
            ),
            "familiar_note_text": (
                "Challenge any wording that implies the run self-promotes."
            ),
        }
    if domain is LaneDomain.WHEN:
        return {
            "claim_text": (
                "This loop resolves only after staging and Logan's explicit decision, not at "
                "first execution success or first contact with today's work queue."
            ),
            "anchor_value": "after staging and review",
            "evidence_refs": [
                "DAILY NOTE TEMPLATE.md",
                ".obsidian/daily-notes.json",
                ".obsidian/plugins/periodic-notes/data.json",
                *backlog_refs,
            ],
            "wizard_note_text": (
                "The candidate's clock does not stop at execution; the lawful ending comes "
                f"only after explicit review and named state transition. Today's note: {context.daily_note_path}"
            ),
            "familiar_note_text": (
                "Do not collapse handling, staging, and promotion into the same moment."
            ),
        }
    if domain is LaneDomain.WHERE:
        return {
            "claim_text": (
                "The live staging surface for this run is !/CREWAI/, while the operator front "
                "door resolves through the configured daily note system and TO DO LIST.md."
            ),
            "anchor_value": "!/CREWAI/",
            "evidence_refs": [
                ".crewai/MANIFEST.md",
                "!/CREWAI/README.md",
                "DAILY NOTE TEMPLATE.md",
                ".github/scripts/daily_rollover.py",
                *backlog_refs,
            ],
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
            "claim_text": (
                "The loop stops before consecration so the candidate handling today's backlog "
                "does not lie about permissions."
            ),
            "anchor_value": "truthful threshold conduct",
            "evidence_refs": [
                "!/WAKEUP.md",
                "!/README.md",
                "CONSTITUTION.md",
                *backlog_refs,
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
    context: OperatorContext | None = None,
) -> FiveWizardsWorkflowInput:
    """Build one fixed, root-first workflow input for the threshold slice."""

    resolved_context = context or load_operator_context(root=repo_root())
    resolved_run_id = run_id or _timestamped_run_id()
    resolved_session_id = session_id or f"{resolved_run_id}-session"

    lane_runs: list[LaneRunInput] = []
    for domain in LaneDomain:
        spec = _lane_spec(domain, resolved_context)
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
            (
                f"Operator front door resolved through {resolved_context.daily_note_path} "
                "and TO DO LIST.md."
            ),
            f"Active backlog preview: {_backlog_preview(resolved_context)}",
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
            "The familiars agreed that the threshold run stayed root-first, touched "
            f"{resolved_context.daily_note_path} and TO DO LIST.md as the operator front "
            "door, staged only to !/CREWAI/, and did not pretend to self-promote."
        ),
        gaggle_evidence_refs=_dedupe(
            [
                *resolved_context.live_boot_chain_refs,
                *resolved_context.live_front_door_refs,
                ".crewai/MANIFEST.md",
            ]
        ),
    )


def _workflow_evidence_refs(workflow: FiveWizardsWorkflowInput) -> list[str]:
    refs = list(workflow.gaggle_evidence_refs)
    for lane_run in workflow.lane_runs:
        refs.extend(lane_run.wizard_note.evidence_refs)
        refs.extend(lane_run.familiar_note.evidence_refs)
        refs.extend(ref for claim in lane_run.claims for ref in claim.evidence_refs)
    return _dedupe(refs)


def _require_threshold_contract(
    context: OperatorContext,
    workflow: FiveWizardsWorkflowInput,
) -> None:
    bootstrap_report = build_contract_report_for_root(context.root)
    errors: list[str] = []

    if not bootstrap_report.ok:
        failed_checks = ", ".join(check.name for check in bootstrap_report.checks if not check.ok)
        errors.append(f"bootstrap contract failed: {failed_checks}")

    if not context.boot_chain_ok:
        errors.append(f"boot chain missing: {', '.join(context.missing_boot_chain)}")

    if not context.operator_front_door_ok:
        errors.append(
            "operator front door missing: "
            f"{', '.join(context.missing_operator_front_door)}"
        )

    evidence_statuses = evaluate_evidence_refs(_workflow_evidence_refs(workflow), root=context.root)
    invalid_evidence = [
        status.ref
        for status in evidence_statuses
        if not status.exists or status.tracked is False
    ]
    if invalid_evidence:
        errors.append(f"unresolved evidence refs: {', '.join(invalid_evidence)}")

    if errors:
        raise ThresholdContractError(
            "Threshold prereflight failed:\n- " + "\n- ".join(errors)
        )


def run_threshold_stage(
    *,
    run_id: str | None = None,
    materialize: bool = True,
    context: OperatorContext | None = None,
) -> FiveWizardsStageResult:
    """Execute the fixed threshold slice and stage it to !/CREWAI/ only."""

    resolved_context = context or load_operator_context(root=repo_root())
    workflow = build_threshold_workflow_input(run_id=run_id, context=resolved_context)
    _require_threshold_contract(resolved_context, workflow)
    request = FiveWizardsStageRequest(
        workflow=workflow,
        stage_root=str(threshold_stage_root(resolved_context.root)),
        materialize=materialize,
    )
    return run_and_stage_five_wizards(request)


def render_threshold_stage_summary(
    result: FiveWizardsStageResult,
    *,
    context: OperatorContext | None = None,
) -> str:
    """Render a short console summary for the threshold slice."""

    resolved_context = context or load_operator_context(root=repo_root())
    orientation = " -> ".join(ROOT_ORIENTATION_SURFACES)
    front_door = " -> ".join(OPERATOR_FRONT_DOOR_SURFACES)
    stage_root = (
        Path(result.stage_root)
        if result.stage_root is not None
        else threshold_stage_root(resolved_context.root)
    )
    pack_root = result.pack_root or str(stage_root / result.run_id)
    return "\n".join(
        [
            f"5Wizards threshold run `{result.run_id}`",
            f"- Boot chain validated: {orientation}",
            f"- Operator front door: {front_door}",
            f"- Current daily note: {resolved_context.daily_note_path}",
            f"- Active backlog items: {len(resolved_context.open_backlog_items)}",
            f"- Gate state: {result.workflow.gate_report.overall_state.value}",
            f"- Council ready: {'yes' if result.workflow.gate_report.council_ready else 'no'}",
            f"- Staging surface: {stage_root}",
            f"- Pack root: {pack_root}",
            "- Promotion: Logan approval is still required before anything staged becomes canon.",
        ]
    )
