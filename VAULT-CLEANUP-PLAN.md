# VAULT CLEANUP PLAN - IDAHO-VAULT

## Current State
- **Git repo**: 1GB .git folder (bloated)
- **Duplicates**: 20,999 files, 3.14 GB recoverable
- **Large media in root**: 21GB+ MXF files, 9GB+ MP4s (not suitable for git)
- **Total files**: 165,026 (28K in root + 137K in subdirs)

## Phase 1: Git Bloat Analysis

### Check what's bloating .git
```bash
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' | sort -k2 -n | tail -20
```

### Remove large files from git history
Use BFG Repo-Cleaner or git filter-repo to remove:
- `*.MXF` files (21GB+ each)
- `*.mp4` files >100MB
- Any binaries accidentally committed

### Verify .gitignore
Ensure these are NOT tracked by git:
- `*.MXF`, `*.mxf`
- `*.mp4`, `*.MP4` 
- `*.jpg`, `*.png` (unless specifically needed)
- `google-cloud-sdk/`
- `node_modules/`
- `venv/`, `__pycache__/`

## Phase 2: Remove Duplicates (3.14 GB)

Based on `DEDUPE-REPORT.md` (493 groups, 20,999 files):

### Patterns to clean:
1. **`__src_scratch-folder__` files** - Likely safe to delete (copies from scratch)
2. **Version numbers `(1)`, `(2)`** - Review first, may be different content
3. **Numeric suffixes ` 1`, ` 2`** - Often true duplicates

### Cleanup script approach:
- Present each group interactively
- Default: Keep oldest (original), delete rest
- Option to skip, keep specific files, or mark as not duplicates

## Phase 3: Large Media Files (Root → Archive/External)

### Files over 1GB in root:
- `XD4_6602.MXF` (21.5 GB)
- `XD4_6594.MXF` (19.8 GB)
- `Clip0001-edited.mxf` (16.8 GB)
- `Clip0001.MXF` (16.1 GB)

**Recommendation**: Move to external storage or `!/archive/media/` - these don't belong in:
- Git repo (too large)
- Root (Obsidian Vault) - Obsidian can't preview MXF
- Cloud sync (bandwidth waste)

## Phase 4: Cloud Drive & MISPLACED Directories

### Google Cloud SDK (7,245 files)
- **Location**: `google-cloud-sdk/`
- **Status**: MISPLACED (not `!/` or `.*/`)
- **Action**: Should this be in vault? If yes, move to `!/tools/` or `!/archive/`. If no, delete.

### Other misplaced directories:
- `tweets/` (7,821 files) → Move to `!/archive/tweets/` or delete
- `THE-GEMSTONE/` (1,700 files) → Should be in `!/` or `.*/`?
- `go/` (661 files) → Likely should not be in vault
- `INBOX/`, `src/`, `scripts/` → Move to appropriate `!/` or `.*/` location

## Phase 5: Git Compression & Cleanup

After removing large files and duplicates:

```bash
# Prune loose objects
git gc --aggressive --prune=now

# Clean reflog
git reflog expire --expire=now --all

# Verify pack
git fsck --full
```

Expected result: .git folder from 1GB → <100MB

## Phase 6: Cloud Sync Optimization

### If using OneDrive/Google Drive/Dropbox:
1. **Exclude large media** from sync (use selective sync)
2. **Ensure `.git/` is synced** (critical for repo)
3. **Add to cloud exclude list**:
   - `*.MXF`, `*.mxf`
   - `google-cloud-sdk/`
   - `__pycache__/`, `*.pyc`
   - `node_modules/`

## Execution Order

1. **Phase 1**: Analyze git bloat (find large files in history)
2. **Phase 2**: Remove duplicates (safest, immediate space savings)
3. **Phase 3**: Move large media externally (biggest space savings)
4. **Phase 4**: Clean misplaced directories
5. **Phase 5**: Git cleanup (after files removed)
6. **Phase 6**: Cloud sync optimization

## Space Savings Estimate

| Phase | Action | Savings |
|-------|--------|---------|
| 2 | Remove duplicates | 3.14 GB |
| 3 | Move large media | 80+ GB |
| 4 | Clean misplaced dirs | 10-20 GB |
| 5 | Git compression | 500+ MB (from 1GB → <100MB) |
| **Total** | | **90-100+ GB** |

## Next Steps

Run Phase 1 analysis first to see what's in git history.
