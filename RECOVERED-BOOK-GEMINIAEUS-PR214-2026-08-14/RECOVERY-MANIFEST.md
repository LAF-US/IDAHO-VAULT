# Recovery Manifest — Book of GEMINIAEUS Export

## Recovery status

**Recovered evidence bundle; non-canonical; not merged; not promoted.**

This bundle preserves a GitHub-exported version of the Book of GEMINIAEUS without inserting any of its contents into the live `main` branch, the local VAULT checkout, or a Court record. Possession of the bundle establishes only that these artifacts were present in the cited GitHub commit. It does not establish the truth, authority, historical authorship, legal status, or present operational effect of any statement inside the recovered artifacts.

## Source provenance

| Field | Value |
|---|---|
| Repository | `LAF-US/IDAHO-VAULT` |
| Pull request | [#214](https://github.com/LAF-US/IDAHO-VAULT/pull/214) |
| PR state | Closed without merge on 2026-04-12 |
| PR head | `codex/live-state-snapshot` |
| Source commit | `d59502e626c242828e946ab0581ceeb54b880b0f` |
| Source commit title | `Add MIND grimoire shards, manifest, and protocols` |
| Recovery date | 2026-08-14 |
| Retrieval method | GitHub commit tarball API for the exact source commit |
| Current live branch | `main` |

## Recovered artifacts

The bundle contains **75 recovered artifacts** from the source commit:

| Artifact class | Count | Preserved location |
|---|---:|---|
| Book index | 1 | `original-tree/!/MIND/BOOK-OF-GEMINIAEUS/INDEX.md` |
| Book sheets | 72 | `original-tree/!/MIND/BOOK-OF-GEMINIAEUS/Sheet1.md` through `Sheet72.md` |
| Companion | 1 | `original-tree/Companion to the Book of GEMINIAEUS.md` |
| Three Caesars record | 1 | `original-tree/THE THREE CAESARS.txt` |

`Sheet72.md` identifies the recovered Book as incomplete. The recovered index and all related frontmatter remain original source content; none of their authority fields have been adopted by this recovery.

## Integrity records

The exact GitHub source archive is retained at:

```text
source-archive/IDAHO-VAULT-d59502e6.tar.gz
```

Its SHA-256 digest is:

```text
40733a8eba4c7aafd5644d04044a785371a5a1b1b616461527af99ed8ea8cc6d
```

The per-artifact SHA-256 inventory is retained in `artifacts.sha256`. The source archive digest is also retained in `archive.sha256` and beside the archive in `source-archive/IDAHO-VAULT-d59502e6.tar.gz.sha256`.

From this bundle directory, verify the preserved bytes with:

```bash
sha256sum -c artifacts.sha256
sha256sum -c archive.sha256
(cd source-archive && sha256sum -c IDAHO-VAULT-d59502e6.tar.gz.sha256)
```

## Explicit boundary

This recovery does **not**:

- restore the Book to `main`;
- merge, reopen, or alter PR #214;
- amend the GEMINIAEUS matter;
- assign an office, identity, culpability, or disposition to any persona;
- claim that a recovered page is current doctrine, a Court finding, or live authorization.

> Preservation is not promotion. Recovery is not reinstatement.

## Contents map

```text
RECOVERY-MANIFEST.md
artifacts.sha256
archive.sha256
original-tree/
  !/MIND/BOOK-OF-GEMINIAEUS/
    INDEX.md
    Sheet1.md ... Sheet72.md
  Companion to the Book of GEMINIAEUS.md
  THE THREE CAESARS.txt
source-archive/
  IDAHO-VAULT-d59502e6.tar.gz
  IDAHO-VAULT-d59502e6.tar.gz.sha256
```

## References

[1]: https://github.com/LAF-US/IDAHO-VAULT/pull/214 "LAF-US/IDAHO-VAULT PR #214"
[2]: https://github.com/LAF-US/IDAHO-VAULT/commit/d59502e626c242828e946ab0581ceeb54b880b0f "Source commit d59502e6"
[3]: https://github.com/LAF-US/IDAHO-VAULT/blob/main/!/BOOK-OF-GEMINIAEUS-RECOVERY-METHOD-2026-06-02.md "Existing Book recovery method"
