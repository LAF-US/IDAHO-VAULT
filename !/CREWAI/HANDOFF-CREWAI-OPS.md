---
title: "CrewAI Operations Handoff"
date created: "2026-04-04"
authority: crewai
doc_class: handoff
---

# CrewAI Operations Handoff

Historical note for the retired demo harbor. Do not use this file as the current runbook for the redesigned CrewAI Python layer.

---

## Prerequisites

1. **Python 3.13+** with venv active:
   ```bash
   cd /path/to/IDAHO-VAULT
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. **Dependencies installed:**
   ```bash
   pip install -r requirements.txt
   ```
   Key packages: `crewai[tools,anthropic]>=1.12.0`, `python-dotenv>=1.0.0`, `op` (1Password CLI)

3. **API key via `op run`** (local-only — never committed):
   ```
   ANTHROPIC_API_KEY=op://YOUR_VAULT/YOUR_ITEM/YOUR_FIELD
   ```
   Fetch from [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys).
   Account must have API credits loaded at [console.anthropic.com/settings/plans](https://console.anthropic.com/settings/plans).

---

## Running a Crew

### JFAC Parser (Active)

```bash
# From vault root
scripts/op-run-jfac.ps1
```

**What happens:**
1. Loads API key from the environment, ideally provisioned by `op run`
2. Instantiates 3 agents (Budget Scout, Legislative Tracker, H911 Parser)
3. Runs 5 sequential tasks (WHO, WHAT, WHEN, WHERE, WHY)
4. Writes output to `!/CREWAI/jfac-analysis-{run_id}.md`

**Inputs consumed:**
- `minidata-*.csv` — dated JFAC minidata snapshots (vault root)
- `legislature.idaho.gov` — live bill status (scraped by bill_status_checker tool)

**Expected output:** A vault-format markdown file with frontmatter, containing structured analysis of Idaho appropriations bills.

**LLM:** Claude Sonnet (`anthropic/claude-sonnet-4-6`) — configured in `run_jfac.py`

---

## Inspecting Output

All crew output lands in `!/CREWAI/`. Each file has frontmatter:

```yaml
---
title: "JFAC Appropriations Analysis — {run_id}"
date created: "YYYY-MM-DD"
authority: crewai/jfac-crew
doc_class: analysis
crew_run_id: "{run_id}"
---
```

**Nothing moves from `!/CREWAI/` into the main vault without Logan's approval.** This is the staging area — machine-generated, human-reviewed.

---

## Ephemeral vs. Durable

| Surface | Persisted? | Location |
|---|---|---|
| Crew output (analysis files) | **Yes** — committed to vault | `!/CREWAI/` |
| Runtime cache | No — gitignored | `.crewai_cache/` |
| Execution logs | No — gitignored | `.crewai/logs/` |
| API key | No — local-only | `_private/idaho-vault.env.tpl` + `op run` |

---

## Extending: Adding a New Crew

1. **Create the crew file** at `.crewai/crews/{crew_name}_crew.py`
   - Define agents with `llm=llm` (import LLM config from run script or shared module)
   - Define tasks with `agent=` assignment
   - Create a `build_{name}_crew()` function and a `run()` entrypoint

2. **Create tools** (if needed) at `.crewai/tools/{tool_name}.py`
   - Extend `crewai.tools.BaseTool`
   - Wrap existing vault scripts where possible

3. **Create a runner** at `.crewai/run_{name}.py`
   - Prefer environment variables already injected by `op run`
   - Configure LLM
   - Write output to `!/CREWAI/` with vault frontmatter

4. **Update the manifest** at `.crewai/MANIFEST.md`
   - Add the crew, its agents, tasks, tools, inputs, and outputs

5. **Do NOT** modify `swarm.json` — CrewAI crews are instruments within the swarm, not registry entries.

---

## Known Constraints

- **Windows encoding:** CrewAI's event bus emits emoji characters that Windows `charmap` can't encode. Set `PYTHONIOENCODING=utf-8` when running on Windows, or run on Linux/WSL.
- **Runtime secret source:** `op run` is the preferred path. `.crewai/run_jfac.py` only falls back to local env files when no model key is already present in the environment.
- **API billing:** The Anthropic API key must have credits loaded. CrewAI will fail with a 400 error if the balance is zero.
- **JFAC hard gate:** JFAC quotes require audio verification by Logan before publication. CrewAI output is analysis, not publication — but the gate applies to any content derived from it.

---

## Architecture

```
.crewai/                    ← Code/config (committed)
  crews/                    ← Crew definitions
    jfac_crew.py            ← JFAC Parser (active)
    task_to_code_crew.py    ← Task-to-Code Bridge (stub)
    vault_custodian_crew.py ← Vault Custodian (stub)
  tools/                    ← Tool wrappers
  run_jfac.py               ← JFAC runner
  MANIFEST.md               ← Crew manifest

!/CREWAI/                   ← Output staging (committed, human-reviewed)

.crewai_cache/              ← Runtime cache (gitignored)
.crewai/logs/               ← Execution logs (gitignored)
_private/idaho-vault.env.tpl ← 1Password secret refs (gitignored)
```

---

## See Also

- `.crewai/MANIFEST.md` — full crew/agent/task/tool registry
- `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` — architectural directive
- `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md` — strategy document
- `swarm.json` — upstream machine registry (DO NOT MODIFY)
