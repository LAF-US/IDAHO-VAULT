---
title: CrewAI Output Staging
authority: crewai
doc_class: index
status: active
---

# !/CREWAI/ - Output Staging

This directory is the live staging and output surface for the re-founded CrewAI
layer.

It also preserves artifacts from the retired demo harbor. Those older files
stay on record, but they are historical and do not define current procedure.

## Staging Rule

- CrewAI may write staged outputs here.
- Staged outputs are on-record, but they are not canonical by default.
- Promotion from `!/CREWAI/` into canon requires Logan approval.
- Runtime caches, logs, and secret-bearing material do not belong here.

## Current Truth

- Live CrewAI doctrine and topology: `.crewai/MANIFEST.md`
- Control-plane layer registration: `swarm.json`
- Historical harbor records: `!/CREWAI/HANDOFF-CREWAI-OPS.md` and
  `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md`
