---
title: "SPEC — Swarm Linear Gateway"
updated: 2026-03-29
status: draft
authority: GitHub Copilot
type: spec
tags:
  - administration/spec
  - administration/linear
  - swarm/coordination
aliases:
  - Linear Gateway
  - Swarm Linear Gateway
---

# SPEC — Swarm Linear Gateway

**Status:** Draft — awaiting Logan approval before any live-write credentials are issued
**Related Linear issues:** LAF-7 (Swarm coordination), LAF-3 (Connect your tools)
**Produced by:** GitHub Copilot, 2026-03-29

---

## 1. Purpose

Swarm agents need a governed, auditable, single-choke-point interface to Linear. Direct credential distribution to every agent is a security and auditability failure. This spec defines a **Swarm Linear Gateway** — a broker pattern that mediates all agent reads and writes to the Linear GraphQL API under Logan's operating rules.

---

## 2. Architecture

```
                         ┌─────────────────────────────────┐
                         │         LINEAR (GraphQL)         │
                         │  api.linear.app/graphql          │
                         │  Webhook events → forwarder      │
                         └────────────┬────────────────────┘
                                      │
                    ┌─────────────────▼─────────────────────┐
                    │       SWARM LINEAR GATEWAY             │
                    │   .github/scripts/linear_gateway.py   │
                    │                                        │
                    │  • Auth (one scoped API key)           │
                    │  • Permission enforcement              │
                    │  • Idempotency + correlation IDs       │
                    │  • MCP action log emission             │
                    │  • Dry-run default                     │
                    └──┬────────┬────────┬────────┬─────────┘
                       │        │        │        │
              Observer  Executor  Coord.  Secretary
              (read-only) (write)  (reconcile) (draft)
```

**Linear webhook path:**

```
Linear → Cloud forwarder → GitHub repository_dispatch → linear-webhook.yml → gateway script
```

The forwarder (a small Cloud Function or Vercel edge function) is outside this repo. It converts Linear's outbound webhook payload into a `repository_dispatch` event. The GitHub Action (`linear-webhook.yml`) validates and routes it.

---

## 3. Agent Roles

| Role | Can read? | Can write? | Auth scope | Purpose |
|---|---|---|---|---|
| **Observer** | Yes | No | `read` | Summarize issue status, detect drift, generate CHECKPOINT data |
| **Executor** | Yes | Yes (authorized only) | `read+write` | Post comments, update issue status, link PR context |
| **Coordinator** | Yes | Yes (reconcile only) | `read+write` | Reconcile GitHub ↔ Linear mapping; flag conflicts |
| **Secretary** | Yes | Yes (comments only) | `read+comment` | Draft updates, digest summaries, CHECKPOINT records |

Role assignment is per-agent, per-invocation. No agent self-elevates. Roles are passed as CLI flags to the gateway script.

---

## 4. Broker API Contract

All five commands are implemented in `.github/scripts/linear_gateway.py`. All commands emit an MCP action log on completion.

### 4.1 `read_issue`

```
linear_gateway.py read_issue --issue-id <LAF-XX>
```

- **Auth required:** `read`
- **GraphQL:** `query { issue(id: $id) { id identifier title description state { name } assignee { name email } labels { nodes { name } } priority updatedAt } }`
- **Output:** structured YAML to stdout
- **Dry-run:** N/A (reads never mutate state)
- **Writes to vault:** No

### 4.2 `list_project_issues`

```
linear_gateway.py list_project_issues --project-id <id>
```

- **Auth required:** `read`
- **GraphQL:** `query { project(id: $id) { name issues { nodes { id identifier title state { name } assignee { name } priority } } } }`
- **Output:** structured YAML to stdout
- **Dry-run:** N/A
- **Writes to vault:** No

### 4.3 `post_comment`

```
linear_gateway.py post_comment --issue-id <LAF-XX> --body <text> [--live-write]
```

- **Auth required:** `read+write` or `read+comment`
- **GraphQL mutation:** `mutation { commentCreate(input: { issueId: $issueId, body: $body }) { success comment { id url } } }`
- **Idempotency:** body is hashed; duplicate comments within 24h window are suppressed
- **Dry-run:** default — prints body without posting; requires `--live-write` or `MCP_LIVE_WRITE=true` to post
- **Writes to vault:** No (Linear is the target, not the vault)

### 4.4 `update_issue_status`

```
linear_gateway.py update_issue_status --issue-id <LAF-XX> --state-name <"In Progress"|"Done"|...> [--live-write]
```

- **Auth required:** `read+write`
- **GraphQL:** first resolves state name → state ID via `workflowStates` query; then `mutation { issueUpdate(id: $issueId, input: { stateId: $stateId }) { success issue { id state { name } } } }`
- **Dry-run:** default; requires `--live-write` or `MCP_LIVE_WRITE=true`
- **Guard:** rejects status updates without a `--reason` flag (logged in action log)

### 4.5 `link_pr_context`

```
linear_gateway.py link_pr_context --issue-id <LAF-XX> --pr-url <url> --pr-title <title> [--live-write]
```

