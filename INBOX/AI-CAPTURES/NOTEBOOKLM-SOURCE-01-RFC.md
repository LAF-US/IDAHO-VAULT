# RFC 0001: Requirements for a Journalist's Canonical Ledger in a Multi-Agent Environment

**Status:** Informational
**Author:** A working journalist
**Date:** April 2026

## Abstract

This document specifies requirements for a canonical record-keeping system operated by a single human journalist, augmented by multiple artificial intelligence agents, where the outputs are subject to public scrutiny, legal discovery, and the professional standards of broadcast journalism. The system must solve a fundamental tension: leveraging synthetic intelligence for speed and scale while maintaining an unbroken chain of human editorial authority over every publishable claim.

## 1. Problem Statement

A journalist covering state government produces hundreds of notes, source documents, interview transcripts, legislative analyses, and draft stories per week. Traditional note-taking systems (paper notebooks, single-user apps) cannot absorb this volume while maintaining the cross-referencing density required for investigative work. AI agents can process, link, and surface connections at scale — but they also hallucinate, confabulate, and confidently assert falsehoods.

The core problem: **How do you build a system that accepts synthetic contributions while guaranteeing that no synthetic falsehood reaches publication?**

## 2. Requirements

### 2.1 Human Supremacy of Editorial Judgment

No AI-generated claim shall be publishable without explicit human verification. The system must distinguish between:

- **Human-authored content:** Written by the journalist. Publishable on its own authority.
- **Agent-contributed content:** Written by AI. Must be flagged as synthetic until verified.
- **Verified synthetic content:** AI-contributed, human-verified. Publishable with the journalist's authority.

### 2.2 Provenance Tracking

Every piece of content must carry metadata sufficient to answer:

- Who created it? (Human or which agent?)
- When was it created?
- What was the source material?
- Has it been verified? By whom?
- What is its publication status?

### 2.3 Truth Decay Resistance

The system must resist "truth decay" — the gradual process by which a synthetic claim, repeated across enough internal documents, begins to feel authoritative. Mechanisms:

- Claims do not gain authority through repetition.
- A claim's authority derives solely from its sourcing chain.
- Unsourced claims must remain visually and structurally distinct from sourced ones.

### 2.4 Multi-Agent Coordination Without Multi-Agent Trust

Multiple AI agents may contribute to the system simultaneously. No agent trusts another agent's output. The journalist is the sole trust authority. Agents may:

- Read the canonical record.
- Propose additions or modifications.
- Execute structural operations (file management, version control).

Agents may NOT:

- Promote their own claims to canonical status.
- Override another agent's flags or warnings.
- Modify governance documents without human authorization.

### 2.5 Public Accountability

The entire system, including its governance documents, agent configurations, and operational history, is version-controlled and publicly accessible. This is deliberate: the journalist's methods are part of the public record. "All committed content is ON THE RECORD and PUBLISHABLE."

## 3. Architectural Implications

These requirements imply a layered architecture:

1. **Constitutional layer:** Immutable principles. Human-authored. Rarely changed.
2. **Governance layer:** Operational rules derived from principles. Human-authored, agent-readable.
3. **Operational layer:** Day-to-day coordination. Agents may write; humans review.
4. **Data layer:** Raw content. Agents contribute freely; nothing here is canonical until promoted.

The promotion path — data → operational → governance → constitutional — must be explicit, auditable, and reversible.

## 4. Open Questions

- How should the system handle an agent that sincerely believes it has discovered an error in a governance document?
- What happens when two agents produce contradictory analyses of the same source material?
- Can the system scale beyond a single journalist while maintaining editorial coherence?
- What are the legal implications of a public, version-controlled record of AI-assisted journalism?

## 5. Prior Art

Zettelkasten (Luhmann), version-controlled documentation (Git), knowledge graphs (semantic web), and bullet journaling (Carroll) each solve a subset of these requirements. No existing system solves all of them simultaneously in a multi-agent context.

The journalist's notebook has always been a ledger of truth-in-progress. This specification merely formalizes what good reporters have always done: keep the record, question the source, and never let anyone else hold the pen.
