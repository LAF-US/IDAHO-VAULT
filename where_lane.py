"""Compatibility surface for the WHERE + THERE lane runner."""

from __future__ import annotations

from pydantic import model_validator

from idaho_vault.five_wizards.enums import LaneDomain
from idaho_vault.five_wizards.lane_runner import (
    LaneClaimChallengeInput,
    LaneClaimInput,
    LaneNoteInput,
    LaneRunArtifacts,
    LaneRunInput,
    run_lane,
)


WhereClaimChallengeInput = LaneClaimChallengeInput
WhereClaimInput = LaneClaimInput
WhereLaneNoteInput = LaneNoteInput


class WhereLaneRunInput(LaneRunInput):
    lane_domain: LaneDomain = LaneDomain.WHERE
    wizard_role: str | None = "spatial scholar"

    @model_validator(mode="after")
    def validate_where_lane(self) -> "WhereLaneRunInput":
        if self.lane_domain is not LaneDomain.WHERE:
            raise ValueError("WhereLaneRunInput only supports `lane_domain=WHERE`.")
        return self


class WhereLaneRunArtifacts(LaneRunArtifacts):
    lane_domain: LaneDomain = LaneDomain.WHERE

    @model_validator(mode="after")
    def validate_where_lane(self) -> "WhereLaneRunArtifacts":
        if self.lane_domain is not LaneDomain.WHERE:
            raise ValueError("WhereLaneRunArtifacts only supports `lane_domain=WHERE`.")
        return self


def run_where_there_lane(request: WhereLaneRunInput) -> WhereLaneRunArtifacts:
    """Execute the WHERE + THERE lane using the generic lane runner."""

    artifacts = run_lane(request)
    return WhereLaneRunArtifacts.model_validate(artifacts.model_dump())
