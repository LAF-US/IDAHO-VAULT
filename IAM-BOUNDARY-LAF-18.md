---
title: "IAM Boundary Table — LAF-18"
created: 2026-04-01
updated: 2026-04-01
status: draft
authority: "LOGAN"
authors:
  - ChatGPT Codex
linear_id: "LAF-18"
type: implementation-note
source: issue/LAF-18
generated: false
---

## Purpose

This file is the concrete IAM boundary artifact required by `!/BRIEF-LAF-18-2026-03-30.md` before any Gemini + Google Cloud automation lane is promoted beyond pilot.

## Scope Decision

- **Primary project:** `idaho-vault` (Confirmed 2026-04-04 by Claude Code)
- **Environment split:** Single project (`idaho-vault`) for initial swarm-state ledger. `dev` separation is currently logical-only (e.g., bucket paths) rather than project-level.
- **Promotion rule:** No production role grants before one successful dry-run and Logan approval in Linear.

## IAM Boundary Table

| Principal | Principal Type | Role(s) | Scope Level | Scope ID | Reason | Approved By | Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vault-courier@idaho-vault.iam.gserviceaccount.com` | service account | `roles/storage.objectViewer`, `roles/logging.logWriter` | project / resource | `idaho-vault` / `gs://the-ledger-bucket` | Courier for swarm coordination state and ledger audit logs. | LOGAN (via DOCKET) | 2026-04-04 |

## Guardrails

1. Default to least privilege and project-level scope unless an explicit exception is documented.
2. Any folder/org scope grant requires written justification in this file.
3. Service-account keys are disallowed unless no secure alternative exists and Logan explicitly approves.
4. Every role change must be logged in Linear (`LAF-18`) and reflected here.

## Evidence Logs (Pilot Phase)

| Date | Task | Result | Artifact / Proof |
| --- | ---| --- | --- |
| 2026-04-04 | gcloud probe | **BLOCKED** | `IAM_PERMISSION_DENIED` on `gcloud iam service-accounts list` (expected) |
| 2026-04-04 | GCS access | **SUCCESS** | `gsutil ls gs://the-ledger-bucket` (exit code 0) |
| 2026-04-04 | Connected Dry-Run | **SUCCESS** | `gcloud storage cp gs://the-ledger-bucket/pilot/LAF-18-EVIDENCE.txt` |

## Verification Checklist

- [ ] Scope decision confirmed by Logan.
- [ ] At least one principal/role mapping entered.
- [ ] Dry-run evidence linked.
- [ ] Promotion/defer disposition posted in Linear.
