---
name: CrewAI Alignment Protocol
description: CrewAI ignition sequence for IDAHO-VAULT — protocol drafted, five open questions pending Logan's direction
type: project
---

CrewAI Alignment Protocol drafted 2026-04-04 at `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md`.

**Why:** Logan directed the JFAC Budget Strike as the first directive of the NETWEB Era. CrewAI Enterprise account is active at app.crewai.com. The vault has existing budget/appropriations scripts in .github/scripts/ that can be wrapped as CrewAI tools.

**Current state:**
- `crewai` Python package NOT installed (only Flask + GCP packages in .venv)
- `CrewAI.md` is a research stub from 2026-03-29
- `swarm.json` maps vault agents to roles — ready to translate to crew definitions
- Existing scripts: minidata_appropriations_timeline.py, normalize_budget_data.py, idaho_leg_scraper.py
- main.py is a Flask webhook placeholder for GCP Nest Bridge

**Five questions RESOLVED (2026-04-04):**
1. **Local-first (OSS)** — `pip install crewai` in .venv, Linux-native
2. **`!/CREWAI/`** — output staging under the `!` administrative layer
3. **Both, phased** — minidata CSV first, then bill text parsing
4. **Small POC now** — 10 neuron stubs alongside JFAC build
5. **Acceptable for later** — data residency revisited at Enterprise Phase 3

**How to apply:** All five gates are open. Build the JFAC Crew targeting Linux-native execution (LINUX }!{ principle). Output goes to `!/CREWAI/` for Logan's review.

**Clerk's note (2026-04-04):** ★ Insights + ★ Findings = ★ Big IFs. The insight blocks produced during code work should feed into the BIG IFS — UNIFIED SWARM framework as R&D candidates.
