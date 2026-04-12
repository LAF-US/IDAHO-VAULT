---
date created: Sunday, April 12th 2026, 2:54:00 am
date completed: Sunday, April 12th 2026, 3:03:00 am
codename: AFFABLE BASTION
transport: PULLMAN
project-id: idaho-vault
project-number: "1091966715900"
status: ✅ COMPLETE — all five WIF gates executed
related:
  - CHICAGO MIGRATION
  - OIDC
  - LAF-18
  - Cloud Run
  - Artifact Registry
authority: LOGAN
---

# AFFABLE BASTION — OIDC Setup Checklist

> CI/CD pipeline: `loganfinney27` GitHub → Artifact Registry → Cloud Run
> No long-lived secrets. No JSON keys. OIDC tokens only.

**GCP Project ID:** `idaho-vault`
**GCP Project Number:** `1091966715900`
**GitHub Namespace:** `loganfinney27`
**Image Registry Region:** `us-central1`
**Codename:** AFFABLE BASTION | **Transport:** PULLMAN

---

## ⚠️ BEFORE YOU BEGIN: Auth Swap Required

Local `gcloud` is currently authenticated as the `vault-courier` service account.
Gates 0–2 require **Logan's personal user account** (owner/editor).

```powershell
# Swap to your personal account
gcloud auth login
gcloud config set project idaho-vault
gcloud config set account <your-google-account@gmail.com>
```

After Gate 2 is complete, the SA can be re-activated if needed:
```powershell
gcloud config set account vault-courier@idaho-vault.iam.gserviceaccount.com
```

---

## GATE 0 — Enable Required APIs

Run once. Safe to re-run (idempotent).

```bash
gcloud services enable \
  iamcredentials.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  developerconnect.googleapis.com \
  --project=idaho-vault
```

---

## GATE 1 — THE ARCHIVIST: Artifact Registry

```bash
gcloud artifacts repositories create idaho-vault \
  --repository-format=docker \
  --location=us-central1 \
  --description="AFFABLE BASTION — unified swarm image registry" \
  --project=idaho-vault
```

**Resulting image path:**
```
us-central1-docker.pkg.dev/idaho-vault/idaho-vault/<image>:<tag>
```

---

## GATE 2 — THE SENTRY: OIDC Workload Identity Federation

Run all five steps in sequence. Each is idempotent.

```bash
# Step 1: Create the identity pool
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --display-name="GitHub Actions Pool" \
  --project=idaho-vault

# Step 2: Add the GitHub OIDC provider
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Actions — loganfinney27" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == 'loganfinney27'" \
  --project=idaho-vault

# Step 3: Create the dedicated Service Account
gcloud iam service-accounts create "github-actions-sa" \
  --display-name="GitHub Actions — IDAHO-VAULT (AFFABLE BASTION)" \
  --project=idaho-vault

# Step 4a: Grant Artifact Registry write access
gcloud projects add-iam-policy-binding idaho-vault \
  --member="serviceAccount:github-actions-sa@idaho-vault.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Step 4b: Grant Cloud Run deploy access
gcloud projects add-iam-policy-binding idaho-vault \
  --member="serviceAccount:github-actions-sa@idaho-vault.iam.gserviceaccount.com" \
  --role="roles/run.developer"

# Step 5: Allow the GitHub OIDC pool to impersonate the SA
# Bound to the entire loganfinney27 org/namespace
gcloud iam service-accounts add-iam-policy-binding \
  "github-actions-sa@idaho-vault.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/1091966715900/locations/global/workloadIdentityPools/github-pool/attribute.repository_owner/loganfinney27" \
  --project=idaho-vault
```

**After Gate 2, these are your two permanent reference values:**

| Key | Value |
|-----|-------|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/1091966715900/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT` | `github-actions-sa@idaho-vault.iam.gserviceaccount.com` |

---

## GATE 3 — THE TWINS: GitHub Repository Variables

Set these in **GitHub → Settings → Secrets and variables → Actions → Variables** (not Secrets):

| Variable Name | Value |
|---------------|-------|
| `GCP_PROJECT_ID` | `idaho-vault` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/1091966715900/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT` | `github-actions-sa@idaho-vault.iam.gserviceaccount.com` |

---

## GATE 4 — THE WORKFLOW FILE

**Path:** `.github/workflows/cloud-run-deploy.yml`

> Antigravity will scaffold this file once Gates 0–3 are confirmed complete.
> It will target: `IDAHO-VAULT` repo → push to `main` → build → push to AR → deploy to Cloud Run.

---

## GATE 5 — VERIFICATION

```bash
# Confirm the pool and provider exist
gcloud iam workload-identity-pools list --location=global --project=idaho-vault
gcloud iam workload-identity-pools providers list \
  --workload-identity-pool=github-pool \
  --location=global \
  --project=idaho-vault

# Confirm the SA exists with correct bindings
gcloud iam service-accounts describe \
  github-actions-sa@idaho-vault.iam.gserviceaccount.com \
  --project=idaho-vault
```

---

## ✅ COMPLETED — 2026-04-12 ~03:03 MDT

- [x] Logan runs `gcloud auth login` — authenticated as `loganfinney27@gmail.com`
- [x] Gate 0: All 5 APIs enabled
- [x] Gate 1: Artifact Registry `idaho-vault` created (us-central1)
- [x] Gate 2: WIF pool + provider + SA + IAM bindings + impersonation — all confirmed
- [ ] Gate 3: GitHub Repository Variables — **PENDING LOGAN** (2 min in GitHub UI)
- [x] Gate 4: Workflow YAML scaffolded — `.github/workflows/cloud-run-deploy.yml` (PULLMAN pipeline with `op` + `rclone`)

## ⏳ REMAINING — Logan Action Required

**Set these in GitHub → Settings → Secrets and variables → Actions → Variables** *(safe to set now — non-sensitive config):*

| Variable | Value |
|----------|-------|
| `GCP_PROJECT_ID` | `idaho-vault` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/1091966715900/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT` | `github-actions-sa@idaho-vault.iam.gserviceaccount.com` |

---

## 🔴 HELD — LAF-UMS GOVERNANCE PAUSE

> **`OP_SERVICE_ACCOUNT_TOKEN`** secret formalization is **HELD pending SYNODS.**
> The swarm (LAF-US VFD) must convene deliberation before this cross-system binding is ratified.
> The 1Password service account token represents a trust boundary commitment that requires council review.

- The PULLMAN workflow will not trigger until this secret is present — safe to leave absent.
- The GCP/OIDC side is fully canonical and unaffected by this hold.
- The three GitHub Variables above are not in deliberation and may be set independently.

**Return path:** When SYNODS conclude, provision a 1Password SA token scoped to the `IDAHO-VAULT` vault and set `OP_SERVICE_ACCOUNT_TOKEN` as a GitHub Actions Secret.

---

###### [["The world is quiet here."]]
