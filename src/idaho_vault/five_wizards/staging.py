"""Artifact pack assembly and optional local materialization for 5Wizards runs."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.lane_runner import LaneRunArtifacts
from idaho_vault.five_wizards.renderers import (
    artifact_filename,
    council_artifact_group,
    lane_artifact_group,
    render_claim_markdown,
    render_council_repo***REMOVED***markdown,
    render_council_session_markdown,
    render_familiar_gaggle_markdown,
    render_gate_repo***REMOVED***markdown,
    render_lane_run_markdown,
    render_objection_markdown,
    render_personal_note_markdown,
    render_validation_verdict_markdown,
    render_workflow_markdown,
    to_canonical_json,
)
from idaho_vault.five_wizards.workflow import FiveWizardsWorkflowArtifacts


class StagedArtifact(BaseModel):
    """One staged artifact file within a run pack."""

    model_config = ConfigDict(extra="forbid")

    group: str = Field(min_length=1)
    relative_path: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    source_id: str | None = None
    content: str

    @model_validator(mode="after")
    def validate_relative_path(self) -> "StagedArtifact":
        normalized = self.relative_path.replace("\\", "/")
        if normalized.startswith("/") or normalized.startswith("../") or "/../" in normalized:
            raise ValueError("Staged artifact paths must remain relative to the pack root.")
        return self


class ArtifactPack(BaseModel):
    """A stable in-memory run pack of staged artifacts."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    root_dir_name: str = Field(min_length=1)
    artifacts: list[StagedArtifact]
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_paths(self) -> "ArtifactPack":
        if self.root_dir_name != self.run_id:
            raise ValueError("Artifact pack root_dir_name must match the run id.")
        relative_paths = [artifact.relative_path for artifact in self.artifacts]
        if len(relative_paths) != len(set(relative_paths)):
            raise ValueError("Artifact pack paths must be unique.")
        return self


def _json_artifact(
    *,
    group: str,
    relative_path: str,
    source_type: str,
    source_id: str | None,
    content: str,
) -> StagedArtifact:
    return StagedArtifact(
        group=group,
        relative_path=relative_path,
        media_type="application/json",
        source_type=source_type,
        source_id=source_id,
        content=content,
    )


def _markdown_artifact(
    *,
    group: str,
    relative_path: str,
    source_type: str,
    source_id: str | None,
    content: str,
) -> StagedArtifact:
    return StagedArtifact(
        group=group,
        relative_path=relative_path,
        media_type="text/markdown",
        source_type=source_type,
        source_id=source_id,
        content=content,
    )


def _pair_artifacts(
    *,
    group: str,
    directory: str,
    run_id: str,
    stem: str,
    source_type: str,
    source_id: str | None,
    json_content: str,
    markdown_content: str,
) -> list[StagedArtifact]:
    json_name = artifact_filename(run_id, stem, "json")
    markdown_name = artifact_filename(run_id, stem, "md")
    return [
        _json_artifact(
            group=group,
            relative_path=f"{directory}/{json_name}",
            source_type=source_type,
            source_id=source_id,
            content=json_content,
        ),
        _markdown_artifact(
            group=group,
            relative_path=f"{directory}/{markdown_name}",
            source_type=source_type,
            source_id=source_id,
            content=markdown_content,
        ),
    ]


