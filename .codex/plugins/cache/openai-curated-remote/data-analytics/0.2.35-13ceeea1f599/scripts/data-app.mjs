#!/usr/bin/env node
import { join } from "node:path";
import { parseArgs } from "node:util";

import { buildPrebuiltDataApp, preparePrebuiltDataApp } from "./data-app-build.mjs";
import { assertSupportedDataNode, localSourceVite, runDataNode } from "./data-app-runtime.mjs";
import { readRegularFile, sha256 } from "./prebuilt/manifest.mjs";

function usage() {
  console.log(
    "Usage: <codex-node> data-app.mjs <prepare|build> --project-dir <copied-data-app> [--offline] [--source]",
  );
}

async function sourceBuild(projectDir, build, onProgress) {
  const { projectRoot, vitePath } = await localSourceVite(projectDir);
  runDataNode([join(projectRoot, "scripts/verify-protected-runtime.mjs")], { cwd: projectRoot, onProgress });
  let documentation = null;
  for (const entry of ["docs/components/README.md", "src/content/COMPONENTS.md"]) {
    try {
      await readRegularFile(projectRoot, entry);
    } catch (error) {
      if (error.code === "ENOENT") continue;
      throw error;
    }
    documentation = {
      entryPoint: join(projectRoot, entry),
      source: "project-source",
      protectedRuntimeSha256: sha256(await readRegularFile(projectRoot, "protected-runtime.json")),
    };
    break;
  }
  if (!build) return { projectRoot, prebuilt: false, source: true, vitePath, documentation };
  runDataNode([vitePath, "build"], { cwd: projectRoot, onProgress });
  const html = await readRegularFile(projectRoot, "dist/index.html");
  return {
    projectRoot,
    prebuilt: false,
    source: true,
    documentation,
    htmlPath: join(projectRoot, "dist/index.html"),
    htmlSha256: sha256(html),
    snapshotSha256: sha256(await readRegularFile(projectRoot, "src/data.json")),
  };
}

try {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      "project-dir": { type: "string" },
      offline: { type: "boolean" },
      source: { type: "boolean", default: false },
      help: { type: "boolean", short: "h" },
    },
    strict: true,
  });
  if (values.help) usage();
  else {
    assertSupportedDataNode();
    const [command] = positionals;
    if (positionals.length !== 1 || !["prepare", "build"].includes(command) || !values["project-dir"]?.trim()) {
      usage();
      throw new Error("Specify a copied Data app directory and either prepare or build.");
    }
    const onProgress = (message) => console.error(message);
    // --offline remains accepted for existing callers. Neither path installs or
    // downloads anything, and source compilation is always an explicit choice.
    const result = values.source
      ? await sourceBuild(values["project-dir"], command === "build", onProgress)
      : await (command === "build" ? buildPrebuiltDataApp : preparePrebuiltDataApp)({
          projectDir: values["project-dir"],
          onProgress,
        });
    console.log(JSON.stringify(result));
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
