# Plan: NETWEB UNIFIED (US) SWARM → CrewAI Alignment

## Context

Bartimaeus delivered an alignment brief (relayed by Logan, 2026-04-04) defining how CrewAI docks into the existing IDAHO-VAULT control plane. CrewAI is an **orchestration layer**, not a new source of truth. The vault, GitHub, and Linear remain the authority/evidence/coordination anchors.

The JFAC Crew exists in `.crewai/` but has **never run end-to-end**. Two additional crews are directed: Task-to-Code Bridge and Vault Custodian. B's core mandate: "Do not create a theatrical swarm before the three concrete crews work end-to-end."

**Antigravity worktreeConfig fix** was applied earlier this session — unblocked the IDE's agent/MCP servers.

---

## Current State

| Component | Status | Location |
|---|---|---|
| JFAC Crew (3 agents, 5 tasks, 4 tools) | Built, **untested** | `.crewai/crews/jfac_crew.py` |
| CrewAI runner | Built, untested | `.crewai/run_jfac.py` |
| Tools (minidata, timeline, scraper, address) | Built | `.crewai/tools/` |
| Output staging | Ready | `!/CREWAI/` |
| `.gitignore` (cache + logs) | Done | `.gitignore` lines 14-15 |
| `crewai` in requirements.txt | **MISSING** | `requirements.txt` has only Flask/GCP |
| Manifest | **Does not exist** | — |
| Reproducible example run | **Does not exist** | — |
| Operational handoff note | **Does not exist** | — |
| Task-to-Code Bridge crew | **Not started** | — |
| Vault Custodian crew | **Not started** | — |
| `swarm.json` | Canonical, must NOT be replaced | `swarm.json` (root) |

---

## Task Assignments

### CLAUDE CODE (The Abhorsen) — executes

1. **Add `crewai` to dependency tracking**
   - Add `crewai[tools]` and `python-dotenv` to `requirements.txt`
   - File: `requirements.txt`

2. **Write B's alignment brief as a vault note**
   - File: `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md`
   - Content: B's full directive (verbatim from Logan's relay), with frontmatter
   - This is the durable architectural directive CrewAI must obey

3. **Build the crew manifest**
   - File: `.crewai/MANIFEST.md`
   - Contents: all crews, agents, tasks, tools, input sources, output destinations
   - Machine-scannable, human-readable
   - Points to `swarm.json` as upstream authority (does NOT duplicate it)

4. **Run JFAC Crew end-to-end**
   - Execute `.crewai/run_jfac.py` in the local `.venv`
   - Capture: what ran, inputs consumed, outputs produced, errors hit
   - Write result to `!/CREWAI/` as a dated analysis file
   - Write a run log note documenting the example

5. **Write the operational handoff note**
   - File: `!/CREWAI/HANDOFF-CREWAI-OPS.md`
   - How to: run a crew, inspect output, extend with new crews/tools
   - Prerequisites, environment setup, known constraints

6. **Stub the two new crews**
   - `.crewai/crews/task_to_code_crew.py` — converts scoped work items → implementation plans
   - `.crewai/crews/vault_custodian_crew.py` — classify, normalize, propose filing/metadata
   - Stubs only: agent/task definitions, no tools yet, docstrings explain intent

### LOGAN — directs and gates

- **Review** B's alignment brief once committed — confirm it captures intent
- **Gate** the JFAC Crew first run output — verify journalistic accuracy before any publication
- **JFAC audio verification** remains a HARD GATE (Monday H 911 deadline)
- **Decide** whether `.crewai/` stays as dotfolder or surfaces to visible `crew/` per B's suggestion

### CODEX — stays in lane

- **No CrewAI work** — CrewAI implementation is Claude Code's lane
- Available for code analysis/refactoring if Claude Code needs a second pair of eyes on the crew code
- Continues existing scoped work per DOCKET

---

## Execution Order

```
Step 1: Write B's alignment brief → !/GRIMOIRE/
Step 2: Add crewai to requirements.txt
Step 3: Build MANIFEST.md
Step 4: Run JFAC Crew E2E → capture output + log
Step 5: Write operational handoff note
Step 6: Stub Task-to-Code Bridge + Vault Custodian
Step 7: Update DOCKET with completion status
```

Steps 1-3 can run in quick succession (all writes). Step 4 is the critical test — first real crew execution. Steps 5-6 depend on step 4's results.

---

## Verification

- [ ] `python -m crewai version` confirms installed version in `.venv`
- [ ] `python .crewai/run_jfac.py` completes without error
- [ ] Output file appears in `!/CREWAI/` with proper frontmatter
- [ ] MANIFEST.md lists all 3 crews (1 active, 2 stubbed)
- [ ] Handoff note is self-contained: a new agent could read it and run a crew
- [ ] `swarm.json` is **unchanged** — no CrewAI contamination
- [ ] `.gitignore` continues to exclude `.crewai_cache/` and `.crewai/logs/`

---

## Non-Goals (per B)

- Do not replace `swarm.json` with CrewAI config
- Do not collapse personas into generic CrewAI placeholders
- Do not make Slack or transient logs the operational memory
- Do not build theatrical architecture before the three crews work E2E

---

## Key Files

| File | Role |
|---|---|
| `.crewai/crews/jfac_crew.py` | JFAC Crew definition (active) |
| `.crewai/run_jfac.py` | JFAC runner script |
| `.crewai/tools/*.py` | CrewAI tool wrappers |
| `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md` | Strategy doc (existing) |
| `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` | B's directive (to create) |
| `.crewai/MANIFEST.md` | Crew manifest (to create) |
| `!/CREWAI/HANDOFF-CREWAI-OPS.md` | Ops handoff (to create) |
| `swarm.json` | Machine registry (DO NOT MODIFY) |
| `requirements.txt` | Python deps (add crewai) |
