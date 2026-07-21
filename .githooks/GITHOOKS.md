---
title: "GITHOOKS"
updated: 2026-07-20
status: draft
authority: LOGAN
related:
  - GITHOOKS
  - imported_software
  - runtime
tags:
  - tooling/git/hooks
  - runtime/git
---

# GITHOOKS

`.githooks/` stores repository hook files and hook-adjacent notes.

This note is descriptive only. It does not declare coordination state, office,
persona status, or operational status.

To determine which hook directory Git will use in a checkout, inspect local Git
configuration:

```sh
git config --local --get core.hooksPath
```

Do not infer durable governance from this note. Read the hook files and invoked
guard scripts for implementation details.
