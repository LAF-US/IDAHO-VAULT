---
date created: Sunday, March 29th 2026, 9:16:51 pm
date modified: Monday, March 30th 2026, 10:16:53 am
related:
- Bridge
- CLI
- Cloud
- Gemini CLI
- III
- THE
- format
- infrastructure
authority: LOGAN
---
**SITREP: 032926.2120**
**FROM: Vault Advisor (Gemini CLI)**
**TO: Logan (for relay to Gemini Cloud Assist)**
**RE: BRIDGE DEPLOYMENT: PHASE II - THE BLOCKS**

Here are the three blocks required to move the "Nest Bridge" from code to infrastructure.


### 1. The `requirements.txt`

The service requires the following Python dependencies, with pinned versions as specified in `requirements.txt`:

```text
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
google-cloud-storage==2.14.0
google-cloud-secret-manager==2.17.0
google-cloud-pubsub==2.19.0
```

---

### 2. The Secret Injection

To securely mount `the-gatekeeper-secret` as the `GITHUB_PAT` environment variable within the Cloud Run service, use the following flag in your `gcloud run deploy` command:

```bash
--set-secrets=GITHUB_PAT=the-gatekeeper-secret:latest
```

---

### 3. The Artifact Protocol

Before building the container, create the Docker repository in Artifact Registry to store the image.

```bash
gcloud artifacts repositories create idaho-vault-repo \
    --repository-format=docker \
    --location=us-west1 \
    --description="Docker repository for IDAHO-VAULT sync service"
```

---

**STATUS:** The blocks are delivered. Awaiting confirmation for PHASE III.
