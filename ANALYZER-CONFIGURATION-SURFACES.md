---
authority: LOGAN
status: staged
scope: repository-side analyzer control surfaces
---

# Analyzer Configuration Surfaces

This registry records analyzer configuration surfaces that deliberately exist in the Vault. Their presence means that future maintainers must refine analyzer behavior through reviewed repository policy rather than assume a vendor default, add a path-specific workaround, or disable a failing check.

It does **not** classify every analyzer-facing file as configuration. In particular, the root `!.js` and `!.ts` files are controlled experimental artifacts for CodeQL and are documented separately below.

> **Smoke Detector Rule:** A finding is smoke until investigated. A confirmed defect or unsafe behavior is flame. Repair the cause; do not silence the detector.

The files below are intentionally minimal. They establish a durable, versioned place for fine-grained policy while avoiding invented rules that have not been directed by Logan.

| Control surface | Current default | Future fine-grained control |
|---|---|---|
| `abaplint-app.jsonc` | `noArtifactsOkay: true` because the Vault currently has no ABAP artifacts. | Add ABAP rule configuration only when ABAP artifacts are intentionally introduced. |
| `.github/prlint.json` | Empty valid rule object; PRLint Reloaded is present but no VAULT PR metadata rules are yet enacted. | Define only approved title, body, label, branch, reviewer, or size requirements. |
| `.hound.yml` | Empty valid configuration map; Hound retains its service defaults. | Name the language linters, style files, and ignored paths through a reviewed lint policy. |
| `.guardrails/config.yml` | Explicit GuardRails defaults: auto-detected bundles, changed-line findings, and PR comments. | Change bundles, reporting scope, or notifications only with a documented security-policy decision. |
| `.cleanthat/cleanthat.yaml` | Current syntax version only; no formatter engine is selected. | Add a language engine and any formatter configuration only when the Vault adopts that language’s formatting policy. |

## Controlled CodeQL Experiment Artifacts

The root-level `!.js` and `!.ts` files are **not configuration surfaces**. They are pre-existing controlled source artifacts, introduced to test and satisfy CodeQL JavaScript/TypeScript extraction when the repository otherwise had no analyzable source in those languages.

Both files contain a real, deliberately minimal function rather than a comment-only stub. Their Git history records the experiment: the initial stubs were added to satisfy CodeQL, then changed to real code to resolve CodeQL’s “no source code seen during build” error. The historical check record corroborates the controlled result: the JavaScript/TypeScript analysis failed at the initial stub commit and succeeded after the real-code revision. [6]

They must not be mistaken for dead configuration, excluded by a path-specific analyzer exception, or deleted solely because they are not imported by an application. They are retained as evidence-bearing controls for the analysis pipeline.

## Boundaries

These configuration surfaces are not permission to disable scanning, invent required PR metadata, or add broad ignore lists. Any future refinement must state the analyzer, the source-language or review domain, the concrete problem addressed, the expected behavior, and the validation evidence.

The registry is a staging record, not an assertion that every analyzer has a live or mandatory policy. The protected `main` branch remains the authoritative promotion surface after review and merge-queue requirements are met.

## References

[1]: https://docs.abaplint.app/abaplint-app-documentation.pdf "abaplint.app configuration"
[2]: https://github.com/maor-rozenfeld/prlint-reloaded "PRLint Reloaded configuration"
[3]: http://help.houndci.com/en/articles/2138473-hound "Hound configuration"
[4]: https://docs.guardrails.io/docs/configuration "GuardRails configuration"
[5]: https://github.com/solven-eu/cleanthat "CleanThat configuration"
[6]: https://github.com/LAF-US/IDAHO-VAULT/commit/acfc3874f54bfc4f16427d95537f2a813bc18d87 "CodeQL controlled-artifact revision"
