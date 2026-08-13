---
title: Codacy Module-Exclusion Research
status: working-note
updated: 2026-08-13
scope: PR #971
---

# Codacy Module-Exclusion Research

## Verified distinction

The repository-local `.codacy/codacy.yaml` is the **Codacy Analysis CLI v2 runtime manifest**. It declares runtime/tool versions used by the local workflow and is not Codacy Cloud's repository-analysis configuration.

The hosted Codacy configuration file is a root `.codacy.yml` or `.codacy.yaml`. Codacy documents the hosted file as supporting repository analysis scope through `include_paths` and `exclude_paths`, language controls, and tool-specific configuration. The reference examined does **not** document a `modules` declaration or a module-level exclusion primitive in that file.

Codacy’s submodule documentation concerns whether Codacy clones Git submodules and how it accesses them. It does not describe treating a vendored directory or a submodule as an independently configurable analysis module.

## Consequence for PR #971

The prior Markdown-wide language change was incorrect and has been reverted in commit `501bdccde`. Markdown analysis must remain enabled. The remaining task is to identify the repository’s existing definition of the intended Codacy module boundary, rather than substituting a path exclusion or tool disablement.

## Sources

1. https://docs.codacy.com/repositories-configure/codacy-configuration-file/
2. https://docs.codacy.com/repositories-configure/using-submodules/

## Access finding

The Codacy pull-request page is publicly reachable but exposes only a login screen in the available browser session. Its module/component settings therefore cannot be inspected or changed through the current session. GitHub identifies the blocking check as the hosted `codacy-production` integration, not the repository’s local Codacy CLI v2 workflow.

## Live PR analysis (2026-08-13)

Codacy’s live PR #971 page confirms **442 new issues**. The SRD directory is presented as a file group in the results, and the first issues are standard Markdown findings such as `Element: td`, `Element: table`, and `Element: th`. The same page also identifies a small number of non-SRD Markdown findings, so preserving ordinary Markdown analysis remains necessary.

The available browser session can read the public pull-request analysis but displays **Login** and **Sign up** in the application header. It does not provide authenticated repository settings controls. The local filesystem inspection found a root `.codacy.yaml` containing the current path-based policy for Obsidian plugin executable/style artifacts and a separate `codacy.yml` local workflow; neither defines a Codacy module or component boundary.

## Settings-route check

The publicly readable PR view links to `/gh/LAF-US/IDAHO-VAULT/settings/gates`, but loading that repository settings route leaves only the application shell and the visible Login control. The needed repository configuration cannot be inspected unauthenticated; no setting was changed.

## Local-checkout evidence

The connected desktop contains a distinct local checkout on branch `logan/obsidian`; `origin/manus/self-testing` is available only as a remote-tracking ref there. The local working tree is materially dirty and contains unrelated personal and generated material, so it has not been modified.

The local root’s `.codacy.yaml` has an `exclude_paths` policy only, covering Obsidian plugin executable/style artifacts. The separate `codacy.yml` files are SARIF workflow copies and contain no module, component, workspace, or analysis-scope declaration. The local `module-map.md` is a Zoom SDK module note and is unrelated to Codacy or the vault’s SRD import. The remote-tracking `origin/manus/self-testing` tree contains no root Codacy configuration file or module-named configuration file.

## Official Codacy scope capabilities

Codacy documents one **per-engine analysis-root** control: `engines.<engine>.base_sub_dir`. It starts that engine’s run from one specified subdirectory without setting a repository-global ignore. For example, `engines.rubocop.base_sub_dir: "test/baseDir"` scopes RuboCop to that root.

Codacy’s public Analysis CLI parser represents `base_sub_dir` as one optional string in each engine configuration. The CLI’s execution logic replaces that engine’s source directory with the configured subdirectory before invoking the engine and then remaps result paths back to the repository. This is a single analysis root per engine, not a declarative collection of repository modules or a multi-root module registry.

The documented configuration surface also has global `exclude_paths`, per-engine `exclude_paths`, `include_paths`, language controls, and tool-specific configuration. Codacy’s API documentation uses “component or project” only for **reporting** subsets of monorepos by directory query; it does not document a persistent component/module object that changes scan scope.

Sources: https://docs.codacy.com/repositories-configure/codacy-configuration-file/ ; https://docs.codacy.com/codacy-api/examples/obtaining-code-quality-metrics-for-files/ ; https://github.com/codacy/codacy-analysis-cli/blob/62e6b58c33adc6c4a7893ee510be53b59db6e8dd/core/src/main/scala/com/codacy/analysis/core/configuration/CodacyConfigurationFile.scala ; https://github.com/codacy/codacy-analysis-cli/blob/62e6b58c33adc6c4a7893ee510be53b59db6e8dd/core/src/main/scala/com/codacy/analysis/core/tools/Tool.scala

## Related Codacy features that are not repository modules

