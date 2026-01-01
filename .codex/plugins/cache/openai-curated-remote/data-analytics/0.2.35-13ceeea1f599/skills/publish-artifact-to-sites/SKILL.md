---
name: publish-artifact-to-sites
description: "Publish an already-built Data app through Sites. Use automatically for durable reports in positively identified Work Mode when the full Sites lifecycle is callable, or when a focused skill's publication policy and user authorization permit it."
---

# Publish Data App To Sites

Publish the exact verified app selected by the focused workflow. Read and preserve the [Data App Contract](../../shared/data-app.md). The hosted app and local `dist/index.html` must come from the same source tree, reviewed data, shared components, and build.

## Routing

- In positively identified Work Mode, use this skill automatically for a durable report when the full Sites building and hosting lifecycle is callable.
- Outside Work Mode, use it only after the user explicitly requests Sites or accepts a sharing offer.
- Development preview is not publication; never deploy merely to preview an app. Where local preview is supported, show the first working version without waiting for publication setup. Do not require an extra preview environment before an authorized publication.
- If the Sites lifecycle is unavailable or publishing fails in Work Mode, keep the verified self-contained HTML as the report and state the failed stage briefly.
- If the user explicitly requested only Sites, report an actual publication blocker instead of silently changing delivery. Unavailable hosted editing does not by itself block an authorized publication.

## Workflow

