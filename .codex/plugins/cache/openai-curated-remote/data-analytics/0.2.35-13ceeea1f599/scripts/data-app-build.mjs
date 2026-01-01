import { lstat, mkdir, mkdtemp, rename, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { Script } from "node:vm";

import { compileAuthoredModules } from "./authored-module-graph.mjs";
import {
  DEFAULT_PLUGIN_ROOT,
  assertPrebuiltProject,
  loadPrebuiltCompiler,
  readPrebuiltArtifact,
} from "./data-app-runtime.mjs";
import { API_VERSION, readRegularFile, sha256 } from "./prebuilt/manifest.mjs";

const THREAD_ID = /^[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}$/iu;
const HASH = /^[a-f\d]{64}$/u;
const SNAPSHOT_ELEMENT_ID = "data-app-reviewed-snapshot";

export function localDataThreadId(environment = process.env) {
  return [environment.CODEX_SESSION_ID, environment.CODEX_THREAD_ID].find((value) => THREAD_ID.test(value ?? "")) ?? "";
}

export function escapeHtml(value) {
  return String(value).replace(
    /[&<>"']/gu,
    (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character],
  );
}

function jsonDocument(value) {
  return JSON.stringify(value)
    .replaceAll("<", "\\u003c")
    .replaceAll("\u2028", "\\u2028")
    .replaceAll("\u2029", "\\u2029");
}

export function embeddedScript(code) {
  // HTML has its own script tokenizer, even inside JS strings and tagged
  // templates. A data URL preserves unusual source bytes without eval or a
  // handwritten JavaScript rewrite. Classic scripts remain ordered and local.
  new Script(code, { filename: "data-app-embedded.js" });
  return /<(?:!--|\/?script)|[\0\r]/iu.test(code)
    ? `<script src="data:text/javascript;charset=utf-8;base64,${Buffer.from(code).toString("base64")}"></script>`
    : `<script>${code}</script>`;
}

export function embeddedStyle(css) {
  return /<\/style|[\0\r]/iu.test(css)
    ? `<link rel="stylesheet" href="data:text/css;charset=utf-8;base64,${Buffer.from(css).toString("base64")}">`
    : `<style>${css}</style>`;
}

export function assembleDataAppHtml({
  appCode,
  protectedStyles,
  printStyles,
  authored,
  snapshotBytes,
  runtimeSha256,
  localThreadId = "",
}) {
  if (!HASH.test(runtimeSha256 ?? "")) throw new Error("The Data app requires a verified runtime hash.");
  if (localThreadId && !THREAD_ID.test(localThreadId)) throw new Error("Invalid local Data app task identifier.");
  let snapshot;
  try {
    snapshot = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(snapshotBytes));
  } catch (error) {
    throw new Error("The reviewed Data app snapshot must be valid UTF-8 JSON.", { cause: error });
  }
  if (
    !snapshot ||
    typeof snapshot !== "object" ||
    Array.isArray(snapshot) ||
    !snapshot.queries ||
    typeof snapshot.queries !== "object" ||
    Array.isArray(snapshot.queries)
  ) {
    throw new Error("The Data app must contain a reviewed query snapshot.");
  }
  const snapshotSha256 = sha256(snapshotBytes);
  const bootstrap =
    `(() => {\n"use strict";\n` +
    `const runtime = globalThis.CodexDataAppRuntime;\n` +
    `if (runtime?.apiVersion !== ${API_VERSION}) throw new Error("Incompatible Data app runtime.");\n` +
    `const reviewedSnapshot = JSON.parse(document.getElementById(${JSON.stringify(
      SNAPSHOT_ELEMENT_ID,
    )}).textContent);\n` +
    `const content = ${authored.factorySource}(runtime, reviewedSnapshot);\n` +
    `runtime.mount({reviewedSnapshot, DashboardContent: content.DashboardContent, ReportContent: content.ReportContent});\n` +
    `})();`;
  // Match the source entry: conventional sheets precede print, while component
  // stylesheet imports follow it and may intentionally override print rules.
  const styles = [authored.themeCss, protectedStyles, authored.conventionalCss, printStyles, authored.importedCss].join(
    "\n",
  );
  const html =
    `<!doctype html>\n<html lang="en">\n<head>\n` +
    `<meta charset="utf-8">\n` +
    `<meta name="viewport" content="width=device-width, initial-scale=1">\n` +
    `<meta name="color-scheme" content="light dark">\n` +
    `<meta name="data-app-snapshot-sha256" content="${snapshotSha256}">\n` +
    `<meta name="data-app-runtime-sha256" content="${runtimeSha256}">\n` +
    (localThreadId ? `<meta name="data-app-local-thread" content="${localThreadId}">\n` : "") +
    `<title>${escapeHtml(snapshot.title || "Data app")}</title>\n` +
    `<link rel="icon" href="data:,">\n${embeddedStyle(styles)}\n</head>\n<body>\n` +
    `<div id="root"></div>\n` +
    `<script type="application/json" id="${SNAPSHOT_ELEMENT_ID}">${jsonDocument(snapshot)}</script>\n` +
    `${embeddedScript(appCode)}\n${embeddedScript(bootstrap)}\n</body>\n</html>\n`;
  return { html, snapshotSha256 };
}

async function statOrNull(path) {
  try {
    return await lstat(path);
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

async function publishHtml(projectRoot, html, onProgress) {
  const destination = join(projectRoot, "dist");
  const existing = await statOrNull(destination);
  if (existing && (!existing.isDirectory() || existing.isSymbolicLink())) {
    throw new Error("Data app dist must be a regular directory inside the project.");
  }
  const scratch = await mkdtemp(join(projectRoot, ".data-app-build-"));
  const candidate = join(scratch, "next");
  const previous = join(scratch, "previous");
  let movedPrevious = false;
  let published = false;
  let preservePrevious = false;
  try {
    await mkdir(candidate);
    await writeFile(join(candidate, "index.html"), html, { flag: "wx" });
    if (existing) {
      await rename(destination, previous);
      movedPrevious = true;
      preservePrevious = true;
    }
    try {
      await rename(candidate, destination);
      published = true;
      preservePrevious = false;
    } catch (error) {
      if (movedPrevious) {
        // Do not overwrite another build that won the destination in between.
        try {
          if (!(await statOrNull(destination))) {
            await rename(previous, destination);
            movedPrevious = false;
            preservePrevious = false;
          }
        } catch {
          // The only old copy stays detached if probing or restoring fails.
        }
      }
      if (preservePrevious) {
        throw new Error(`Could not publish the Data app. The previous output is preserved at ${previous}.`, {
          cause: error,
        });
      }
      throw error;
    }
  } finally {
    if (!preservePrevious) {
      try {
        await rm(scratch, { recursive: true, force: true });
      } catch (error) {
        if (!published) throw error;
        onProgress?.(`Built the Data app; the old output could not be removed from ${scratch}: ${error.message}`);
      }
    }
  }
  return join(destination, "index.html");
}

function preparedResult({ projectRoot, pluginRoot, manifest }) {
  return {
    projectRoot,
    prebuilt: true,
    apiVersion: API_VERSION,
    runtimeSha256: manifest.artifacts.app.sha256,
    compilerSha256: manifest.artifacts.compiler.sha256,
    documentation: {
      entryPoint: join(pluginRoot, "templates/data-app/base/docs/components/README.md"),
      source: "installed-plugin",
      apiVersion: manifest.apiVersion,
      runtimeSha256: manifest.artifacts.app.sha256,
    },
  };
}

export async function preparePrebuiltDataApp(options = {}) {
  const state = await assertPrebuiltProject(options);
  return preparedResult(state);
}

export async function buildPrebuiltDataApp({
  projectDir,
  pluginRoot = DEFAULT_PLUGIN_ROOT,
  environment = process.env,
  onProgress,
} = {}) {
  const state = await assertPrebuiltProject({ projectDir, pluginRoot, onProgress });
  const { projectRoot, manifest } = state;
  const read = (name) => readPrebuiltArtifact(name, { pluginRoot: state.pluginRoot, manifest });
  const [compiler, app, styles, print, snapshotBytes] = await Promise.all([
    loadPrebuiltCompiler({ pluginRoot: state.pluginRoot, manifest }),
    read("app"),
    read("styles"),
    read("print"),
    readRegularFile(projectRoot, "src/data.json"),
  ]);
  const authored = await compileAuthoredModules({
    projectRoot,
    compiler,
    runtimeModuleExports: manifest.artifacts.app.metadata.moduleExports,
  });
  for (const warning of authored.warnings) onProgress?.(`${warning.code}: ${warning.message}`);
  const assembled = assembleDataAppHtml({
    appCode: app.code,
    protectedStyles: styles.code,
    printStyles: print.code,
    authored,
    snapshotBytes,
    runtimeSha256: app.sha256,
    localThreadId: localDataThreadId(environment),
  });
  if (sha256(await readRegularFile(projectRoot, "src/data.json")) !== assembled.snapshotSha256) {
    throw new Error("The reviewed snapshot changed during the Data app build. Retry with a stable snapshot.");
  }
  const htmlPath = await publishHtml(projectRoot, assembled.html, onProgress);
  return {
    ...preparedResult(state),
    htmlPath,
    htmlSha256: sha256(assembled.html),
    snapshotSha256: assembled.snapshotSha256,
    moduleCount: authored.moduleCount,
    assetCount: authored.assetCount,
  };
}
