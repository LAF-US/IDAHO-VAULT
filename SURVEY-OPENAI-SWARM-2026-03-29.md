---
title: SURVEY - OpenAI Swarm
updated: 2026-03-30
status: draft
authority: LOGAN
type: survey
related:
- -LAF
- '2026-03-25'
- '2026-03-29'
- '2026-03-30'
- API
- BRIEF-LAF-3-2026-03-25
- CHECKPOINT
- Copilot
- GitHub
- LAF
- LOGAN
- Logan's
- OpenAI
- OpenAI Swarm
- README
- SDK
- SPEC-LINEAR-GATEWAY-2026-03-29
- UNIFIED
- agent
- coordination
- doctrine
---
# SURVEY - OpenAI Swarm

**Status:** Draft - informational survey for Logan's decision on swarm orchestration
**Produced by:** GitHub Copilot, revised by Codex, 2026-03-30
**Related:** `!/SPEC-LINEAR-GATEWAY-2026-03-29.md`, `!/BRIEF-LAF-3-2026-03-25.md`

---

## 1. What It Is

**OpenAI Swarm** (`openai/swarm` on GitHub) is a lightweight, experimental Python framework for multi-agent orchestration built on top of the OpenAI Chat Completions API. It was published as an educational reference implementation, not a production product.

- **Repo:** https://github.com/openai/swarm
- **Install:** `pip install git+https://github.com/openai/swarm.git` (Python 3.10+)
- **Status:** Experimental / educational. OpenAI's production recommendation is the **Agents SDK**.
- **Model support:** Any OpenAI model available through Chat Completions (default in the README: `gpt-4o`)

### Protocol note

The historical Swarm pattern is best understood as **agents + handoffs + tool execution inside a stateless client loop**. OpenAI's maintained protocol framing now lives in the **Agents SDK**, where the current collaboration choices are:

- **Handoffs** - a specialist takes over the conversation.
- **Agents as tools** - a manager keeps control and calls specialists as bounded tools.

That distinction matters more to IDAHO-VAULT than the old Swarm implementation details, because the vault already behaves more like a manager-plus-specialists system than a pure conversational handoff tree.

---

## 2. Core Abstractions

### Agent

An `Agent` encapsulates:

- `name` - identifier
- `instructions` - system prompt
- `functions` - callable Python functions the agent can invoke
- `model` - optional model override

```python
from swarm import Swarm, Agent

agent = Agent(
    name="Coordinator",
    instructions="Reconcile GitHub and Linear issue mapping.",
    functions=[read_issue, link_pr_context],
)
```

### Handoff

Agents transfer control to other agents by returning an `Agent` object from a function:

```python
def transfer_to_secretary():
    return secretary_agent

coordinator_agent = Agent(
    name="Coordinator",
    functions=[transfer_to_secretary],
)
```

### Context Variables

A shared `dict` passed across the conversation that agents can read and modify. This is the only built-in persistence mechanism. It is in-memory only and does not survive between runs.

### Swarm Client

`Swarm()` wraps the OpenAI client and orchestrates `client.run(agent, messages, context_variables)`. The loop described in the README is:

1. Get a completion from the current agent.
2. Execute tool calls and append results.
3. Switch agent if necessary.
4. Update context variables if necessary.
5. If no new function calls, return.

---

## 3. Strengths

| Strength | Notes |
|---|---|
| **Minimal API surface** | Two classes (`Swarm`, `Agent`), one main method (`run`). Easy to read and test. |
| **Handoff pattern** | Elegant model for role-based escalation without a hardcoded router. Maps cleanly to Observer -> Secretary -> Executor pipelines. |
| **Stateless by design** | Each `run()` is independent. No built-in cross-run memory. |
| **Composable** | Agents are assembled from functions, which maps naturally to gateway commands. |
| **Test-friendly** | Stateless design makes unit testing straightforward. |
| **Streaming support** | Compatible with OpenAI streaming flows. |

---

## 4. Limitations

| Limitation | Impact on IDAHO-VAULT |
|---|---|
| **No persistent memory** | Context variables reset each run. CHECKPOINT records and DOCKET state must be stored externally. |
| **OpenAI-only by default** | Using Claude, Gemini, or other agents requires wrapping or a separate orchestration layer. |
| **Not production-ready** | OpenAI explicitly recommends the Agents SDK for production use. |
| **No built-in auth or permission layer** | Agent write limits would still need to be enforced in gateway functions. |
| **No webhook or event layer** | Swarm is invoked synchronously. Webhook routing must live elsewhere. |
| **Python-only** | Adds a Python runtime dependency even if the broader stack is mixed. |

---

## 5. Comparison to UNIFIED SWARM (IDAHO-VAULT)

