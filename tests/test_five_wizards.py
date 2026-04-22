from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.five_wizards.enums import (
    AnchorType,
    ClaimConfidence,
    ClaimStatus,
    CouncilDomain,
    CouncilReportStatus,
    CouncilSessionStatus,
    FamiliarId,
    FamiliarMode,
    GateState,
    InstitutionId,
    LaneDomain,
    MirageCategory,
    NoteAuthorKind,
    NoteVisibility,
    ObjectionScope,
    ObjectionSeverity,
    ObjectionStatus,
    SurfaceMode,
    WizardEntityId,
    WizardPersonalityId,
    lane_inquiry_prompt,
    COUNCIL_INQUIRY_PROMPT,
)
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
from idaho_vault.five_wizards.renderers import (
    render_claim_markdown,
    render_council_repo***REMOVED***markdown,
    render_council_session_markdown,
    render_familiar_gaggle_markdown,
    render_gate_repo***REMOVED***markdown,
    render_objection_markdown,
    render_personal_note_markdown,
    render_validation_verdict_markdown,
    to_canonical_json,
)
from idaho_vault.five_wizards.pipelines import (
    awaken_council,
    challenge_council_report,
    convene_council,
    create_personal_note,
    draft_council_report,
    finalize_council_report,
    record_familiar_gaggle,
)
from idaho_vault.five_wizards.lane_runner import (
    LaneClaimChallengeInput,
    LaneClaimInput,
    LaneNoteInput,
    LaneRunInput,
    run_lane,
)
from idaho_vault.five_wizards.staging import (
    build_lane_artifact_pack,
    build_workflow_artifact_pack,
    materialize_artifact_pack,
)
from idaho_vault.five_wizards.service import (
    FiveWizardsStageRequest,
    run_and_stage_five_wizards,
)
from idaho_vault.five_wizards.who_lane import WhoLaneRunInput, run_who_thou_lane
from idaho_vault.five_wizards.when_lane import WhenLaneRunInput, run_when_then_lane
from idaho_vault.five_wizards.where_lane import WhereLaneRunInput, run_where_there_lane
from idaho_vault.five_wizards.why_lane import WhyLaneRunInput, run_why_thy_lane
from idaho_vault.five_wizards.what_lane import (
    WhatClaimChallengeInput,
    WhatClaimInput,
    WhatLaneNoteInput,
    WhatLaneRunInput,
    run_what_that_lane,
)
from idaho_vault.five_wizards.workflow import (
    FiveWizardsWorkflowInput,
    run_five_wizards_workflow,
)
from idaho_vault.five_wizards.validators import adjudicate_claim, build_gate_report


