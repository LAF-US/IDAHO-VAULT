---
title: "OpenAI Swarm"
updated: 2026-03-29
status: stub
authority: perplexity
doc_class: organization
tags:
  - swarm
  - r-and-d
  - unified-swarm
  - multi-agent
  - openai
  - tools
url: https://github.com/openai/swarm
---

# OpenAI Swarm

**OpenAI Swarm** is a lightweight, educational multi-agent framework focused on clarity and reliability of handoffs. Agents are simple Python classes with system prompts, tools, and routines, coordinated via explicit handoff functions rather than complex memory layers.

Swarm favors observability and testability over heavy infrastructure, making it suitable as a reference pattern for agent handoffs and microservice-style specialization—but not as a full production platform by itself.

## R&D Inquiry

**Flagged by Logan Finney, 2026-03-29**, via Perplexity unified swarm research session.

In the [[BIG IFS — UNIFIED SWARM]] framework, OpenAI Swarm is identified as the **pattern library and testing ground** for simple, transparent multi-agent behaviors and handoffs—especially useful for prototyping new swarm routines before embedding them into [[Factory]] or [[CrewAI]] flows.

Key architectural notes from the research:
- Swarm's **handoff model** (explicit intent + state transfer between agents) is the proposed substrate for the Unified Swarm cross-platform handoff protocol (Big IF 3).
- Its stateless, minimal design minimizes cascade risk—aligns with the VAULTED A&I monster/dragon containment principles documented in [[ARCHITECTURE & INFRASTRUCTURE REPORT]] and [[CIVILIZATION-SCALE ARCHITECTURE REPORT]].
- `swarm/app.py` in this vault is a minimal implementation inspired by these patterns.

Open questions for R&D evaluation:
- Swarm is educational/experimental per OpenAI's own framing—what production hardening is required before any IDAHO-VAULT dependency?
- Handoff protocol formalization: can the YAML-defined agent schema in `!/VAULT-TEMPLATES.md` serve as the common descriptor?

## See Also

- [[BIG IFS — UNIFIED SWARM]]
- [[Factory]]
- [[CrewAI]]
- [[ARCHITECTURE & INFRASTRUCTURE REPORT]]
- [[CIVILIZATION-SCALE ARCHITECTURE REPORT]]
