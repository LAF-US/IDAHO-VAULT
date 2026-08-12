---
authority: LOGAN
related:
  - CODACY
  - imported_software
  - runtime
---

**.codacy** — Imported software runtime persona.

Codacy CLI v2 runtime and configuration.

`codacy.yaml` here is the **local CLI's** manifest: which language runtimes and
which tool versions `.github/workflows/codacy.yml` installs and runs.

It is not the same file as the repository-root `.codacy.yaml`, which is **Codacy
Cloud's** configuration — exclusions, languages, per-engine settings, read from
the default branch by the hosted analyser. Both exist; neither substitutes for
the other, and the workflow reads the root file's `exclude_paths` so the
exclusion policy is declared in one place rather than two.
