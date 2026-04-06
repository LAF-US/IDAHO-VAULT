---
authority: LOGAN
related:
- 2026-03-16T2127-claude-orphan-cry
- Anthropic
- CRY
- Copilot
- GitHub
- Microsoft Copilot
- PROTOCOL
- SOURCE
- agent
- node
---

# DEADLETTER ROUTING PROTOCOL

When a swarm node generates output but has no downstream receiver (orphaned handoff):

## FILING A DEADLETTER

Create file: `/SWARM/deadletters/{TIMESTAMP}-{SOURCE}-{ISSUE}.md`

Example:
```
/SWARM/deadletters/2026-03-16T2127-claude-orphan-cry.md
```

### Content Format

```markdown
# DEADLETTER REPORT

**Timestamp**: 2026-03-16T21:27:23-06:00  
**Source**: Claude (Anthropic)  
**Issue**: ORPHAN CRY handoff — no recipient identified

## What was attempted

[Describe what the agent tried to do]

## Why it failed / why it's orphaned

[Root cause of breakdown]

## What needs to happen next

[Specific actions required to resolve]

## Suggested recipients

- Microsoft Copilot?
- GitHub Admin Agents?
- Logan directly?

---

**Status**: AWAITING PRINCIPAL TRIAGE  
**@loganfinney27**: Please review and route.
```

## TRIAGE CHECKLIST

Principal (Logan) should:
- [ ] Review all deadletters in `/SWARM/deadletters/`
- [ ] Decide: who should own this? (which agent?)
- [ ] Route to appropriate node OR update agent role
- [ ] Mark resolved (delete deadletter or archive)
- [ ] Update `agents.json` if new capability revealed
