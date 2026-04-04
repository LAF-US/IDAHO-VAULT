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

## Scope Decision (to be confirmed)

- **Primary project:** `idaho-vault` *(confirm or replace)*
- **Environment split:** `dev` and `prod` separation *(confirm pattern: separate projects vs folder split)*
- **Promotion rule:** no production role grants before one successful dry-run and Logan approval in Linear.

## IAM Boundary Table

| Principal | Principal Type | Role(s) | Scope Level | Scope ID | Reason | Approved By | Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _TBD_ | user / service account / group | _TBD_ | org / folder / project / resource | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

## Guardrails

1. Default to least privilege and project-level scope unless an explicit exception is documented.
2. Any folder/org scope grant requires written justification in this file.
3. Service-account keys are disallowed unless no secure alternative exists and Logan explicitly approves.
4. Every role change must be logged in Linear (`LAF-18`) and reflected here.

## Verification Checklist

- [ ] Scope decision confirmed by Logan.
- [ ] At least one principal/role mapping entered.
- [ ] Dry-run evidence linked.
- [ ] Promotion/defer disposition posted in Linear.
