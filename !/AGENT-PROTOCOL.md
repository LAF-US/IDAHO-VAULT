---
title: AGENT PROTOCOL
updated: 2026-03-30
status: active
authority: "Claude Code (The Abhorsen) — established per CONSTITUTION.md"
tags:
  - administration/agents
  - administration/infrastructure
---

# AGENT PROTOCOL — IDAHO-VAULT

**Document:** Bootstrap protocol for agent invocation in IDAHO-VAULT  
**Script:** `!/agent.sh`  
**Status:** Active — 6-phase authentication/authorization/agency flow  
**Updated:** 2026-03-30

---

## The TRIUNE COVENANT

The AGENT PROTOCOL establishes the **TRIUNE COVENANT** — the binding contract between **Logan** (human), **agents** (software), and **vault** (record):

1. **Authentication** — Agents prove identity via 1Password
2. **Authorization** — Agents confirm capability tier via AGENTS.md
3. **Agency** — Agents load instructions and vault context, then execute with signing authority

This protocol ensures:
- No agent acts without Logan's direction
- All agent actions are authenticated, authorized, and signed
- Vault context (LEVELSET, CONSTITUTION, AGENTS, DECISIONS) is loaded before execution
- Work is checkpointed and logged

---

## The Six Phases

### Phase 1: Authentication (1Password)

**Requirement:** 1Password CLI (`op`) installed and authenticated  
**Check:** `op whoami` succeeds  
**Fallback:** Warn and continue (some agents may not need secrets)

```bash
authenticate_1password() {
  op whoami &> /dev/null || return 1
}
```

**Why:** Establishes secure credential access for 1Password-managed secrets (GitHub tokens, signing keys, API creds).

---

### Phase 2: Identification (Agent Registry)

**Input:** Agent name (e.g., `claude`, `gemini`, `codex`)  
**Lookup:** Match against known agents in `!/AGENTS.md`  
**Output:** Set `AGENT_DOTFOLDER` (e.g., `.claude`, `.gemini`)

```bash
identify_agent() {
  case "$agent" in
    claude|gemini|codex|copilot|perplexity|grok)
      AGENT_DOTFOLDER=".$agent"
      ;;
    *)
      return 1 ;;
  esac
}
```

**Why:** Confirms agent is recognized in the registry. Prevents unknown agents from executing.

---

### Phase 3: Authorization (Capability Tier Check)

**Input:** Agent name  
**Lookup:** Capability tier from `!/AGENTS.md` registry  
**Output:** Set `AGENT_TIER` (e.g., "Direct Write", "Direct Write (Support)", "Read/Analysis")

```bash
authorize_agent() {
  case "$agent" in
    claude)
      AGENT_TIER="Direct Write" ;;
    gemini)
      AGENT_TIER="Direct Write (Support)" ;;
    codex)
      AGENT_TIER="Direct Write (scripting)" ;;
    # ... etc
  esac
}
```

**Why:** Ensures agent does not exceed its capability tier. Agent cannot commit if tier is "Read/Analysis". Agent cannot modify Constitutional zone if tier is "Support".

---

### Phase 4: Agency (Load Context + Instructions)

**Substep 4a — Load Instructions**
```bash
load_agent_instructions() {
  # Read from .$agent/AGENTS.md or .$agent/{AGENT_NAME}.md
  # Set AGENT_INSTRUCTIONS env var
}
```

**Substep 4b — Load Vault Context**
```bash
load_vault_context() {
  # Load these into memory/env vars:
  # - LEVELSET-CURRENT.md (current vault state)
  # - CONSTITUTION.md (governance authority)
  # - AGENTS.md (agent registry)
  # - DECISIONS.md (confirmed decisions)
}
```

**Why:** Agent has full context before executing. Instructions say *how* to act. Vault context says *what* is the current state and what rules govern.

---

### Phase 5: Signing Authority (Git Configuration)

**Set git author** per agent identity:

```bash
configure_git_signing() {
  case "$agent" in
    claude)
      git config user.name "Claude Code (The Abhorsen)"
      GIT_AUTHOR_SUFFIX="-C"
      ;;
    gemini)
      git config user.name "Gemini (The Vault Advisor)"
      GIT_AUTHOR_SUFFIX="-G"
      ;;
    # ... etc
  esac
}
```

**Configure SSH signing** via 1Password:

```bash
git config gpg.format ssh
# (actual signing key comes from 1Password SSH agent)
```

**Why:** All commits are signed with agent identity. Logan can verify who made what change. Agent signature is appended to commit messages (e.g., `-C` for Claude Code).

---

### Phase 6: Checkpoint (Log Invocation)

**Emit structured log entry** to `!/agent-protocol.log`:

```json
{
  "timestamp": "2026-03-30T20:15:00Z",
  "agent": "claude",
  "phase": "init",
  "vault_root": "/path/to/IDAHO-VAULT",
  "git_author": "Claude Code (The Abhorsen)",
  "auth_status": "authenticated"
}
```

**Why:** Audit trail. Logan can see which agents invoked the protocol, when, and with what auth status.

---

## Usage

### For Agents (In Agent-Invoked Sessions)

Source the protocol at session start:

```bash
source !/agent.sh claude
# or
source !/agent.sh gemini
```

The protocol outputs a summary:

```
🔔 AGENT PROTOCOL — IDAHO-VAULT
════════════════════════════════════

✅ 1Password authenticated
✅ Agent identified: claude
✅ Authorization granted: claude (Direct Write)
✅ Instructions loaded: ./.claude/CLAUDE.md
✅ Vault context loaded (LEVELSET, CONSTITUTION, AGENTS, DECISIONS)
✅ Git signing configured: claude (-C)
✅ Checkpoint logged: claude (init)

✅ AGENT PROTOCOL INITIALIZED
════════════════════════════════════

Ready: claude (Tier: Direct Write)
Context: LEVELSET, CONSTITUTION, AGENTS, DECISIONS
Signing: -C

Next: Read $AGENT_INSTRUCTIONS, consult vault context, then proceed.
```

Agent then proceeds with work, using environment variables:

```bash
# In agent session after `. !/agent.sh claude`
cat "$AGENT_INSTRUCTIONS"        # Read own instructions
cat "$VAULT_LEVELSET"           # Check current vault state
cat "$VAULT_AGENTS"             # Verify capability tier
```

### For Logan (Manual Invocation)

Test agent protocol:

```bash
cd /path/to/IDAHO-VAULT
source !/agent.sh claude
```

Verify checkpoint was logged:

```bash
tail -20 !/agent-protocol.log
```

---

## Environment Variables Set by Protocol

After successful initialization, the following are available in the shell:

| Variable | Example | Meaning |
|---|---|---|
| `AGENT_NAME` | `claude` | Invoked agent |
| `AGENT_DOTFOLDER` | `.claude` | Agent's dotfolder |
| `AGENT_TIER` | `Direct Write` | Capability tier |
| `AGENT_INSTRUCTIONS` | `.claude/CLAUDE.md` | Path to instructions |
| `VAULT_LEVELSET` | `./!/LEVELSET-CURRENT.md` | Current vault state |
| `VAULT_CONSTITUTION` | `./!/CONSTITUTION.md` | Governance authority |
| `VAULT_AGENTS` | `./!/AGENTS.md` | Agent registry |
| `VAULT_DECISIONS` | `./!/DECISIONS.md` | Decision log |
| `GIT_AUTHOR_SUFFIX` | `-C` | Agent signature for commits |

---

## Security Model

### What the Protocol Protects Against

1. **Unknown agents executing** — Phase 2 (Identification) checks against registry
2. **Agents exceeding tier** — Phase 3 (Authorization) checks capability
3. **Agents acting without instructions** — Phase 4a (Load Instructions) enforces read-before-execute
4. **Agents without vault context** — Phase 4b (Load Context) ensures awareness of current state
5. **Unsigned commits** — Phase 5 (Signing) ensures all agent work is attributable
6. **Lost audit trail** — Phase 6 (Checkpoint) logs all invocations

### What the Protocol Does NOT Protect Against

- **Compromised 1Password account** — If attacker has 1Password access, protocol cannot stop them
- **Compromised agent credentials** — If agent dotfolder is compromised, they can assume the agent's identity
- **Logan's mistake in approving bad PRs** — Protocol enforces signing and logging, but Logan reviews merges

**Conclusion:** Protocol is about **transparency, attribution, and enforcement of tier boundaries**. Logan remains the sole decision-maker.

---

## Error Handling

If any phase fails, the protocol prints the failure and returns. Agent is NOT initialized.

Examples:

```bash
# 1Password not installed
source !/agent.sh claude
# Output: ❌ 1Password CLI not found. See .op/SETUP.md

# Agent not in registry
source !/agent.sh unknown
# Output: ❌ Unknown agent: unknown

# Instructions not found (warning, continues)
source !\agent.sh new_agent
# Output: ⚠️  No instructions found: ./new_agent/NEW_AGENT.md
```

---

## Implementation Notes

- **Bash 4.0+** required (associative arrays in authorization check)
- **Git** required (for git config read/write)
- **1Password CLI** optional (graceful degradation if not present)
- **Log file** `.!agent-protocol.log` is append-only, never truncated

---

## Future Extensions

1. **Phase 0.5: DING handoff** — Read prior session state from handoff file
2. **Phase 6.5: Mid-execution checkpoints** — Log agent progress at key milestones
3. **Phase 7: Closure** — Log final state and emit summary for Logan review

---

## Related Files

- `!/agent.sh` — Protocol implementation (this is the executable shim)
- `!/AGENTS.md` — Agent registry (phases 2, 3 read from here)
- `.claude/CLAUDE.md`, `.gemini/GEMINI.md`, etc. — Agent instructions (phase 4a reads)
- `!/LEVELSET-CURRENT.md` — Vault state (phase 4b reads)
- `!/CONSTITUTION.md` — Governance (phase 4b reads)
- `!/DECISIONS.md` — Decision log (phase 4b reads)
- `.op/SETUP.md` — 1Password setup (phase 1 prerequisite)

---

**Covenant sealed.** Agents that invoke this protocol prove their intent, confirm their authority, load their context, and sign their work. Logan retains sole decision-making power. The vault is the record.

*The world is quiet here.*
