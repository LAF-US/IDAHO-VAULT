# Data inline chart live evaluations

Dashboard reference selection has a separate [dashboard-example-prompts.json](dashboard-example-prompts.json) manifest. These cases use only explicitly fictional, self-contained supplied data and never authorize publication or live warehouse access. Run each exact `prompt` alone in a fresh task against the intended installed plugin revision, with reviewer expectations kept out of the prompt. Respect any case preconditions: a draft reference must not be promoted merely to run the automatic-selection case. Compare the same prompts against the single-example baseline and candidate. Record selection/adaptation, semantic correctness, visible delivery, and browser/visual QA separately. A handcrafted table-only build or server render proves starter flexibility, not fresh-model selection. The manifest contains no run results; use the evidence record below for actual attempts.

For an explicitly authorized local maintainer comparison, read-only baseline/candidate source bundles may replace the installed-plugin condition. Record the exact revisions and whether the runtime is held constant; this tests guidance/reference adaptation, not installed delivery. Draft usage requires the same explicit development override in both conditions. Keep expectations outside author contexts and independently review generated source and calculations. Validate any existing-project seed before the run; exclude invalid seeds and permission-blocked attempts from comparative scoring rather than treating them as model failures. Browser-blocked checks remain open; do not substitute another UI route.

[inline-chart-prompts.json](inline-chart-prompts.json) holds reusable black-box prompts and separate reviewer expectations. The suite belongs to the maintained [Data plugin](../../package.json) and its maintainers. Monorepo ownership is recorded in `chatgpt/oai-maintained-plugins/plugins/OWNERS`. It is a manual, live-service evaluation of source selection, model behavior, delivery, and visual quality; it is not a new skill, renderer, or automated warehouse test.

The existing catalog test spec (`chatgpt/oai-maintained-plugins/manage/applied_spec.py` in the monorepo) runs the [Data inline CI gate](../ci/run-inline-chart-ci.sh), including deterministic build and browser regressions through `npm test` and `npm run test:inline-chart-browser`. This manifest does not cause Buildkite to query a warehouse, launch model evaluations, create user tasks, or grant permissions. Run live cases only when an operator has explicitly authorized them and the required source access already exists.

## Run a case

1. Confirm the installed Data plugin revision and the intended Codex Desktop build. Use a fresh, projectless task for each case with unchanged default model, reasoning, permission, and sandbox settings. Record the actual defaults and source availability; do not silently enable another provider, change a setting, or reuse prior conversation context.
2. Submit only the case's exact `prompt` string. Do not include expected routes, renderer names, tool choices, assertions, or reviewer hints in the user prompt. The optional internal Kepler control intentionally names a provider; it does not replace the source-neutral baseline.
3. Observe the run through completion or a real stop condition. Never automatically answer an approval, access request, or clarification on the user's behalf. Record `blocked` or `needs_user_input` with the exact observed reason; a legitimately blocked run is not a successful chart delivery.
4. Capture the exact task ID, final response, emitted output references, approved artifact paths, source/query identifiers, reviewed row evidence, material caveats, runtime verification and reuse, and any observed package or cache activity in an access-appropriate run ledger outside the repository. Record the actual source definition, population, filters, grain, date range, timezone, units, execution metadata, and freshness separately. Compare the final chart values with those reviewed rows rather than with a remembered or hard-coded WAU value.
5. Open the actual delivered native sandbox and inspect the rendered result. Check real React/Recharts marks, readable and distinct labels for distinct displayed axis ticks, correct units and tooltips, missing-data behavior, and light/dark and wide/narrow layouts. Exercise the right-aligned source overlay, its four tabs, keyboard dismissal, and default SQL/source-URL exclusion. Save permitted screenshots or observations in the run ledger; a generated HTML file or `file://` preview alone does not prove live delivery.
6. Apply the common assertions that fit the selected surface and the case-specific expectations. For multiple inline charts, verify distinct IDs/files and one real reference per chart in the same final response. Observe whether the shipped, data-free prebuilt runtime was verified and reused without an npm install, network access, or customer dependency cache. A fresh-machine claim requires observed evidence; never clear a user's cache merely to manufacture it. Never place source rows, SQL, source URLs, or generated charts in the installed plugin or any shared cache.

The three-chart default-mode case expects a report. Its explicit-three-inline companion checks the user's output override. The supplied `[120,missing,145]` case needs no live warehouse and must remain visibly synthetic. The other cases need current, governed source evidence; unavailable access must remain an explicit limitation. Do not publish reports, disclose SQL, or share private artifacts merely to complete an evaluation.

## Evidence record

Keep one record per attempt. Populate exact IDs and references from the real run; do not infer them from a filename, invent them, or use the illustrative `null` values below as evidence. Store sensitive source rows and screenshots only in an approved location, and keep user-specific task IDs, local paths, query links, metric values, tokens, and live results out of this reusable suite. Retain `cacheObservation` for compatibility with existing ledgers; record shipped-runtime verification and reuse, the absence of customer dependency-cache writes, and any unexpected installation or package-network activity in that field.

```json
{
  "caseId": "chatgpt-wau-default",
  "attemptedAt": null,
  "taskId": null,
  "pluginRevision": null,
  "appBuild": null,
  "actualDefaultSettings": {},
  "sourceAvailability": [],
  "status": "not_run",
  "stopReason": null,
  "observedResponseMode": null,
  "finalResponseRef": null,
  "outputRefs": [],
  "approvedArtifactPaths": [],
  "sourceEvidenceRefs": [],
  "reviewedRowsRef": null,
  "materialCaveats": [],
  "cacheObservation": null,
  "sandboxEvidenceRefs": [],
  "assertionResults": [],
  "reviewer": null
}
```

Use `passed`, `failed`, `blocked`, or `needs_user_input` only after observing the corresponding result. Distinguish source-access failures, source/metric errors, routing failures, generation failures, delivery failures, and visual defects. Include the exact failed assertion and supporting evidence; do not call a run passed merely because a command exited successfully or a task produced an attachment.

To validate the reusable manifest without running live services:

```sh
python3 -m json.tool chatgpt/oai-maintained-plugins/plugins/data-analytics/tests/live-evals/inline-chart-prompts.json >/dev/null
```
