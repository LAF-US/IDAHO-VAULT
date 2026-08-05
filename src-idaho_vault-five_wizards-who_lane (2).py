"""Compatibility surface for the WHO + THOU lane runner."""

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


WhoClaimChallengeInput = LaneClaimChallengeInput
WhoClaimInput = LaneClaimInput
WhoLaneNoteInput = LaneNoteInput


class WhoLaneRunInput(LaneRunInput):
    lane_domain: LaneDomain = LaneDomain.WHO
    wizard_role: str | None = "identity scholar"

    @model_validator(mode="after")
    def validate_who_lane(self) -> "WhoLaneRunInput":
        if self.lane_domain is not LaneDomain.WHO:
            raise ValueError("WhoLaneRunInput only supports `lane_domain=WHO`.")
        return self


class WhoLaneRunArtifacts(LaneRunArtifacts):
    lane_domain: LaneDomain = LaneDomain.WHO

    @model_validator(mode="after")
    def validate_who_lane(self) -> "WhoLaneRunArtifacts":
        if self.lane_domain is not LaneDomain.WHO:
            raise ValueError("WhoLaneRunArtifacts only supports `lane_domain=WHO`.")
        return self


def run_who_thou_lane(request: WhoLaneRunInput) -> WhoLaneRunArtifacts:
    """Execute the WHO + THOU lane using the generic lane runner."""

    artifacts = run_lane(request)
    return WhoLaneRunArtifacts.model_validate(artifacts.model_dump())