def _lane_entries(lane_run: LaneRunArtifacts) -> list[StagedArtifact]:
    group = lane_artifact_group(lane_run.lane_domain)
    artifacts: list[StagedArtifact] = []

    artifacts.extend(
        _pair_artifacts(
            group=group,
            directory=f"{group}/bundle",
            run_id=lane_run.run_id,
            stem=f"lane-run-{lane_run.lane_domain.value.lower()}",
            source_type="lane-run",
            source_id=lane_run.lane_domain.value,
            json_content=to_canonical_json(lane_run),
            markdown_content=render_lane_run_markdown(lane_run),
        )
    )

    for note in (lane_run.wizard_note, lane_run.familiar_note):
        artifacts.extend(
            _pair_artifacts(
                group=group,
                directory=f"{group}/notes",
                run_id=lane_run.run_id,
                stem=f"personal-note-{note.note_id}",
                source_type="personal-note",
                source_id=note.note_id,
                json_content=to_canonical_json(note),
                markdown_content=render_personal_note_markdown(note),
            )
        )

    for claim in lane_run.claims:
        artifacts.extend(
            _pair_artifacts(
                group=group,
                directory=f"{group}/claims",
                run_id=lane_run.run_id,
                stem=f"claim-{claim.claim_id}",
                source_type="claim",
                source_id=claim.claim_id,
                json_content=to_canonical_json(claim),
                markdown_content=render_claim_markdown(claim),
            )
        )

    for objection in lane_run.objections:
        artifacts.extend(
            _pair_artifacts(
                group=group,
                directory=f"{group}/objections",
                run_id=lane_run.run_id,
                stem=f"objection-{objection.objection_id}",
                source_type="objection",
                source_id=objection.objection_id,
                json_content=to_canonical_json(objection),
                markdown_content=render_objection_markdown(objection),
            )
        )

    for verdict in lane_run.verdicts:
        artifacts.extend(
            _pair_artifacts(
                group=group,
                directory=f"{group}/verdicts",
                run_id=lane_run.run_id,
                stem=f"verdict-{verdict.claim_id}",
                source_type="validation-verdict",
                source_id=verdict.claim_id,
                json_content=to_canonical_json(verdict),
                markdown_content=render_validation_verdict_markdown(verdict),
            )
        )

    repo***REMOVED***specs = [
        ("draft", lane_run.draft_report),
        ("challenged", lane_run.challenged_report),
    ]
    if lane_run.finalized_report is not None:
        repo***REMOVED***specs.append(("finalized", lane_run.finalized_report))
    for stage_name, report in repo***REMOVED***specs:
        artifacts.extend(
            _pair_artifacts(
                group=group,
                directory=f"{group}/reports",
                run_id=lane_run.run_id,
                stem=f"council-report-{stage_name}-{report.repo***REMOVED***id}",
                source_type="council-report",
                source_id=report.repo***REMOVED***id,
                json_content=to_canonical_json(report),
                markdown_content=render_council_repo***REMOVED***markdown(report),
            )
        )

    return artifacts


def _pack_manifest(pack: ArtifactPack) -> str:
    manifest = {
        "run_id": pack.run_id,
        "root_dir_name": pack.root_dir_name,
        "artifact_count": len(pack.artifacts),
        "summary": pack.summary,
        "artifacts": [
            {
                "group": artifact.group,
                "relative_path": artifact.relative_path,
                "media_type": artifact.media_type,
                "source_type": artifact.source_type,
                "source_id": artifact.source_id,
            }
            for artifact in pack.artifacts
        ],
    }
    return json.dumps(manifest, indent=2, so***REMOVED***keys=True)


def build_lane_artifact_pack(lane_run: LaneRunArtifacts) -> ArtifactPack:
    """Build a stable dual-format artifact pack for one lane run."""

    artifacts = _lane_entries(lane_run)
    pack = ArtifactPack(
        run_id=lane_run.run_id,
        root_dir_name=lane_run.run_id,
        artifacts=artifacts,
        summary=f"Lane artifact pack for {lane_run.lane_domain.value}: {lane_run.summary}",
    )
    manifest_artifact = _json_artifact(
        group="meta",
        relative_path=f"meta/{artifact_filename(lane_run.run_id, 'lane-artifact-manifest', 'json')}",
        source_type="artifact-pack-manifest",
        source_id=lane_run.lane_domain.value,
        content=_pack_manifest(pack),
    )
    summary_artifact = _markdown_artifact(
        group="meta",
        relative_path=f"meta/{artifact_filename(lane_run.run_id, 'lane-artifact-summary', 'md')}",
        source_type="artifact-pack-summary",
        source_id=lane_run.lane_domain.value,
        content=render_lane_run_markdown(lane_run),
    )
    return ArtifactPack(
        run_id=pack.run_id,
        root_dir_name=pack.root_dir_name,
        artifacts=[manifest_artifact, summary_artifact, *pack.artifacts],
        summary=pack.summary,
    )