class FiveWizardsTest(unittest.TestCase):
    def make_claim(self, domain: LaneDomain = LaneDomain.WHO) -> Claim:
        if domain is LaneDomain.WHO:
            return Claim(
                claim_id="who-001",
                run_id="run-001",
                domain=LaneDomain.WHO,
                entity=WizardEntityId.WHO,
                personality=WizardPersonalityId.WHO,
                surface_mode=SurfaceMode.LANE,
                wizard_role="identity scholar",
                familiar=FamiliarId.THOU,
                familiar_mode=None,
                text="Logan is identified as the author.",
                anchor_type=AnchorType.THOU,
                anchor_value="Logan",
                evidence_refs=["src-01#l1"],
                confidence=ClaimConfidence.GROUNDED,
                status=ClaimStatus.PROPOSED,
                objections=[],
            )
        if domain is LaneDomain.WHAT:
            return Claim(
                claim_id="what-001",
                run_id="run-001",
                domain=LaneDomain.WHAT,
                entity=WizardEntityId.WHAT,
                personality=WizardPersonalityId.WHAT,
                surface_mode=SurfaceMode.LANE,
                wizard_role="content scholar",
                familiar=FamiliarId.THAT,
                familiar_mode=None,
                text="The document defines a schema foundation.",
                anchor_type=AnchorType.THAT,
                anchor_value="schema foundation",
                evidence_refs=["src-02#p3"],
                confidence=ClaimConfidence.GROUNDED,
                status=ClaimStatus.PROPOSED,
                objections=[],
            )
        if domain is LaneDomain.WHEN:
            return Claim(
                claim_id="when-001",
                run_id="run-001",
                domain=LaneDomain.WHEN,
                entity=WizardEntityId.WHEN,
                personality=WizardPersonalityId.WHEN,
                surface_mode=SurfaceMode.LANE,
                wizard_role="temporal scholar",
                familiar=FamiliarId.THEN,
                familiar_mode=None,
                text="The update happened on 2026-04-15.",
                anchor_type=AnchorType.THEN,
                anchor_value="2026-04-15",
                evidence_refs=["src-03#l9"],
                confidence=ClaimConfidence.GROUNDED,
                status=ClaimStatus.PROPOSED,
                objections=[],
            )
        if domain is LaneDomain.WHERE:
            return Claim(
                claim_id="where-001",
                run_id="run-001",
                domain=LaneDomain.WHERE,
                entity=WizardEntityId.WHERE,
                personality=WizardPersonalityId.WHERE,
                surface_mode=SurfaceMode.LANE,
                wizard_role="spatial scholar",
                familiar=FamiliarId.THERE,
                familiar_mode=None,
                text="The file lives in src/idaho_vault.",
                anchor_type=AnchorType.THERE,
                anchor_value="src/idaho_vault",
                evidence_refs=["src-04#l2"],
                confidence=ClaimConfidence.GROUNDED,
                status=ClaimStatus.PROPOSED,
                objections=[],
            )
        if domain is LaneDomain.WHY:
            return Claim(
                claim_id="why-001",
                run_id="run-001",
                domain=LaneDomain.WHY,
                entity=WizardEntityId.WHY,
                personality=WizardPersonalityId.WHY,
                surface_mode=SurfaceMode.LANE,
                wizard_role="meaning scholar",
                familiar=FamiliarId.THY_THE,
                familiar_mode=FamiliarMode.THY,
                text="The schema exists to preserve objections durably.",
                anchor_type=AnchorType.THY,
                anchor_value="durable objection handling",
                evidence_refs=["src-05#l4"],
                confidence=ClaimConfidence.GROUNDED,
                status=ClaimStatus.PROPOSED,
                objections=[],
            )
        raise AssertionError(f"Unsupported test domain: {domain}")

    def make_personal_note(self, domain: LaneDomain = LaneDomain.WHO) -> PersonalNote:
        claim = self.make_claim(domain)
        return PersonalNote(
            note_id=f"{domain.value.lower()}-note-001",
            run_id=claim.run_id,
            domain=claim.domain,
            author_kind=NoteAuthorKind.WIZARD,
            entity=claim.entity,
            personality=claim.personality,
            surface_mode=claim.surface_mode,
            familiar=claim.familiar,
            familiar_mode=claim.familiar_mode,
            text=f"Private note for {domain.value}.",
            evidence_refs=claim.evidence_refs,
            inquiry_question=lane_inquiry_prompt(domain),
            recurring_questions=[lane_inquiry_prompt(domain)],
            cautions=["Do not mistake a title for a true name."],
            unresolved_tensions=["One actor remains unnamed."],
            visibility=NoteVisibility.PAIR_PRIVATE,
            include_in_final_report=True,
        )

    def make_lane_objection(self) -> Objection:
        return Objection(
            objection_id="obj-001",
            run_id="run-001",
            target_claim_id="who-001",
            scope=ObjectionScope.LANE,
            lane_domain=LaneDomain.WHO,
            council_domain=None,
            entity=WizardEntityId.WHO,
            personality=WizardPersonalityId.WHO,
            surface_mode=SurfaceMode.LANE,
            familiar=FamiliarId.THOU,
            familiar_mode=None,
            severity=ObjectionSeverity.NOTE,
            category=MirageCategory.OVERREACH,
            text="The attribution needs stronger corroboration.",
            evidence_refs=["src-01#l2"],
            status=ObjectionStatus.OPEN,
            resolution_note=None,
        )

    def make_council_objection(self) -> Objection:
        return Objection(
            objection_id="obj-002",
            run_id="run-001",
            target_claim_id="why-001",
            scope=ObjectionScope.COUNCIL,
            lane_domain=None,
            council_domain=CouncilDomain.HOW,
            entity=WizardEntityId.WHY,
            personality=WizardPersonalityId.HOW,
            surface_mode=SurfaceMode.COUNCIL,
            familiar=FamiliarId.THY_THE,
            familiar_mode=FamiliarMode.THE,
            severity=ObjectionSeverity.CONCERN,
            category=MirageCategory.CONTRADICTORY_EVIDENCE,
            text="The council wants more evidence before synthesis.",
            evidence_refs=["src-05#l5"],
            status=ObjectionStatus.ADDRESSED,
            resolution_note="Tracked for later council review.",
        )

    def make_council_report(self, domain: LaneDomain = LaneDomain.WHO) -> CouncilReport:
        claim = self.make_claim(domain)
        note = self.make_personal_note(domain)
        return CouncilReport(
            repo***REMOVED***id=f"{domain.value.lower()}-report-001",
            run_id=claim.run_id,
            domain=claim.domain,
            entity=claim.entity,
            personality=claim.personality,
            surface_mode=claim.surface_mode,
            wizard_role=claim.wizard_role,
            familiar=claim.familiar,
            familiar_mode=claim.familiar_mode,
            status=CouncilReportStatus.FINALIZED,
            personal_note_ids=[note.note_id],
            challenge_objection_ids=[],
            inquiry_question=lane_inquiry_prompt(domain),
            unresolved_questions=["What still resists closure here?"],
            cautions=["Do not mistake a function for a being."],
            council_text=f"Council report for {domain.value}.",
            evidence_refs=claim.evidence_refs,
        )

    def make_familiar_gaggle_note(self) -> FamiliarGaggleNote:
        return FamiliarGaggleNote(
            note_id="gaggle-001",
            run_id="run-001",
            council_domain=CouncilDomain.HOW,
            host_entity=WizardEntityId.WHY,
            host_personality=WizardPersonalityId.HOW,
            host_surface_mode=SurfaceMode.COUNCIL,
            host_familiar=FamiliarId.THY_THE,
            host_familiar_mode=FamiliarMode.THE,
            participant_familiars=[
                FamiliarId.THOU,
                FamiliarId.THAT,
                FamiliarId.THEN,
                FamiliarId.THERE,
                FamiliarId.THY_THE,
            ],
            participant_modes=[None, None, None, None, FamiliarMode.THY],
            watched_repo***REMOVED***ids=["who-report-001", "why-report-001"],
            gossip_text="The familiars traded skeptical notes while the council debated.",
            evidence_refs=["src-06#l1"],
            include_in_final_report=True,
        )

    def make_council_session(self) -> CouncilSession:
        return CouncilSession(
            session_id="session-001",
            run_id="run-001",
            council_domain=CouncilDomain.HOW,
            convener_entity=WizardEntityId.WHY,
            convener_personality=WizardPersonalityId.HOW,
            convener_surface_mode=SurfaceMode.COUNCIL,
            convener_familiar=FamiliarId.THY_THE,
            convener_familiar_mode=FamiliarMode.THE,
            status=CouncilSessionStatus.CONVENED,
            council_repo***REMOVED***ids=[f"{domain.value.lower()}-report-001" for domain in LaneDomain],
            familiar_gaggle_note_ids=["gaggle-001"],
            inquiry_question=COUNCIL_INQUIRY_PROMPT,
            debate_threads=[
                "How should the council hold relation without forcing closure?",
                "Which lane still carries unresolved danger?",
            ],
            method_warnings=[
                "Read before naming.",
                "Do not mistake passage for ownership.",
            ],
            debate_summary="HOW awakened the council and opened debate across the five lanes.",
            outcome_summary="The council adjourned pending final synthesis.",
        )

    def make_pipeline_final_report(self, domain: LaneDomain) -> CouncilReport:
        claim = self.make_claim(domain)
        wizard_note = create_personal_note(
            note_id=f"{domain.value.lower()}-wizard-note-pipeline",
            run_id=claim.run_id,
            domain=domain,
            author_kind=NoteAuthorKind.WIZARD,
            text=f"{domain.value} wizard note.",
            evidence_refs=claim.evidence_refs,
            cautions=["Read before naming."],
            unresolved_tensions=["One thread remains unsettled."],
        )
        familiar_note = create_personal_note(
            note_id=f"{domain.value.lower()}-familiar-note-pipeline",
            run_id=claim.run_id,
            domain=domain,
            author_kind=NoteAuthorKind.FAMILIAR,
            text=f"{domain.value} familiar note.",
            evidence_refs=[f"{claim.claim_id}#challenge"],
            cautions=["Do not mistake passage for ownership."],
            unresolved_tensions=["One challenge still shadows the lane."],
        )
        draft = draft_council_report(
            repo***REMOVED***id=f"{domain.value.lower()}-pipeline-report",
            run_id=claim.run_id,
            domain=domain,
            wizard_role=claim.wizard_role,
            council_text=f"Draft council report for {domain.value}.",
            personal_notes=[wizard_note, familiar_note],
        )
        return finalize_council_report(
            draft,
            final_council_text=f"Final council report for {domain.value}.",
        )

    def make_lane_run_input(
        self,
        domain: LaneDomain,
        *,
        fatal_open: bool = False,
        missing_evidence: bool = False,
    ) -> LaneRunInput:
        claim = self.make_claim(domain)
        challenges: list[LaneClaimChallengeInput] = []
        if fatal_open:
            challenges.append(
                LaneClaimChallengeInput(
                    objection_id=f"{domain.value.lower()}-lane-open-fatal",
                    text=f"{domain.value} lane challenge remains open.",
                    category=MirageCategory.OVERREACH,
                    severity=ObjectionSeverity.FATAL,
                    evidence_refs=[f"{claim.claim_id}#challenge"],
                    status=ObjectionStatus.OPEN,
                )
            )

        return LaneRunInput(
            lane_domain=domain,
            run_id=claim.run_id,
            repo***REMOVED***id=f"{domain.value.lower()}-lane-run-report",
            claims=[
                LaneClaimInput(
                    claim_id=f"{domain.value.lower()}-lane-run-claim",
                    text=claim.text,
                    anchor_value=claim.anchor_value,
                    evidence_refs=[] if missing_evidence else claim.evidence_refs,
                    confidence=claim.confidence,
                    challenges=challenges,
                )
            ],
            wizard_note=LaneNoteInput(
                note_id=f"{domain.value.lower()}-wizard-lane-note",
                text=f"{domain.value} wizard lane note.",
                evidence_refs=claim.evidence_refs,
                cautions=["Read before naming."],
            ),
            familiar_note=LaneNoteInput(
                note_id=f"{domain.value.lower()}-familiar-lane-note",
                text=f"{domain.value} familiar lane note.",
                evidence_refs=[f"{claim.claim_id}#familiar"],
                cautions=["Do not mistake a function for a being."],
            ),
        )

    def test_valid_lane_mappings(self) -> None:
        for domain in LaneDomain:
            claim = self.make_claim(domain)
            self.assertEqual(claim.domain, domain)

    def test_why_and_how_switch_modes(self) -> None:
        why_claim = self.make_claim(LaneDomain.WHY)
        how_objection = self.make_council_objection()
        self.assertEqual(why_claim.entity, WizardEntityId.WHY)
        self.assertEqual(why_claim.personality, WizardPersonalityId.WHY)
        self.assertEqual(why_claim.surface_mode, SurfaceMode.LANE)
        self.assertEqual(why_claim.familiar, FamiliarId.THY_THE)
        self.assertEqual(why_claim.familiar_mode, FamiliarMode.THY)
        self.assertEqual(how_objection.entity, WizardEntityId.WHY)
        self.assertEqual(how_objection.personality, WizardPersonalityId.HOW)
        self.assertEqual(how_objection.surface_mode, SurfaceMode.COUNCIL)
        self.assertEqual(how_objection.familiar, FamiliarId.THY_THE)
        self.assertEqual(how_objection.familiar_mode, FamiliarMode.THE)

    def test_personal_note_round_trip(self) -> None:
        note = self.make_personal_note(LaneDomain.WHY)
        restored = PersonalNote.model_validate_json(to_canonical_json(note))
        self.assertEqual(restored, note)

    def test_objection_round_trip_lane_and_council(self) -> None:
        for objection in (self.make_lane_objection(), self.make_council_objection()):
            payload = to_canonical_json(objection)
            restored = Objection.model_validate_json(payload)
            self.assertEqual(restored, objection)

    def test_council_repo***REMOVED***round_trip(self) -> None:
        report = self.make_council_report(LaneDomain.WHY)
        restored = CouncilReport.model_validate_json(to_canonical_json(report))
        self.assertEqual(restored, report)

    def test_familiar_gaggle_and_council_session_round_trip(self) -> None:
        gaggle = self.make_familiar_gaggle_note()
        session = self.make_council_session()
        restored_gaggle = FamiliarGaggleNote.model_validate_json(to_canonical_json(gaggle))
        restored_session = CouncilSession.model_validate_json(to_canonical_json(session))
        self.assertEqual(restored_gaggle, gaggle)
        self.assertEqual(restored_session, session)

    def test_claim_fails_without_anchor(self) -> None:
        claim = self.make_claim()
        broken = claim.model_copy(update={"anchor_value": "   "})
        verdict = adjudicate_claim(broken)
        self.assertEqual(verdict.status, ClaimStatus.FAIL)
        self.assertEqual(verdict.reason, "missing_anchor")

    def test_claim_fails_without_evidence(self) -> None:
        claim = self.make_claim()
        broken = claim.model_copy(update={"evidence_refs": []})
        verdict = adjudicate_claim(broken)
        self.assertEqual(verdict.status, ClaimStatus.FAIL)
        self.assertEqual(verdict.reason, "missing_evidence")

    def test_claim_disputed_for_fatal_open_objection(self) -> None:
        fatal = self.make_lane_objection().model_copy(update={"severity": ObjectionSeverity.FATAL})
        claim = self.make_claim().model_copy(update={"objections": [fatal]})
        verdict = adjudicate_claim(claim)
        self.assertEqual(verdict.status, ClaimStatus.DISPUTED)
        self.assertEqual(verdict.blocking_objection_ids, [fatal.objection_id])

    def test_claim_blocked_for_invalid_mapping(self) -> None:
        claim = Claim.model_construct(
            claim_id="who-001",
            run_id="run-001",
            institution=InstitutionId.FIVE_WIZARDS,
            domain=LaneDomain.WHO,
            entity=WizardEntityId.WHAT,
            personality=WizardPersonalityId.WHAT,
            surface_mode=SurfaceMode.LANE,
            wizard_role="identity scholar",
            familiar=FamiliarId.THOU,
            familiar_mode=None,
            text="Logan is identified as the author.",
            anchor_type=AnchorType.THOU,
            anchor_value="Logan",
            evidence_refs=["src-01#l1"],
            confidence=ClaimConfidence.GROUNDED,
            status=ClaimStatus.PROPOSED,
            objections=[],
        )
        verdict = adjudicate_claim(claim)
        self.assertEqual(verdict.status, ClaimStatus.BLOCKED)
        self.assertEqual(verdict.reason, "invalid_mapping")

    def test_gate_aggregation_states(self) -> None:
        pass_verdicts = [adjudicate_claim(self.make_claim(domain)) for domain in LaneDomain]
        green = build_gate_report(pass_verdicts)
        self.assertEqual(green.overall_state, GateState.GREEN)
        self.assertTrue(green.council_ready)

        disputed_claim = self.make_claim(LaneDomain.WHO).model_copy(
            update={
                "objections": [
                    self.make_lane_objection().model_copy(update={"severity": ObjectionSeverity.FATAL})
                ]
            }
        )
        yellow_verdicts = [
            adjudicate_claim(disputed_claim),
            adjudicate_claim(self.make_claim(LaneDomain.WHAT)),
            adjudicate_claim(self.make_claim(LaneDomain.WHEN)),
            adjudicate_claim(self.make_claim(LaneDomain.WHERE)),
            adjudicate_claim(self.make_claim(LaneDomain.WHY)),
        ]
        yellow = build_gate_report(yellow_verdicts)
        self.assertEqual(yellow.overall_state, GateState.YELLOW)
        self.assertFalse(yellow.council_ready)

        red_claim = self.make_claim(LaneDomain.WHAT).model_copy(update={"evidence_refs": []})
        red_verdicts = [
            adjudicate_claim(self.make_claim(LaneDomain.WHO)),
            adjudicate_claim(red_claim),
            adjudicate_claim(self.make_claim(LaneDomain.WHEN)),
            adjudicate_claim(self.make_claim(LaneDomain.WHERE)),
            adjudicate_claim(self.make_claim(LaneDomain.WHY)),
        ]
        red = build_gate_report(red_verdicts)
        self.assertEqual(red.overall_state, GateState.RED)
        self.assertFalse(red.council_ready)

    def test_pipeline_transitions_private_notes_to_final_council_report(self) -> None:
        wizard_note = create_personal_note(
            note_id="who-wizard-note-002",
            run_id="run-001",
            domain=LaneDomain.WHO,
            author_kind=NoteAuthorKind.WIZARD,
            text="Wizard private note.",
            evidence_refs=["src-01#l1"],
            cautions=["Read before naming."],
            unresolved_tensions=["One witness still remains unnamed."],
        )
        familiar_note = create_personal_note(
            note_id="who-familiar-note-002",
            run_id="run-001",
            domain=LaneDomain.WHO,
            author_kind=NoteAuthorKind.FAMILIAR,
            text="Familiar private note.",
            evidence_refs=["src-01#l2"],
            cautions=["Do not mistake a title for a true name."],
            unresolved_tensions=["The attribution remains pressurized."],
        )

        draft = draft_council_report(
            repo***REMOVED***id="who-report-pipeline-002",
            run_id="run-001",
            domain=LaneDomain.WHO,
            wizard_role="identity scholar",
            council_text="Initial council report.",
            personal_notes=[wizard_note, familiar_note],
        )
        self.assertEqual(draft.status, CouncilReportStatus.DRAFT)
        self.assertEqual(draft.personal_note_ids, [wizard_note.note_id, familiar_note.note_id])
        self.assertIn("The attribution remains pressurized.", draft.unresolved_questions)
        self.assertIn("Read before naming.", draft.cautions)

        objection = self.make_lane_objection().model_copy(
            update={"status": ObjectionStatus.ADDRESSED}
        )
        challenged = challenge_council_report(
            draft,
            [objection],
            revised_council_text="Council report after familiar pressure-testing.",
            unresolved_questions=["Who is still missing from the record?"],
            cautions=["Look both ways at a crossroads."],
        )
        self.assertEqual(challenged.status, CouncilReportStatus.CHALLENGED)
        self.assertEqual(challenged.challenge_objection_ids, [objection.objection_id])
        self.assertIn("Who is still missing from the record?", challenged.unresolved_questions)
        self.assertIn("Look both ways at a crossroads.", challenged.cautions)

        finalized = finalize_council_report(
            challenged,
            [objection],
            final_council_text="Final council report.",
            evidence_refs=["src-09#l4"],
        )
        self.assertEqual(finalized.status, CouncilReportStatus.FINALIZED)
        self.assertEqual(finalized.council_text, "Final council report.")
        self.assertIn("src-09#l4", finalized.evidence_refs)

    def test_pipeline_rejects_open_fatal_challenge_during_finalization(self) -> None:
        draft = draft_council_report(
            repo***REMOVED***id="who-report-pipeline-003",
            run_id="run-001",
            domain=LaneDomain.WHO,
            wizard_role="identity scholar",
            council_text="Initial council report.",
            personal_notes=[
                create_personal_note(
                    note_id="who-wizard-note-003",
                    run_id="run-001",
                    domain=LaneDomain.WHO,
                    author_kind=NoteAuthorKind.WIZARD,
                    text="Wizard note.",
                    evidence_refs=["src-01#l1"],
                )
            ],
        )
        fatal_objection = self.make_lane_objection().model_copy(
            update={"severity": ObjectionSeverity.FATAL}
        )
        challenged = challenge_council_report(draft, [fatal_objection])
        with self.assertRaisesRegex(ValueError, "fatal challenge objections remain open"):
            finalize_council_report(challenged, [fatal_objection])

    def test_pipeline_awakens_and_convenes_full_council(self) -> None:
        reports = [self.make_pipeline_final_report(domain) for domain in LaneDomain]
        gaggle = record_familiar_gaggle(
            note_id="gaggle-pipeline-001",
            run_id="run-001",
            council_reports=reports,
            gossip_text="The familiars watched, compared notes, and kept score.",
        )
        awakened = awaken_council(session_id="session-pipeline-001", run_id="run-001")
        session = convene_council(
            awakened,
            council_reports=reports,
            familiar_gaggle_notes=[gaggle],
            debate_threads=[
                "How should the council keep relation without forcing closure?",
                "Which lane carries the sharpest unresolved risk?",
            ],
            method_warnings=["Read before naming."],
            debate_summary="HOW convened the council after every lane finalized its report.",
            outcome_summary="The council entered formal debate.",
        )

        self.assertEqual(session.status, CouncilSessionStatus.CONVENED)
        self.assertEqual(session.council_repo***REMOVED***ids, [report.repo***REMOVED***id for report in reports])
        self.assertEqual(session.familiar_gaggle_note_ids, [gaggle.note_id])
        self.assertEqual(session.convener_entity, WizardEntityId.WHY)
        self.assertEqual(session.convener_personality, WizardPersonalityId.HOW)
        self.assertEqual(session.convener_surface_mode, SurfaceMode.COUNCIL)
        self.assertEqual(gaggle.participant_familiars[-1], FamiliarId.THY_THE)
        self.assertEqual(gaggle.participant_modes[-1], FamiliarMode.THY)

    def test_pipeline_requires_all_five_lanes_to_convene_council(self) -> None:
        awakened = awaken_council(session_id="session-pipeline-002", run_id="run-001")
        partial_reports = [self.make_pipeline_final_report(LaneDomain.WHO)]
        with self.assertRaisesRegex(ValueError, "five lanes"):
            convene_council(awakened, council_reports=partial_reports)

    def test_what_lane_runner_green_path(self) -> None:
        request = WhatLaneRunInput(
            run_id="run-what-001",
            repo***REMOVED***id="what-report-operator-001",
            claims=[
                WhatClaimInput(
                    claim_id="what-operator-001",
                    text="The artifact is a schema foundation document.",
                    anchor_value="schema foundation document",
                    evidence_refs=["src-what-01#l1"],
                    challenges=[
                        WhatClaimChallengeInput(
                            objection_id="what-obj-001",
                            text="The label should stay tied to the document text.",
                            category=MirageCategory.OVERREACH,
                            severity=ObjectionSeverity.CONCERN,
                            evidence_refs=["src-what-01#l2"],
                            status=ObjectionStatus.ADDRESSED,
                            resolution_note="Language tightened in the report.",
                        )
                    ],
                )
            ],
            wizard_note=WhatLaneNoteInput(
                note_id="what-wizard-note-operator-001",
                text="The document behaves like a schema foundation.",
                evidence_refs=["src-what-01#l1"],
                cautions=["Read before naming."],
                unresolved_tensions=["The document title could drift from the evidence."],
            ),
            familiar_note=WhatLaneNoteInput(
                note_id="what-familiar-note-operator-001",
                text="Keep the artifact claim close to its exact language.",
                evidence_refs=["src-what-01#l2"],
                cautions=["Do not mistake a function for a being."],
            ),
        )

        result = run_what_that_lane(request)

        self.assertEqual(result.lane_domain, LaneDomain.WHAT)
        self.assertEqual(result.wizard_note.author_kind, NoteAuthorKind.WIZARD)
        self.assertEqual(result.familiar_note.author_kind, NoteAuthorKind.FAMILIAR)
        self.assertEqual(result.lane_state, GateState.GREEN)
        self.assertTrue(result.council_ready)
        self.assertIsNotNone(result.finalized_report)
        self.assertEqual(result.challenged_report.status, CouncilReportStatus.CHALLENGED)
        self.assertEqual(result.finalized_report.status, CouncilReportStatus.FINALIZED)
        self.assertEqual(result.verdicts[0].status, ClaimStatus.PASS)
        self.assertEqual(result.blocking_claim_ids, [])
        self.assertIn("state=green", result.summary)

    def test_what_lane_runner_withholds_final_repo***REMOVED***for_open_fatal_objection(self) -> None:
        request = WhatLaneRunInput(
            run_id="run-what-002",
            repo***REMOVED***id="what-report-operator-002",
            claims=[
                WhatClaimInput(
                    claim_id="what-operator-002",
                    text="The artifact definitively proves the larger thesis.",
                    anchor_value="larger thesis artifact",
                    evidence_refs=["src-what-02#l1"],
                    challenges=[
                        WhatClaimChallengeInput(
                            objection_id="what-obj-002",
                            text="The claim overreaches what the artifact can support.",
                            category=MirageCategory.OVERREACH,
                            severity=ObjectionSeverity.FATAL,
                            evidence_refs=["src-what-02#l4"],
                            status=ObjectionStatus.OPEN,
                        )
                    ],
                )
            ],
            wizard_note=WhatLaneNoteInput(
                note_id="what-wizard-note-operator-002",
                text="The artifact may support a narrower conclusion.",
                evidence_refs=["src-what-02#l1"],
            ),
            familiar_note=WhatLaneNoteInput(
                note_id="what-familiar-note-operator-002",
                text="The evidence does not justify the larger thesis claim.",
                evidence_refs=["src-what-02#l4"],
            ),
        )

        result = run_what_that_lane(request)

        self.assertEqual(result.lane_state, GateState.YELLOW)
        self.assertFalse(result.council_ready)
        self.assertIsNone(result.finalized_report)
        self.assertEqual(result.verdicts[0].status, ClaimStatus.DISPUTED)
        self.assertEqual(result.blocking_objection_ids, ["what-obj-002"])
        self.assertIn("finalization_withheld", result.summary)

    def test_what_lane_runner_red_state_can_still_finalize_report(self) -> None:
        request = WhatLaneRunInput(
            run_id="run-what-003",
            repo***REMOVED***id="what-report-operator-003",
            claims=[
                WhatClaimInput(
                    claim_id="what-operator-003",
                    text="The artifact exists but has no cited support here.",
                    anchor_value="uncited artifact",
                    evidence_refs=[],
                )
            ],
            wizard_note=WhatLaneNoteInput(
                note_id="what-wizard-note-operator-003",
                text="The artifact is present but under-cited.",
                evidence_refs=["src-what-03#l1"],
            ),
            familiar_note=WhatLaneNoteInput(
                note_id="what-familiar-note-operator-003",
                text="The lane should surface the missing evidence explicitly.",
                evidence_refs=["src-what-03#l2"],
            ),
        )

        result = run_what_that_lane(request)

        self.assertEqual(result.lane_state, GateState.RED)
        self.assertFalse(result.council_ready)
        self.assertIsNotNone(result.finalized_report)
        self.assertEqual(result.finalized_report.status, CouncilReportStatus.FINALIZED)
        self.assertEqual(result.verdicts[0].status, ClaimStatus.FAIL)
        self.assertEqual(result.blocking_claim_ids, ["what-operator-003"])
        self.assertIn("failed=1", result.summary)

    def test_what_lane_runner_round_trip(self) -> None:
        request = WhatLaneRunInput(
            run_id="run-what-004",
            repo***REMOVED***id="what-report-operator-004",
            claims=[
                WhatClaimInput(
                    claim_id="what-operator-004",
                    text="The artifact is a ledger.",
                    anchor_value="ledger artifact",
                    evidence_refs=["src-what-04#l1"],
                )
            ],
            wizard_note=WhatLaneNoteInput(
                note_id="what-wizard-note-operator-004",
                text="Wizard note for the ledger artifact.",
                evidence_refs=["src-what-04#l1"],
            ),
            familiar_note=WhatLaneNoteInput(
                note_id="what-familiar-note-operator-004",
                text="Familiar note for the ledger artifact.",
                evidence_refs=["src-what-04#l2"],
            ),
        )

        result = run_what_that_lane(request)
        restored_request = WhatLaneRunInput.model_validate_json(to_canonical_json(request))
        self.assertEqual(restored_request, request)
        restored_result = type(result).model_validate_json(to_canonical_json(result))
        self.assertEqual(restored_result, result)

    def test_generic_lane_runner_supports_who_lane(self) -> None:
        request = LaneRunInput(
            lane_domain=LaneDomain.WHO,
            run_id="run-who-001",
            repo***REMOVED***id="who-report-operator-001",
            claims=[
                LaneClaimInput(
                    claim_id="who-operator-001",
                    text="Logan is identified as the reporter of record.",
                    anchor_value="Logan Finney",
                    evidence_refs=["src-who-01#l1"],
                    challenges=[
                        LaneClaimChallengeInput(
                            objection_id="who-obj-001",
                            text="The title should stay tied to the byline evidence.",
                            category=MirageCategory.OVERREACH,
                            severity=ObjectionSeverity.CONCERN,
                            evidence_refs=["src-who-01#l2"],
                            status=ObjectionStatus.ADDRESSED,
                        )
                    ],
                )
            ],
            wizard_note=LaneNoteInput(
                note_id="who-wizard-note-operator-001",
                text="The byline identifies the reporting actor.",
                evidence_refs=["src-who-01#l1"],
            ),
            familiar_note=LaneNoteInput(
                note_id="who-familiar-note-operator-001",
                text="Keep identity claims close to the exact naming evidence.",
                evidence_refs=["src-who-01#l2"],
            ),
        )

        result = run_lane(request)

        self.assertEqual(result.lane_domain, LaneDomain.WHO)
        self.assertEqual(result.claims[0].entity, WizardEntityId.WHO)
        self.assertEqual(result.claims[0].personality, WizardPersonalityId.WHO)
        self.assertEqual(result.claims[0].familiar, FamiliarId.THOU)
        self.assertIsNone(result.claims[0].familiar_mode)
        self.assertEqual(result.lane_state, GateState.GREEN)
        self.assertTrue(result.council_ready)
        self.assertIn("WHO lane produced 1 claims", result.summary)

    def test_generic_lane_runner_supports_why_split_brain_lane(self) -> None:
        request = LaneRunInput(
            lane_domain=LaneDomain.WHY,
            run_id="run-why-001",
            repo***REMOVED***id="why-report-operator-001",
            claims=[
                LaneClaimInput(
                    claim_id="why-operator-001",
                    text="The schema exists to preserve durable objections.",
                    anchor_value="durable objection handling",
                    evidence_refs=["src-why-01#l1"],
                )
            ],
            wizard_note=LaneNoteInput(
                note_id="why-wizard-note-operator-001",
                text="The rationale centers durable disagreement handling.",
                evidence_refs=["src-why-01#l1"],
            ),
            familiar_note=LaneNoteInput(
                note_id="why-familiar-note-operator-001",
                text="Guard against inventing motives beyond the evidence.",
                evidence_refs=["src-why-01#l2"],
            ),
        )

        result = run_lane(request)

        self.assertEqual(result.lane_domain, LaneDomain.WHY)
        self.assertEqual(result.claims[0].entity, WizardEntityId.WHY)
        self.assertEqual(result.claims[0].personality, WizardPersonalityId.WHY)
        self.assertEqual(result.claims[0].surface_mode, SurfaceMode.LANE)
        self.assertEqual(result.claims[0].familiar, FamiliarId.THY_THE)
        self.assertEqual(result.claims[0].familiar_mode, FamiliarMode.THY)
        self.assertEqual(result.wizard_note.familiar_mode, FamiliarMode.THY)
        self.assertEqual(result.lane_state, GateState.GREEN)
        self.assertTrue(result.council_ready)

    def test_generic_lane_runner_round_trip(self) -> None:
        request = LaneRunInput(
            lane_domain=LaneDomain.WHERE,
            run_id="run-where-001",
            repo***REMOVED***id="where-report-operator-001",
            claims=[
                LaneClaimInput(
                    claim_id="where-operator-001",
                    text="The file lives in src/idaho_vault/five_wizards.",
                    anchor_value="src/idaho_vault/five_wizards",
                    evidence_refs=["src-where-01#l1"],
                )
            ],
            wizard_note=LaneNoteInput(
                note_id="where-wizard-note-operator-001",
                text="The path is anchored inside the five_wizards package.",
                evidence_refs=["src-where-01#l1"],
            ),
            familiar_note=LaneNoteInput(
                note_id="where-familiar-note-operator-001",
                text="Keep the path claim precise at directory level.",
                evidence_refs=["src-where-01#l2"],
            ),
        )

        result = run_lane(request)
        restored_request = LaneRunInput.model_validate_json(to_canonical_json(request))
        self.assertEqual(restored_request, request)
        restored_result = type(result).model_validate_json(to_canonical_json(result))
        self.assertEqual(restored_result, result)

    def test_lane_wrappers_cover_remaining_domains(self) -> None:
        who_request = WhoLaneRunInput.model_validate(self.make_lane_run_input(LaneDomain.WHO).model_dump())
        when_request = WhenLaneRunInput.model_validate(self.make_lane_run_input(LaneDomain.WHEN).model_dump())
        where_request = WhereLaneRunInput.model_validate(self.make_lane_run_input(LaneDomain.WHERE).model_dump())
        why_request = WhyLaneRunInput.model_validate(self.make_lane_run_input(LaneDomain.WHY).model_dump())

        who_result = run_who_thou_lane(who_request)
        when_result = run_when_then_lane(when_request)
        where_result = run_where_there_lane(where_request)
        why_result = run_why_thy_lane(why_request)

        self.assertEqual(who_result.lane_domain, LaneDomain.WHO)
        self.assertEqual(who_result.claims[0].familiar, FamiliarId.THOU)
        self.assertEqual(when_result.lane_domain, LaneDomain.WHEN)
        self.assertEqual(when_result.claims[0].familiar, FamiliarId.THEN)
        self.assertEqual(where_result.lane_domain, LaneDomain.WHERE)
        self.assertEqual(where_result.claims[0].familiar, FamiliarId.THERE)
        self.assertEqual(why_result.lane_domain, LaneDomain.WHY)
        self.assertEqual(why_result.claims[0].entity, WizardEntityId.WHY)
        self.assertEqual(why_result.claims[0].personality, WizardPersonalityId.WHY)
        self.assertEqual(why_result.claims[0].familiar, FamiliarId.THY_THE)
        self.assertEqual(why_result.claims[0].familiar_mode, FamiliarMode.THY)

    def test_workflow_awakens_and_convenes_green_run(self) -> None:
        workflow_input = FiveWizardsWorkflowInput(
            run_id="run-001",
            session_id="workflow-session-001",
            familiar_gaggle_note_id="workflow-gaggle-001",
            lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
            awaken_method_warnings=["Read before naming."],
            convene_debate_threads=["How should the five lanes be held together responsibly?"],
        )

        workflow = run_five_wizards_workflow(workflow_input)

        self.assertEqual(workflow.awakened_session.status, CouncilSessionStatus.AWAKENED)
        self.assertEqual(workflow.gate_report.overall_state, GateState.GREEN)
        self.assertTrue(workflow.gate_report.council_ready)
        self.assertIsNotNone(workflow.familiar_gaggle_note)
        self.assertIsNotNone(workflow.convened_session)
        self.assertEqual(workflow.convened_session.status, CouncilSessionStatus.CONVENED)
        self.assertEqual(
            [lane_result.lane_domain for lane_result in workflow.lane_results],
            list(LaneDomain),
        )
        self.assertIn("gate=green", workflow.summary)

    def test_workflow_holds_at_awakened_when_gate_not_green(self) -> None:
        lane_runs = [self.make_lane_run_input(domain) for domain in LaneDomain]
        lane_runs[1] = self.make_lane_run_input(LaneDomain.WHAT, missing_evidence=True)
        workflow_input = FiveWizardsWorkflowInput(
            run_id="run-001",
            session_id="workflow-session-002",
            lane_runs=lane_runs,
        )

        workflow = run_five_wizards_workflow(workflow_input)

        self.assertEqual(workflow.awakened_session.status, CouncilSessionStatus.AWAKENED)
        self.assertEqual(workflow.gate_report.overall_state, GateState.RED)
        self.assertFalse(workflow.gate_report.council_ready)
        self.assertIsNone(workflow.familiar_gaggle_note)
        self.assertIsNone(workflow.convened_session)
        self.assertIn(LaneDomain.WHAT, workflow.gate_report.blocking_domains)

    def test_workflow_round_trip(self) -> None:
        workflow_input = FiveWizardsWorkflowInput(
            run_id="run-001",
            session_id="workflow-session-003",
            lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
        )
        workflow = run_five_wizards_workflow(workflow_input)

        restored_input = FiveWizardsWorkflowInput.model_validate_json(to_canonical_json(workflow_input))
        self.assertEqual(restored_input, workflow_input)
        restored_workflow = type(workflow).model_validate_json(to_canonical_json(workflow))
        self.assertEqual(restored_workflow, workflow)

    def test_lane_artifact_pack_contains_dual_format_outputs(self) -> None:
        lane_result = run_lane(self.make_lane_run_input(LaneDomain.WHO))
        pack = build_lane_artifact_pack(lane_result)

        self.assertEqual(pack.run_id, lane_result.run_id)
        self.assertEqual(pack.root_dir_name, lane_result.run_id)
        self.assertTrue(
            any(artifact.relative_path.endswith("lane-artifact-manifest.json") for artifact in pack.artifacts)
        )
        self.assertTrue(
            any("lane/who/claims/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertTrue(
            any(artifact.media_type == "text/markdown" for artifact in pack.artifacts)
        )
        self.assertTrue(
            any(artifact.media_type == "application/json" for artifact in pack.artifacts)
        )

    def test_workflow_artifact_pack_includes_council_outputs_for_green_run(self) -> None:
        workflow = run_five_wizards_workflow(
            FiveWizardsWorkflowInput(
                run_id="run-001",
                session_id="workflow-session-004",
                familiar_gaggle_note_id="workflow-gaggle-004",
                lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
            )
        )
        pack = build_workflow_artifact_pack(workflow)

        self.assertTrue(
            any("council/how/workflow/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertTrue(
            any("council/how/gate/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertTrue(
            any("council/how/gaggle/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertTrue(
            any("council/how/sessions/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertTrue(
            any("lane/why/" in artifact.relative_path for artifact in pack.artifacts)
        )

    def test_workflow_artifact_pack_omits_convened_artifacts_when_not_green(self) -> None:
        lane_runs = [self.make_lane_run_input(domain) for domain in LaneDomain]
        lane_runs[2] = self.make_lane_run_input(LaneDomain.WHEN, fatal_open=True)
        workflow = run_five_wizards_workflow(
            FiveWizardsWorkflowInput(
                run_id="run-001",
                session_id="workflow-session-005",
                lane_runs=lane_runs,
            )
        )
        pack = build_workflow_artifact_pack(workflow)

        self.assertFalse(workflow.gate_report.council_ready)
        self.assertFalse(
            any("council/how/gaggle/" in artifact.relative_path for artifact in pack.artifacts)
        )
        self.assertEqual(
            sum("council/how/sessions/" in artifact.relative_path for artifact in pack.artifacts),
            2,
        )

    def test_materialize_artifact_pack_writes_to_selected_root(self) -> None:
        lane_result = run_lane(self.make_lane_run_input(LaneDomain.WHERE))
        pack = build_lane_artifact_pack(lane_result)

        tempdir = Path.cwd() / "_tmp_five_wizards_artifacts"
        try:
            shutil.rmtree(tempdir, ignore_errors=True)
            tempdir.mkdir(exist_ok=True)
            written = materialize_artifact_pack(pack, tempdir)
            pack_root = tempdir / pack.run_id
            self.assertTrue(pack_root.exists())
            self.assertEqual(len(written), len(pack.artifacts))
            manifest_path = pack_root / "meta" / f"{pack.run_id}__lane-artifact-manifest.json"
            self.assertTrue(manifest_path.exists())
            manifest_text = manifest_path.read_text(encoding="utf-8")
            self.assertIn('"artifact_count"', manifest_text)
        finally:
            shutil.rmtree(tempdir, ignore_errors=True)

    def test_run_and_stage_service_supports_dry_run(self) -> None:
        request = FiveWizardsStageRequest(
            workflow=FiveWizardsWorkflowInput(
                run_id="run-001",
                session_id="workflow-session-006",
                lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
            ),
            materialize=False,
        )

        result = run_and_stage_five_wizards(request)

        self.assertFalse(result.materialized)
        self.assertIsNone(result.pack_root)
        self.assertEqual(result.materialized_paths, [])
        self.assertEqual(result.workflow.run_id, "run-001")
        self.assertEqual(result.artifact_pack.run_id, "run-001")
        self.assertIn("materialized=no", result.summary)

    def test_run_and_stage_service_materializes_to_selected_root(self) -> None:
        tempdir = Path.cwd() / "_tmp_five_wizards_service"
        try:
            shutil.rmtree(tempdir, ignore_errors=True)
            tempdir.mkdir(exist_ok=True)
            request = FiveWizardsStageRequest(
                workflow=FiveWizardsWorkflowInput(
                    run_id="run-001",
                    session_id="workflow-session-007",
                    lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
                ),
                stage_root=str(tempdir),
                materialize=True,
            )

            result = run_and_stage_five_wizards(request)

            self.assertTrue(result.materialized)
            self.assertEqual(result.pack_root, str(tempdir / "run-001"))
            self.assertGreater(len(result.materialized_paths), 0)
            self.assertTrue((tempdir / "run-001").exists())
            self.assertTrue(
                any(path.endswith("workflow-artifact-manifest.json") for path in result.materialized_paths)
            )
            self.assertIn("materialized=yes", result.summary)
        finally:
            shutil.rmtree(tempdir, ignore_errors=True)

    def test_run_and_stage_service_requires_stage_root_when_materializing(self) -> None:
        with self.assertRaisesRegex(ValueError, "stage_root is required"):
            FiveWizardsStageRequest(
                workflow=FiveWizardsWorkflowInput(
                    run_id="run-001",
                    session_id="workflow-session-008",
                    lane_runs=[self.make_lane_run_input(domain) for domain in LaneDomain],
                ),
                materialize=True,
            )

    def test_json_round_trip_for_core_schemas(self) -> None:
        claim = self.make_claim(LaneDomain.WHY)
        verdict = adjudicate_claim(claim)
        report = build_gate_report([adjudicate_claim(self.make_claim(domain)) for domain in LaneDomain])
        for model, model_type in (
            (claim, Claim),
            (self.make_personal_note(LaneDomain.WHY), PersonalNote),
            (self.make_lane_objection(), Objection),
            (self.make_council_report(LaneDomain.WHY), CouncilReport),
            (self.make_familiar_gaggle_note(), FamiliarGaggleNote),
            (self.make_council_session(), CouncilSession),
            (verdict, ValidationVerdict),
            (report, GateReport),
        ):
            payload = to_canonical_json(model)
            restored = model_type.model_validate_json(payload)
            self.assertEqual(restored, model)

    def test_markdown_renderers_include_required_context(self) -> None:
        note = self.make_personal_note(LaneDomain.WHY)
        claim = self.make_claim(LaneDomain.WHY)
        objection = self.make_council_objection()
        council_report = self.make_council_report(LaneDomain.WHY)
        gaggle = self.make_familiar_gaggle_note()
        session = self.make_council_session()
        verdict = adjudicate_claim(claim)
        report = build_gate_report([adjudicate_claim(self.make_claim(domain)) for domain in LaneDomain])

        note_md = render_personal_note_markdown(note)
        self.assertIn("PAIR-PRIVATE", note_md.upper())
        self.assertIn("THY_THE[THY]", note_md)
        self.assertIn("Inquiry Question", note_md)
        self.assertIn("Recurring Questions", note_md)
        self.assertIn("Cautions", note_md)
        self.assertIn("Unresolved Tensions", note_md)

        claim_md = render_claim_markdown(claim)
        self.assertIn("WHY", claim_md)
        self.assertIn("THY_THE[THY]", claim_md)
        self.assertIn("src-05#l4", claim_md)

        objection_md = render_objection_markdown(objection)
        self.assertIn("COUNCIL", objection_md.upper())
        self.assertIn("THY_THE[THE]", objection_md)
        self.assertIn("contradictory-evidence", objection_md)

        council_repo***REMOVED***md = render_council_repo***REMOVED***markdown(council_report)
        self.assertIn("finalized", council_repo***REMOVED***md)
        self.assertIn("THY_THE[THY]", council_repo***REMOVED***md)
        self.assertIn("Unresolved Questions", council_repo***REMOVED***md)
        self.assertIn("Cautions", council_repo***REMOVED***md)

        gaggle_md = render_familiar_gaggle_markdown(gaggle)
        self.assertIn("Gossip Text", gaggle_md)
        self.assertIn("THY_THE[THE]", gaggle_md)

        session_md = render_council_session_markdown(session)
        self.assertIn("CONVENED", session_md.upper())
        self.assertIn("Convener Entity", session_md)
        self.assertIn("Convener Personality", session_md)
        self.assertIn("HOW", session_md)
        self.assertIn("Method Warnings", session_md)
        self.assertIn("Debate Threads", session_md)

        verdict_md = render_validation_verdict_markdown(verdict)
        self.assertIn("pass", verdict_md)
        self.assertIn("Surface Mode", verdict_md)

        repo***REMOVED***md = render_gate_repo***REMOVED***markdown(report)
        self.assertIn("HOW", repo***REMOVED***md)
        self.assertIn("Council Entity", repo***REMOVED***md)
        self.assertIn("Council Personality", repo***REMOVED***md)
        self.assertIn("green", repo***REMOVED***md)


if __name__ == "__main__":
    unittest.main()
