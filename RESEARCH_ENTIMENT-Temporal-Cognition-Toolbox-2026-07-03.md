---
title: "RESEARCH — ENTIMENT: commercializing time-aware robots (the Temporal Cognition Toolbox)"
date created: 2026-07-03
updated: 2026-07-03
status: active
doc_class: research
authority: "External research compiled by Claude Code this session from public web sources. NOT Logan-authored and NOT vault doctrine. Provenance is [research — secondary]: the CORDIS fact sheet (754423) and entiment.eu 403'd through the agent proxy this pass, so the facts below come from search-engine summaries of those pages, not direct reads. Gaps are flagged inline. Follow-on to [[RESEARCH_TimeStorm-Consortium-2026-07-03]]."
authors:
  - "Claude Code — session https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd"
source: web
session: "https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd"
related:
  - "[[RESEARCH_TimeStorm-Consortium-2026-07-03]]"
tags: [research, entiment, timestorm, temporal-cognition-toolbox, time-perception, human-robot-interaction, ROS, commercialization, EU-FET, innovation-launchpad, horizon-2020, secondary-source]
---

# RESEARCH — ENTIMENT

> **What this is.** A full external-research report on **ENTIMENT** — the commercialization
> follow-on to **TIMESTORM** (`[[RESEARCH_TimeStorm-Consortium-2026-07-03]]`). **Provenance is
> secondary:** the CORDIS fact sheet and entiment.eu 403'd through the proxy this pass, so this is
> assembled from search summaries. Facts that could not be pinned are marked `*`.

> **Provenance tiers:** `[research — secondary]` = search-summary of a primary page not directly
> read this pass · `[research]` = corroborated across ≥2 summaries · **`*`** = an honest gap.

---

## 1. At a glance — `[research]`

| Field | Value |
|---|---|
| **Acronym** | ENTIMENT (styled *EnTiment*) |
| **Full title** | *Industrial Exploitation and Market Uptake of a Temporal Cognition Toolbox for Commercial Robots* |
| **Grant Agreement** | **754423** |
| **Programme / call** | EU **Horizon 2020**, **FET Innovation Launchpad** (call FETOPEN-04-2016-2017) |
| **Dates** | **01 Jul 2017 – 31 Dec 2018** (~18 months) |
| **Budget** | **€100,000** (100% EU-funded) |
| **Coordinator** | **FORTH** — Foundation for Research and Technology – Hellas (Heraklion, Crete); single beneficiary |
| **Parent project** | **TIMESTORM** (GA 641100) — from which ENTIMENT takes its technology |

## 2. What it was for — `[research]`

ENTIMENT is not new science; it is a **launchpad-to-market grant.** Its purpose was to *"assess,
deploy and commercialize a novel **Temporal Cognition Toolbox (TCT)** that greatly facilitates the
development of time-aware robots, capable to engage in prolonged, symbiotic interaction with
humans."* It **capitalizes on TIMESTORM's** artificial-time-perception R&D — taking research that
*proved* robots could be made time-aware and turning it toward *"a genuine social and economic
innovation."* Note the **overlap**: ENTIMENT (Jul 2017 →) ran alongside TIMESTORM's final year and
continued six months past its June 2018 end — the standard shape of a FET Innovation Launchpad
(a small grant to push a parent project's results toward uptake while the science wraps).

## 3. The deliverable — the Temporal Cognition Toolbox (TCT) — `[research]`

The core output: FORTH's *"already available and tested robotic temporal cognition modules,
implemented in TimeStorm"* — the Generative-Time-Model line (predicting how long an unfolding
activity will take, coordinating action around it, remembering it episodically) — **refined and
integrated into the TCT**, which was *"further released as an **open-source ROS node** for robotic
developers."* In other words: package "make your robot time-aware" as a drop-in **ROS** component
any robotics developer could adopt. *(Whether the open-source node actually shipped, and where it
lives, is `*` below — the aim is documented; the release I could not confirm.)*

## 4. Commercialization and the industry anchor — `[research]`

The "market uptake" half rested on a named industrial relationship: a **FORTH – Honda Research
Institute Japan joint research project** *"focused on predicting the temporal properties of
activities to facilitate human-robot symbiosis and cooperative intelligence."* Alongside it,
FORTH reported **ongoing discussions and negotiations with robotics companies** about potential
commercial applications. So ENTIMENT's uptake story has two legs: an **open-source release** (reach
developers) and a **strategic partner** (Honda RI Japan) plus commercial outreach.

## 5. Reported results — `[research — secondary]`

The claimed validation is human-facing and concrete: embodying the models in robots collaborating
with people in **home-like realistic setups** showed that *"humans appreciate and consider much
more natural and productive the collaboration with time-informed robotic systems in comparison to
ordinary systems,"* and that *"taking into account temporal context facilitates the coordination of
robot behavior with the dynamic unfolding of human-robot interaction scenarios."* The headline, in
plain terms: **people prefer working with a robot that has a sense of timing**, and temporal
context measurably smooths the back-and-forth of collaboration.

