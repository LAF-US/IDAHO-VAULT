---
title: "HANDOFF - Codex Registry Repair"
created: 2026-04-02
updated: 2026-04-02
status: active
authority: "[[LOGAN]]"
authors:
  - ChatGPT Codex
type: handoff
source: issue/LAF-28
related:
  - LAF-25
  - LAF-28
tags:
  - administration/handoff
  - administration/control-plane
  - administration/registry
---

# HANDOFF - Codex Registry Repair

## Why this repair was needed

The vault's agent registry was conceptually coherent but materially split.
Docs pointed to `!/AGENTS.md`, `!/README.md`, `!/agents.json`, and `!/agent.sh`, while those files were missing or only partially represented on disk.
Root `agent.sh` was also computing the wrong vault root because it lived at repo root while behaving as if it lived under `!/`.

## Exact files touched

- `.github/scripts/generate_agents_bootstrap.py`
- `AGENTS.md`
- `AGENT-PROTOCOL.md`
- `AGENT-REGISTRY.md`
- `CONSTITUTION.md`
- `DECISIONS.md`
- `LEVELSET.md`
- `VAULT-CONVENTIONS.md`
- `agent.sh`
- `agents.json`
- `!/README.md`
- `!/AGENTS.md`
- `!/CONSTITUTION.md`
- `!/DECISIONS.md`
- `!/LEVELSET.md`
- `!/VAULT-CONVENTIONS.md`
- `!/agent.sh`
- `!/agents.json`
- `!/README 1.md`
- `BRIEF-LAF-28-2026-04-02.md`
- `!/__!__/!/! The world is quiet here/DOCKET.md`

## Reproduction commands

```bash
python .github/scripts/generate_agents_bootstrap.py
python .github/scripts/generate_agents_bootstrap.py --check
source !/agent.sh --describe codex
source !/agent.sh --validate codex
source ./agent.sh --describe codex
```

## Verification runbook

1. Confirm both generated indices exist and match:
   - `!/agents.json`
   - `agents.json`
2. Confirm canonical routing files exist:
   - `!/README.md`
   - `!/AGENTS.md`
   - `!/CONSTITUTION.md`
   - `!/DECISIONS.md`
   - `!/LEVELSET.md`
   - `!/VAULT-CONVENTIONS.md`
   - `!/agent.sh`
3. Confirm no conflict markers remain in:
   - `CONSTITUTION.md`
   - `DECISIONS.md`
   - `LEVELSET.md`
   - `VAULT-CONVENTIONS.md`
   - `agents.json`
4. Confirm the same authority chain is described in:
   - `AGENTS.md`
   - `!/AGENTS.md`
   - `AGENT-PROTOCOL.md`
   - `BRIEF-LAF-28-2026-04-02.md`
   - `DOCKET.md`

## Unresolved follow-ups

- The broader vault still has many unrelated working-tree changes outside this lane; they were intentionally left alone.
- If Logan wants the compatibility surfaces removed later, delete root `agent.sh` and root `agents.json` only after downstream references have been cleaned up.
