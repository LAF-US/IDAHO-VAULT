---
title: CODACY
updated: 2026-08-13
status: active
authority: LOGAN
authors:
  - Claude Code CLI
source: "Created at Logan's instruction on PR #885 (\"add the stub.txt and
  title: CODACY personadir anchors\"), written by session
  013ie6MP332hZgSgAiSkyPZ7. Authorship is recorded here; `authority` records
  who has final say, per VAULT-METADATA-STANDARD.md line 130. Merged 2026-08-13
  with the version that landed on main independently; that version's
  \"imported runtime persona\" gloss and dangling related targets were stripped
  per Logan's instruction on PR #885, its codacy.yaml content kept."
related:
  - .github/workflows/codacy.yml
  - The world is quiet here
---

Codacy analyzes every pull request in this repository. Its workflow is
`.github/workflows/codacy.yml`.

`codacy.yaml` here is the **local CLI's** manifest, specifying which language
runtimes and which tool versions `.github/workflows/codacy.yml` installs and
runs.

It is not the same file as the repository-root `.codacy.yaml`, which is **Codacy
Cloud's** configuration — exclusions, languages, per-engine settings, read from
the default branch by the hosted analyser. Both exist; neither substitutes for
the other, and the workflow reads the root file's `exclude_paths` so the
exclusion policy is declared in one place rather than two.

Two more facts about this folder, established 2026-08-11, so the next reader
does not have to work them out again:

- The Codacy Analysis CLI writes `generated/` here, and a `.gitignore`
  alongside it. Both appear untracked after any local run. Both are tool
  residue, not vault content — do not commit them.
- A committed Codacy config governs **local** analysis only. Per Codacy's own
  documentation, `.codacy/codacy.config.json` has no effect on Codacy Cloud
  unless it is explicitly imported (`codacy tools --import`). Cloud rule
  selection lives in the Codacy project settings, not in this folder.
