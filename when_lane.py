"""Compatibility surface for the WHEN + THEN lane runner."""

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


WhenClaimChallengeInput = LaneClaimChallengeInput
WhenClaimInput = LaneClaimInput
WhenLaneNoteInput = LaneNoteInput


class WhenLaneRunInput(LaneRunInput):
    lane_domain: LaneDomain = LaneDomain.WHEN
    wizard_role: str | None = "temporal scholar"

    @model_validator(mode="after")
    def validate_when_lane(self) -> "WhenLaneRunInput":
        if self.lane_domain is not LaneDomain.WHEN:
            raise ValueError("WhenLaneRunInput only supports `lane_domain=WHEN`.")
        return self


class WhenLaneRunArtifacts(LaneRunArtifacts):
    lane_domain: LaneDomain = LaneDomain.WHEN

    @model_validator(mode="after")
    def validate_when_lane(self) -> "WhenLaneRunArtifacts":
        if self.lane_domain is not LaneDomain.WHEN:
            raise ValueError("WhenLaneRunArtifacts only supports `lane_domain=WHEN`.")
        return self


def run_when_then_lane(request: WhenLaneRunInput) -> WhenLaneRunArtifacts:
    """Execute the WHEN + THEN lane using the generic lane runner."""

    artifacts = run_lane(request)
    return WhenLaneRunArtifacts.model_validate(artifacts.model_dump())
