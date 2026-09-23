---
title: PULLMAN Cloud Run Snapshot Backup
date: 2026-06-18
status: current-after-pr-566
related:
  - "#566"
  - "#552"
  - "#512"
  - ".github/workflows/cloud-run-deploy.yml"
  - ".github/rclone-filter.txt"
---

# PULLMAN Cloud Run Snapshot Backup

## Plain-language summary

PULLMAN is the vault-to-Google-Cloud deploy and snapshot path for
`LAF-US/IDAHO-VAULT`.

When the `PULLMAN - Cloud Run Deploy` workflow succeeds, it proves that GitHub
Actions can authenticate to the `idaho-vault` Google Cloud project, build and
deploy the vault service container, and sync a filtered vault snapshot into
Google Cloud Storage.

The snapshot target is:

```text
gs://the-ledger-bucket/vault-snapshots/<github-sha>/
```

Because the path contains the Git commit SHA, each successful run writes to a
commit-addressed snapshot directory.

## What gets backed up

The backup is not a full repository clone. It is a filtered snapshot controlled
by `.github/rclone-filter.txt`.

Currently included:

- `!/**`
- `.github/workflows/**`
- `.github/scripts/**`
- `swarm.json`
- `AGENTS.md`
- `README.md`

Currently excluded:

- `_private/**`
- `.gemini/**`
- `.obsidian/**`
- `.venv/**`
- `.crewai/**`
- `node_modules/**`
- `.git/**`
- Python caches
- common local OS junk
- everything else not explicitly included

So the accurate claim is:

> Successful PULLMAN runs create a commit-keyed Google Cloud Storage snapshot of
> the canonical vault/control surfaces selected by `.github/rclone-filter.txt`.
> They do not create a complete clone of the repository.

## What the Cloud Run connection does

The workflow performs these stages:

1. Checks out the repository.
2. Loads the 1Password service account token from GitHub Actions secrets.
3. Authenticates to Google Cloud using GitHub OIDC and Workload Identity
   Federation.
4. Builds the Docker image from `Dockerfile`.
5. Pushes the image to Artifact Registry:

```text
us-central1-docker.pkg.dev/idaho-vault/idaho-vault/idaho-vault-swarm:<github-sha>
```

6. Deploys the image to Cloud Run service:

```text
idaho-vault-swarm
```

7. Installs and configures `rclone`.
8. Runs:

```text
rclone sync . gcs:the-ledger-bucket/vault-snapshots/<github-sha> \
  --filter-from .github/rclone-filter.txt \
  --transfers=8 \
  --checksum \
  --verbose
```

## Trigger behavior

The workflow runs on:

- `push` to `main` when `Dockerfile` or `.github/workflows/cloud-run-deploy.yml`
  changes.
- `merge_group`.
- Manual `workflow_dispatch`.

That means a successful PR-branch manual PULLMAN run can prove the branch is
deployable, but the durable post-merge evidence is the successful `main` or
merge-queue run.

## Current Google Cloud identities

Project:

```text
idaho-vault
```

Project number:

```text
1091966715900
```

Workload Identity Federation:

```text
pool: github-pool
provider: github-provider
condition: assertion.repository == 'LAF-US/IDAHO-VAULT'
```

GitHub Actions deployer identity:

```text
github-actions-sa@idaho-vault.iam.gserviceaccount.com
```

Cloud Run runtime identity:

```text
pullman-runtime@idaho-vault.iam.gserviceaccount.com
```

GitHub Actions repository variables:

```text
GCP_WORKLOAD_IDENTITY_PROVIDER
GCP_SERVICE_ACCOUNT
CLOUD_RUN_RUNTIME_SERVICE_ACCOUNT
```

GitHub Actions repository secret:

```text
OP_SERVICE_ACCOUNT_TOKEN
```

## Repair record

On 2026-06-18, PR #566 restored the PULLMAN connection after Logan provisioned
`OP_SERVICE_ACCOUNT_TOKEN` and the next infrastructure faults became visible.

Fixed chain:

- The old Google OIDC condition still trusted `loganfinney27` instead of the
  `LAF-US` organization repository.
- The Workload Identity service-account impersonation binding was stale.
- The Docker image used Python 3.9 even though the project requires Python
  3.10+.
- The Docker build ran `pip install -r requirements.txt` before copying
  `pyproject.toml` and `src/`, even though `requirements.txt` contains `-e .`.
- The container command used `gunicorn` without installing it.
- Cloud Run deployment needed a dedicated runtime service account rather than
  reusing the GitHub deployer identity.

Verified successful post-merge `main` run:

```text
https://github.com/LAF-US/IDAHO-VAULT/actions/runs/27784426335
```

That run passed:

- 1Password load
- Google OIDC auth
- Docker build
- Artifact Registry push
- Cloud Run deploy
- service URL output
- rclone setup
- GCS sync

Issues closed as resolved:

- #552
- #512

## Operational caveats

- Treat this as a filtered operational snapshot, not the only backup of the
  repository.
- If the filter changes, the backup meaning changes.
- If `rclone sync` is pointed at an already-used SHA path and the filter is
  changed, the path can be made to match the new filtered source. The current
  SHA-addressed target prevents normal runs from overwriting unrelated commits.
- The Cloud Run service is still a minimal application surface; the critical
  value today is the authenticated deploy and GCS snapshot path.
