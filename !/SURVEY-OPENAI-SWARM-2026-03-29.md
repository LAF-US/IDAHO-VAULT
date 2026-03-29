---
title: "SURVEY — OpenAI Swarm"
updated: 2026-03-29
status: draft
authority: GitHub Copilot
type: survey
tags:
  - administration/survey
  - swarm/coordination
  - ai/openai
aliases:
  - OpenAI Swarm
  - openai/swarm
---

# SURVEY — OpenAI Swarm

**Status:** Draft — informational survey for Logan's decision on swarm orchestration
**Produced by:** GitHub Copilot, 2026-03-29
**Related:** `!/SPEC-LINEAR-GATEWAY-2026-03-29.md`, `!/BRIEF-LAF-3-2026-03-25.md`

---

## 1. What It Is

**OpenAI Swarm** (`openai/swarm` on GitHub) is a lightweight, experimental Python framework for multi-agent orchestration built on top of the OpenAI Chat Completions API. It was released by OpenAI's Solutions team in late 2024 as an educational reference implementation — not a production product.

- **Repo:** https://github.com/openai/swarm
- **Install:** `pip install git+https://github.com/openai/swarm.git` (Python 3.10+)
- **Status:** Experimental / educational. OpenAI's production recommendation is the **Agents SDK** (separate, maintained product).
- **Model support:** Any OpenAI model via Chat Completions API (default: `gpt-4o`).

---

## 2. Core Abstractions

### Agent

An `Agent` encapsulates:
- `name` — identifier
- `instructions` — system prompt
- `functions` — callable Python functions the agent can invoke
- `model` — optional model override

```python
from swarm import Swarm, Agent

agent = Agent(
    name="Coordinator",
    instructions="Reconcile GitHub and Linear issue mapping.",
    functions=[read_issue, link_pr_context],
)
```

### Handoff

Agents transfer control to other agents by returning an `Agent` object from a function. This enables multi-step, multi-role workflows without a central router:

```python
def transfer_to_secretary():
    return secretary_agent

coordinator_agent = Agent(
    name="Coordinator",
    functions=[transfer_to_secretary],
)
```

### Context Variables

A shared `dict` passed across the conversation that agents can read and modify. This is the only built-in persistence mechanism — it is in-memory only and does not survive between runs.

### Swarm Client

`Swarm()` wraps the OpenAI client and orchestrates `client.run(agent, messages, context_variables)`. The loop runs until no more tool calls are pending.

---

## 3. Strengths

| Strength | Notes |
|---|---|
| **Minimal API surface** | Two classes (`Swarm`, `Agent`), one method (`run`). Easy to read and extend. |
| **Handoff pattern** | Elegant model for role-based escalation without a hardcoded router. Maps cleanly to Observer → Secretary → Executor pipelines. |
| **Stateless by design** | Each `run()` is independent. Privacy-friendly; no cross-user leakage risk. |
| **Composable** | Agents can be assembled from functions, which map naturally to Linear gateway commands (`read_issue`, `post_comment`, etc.). |
| **Test-friendly** | Stateless design makes unit testing straightforward. |
| **Streaming support** | Compatible with OpenAI streaming API for real-time output. |

---

## 4. Limitations

| Limitation | Impact on IDAHO-VAULT |
|---|---|
| **No persistent memory** | Context variables reset each run. CHECKPOINT records and DOCKET state must be stored externally (vault files, Linear comments). |
| **OpenAI-only by default** | Hardcoded to Chat Completions API. Using Claude/Gemini agents requires patching or wrapping. |
| **Not production-ready** | No SLA, no regular PR reviews, no official support. OpenAI recommends migrating to Agents SDK for production. |
| **No built-in auth/permission layer** | Swarm has no concept of agent roles or write permissions. These would need to be enforced in the gateway functions themselves. |
| **No webhook/event support** | Swarm is invoked synchronously; it does not natively receive or react to external events. Linear webhook routing must be handled upstream. |
| **Python-only** | Must run in a Python environment. GitHub Actions can support this, but it is one more dependency. |

---

## 5. Comparison to UNIFIED SWARM (IDAHO-VAULT)

