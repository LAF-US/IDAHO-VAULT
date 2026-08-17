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
  - Git Annex
---

# VAULT-MEDIA-STORAGE

The vault treats media, documents, and binaries as source material when they are
part of the record. Git should preserve the reference and ordinary repository
workflow, but Git is not the storage backend for every raw object.

## Storage Lanes

1. Files at or below normal GitHub limits can be committed directly when they
   are intentional vault content.
2. Files over 100 MB and at or below 2 GB use Git LFS when their payload belongs
   in GitHub's shared repository workflow.
3. Payloads deliberately managed as a distributed archive remain in their
   existing semantic Vault locations and use explicit per-path git-annex
   attributes. Git-annex payloads must have at least two known copies before a
   local copy may be dropped.
4. Files over 2 GB must not be committed to Git or Git LFS. They may use the
   git-annex path opt-in only after a durable annex content remote is configured
   and verified; otherwise store the object externally and commit a manifest.

The 2 GB ceiling is the GitHub LFS per-object platform limit. Older vault notes
may refer to a 5 GB ceiling; for GitHub transport, treat 2 GB as authoritative.

## Transport and Mirrors

Git-annex is the content-addressed coordination layer for explicitly selected
payloads. Vault Toolbox `rclone`, Vault Toolbox `rsync`, and
`gcloud storage rsync` remain
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

## Git, LFS, and Annex Ownership

The three systems have non-overlapping authority:

| Owner | Paths/content | Transport |
| --- | --- | --- |
| Git | Notes, code, configuration, and annex manifests | Normal branches and PRs |
| Git LFS | Existing `.gitattributes` media/document classes unless explicitly overridden | GitHub LFS |
| git-annex | Individually opted-in payloads at their existing semantic paths | Configured annex content remotes |

The root `.gitattributes` defaults `annex.largefiles` to `nothing`. It does not
assign annex ownership to any directory or extension. Opt in only a specific
existing path with a later rule that also clears any inherited LFS filter:

```gitattributes
/existing/semantic/path/payload.ext -filter -diff -merge -text annex.largefiles=anything
```

Then run `git annex add -- existing/semantic/path/payload.ext`. The ownership
validator rejects Git LFS/annex overlap, annex pointers without an explicit
path opt-in, LFS pointers at annex-owned paths, and raw Git blobs at annex-owned
paths. Moving a file into a special directory is neither required nor desired.

GitHub `origin` is branch/PR transport, not an annex payload remote. The
bootstrap disables automatic `git annex sync` against `origin`; operators must
configure a separate content remote before annexed bytes can leave a device.

## Cross-OS Initialization

Install Git, Git LFS, git-annex, and Python on each device. From a clean,
attached checkout run:

```sh
# Windows (Scoop)
scoop install git-annex

# macOS (Homebrew)
brew install git-annex

# Debian/Ubuntu
sudo apt install git-annex
```

Then verify and initialize this clone:

```sh
python .github/scripts/vault_git_storage.py doctor
python .github/scripts/vault_git_storage.py init --description "DEVICE-NAME OS"
```

The bootstrap uses repository version 10 defaults, SHA256E keys, two desired
copies, one minimum copy, and unlocked files on Windows, macOS, and Linux.
Unlocked pointer commits avoid making native Windows consume Unix symlinks.
`annex.thin` remains disabled because retaining the protected prior content is
more important than saving one local copy's disk space.

Native Windows may briefly enter an adjusted branch during filesystem probing.
The bootstrap refuses dirty/detached checkouts and restores the original clean
branch before returning. Normal code and pointer changes still move through
feature branches and pull requests; do not use an unrestricted `git annex sync`
as a substitute for the Vault's PR workflow.

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