- **Auth required:** `read+write`
- **GraphQL mutation:** `mutation { attachmentCreate(input: { issueId: $issueId, url: $url, title: $title, subtitle: "GitHub PR" }) { success attachment { id } } }`
- **Dry-run:** default
- **Note:** Linear's native GitHub integration handles this automatically when GitHub integration is enabled; this command is the fallback for agents that cannot use the native integration

---

## 5. Webhook Design

### 5.1 Events subscribed

| Linear event | GitHub workflow trigger | Handler |
|---|---|---|
| `Issue` created/updated | `linear-webhook` dispatch | Observer: log drift; Coordinator: map to GitHub |
| `Comment` created | `linear-webhook` dispatch | Secretary: may draft reply if flagged |
| `Project` updated | `linear-webhook` dispatch | Coordinator: update DOCKET |
| `IssueStatus` changed | `linear-webhook` dispatch | Coordinator: reconcile GitHub label |

### 5.2 Signature validation

Linear webhooks include a `Linear-Signature` header (HMAC-SHA256 of the raw body, keyed by the webhook secret). The forwarder and the GitHub Action both validate this signature before processing. The gateway script's `--webhook-secret` flag (or `LINEAR_WEBHOOK_SECRET` env var) is required for any inbound event processing.

### 5.3 Repository dispatch payload schema

```json
{
  "event_type": "linear-webhook",
  "client_payload": {
    "action": "Issue.updated",
    "data": { "...": "Linear event data" },
    "url": "https://linear.app/...",
    "webhookTimestamp": "ISO-8601",
    "webhookId": "uuid"
  }
}
```

---

## 6. Security and Auth Model

| Concern | Mitigation |
|---|---|
| Credential sprawl | One `LINEAR_API_KEY` secret in GitHub repo secrets; never in vault files |
| Over-permissioned keys | Scope key to team LAF only; read-only by default |
| Runaway writes | Dry-run default; `--live-write` flag required for all mutations |
| Replay attacks | Idempotency key (24h window) suppresses duplicate mutations |
| Webhook forgery | HMAC-SHA256 signature validation required before processing |
| Audit trail | Every call emits MCP action log (correlation_id, outcome, idempotency_key) |
| Path traversal | All vault writes use `safe_output_path()` guardrails (same as `linear_brief_generator.py`) |

---

## 7. Operating Rules

1. **No meaningful work without a mapped Linear issue.** Every gateway write must include `--issue-id`. The script rejects calls without it.
2. **Dry-run is the default.** All mutations require explicit `--live-write` opt-in. This matches `mcp_guardrails.py` `resolve_live_write()`.
3. **All writes are logged.** `emit_action_log()` is called on every command completion (success or failure).
4. **Agents declare intent.** Every gateway invocation includes `--role` (observer|executor|coordinator|secretary) and `--initiating-agent` (e.g., `github-copilot`, `claude-code`).
5. **Logan approves new write permissions.** Role upgrades from read to write require a vault DECISION record before the secret is updated.

---

## 8. Audit Log Format

Per `mcp_guardrails.py`, every gateway call emits:

```yaml
mcp_action_log:
  action_type: "linear.post_comment"          # or read_issue, update_issue_status, etc.
  system_or_resource_id: "LAF-7"             # Linear issue identifier
  initiating_agent: "github-copilot"
  correlation_id: "20260329T010925Z-abc123def456"
  outcome: "success"                          # or "failure"
  retry_count: 0
  related_ref: "copilot/logans-project-execution"
  idempotency_key: "a1b2c3d4e5f6a1b2c3d4e5f6"
  live_write: true
```

---

## 9. Phase Rollout

| Phase | Scope | Gate |
|---|---|---|
| **Phase 0** | Read-only commands (`read_issue`, `list_project_issues`). No secrets required — uses public API. | This spec approved |
| **Phase 1** | `post_comment` live-write enabled. `LINEAR_API_KEY` added to repo secrets (scoped read+comment). | Logan decision record in `!/DECISIONS.md` |
| **Phase 2** | `update_issue_status` and `link_pr_context` enabled. Key scope upgraded to `read+write`. | Logan decision record + one dry-run verified |
| **Phase 3** | Webhook receiver deployed. Forwarder function running. Agents react to Linear events. | Logan approves forwarder service |

---

## 10. Open Questions for Logan

- [ ] Which GitHub secret name should hold the Linear API key? (`LINEAR_API_KEY` assumed)
- [ ] Should the API key scope cover all LAF projects or only specific teams?
- [ ] Where will the webhook forwarder function live? (Vercel, Cloudflare, AWS Lambda?)
- [ ] Should the Coordinator role be a separate GitHub Actions job or a flag in the same script?
- [ ] Does the Secretary role need to write CHECKPOINT records back to Linear comments automatically?
- [ ] Is OpenAI Swarm (see `!/SURVEY-OPENAI-SWARM-2026-03-29.md`) a candidate for the gateway orchestration layer?
