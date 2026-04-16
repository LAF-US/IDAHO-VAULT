"""Pure-Python service layer for running and staging 5Wizards workflow executions."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from idaho_vault.five_wizards.staging import (
    ArtifactPack,
    build_workflow_artifact_pack,
    materialize_artifact_pack,
)
from idaho_vault.five_wizards.workflow import (
    FiveWizardsWorkflowArtifacts,
    FiveWizardsWorkflowInput,
    run_five_wizards_workflow,
)


class ServiceBaseModel(BaseModel):
    """Strict base model for service-layer request and result types."""

    model_config = ConfigDict(extra="forbid")


class FiveWizardsStageRequest(ServiceBaseModel):
    workflow: FiveWizardsWorkflowInput
    stage_root: str | None = None
    materialize: bool = False

    @model_validator(mode="after")
    def validate_request(self) -> "FiveWizardsStageRequest":
        if self.materialize and not self.stage_root:
            raise ValueError("A stage_root is required when materialize=true.")
        return self


class FiveWizardsStageResult(ServiceBaseModel):
    run_id: str = Field(min_length=1)
    workflow: FiveWizardsWorkflowArtifacts
    artifact_pack: ArtifactPack
    materialized: bool
    stage_root: str | None = None
    pack_root: str | None = None
    materialized_paths: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_result(self) -> "FiveWizardsStageResult":
        if self.workflow.run_id != self.run_id:
            raise ValueError("Service results must align workflow and result run ids.")
        if self.artifact_pack.run_id != self.run_id:
            raise ValueError("Service results must align artifact pack and result run ids.")
        if self.materialized:
            if not self.stage_root or not self.pack_root or not self.materialized_paths:
                raise ValueError("Materialized results require stage_root, pack_root, and materialized_paths.")
        else:
            if self.materialized_paths:
                raise ValueError("Dry-run service results must not report written paths.")
        return self


def _pack_root(stage_root: str, run_id: str) -> str:
    return str(Path(stage_root) / run_id)


def run_and_stage_five_wizards(request: FiveWizardsStageRequest) -> FiveWizardsStageResult:
    """Run the workflow, build the artifact pack, and optionally materialize it."""

    workflow = run_five_wizards_workflow(request.workflow)
    artifact_pack = build_workflow_artifact_pack(workflow)

    materialized_paths: list[str] = []
    pack_root: str | None = None
    if request.materialize and request.stage_root is not None:
        written = materialize_artifact_pack(artifact_pack, request.stage_root)
        materialized_paths = [str(path) for path in written]
        pack_root = _pack_root(request.stage_root, workflow.run_id)

    summary = (
        f"Run {workflow.run_id}: gate={workflow.gate_report.overall_state.value}; "
        f"council_ready={'yes' if workflow.gate_report.council_ready else 'no'}; "
        f"materialized={'yes' if request.materialize else 'no'}."
    )

    return FiveWizardsStageResult(
        run_id=workflow.run_id,
        workflow=workflow,
        artifact_pack=artifact_pack,
        materialized=request.materialize,
        stage_root=request.stage_root,
        pack_root=pack_root,
        materialized_paths=materialized_paths,
        summary=summary,
    )