1. Confirm that `$sites-building` and `$sites-hosting` can complete project creation or reopening, version saving, deployment, and status polling. Create or reuse one Site per logical app under its authorized access and read it with `get_site`. Require exactly one non-external `access_policy.allowed_users` row with `role: "owner"` for that exact Site and use its email. Never substitute the publishing editor's email or pick the first of multiple owner rows. Owner editing is the default for authorized publication; shared and public Sites use the same email flow. Preserve existing sharing and the D1 database. If the owner row or email is missing, ambiguous, or invalid, or the user requests read-only, explicitly use `--read-only` and disclose that hosted editing is unavailable.
2. Use the Data App Contract's successful prebuilt-runtime build, or its explicitly selected source build, with the resolved absolute Codex Node executable. Rebuild after content or data changes. The helper rebuilds missing or older-runtime HTML and otherwise preserves the reviewed client; copied runtime drift needs no upgrade, confirmation, old plugin cache, or dependencies. The helper verifies the snapshot marker and rejects credential-bearing source metadata, retaining only the contract's [approved source-locator exception](../../shared/data-app.md#security-and-quality-gates); do not repeat these deterministic checks manually. Review the data's suitability for its intended audience: the HTML embeds the complete snapshot, so hiding sensitive content in the UI does not prevent disclosure. Do not publish a separately reconstructed page or require a browser QA tour.
3. Package the app, pinned prebuilt Worker factory, initial presentation, project identity, and logical `DB` binding with the publication helper as the last client/Worker-producing step. Normal packaging requires no package install or Worker compilation:

   Invoke the helper through a non-shell argument-array API, with the resolved paths, Site ID, and owner email held as data variables. Never interpolate `get_site` values into shell commands or generated script source. If those values must cross a process boundary, write only the argument values as JSON with a structured file tool in private temporary storage outside the app/Git tree, read them as JSON in the launcher, and delete that file in `finally`, including on failure. For example, in a Node execution context:

   ```js
   import { spawnSync } from "node:child_process";
   const result = spawnSync(codexNode, [
     `${dataPluginRoot}/skills/publish-artifact-to-sites/scripts/package-data-app-for-sites.mjs`,
     "--project-dir", appProject,
     "--project-id", projectId,
     "--owner-email=" + ownerEmail,
   ], { shell: false, stdio: "inherit" });
   if (result.error || result.status !== 0) throw new Error("Data app packaging failed.");
   ```

   Select exactly one owner mode: `--owner-email` or the explicit `--read-only` alternative. For an explicitly selected source build, add `--source`; this uses the source Worker wrapper and already-installed local Vite, and must never silently replace a modified, authorized Worker with the prebuilt factory. An older ID-only source Worker needs the existing scoped runtime-upgrade workflow to support email; the packaging-manifest repair below does not authorize that upgrade. Append `--presentation-file <app-project>/presentation.json` only when an initial-presentation file is provided, and keep it inside the app project. The official UI handoff may include `filterDefinitions`; the helper accepts that duplicate metadata only when it exactly matches the reviewed snapshot's filters, keeps the definitions in the unchanged snapshot, and strictly validates the remaining saved presentation. The helper removes transient local-task metadata, rejects unsafe source metadata and mismatched HTML snapshots, writes the resolved project ID and `DB` binding, validates initial presentation, and emits `dist/server/index.js` plus `dist/.openai/hosting.json`.
4. Never rebuild after packaging. Commit the exact source, save and deploy the helper-verified outputs without intervening edits through `$sites-hosting` under the Site's authorized access, and poll to a successful terminal state. Preserve the same Site and D1 database across deployments; do not reset presentation or reviewed data. Return the clean Site URL and reviewed snapshot timestamp. State that source data is a published snapshot unless the app has an explicitly supported refresh path. Claim hosted editing works only after `/api/presentation` returns `canEdit: true` in the owner's normally signed-in browser; this check is not a prerequisite for completing an authorized publication. In Codex Desktop, reopen the clean verified Site in the existing stable in-app browser tab without a task fragment. Canonical Site URLs and copied/shared Site links remain query- and fragment-free.

## Owner email

The packager normalizes the owner email with `trim().toLowerCase()` and seeds only its SHA-256. The Worker compares that hash with the Sites-authenticated `oai-authenticated-user-email` on each edit request. Other visitors remain read-only. Obtain the owner email from connected `get_site`, without saving the full response or putting raw email in source or published artifacts; no browser identity discovery or proof file is needed.

If ownership or the owner's email changes, repackage and redeploy the same Site with the current owner email, or explicitly use `--read-only` to remove editing. The deployed email seed does not update automatically.

## Scoped packaging-manifest repair

Prebuilt apps normalize supported owner/project metadata automatically; copied runtime hashes are not a prerequisite. The following repair applies only to explicitly selected `--source` builds. Older publication helpers could leave the protected hashes for `.openai/hosting.json` and `src/data-app-owner.js` stale. This also applies to a newly bound, unpublished Site where project creation already wrote the exact project ID and `d1: "DB"`, leaving only the hosting hash stale before first packaging; no prior deployment or Worker bundle is required. For a source build with **only** these mismatches, append `--source --migrate-packaging-manifest` to one packaging command with an explicit owner mode. This source-only repair requires already-installed project Vite; it never downloads dependencies or makes a legacy monolithic Worker compatible with the prebuilt path. The helper requires an existing reviewed `dist/index.html`, the exact existing `project_id`, `d1: "DB"`, valid owner-module syntax, and every unrelated protected hash to verify. It preserves the Site, DB binding, reviewed content, and all unrelated integrity entries. It rejects a migration with no applicable packaging-owned mismatch or with any unrelated mismatch.

When the reviewed client is unchanged, package the existing verified `dist/index.html` with the scoped migration and the appropriate owner mode, then run `"<codex-node>" scripts/verify-protected-runtime.mjs` from the app directory. Do not rebuild the client merely to synchronize hosting metadata; that packaging invocation can be the final package. If source changes genuinely require a new client build and stale packaging-owned entries block it, run the one-time migration **before** the Data App Contract's [build command](../../shared/data-app.md#build-and-verification), then rebuild with `--source` and run ordinary final packaging again without the migration flag, retaining `--source`. Never rebuild after final packaging. Requested custom runtime changes use the existing scoped source-authorization workflow; this flag never approves them. Never run generic manifest regeneration, manually rewrite integrity hashes, or use the maintainer-only integrity updater inside a generated app to work around a failed check.

## Invariants

- Local and hosted UI are the same compiled app.
- Query rows and source metadata remain in the shared reviewed-data contract.
- The Worker may serve and persist hosted state; it must not introduce another renderer.
- Credentials, personal identifiers, live warehouse connections, and machine-local paths never enter the browser bundle.
- Do not claim publication success until deployment reaches a successful terminal state. Claim owner editing works only after an actual owner-browser response with `canEdit: true`.

## Dashboard refresh follow-up

After successful dashboard publication, read [dashboard refresh follow-up](references/dashboard-refresh.md) and apply its refreshable-source offer and cloud scheduling workflow. This does not apply to ordinary local preview or one-time sample inputs.
