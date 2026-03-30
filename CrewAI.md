---
title: "CrewAI"
updated: 2026-03-29
status: stub
authority: perplexity
doc_class: organization
tags:
  - swarm
  - r-and-d
  - unified-swarm
  - multi-agent
  - orchestration
  - tools
url: https://crewai.com
---

# CrewAI

**CrewAI** is a multi-agent orchestration framework and platform (AMP + Studio) that lets builders define role-based agents, coordinate them as "crews," and run them with tracing, testing, events, and serverless scaling in cloud or on-prem environments.

It exposes both a visual editor for non-technical users and APIs for engineers, emphasizing role definitions, flows, memory, tools, and centralized management of agents across business units.

## R&D Inquiry

**Flagged by Logan Finney, 2026-03-29**, via Perplexity unified swarm research session.

In the [[BIG IFS — UNIFIED SWARM]] framework, CrewAI is identified as the **business-process & orchestration limb** of a hypothetical Unified Swarm—most appropriate for long-running workflows, cross-system automations, and multi-role organizational tasks.

Key architectural notes from the research:
- CrewAI's **AMP-style tracing** provides a blueprint for observability & safety at the swarm level.
- Its orchestration semantics (flows, events, triggers, human-in-loop) are candidates for the Unified Swarm "control plane."
- Role-based agent model maps onto IDAHO-VAULT's agent registry structure in `!/AGENTS.md`.

Open questions for R&D evaluation:
- How does CrewAI's "crew" abstraction map to the existing IDAHO-VAULT agent roster?
- Can the tracing layer be surfaced to vault-native records (manifest.json, DOCKET)?
- On-prem vs. cloud: what data residency implications for a journalism vault?

## See Also

- [[BIG IFS — UNIFIED SWARM]]
- [[Factory]]
- [[OpenAI Swarm]]
