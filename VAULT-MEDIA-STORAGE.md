---
authority: LOGAN
related:
  - Git
  - GitHub
  - Git LFS
  - gcloud
  - rclone
  - rsync
  - LAF-USB
  - VAULT-CONVENTIONS
  - media
  - source documents
---

# VAULT-MEDIA-STORAGE

The vault treats media, documents, and binaries as source material when they are
part of the record. Git should preserve the reference and ordinary repository
workflow, but Git is not the storage backend for every raw object.

## Storage Lanes

1. Files at or below normal GitHub limits can be committed directly when they
   are intentional vault content.
2. Files over 100 MB must be covered by Git LFS attributes before commit.
3. Files over 2 GB must not be committed to Git or Git LFS. Store the object in
   external durable storage and commit a Markdown note or manifest reference.

The 2 GB ceiling is the GitHub LFS per-object platform limit. Older vault notes
may refer to a 5 GB ceiling; for GitHub transport, treat 2 GB as authoritative.

## Transport and Mirrors

rclone, rsync, and `gcloud storage rsync` are the intended transport tools for
distribution, mirroring, caching, and backup lanes. Git remains the
authoritative index for small source files, LFS pointers, manifests, and notes.
These tools carry object payloads that are too large or too operationally heavy
for GitHub.

The Universal Sync Bus protocol is not yet live. Treat
`.github/scripts/vault-courier-sync.sh` as disabled historical scaffolding: it
depended on a credential that leaked and has not been reprovisioned. Do not use
that script as the active sync path. See `LAF-USB-PROTOCOL-FRAMEWORK.md` for
the proposed high-level framework. USB transport events may later be observed
through SBP pheromone trails, but SBP does not authorize transfers.

Track durable inventories and reference notes. Do not track local rclone
configs, gcloud credential stores, tokens, caches, logs, rsync partial
directories, or machine-local mirror state.

## External Object References

For an object that cannot live in Git LFS, commit a small durable reference
instead of the raw file. The reference should include:

- original filename
- external storage location, rclone remote key, or inventory key
- size
- checksum when available
- owner/source
- date acquired or created
- related note, package, episode, meeting, or record
- sensitivity/status metadata if the object is not publishable

The reference can live in a companion Markdown note, YAML frontmatter, or a
small manifest file near the related material. Do not commit access tokens,
signed URLs, private credentials, or local-only absolute paths as the durable
reference.

Example reference shape:

```yaml
external_objects:
  - original_filename: XD4_6602.MXF
    storage_key: media-archive:IDAHO-VAULT/2026/XD4_6602.MXF
    size: 21.03 GB
    checksum: null
    transport: rclone
    status: external
```

## Enforcement

The local pre-commit hook runs `.github/scripts/check_large_files.py --staged`.
GitHub Actions runs the same policy against changed files. These checks are
guards, not substitutes for editorial judgment.
