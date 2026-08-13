# Codacy Research and PR #971 Check Notes

## Verified Codacy behavior

Codacy Cloud does not initialize Git submodules by default; therefore, the existing `DND-SRD-5.2.1-UPSTREAM` Gitlink is outside the parent repository’s normal hosted static-analysis input. This is the relevant module-native behavior. Source: <https://docs.codacy.com/repositories-configure/using-submodules/>.

The normal tracked `DND-SRD-5.2.1/` tree was scanned and generated 442 Markdown findings. It was removed in commit `a460d4185`, while `.gitmodules` continues to pin `DND-SRD-5.2.1-UPSTREAM` to upstream commit `1b4b99dcb786cdd1a2fb26f8acec1551191f1ca4`. The upstream module’s `LICENSE` and `README.md` retain CC BY 4.0 and Wizards of the Coast attribution.

Codacy’s public configuration documentation distinguishes root-level and per-engine path exclusions, per-engine `base_sub_dir`, language controls, tool configuration, and native tool configuration. It does not document a persistent multi-module registry. Its published CLI parser represents `base_sub_dir` as one optional string per engine and recognizes `exclude_paths` per engine. Sources: <https://docs.codacy.com/repositories-configure/codacy-configuration-file/>, <https://github.com/codacy/codacy-analysis-cli/blob/62e6b58c33adc6c4a7893ee510be53b59db6e8dd/core/src/main/scala/com/codacy/analysis/core/configuration/CodacyConfigurationFile.scala>, and <https://github.com/codacy/codacy-analysis-cli/blob/62e6b58c33adc6c4a7893ee510be53b59db6e8dd/core/src/main/scala/com/codacy/analysis/core/tools/Tool.scala>.

Codacy Segments group whole repositories; the API’s “components/projects” language is for reporting by directory; Coverage Reporter’s monorepo modules concern coverage uploads. None changes hosted static-analysis scope. Sources: <https://docs.codacy.com/organizations/segments/>, <https://docs.codacy.com/codacy-api/examples/obtaining-code-quality-metrics-for-files/>, and <https://docs.codacy.com/coverage-reporter/>.

The published Codacy markdownlint engine accepts files selected by Codacy’s runner and uses native markdownlint configuration only as rule configuration, not as a scan-module boundary. Sources: <https://github.com/codacy/codacy-markdownlint/blob/91911ce/src/configCreator.ts> and <https://github.com/codacy/codacy-markdownlint/blob/91911ce/src/engineImpl.ts>.

## Current PR state after the submodule correction

Codacy’s PR #971 result changed from 442 issues (all SRD reference material) to 30 non-SRD Markdown issues. No SRD paths remain in the current Codacy issue list. The remaining documents are `!/FIRST-CONGRESS-AND-EXPANDED-FRAMEWORKS.md` (12), `!/VAULT-RESEARCH-SUMMARY.md` (11), `5W-ANSWERS.md` (1), `A&I-RD-5WIZARDS-COMPOSED-ARCHITECTURE-2026-08-13.md` (3), and `MUD-MUSH-ARCHITECTURE.md` (3). Findings are Markdown structural rules: missing blank lines around lists, incorrect ordered-list spacing, multiple H1 headings, and heading spacing. The live PR view is <https://app.codacy.com/gh/LAF-US/IDAHO-VAULT/pull-requests/971/issues>.
