---
name: GCP Vault Sync Infrastructure
description: Google Cloud infrastructure being built to sync/mirror IDAHO-VAULT content — "Nest Bridge" project
type: project
---

Logan is building a Google Cloud sync service for IDAHO-VAULT called the "Nest Bridge." Setup is guided step-by-step (likely via Gemini in Cloud Shell).

**Why:** Mirror vault README.md files to GCP storage; GitHub PAT securely stored in Secret Manager for repo access.

**GCP project ID:** `idaho-vault`
**Region:** `us-west1`

## Components (Phase III)

| Name | GCP Resource | Status |
|---|---|---|
| The Gatekeeper | Secret Manager secret: `Google-Cloud-idaho-vault-sync-service` (holds GitHub PAT) | Created — version 1 live |
| The Ledger | Cloud Storage bucket: `gs://the-ledger-bucket` | Live — provisioned `us-west1` @ 032926.2155 |
| The Trigger | Pub/Sub topic: `the-trigger-topic` | Step 4 — pending Logan's Cloud Shell run |
| The Forge | Artifact Registry: `us-west1-docker.pkg.dev/idaho-vault/idaho-vault-repo/vault-sync-service:latest` | Build uploading @ 032926.2224 |

**Next step after Trigger:** Deploy `vault-sync-service` to **Cloud Run** — final step before Nest Bridge is fully operational.

**How to apply:** When Logan references GCP sync, vault bridge, Cloud Storage, Secret Manager, or Cloud Run — this is the project. Check this memory for canonical resource names before suggesting anything.
