---
title: "Report - Metadata and Frontmatter Findings"
date created: 2026-04-18
authority: codex
doc_class: report
status: active
related:
  - "VAULT-METADATA-STANDARD.md"
  - "VAULT-TEMPLATES.md"
  - "DAILY NOTE TEMPLATE.md"
  - "!/PLUGIN-REGISTRY.md"
  - ".github/scripts/metadata_survey.py"
  - "tests/test_metadata_survey.py"
  - ".github/scripts/daily_rollover.py"
  - ".github/scripts/tidy_daily_notes.py"
  - ".github/scripts/validate_content.py"
source:
  - "live metadata survey run on 2026-04-18"
  - "repo doctrine readback"
---

# Report - Metadata and Frontmatter Findings

## Scope

This report records the current metadata/frontmatter state of `IDAHO-VAULT`
with two standards in view:

- cleanliness and logic
- vaulted agent utility

The point is not to propose a total rewrite.
The point is to say what the current machine state actually is, where the drift
really lives, and what the next lawful repair seam should be.

## Findings

### Finding 1

`[P1]` The main problem is schema fragmentation, not merely missing frontmatter.

The live survey scanned `32,084` markdown files.
Of those:

- `11,542` have valid frontmatter
- `19,637` have no frontmatter
- `905` have malformed frontmatter

That alone would be enough to justify stabilization work.
But the more important read is this:

even among notes that *do* have valid frontmatter, the baseline metadata
contract is still not converged.

For non-daily notes with valid frontmatter, missing required-field counts are
still very high:

- `updated`: `11,412`
- `title`: `11,352`
- `status`: `11,300`
- `authority`: `711`

So the repo is not mainly suffering from absence of a standard.
It is suffering from partial adoption, mixed eras, and multiple competing local
shapes.

### Finding 2

`[P1]` Daily notes are much closer to stable than the broader corpus, but the
daily contract is still split between doctrine and lived practice.

The survey found `36` daily-note files, `35` of them with valid frontmatter.
That is materially healthier than the non-daily corpus.

The remaining drift is specific and manageable:

- `9` daily notes are missing `aliases`
- `35` still carry `date created`
- `35` still carry `date modified`
- `7` carry `authority`

This means the daily lane is already close enough to harden.
The open question is not "what is a daily note?"
The open question is whether the repo intends daily notes to remain a special
metadata class with legacy fields, or whether they should be pulled closer to
the broader baseline metadata doctrine.

### Finding 3

`[P1]` The repo has a doctrinal standard, but the templates and the live corpus
are not yet tightly converged around it.

The good news is that the repo is not missing metadata doctrine.

The core surfaces exist:

- `VAULT-METADATA-STANDARD.md`
- `VAULT-TEMPLATES.md`
- `DAILY NOTE TEMPLATE.md`
- `!/PLUGIN-REGISTRY.md`

The bad news is that the living note population does not yet reliably inherit
or satisfy those surfaces.

This is visible in template-field adoption:

- `doc_class`: `48`
- `template_id`: `2`
- `template_version`: `0`

That is near-zero effective template uptake relative to corpus size.
In practice, the template system currently behaves more like a declared law than
an enforced or widely instantiated contract.

### Finding 4

`[P1]` `status` and `authority` are carrying too many local dialects to remain
clean machine fields.

The survey found a narrow lawful center and a large fringe of improvised
variants.

For `status`, the corpus includes a small clean core like:

- `active`
- `draft`
- `archived`
- `superseded`

but also many one-off or prose-like values such as:

- `AUTHORITATIVE - no agent enables, disables, installs, or removes plugins without updating this registry`
- `exploratory companion`
- `incident report`
- `witness record`
- `terminated-clean`

For `authority`, the center is strong:

- `LOGAN`: `10,729`

but the edges are noisy:

- `Codex`
- `codex`
- `claude`
- `Logan Finney`
- `[[LOGAN]]`
- `[[ADMIN]][[LOGAN]]`
- `crewai/address-space`

This is exactly the kind of drift that weakens agent utility.
These fields should be stable indexes, not expressive prose surfaces.

### Finding 5

`[P2]` The frontmatter debt is concentrated enough to survey and repair
incrementally.

The missing-frontmatter examples are not random.
They cluster in recognizable families:

- archive/log surfaces
- ingest artifacts
- historical notes
- malformed legacy note titles

That matters because it means the repair path does *not* need to start with the
entire vault.
The right next move is cohort-based normalization, not global mutation.

### Finding 6

`[P2]` The repo now has a lawful baseline inspection tool, and that changes the
repair posture materially.

This pass added a reusable survey tool:

- `.github/scripts/metadata_survey.py`

with verification in:

- `tests/test_metadata_survey.py`

This matters because agents now have a machine-readable way to answer:

- which notes have valid frontmatter
- which fields are missing most often
- how daily notes differ from non-daily notes
- how fragmented `status` and `authority` currently are
- how little template adoption has actually landed

That is a real gain for vaulted agent utility.
It reduces guesswork and gives future repair work a factual baseline.

## Interpretive Read

The repo's metadata problem is now clearer than before.

It is not:

- no standard
- no templates
- no awareness

It is:

- declared standards with weak uptake
- one comparatively healthy live lane (`daily notes`)
- a huge historical corpus with mixed-era metadata shapes
- expressive drift in fields that should stay boring

The right diagnosis is:

metadata/frontmatter debt is now primarily a convergence problem.

## Next Material Gains

### 1. Normalize `status` and `authority` on active governance/report/spec/handoff families first

This is the highest-leverage cleanup because those are the surfaces agents will
read as live authority.

### 2. Decide the daily-note contract explicitly

Pick one of two paths:

- daily notes are intentionally special and keep `date created` /
  `date modified`
- daily notes are pulled closer to the general metadata baseline

Until that choice is explicit, the daily lane will keep looking half-legacy and
half-canonical.

### 3. Retrofit template fields only on active high-signal classes

Do not attempt vault-wide `doc_class` / `template_id` retrofits yet.
Start with live report/spec/proposal/doctrine families where the gain is real.

### 4. Treat malformed frontmatter as a repair queue, not a philosophical problem

The malformed cohort is finite and identifiable.
It should be triaged and repaired as a technical hygiene pass.

## Bottom Line

The metadata layer is no longer mysterious.

The survey makes the situation plain:

- daily notes are close
- non-daily notes are fragmented
- template adoption is minimal
- `status` and `authority` need narrowing
- the repo now has a factual instrument for staged repair

That is enough to move from "we know metadata is messy" to a real repair
program with narrow, testable seams.
