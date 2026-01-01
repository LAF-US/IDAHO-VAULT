import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { digestProtectedFile } from "../templates/data-app/base/scripts/protected-file-digest.mjs";

const helper = fileURLToPath(
  new URL("../skills/publish-artifact-to-sites/scripts/package-data-app-for-sites.mjs", import.meta.url),
);
const fixturePresentationSource = [
  "const allowedPresentationFields = new Set([",
  '  "theme", "appearance", "title", "description", "hiddenBlocks", "componentTitles", "textEdits",',
  '  "chartOverrides", "filters", "assumptions", "notes", "refreshSchedule", "tabs", "blockLayouts", "verification",',
  "]);",
  "export function validatePresentation(value) {",
  '  if (value.invalid) throw new Error("Presentation is invalid.");',
  "  const unexpected = Object.keys(value).filter((key) => !allowedPresentationFields.has(key));",
  '  if (unexpected.length) throw new Error(`Unsupported presentation fields: ${unexpected.join(", ")}.`);',
  "  return value;",
  "}",
].join("\n");
const fixtureOwnerSource = (emailHash = "") => `export const dataAppOwnerEmailSha256 = "${emailHash}";\n`;
const fixtureWorkerSource = [
  'import dataAppHtml from "../dist/index.html?raw";',
  'import seedSnapshot from "./data.json";',
  'import { dataAppOwnerEmailSha256 } from "./data-app-owner.js";',
  'import { createDataAppWorker } from "./data-app-worker.js";',
  "export default createDataAppWorker({",
  "  html: dataAppHtml, seedSnapshot,",
  "  ownerEmailSha256: dataAppOwnerEmailSha256,",
  "});",
].join("\n");
const fixtureRuntimeSource = [
  fixturePresentationSource,
  "export function createDataAppWorker(configuration) {",
  "  validatePresentation(configuration.initialPresentation);",
  "  return { configuration, fetch() { return new Response(configuration.html); } };",
  "}",
].join("\n");
const digest = (value) => createHash("sha256").update(value).digest("hex");
const fixtureAppRuntimeHash = "a".repeat(64);
const digestHelperUrl = new URL("../templates/data-app/base/scripts/protected-file-digest.mjs", import.meta.url);

function reviewedHtml(snapshot) {
  return (
    `<!doctype html><head><meta name="data-app-snapshot-sha256" content="${digest(snapshot)}">` +
    `<meta name="data-app-runtime-sha256" content="${fixtureAppRuntimeHash}"></head>` +
    "<main>Reviewed Data app</main>"
  );
}

function writeSnapshot({ project }, snapshot) {
  const content = typeof snapshot === "string" || Buffer.isBuffer(snapshot) ? snapshot : JSON.stringify(snapshot);
  writeFileSync(join(project, "src/data.json"), content);
  writeFileSync(join(project, "dist/index.html"), reviewedHtml(content));
}

const legacyFixtureProtectedPaths = [
  ".openai/hosting.json",
  "package.json",
  "scripts/verify-protected-runtime.mjs",
  "src/data-app-owner.js",
  "src/worker.js",
];
const fixtureProtectedPaths = [
  ...legacyFixtureProtectedPaths,
  "scripts/protected-file-digest.mjs",
  "src/presentation-state.js",
  "src/data-app-worker.js",
];

function updateFixtureProtectedManifest({ project }, paths) {
  const manifestPath = join(project, "protected-runtime.json");
  const normalized = existsSync(join(project, "scripts/protected-file-digest.mjs"));
  const manifest = existsSync(manifestPath)
    ? JSON.parse(readFileSync(manifestPath, "utf8"))
    : { version: 1, editablePaths: ["src/content/", "src/theme.css", "src/data.json"], files: {} };
  for (const path of paths ?? (normalized ? fixtureProtectedPaths : legacyFixtureProtectedPaths)) {
    const bytes = readFileSync(join(project, path));
    manifest.files[path] = normalized ? digestProtectedFile(path, bytes) : digest(bytes);
  }
  writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
}

