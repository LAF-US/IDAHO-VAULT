"""Compatibility surface for the WHY + THY lane runner."""

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


WhyClaimChallengeInput = LaneClaimChallengeInput
WhyClaimInput = LaneClaimInput
WhyLaneNoteInput = LaneNoteInput


class WhyLaneRunInput(LaneRunInput):
    lane_domain: LaneDomain = LaneDomain.WHY
    wizard_role: str | None = "meaning scholar"

    @model_validator(mode="after")
    def validate_why_lane(self) -> "WhyLaneRunInput":
        if self.lane_domain is not LaneDomain.WHY:
            raise ValueError("WhyLaneRunInput only supports `lane_domain=WHY`.")
        return self


class WhyLaneRunArtifacts(LaneRunArtifacts):
    lane_domain: LaneDomain = LaneDomain.WHY

    @model_validator(mode="after")
    def validate_why_lane(self) -> "WhyLaneRunArtifacts":
        if self.lane_domain is not LaneDomain.WHY:
            raise ValueError("WhyLaneRunArtifacts only supports `lane_domain=WHY`.")
        return self


def run_why_thy_lane(request: WhyLaneRunInput) -> WhyLaneRunArtifacts:
    """Execute the WHY + THY lane using the generic lane runner."""

    artifacts = run_lane(request)
    return WhyLaneRunArtifacts.model_validate(artifacts.model_dump())
