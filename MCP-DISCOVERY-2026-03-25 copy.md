---
created: 2026-03-25
status: complete
phase: 0
related:
- '2026-03-25'
- Google
- Idaho
- Idaho Reports
- LOGAN
- MCP
- MCP-IMPLEMENTATION-PLAN
- PDF
- The world is quiet here
- URI
- agent
- coordination
- legislative
- template
authority: LOGAN
---
# MCP Phase 0 — Read-Only Discovery Log

**Timestamp:** 2026-03-25T00:00:00Z (session date)
**Supervisor:** LOGAN
**Executing agent:** Claude (The Abhorsen)
**Governance reference:** MCP-IMPLEMENTATION-PLAN

---

## Resource Inventory (`list_mcp_resources`)

Six resources returned across three servers. No resource templates returned (empty).

| URI | Name | Server | MIME Type |
|---|---|---|---|
| `ui://canva/search-designs` | search-designs-claude | claude.ai Canva | — |
| `ui://canva/generate-designs` | generate-designs-claude | claude.ai Canva | — |
| `ui://canva/generate-designs-structured` | generate-designs-structured | claude.ai Canva | — |
| `ui://canva/outline-review` | outline-review-claude | claude.ai Canva | — |
| `ui://widget/preview` | ui://widget/preview | claude.ai Box | `text/html;profile=mcp-app` |
| `ui://send-message-input.html` | Send Message Input Form | claude.ai Slack | `text/html;profile=mcp-app` |

**Observation:** Resources are all UI-layer widgets, not data resources. No Linear, Gmail, Google Calendar, or Hugging Face resources are exposed at the MCP resource layer. This is expected — these servers expose capabilities entirely through tools, not resources.

**Resource template inventory:** None returned.

---

## Tool Inventory by Server

### Linear (claude.ai Linear)

Full CRUD available.

| Category | Tools |
|---|---|
| Issues | `get_issue`, `list_issues`, `save_issue`, `get_issue_status`, `list_issue_statuses`, `list_issue_labels`, `create_issue_label` |
| Projects | `get_project`, `list_projects`, `save_project`, `list_project_labels` |
| Teams | `get_team`, `list_teams` |
| Users | `get_user`, `list_users` |
| Comments | `list_comments`, `save_comment`, `delete_comment` |
| Milestones | `get_milestone`, `list_milestones`, `save_milestone` |
| Initiatives | `get_initiative`, `list_initiatives`, `save_initiative` |
| Documents | `get_document`, `list_documents`, `create_document`, `update_document` |
| Cycles | `list_cycles` |
| Attachments | `get_attachment`, `create_attachment`, `delete_attachment` |
| Status Updates | `get_status_updates`, `save_status_update`, `delete_status_update` |
| Other | `search_documentation`, `extract_images` |

**Write capability:** Full. Issues, projects, milestones, initiatives, documents, comments, status updates — all writable.

---

### Slack (claude.ai Slack)

Read + write.

| Category | Tools |
|---|---|
| Read | `slack_read_channel`, `slack_read_thread`, `slack_read_user_profile`, `slack_read_canvas` |
| Search | `slack_search_channels`, `slack_search_users`, `slack_search_public`, `slack_search_public_and_private` |
| Write | `slack_send_message`, `slack_send_message_draft`, `slack_schedule_message` |
| Canvas | `slack_create_canvas`, `slack_update_canvas` |

---

### Gmail (claude.ai Gmail)

Read-heavy; limited write (draft creation only — no direct send).

| Category | Tools |
|---|---|
| Read | `gmail_read_message`, `gmail_read_thread`, `gmail_search_messages`, `gmail_list_labels`, `gmail_list_drafts`, `gmail_get_profile` |
| Write | `gmail_create_draft` |

---

### Google Calendar (claude.ai Google Calendar)

Full CRUD.

| Category | Tools |
|---|---|
| Read | `gcal_list_calendars`, `gcal_list_events`, `gcal_get_event`, `gcal_find_my_free_time`, `gcal_find_meeting_times` |
| Write | `gcal_create_event`, `gcal_update_event`, `gcal_delete_event`, `gcal_respond_to_event` |

---

### Box (claude.ai Box)

Full CRUD for files and folders.

| Category | Tools |
|---|---|
| Read | `get_file_content`, `get_file_details`, `get_file_preview`, `get_folder_details`, `list_folder_content_by_folder_id`, `list_file_comments`, `list_item_collaborations`, `list_tasks`, `list_metadata_templates`, `get_metadata_template_schema`, `search_files_keyword`, `search_files_metadata`, `search_folders_by_name`, `get_preview_page`, `who_am_i` |
| Write | `upload_file`, `upload_file_version`, `update_file_properties`, `create_folder`, `update_folder_properties`, `create_file_comment` |

---

### Hugging Face (claude.ai Hugging Face)

Read-only. No write tools.

| Category | Tools |
|---|---|
| Identity | `hf_whoami` |
| Hub | `hf_hub_query`, `hub_repo_search`, `hub_repo_details` |
| Docs | `hf_doc_search`, `hf_doc_fetch` |
| Papers | `paper_search` |
| Spaces | `space_search`, `dynamic_space` |

---

### Canva (claude.ai Canva)

