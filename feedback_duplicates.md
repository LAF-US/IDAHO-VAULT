---
name: Duplicate file verification
description: Always verify files are identical by hash before treating them as duplicates
type: feedback
originSessionId: 64453b73-bd74-4371-bfea-6f3a3ad15921
---
Never assume files with similar names, "(1)"/"(2)" suffixes, or identical sizes are actually identical.

**Why:** Superficially similar filenames can hide meaningful differences. Data loss from incorrect deduplication is irreversible.

**How to apply:** Always verify with `md5` or `shasum` before deleting any suspected duplicate. This applies to any file operation involving potential duplicates, regardless of how obvious the duplication looks.
