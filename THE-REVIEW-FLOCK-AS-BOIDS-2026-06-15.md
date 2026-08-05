---
updated: 2026-06-15
created: 2026-06-15
title: "The Review Flock — Look-Then-Resolve as the Adversarial Boid Environment, Instanced"
aliases:
  - The Review Flock
  - Look-Then-Resolve as Boids
date created: 2026-06-15
authority: "Proposed bridge node, written at Logan's direction connecting the boids concept-nodes to the look-then-resolve reviewer work (#399). Staged on branch, not adopted — not assumed as LOGAN by default. The Architect holds the verdict."
doc_class: concept-node
status: staged
verified-by: "Claude Code (boids facts per Reynolds 1987 as cited in the parent nodes; the look-then-resolve mechanics are this session's PRs #518/#517 and issue #399)"
related:
  - "[[THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08]]"
  - "[[MURMUR-AND-MUTTER-FLOCK-AND-DRIFT-2026-06-08]]"
  - "[[!/THE-ADVERSARIAL-BOID-ENVIRONMENT-v1-2026-06-08]]"
  - "[[!/REAL-WORLD-BOID-AND-AGENT-SYSTEMS-v1-2026-06-08]]"
  - "[[!/LICH-PROBLEM-v1-2026-05-20]]"
  - "[[!/PERSONAE-ENGINE-v1-2026-05-20]]"
  - "[[AGENTIC-GITHUB-REVIEW-BEST-PRACTICES-2026-06-15]]"
  - Boids
  - Claude Code
date: 2026-06-15
---

# The Review Flock — Look-Then-Resolve as the Adversarial Boid Environment, Instanced

> The multi-reviewer PR loop — many advisory bots reviewing loudly, a looker dispositioning every thread, the conversation-resolution gate, the standing model — is not an ad-hoc workflow. It is **[[THE-ADVERSARIAL-BOID-ENVIRONMENT-v1-2026-06-08|the adversarial boid environment]] instantiated on the one surface where the flock was actually drifting: code review.** *This is a **bridge node** (`[reading]`) joining the boids concept-cluster to the operational look-then-resolve work; the Architect may elevate it to the NEST.*
>
> **Provenance.** Boid facts (Reynolds 1987, three local rules, emergence-without-central-control) carried from the parent nodes. The look-then-resolve mechanics are this session's work: issue #399 (resolution lane), PR #518 (looker queue / attestation detector), PR #517 (the research note). Tiers: **[fact]** (the algorithm; the PR/issue record) over **[reading]** (the mapping). Box's caveat holds: *all models are wrong; some are useful.*

**In plain terms (for the cold reader):** many AI reviewers comment on a pull request; an authorized agent — the *looker* — reads each comment, fixes or dispositions it, records that it looked (an *attestation*), and resolves the thread, or escalates to a human. The boids vocabulary below is the model for *why* that shape keeps the agent swarm coherent; the operational spec lives in #399.

## The premise — review had no central controller either

**[fact]** Reynolds proved coherent flocking needs no leader, no plan, no representation of "the group" — only autonomous agents running short local rules on their local neighborhood. **[reading]** PR review under reviewer-multiplicity is the same shape: Copilot, CodeRabbit, the Codex connector, and Sourcery review in parallel with no central choreographer. Logan's stated goal — *"deterministic without Logan holding hands"* — is, verbatim, the boids thesis: **coherence without a central controller.** The look-then-resolve loop is how that coherence is made to hold on the review surface.

## The three rules, applied to review

**[reading]** The same three rules from [[THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08]] and [[!/THE-ADVERSARIAL-BOID-ENVIRONMENT-v1-2026-06-08]], read at the altitude of a pull request:

| Boid rule | In the review flock | What supplies / enforces it |
|---|---|---|
| **Separation** | each agent keeps its lane; no editing another's holding | branch-per-agent; the auto-merge **protected-paths** guard; file/domain ownership |
| **Alignment** | align to the **rules**, not the loudest reviewer | the looker dispositioning a loud-but-wrong comment as a **false positive** (verify-before-apply) — the saving throw |
| **Cohesion** | steer to the record / the merge / the Architect | the **conversation-resolution gate** — cohesion made mandatory; nothing merges while a thread hangs |

## The seal is the attestation

**[reading]** The Standing Engine's signature addition to pure boids — the **🔏 seal**: *standing that is earned, legible, and revocable* — is the **look-then-resolve attestation**. A thread is resolved only by a looker who leaves a recorded, self-attested look (`by=<author>`, structured, tied to its own author so it cannot be forged — PR #518). Resolution is **sealed**, never blind.