def build_workflow_artifact_pack(workflow: FiveWizardsWorkflowArtifacts) -> ArtifactPack:
    """Build a stable dual-format artifact pack for the full workflow run."""

    artifacts: list[StagedArtifact] = []
    for lane_result in workflow.lane_results:
        artifacts.extend(_lane_entries(lane_result))

    council_group = council_artifact_group()
    artifacts.extend(
        _pair_artifacts(
            group=council_group,
            directory=f"{council_group}/workflow",
            run_id=workflow.run_id,
            stem="workflow-run",
            source_type="workflow-run",
            source_id=workflow.run_id,
            json_content=to_canonical_json(workflow),
            markdown_content=render_workflow_markdown(workflow),
        )
    )
    artifacts.extend(
        _pair_artifacts(
            group=council_group,
            directory=f"{council_group}/gate",
            run_id=workflow.run_id,
            stem="gate-report",
            source_type="gate-report",
            source_id=workflow.run_id,
            json_content=to_canonical_json(workflow.gate_report),
            markdown_content=render_gate_repo***REMOVED***markdown(workflow.gate_report),
        )
    )
    artifacts.extend(
        _pair_artifacts(
            group=council_group,
            directory=f"{council_group}/sessions",
            run_id=workflow.run_id,
            stem=f"council-session-awakened-{workflow.awakened_session.session_id}",
            source_type="council-session",
            source_id=workflow.awakened_session.session_id,
            json_content=to_canonical_json(workflow.awakened_session),
            markdown_content=render_council_session_markdown(workflow.awakened_session),
        )
    )
    if workflow.familiar_gaggle_note is not None:
        artifacts.extend(
            _pair_artifacts(
                group=council_group,
                directory=f"{council_group}/gaggle",
                run_id=workflow.run_id,
                stem=f"familiar-gaggle-{workflow.familiar_gaggle_note.note_id}",
                source_type="familiar-gaggle-note",
                source_id=workflow.familiar_gaggle_note.note_id,
                json_content=to_canonical_json(workflow.familiar_gaggle_note),
                markdown_content=render_familiar_gaggle_markdown(workflow.familiar_gaggle_note),
            )
        )
    if workflow.convened_session is not None:
        artifacts.extend(
            _pair_artifacts(
                group=council_group,
                directory=f"{council_group}/sessions",
                run_id=workflow.run_id,
                stem=f"council-session-convened-{workflow.convened_session.session_id}",
                source_type="council-session",
                source_id=workflow.convened_session.session_id,
                json_content=to_canonical_json(workflow.convened_session),
                markdown_content=render_council_session_markdown(workflow.convened_session),
            )
        )

    pack = ArtifactPack(
        run_id=workflow.run_id,
        root_dir_name=workflow.run_id,
        artifacts=artifacts,
        summary=f"Workflow artifact pack: {workflow.summary}",
    )
    manifest_artifact = _json_artifact(
        group="meta",
        relative_path=f"meta/{artifact_filename(workflow.run_id, 'workflow-artifact-manifest', 'json')}",
        source_type="artifact-pack-manifest",
        source_id=workflow.run_id,
        content=_pack_manifest(pack),
    )
    summary_artifact = _markdown_artifact(
        group="meta",
        relative_path=f"meta/{artifact_filename(workflow.run_id, 'workflow-artifact-summary', 'md')}",
        source_type="artifact-pack-summary",
        source_id=workflow.run_id,
        content=render_workflow_markdown(workflow),
    )
    return ArtifactPack(
        run_id=pack.run_id,
        root_dir_name=pack.root_dir_name,
        artifacts=[manifest_artifact, summary_artifact, *pack.artifacts],
        summary=pack.summary,
    )


def materialize_artifact_pack(pack: ArtifactPack, root: str | Path) -> list[Path]:
    """Write an artifact pack beneath a chosen local root and return written paths."""

    root_path = Path(root)
    pack_root = root_path / pack.root_dir_name
    pack_root.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    for artifact in pack.artifacts:
        artifact_path = pack_root / Path(artifact.relative_path)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(artifact.content, encoding="utf-8")
        written_paths.append(artifact_path)
    return written_paths
