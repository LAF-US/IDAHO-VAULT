"""Compatibility surface for the WHAT + THAT lane runner."""

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


WhatClaimChallengeInput = LaneClaimChallengeInput
WhatClaimInput = LaneClaimInput
WhatLaneNoteInput = LaneNoteInput


class WhatLaneRunInput(LaneRunInput):
    lane_domain: LaneDomain = LaneDomain.WHAT
    wizard_role: str | None = "content scholar"

    @model_validator(mode="after")
    def validate_what_lane(self) -> "WhatLaneRunInput":
        if self.lane_domain is not LaneDomain.WHAT:
            raise ValueError("WhatLaneRunInput only supports `lane_domain=WHAT`.")
        return self


class WhatLaneRunArtifacts(LaneRunArtifacts):
    lane_domain: LaneDomain = LaneDomain.WHAT

    @model_validator(mode="after")
    def validate_what_lane(self) -> "WhatLaneRunArtifacts":
        if self.lane_domain is not LaneDomain.WHAT:
            raise ValueError("WhatLaneRunArtifacts only supports `lane_domain=WHAT`.")
        return self


def run_what_that_lane(request: WhatLaneRunInput) -> WhatLaneRunArtifacts:
    """Execute the WHAT + THAT lane using the generic lane runner."""

    artifacts = run_lane(request)
    return WhatLaneRunArtifacts.model_validate(artifacts.model_dump())
