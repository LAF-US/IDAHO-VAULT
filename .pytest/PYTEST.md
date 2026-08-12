---
canonical_name: PULLMAN
persona_class: infrastructure_stub
status: reserved
origin: vault
load_mechanism: github_actions
anchor_file: .pullman/PULLMAN.md
stub_sentinel: "¿!?"
sync_policy: one-way
authority: LOGAN
related:
  - VAULT-CONVENTIONS
  - AGENTS
  - rclone-filter.txt
date created: 2026-06-17
---

# PULLMAN

Named for the Pullman Palace Car Company — George Pullman's railroad sleeping car enterprise. The name carries the sense of a smooth, reliable conveyance: content loaded, delivered without friction.

**Function:** One-way vault-to-GCS sync system. Moves committed vault content from the repository to a Google Cloud Storage bucket for durable external delivery.

**Infrastructure artifacts:**

- `.github/workflows/cloud-run-deploy.yml` — deployment workflow; currently a merge queue required check
- `.github/rclone-filter.txt` — rclone filter rules governing which vault content syncs

**Status note:** The original OIDC-based pipeline (`antigravity/pullman-oidc`) was pruned in April 2026 — pipeline files had a line-ending collision with 9,000 `.md` files in the same commit. The `cloud-run-deploy.yml` workflow is the intended clean rebuild, but the underlying infrastructure (GCP project, Cloud Run service, GCS bucket, 1Password service account, `OP_SERVICE_ACCOUNT_TOKEN`) has not been confirmed provisioned. See GitHub Issue #552.

**Open decision (Logan):** Path A — remove from merge queue required checks until infrastructure is ready. Path B — full provisioning.
