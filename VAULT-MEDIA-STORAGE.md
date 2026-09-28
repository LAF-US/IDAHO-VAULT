---
authority: LOGAN
related:
  - STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17
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

Vault Toolbox `rclone`, Vault Toolbox `rsync`, and `gcloud storage rsync` are
the intended transport tools for distribution, mirroring, caching, and backup
lanes. Git remains the authoritative index for small source files, LFS pointers,
manifests, and notes. These tools carry object payloads that are too large or
too operationally heavy for GitHub.

The Universal Sync Bus transfer layer is not yet delete-capable or fully
automated. Treat `.github/scripts/vault-courier-sync.sh` as disabled historical
scaffolding: it depended on a credential that leaked and has not been
reprovisioned. Do not use that script as the active sync path. See
`LAF-USB-PROTOCOL-FRAMEWORK.md` for the staged framework and
`.github/scripts/laf_usb_manifest.py` for the stable manifest connector. USB
transport events may later be observed through SBP pheromone trails, but SBP
does not authorize transfers.

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

### `.gitattributes` is case-sensitive

Git matches `.gitattributes` patterns case-sensitively by default, and
case-folding can't be relied on across platforms and configs (e.g.
`core.ignorecase` on case-insensitive filesystems), so a bare `*.mov` pattern is
not guaranteed to match `CLIP.MOV`. Cameras, decks, and phones routinely
write UPPERCASE extensions (`XD4_6602.MXF`, `MVI_1487.MOV`), so a lowercase-only
list would silently fail to LFS-track exactly the broadcast media this vault
holds the most of. To close that gap, every binary pattern in `.gitattributes`
uses case-folding character classes — `*.[Mm][Oo][Vv]` — that match all case
permutations. When adding a new binary type, follow the same form rather than a
bare lowercase glob.

One deliberate exception: `.mts` is shared between AVCHD camera video (binary)
and TypeScript module source (text). Its LFS rule is scoped to **uppercase
`.MTS`** only, and lowercase `.mts`/`.cts` are normalized as text — so not every
`.mts` variant is LFS-tracked.

This is belt-and-suspenders: `check_large_files.py` is the case-agnostic
backstop that still blocks any >100 MB file lacking LFS attributes (and any
file over the 2 GB ceiling) regardless of extension casing. The
`.gitattributes` form keeps the happy path working so that correctly cased
media is tracked automatically instead of tripping the guard.
