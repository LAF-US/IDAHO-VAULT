---
title: AGENT PROTOCOL
updated: 2026-04-02
status: active
authority: LOGAN
related:
- 1Password
- '2026-04-02'
- AGENTS
- CONSTITUTION
- DECISIONS
- GitHub
- LEVELSET
- LEVELSET-CURRENT
- LOGAN
- PROTOCOL
- README
- TRIUNE
- VAULT-CONVENTIONS
- agent
- chain
- codex
- coordination
- format
- index
- sign
---
# AGENT PROTOCOL - IDAHO-VAULT

**Document:** Local bootstrap protocol for agent invocation in IDAHO-VAULT  
**Entrypoint:** `!/agent.sh`  
**Bootstrap index:** `!/agents.json` (generated from `swarm.json`)  
**Status:** Active

---

## Summary

The local bootstrap path now follows a clear authority chain:

1. `!/AGENTS.md` is the canonical narrative registry.
2. `swarm.json` is the canonical machine-readable registry.
3. `!/agents.json` is a generated bootstrap index for local shell use only.
4. `!/agent.sh` is the executable entrypoint.

This protocol is for local agent bootstrap, context loading, git identity setup, and checkpoint logging. It is **not** the place for Linear, Slack, or Hugging Face authentication.

---

## TRIUNE COVENANT

The protocol still enforces the same three commitments:

1. **Authentication** - confirm 1Password availability when needed
2. **Authorization** - resolve the agent through the registry chain
3. **Agency** - load vault context before execution and sign attributable work

---

## Bootstrap Data Model

`!/agents.json` is derived from `swarm.json` and should not be edited by hand.
Root `agents.json` is a byte-for-byte compatibility mirror and is also generated.

Each bootstrap-capable agent record includes:

- invocation name (`claude`, `codex`, `copilot`, `gemini`, `grok`, `perplexity`)
- resolved instructions file
- capability tier
- git identity
- required context bundle
- optional context bundle

The root mirror exists for continuity with older `agents.json` references, but it is not an independent source of truth.

---

## Required And Optional Context

`!/agent.sh` requires these files before execution:

- `!/README.md`
- `!/CONSTITUTION.md`
- `!/AGENTS.md`
- `!/DECISIONS.md`
- `!/VAULT-CONVENTIONS.md`

Optional advisory context:

- `!/LEVELSET.md`

`!/LEVELSET-CURRENT.md` is **not** required and is no longer a bootstrap gate.

---

## Protocol Phases

### 1. Authentication

- Checks whether `op` is available.
- Reuses an existing 1Password session when possible.
- Warns and continues if secrets are unavailable.

### 2. Identification

- Resolves the invocation name through generated `!/agents.json`.
- Rejects unknown agents.

### 3. Authorization

- Reads the capability tier from the generated bootstrap record.
- Uses registry-derived tier data instead of hardcoded shell tables.

### 4. Agency

- Loads the agent instructions file from the bootstrap record.
- Loads the required vault context bundle.
- Surfaces `!/LEVELSET.md` only as optional advisory context.

### 5. Signing Authority

- Configures git author name and email from the bootstrap record.
- Sets `gpg.format ssh` for attributable agent work.

### 6. Checkpoint

- Appends a structured invocation record to `!/agent-protocol.log`.
- Uses the same log path everywhere in the protocol and documentation.

---

## Read-Only Inspection Modes

The shell entrypoint now supports non-mutating inspection:

```bash
source !/agent.sh --describe codex
source !/agent.sh --validate codex
source ./agent.sh --describe codex
```

Use these modes to verify bootstrap facts without changing git config or writing a checkpoint.

- `--describe <agent>` prints the resolved bootstrap record, context paths, and control-plane roles.
- `--validate <agent>` checks that the instructions file and required context files exist.

---

## Control-Plane Triptych

For this lane, the swarm control plane is intentionally narrow:

- **GitHub** handles branches, PRs, workflows, and durable execution transport.
- **Linear** handles issue state, routing, handoffs, and active coordination.
- **Slack** is breadcrumb-only and never the durable record.
- **Hugging Face** is available for research/models/docs/jobs, but remains outside bootstrap and outside live coordination writes in this issue.

This mapping is documented in `swarm.json` under `control_plane` and echoed into `!/agents.json` for local inspection.

---

## Usage

### Bootstrap a session

```bash
source !/agent.sh claude
source !/agent.sh codex
source !/agent.sh copilot
```

### Inspect a session target

```bash
source !/agent.sh --describe gemini
source !/agent.sh --validate copilot
```

---

## Related Files

- `!/agent.sh` - executable bootstrap entrypoint
- `agent.sh` - root compatibility wrapper that delegates to `!/agent.sh`
- `!/agents.json` - generated bootstrap index
- `agents.json` - root compatibility mirror of `!/agents.json`
- `swarm.json` - canonical machine-readable registry
- `!/AGENTS.md` - canonical narrative registry
- `!/README.md` - orientation anchor
- `!/VAULT-CONVENTIONS.md` - routing and shared behavior
- `.github/scripts/generate_agents_bootstrap.py` - generator for `!/agents.json`

---

The vault is the record. Logan decides. Agents bootstrap through the registry chain and act only inside those boundaries.
