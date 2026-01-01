import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { lstatSync, readFileSync, readdirSync, realpathSync, writeFileSync } from "node:fs";
import { isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { digestProtectedFile } from "../../templates/data-app/base/scripts/protected-file-digest.mjs";

const digest = (contents) => createHash("sha256").update(contents).digest("hex");

function regularFile(path, description, { allowEmpty = false } = {}) {
  const metadata = lstatSync(path, { throwIfNoEntry: false });
  assert.ok(metadata?.isFile() && (allowEmpty || metadata.size > 0), `Missing or invalid ${description}: ${path}`);
  return metadata;
}

function markerHash(html, name) {
  const head = /<head(?:\s[^>]*)?>([\s\S]*?)<\/head\s*>/iu.exec(html)?.[1] ?? "";
  const markers = [...head.matchAll(new RegExp(`<meta\\b[^>]*\\bname\\s*=\\s*(["'])${name}\\1[^>]*>`, "giu"))];
  const hash = markers.length === 1 ? /\bcontent\s*=\s*(["'])([a-f\d]{64})\1/u.exec(markers[0][0])?.[2] : null;
  assert.ok(hash, `The Data HTML must contain exactly one valid ${name} marker`);
  return hash;
}

export function readBuildIntegrity(projectRoot) {
  regularFile(join(projectRoot, "dist/index.html"), "Data client build");
  regularFile(join(projectRoot, "src/data.json"), "reviewed Data snapshot");
  const html = readFileSync(join(projectRoot, "dist/index.html"), "utf8");
  const snapshotSha256 = digest(readFileSync(join(projectRoot, "src/data.json")));
  assert.equal(
    markerHash(html, "data-app-snapshot-sha256"),
    snapshotSha256,
    "The Data HTML must match the exact reviewed snapshot bytes",
  );
  return {
    htmlSha256: digest(html),
    snapshotSha256,
    runtimeSha256: markerHash(html, "data-app-runtime-sha256"),
  };
}

function sourceState(projectRoot) {
  const manifest = JSON.parse(readFileSync(join(projectRoot, "protected-runtime.json"), "utf8"));
  assert.equal(manifest.version, 1, "Unexpected protected runtime format");
  assert.ok(manifest.files && typeof manifest.files === "object" && !Array.isArray(manifest.files));
  const names = new Set([
    "package.json",
    "package-lock.json",
    "protected-runtime.json",
    "src/data.json",
    "src/theme.css",
    ...Object.keys(manifest.files),
  ]);
  function visit(name) {
    for (const entry of readdirSync(join(projectRoot, name), { withFileTypes: true })) {
      const child = `${name}/${entry.name}`;
      assert.ok(!entry.isSymbolicLink(), `The offline source must not contain symlinks: ${child}`);
      if (entry.isDirectory()) visit(child);
      else {
        assert.ok(entry.isFile(), `The offline source must contain regular files: ${child}`);
        names.add(child);
      }
    }
  }
  visit("src/content");
  return Object.fromEntries(
    [...names].sort().map((name) => {
      assert.ok(
        !isAbsolute(name) &&
          !name.includes("\\") &&
          !name.split("/").some((part) => !part || part === "." || part === ".."),
        `Invalid protected source path: ${name}`,
      );
      regularFile(join(projectRoot, name), `Data source ${name}`, { allowEmpty: true });
      return [name, digestProtectedFile(name, readFileSync(join(projectRoot, name)))];
    }),
  );
}

async function verifyWorker(projectRoot) {
  const workerPath = join(projectRoot, "dist/server/index.js");
  regularFile(workerPath, "Sites Worker build");
  regularFile(join(projectRoot, "dist/.openai/hosting.json"), "Sites hosting metadata");
  const hosting = JSON.parse(readFileSync(join(projectRoot, "dist/.openai/hosting.json"), "utf8"));
  assert.equal(hosting.d1, "DB", "The offline Sites package must preserve its database binding");
  assert.ok(
    typeof hosting.project_id === "string" && hosting.project_id.trim(),
    "The Sites package must identify its project",
  );
  // Loading from a data URL also proves the Worker has no filesystem-relative
  // chunks or package imports that happened to be installed by the CI worker.
  const workerUrl = `data:text/javascript;base64,${readFileSync(workerPath).toString("base64")}`;
  const worker = (await import(workerUrl)).default;
  assert.equal(typeof worker?.fetch, "function", "The offline Sites package must export a real Worker");
  const response = await worker.fetch(new Request("https://offline-data.example/"), {});
  assert.equal(response.status, 200);
  assert.equal(
    await response.text(),
    readFileSync(join(projectRoot, "dist/index.html"), "utf8").replace(
      "<head>", `<head><meta name="data-app-sites-project" content="${hosting.project_id}">`,
    ),
    "The offline Sites Worker must serve the exact reviewed HTML with its Sites project marker",
  );
}

async function main() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      "project-dir": { type: "string" },
      "state-file": { type: "string" },
      "require-worker": { type: "boolean", default: false },
    },
    strict: true,
  });
  const [command] = positionals;
  assert.ok(
    positionals.length === 1 &&
      ["capture", "verify"].includes(command) &&
      values["project-dir"] &&
      values["state-file"],
    "Usage: verify-offline-build.mjs <capture|verify> --project-dir <app> --state-file <state.json> [--require-worker]",
  );
  const projectRoot = realpathSync(values["project-dir"]);
  const statePath = resolve(values["state-file"]);
  assert.equal(
    lstatSync(join(projectRoot, "node_modules"), { throwIfNoEntry: false }),
    undefined,
    "The prebuilt Data build must not create project node_modules",
  );
  const built = readBuildIntegrity(projectRoot);
  const sources = sourceState(projectRoot);
  if (values["require-worker"]) await verifyWorker(projectRoot);
  if (command === "capture") {
    assert.equal(values["require-worker"], false, "Capture the baseline before Sites packaging");
    writeFileSync(statePath, `${JSON.stringify({ format: 2, projectRoot, built, sources }, null, 2)}\n`, {
      flag: "wx",
    });
  } else {
    const state = JSON.parse(readFileSync(statePath, "utf8"));
    assert.equal(state.format, 2, "Unexpected offline build checkpoint format");
    assert.equal(state.projectRoot, projectRoot, "Offline build checkpoint belongs to another app");
    assert.deepEqual(sources, state.sources, "The reviewed Data app source was modified by an offline build");
    assert.equal(built.snapshotSha256, state.built.snapshotSha256, "The reviewed Data snapshot changed");
    assert.equal(built.runtimeSha256, state.built.runtimeSha256, "The prebuilt browser runtime changed between builds");
    if (!values["require-worker"]) {
      assert.equal(
        built.htmlSha256,
        state.built.htmlSha256,
        "Repeated prebuilt builds must preserve the same HTML bytes",
      );
    }
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
