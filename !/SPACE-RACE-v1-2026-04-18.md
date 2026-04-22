---
title: "SPACE RACE v1"
date created: 2026-04-18
authority: LOGAN
doc_class: spec
status: draft
related:
  - CREWAI
  - CHAINFIRE
  - CLI
  - CONSTITUTION
  - VAULT-CONVENTIONS
  - "!/CREWAI/README.md"
  - ".crewai/MANIFEST.md"
  - ".github/scripts/topology_census.py"
  - "!/CREWAI/LINKER-SUMMARY-v1.md"
---

# SPACE RACE v1

*Filed 2026-04-18 as a spec-first surface for Logan's review. This note defines
an agency model and launch contract. It does not register a live CrewAI crew,
change runtime topology, or authorize direct writes outside staging.*

## Summary

`SPACE RACE` v1 is a single mission agency inside the vault.

It is modeled on launch-program discipline: schedule pressure, launch windows,
readiness, payload integrity, retrieval, and review.

Its opponent is not another internal agency yet. The rival is the broken
machine itself:

- delay
- drift
- false starts
- cycle-bind
- flame-pressure
- launch-window collapse

The agency exists to get lawful missions off the ground before those failure
modes harden into structural blockage.

## Agency Charter

`SPACE RACE` v1 is authorized to:

1. receive bounded mission briefs
2. survey target surfaces without widening scope
3. prepare typed staged payloads
4. return those payloads to Logan for review

`SPACE RACE` v1 is not authorized to:

- self-promote staged output into canon
- infer ontology from weak similarity
- treat broad content resemblance as relation proof
- present historical linker output as precedent
- modify live CrewAI registration on its own

## Agency Structure

### Mission Control

Mission Control is Logan alone.

Mission Control:

- approves mission charter
- names or accepts mission scope
- reviews staged payloads
- decides launch, deferment, or abort

### Program Office

The Program Office is the bounded mission-definition and orchestration layer.

In v1 it is represented by:

- this spec
- future Python orchestration
- staged machine-readable mission packets

It is not yet a separate live service or CrewAI body.

### Crawler

The Crawler is the broad-range survey craft.

Its job is to discover what is actually present on the target surface and emit
evidence only.

The Crawler may:

- inventory files and filenames
- read frontmatter presence and keys
- record headings and explicit links
- record anomalies and missing baseline structure

The Crawler may not:

- propose canon
- write repairs directly
- widen mission boundaries
- treat similarity as relation

### Linker

The Linker is the surface-contact repair craft.

Its job is to take crawler evidence and turn it into typed staged proposals.

The Linker may:

- consume crawler output
- emit typed repair proposals
- stage proposal cargo under `!/CREWAI/`

The Linker may not:

- free-associate from content resemblance
- write directly into note surfaces
- promote proposals into canon
- bypass Mission Control

## First Launch Program

The first launch program is a governed metadata-repair program.

Its mission family is:

- bounded governed Markdown subset
- baseline metadata survey
- lawful repair payload staging before drift spreads

### Crawler v1 scope

The Crawler inventories only enough truth to support baseline metadata repair:

- filename
- frontmatter presence
- frontmatter keys
- `title`
- `authority`
- `status`
- `related`
- headings
- explicit links

The Crawler may also emit anomaly evidence for:

- missing baseline fields
- malformed frontmatter
- malformed `related` lists
- duplicate `related` entries
- duplicate or collision candidates

Duplicate or collision candidates remain anomaly evidence in v1. They are not
link actions yet.

### Linker v1 scope

The Linker consumes crawler evidence and emits only these proposal types:

- `missing_baseline_field`
- `frontmatter_related_repair`

Everything else is out of scope for the first launch.

## Launch State Model

`SPACE RACE` v1 uses launch states rather than generic workflow labels.

| State | Meaning |
| --- | --- |
| `briefed` | Mission need recorded but not yet bounded |
| `scoped` | Target paths and mission limits fixed |
| `window-open` | Authority, timing, and staging path are ready |
| `surveying` | Crawler is gathering evidence |
| `linking` | Linker is generating typed proposals from evidence |
| `payload-staged` | Cargo exists in `!/CREWAI/` but is not canonical |
| `retrieved` | Payload is ready for Logan review |
| `reviewed` | Mission Control has examined the payload |
| `launched` | Logan approved promotion into a durable live surface |
| `aborted` | Mission stood down without pretending partial work was a launch |

Hard rule:

**A staged payload is not a launch.**

Launch occurs only at the Logan review gate.

## Artifact Contract

The agency's cargo hold and launch bay is `!/CREWAI/`.

Each mission should stage to:

`!/CREWAI/space-race/<mission_id>/`

Required staged artifacts:

- `mission_packet.json`
- `launch_readiness.json`
- `crawl_report.json`
- `surface_index.json`
- `anomaly_report.md`
- `edge_proposals.json`
- `link_plan.json`
- `payload_summary.md`

### `launch_readiness.json`

This contract should confirm:

- mission scope is bounded
- authority refs are present
- evidence pass completed
- no out-of-scope writes are proposed
- proposal types are v1-legal only
- return path to Logan review is intact

## Public Interfaces

Future runtime interfaces for this system are:

### `MissionPacket`

Defines:

- mission identity
- mission type
- authority refs
- target scope
- launch window
- staging path

### `LaunchReadiness`

Defines the go/no-go contract for whether a payload is lawful to stage and
retrieve.

### `CrawlReport`

Summarizes evidence gathered by the Crawler.

### `SurfaceIndex`

Stores normalized per-note structural inventory for the mission scope.

### `AnomalyRecord`

Stores issue evidence without granting repair authority by itself.

### `EdgeProposal`

Stores typed repair proposals with:

- proposal type
- source path
- target ref or field target
- evidence refs
- confidence

### `LinkPlan`

Groups staged proposal cargo into one reviewable payload.

## Relation To Existing Machinery

This agency remains separate from live CrewAI topology in v1.

Therefore:

- `.crewai/MANIFEST.md` remains unchanged
- no live crawler/linker crew is claimed
- historical harbor notes remain historical
- the older linker payload is treated as a negative precedent, not a reusable
  result

The failure mode to avoid is already visible in the historical linker output:

- weak similarity
- untyped proposals
- junk edges
- relation inflation without authority

`topology_census.py` is adjacent machinery and may become a future merge
candidate, but it is not the first launch program.

## Guardrails

The agency must keep these limits:

- transport and staging are not canon
- evidence is not proposal
- proposal is not launch
- launch is not self-authorization
- similarity is not relation
- survival of an old output is not legitimacy

## Acceptance Checks

This spec is correct only if it leaves the following truths intact:

1. `SPACE RACE` is an agency, not just a metaphor.
2. The opposing force is the broken machine and its failure modes.
3. The Crawler remains evidence-only.
4. The Linker remains proposal-only.
5. The first launch program is metadata repair, not broad entity graphing.
6. `payload-staged` and `launched` remain distinct states.
7. `!/CREWAI/` remains the singular staging surface.
8. CrewAI manifest and live runtime topology remain unchanged in this pass.

## Default Assumptions

- `SPACE RACE` v1 is one agency, not a two-agency simulation.
- The "other team" is implemented as machine failure pressure for now.
- The tone is launch-program urgency, not borrowed franchise imitation.
- The first success condition is a lawful staged repair payload that survives
  Logan review.