function verifyFixtureProtectedManifest({ project }) {
  execFileSync(process.execPath, [join(project, "scripts/verify-protected-runtime.mjs")], {
    cwd: project,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
}

function fixtureRuntime({
  body = "",
  artifactBody = "",
  runtimeSource = fixtureRuntimeSource,
} = {}) {
  const plugin = mkdtempSync(join(tmpdir(), "data-app-sites-runtime-"));
  const helperPath = join(plugin, "skills/publish-artifact-to-sites/scripts/package-data-app-for-sites.mjs");
  mkdirSync(dirname(helperPath), { recursive: true });
  copyFileSync(helper, helperPath);
  mkdirSync(join(plugin, "scripts"));
  // Real missing/outdated-client builds are covered by the build integration tests.
  writeFileSync(
    join(plugin, "scripts/data-app-build.mjs"),
    'export async function buildPrebuiltDataApp() { throw new Error("Unexpected fixture client rebuild."); }\n',
  );
  copyFileSync(new URL("../scripts/data-url.mjs", import.meta.url), join(plugin, "scripts/data-url.mjs"));
  mkdirSync(join(plugin, "templates/data-app/base/scripts"), { recursive: true });
  copyFileSync(digestHelperUrl, join(plugin, "templates/data-app/base/scripts/protected-file-digest.mjs"));
  mkdirSync(join(plugin, "templates/data-app/base/src"));
  copyFileSync(
    new URL("../templates/data-app/base/src/owner-email.js", import.meta.url),
    join(plugin, "templates/data-app/base/src/owner-email.js"),
  );
  mkdirSync(join(plugin, "assets"));
  writeFileSync(join(plugin, "assets/worker.mjs"), runtimeSource);
  writeFileSync(
    join(plugin, "scripts/data-app-runtime.mjs"),
    [
      'import { createHash } from "node:crypto";',
      'import { readFileSync, writeFileSync } from "node:fs";',
      'import { join } from "node:path";',
      'const digest = (value) => createHash("sha256").update(value).digest("hex");',
      `export async function readPrebuiltManifest() { return { artifacts: { app: { sha256: "${fixtureAppRuntimeHash}" } } }; }`,
      "export async function assertPrebuiltProject({ projectDir, pluginRoot }) {",
      '  writeFileSync(join(projectDir, ".test-runtime-verified"), "yes");',
      body,
      "  return { projectRoot: projectDir, pluginRoot, manifest: {} };",
      "}",
      "export async function readPrebuiltArtifact(name, { pluginRoot }) {",
      '  if (name !== "worker") throw new Error("Unexpected runtime asset.");',
      '  const path = join(pluginRoot, "assets/worker.mjs");',
      '  const code = readFileSync(path, "utf8");',
      `  if (digest(code) !== ${JSON.stringify(
        digest(runtimeSource),
      )}) throw new Error("Prebuilt Worker integrity mismatch.");`,
      artifactBody,
      "  return { path, code, sha256: digest(code), bytes: Buffer.byteLength(code) };",
      "}",
    ].join("\n"),
  );
  return helperPath;
}

function fixture({ legacySource = false } = {}) {
  const project = realpathSync(mkdtempSync(join(tmpdir(), "data-app-sites-package-")));
  for (const directory of [".openai", "dist", "src", "scripts", "node_modules/vite/bin"]) {
    mkdirSync(join(project, directory), { recursive: true });
  }
  writeFileSync(
    join(project, "package.json"),
    JSON.stringify({
      type: "module",
      scripts: { build: "node scripts/verify-protected-runtime.mjs" },
    }),
  );
  if (!legacySource) copyFileSync(digestHelperUrl, join(project, "scripts/protected-file-digest.mjs"));
  writeFileSync(
    join(project, "scripts/verify-protected-runtime.mjs"),
    [
      'import { createHash } from "node:crypto";',
      'import { readFileSync, writeFileSync } from "node:fs";',
      ...(legacySource ? [] : ['import { digestProtectedFile } from "./protected-file-digest.mjs";']),
      'const manifest = JSON.parse(readFileSync("protected-runtime.json", "utf8"));',
      "for (const [path, expected] of Object.entries(manifest.files)) {",
      legacySource
        ? '  const actual = createHash("sha256").update(readFileSync(path)).digest("hex");'
        : "  const actual = digestProtectedFile(path, readFileSync(path));",
      "  if (actual !== expected) throw new Error(`Protected runtime mismatch: ${path}`);",
      "}",
      'writeFileSync(".test-source-verified", "yes");',
    ].join("\n"),
  );
  writeSnapshot(
    { project },
    {
      generatedAt: "2026-08-02T04:57:36.243Z",
      queries: { reviewed: { rows: [{ amount: 42 }] } },
    },
  );
  writeFileSync(
    join(project, "src/data-app-schedule.js"),
    "export const normalizeDataAppRefreshSchedule = (value) => value;\n",
  );
  writeFileSync(join(project, "src/presentation-state.js"), fixturePresentationSource);
  writeFileSync(join(project, "src/data-app-owner.js"), fixtureOwnerSource());
  writeFileSync(join(project, "src/worker.js"), fixtureWorkerSource);
  writeFileSync(join(project, "src/data-app-worker.js"), fixtureRuntimeSource);
  writeFileSync(
    join(project, "node_modules/vite/bin/vite.js"),
    [
      'import { mkdirSync, readFileSync, writeFileSync } from "node:fs";',
      'import { join } from "node:path";',
      'const entry = process.argv[process.argv.indexOf("--ssr") + 1];',
      'const output = process.argv[process.argv.indexOf("--outDir") + 1];',
      'writeFileSync(join(process.cwd(), ".test-vite-arguments.json"), JSON.stringify(process.argv.slice(2)));',
      'writeFileSync(join(process.cwd(), ".test-vite-node-arguments.json"), JSON.stringify(process.execArgv));',
      "mkdirSync(output, { recursive: true });",
      'const source = readFileSync(entry, "utf8");',
      'const html = readFileSync(join(process.cwd(), "dist/index.html"), "utf8");',
      'writeFileSync(join(output, "index.js"), source + "\\n// reviewed HTML " + JSON.stringify(html)' +
        ' + "\\n// inherited session " + JSON.stringify(process.env.CODEX_SESSION_ID ?? "")' +
        ' + "\\n// inherited task " + JSON.stringify(process.env.CODEX_THREAD_ID ?? "")' +
        ' + "\\n// inherited WASI mode " + JSON.stringify(process.env.NAPI_RS_FORCE_WASI ?? "")' +
        ' + "\\n// inherited native library " + JSON.stringify(process.env.NAPI_RS_NATIVE_LIBRARY_PATH ?? null));',
    ].join("\n"),
  );
  writeFileSync(
    join(project, ".openai/hosting.json"),
    legacySource ? JSON.stringify({ d1: null, r2: null }) : `${JSON.stringify({ d1: "DB", r2: null }, null, 2)}\n`,
  );
  writeFileSync(
    join(project, "presentation.json"),
    JSON.stringify({
      theme: "codex-classic",
      title: "Reviewed Data app",
      filters: { week: "all" },
      blockLayouts: {
        "dashboard:dashboard:canvas": {
          authoredRevision: 2,
          order: ["trend", "metric"],
          rows: [{ id: "overview", items: ["trend", "metric"] }],
          spans: { trend: 8, metric: 4 },
          preferredSpans: { trend: 8, metric: 4 },
        },
      },
    }),
  );
  updateFixtureProtectedManifest({ project });
  return { project, helperPath: fixtureRuntime(), legacySource };
}

function legacyFixture() {
  return fixture({ legacySource: true });
}

function packageDataApp(
  { project, helperPath: fixtureHelper, legacySource = false },
  {
    projectId = "appgprj_reviewed",
    ownerEmail = "owner@example.com",
    readOnly = false,
    migratePackagingManifest = false,
    presentationPath = join(project, "presentation.json"),
    environment = process.env,
    helperPath = fixtureHelper,
    source = legacySource,
    extra = [],
  } = {},
) {
  return execFileSync(
    process.execPath,
    [
      helperPath,
      "--project-dir",
      project,
      `--project-id=${projectId}`,
      ...(ownerEmail === null ? [] : ["--owner-email", ownerEmail]),
      ...(readOnly ? ["--read-only"] : []),
      ...(migratePackagingManifest ? ["--migrate-packaging-manifest"] : []),
      ...(presentationPath ? ["--presentation-file", presentationPath] : []),
      ...(source ? ["--source"] : []),
      ...extra,
    ],
    { encoding: "utf8", env: environment, stdio: ["ignore", "pipe", "pipe"] },
  );
}

export {
  digest,
  fixture,
  fixtureOwnerSource,
  fixtureRuntime,
  fixtureRuntimeSource,
  fixtureWorkerSource,
  legacyFixture,
  packageDataApp,
  reviewedHtml,
  updateFixtureProtectedManifest,
  verifyFixtureProtectedManifest,
  writeSnapshot,
};
