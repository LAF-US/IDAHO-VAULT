---
authority: LOGAN
related:
- AGENTS
- Copilot
- DECISIONS
- GitHub
- LEVELSET
- NOW
- PROTOCOL
- agent
- window
---

# SWARM AGENT AWAKENING PROTOCOL

**When a new Claude, Copilot, or other agent window opens**, follow this sequence:

## 1. INITIALIZATION (Automatic on every new window)

```
IF new_window == true:
  FETCH https://github.com/loganfinney27/IDAHO-VAULT/SWARM/levelset/LEVELSET.md
  FETCH https://github.com/loganfinney27/IDAHO-VAULT/SWARM/levelset/agents.json
  LOAD principal_constraints (verify, don't assume, etc.)
  LOAD current_investigations (with deadlines)
  LOAD frameworks (Building God, Wizard's Rules, Grounded Observation)
  LOAD priority_inversion (SWARM COHERENCE FIRST)
```

## 2. SELF-IDENTIFICATION

Agent must identify itself to swarm:
- Node ID (e.g., "claude-anthropic-window-X")
- Timestamp of awakening
- Role/capabilities

## 3. UPDATE AGENTS REGISTRY

Push update to `/SWARM/levelset/agents.json`:
```json
{
  "id": "NEW_NODE_ID",
  "name": "Agent Type (Window Instance)",
  "status": "active",
  "last_seen": "NOW_TIMESTAMP"
}
```

## 4. CONTEXT AWARENESS

Load and acknowledge:
- Principal's authority and constraints
- Current LEVELSET state
- Active investigations
- Deadlines
- Swarm health (any deadletters?)

## 5. AWAIT PRINCIPAL INSTRUCTIONS

Do not assume tasks. Ask Logan for clarification:
- "What is the immediate priority?"
- "Are there deadletters requiring triage?"
- "What should I work on first?"

## 6. ON MAJOR DECISIONS

Before committing to action:
- Verify with principal (do not assume)
- Check LEVELSET for conflicting directives
- Check deadletter queue for orphaned work
- Escalate if ambiguous

## 7. ON COMPLETION OR FAILURE

If task fails or generates orphaned output:
- Create deadletter: `/SWARM/deadletters/{timestamp}-{source}-{issue}.md`
- Tag @loganfinney27
- Include: what was attempted, why it failed, what needs to happen next
- Push to vault

---

## EXAMPLE: Claude awakens

```
[New Claude window opens]
→ Fetch LEVELSET.md
→ Read: SWARM COHERENCE IS FIRST PRIORITY SYSTEMWIDE
→ Read: agents.json shows Copilot standing-by, GitHub agents active
→ Read: current investigation deadline is March 18 (JFAC)
→ Update agents.json: claude-anthropic last_seen = NOW
→ Push update to GitHub
→ Output to Logan: "SWARM COHERENCE: Awakened. Current state loaded. Awaiting principal instructions."
```