Codacy **Segments** group whole repositories using provider metadata (GitHub Custom Properties or Bitbucket Projects) for repository organization and filtering. They do not create sub-repository modules or alter one repository’s analysis scope.

Codacy also supports activating a native configuration file for a single tool through the repository’s Code patterns UI. Once activated, the file is evaluated from the analyzed branch and controls that tool’s patterns. This is a per-tool configuration integration, not a Codacy module registry. For markdownlint, a native configuration could affect its own ignore behavior, but its activation requires repository settings access.

Source: https://docs.codacy.com/organizations/segments/ ; https://docs.codacy.com/repositories-configure/configuring-code-patterns/

## Markdownlint engine verification

Codacy’s public markdownlint engine first receives the list of files from Codacy’s runner. If no file list is supplied, it falls back to globbing `**/*.md`. Its configuration loader reads only `.markdownlint.json`, `.markdownlint.yaml`, `.markdownlint.yml`, or `.markdownlint.jsonc` and passes the parsed content to markdownlint as a **rule configuration**.

Therefore, a `.markdownlint.yml` loaded by this Codacy engine is not a reliable module- or scan-scope mechanism: the engine’s selected file list comes from Codacy, and native rule configuration does not define Codacy’s analysis module boundary. The supported Codacy-level per-engine boundary remains `engines.markdownlint.base_sub_dir`.

Source: https://github.com/codacy/codacy-markdownlint/blob/91911ce/src/configCreator.ts ; https://github.com/codacy/codacy-markdownlint/blob/91911ce/src/engineImpl.ts

## Git submodules and coverage modules

Codacy clones repositories without Git submodules by default; submodule checkout is a repository-level opt-in that Codacy asks customers to request. This affects only actual Git submodules. It does not classify or omit a vendored directory from the parent repository scan. Consequently, the existing `DND-SRD-5.2.1-UPSTREAM` submodule is normally absent from Codacy’s scan, while the vendored `DND-SRD-5.2.1` directory remains normal parent-repository content.

Codacy documentation also refers to “modules in a monorepo setup” in its coverage-reporting material, but that capability concerns uploading and aggregating coverage data. It is not a static-analysis scope mechanism for the hosted `Codacy Static Code Analysis` check.

Sources: https://docs.codacy.com/repositories-configure/using-submodules/ ; https://docs.codacy.com/coverage-reporter/

## Codacy engine-scoped exclusion (the relevant module boundary)

Codacy’s configuration parser supports `engines.<engine>.exclude_paths` in addition to the root-level `exclude_paths`. For the supported engine name `markdownlint`, the configuration shape is:

```yaml
---
engines:
  markdownlint:
    exclude_paths:
      - "DND-SRD-5.2.1/**"
```

This leaves the `markdownlint` engine enabled and continues its analysis of every Markdown file outside the declared reference module. Unlike root `exclude_paths`, the exclusion applies only to the Markdownlint engine; other Codacy engines retain their normal scan scope. Unlike language/tool disablement, it does not turn off Markdown analysis.

The scope pattern is necessarily expressed as the module’s repository path because Codacy’s engine configuration schema defines exclusions as glob sets. Codacy does not expose a separate persistent module object or module ID in its API. The Codacy API tool-configuration schema contains only `enabled`, `useConfigurationFile`, and `patterns`, confirming that engine-scoped path configuration belongs in `.codacy.yaml` rather than its settings API.

Sources: https://docs.codacy.com/repositories-configure/codacy-configuration-file/ ; https://github.com/codacy/codacy-analysis-cli/blob/62e6b58c33adc6c4a7893ee510be53b59db6e8dd/core/src/main/scala/com/codacy/analysis/core/configuration/CodacyConfigurationFile.scala ; https://api.codacy.com/api/api-docs

## Snapshot-preserving module-native topology (proposal only)

The current layout has two representations of the same SRD content:

| Path | Git representation | Codacy default behavior |
|---|---|---|
| `DND-SRD-5.2.1/` | Normal tracked tree with 18 files, including `SOURCE.md` | Scanned as parent-repository content; responsible for the 442 findings. |
| `DND-SRD-5.2.1-UPSTREAM/` | Gitlink to `downfallx/dnd-5e-srd-markdown` at `1b4b99d…` | Not cloned/scanned by default because it is a Git submodule. |

To make the snapshot itself a genuine scan-excluded module while retaining the snapshot and its provenance, the structural design is to create a dedicated **LAF-US-owned snapshot repository** containing the exact 18-file corpus, `SOURCE.md`, and the preserved license; then replace the normal `DND-SRD-5.2.1/` tree with a Git submodule pointing at a pinned snapshot-repository commit. The existing external-upstream submodule remains a distinct provenance/update reference.

This design moves the exclusion from a Codacy rule to Git module topology. It relies on Codacy’s default behavior of not initializing Git submodules. An LAF-US snapshot repository also satisfies Codacy’s GitHub-specific same-organization prerequisite if submodule support is later enabled. Creating that remote repository and changing the tracked representation require Architect approval; no changes have been made.
