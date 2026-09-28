---
authority: LOGAN
related:
  - GitHub
  - workflows
  - automation
  - Linear
  - agent
  - vault
date created: Monday, April 13th 2026
date modified: Monday, April 13th 2026
status: exploratory companion
---

# Automation Corridor - Explorer Companion

This note accompanies the workflow surfaces in `.github/workflows/`.

It is a corridor sketch, not a source of truth. The workflow files themselves
remain authoritative.

## Observed Workflow Character

The workflow layer reads less like a single pipeline and more like a civic
district with specialized public offices.

Examples observed during this passage:

- `check-dotfolder-anchors.yml` enforces durable identity anchors
- `linear-webhook.yml` acts as a routed bridge between Linear events and vault
  automation
- `vault-courier.yml` backs up the `!/` ledger to Google Cloud Storage

Nearby filenames suggest additional districts for:

- branch hygiene
- daily rollover
- large-file and path portability checks
- wayback preservation
- budget export
- review and response flows

## Useful Distinction

The workflows are mostly summons and guardrails.

Much of the actual procedural force lives one room over in
`.github/scripts/`, where the Python and shell tools perform the work after a
workflow wakes them.

That split matters:

- the workflow answers "when and under what authority does this run?"
- the script answers "what actually happens once the bell is struck?"

## Field Note

This machinery does not feel ornamental. It feels administrative in the old
sense: clerks, couriers, inspectors, and watchmen moving through a living
archive.

The vault's automation layer is not trying to replace the record. It patrols
the edges, moves materials between systems, and checks that the declared order
still holds.
