Project shape
Working title: CROSSFRAMING-US
Purpose: express the vault’s structural framing rules in Python so agents and tools can validate route maps, lane assignments, and house-level standing decisions from a closed grammar instead of from prose alone.

This should be small, typed, and testable.

What it should do
The project should support one core use case:

define one live operator loop
define the allowed vocabulary for that loop
define one driver lane per step
validate supporting/discouraged/out-of-jurisdiction lanes
render the loop back out as machine-readable JSON and human-readable Markdown
That is enough to prove the concept.

What it should not do
For a midterm-scale build, it should not:

replace 5Wizards
replace CrewAI
become a universal agent framework
own canon promotion logic
reach into external systems automatically
try to model every vault district at once
Keep it to framing, validation, and rendering.

Best fit in this repo
This should live as a small pure-Python package layer beside the existing domain code, following the same style as five_wizards and civic_scaffold.

A plausible package shape is:

src/idaho_vault/crossframing/
enums.py
models.py
validators.py
renderers.py
service.py
maybe one operator_loop.py or presets.py for the first worked loop
That mirrors the repo’s current habits and avoids inventing a new schema culture.

Core model
1. Closed enums
Use string enums for the framing grammar.

Minimum enums:

LifecyclePosture
LIVE
STAGED
RUNTIME
ARCHIVE
PermissionBoundary
LOCAL_READ
LOCAL_WRITE
EXTERNAL_READ
EXTERNAL_WRITE
ProductShape
NOTE
PLAN
STAGED_ARTIFACT
STATE_UPDATE
TRANSPORT_EVENT
RECOMMENDATION
LaneFamily
VAULT_NOTE
PYTHON_CORE
CREWAI
GITHUB
LINEAR
PLUGIN
LaneStatus
DRIVER
SUPPORTING
DISCOURAGED
OUT_OF_JURISDICTION
2. Models
Use strict Pydantic models with extra="forbid".

Minimum models:

LoopStep
step_id
title
goal
lifecycle_posture
permission_boundary
product_shape
driver_lane
supporting_lanes
discouraged_lanes
out_of_jurisdiction_lanes
OperatorLoopMap
loop_id
title
steps
notes
source_refs
DriverRule
explicit tie-break criteria, likely as metadata rather than dynamic scoring at first
3. Validation rules
This is the real point of the project.

Validators should enforce:

every step uses declared vocabulary only
every step has exactly one driver_lane
the driver lane cannot also appear in other lane lists
no lane appears in more than one bucket for the same step
every lane listed is in the closed LaneFamily enum
optional: forbid impossible combinations you already know are wrong
Examples of useful first-pass invariants:

EXTERNAL_WRITE steps should not be driven by VAULT_NOTE
TRANSPORT_EVENT steps should usually be driven by GITHUB
STAGED_ARTIFACT steps should not be driven by LINEAR
NOTE steps should usually begin in VAULT_NOTE
Do not overbuild heuristic logic yet. Hard validation first, soft recommendations second.

First preset
Ship with one hardcoded preset only:

daily-note-live-loop

intake
classify/plan
stage artifact
transport if needed
Logan review gate
That preset should reproduce the v2 map you already drafted, but as data plus validation rather than prose table only.

Outputs
The project should emit two outputs from the same model:

JSON
for machine consumption
exact enum values
Markdown
for vault filing
one clean table plus a short “fast reads” summary
That keeps the Python layer and the note layer aligned.

Suggested CLI surface
One CLI entrypoint is enough:

crossframe_operator_loop
Inputs:

maybe --preset daily-note-live-loop
Outputs:

print markdown summary
optionally write JSON and Markdown to a staging location
For a midterm, it is enough if it prints to stdout and supports a local write option later.

Test scope
Keep the test suite narrow and strict.

Minimum tests:

valid loop map passes
duplicate driver lane fails
undeclared lifecycle value fails
lane listed in two buckets fails
preset renders stable Markdown
preset serializes stable JSON
That is enough to prove it is not just a conceptual wrapper.

Why this is the right scale
This project is small enough to finish, but real enough to matter.

It does three useful things for the House:

moves key framing rules from essay-space into typed validation
gives future drafts a reusable grammar
creates a bridge between notes and machinery without pretending the machinery is the House itself
That is exactly the kind of “sturdy up the framing of the House” move that fits a midterm project.

Best implementation order
enums.py
models.py
validators.py
one preset loop
renderers.py
tests
optional CLI wrapper