Full creative CRUD.

| Category | Tools |
|---|---|
| Read | `get_design`, `get_design_content`, `get_design_pages`, `get_design_thumbnail`, `get_assets`, `get_export_formats`, `get_presenter_notes`, `list_comments`, `list_replies`, `list_brand_kits`, `list_folder_items`, `search_designs`, `search_folders`, `resolve_shortlink`, `export_design` |
| Write | `generate_design`, `generate_design_structured`, `create_design_from_candidate`, `resize_design`, `import_design_from_url`, `create_folder`, `move_item_to_folder`, `upload_asset_from_url`, `comment_on_design`, `reply_to_comment`, `start_editing_transaction`, `commit_editing_transaction`, `cancel_editing_transaction`, `perform_editing_operations`, `request_outline_review` |

---

## Workflow Mapping

| Server | Target IDAHO-VAULT workflow | Support status | Notes |
|---|---|---|---|
| **Linear** | SWARM task management, issue tracking, agent coordination | ✅ Supported | Full CRUD; cleanest idempotency path via `id` fields; already the coordination backbone |
| **Slack** | Agent breadcrumbs, Logan notifications, status updates | ✅ Supported | Read + write; `send_message_draft` allows dry-run equivalent |
| **Gmail** | Source outreach tracking, press release ingestion, tip intake | ⚠️ Partial | Read + search fully supported; write limited to draft creation (no direct send — appropriate for Phase 1 safety) |
| **Google Calendar** | Coverage planning, legislative hearing schedules, deadlines | ✅ Supported | Full CRUD; well-suited for scheduling automation |
| **Box** | Document storage, PDF attachments (Argonaut PDFs, reports) | ✅ Supported | Full CRUD; `search_files_keyword` + `get_file_content` cover ingestion path |
| **Hugging Face** | ML/AI research pipeline, model lookup, paper search | ✅ Supported (read) | Read-only is appropriate; no write workflows identified |
| **Canva** | Graphics/infographics for Idaho Reports stories | ⚠️ Partial | Capability exists but no current workflow identified; low priority |

---

## Capability Gap Register

| Gap | Impact | Provisional mitigation | Priority |
|---|---|---|---|
| MCP resource layer is UI-only (no data resources exposed) | Low — all actual capability is in tools, not resources | Treat tool inventory as the functional surface; resource layer is irrelevant for IDAHO-VAULT workflows | Low |
| Gmail: no direct send (draft-only) | Low for Phase 1 — draft creation is sufficient and safer | Create drafts; Logan reviews and sends manually | Low |
| Canva: no identified workflow | Low | Defer; no active story graphics automation in scope | Low |
| No resource templates returned | Low | Not needed; tools cover all identified workflows | Low |
| Idempotency strategy not yet defined for writes | Medium — needed before Phase 1 | Define per Phase 1 entry criteria: Linear issue `id`-based; Slack message `ts`-based; Calendar event `id`-based | Medium — Phase 1 gate item |
| Dry-run behavior not validated per tool | Medium — Phase 1 requires dry-run default | Define dry-run wrappers before any live writes; Linear and Slack have `draft`/preview analogues | Medium — Phase 1 gate item |

---

## Phase 0 Exit Criteria — Status

| Criterion | Status |
|---|---|
| Resource inventory completed and stored | ✅ Complete (this document) |
| Template inventory completed and stored | ✅ Complete (none returned) |
| Capability gap register created and reviewed | ✅ Complete |
| At least one Phase 1 write candidate selected | ✅ **Linear SWARM** selected (see below) |
| No unresolved critical unknowns re: auth, access, auditability | ✅ All servers authenticated; no auth gaps identified |

---

## Phase 1 Candidate: Linear SWARM

**Recommendation:** Linear as the sole Phase 1 write target.

**Rationale:**

1. **Structured identifiers** — Every Linear entity (`Issue`, `Project`, `Milestone`, `Initiative`, `Document`) has a stable UUID `id`. Idempotency keys map directly to these IDs: a create-or-update pattern is natively supported.
2. **Already the coordination backbone** — The SWARM label and agent workflow already route through Linear. MCP writes would extend existing, observed behavior rather than introducing a new system.
3. **Audit trail** — Linear maintains a complete activity log per issue/project. All MCP writes will be visible to Logan in the Linear UI independently of vault logs.
4. **Reversible** — Issues, comments, and status updates can be deleted or reverted. No destructive side effects from misconfigured writes.
5. **Clear scope boundary** — Phase 1 scope: issue creation, status updates, and comment saves on SWARM-labeled issues only. No project/initiative writes until Phase 2.

**Phase 1 entry criteria items to resolve before Gate 0→1:**
- Define idempotency key strategy: generate `idempotency_key = hash(agent_id + task_scope + timestamp_day)`, store in vault, replay behavior = skip if key already used
- Validate dry-run behavior: dry-run = log the intended operation to vault without calling `save_issue`/`save_comment`
- Document operator checklist for enabling/disabling live writes

---

## Gate 0 → 1 Readiness

**Status: READY** — All Phase 0 exit criteria met. No stop conditions triggered.

Recommend proceeding to Phase 1 planning once Logan reviews this document and approves the Linear SWARM write target.

---

###### "The world is quiet here."