## 6. People — `[research]`

- **Michail Maniadakis** (FORTH ICS / Univ. of Crete) — central researcher; lead of the
  temporal-cognition modules the TCT is built from.
- **Panos Trahanias** (FORTH) — senior/coordinating figure (as in TIMESTORM).
- **Emmanouil Hourdakis** and **Stylianos Piperakis** (FORTH) — collaborators appearing on the
  associated robotics/temporal work.

## 7. Context — what a FET Innovation Launchpad is — `[research]`

A small (~€100k), short EU instrument whose sole job is to **carry results from a completed/ongoing
FET research project across the "valley of death" toward commercial or societal value** — IP, a
business case, an MVP, partner engagement. ENTIMENT is a textbook instance: FET-Open science
(TIMESTORM) → Launchpad (ENTIMENT) → a toolbox, an open-source release, and an industrial partner.

## 8. Sources — `[research — secondary]`

- CORDIS — ENTIMENT fact sheet (754423): <https://cordis.europa.eu/project/id/754423> *(403 this pass)*
- entiment.eu: <http://www.entiment.eu/> *(not directly read)*
- OpenAIRE — ENTIMENT project record:
  <https://explore.openaire.eu/search/project?projectId=corda__h2020::f41df515412eb09ad6b8aae10caa692b>
- EU success story — *Robots in a rush: time-aware AI aids human-machine interaction*:
  <https://projects.research-and-innovation.ec.europa.eu/en/projects/success-stories/all/robots-rush-time-aware-ai-aids-human-machine-interaction>
- Maniadakis homepage (FORTH): <http://users.ics.forth.gr/~mmaniada/index.htm>
- Frontiers — *Time-Aware Multi-Agent Symbiosis* (2020 synthesis):
  <https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2020.503452/full>

## 9. Open / to verify — `*`

- **Did the open-source ROS node actually ship, and where does it live?** — **Partly resolved
  (2026-07-03); see §10.** An open-source ROS package from this research line *does* exist —
  **`daisy_planner`** (BSD-2-Clause) — though its README badges it to *TIMESTORM*, not explicitly to
  ENTIMENT's *Temporal Cognition Toolbox.* Whether `daisy_planner` **is** the TCT, or one module of
  it, is unconfirmed.
- **What came of the Honda RI Japan partnership** — a product, a paper, or discontinued? Unconfirmed.
- **Direct reads** of the CORDIS fact sheet and entiment.eu (both 403'd) for exact deliverables,
  final report, and any adoption metrics.
- Whether ENTIMENT had **any partner beyond FORTH** (Innovation Launchpads are usually single-
  beneficiary — likely FORTH alone — but not confirmed here).

## 10. Found — the open-source ROS artifact (`daisy_planner`) — `[research]`

Pointer supplied by Logan, confirmed against the repository.

- **Repo:** **`github.com/mrsp/daisy_planner`** — *"Daisy Planner — Planning Time Informed
  Multi-agent Interactions."*
- **What it is:** a **ROS package** (`rosrun daisy_planner daisy_planner`, with a `daisy_plot`
  visualizer) that **devises plans for the timely accomplishment of goals**, working alongside an
  **Episodic Memory** module and **Generative Time Models** to coordinate a multi-agent team — the
  software form of the *"Time-informed task planning in multi-agent collaboration"* line (§5).
- **License:** **BSD-2-Clause** — genuinely open source. The *"release it as an open-source ROS
  node"* ambition was, for the planning component, **realized**.
- **Author:** **Stylianos Piperakis** (GitHub `mrsp`), FORTH ICS — subsequently **Senior Software
  Engineer at Agility Robotics** (makers of the *Digit* humanoid). A concrete commercialization
  path: a researcher off this time-aware work carried into a leading commercial-humanoid company.
- **Deps / status:** Ubuntu 14.04+, ROS Indigo+, gnuplot; README notes it is *"on-going research…
  some parts are not fully developed yet."*

**Two caveats, kept honest:** (1) the README attributes `daisy_planner` to **TIMESTORM (GA
641100)**, *not* ENTIMENT — so this confirms an **open-source ROS artifact of the research line**,
not, on its own text, the specific branded ENTIMENT *TCT*. (2) The **Honda RI Japan** partnership
(§4) is still `*` — `daisy_planner` carries no Honda reference; a Honda product or joint paper I
have not located.

---

*Compiled by Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd`, 2026-07-03. Secondary-sourced (the
CORDIS/entiment.eu primaries 403'd through the proxy); seams marked for a later tightening pass.*

*Revision (2026-07-03): §10 added — Logan supplied the repo `mrsp/daisy_planner`; confirmed an
open-source (BSD-2-Clause) ROS planning artifact of the research line, README-badged TIMESTORM.
The Honda RI Japan outcome remains `*`.*