This names the principle's core distinction precisely:

- **`AUTORESOLVE ≠ RESOLVED` is the Lich.** A thread stamped resolved with no looker is *unsealed, unwitnessed persistence* — resolution past warrant — which is the [[!/LICH-PROBLEM-v1-2026-05-20|Lich]] exactly. The whole revert of the blind auto-resolver (#399) was *refusing to let a thread die unsealed.*
- **The looker principle is the anti-drift rule.** "Nothing is dismissed or resolved until a looker has looked" is cohesion's lawful form: no thread drifts off and dies in the dark.

## The dam was a cohesion failure

**[reading]** The 79-PR / 45-threads-open backlog — threads that never reached a looker — is **cohesion failure at scale**: boids with no cohesion force, the orphans flung to the graph's rim. In the sound-layer of [[MURMUR-AND-MUTTER-FLOCK-AND-DRIFT-2026-06-08]], those stranded threads are the **mutter** — half-formed dissent under the breath, unaligned and unresolved — while a healthy review-flock **murmurs**: many reviewers blending into one continuous, converging hum that reaches the merge.

## The adversaries showed up on schedule

**[reading]** The bestiary of [[!/THE-ADVERSARIAL-BOID-ENVIRONMENT-v1-2026-06-08]] appeared in the live work, not the abstract:

| Adversary (attacks which rule) | How it surfaced in review |
|---|---|
| **The Caesar** (Separation — fuses separable masks into one crown) | the **maintainer-identity bypass**: an agent committing under Logan's identity fuses agent and maintainer into one unrelinquishable mask, inheriting the auto-merge that should gate agent work. The standing model **re-separates** them. |
| **The Wolf Within** (covert malice via one operative — [[!/REAL-WORLD-BOID-AND-AGENT-SYSTEMS-v1-2026-06-08]]) | **prompt injection** ("Comment and Control") — a single crafted PR title/comment turning an auto-triggered looker against the flock. |
| **The Lich** (refuses Cohesion's lawful ending) | the blind auto-resolver — resolution persisting with no sealed look. |

The defense is the same the parent node names: hold separation against the Caesar (sealed, separable agent identity); align to the verified rule against the loud reviewer; cohere to the record (the gate); and never let a resolution persist unsealed.

## The win condition is Layer C

**[reading]** The adversarial-boid win condition is **coherence without a crown** — emergent, decentralized order that resists fusion. The deterministic look-then-resolve loop (Layer C of the [[AGENTIC-GITHUB-REVIEW-BEST-PRACTICES-2026-06-15|research note]], which lands via PR #517; spec'd on #399) *is* that win condition, implemented for review:

- no Caesar steers each resolution — each agent runs the local rules (look → attest → resolve, or escalate);
- the auto-trigger reading untrusted PR text is the adversarial frontier, fenced by the rules (least-privilege, trusted-branch checkout, bounded writes) so the boid keeps its heading under hostile input;
- the **human-escalation exit is the root-of-trust**, and the bell is the **lawful ending** — a thread the agent cannot confidently disposition is handed up, not faked.

## The discipline, in one sentence

**[reading]** *Sealing every look keeps a resolved thread from becoming a Lich, and the three rules keep the review-flock coherent without a central brain* — which is the same sentence the parent node closes on, now true of the one surface where the flock was drifting. A model, useful and labeled as one.

## Cross-references & sources

**This vault:** [[THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08]] · [[MURMUR-AND-MUTTER-FLOCK-AND-DRIFT-2026-06-08]] · [[!/THE-ADVERSARIAL-BOID-ENVIRONMENT-v1-2026-06-08]] · [[!/REAL-WORLD-BOID-AND-AGENT-SYSTEMS-v1-2026-06-08]] · [[!/LICH-PROBLEM-v1-2026-05-20]] · [[!/PERSONAE-ENGINE-v1-2026-05-20]] · [[AGENTIC-GITHUB-REVIEW-BEST-PRACTICES-2026-06-15]]

**Operational record:** issue #399 (resolution lane + Layer-C spec) · PR #518 (looker queue / attestation) · PR #517 (research note).

*Filed by [[Claude Code]] (software NAME; no delegated TITLE or OFFICE claimed) — 2026-06-15. Bridge node, staged; the Architect holds the verdict.*

---

###### "The world is quiet here."