| Dimension | OpenAI Swarm | IDAHO-VAULT UNIFIED SWARM |
|---|---|---|
| **Coordination layer** | In-memory `context_variables` | Linear (durable), vault files, GitHub PRs |
| **Agent communication** | Handoff via return values | Logan relays; vault = shared state |
| **Persistence** | None (stateless per run) | Linear issues + vault markdown files |
| **Auth/permissions** | None built-in | Role flags in gateway script; scoped API keys |
| **Multi-model** | OpenAI models only | Claude, Codex, Gemini, Copilot, Grok |
| **Production posture** | Experimental | Operational (scraper, briefs, sorter running) |
| **Orchestration style** | Code-defined (Python) | Instruction-defined (markdown + LEVELSET) |
| **Audit trail** | None | MCP action logs (VAULT-CONVENTIONS) |

---

## 6. Applicability to IDAHO-VAULT

### What maps well

- **Agent + function model** is a good abstraction for the gateway broker. The five Linear gateway commands (`read_issue`, `list_project_issues`, `post_comment`, `update_issue_status`, `link_pr_context`) map directly to Swarm functions.
- **Handoff pattern** maps to the Secretary → Executor escalation path in the CHECKPOINT workflow.
- **Stateless design** matches the vault's approach: agents think ephemerally, write durably to Linear or the vault.

### What does not map

- **OpenAI-only** is a blocker. IDAHO-VAULT's swarm is multi-model (Claude, Codex, Gemini, Copilot). Any orchestration layer must be model-agnostic or use a wrapper.
- **No persistent memory** means Swarm cannot replace Linear as the durable coordination layer — it can only invoke the gateway script that reads/writes Linear.
- **No webhook support** means Swarm cannot serve as the webhook receiver. The GitHub Action (`linear-webhook.yml`) must handle event ingestion.

### Recommended use (if adopted)

Use OpenAI Swarm as a **local orchestration shell** for multi-step Linear gateway sequences — not as the primary coordination infrastructure:

```
GitHub Action / webhook event
  → linear_gateway.py (auth, logging, permissions)
    → [optional] Swarm session for multi-step reasoning
      → gateway functions (read_issue, post_comment, etc.)
        → Linear API
```

This keeps Swarm inside a single GitHub Actions job, stateless, model-specific, and fully auditable.

---

## 7. OpenAI Agents SDK (Successor)

OpenAI's production recommendation is the **Agents SDK** (separate repo, under active development). Key differences:

| Feature | OpenAI Swarm | Agents SDK |
|---|---|---|
| Production status | Experimental | Supported |
| Memory/storage | None | Built-in thread management |
| Tracing | None | Built-in tracing |
| Model support | OpenAI only | OpenAI + some third-party |
| Maintenance | Minimal | Active |

For IDAHO-VAULT, the Agents SDK has the same multi-model limitation as Swarm. Unless Logan standardizes on OpenAI models for gateway orchestration, neither Swarm nor the Agents SDK replaces the vault's existing multi-model swarm architecture.

---

## 8. Recommendation

| Scenario | Recommendation |
|---|---|
| **Gateway orchestration for multi-step Linear sequences** | Adopt Swarm as an optional local session shell — lightweight, low-risk, easy to drop later |
| **Primary swarm coordination layer** | Do not adopt — Swarm cannot replace Linear, vault files, or the multi-model agent roster |
| **Production webhook routing** | Do not adopt — use `linear-webhook.yml` GitHub Action instead |
| **Long-term** | Monitor OpenAI Agents SDK; revisit when multi-model support matures |

**Bottom line:** OpenAI Swarm is useful as a thin reasoning shell inside a single gateway invocation. It is not a coordination platform. Linear remains the durable execution layer. The vault remains doctrine. Logan remains the principal.

---

## 9. Open Questions for Logan

- [ ] Should `linear_gateway.py` optionally wrap Swarm for multi-step reasoning, or keep the gateway flat (no orchestration framework)?
- [ ] Is there a preference for OpenAI models (Codex/GPT-4o) vs. Claude for the gateway's reasoning steps?
- [ ] Should this survey be shared with Gemini (advisory) for a second opinion on the architecture framing?
