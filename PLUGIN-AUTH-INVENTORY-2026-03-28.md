---
tags:
  - administration/mcp
  - administration/plugins
  - administration/inventory
created: 2026-03-28
status: complete
phase: auth-inventory
---
# Plugin Auth Inventory - 2026-03-28

**Timestamp:** 2026-03-28T20:00:33-06:00
**Supervisor:** [[LOGAN]]
**Executing agent:** [[Codex]]
**Mode:** Read-only connector inventory
**Mutation rule:** No external writes performed

---

## Summary

Enabled plugin surfaces were checked for identity, minimal read access, and near-term workflow fit.

- GitHub, Linear, Slack, Google Calendar, Google Drive, and Hugging Face all returned valid read-only probes.
- Cloudflare has no direct identity/account probe exposed in this session, so it is marked `not-directly-probeable`.
- No auth failures were observed in the connectors that were directly probed.

---

## Inventory Matrix

| plugin | auth_state | identity | read_probe | write_surface_summary | vault_workflow_fit | risks_or_notes | recommended_next_action |
|---|---|---|---|---|---|---|---|
| GitHub | `verified` | `loganfinney27` (`id` `136375980`) | Authenticated profile returned; installation `118136039` present; `IDAHO-VAULT` visible in owned repositories; no org installs surfaced | Issues, PRs, reviews, labels, repo metadata, Actions-adjacent workflows | Core repo coordination surface; already canonical for branches, PRs, and Issues | App currently appears installed only on Logan's personal GitHub user account; `IDAHO-VAULT` visibility confirmed | Keep as a core coordination surface; do not use as the first MCP write pilot |
| Linear | `verified` | Logan Finney (`loganfinney27@gmail.com`) | Authenticated profile returned; team list returned one workspace team: `Logan Finney` (`58085b2c-f6e6-49e4-8ad3-04fc10d09f6c`) | Issues, comments, status updates, projects, milestones, documents | Best fit for SWARM execution tracking and the cleanest first write target | Workspace surface is live and readable; aligns with prior vault discovery recommending Linear-first | Use as **Phase 1** write pilot once live-write guardrails are explicitly scoped |
| Slack | `verified-read-only` | User `U0ALJEJMJM9`; username `loganfinney27`; real name Logan Finney; workspace/org `Logan Finney` | Current user profile returned with timezone `America/Denver`; owner/admin flags visible | Draft/send message and coordination surfaces exist, but Slack remains ephemeral by doctrine | Breadcrumbs, notifications, transient coordination only | Doctrine still applies: durable decisions must be promoted to Vault or Linear | Keep Slack breadcrumb-only for now; no pilot writes before Linear is stable |
| Google Calendar | `verified-read-only` | Logan Finney (`loganfinney27@gmail.com`) | Profile returned; `primary` availability probe for `2026-04-05T09:00:00-06:00` to `2026-04-05T17:00:00-06:00` returned no errors and no busy blocks | Event read/write/delete surfaces exist, but no mutation tested here | Coverage planning, deadline windows, hearing scheduling | Read path is clean; no event mutation was exercised in this pass | Defer to a later scheduling-specific pilot after Linear |
| Google Drive | `verified-read-only` | Logan Finney (`loganfinney27@gmail.com`) | Profile returned; shared drives list returned empty; recent documents returned valid surfaces including `Linear issues`, `Linear projects`, and `Constitutional revision` | File discovery and document access are available; broader edit workflows should be scoped separately | Supporting docs, staging surfaces, shared context overlap | Empty shared-drives result is not a failure; personal Drive visibility is clearly working | Treat Drive as a supporting read surface, not the first workflow target |
| Hugging Face | `verified-read-only` | `loganfinney27` | `whoami` returned authenticated user `loganfinney27` | Research/model/paper/job surfaces may exist, but no write workflow is in scope here | AI/ML research, model lookup, paper discovery | Read-only verification is sufficient for current vault needs | Keep read-only until a concrete research workflow requires more |
| Cloudflare | `not-directly-probeable` | No direct identity probe exposed in this session | No direct account/profile/auth probe was available from the current Cloudflare tool surface | Cloudflare skills are available for future Workers/Agents/MCP work, but no direct auth check was possible here | Future deployment and runtime infrastructure, not immediate vault coordination | This is a tool-surface limitation in the current session, not evidence of auth failure | Do not block the overall plugin program on Cloudflare; verify only when a concrete Cloudflare task exists |

---

## Acceptance Check

| Criterion | Status | Notes |
|---|---|---|
| Every enabled plugin is classified in the matrix | Complete | GitHub, Linear, Slack, Google Calendar, Google Drive, Hugging Face, Cloudflare all included |
| Identity captured for GitHub, Linear, Slack, Google Calendar, Google Drive, and Hugging Face | Complete | All six returned valid identity information |
| `IDAHO-VAULT` visibility confirmed in GitHub | Complete | Repository visible in owned repo listing |
| Google Drive returned at least one valid read surface | Complete | Recent document sample returned multiple valid docs |
| Google Calendar returned a valid read surface without mutation | Complete | Availability probe on `primary` returned cleanly |
| Cloudflare either verified with a real probe or explicitly marked `not-directly-probeable` | Complete | Marked `not-directly-probeable` due missing direct probe |
| Final report includes a single recommended first pilot and blocker list | Complete | See recommendation and blockers below |

---

## Recommendation

**Recommendation:** Proceed to **Phase 1 = Linear-first pilot**.

Why:

1. GitHub, Linear, Slack, Google Calendar, Google Drive, and Hugging Face all verified cleanly through read-only probes.
2. Linear returned both identity and workspace-team visibility, which is the strongest coordination signal in the enabled set.
3. Prior vault discovery already selected Linear SWARM as the cleanest first write target, and this inventory did not surface any auth surprise that would overturn that choice.

### Recommended Phase 1 shape

- **Linear SWARM only**
- Later read/write scope limited to issue creation, comments, and status updates
- Vault remains the durable record
- Slack remains breadcrumb-only
- No multi-plugin orchestration until the Linear pilot is stable

---

## Blockers

- No blocker was found in GitHub, Linear, Slack, Google Calendar, Google Drive, or Hugging Face during this inventory.
- Cloudflare remains unverified at the identity/account level only because no direct probe was exposed in this session. This should **not** block the next step.

---

## Suggested Next Step

Prepare a narrowly scoped implementation plan for a **Linear-first live-write pilot** using:

- explicit live-write gating
- deterministic idempotency keys
- structured MCP action logs in vault format
- no Slack writes except optional breadcrumb drafts after the Linear operation succeeds