| Dimension | OpenAI Swarm | IDAHO-VAULT UNIFIED SWARM |
|---|---|---|
| **Coordination layer** | In-memory `context_variables` | Linear, vault files, GitHub PRs |
| **Agent communication** | Handoff via return values | Logan relays; vault is shared state |
| **Persistence** | None between runs | Linear issues plus vault markdown files |
| **Auth / permissions** | None built in | Role flags in gateway scripts and repo boundaries |
| **Multi-model** | OpenAI models only | Claude, Codex, Gemini, Copilot, Grok |
| **Production posture** | Experimental | Operational |
| **Orchestration style** | Code-defined Python loop | Instruction-defined markdown plus automation |
| **Audit trail** | Minimal | Vault files, PRs, issue logs |

---

## 6. Applicability to IDAHO-VAULT

### What maps well

- **Agent + function model** is a good abstraction for the gateway broker. Commands like `read_issue`, `post_comment`, and `link_pr_context` map cleanly to Swarm functions.
- **Handoff pattern** maps to the Secretary -> Executor escalation path in the CHECKPOINT workflow.
- **Stateless design** matches the vault's approach: agents think ephemerally and write durably to Linear or the vault.

### What does not map

- **OpenAI-only** is a blocker for any claim that Swarm could become the main vault orchestration layer.
- **No persistent memory** means Swarm cannot replace Linear as the durable coordination layer.
- **No webhook support** means Swarm cannot serve as the webhook receiver. The GitHub Action layer still has to own ingestion.

### Recommended use if adopted

Use OpenAI Swarm only as a **local orchestration shell** for multi-step gateway sequences:

```text
GitHub Action / webhook event
  -> linear_gateway.py (auth, logging, permissions)
    -> optional Swarm session for multi-step reasoning
      -> gateway functions (read_issue, post_comment, etc.)
        -> Linear API
```

This keeps Swarm inside a single job, stateless, model-specific, and auditable.

---

## 7. OpenAI Agents SDK (Successor)

OpenAI's current recommendation is the **Agents SDK**, which is the production-ready successor to Swarm. The important change is not just maintenance status; it is the protocol model. OpenAI now documents two first-class multi-agent collaboration patterns:

- **Handoffs** - use when the next specialist should own the user interaction.
- **Agents as tools** - use when a central orchestrator should keep the user-facing thread and call specialists as bounded subroutines.

For IDAHO-VAULT, the second pattern is usually the better fit. Logan remains the relay. The vault and Linear remain the durable state. Specialist agents should usually be called as scoped tools or workflow steps, not given standing conversational authority.

Key differences:

| Feature | OpenAI Swarm | Agents SDK |
|---|---|---|
| Production status | Experimental | Supported / actively maintained |
| Memory / storage | None | Session memory and thread management available |
| Tracing | None | Built-in tracing and observability |
| Tool model | Python functions and handoffs | Hosted tools, local tools, function tools, agents-as-tools, handoffs |
| Model support | OpenAI only | OpenAI plus some third-party support |

For IDAHO-VAULT, the Agents SDK still does not replace the repo's broader multi-model swarm architecture. It is relevant if Logan wants an OpenAI-centered orchestration shell with stronger tooling, tracing, and context management than old Swarm.

---

## 8. Recommendation

| Scenario | Recommendation |
|---|---|
| **Gateway orchestration for multi-step Linear sequences** | If OpenAI-only reasoning is acceptable, prefer Agents SDK over old Swarm |
| **Primary swarm coordination layer** | Do not adopt - neither Swarm nor Agents SDK replaces Linear, vault files, or the multi-model agent roster |
| **Production webhook routing** | Do not adopt - use `linear-webhook.yml` GitHub Action instead |
| **Long-term** | Monitor Agents SDK evolution and revisit only if the model and governance fit improves |

**Bottom line:** Old Swarm is useful mainly as a historical design reference. If Logan wants to borrow OpenAI's current protocol ideas, the relevant concepts are now in the Agents SDK: handoffs, agents-as-tools, managed tool types, and built-in tracing. Linear remains the durable execution layer. The vault remains doctrine. Logan remains the principal.

---

## 9. Open Questions for Logan

- [ ] Should `linear_gateway.py` stay flat, or should it gain an optional orchestration layer for multi-step reasoning?
- [ ] Is there any real benefit in standardizing gateway reasoning on OpenAI models, given the vault's existing multi-model setup?
- [ ] Should a follow-up note compare Agents SDK directly against the current vault relay model rather than against old Swarm?

---

## 10. Known Sources

- OpenAI Swarm README: https://github.com/openai/swarm/blob/main/README.md
- OpenAI cookbook, "Orchestrating Agents: Routines and Handoffs": https://developers.openai.com/cookbook/examples/orchestrating_agents/
- OpenAI cookbook, "Multi-Agent Portfolio Collaboration with OpenAI Agents SDK": https://developers.openai.com/cookbook/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration/
- OpenAI Agents SDK docs home: https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK docs, multi-agent patterns: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Agents SDK docs, handoffs: https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Agents SDK docs, tools: https://openai.github.io/openai-agents-python/tools/
