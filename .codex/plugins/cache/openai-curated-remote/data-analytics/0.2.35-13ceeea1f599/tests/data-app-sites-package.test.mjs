import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  readlinkSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
import test, { describe } from "node:test";

import { embeddedScript, embeddedStyle } from "../scripts/data-app-build.mjs";
import { loadPrebuiltCompiler } from "../scripts/data-app-runtime.mjs";
import { encodeDataAssetFragment } from "../scripts/data-url.mjs";

import {
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
} from "./data-app-sites-package-fixtures.mjs";

function packagedConfiguration({ project }) {
  const worker = readFileSync(join(project, "dist/server/index.js"), "utf8");
  const prefix = "\nexport default createDataAppWorker(JSON.parse(";
  const suffix = "));\n";
  assert.ok(worker.endsWith(suffix));
  const offset = worker.lastIndexOf(prefix);
  assert.ok(offset >= 0);
  return JSON.parse(JSON.parse(worker.slice(offset + prefix.length, -suffix.length)));
}

const publicationPaths = [
  "dist/index.html",
  "src/data.json",
  "src/data-app-owner.js",
  ".openai/hosting.json",
  "protected-runtime.json",
  "dist/.openai/hosting.json",
  "dist/server/index.js",
];

function publicationBytes({ project }) {
  return publicationPaths.map((path) => (existsSync(join(project, path)) ? readFileSync(join(project, path)) : null));
}

function outputTree(path) {
  const metadata = lstatSync(path);
  if (metadata.isSymbolicLink()) return { symlink: readlinkSync(path) };
  if (metadata.isDirectory()) {
    return Object.fromEntries(
      readdirSync(path)
        .sort()
        .map((name) => [name, outputTree(join(path, name))]),
    );
  }
  return readFileSync(path).toString("base64");
}

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function localReferenceMarker(
  { project },
  document = JSON.stringify({
    root: project,
    htmlPath: realpathSync(join(project, "dist/index.html")),
  }),
) {
  return `<meta name="data-app-local-reference" content="${escapeAttribute(document)}">`;
}

function textualDataUrl(kind, source) {
  return `data:text/${kind};charset=utf-8;base64,${Buffer.from(source).toString("base64")}`;
}

function assetDataUrl(mime, bytes, fragment = "") {
  return (
    `data:${mime};base64,${Buffer.from(bytes).toString("base64")}` +
    (fragment ? `#${encodeDataAssetFragment(fragment)}` : "")
  );
}

function hazardMarkup(kind, value) {
  return kind === "javascript"
    ? embeddedScript(`globalThis.dataAppHazard = ${JSON.stringify(`</script>${value}`)};`)
    : embeddedStyle(`.data-note::after { content: ${JSON.stringify(`</style>${value}`)}; }`);
}

function graphAssetMarkup(url) {
  return embeddedScript(
    `globalThis.dataAppAsset = JSON.parse(${JSON.stringify(JSON.stringify(url))});` +
      'globalThis.dataAppHazard = "</script>";',
  );
}

test("the default packages a verified prebuilt Worker without node_modules, npm, or Vite", async () => {
  const state = fixture();
  rmSync(join(state.project, "node_modules"), { recursive: true, force: true });
  const result = JSON.parse(packageDataApp(state, { environment: { ...process.env, PATH: "" } }).trim());
  assert.equal(result.buildMode, "prebuilt");
  assert.equal(result.workerRuntimeSha256, digest(fixtureRuntimeSource));
  assert.equal(readFileSync(join(state.project, ".test-runtime-verified"), "utf8"), "yes");
  assert.equal(existsSync(join(state.project, ".test-source-verified")), false);
  assert.equal(existsSync(join(state.project, "node_modules")), false);
  assert.equal(existsSync(join(state.project, ".test-vite-arguments.json")), false);
  const worker = (await import(pathToFileURL(join(state.project, "dist/server/index.js")).href)).default;
  assert.equal(
    await (await worker.fetch(new Request("https://dashboard.chatgpt.site"))).text(),
    readFileSync(join(state.project, "dist/index.html"), "utf8"),
  );
});

test("loads verified runtime bytes rather than re-reading a changed asset or a project-local validator", () => {
  const state = fixture();
  const poisonedValidator = 'throw new Error("Project-local validator was executed.");';
  writeFileSync(join(state.project, "src/presentation-state.js"), poisonedValidator);
  updateFixtureProtectedManifest(state, ["src/presentation-state.js"]);
  const helperPath = fixtureRuntime({
    artifactBody: "  writeFileSync(path, 'throw new Error(\"Changed runtime was executed.\");');",
  });
  const output = JSON.parse(packageDataApp(state, { helperPath }).trim());
  assert.equal(output.buildMode, "prebuilt");
  assert.equal(packagedConfiguration(state).initialPresentation.title, "Reviewed Data app");
});

test("rejects damaged runtime bytes before mutating a publication", async (t) => {
  for (const [name, prepare, expected] of [
    [
      "runtime tampering",
      (state) =>
        writeFileSync(
          join(dirname(state.helperPath), "../../../assets/worker.mjs"),
          `${fixtureRuntimeSource}\n// modified\n`,
        ),
      /Prebuilt Worker integrity mismatch/u,
    ],
    [
      "invalid runtime module",
      (state) => {
        state.helperPath = fixtureRuntime({ runtimeSource: "export const broken = ;" });
      },
      /verified Data Worker module could not be loaded/u,
    ],
    [
      "missing stable local factory binding",
      (state) => {
        state.helperPath = fixtureRuntime({
          runtimeSource:
            fixtureRuntimeSource.replace("export function createDataAppWorker(", "function renamedFactory(") +
            "\nexport { renamedFactory as createDataAppWorker };",
        });
      },
      /verified Data Worker module could not be loaded/u,
    ],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      mkdirSync(join(state.project, "dist/server"));
      writeFileSync(join(state.project, "dist/server/index.js"), "// previous reviewed Worker\n");
      prepare(state);
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state), expected);
      assert.deepEqual(publicationBytes(state), before);
      assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
    });
  }
});

test("rejects invalid publication inputs before loading the prebuilt runtime", () => {
  const state = fixture();
  const htmlPath = join(state.project, "dist/index.html");
  writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace(/<meta name="data-app-snapshot-sha256"[^>]*>/u, ""));
  assert.throws(() => packageDataApp(state), /exactly one matching reviewed snapshot integrity marker/u);
  assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
  assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
});

test("prebuilt publishing preserves database bindings and rejects unknown hosting metadata", async (t) => {
  for (const fields of [{ d1: "EXISTING_DB" }, { r2: "FILES" }, { deployment_token: "synthetic-secret" }]) {
    await t.test(JSON.stringify(fields), () => {
      const state = fixture();
      writeFileSync(join(state.project, ".openai/hosting.json"), JSON.stringify({ d1: "DB", r2: null, ...fields }));
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state), /Prebuilt Data hosting/u);
      assert.deepEqual(publicationBytes(state), before);
    });
  }
});

test("prebuilt packaging rejects stale executable outputs and symlinks without deleting them", async (t) => {
  for (const [name, prepare] of [
    [
      "extra chunk",
      ({ project }) => {
        writeFileSync(join(project, "dist/server/old-chunk.js"), "// private old chunk\n");
      },
    ],
    [
      "extra directory",
      ({ project }) => {
        mkdirSync(join(project, "dist/server/chunks"));
        writeFileSync(join(project, "dist/server/chunks/old.js"), "// private nested chunk\n");
      },
    ],
    [
      "Worker symlink",
      ({ project }) => {
        rmSync(join(project, "dist/server/index.js"));
        symlinkSync(join(project, "src/worker.js"), join(project, "dist/server/index.js"));
      },
    ],
    [
      "server-directory symlink",
      ({ project }) => {
        rmSync(join(project, "dist/server"), { recursive: true, force: true });
        mkdirSync(join(project, "old-server"));
        writeFileSync(join(project, "old-server/index.js"), "// previous reviewed Worker\n");
        symlinkSync(
          join(project, "old-server"),
          join(project, "dist/server"),
          process.platform === "win32" ? "junction" : "dir",
        );
      },
    ],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      mkdirSync(join(state.project, "dist/server"));
      writeFileSync(join(state.project, "dist/server/index.js"), "// previous reviewed Worker\n");
      prepare(state);
      const before = publicationBytes(state);
      const serverBefore = outputTree(join(state.project, "dist/server"));
      assert.throws(
        () => packageDataApp(state),
        /Review and remove stale source-build outputs, or use explicit --source/u,
      );
      assert.deepEqual(publicationBytes(state), before);
      assert.deepEqual(outputTree(join(state.project, "dist/server")), serverBefore);
      assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
    });
  }
});

test("explicit source packaging verifies and retains a customized local Worker without installing packages", () => {
  const state = fixture();
  const customized = `${fixtureWorkerSource}\n// authorized source customization\n`;
  writeFileSync(join(state.project, "src/worker.js"), customized);
  updateFixtureProtectedManifest(state, ["src/worker.js"]);
  const output = JSON.parse(
    packageDataApp(state, {
      source: true,
      environment: { ...process.env, PATH: "", NAPI_RS_FORCE_WASI: "existing-selection" },
    }).trim(),
  );
  assert.equal(output.buildMode, "source");
  assert.equal(readFileSync(join(state.project, ".test-source-verified"), "utf8"), "yes");
  const worker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
  assert.match(worker, /authorized source customization/u);
  assert.match(worker, /initialPresentation: JSON\.parse\(/u);
  assert.match(worker, /inherited WASI mode "existing-selection"/u);
  assert.deepEqual(JSON.parse(readFileSync(join(state.project, ".test-vite-node-arguments.json"))), []);
});

test("source-mode integrity and local dependency failures leave reviewed files unchanged", async (t) => {
  for (const [name, prepare, expected] of [
    [
      "modified source Worker",
      ({ project }) => writeFileSync(join(project, "src/data-app-worker.js"), "throw new Error('Unapproved source');\n"),
      /runtime files were modified outside packaging ownership/u,
    ],
    [
      "missing local Vite",
      ({ project }) => rmSync(join(project, "node_modules"), { recursive: true, force: true }),
      /already-installed project Vite/u,
    ],
    [
      "failed source verifier",
      ({ project }) => writeFileSync(join(project, "scripts/verify-protected-runtime.mjs"), "process.exit(17);\n"),
      /source verification failed with status 17/u,
    ],
    [
      "missing owner factory argument",
      ({ project }) =>
        writeFileSync(
          join(project, "src/worker.js"),
          fixtureWorkerSource.replace("ownerEmailSha256: dataAppOwnerEmailSha256,", ""),
        ),
      /requires a confirmed, scoped protected runtime upgrade/u,
    ],
    [
      "an extra owner seed overrides the packaged email",
      ({ project }) =>
        writeFileSync(
          join(project, "src/worker.js"),
          fixtureWorkerSource.replace("});", `  ownerEmailSha256: "${digest("another-owner@example.com")}",\n});`),
        ),
      /expected owner authorization and presentation factory/u,
    ],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      prepare(state);
      updateFixtureProtectedManifest(state, ["scripts/verify-protected-runtime.mjs", "src/worker.js"]);
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state, { source: true }), expected);
      assert.deepEqual(publicationBytes(state), before);
      assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
      assert.equal(existsSync(join(state.project, ".test-vite-arguments.json")), false);
    });
  }
});

test("source-mode Vite must stay inside the reviewed project", () => {
  const state = fixture();
  const outside = fixture();
  const localVite = join(state.project, "node_modules/vite/bin/vite.js");
  rmSync(localVite);
  symlinkSync(join(outside.project, "node_modules/vite/bin/vite.js"), localVite);
  const before = publicationBytes(state);
  assert.throws(() => packageDataApp(state, { source: true }), /inside the Data app project/u);
  assert.deepEqual(publicationBytes(state), before);
});

test("packages the exact reviewed Data app with owner, presentation, and DB binding", () => {
  const state = fixture();
  const html = readFileSync(join(state.project, "dist/index.html"));
  const snapshot = readFileSync(join(state.project, "src/data.json"));
  const output = JSON.parse(packageDataApp(state).trim());
  const ownerHash = createHash("sha256").update("owner@example.com").digest("hex");

  assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), html);
  assert.deepEqual(readFileSync(join(state.project, "src/data.json")), snapshot);
  assert.equal(output.htmlSha256, createHash("sha256").update(html).digest("hex"));
  assert.equal(output.snapshotSha256, createHash("sha256").update(snapshot).digest("hex"));
  assert.equal(output.databaseBinding, "DB");
  assert.equal(output.ownerSeeded, true);
  assert.equal(output.ownerPreserved, false);
  assert.equal(output.ownerTransferred, false);
  assert.equal(output.ownerRevoked, false);
  assert.deepEqual(output.queryIds, ["reviewed"]);
  assert.deepEqual(JSON.parse(readFileSync(join(state.project, "dist/.openai/hosting.json"))), {
    d1: "DB",
    r2: null,
    project_id: "appgprj_reviewed",
  });
  assert.match(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), new RegExp(ownerHash));
  assert.doesNotMatch(
    readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"),
    /owner@example.com/u,
  );
  const packagedWorker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
  assert.match(packagedWorker, /codex-classic/u);
  const configuration = packagedConfiguration(state);
  assert.equal(
    configuration.ownerEmailSha256,
    ownerHash,
    "The Worker must use the staged Site owner email hash before it is persisted",
  );
  assert.doesNotMatch(packagedWorker, /owner@example.com/u);
  assert.deepEqual(configuration.seedSnapshot, JSON.parse(snapshot));
  assert.equal(configuration.projectId, "appgprj_reviewed");
  assert.equal(configuration.html, html.toString("utf8"));
  const seededPresentation = configuration.initialPresentation;
  assert.deepEqual(
    seededPresentation.blockLayouts["dashboard:dashboard:canvas"],
    {
      authoredRevision: 2,
      order: ["trend", "metric"],
      rows: [{ id: "overview", items: ["trend", "metric"] }],
      spans: { trend: 8, metric: 4 },
      preferredSpans: { trend: 8, metric: 4 },
    },
    "Sites packaging must seed the owner's exact block order, row membership, widths, and preferred widths",
  );
  assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
});

test("serializes reviewed configuration as data, preserving special property names and script-like strings", async () => {
  const state = fixture();
  const snapshot = JSON.parse('{"queries":{"reviewed":{"rows":[{"__proto__":{"kept":true}}]}}}');
  snapshot.queries.reviewed.rows[0].text = '"); globalThis.__dataAppWorkerInjection = true; // </script> \u2028\u2029';
  writeSnapshot(state, snapshot);
  packageDataApp(state);
  const worker = (await import(pathToFileURL(join(state.project, "dist/server/index.js")).href)).default;
  const row = worker.configuration.seedSnapshot.queries.reviewed.rows[0];
  assert.deepEqual(row, snapshot.queries.reviewed.rows[0]);
  assert.equal(Object.hasOwn(row, "__proto__"), true);
  assert.equal(Object.getPrototypeOf(row), Object.prototype);
  assert.equal(globalThis.__dataAppWorkerInjection, undefined);
});

test("removes canonical local preview references together with transient task metadata", () => {
  const state = fixture();
  const htmlPath = join(state.project, "dist/index.html");
  const reviewed = readFileSync(htmlPath, "utf8").replace("Reviewed Data app", "Reviewed Data app · α");
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  writeFileSync(
    htmlPath,
    reviewed.replace(
      "</head>",
      `${localReferenceMarker(state)}<meta name="data-app-local-thread" content="${threadId}"></head>`,
    ),
  );
  const output = JSON.parse(
    packageDataApp(state, {
      environment: { ...process.env, CODEX_SESSION_ID: threadId },
    }).trim(),
  );
  assert.equal(readFileSync(htmlPath, "utf8"), reviewed);
  assert.equal(packagedConfiguration(state).html, reviewed);
  assert.equal(output.htmlSha256, digest(reviewed));
  const worker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
  assert.equal(worker.includes(state.project), false);
  assert.equal(worker.includes(threadId), false);
  assert.doesNotMatch(worker, /<meta name=\\?"data-app-local-reference/u);
});

test("rejects duplicate, malformed, foreign, or leaked local preview references before publication", async (t) => {
  const outside = fixture();
  for (const [name, buildMarkers, expected] of [
    ["duplicate", (state) => localReferenceMarker(state).repeat(2), /duplicate local-reference metadata/u],
    [
      "extra key",
      (state) =>
        localReferenceMarker(
          state,
          JSON.stringify({
            root: state.project,
            htmlPath: join(state.project, "dist/index.html"),
            extra: true,
          }),
        ),
      /malformed local-reference metadata/u,
    ],
    [
      "duplicate JSON key",
      (state) =>
        localReferenceMarker(
          state,
          `{\"root\":${JSON.stringify(state.project)},\"root\":${JSON.stringify(state.project)},` +
            `\"htmlPath\":${JSON.stringify(join(state.project, "dist/index.html"))}}`,
        ),
      /malformed local-reference metadata/u,
    ],
    [
      "relative root",
      (state) =>
        localReferenceMarker(
          state,
          JSON.stringify({
            root: ".",
            htmlPath: join(state.project, "dist/index.html"),
          }),
        ),
      /malformed local-reference metadata/u,
    ],
    ["foreign project", () => localReferenceMarker(outside), /malformed local-reference metadata/u],
    [
      "attribute order",
      (state) =>
        localReferenceMarker(state)
          .replace('<meta name="data-app-local-reference" content=', "<meta content=")
          .replace(/>$/u, ' name="data-app-local-reference">'),
      /malformed local-reference metadata/u,
    ],
    [
      "unquoted name",
      (state) =>
        localReferenceMarker(state).replace('name="data-app-local-reference"', "name=data-app-local-reference"),
      /malformed local-reference metadata/u,
    ],
    [
      "literal path leak",
      (state) => `${localReferenceMarker(state)}<span>${state.project}</span>`,
      /local filesystem reference outside/u,
    ],
    [
      "encoded path leak",
      (state) => `${localReferenceMarker(state)}<span>${encodeURIComponent(state.project)}</span>`,
      /local filesystem reference outside/u,
    ],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      const htmlPath = join(state.project, "dist/index.html");
      writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${buildMarkers(state)}</head>`));
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state), expected);
      assert.deepEqual(publicationBytes(state), before);
      assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
    });
  }
});

test("local paths cannot leak through the Worker with or without preview metadata", async (t) => {
  for (const withMarker of [false, true]) {
    await t.test(withMarker ? "saved preview" : "normal or previously packaged HTML", () => {
      const state = fixture();
      packageDataApp(state);
      writeSnapshot(state, { queries: { reviewed: { rows: [{ localPath: state.project }] } } });
      const htmlPath = join(state.project, "dist/index.html");
      if (withMarker) {
        writeFileSync(
          htmlPath,
          readFileSync(htmlPath, "utf8").replace("</head>", `${localReferenceMarker(state)}</head>`),
        );
      }
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state), /Sites Worker must not contain a local filesystem reference/u);
      assert.deepEqual(publicationBytes(state), before);
    });
  }
});

test("preserves clean hazard-encoded scripts and styles without fetching or rewriting them", () => {
  const state = fixture();
  const nestedUrl = textualDataUrl("javascript", "globalThis.cleanNestedText = true;");
  const imageUrl = assetDataUrl("image/svg+xml", '<svg xmlns="http://www.w3.org/2000/svg"/>');
  const markup =
    embeddedScript(
      'globalThis.hazard = "</script>"; globalThis.prefix = "data:text/javascript;charset=utf-8;base64,";' +
        `globalThis.templateUrl = \`${nestedUrl}\`;` +
        'const encoded = "YQ=="; globalThis.dynamicUrl = `data:text/javascript;charset=utf-8;base64,${encoded}`;',
    ) +
    embeddedStyle(`.data-note { background-image: url(${imageUrl} ); }` + '.data-note::after { content: "</style>"; }');
  assert.match(markup, /data:text\/javascript;charset=utf-8;base64,/u);
  assert.match(markup, /data:text\/css;charset=utf-8;base64,/u);
  const htmlPath = join(state.project, "dist/index.html");
  const html = readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`);
  writeFileSync(htmlPath, html);

  packageDataApp(state);

  assert.equal(readFileSync(htmlPath, "utf8"), html);
  assert.equal(packagedConfiguration(state).html, html);
});

test("HTML-like dynamic source templates are not mistaken for generated attributes", async (t) => {
  const code =
    'const encoded = "YQ==";' +
    'globalThis.dynamicMarkup = `<script src="data:text/javascript;base64,${encoded}">`;' +
    "globalThis.dynamicCss = `url(data:text/css;base64,${encoded})`;";
  for (const encoded of [false, true]) {
    await t.test(encoded ? "base64 script" : "inline script", () => {
      const state = fixture();
      // The assembler encodes an opening <script token too; a source-built
      // reviewed document can still contain this valid inline template.
      const markup = encoded ? embeddedScript(code + 'globalThis.hazard = "</script>";') : `<script>${code}</script>`;
      assert.equal(markup.startsWith("<script src="), encoded);
      const htmlPath = join(state.project, "dist/index.html");
      const html = readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`);
      writeFileSync(htmlPath, html);

      packageDataApp(state);

      assert.equal(packagedConfiguration(state).html, html);
    });
  }
});

test("ignored noncanonical source examples do not consume the embedded-URL budget", () => {
  const state = fixture();
  const examples = Array.from({ length: 257 }, () => JSON.stringify("data:text/plain;base64,Zh=="));
  const markup = embeddedScript(`globalThis.examples = [${examples.join(",")}]; globalThis.hazard = "</script>";`);
  const htmlPath = join(state.project, "dist/index.html");
  const html = readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`);
  writeFileSync(htmlPath, html);

  packageDataApp(state);

  assert.equal(packagedConfiguration(state).html, html);
});

test("encoded script and stylesheet payloads cannot hide local task IDs or paths", async (t) => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  for (const kind of ["javascript", "css"]) {
    for (const privacy of ["task", "path"]) {
      for (const withMarker of [false, true]) {
        await t.test(`${kind}: ${privacy}, ${withMarker ? "saved preview" : "repeat without metadata"}`, () => {
          const state = fixture();
          packageDataApp(state);
          rmSync(join(state.project, ".test-runtime-verified"));
          const privateValue = privacy === "task" ? threadId : state.project;
          const htmlPath = join(state.project, "dist/index.html");
          const markers = withMarker
            ? `${localReferenceMarker(state)}<meta name="data-app-local-thread" content="${threadId}">`
            : "";
          const encodedMarkup = hazardMarkup(kind, privateValue);
          const html = readFileSync(htmlPath, "utf8").replace("</head>", `${markers}${encodedMarkup}</head>`);
          writeFileSync(htmlPath, html);
          assert.equal(
            encodedMarkup.includes(privateValue),
            false,
            "The private value is present only in the encoded source",
          );
          const before = publicationBytes(state);

          assert.throws(
            () =>
              packageDataApp(state, {
                environment: { ...process.env, CODEX_SESSION_ID: threadId },
              }),
            privacy === "task" ? /local task identifier outside/u : /local filesystem reference outside/u,
          );

          assert.deepEqual(publicationBytes(state), before);
          assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
        });
      }
    }
  }
});

test("nested encoded text and encoded Worker configuration receive the same privacy checks", async (t) => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  await t.test("nested textual data URL", () => {
    const state = fixture();
    const inner = textualDataUrl("css", `/* </style>${threadId} */`);
    const markup = embeddedScript(`globalThis.nested = ${JSON.stringify(inner)}; globalThis.hazard = "</script>";`);
    const htmlPath = join(state.project, "dist/index.html");
    writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
    const before = publicationBytes(state);
    assert.throws(
      () =>
        packageDataApp(state, {
          environment: { ...process.env, CODEX_SESSION_ID: threadId },
        }),
      /local task identifier outside/u,
    );
    assert.deepEqual(publicationBytes(state), before);
  });
  for (const kind of ["javascript", "css"]) {
    for (const privacy of ["task", "path"]) {
      await t.test(`Worker config ${kind}: ${privacy}`, () => {
        const state = fixture();
        packageDataApp(state);
        const privateValue = privacy === "task" ? threadId : state.project;
        writeSnapshot(state, {
          queries: {
            reviewed: {
              rows: [
                {
                  encoded: textualDataUrl(kind, `/* </${kind === "css" ? "style" : "script"}>${privateValue} */`),
                },
              ],
            },
          },
        });
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              environment: { ...process.env, CODEX_SESSION_ID: threadId },
            }),
          privacy === "task"
            ? /Sites Worker must not contain a local task identifier/u
            : /Sites Worker must not contain a local filesystem reference/u,
        );

        assert.deepEqual(publicationBytes(state), before);
      });
    }
  }
});

test("graph-generated CSS, text, JSON, SVG, and opaque assets cannot hide private bytes", async (t) => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  for (const [mime, encode] of [
    ["text/css", (value) => `/* </style>${value} */`],
    ["text/plain", (value) => `Reviewed note: ${value}`],
    ["text/csv", (value) => `name\n${value}\n`],
    ["application/json", (value) => JSON.stringify({ note: value })],
    ["image/svg+xml", (value) => `<svg><title>${value}</title></svg>`],
    ["application/octet-stream", (value) => Buffer.concat([Buffer.from([0xff, 0, 0xfe]), Buffer.from(value)])],
  ]) {
    for (const privacy of ["task", "path"]) {
      await t.test(`${mime}: ${privacy}`, () => {
        const state = fixture();
        packageDataApp(state);
        rmSync(join(state.project, ".test-runtime-verified"));
        const privateValue = privacy === "task" ? threadId : state.project;
        const markup = graphAssetMarkup(assetDataUrl(mime, encode(privateValue)));
        const htmlPath = join(state.project, "dist/index.html");
        writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              environment: { ...process.env, CODEX_SESSION_ID: threadId },
            }),
          privacy === "task" ? /local task identifier outside/u : /local filesystem reference outside/u,
        );

        assert.deepEqual(publicationBytes(state), before);
        assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
      });
    }
  }
});

test("clean binary assets and canonical asset fragments remain publishable", () => {
  const state = fixture();
  const assets = [
    assetDataUrl("application/octet-stream", Buffer.from([0xff, 0xfe, 0, 0x80, 0x7f])),
    assetDataUrl("image/png", Buffer.from([0x89, 0x50, 0x4e, 0x47, 0xff, 0])),
    assetDataUrl("image/svg+xml", '<svg xmlns="http://www.w3.org/2000/svg"/>', "icon:(a)'~"),
    assetDataUrl("application/vnd.example+json", JSON.stringify({ clean: true })),
  ];
  const htmlPath = join(state.project, "dist/index.html");
  const html = readFileSync(htmlPath, "utf8").replace("</head>", `${assets.map(graphAssetMarkup).join("")}</head>`);
  writeFileSync(htmlPath, html);

  packageDataApp(state);

  assert.equal(packagedConfiguration(state).html, html);
});

test("actual CSS serialization preserves punctuation in canonical SVG asset fragments", async () => {
  const state = fixture();
  const compiler = await loadPrebuiltCompiler();
  const url = assetDataUrl("image/svg+xml", '<svg xmlns="http://www.w3.org/2000/svg"/>', "icon:(a)'~");
  const serializedUrl = compiler.generateCss({ type: "Url", value: url });
  assert.equal(serializedUrl, `url(${url})`);
  const css = compiler.generateCss(compiler.parseCss(`.icon { mask-image: ${serializedUrl}; }`));
  const markup = embeddedStyle(css) + embeddedStyle(`${css}.note::after { content: "</style>"; }`);
  const htmlPath = join(state.project, "dist/index.html");
  const html = readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`);
  writeFileSync(htmlPath, html);

  packageDataApp(state);

  assert.equal(packagedConfiguration(state).html, html);
});

test("asset fragments and JSON-escaped URL values cannot bypass privacy or canonicality checks", async (t) => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  await t.test("private canonical asset fragment", () => {
    const state = fixture();
    const markup = graphAssetMarkup(assetDataUrl("image/svg+xml", "<svg/>", state.project));
    const htmlPath = join(state.project, "dist/index.html");
    writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
    const before = publicationBytes(state);
    assert.throws(() => packageDataApp(state), /local filesystem reference outside/u);
    assert.deepEqual(publicationBytes(state), before);
  });
  for (const privacy of ["task", "path"]) {
    await t.test(`nested data URL in an asset fragment: ${privacy}`, () => {
      const state = fixture();
      packageDataApp(state);
      const privateValue = privacy === "task" ? threadId : state.project;
      const fragment = assetDataUrl("text/plain", privateValue);
      const markup = graphAssetMarkup(assetDataUrl("image/svg+xml", "<svg/>", fragment));
      const htmlPath = join(state.project, "dist/index.html");
      writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
      const before = publicationBytes(state);

      assert.throws(
        () => packageDataApp(state, { environment: { ...process.env, CODEX_SESSION_ID: threadId } }),
        privacy === "task" ? /local task identifier outside/u : /local filesystem reference outside/u,
      );

      assert.deepEqual(publicationBytes(state), before);
    });
  }
  for (const whitespace of ["\n", "\r", "\t"]) {
    for (const privacy of ["task", "path"]) {
      await t.test(`configuration ${JSON.stringify(whitespace)}: ${privacy}`, () => {
        const state = fixture();
        packageDataApp(state);
        const privateValue = privacy === "task" ? threadId : state.project;
        const encoded = Buffer.from(`safe${privateValue}`).toString("base64");
        const url = `data:text/plain;base64,${encoded.slice(0, 4)}${whitespace}${encoded.slice(4)}`;
        writeSnapshot(state, { queries: { reviewed: { rows: [{ url }] } } });
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              environment: { ...process.env, CODEX_SESSION_ID: threadId },
            }),
          /malformed embedded data URL/u,
        );

        assert.deepEqual(publicationBytes(state), before);
      });
    }
  }
  await t.test("JSON asset containing escaped URL whitespace", () => {
    const state = fixture();
    const encoded = Buffer.from(`safe${threadId}`).toString("base64");
    const url = `data:text/plain;base64,${encoded.slice(0, 4)}\n${encoded.slice(4)}`;
    const markup = graphAssetMarkup(assetDataUrl("application/json", JSON.stringify({ url })));
    const htmlPath = join(state.project, "dist/index.html");
    writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
    const before = publicationBytes(state);
    assert.throws(
      () =>
        packageDataApp(state, {
          environment: { ...process.env, CODEX_SESSION_ID: threadId },
        }),
      /malformed embedded data URL/u,
    );
    assert.deepEqual(publicationBytes(state), before);
  });
});

test("malformed or unbounded generated text data URLs fail closed", async (t) => {
  const prefix = "data:text/javascript;charset=utf-8;base64,";
  let deeplyNested = "safe";
  let deeplyNestedFragment = "safe";
  for (let depth = 0; depth < 9; depth += 1) deeplyNested = textualDataUrl("javascript", deeplyNested);
  for (let depth = 0; depth < 9; depth += 1) {
    deeplyNestedFragment = assetDataUrl("image/svg+xml", "<svg/>", deeplyNestedFragment);
  }
  for (const [name, url, expected] of [
    ["invalid alphabet", `${prefix}AAAA!`, /malformed embedded data URL/u],
    ["embedded whitespace", `${prefix}YQ== Zg==`, /malformed embedded data URL/u],
    ["missing canonical padding", `${prefix}YQ`, /malformed embedded data URL/u],
    ["nonzero padding bits", `${prefix}Zh==`, /malformed embedded data URL/u],
    ["dynamic actual HTML attribute", `${prefix}\${encoded}`, /malformed embedded data URL/u],
    ["malformed binary asset", "data:application/octet-stream;base64,AAAA!", /malformed embedded data URL/u],
    ["malformed asset fragment", "data:image/svg+xml;base64,PHN2Zy8+#%ZZ", /malformed embedded data URL/u],
    ["non-UTF-8", `${prefix}/w==`, /non-UTF-8 embedded text data URL/u],
    ["non-UTF-8 graph text asset", "data:text/plain;base64,/w==", /non-UTF-8 embedded text data URL/u],
    ["too deeply nested", deeplyNested, /embedded-data privacy inspection limits/u],
    ["too deeply nested asset fragments", deeplyNestedFragment, /embedded-data privacy inspection limits/u],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      const htmlPath = join(state.project, "dist/index.html");
      writeFileSync(
        htmlPath,
        readFileSync(htmlPath, "utf8").replace("</head>", `<script src="${url}"></script></head>`),
      );
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state), expected);
      assert.deepEqual(publicationBytes(state), before);
      assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
    });
  }
  await t.test("too many textual data URLs", () => {
    const state = fixture();
    const htmlPath = join(state.project, "dist/index.html");
    const markup = Array.from(
      { length: 257 },
      (_, index) => `<script src="${textualDataUrl("javascript", `/* clean ${index} */`)}"></script>`,
    ).join("");
    writeFileSync(htmlPath, readFileSync(htmlPath, "utf8").replace("</head>", `${markup}</head>`));
    const before = publicationBytes(state);
    assert.throws(() => packageDataApp(state), /embedded-data privacy inspection limits/u);
    assert.deepEqual(publicationBytes(state), before);
  });
});

test("removes only transient local task metadata before packaging the public HTML and Worker", () => {
  const state = fixture();
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  const childThreadId = "de305d54-75b4-431b-adb2-eb6b9e546014";
  const preservedMarker = '<meta name="color-scheme" content="light dark">';
  const localMarker = `<meta name="data-app-local-thread" content="${threadId}">`;
  const snapshot = readFileSync(join(state.project, "src/data.json"), "utf8");
  const publishedHtml = reviewedHtml(snapshot)
    .replace("</head>", `${preservedMarker}</head>`)
    .replace("Reviewed Data app", "Reviewed Data app · α");
  writeFileSync(join(state.project, "dist/index.html"),
    publishedHtml.replace("</head>", `${localMarker}</head>`));

  const result = packageDataApp(state, {
    environment: {
      ...process.env,
      CODEX_SESSION_ID: threadId,
      CODEX_THREAD_ID: childThreadId,
    },
  });
  const output = JSON.parse(result.trim());
  const html = readFileSync(join(state.project, "dist/index.html"), "utf8");
  const worker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");

  assert.equal(html, publishedHtml, "Only the transient task marker may change in reviewed HTML");
  assert.ok(html.includes(preservedMarker));
  assert.equal(output.htmlSha256, createHash("sha256").update(publishedHtml).digest("hex"));
  for (const artifact of [html, worker, result]) {
    assert.doesNotMatch(artifact, new RegExp(`${threadId}|${childThreadId}`, "iu"));
  }
  assert.doesNotMatch(html, /<meta\s+name="data-app-local-thread"/iu);
});

test("rejects malformed, duplicate, or leaked local task metadata before publication", () => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  const childThreadId = "de305d54-75b4-431b-adb2-eb6b9e546014";
  const validMarker = `<meta name="data-app-local-thread" content="${threadId}">`;
  const environment = {
    ...process.env,
    CODEX_SESSION_ID: threadId,
    CODEX_THREAD_ID: childThreadId,
  };
  for (const [markers, pattern] of [
    ['<meta name="data-app-local-thread" content="not-a-uuid">', /malformed local task metadata/u],
    [
      '<meta name=data-app-local-thread content="550e8400-e29b-41d4-a716-446655440000">',
      /malformed local task metadata/u,
    ],
    [`${validMarker}${validMarker}`, /duplicate local task metadata/u],
    [`${validMarker}<span>${threadId.toUpperCase()}</span>`, /local task identifier outside/u],
    [`${validMarker}<span>${childThreadId}</span>`, /local task identifier outside/u],
  ]) {
    const state = fixture();
    const snapshot = readFileSync(join(state.project, "src/data.json"), "utf8");
    const html = reviewedHtml(snapshot).replace("</head>", `${markers}</head>`);
    writeFileSync(join(state.project, "dist/index.html"), html);
    const owner = readFileSync(join(state.project, "src/data-app-owner.js"));
    const hosting = readFileSync(join(state.project, ".openai/hosting.json"));

    assert.throws(() => packageDataApp(state, { environment }), pattern);
    assert.equal(readFileSync(join(state.project, "dist/index.html"), "utf8"), html);
    assert.deepEqual(readFileSync(join(state.project, "src/data-app-owner.js")), owner);
    assert.deepEqual(readFileSync(join(state.project, ".openai/hosting.json")), hosting);
    assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
    assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
  }

  for (const leakedId of [threadId, childThreadId]) {
    const leakedWorker = fixture();
    const htmlPath = join(leakedWorker.project, "dist/index.html");
    const originalHtml = readFileSync(htmlPath, "utf8").replace("</head>", `${validMarker}</head>`);
    writeFileSync(htmlPath, originalHtml);
    const owner = readFileSync(join(leakedWorker.project, "src/data-app-owner.js"));
    const hosting = readFileSync(join(leakedWorker.project, ".openai/hosting.json"));
    const workerPath = join(leakedWorker.project, "src/worker.js");
    writeFileSync(workerPath, `${readFileSync(workerPath, "utf8")}\n// ${leakedId.toUpperCase()}`);
    updateFixtureProtectedManifest(leakedWorker, ["src/worker.js"]);

    assert.throws(
      () => packageDataApp(leakedWorker, { environment, source: true }),
      (error) => {
        assert.match(error.stderr, /Sites Worker must not contain a local task identifier/u);
        assert.doesNotMatch(`${error.stdout}\n${error.stderr}`, new RegExp(`${threadId}|${childThreadId}`, "iu"));
        return true;
      },
    );
    assert.equal(
      readFileSync(htmlPath, "utf8"),
      originalHtml,
      "A post-build local-task privacy failure must restore the reviewed HTML",
    );
    assert.deepEqual(readFileSync(join(leakedWorker.project, "src/data-app-owner.js")), owner);
    assert.deepEqual(readFileSync(join(leakedWorker.project, ".openai/hosting.json")), hosting);
    assert.equal(
      existsSync(join(leakedWorker.project, "dist/server/index.js")),
      false,
      "A failed privacy check must remove the unsafe newly built Sites Worker",
    );
    assert.equal(existsSync(join(leakedWorker.project, "src/.sites-worker-entry.mjs")), false);
  }
});

test("preserves a verified owner and transfers ownership only with a new owner email", () => {
  const preserved = fixture();
  const ownerHash = createHash("sha256").update("owner@example.com").digest("hex");
  writeFileSync(join(preserved.project, "src/data-app-owner.js"), fixtureOwnerSource(ownerHash));
  const output = JSON.parse(packageDataApp(preserved).trim());
  assert.equal(output.ownerSeeded, true);
  assert.equal(output.ownerPreserved, true);
  assert.equal(output.ownerTransferred, false);
  assert.equal(output.ownerRevoked, false);

  const transferred = JSON.parse(packageDataApp(preserved, { ownerEmail: "new-owner@example.com" }).trim());
  const transferredHash = createHash("sha256").update("new-owner@example.com").digest("hex");
  assert.equal(transferred.ownerSeeded, true);
  assert.equal(transferred.ownerPreserved, false);
  assert.equal(transferred.ownerTransferred, true);
  assert.equal(transferred.ownerRevoked, false);
  assert.match(readFileSync(join(preserved.project, "src/data-app-owner.js"), "utf8"), new RegExp(transferredHash));
  assert.doesNotMatch(readFileSync(join(preserved.project, "src/data-app-owner.js"), "utf8"), new RegExp(ownerHash));
});

test("publishes a new Data app read-only when its Site owner email is unavailable", () => {
  const state = fixture();
  const output = JSON.parse(packageDataApp(state, { ownerEmail: null, readOnly: true }).trim());

  assert.equal(output.ownerSeeded, false);
  assert.equal(output.ownerPreserved, false);
  assert.equal(output.ownerTransferred, false);
  assert.equal(output.ownerRevoked, false);
  assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), fixtureOwnerSource());
  assert.equal(existsSync(join(state.project, "dist/server/index.js")), true);
});

test("revokes a previously seeded owner when the current owner cannot be verified", () => {
  const state = fixture();
  const previousOwnerHash = createHash("sha256").update("previous-site-owner").digest("hex");
  writeFileSync(join(state.project, "src/data-app-owner.js"), fixtureOwnerSource(previousOwnerHash));

  const output = JSON.parse(packageDataApp(state, { ownerEmail: null, readOnly: true }).trim());

  assert.equal(output.ownerSeeded, false);
  assert.equal(output.ownerPreserved, false);
  assert.equal(output.ownerTransferred, false);
  assert.equal(output.ownerRevoked, true);
  assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), fixtureOwnerSource());
  assert.doesNotMatch(
    readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"),
    new RegExp(previousOwnerHash),
  );
  assert.equal(existsSync(join(state.project, "dist/server/index.js")), true);
});

test("rejects a malformed persisted owner seed", () => {
  const malformed = fixture();
  writeFileSync(join(malformed.project, "src/data-app-owner.js"), fixtureOwnerSource("abc"));

  assert.throws(() => packageDataApp(malformed), /owner seed.*(?:invalid|SHA-256)/u);
});

test("failed Sites Worker builds restore reviewed HTML and do not transfer owner or mutate hosting", () => {
  const state = fixture();
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  const ownerPath = join(state.project, "src/data-app-owner.js");
  const hostingPath = join(state.project, ".openai/hosting.json");
  const htmlPath = join(state.project, "dist/index.html");
  const previousOwnerHash = createHash("sha256").update("previous-site-owner").digest("hex");
  writeFileSync(ownerPath, fixtureOwnerSource(previousOwnerHash));
  writeFileSync(
    htmlPath,
    readFileSync(htmlPath, "utf8").replace(
      "</head>",
      `<meta name="data-app-local-thread" content="${threadId}"></head>`,
    ),
  );
  const vitePath = join(state.project, "node_modules/vite/bin/vite.js");
  writeFileSync(vitePath, `${readFileSync(vitePath, "utf8")}\nprocess.exit(23);\n`);
  const ownerBefore = readFileSync(ownerPath);
  const hostingBefore = readFileSync(hostingPath);
  const htmlBefore = readFileSync(htmlPath);

  assert.throws(
    () =>
      packageDataApp(state, {
        ownerEmail: "new-site-owner@example.com",
        environment: { ...process.env, CODEX_SESSION_ID: threadId },
        source: true,
      }),
    /Sites Worker packaging failed with status 23/u,
  );
  assert.deepEqual(readFileSync(ownerPath), ownerBefore);
  assert.deepEqual(readFileSync(hostingPath), hostingBefore);
  assert.deepEqual(readFileSync(htmlPath), htmlBefore);
  assert.equal(
    existsSync(join(state.project, "dist/server/index.js")),
    false,
    "A partially emitted Worker must not survive a failed Sites build",
  );
  assert.equal(existsSync(join(state.project, "dist/.openai/hosting.json")), false);
  assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
});

test("failed Sites publication restores the previously published Worker byte-for-byte", async (t) => {
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  for (const [name, injectFailure, errorPattern] of [
    [
      "failed SSR build",
      ({ project }) => {
        const vitePath = join(project, "node_modules/vite/bin/vite.js");
        writeFileSync(vitePath, `${readFileSync(vitePath, "utf8")}\nprocess.exit(23);\n`);
      },
      /Sites Worker packaging failed with status 23/u,
    ],
    [
      "post-build local-task privacy failure",
      ({ project }) => {
        const workerPath = join(project, "src/worker.js");
        writeFileSync(workerPath, `${readFileSync(workerPath, "utf8")}\n// ${threadId.toUpperCase()}\n`);
      },
      /Sites Worker must not contain a local task identifier/u,
    ],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      const htmlPath = join(state.project, "dist/index.html");
      const ownerPath = join(state.project, "src/data-app-owner.js");
      const hostingPath = join(state.project, ".openai/hosting.json");
      const publishedWorkerPath = join(state.project, "dist/server/index.js");
      mkdirSync(join(state.project, "dist/server"), { recursive: true });
      const publishedWorker = Buffer.from(
        'export default { fetch() { return new Response("previous reviewed Worker"); } };\n',
      );
      writeFileSync(publishedWorkerPath, publishedWorker);
      writeFileSync(
        htmlPath,
        readFileSync(htmlPath, "utf8").replace(
          "</head>",
          `<meta name="data-app-local-thread" content="${threadId}"></head>`,
        ),
      );
      injectFailure(state);
      updateFixtureProtectedManifest(state, ["src/worker.js"]);
      const originalHtml = readFileSync(htmlPath);
      const originalOwner = readFileSync(ownerPath);
      const originalHosting = readFileSync(hostingPath);

      assert.throws(
        () =>
          packageDataApp(state, {
            environment: { ...process.env, CODEX_SESSION_ID: threadId },
            source: true,
          }),
        errorPattern,
      );
      assert.deepEqual(
        readFileSync(publishedWorkerPath),
        publishedWorker,
        "A failed republication must restore the last reviewed Sites Worker exactly",
      );
      assert.deepEqual(readFileSync(htmlPath), originalHtml);
      assert.deepEqual(readFileSync(ownerPath), originalOwner);
      assert.deepEqual(readFileSync(hostingPath), originalHosting);
      assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
    });
  }
});

test("a stale source Worker entry rejects source packaging before owner, hosting, or HTML mutation", () => {
  const state = fixture();
  const threadId = "550e8400-e29b-41d4-a716-446655440000";
  const ownerPath = join(state.project, "src/data-app-owner.js");
  const hostingPath = join(state.project, ".openai/hosting.json");
  const htmlPath = join(state.project, "dist/index.html");
  const temporaryWorkerPath = join(state.project, "src/.sites-worker-entry.mjs");
  const previousOwnerHash = createHash("sha256").update("previous-site-owner").digest("hex");
  writeFileSync(ownerPath, fixtureOwnerSource(previousOwnerHash));
  writeFileSync(
    htmlPath,
    readFileSync(htmlPath, "utf8").replace(
      "</head>",
      `<meta name="data-app-local-thread" content="${threadId}"></head>`,
    ),
  );
  writeFileSync(temporaryWorkerPath, "// existing Worker entry\n");
  const ownerBefore = readFileSync(ownerPath);
  const hostingBefore = readFileSync(hostingPath);
  const htmlBefore = readFileSync(htmlPath);

  assert.throws(
    () => packageDataApp(state, { ownerEmail: null, readOnly: true, source: true }),
    /A stale Sites Worker entry must be removed first/u,
  );
  assert.deepEqual(
    readFileSync(ownerPath),
    ownerBefore,
    "A failed read-only republication must not revoke the current owner",
  );
  assert.deepEqual(readFileSync(hostingPath), hostingBefore);
  assert.deepEqual(readFileSync(htmlPath), htmlBefore);
  assert.equal(readFileSync(temporaryWorkerPath, "utf8"), "// existing Worker entry\n");
  assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
});

test("accepts a UTF-8 BOM while binding the exact original snapshot bytes", () => {
  const state = fixture();
  const snapshot = { queries: { reviewed: { rows: [{ label: "Reviewed α", amount: 42 }] } } };
  const source = Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), Buffer.from(JSON.stringify(snapshot))]);
  writeSnapshot(state, source);
  const html = readFileSync(join(state.project, "dist/index.html"));

  const output = JSON.parse(packageDataApp(state).trim());

  assert.equal(output.snapshotSha256, digest(source));
  assert.notEqual(output.snapshotSha256, digest(source.subarray(3)), "The BOM remains part of the reviewed-byte hash");
  assert.deepEqual(readFileSync(join(state.project, "src/data.json")), source);
  assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), html);
  assert.deepEqual(packagedConfiguration(state).seedSnapshot, snapshot);
});

test("rejects non-UTF-8 snapshot bytes before runtime loading or publication mutation", async (t) => {
  for (const [name, invalid] of [
    ["invalid byte", [0xff]],
    ["truncated multibyte sequence", [0xe2, 0x82]],
    ["overlong sequence", [0xc0, 0xaf]],
    ["UTF-16 byte-order marker", [0xff, 0xfe]],
  ]) {
    await t.test(name, () => {
      const state = fixture();
      const source = Buffer.concat([
        Buffer.from('{"queries":{"reviewed":{"rows":[{"text":"'),
        Buffer.from(invalid),
        Buffer.from('"}]}}}'),
      ]);
      writeSnapshot(state, source);
      mkdirSync(join(state.project, "dist/server"));
      writeFileSync(join(state.project, "dist/server/index.js"), "// previous reviewed Worker\n");
      const before = publicationBytes(state);

      assert.throws(() => packageDataApp(state), /reviewed Data app snapshot must be valid UTF-8/u);

      assert.deepEqual(publicationBytes(state), before);
      assert.deepEqual(readFileSync(join(state.project, "src/data.json")), source);
      assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
    });
  }
});

test("rejects stale, missing, malformed, duplicated, or misplaced snapshot integrity markers", async (t) => {
  const staleSnapshot = JSON.stringify({
    queries: { reviewed: { source: { links: ["https://warehouse.example/private?sig=secret"] } } },
  });
  const staleHash = createHash("sha256").update(staleSnapshot).digest("hex");
  const cases = [
    ["stale credential-bearing HTML", reviewedHtml(staleSnapshot)
      .replace("Reviewed Data app", "https://warehouse.example/private?sig=secret")],
    ["missing marker", ({ html }) => html.replace(/<meta name="data-app-snapshot-sha256"[^>]*>/u, "")],
    ["missing head in source-built HTML", `<meta name="data-app-snapshot-sha256" content="${staleHash}">`, true],
    ["malformed marker", ({ html }) => html.replace(
      /(<meta name="data-app-snapshot-sha256" content=")[^"]*/u, "$1not-a-sha256")],
    ["duplicate markers", ({ html }) => html.replace("</head>",
      `<meta name="data-app-snapshot-sha256" content="${staleHash}"></head>`)],
  ];

  for (const [name, html, source = false] of cases) {
    await t.test(name, () => {
      const state = fixture();
      const htmlPath = join(state.project, "dist/index.html");
      const originalHtml = readFileSync(htmlPath, "utf8");
      writeFileSync(htmlPath, typeof html === "function" ? html({ html: originalHtml }) : html);
      const ownerBefore = readFileSync(join(state.project, "src/data-app-owner.js"), "utf8");
      const hostingBefore = readFileSync(join(state.project, ".openai/hosting.json"), "utf8");

      assert.throws(() => packageDataApp(state, { source }),
        /exactly one matching reviewed snapshot integrity marker/u);
      assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), ownerBefore);
      assert.equal(readFileSync(join(state.project, ".openai/hosting.json"), "utf8"), hostingBefore);
      assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
    });
  }
});

test("rejects credential-bearing source links, table metadata, and nested provenance before mutation", async (t) => {
  const reviewedJwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature";
  const excessivelyEncodedToken = Array.from({ length: 8 }).reduce(
    (encoded) => encoded.replace(/%/gu, "%25"), "%74oken",
  );
  const cases = [
    ...[
      "http://www.google.com/calendar/event?eid=reviewed",
      "https://www.google.com.example/calendar/event?eid=reviewed",
      "https://owner@www.google.com/calendar/event?eid=reviewed",
      "https://www.google.com:8443/calendar/event?eid=reviewed",
      "https://www.google.com/calendar/other?eid=reviewed",
      "https://www.google.com/calendar/event?%65id=reviewed",
      "https://www.google.com/calendar/event?eid=%72eviewed",
      "https://www.google.com/calendar/event?eid=",
      `https://www.google.com/calendar/event?eid=${"a".repeat(2049)}`,
      "https://www.google.com/calendar/event?eid=reviewed&extra=value",
      "https://www.google.com/calendar/event?eid=reviewed&eid=duplicate",
      "https://www.google.com/calendar/event?eid=reviewed#fragment",
      "https://www.google.com/calendar/event?eid=reviewed &extra=value",
      "https://www.google.com/calendar/event?eid=reviewed\n&extra=value",
    ].map((href, index) => [`unapproved Calendar URL ${index}`, { source: { links: [{ href }] } }]),
    ["signed AWS URL", { source: { links: ["https://warehouse.example/data?X-Amz-Signature=private"] } }],
    ["signed Google URL", { source: { links: ["https://warehouse.example/data?X-Goog-Signature=private"] } }],
    ["Azure SAS URL", { source: { tables: [{ name: "reviewed", href: "https://storage.example/data?sv=1&sig=private" }] } }],
    ["percent-encoded query delimiter", {
      source: { links: [{ href: "https://warehouse.example/data%3Ftoken=private" }] },
    }],
    ["percent-encoded query delimiter and assignment", {
      source: { links: [{ href: "https://warehouse.example/data%3Ftoken%3Dprivate" }] },
    }],
    ["percent-encoded fragment delimiter", {
      source: { links: [{ href: "https://warehouse.example/data%23access_token=private" }] },
    }],
    ["mixed-case percent-encoded credential delimiters", {
      source: { links: [{ href: "https://warehouse.example/data%3f%74oken%3dprivate" }] },
    }],
    ["percent-encoded credential key and query parameters", {
      source: { links: [{ href: "https://warehouse.example/data%3Fpublic%3Dok%26%74%6f%6b%65%6e%3Dprivate" }] },
    }],
    ["double-encoded credential query delimiter", {
      source: { links: [{ href: "https://warehouse.example/data%253Ftoken%253Dprivate" }] },
    }],
    ["double-encoded credential fragment delimiter", {
      source: { links: [{ href: "https://warehouse.example/data%2523access_token%253Dprivate" }] },
    }],
    ["protocol-relative URL with encoded credential query", {
      source: { links: [{ href: "//warehouse.example/data%3Ftoken%3Dprivate" }] },
    }],
    ["root-relative URL with encoded credential query", {
      source: { links: [{ href: "/data%3Ftoken%3Dprivate" }] },
    }],
    ["bare relative URL with encoded credential query", {
      source: { links: [{ href: "data%3F%74oken%3Dprivate" }] },
    }],
    ["multisegment relative URL with encoded credential fragment", {
      source: { links: [{ href: "nested/data%23authorization%3Dprivate" }] },
    }],
    ["encoded query-only relative credential URL", {
      source: { links: [{ href: "%3Fauthorization%3Dprivate" }] },
    }],
    ["encoded fragment-only relative credential URL", {
      source: { links: [{ href: "%23credential%3Dprivate" }] },
    }],
    ["protocol-relative credential URL", {
      source: { links: [{ href: "//storage.example/object?token=private" }] },
    }],
    ["root-relative credential URL", { source: { links: [{ href: "/object?token=private" }] } }],
    ["bare relative credential URL", { source: { links: [{ href: "object?token=private" }] } }],
    ["bare relative URL with encoded token key", {
      source: { links: [{ href: "object?%74oken=private" }] },
    }],
    ["bare relative URL with authorization", {
      source: { links: [{ href: "object?authorization=BearerSecret" }] },
    }],
    ["bare relative URL with cookie", { source: { links: [{ href: "object?cookie=private" }] } }],
    ["bare relative URL with credential", { source: { links: [{ href: "object?credential=private" }] } }],
    ["bare relative URL with CSRF secret", { source: { links: [{ href: "object?csrf=private" }] } }],
    ["bare relative URL with Google credential", {
      source: { links: [{ href: "object?X-Goog-Credential=private" }] },
    }],
    ["bare relative URL with access-token fragment", {
      source: { links: [{ href: "object#access_token=private" }] },
    }],
    ["multisegment relative URL with encoded token key", {
      source: { links: [{ href: "folder/object?%74oken=private" }] },
    }],
    ["multisegment relative URL with authorization", {
      source: { links: [{ href: "folder/object?authorization=BearerSecret" }] },
    }],
    ["deep relative URL with CSRF secret", {
      source: { links: [{ href: "nested/path/object?csrf=private" }] },
    }],
    ["multisegment relative URL with cookie fragment", {
      source: { links: [{ href: "folder/object#cookie=private" }] },
    }],
    ["multisegment relative credential URL in prose", {
      source: { evidenceFlow: ["Source folder/object?authorization=BearerSecret"] },
    }],
    ["query-only relative credential URL", {
      source: { links: [{ href: "?authorization=BearerSecret" }] },
    }],
    ["fragment-only relative credential URL", {
      source: { links: [{ href: "#credential=private" }] },
    }],
    ["path-embedded Java session credential", {
      source: { links: [{ href: "https://warehouse.example/object;jsessionid=private" }] },
    }],
    ["uppercase path-embedded Java session credential", {
      source: { links: [{ href: "https://warehouse.example/object;JSESSIONID=private" }] },
    }],
    ["path-embedded PHP session credential", {
      source: { links: [{ href: "https://warehouse.example/object;PHPSESSID=private" }] },
    }],
    ["relative path-embedded Java session credential", {
      source: { links: [{ href: "/object;jsessionid=private" }] },
    }],
    ["percent-encoded path-embedded Java session credential", {
      source: { links: [{ href: "/object%3Bjsessionid%3Dprivate" }] },
    }],
    ["relative path-embedded PHP session credential", {
      source: { links: [{ href: "object;PHPSESSID=private" }] },
    }],
    ["protocol-relative signed URL", {
      source: { tables: [{ metadata: { endpoint: "//storage.example/object?X-Amz-Signature=private" } }] },
    }],
    ["root-relative credential fragment", { source: { provenance: { endpoint: "/object#token=private" } } }],
    ["relative credential URL in prose", {
      source: { evidenceFlow: ["Reviewed source /object?token=private"] },
    }],
    ["URL userinfo", { source: { links: ["https://owner:private@warehouse.example/data"] } }],
    ["PostgreSQL connection URL", {
      source: { tables: [{ metadata: { endpoint: "postgresql://owner:private@warehouse.example/reviewed" } }] },
    }],
    ["MongoDB connection URL", {
      source: { provenance: { endpoint: "mongodb+srv://owner:private@warehouse.example/reviewed" } },
    }],
    ["URL fragment", { source: { links: [{ href: "https://warehouse.example/data#access_token=private" }] } }],
    ["signed URL path", { source: { links: [{ href: "https://warehouse.example/token/private" }] } }],
    ["encoded credential path", { source: { links: [{ href: "https://warehouse.example/%61ccess_token/private" }] } }],
    ["percent-encoded JWT path prefix", {
      source: { links: [{ href: `https://warehouse.example/%65${reviewedJwt.slice(1)}` }] },
    }],
    ["percent-encoded JWT path separators", {
      source: { links: [{ href: `https://warehouse.example/${reviewedJwt.replaceAll(".", "%2e")}` }] },
    }],
    ["double-encoded access-token path", {
      source: { links: [{ href: "https://warehouse.example/%2561ccess_token/private" }] },
    }],
    ["double-encoded token path", {
      source: { links: [{ href: "https://warehouse.example/%2574oken/private" }] },
    }],
    ["triple-encoded access-token path", {
      source: { links: [{ href: "https://warehouse.example/%252561ccess_token/private" }] },
    }],
    ["triple-encoded token path", {
      source: { links: [{ href: "https://warehouse.example/%252574oken/private" }] },
    }],
    ["double-encoded JWT path", {
      source: { links: [{ href: `https://warehouse.example/%2565${reviewedJwt.slice(1)}` }] },
    }],
    ["triple-encoded JWT path", {
      source: { links: [{ href: `https://warehouse.example/%252565${reviewedJwt.slice(1)}` }] },
    }],
    ["double-encoded Java session path", {
      source: { links: [{ href: "https://warehouse.example/object%253Bjsessionid%253Dprivate" }] },
    }],
    ["double-encoded PHP session path", {
      source: { links: [{ href: "https://warehouse.example/object%253BPHPSESSID%253Dprivate" }] },
    }],
    ["triple-encoded PHP session path", {
      source: { links: [{ href: "https://warehouse.example/object%25253BPHPSESSID%25253Dprivate" }] },
    }],
    ["excessively nested percent-encoded credential path", {
      source: { links: [{ href: `https://warehouse.example/${excessivelyEncodedToken}/private` }] },
    }],
    ["signature path", { source: { links: [{ href: "https://warehouse.example/x-amz-signature/private" }] } }],
    ["embedded prose URL", { source: { evidenceFlow: ["Source https://warehouse.example/data?token=private"] } }],
    ["nested access token", { source: { tables: [{ metadata: { accessToken: "private" } }] } }],
    ["nested token object", { source: { metadata: { token: { value: "private" } } } }],
    ["nested session object", { source: { metadata: { session: { id: "private" } } } }],
    ["numeric API key", { source: { metadata: { apiKey: 123456789 } } }],
    ["numeric session secret", { source: { metadata: { session: 987654321 } } }],
    ["numeric access token", { source: { metadata: { accessToken: 424242 } } }],
    ["zero-valued numeric API key", { source: { metadata: { apiKey: 0 } } }],
    ["string-valued token count", { source: { metadata: { tokenCount: "private" } } }],
    ["object-valued authentication rate", {
      source: { metadata: { authenticationRate: { value: "private" } } },
    }],
    ["nested authorization", { provenance: { upstream: [{ authorization: "Bearer private" }] } }],
    ["nested API key", { source: { tableMetadata: { headers: { api_key: "private" } } } }],
    ["connection string", { source: { tables: [{ metadata: { connectionString: "private" } }] } }],
    ["bearer value", { source: { provenance: { note: "Bearer sk-live-private" } } }],
    ["JWT value", { source: { provenance: { note: "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature" } } }],
    ["top-level provenance", { provenance: { links: ["https://warehouse.example/private?sig=secret"] } }, true],
    ["row-named metadata object", { source: { rows: { accessToken: "private" } } }],
    ["row-named provenance array", { source: { provenance: { rows: [
      { href: "https://warehouse.example/private?sig=secret" },
    ] } } }],
    ["source row-named table metadata", { source: { tables: [{ metadata: { sourceRows: [
      { accessToken: "private" },
    ] } }] } }],
  ];

  for (const [name, value, topLevel = false] of cases) {
    await t.test(name, () => {
      const state = fixture();
      const snapshotPath = join(state.project, "src/data.json");
      const snapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
      if (topLevel) Object.assign(snapshot, value);
      else Object.assign(snapshot.queries.reviewed, value);
      writeSnapshot(state, snapshot);
      const ownerBefore = readFileSync(join(state.project, "src/data-app-owner.js"), "utf8");
      const hostingBefore = readFileSync(join(state.project, ".openai/hosting.json"), "utf8");

      assert.throws(() => packageDataApp(state),
        /snapshot contains (?:embedded credentials|a credential-bearing source URL|an invalid source URL|credential metadata)/u);
      assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), ownerBefore);
      assert.equal(readFileSync(join(state.project, ".openai/hosting.json"), "utf8"), hostingBefore);
      assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
      assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
    });
  }
});

test("accepts clean nested source provenance and does not inspect reviewed row payloads", () => {
  const state = fixture();
  const snapshotPath = join(state.project, "src/data.json");
  const snapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
  snapshot.queries.reviewed.rows = [{ token: "reviewed business metric", password: "reviewed field value" }];
  snapshot.queries.reviewed.source = {
    links: [
      { href: "https://warehouse.example/reviewed", label: "Reviewed warehouse query" },
      { href: "https://www.google.com/calendar/event?eid=cmV2aWV3ZWQtZXZlbnQ", label: "Reviewed event" },
    ],
    tables: [{ name: "analytics.reviewed", metadata: { catalog: "https://catalog.example/reviewed" } }],
    provenance: { upstream: [{ note: "Reviewed event https://www.google.com:443/calendar/event?eid=cmV2aWV3ZWQtZXZlbnQ" }] },
  };

  writeSnapshot(state, snapshot);
  const snapshotBefore = readFileSync(snapshotPath);
  assert.deepEqual(JSON.parse(packageDataApp(state).trim()).queryIds, ["reviewed"]);
  assert.deepEqual(readFileSync(snapshotPath), snapshotBefore);
  assert.deepEqual(packagedConfiguration(state).seedSnapshot, snapshot);
});

test("accepts analytics query identities and numeric or boolean security-themed metrics", () => {
  const state = fixture();
  const snapshotPath = join(state.project, "src/data.json");
  const snapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
  snapshot.queries = Object.fromEntries([
    "sessions",
    "session_metrics",
    "token_usage",
    "token_counts",
    "authentication_funnel",
    "password_reset_rate",
    "signature_conversion",
  ].map((queryId) => [queryId, {
    rows: [{ token: "reviewed token usage", session: "reviewed session category" }],
    source: {
      label: "Reviewed analytics",
      metadata: {
        sessionCount: 42,
        tokenCount: 9000,
        signatureCount: 7,
        authenticationRate: 0.98,
        authenticationEnabled: true,
        hasSessionCookie: false,
      },
    },
  }]));

  writeSnapshot(state, snapshot);

  assert.deepEqual(JSON.parse(packageDataApp(state).trim()).queryIds, Object.keys(snapshot.queries));
});

test("still checks source credentials under security-themed analytics query identities", () => {
  const state = fixture();
  const snapshotPath = join(state.project, "src/data.json");
  const snapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
  snapshot.queries = {
    token_usage: {
      rows: [{ tokens: 42 }],
      source: { tables: [{ metadata: { accessToken: "private" } }] },
    },
  };
  writeSnapshot(state, snapshot);

  assert.throws(() => packageDataApp(state), /snapshot contains credential metadata/u);
});

test("rejects project IDs that cannot survive normalized protected-metadata verification", async (t) => {
  for (const projectId of ["bad project", "../other", "bad/project", "-leading", "bad.id", "bad:id", "α-project"]) {
    await t.test(projectId, () => {
      const state = fixture();
      const before = publicationBytes(state);
      assert.throws(() => packageDataApp(state, { projectId }), /Sites project ID must begin with a letter or digit/u);
      assert.deepEqual(publicationBytes(state), before);
      assert.equal(existsSync(join(state.project, ".test-runtime-verified")), false);
    });
  }
  const state = fixture();
  const output = JSON.parse(packageDataApp(state, { projectId: "appgprj_ABC-123" }).trim());
  assert.equal(output.projectId, "appgprj_ABC-123");
});

test("rejects a different Sites project, external presentation, or invalid presentation", () => {
  const mismatched = fixture();
  writeFileSync(
    join(mismatched.project, ".openai/hosting.json"),
    JSON.stringify({ project_id: "appgprj_other", d1: "DB" }),
  );
  updateFixtureProtectedManifest(mismatched, [".openai/hosting.json"]);
  assert.throws(() => packageDataApp(mismatched), /does not belong to the requested Sites project/u);

  const external = fixture();
  const outside = join(tmpdir(), `external-presentation-${process.pid}.json`);
  writeFileSync(outside, "{}");
  assert.throws(
    () =>
      packageDataApp(external, {
        presentationPath: outside,
      }),
    /inside the Data app project/u,
  );

  const invalid = fixture();
  writeFileSync(join(invalid.project, "presentation.json"), JSON.stringify({ invalid: true }));
  assert.throws(() => packageDataApp(invalid), /Presentation is invalid/u);
});

// Owner setup and presentation handoffs must work through the no-install default.
describe("current prebuilt ownership and presentation contracts", () => {
  test("migrates historical static owner seeds to one email seed", async (t) => {
    const emailHash = digest("owner@example.com");
    const userIdHash = digest("historical-site-user-id");
    for (const [name, ownerSource, preserved] of [
      ["old single user ID", `export const dataAppOwnerUserIdSha256 = "${userIdHash}";\n`, false],
      ["old dual user ID", `export const dataAppOwnerUserIdSha256 = "${userIdHash}";\n${fixtureOwnerSource()}`, false],
      ["old dual email", `export const dataAppOwnerUserIdSha256 = "";\n${fixtureOwnerSource(emailHash)}`, true],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        writeFileSync(join(state.project, "src/data-app-owner.js"), ownerSource);
        const output = JSON.parse(packageDataApp(state));
        const configuration = packagedConfiguration(state);
        assert.equal(output.ownerAuthorization, "email");
        assert.equal(output.ownerPreserved, preserved);
        assert.equal(output.ownerTransferred, !preserved);
        assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), fixtureOwnerSource(emailHash));
        assert.equal(configuration.ownerEmailSha256, emailHash);
        assert.equal(Object.hasOwn(configuration, "ownerUserIdSha256"), false);
        assert.doesNotMatch(readFileSync(join(state.project, "dist/server/index.js"), "utf8"), new RegExp(userIdHash));
      });
    }
  });

  test("rejects simultaneous email/read-only choices and retired owner modes", async (t) => {
    for (const [name, options, expected] of [
      ["both choices", { readOnly: true }, /Choose exactly one/u],
      ...["--owner-user-id", "--owner-user-id-sha256", "--legacy-owner-email-site-file", "--bootstrap-owner"].map(
        (flag) => [flag, { extra: [flag] }, /Unknown option/u],
      ),
    ]) {
      await t.test(name, () => {
        const state = fixture();
        const before = publicationBytes(state);
        assert.throws(() => packageDataApp(state, options), expected);
        assert.deepEqual(publicationBytes(state), before);
      });
    }
  });

  test("packages the Site owner's email without identity setup or owner proof", () => {
    const state = fixture();
    packageDataApp(state);
    const snapshot = readFileSync(join(state.project, "src/data.json"));
    const html = readFileSync(join(state.project, "dist/index.html"));
    const ownerEmailHash = digest("owner@example.com");

    const result = packageDataApp(state, { ownerEmail: " Owner@Example.COM " });
    const output = JSON.parse(result);
    const configuration = packagedConfiguration(state);
    assert.equal(output.ownerSeeded, true);
    assert.equal(output.ownerPreserved, true);
    assert.equal(Object.hasOwn(output, "ownerSetupRequired"), false);
    assert.equal(Object.hasOwn(configuration, "ownerUserIdSha256"), false);
    assert.equal(configuration.ownerEmailSha256, ownerEmailHash);
    assert.deepEqual(readFileSync(join(state.project, "src/data.json")), snapshot);
    assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), html);
    for (const artifact of [
      result,
      readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"),
      readFileSync(join(state.project, "dist/server/index.js"), "utf8"),
    ]) {
      assert.doesNotMatch(artifact, /owner@example\.com/iu);
    }
    verifyFixtureProtectedManifest(state);
  });

  test("rejects a malformed owner email before changing the app", async (t) => {
    for (const email of ["", "not-an-email", "owner\n@example.com", "owner@example.com\n", `${"x".repeat(243)}@example.com`]) {
      await t.test(JSON.stringify(email), () => {
        const state = fixture();
        const before = publicationBytes(state);
        assert.throws(() => packageDataApp(state, { ownerEmail: email }), /valid Site owner email/u);
        assert.deepEqual(publicationBytes(state), before);
      });
    }
  });

  test("accepts matching reviewed filter definitions without changing saved presentation or snapshot", () => {
    const state = fixture();
    const reviewedFilters = [
      {
        id: "region",
        label: "Region",
        field: "region",
        defaultValue: "all",
        options: [
          { value: "all", label: "All regions" },
          { value: "west", label: "West" },
        ],
      },
      {
        id: "week",
        label: "Week",
        field: "week",
        defaultValue: "current",
        options: [{ value: "current", label: "Current week" }],
      },
    ];
    writeSnapshot(state, {
      generatedAt: "2026-08-02T04:57:36.243Z",
      queries: { reviewed: { rows: [{ amount: 42, region: "west" }] } },
      filters: reviewedFilters,
    });
    const presentationPath = join(state.project, "presentation.json");
    const reviewedPresentation = {
      ...JSON.parse(readFileSync(presentationPath, "utf8")),
      filters: { region: "west", week: "current" },
      assumptions: { growthRate: 0.15 },
    };
    const handoffPresentation = {
      ...reviewedPresentation,
      filterDefinitions: structuredClone(reviewedFilters),
    };
    writeFileSync(presentationPath, JSON.stringify(handoffPresentation, null, 2));
    const presentationBefore = readFileSync(presentationPath);
    const snapshotBefore = readFileSync(join(state.project, "src/data.json"));
    const htmlBefore = readFileSync(join(state.project, "dist/index.html"));

    const output = JSON.parse(packageDataApp(state).trim());

    const packagedWorker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
    const seededPresentation = packagedConfiguration(state).initialPresentation;
    assert.deepEqual(
      seededPresentation,
      reviewedPresentation,
      "Only duplicate reviewed filter definitions may be removed from the persisted presentation",
    );
    assert.equal(Object.hasOwn(seededPresentation, "filterDefinitions"), false);
    assert.deepEqual(
      readFileSync(presentationPath),
      presentationBefore,
      "Packaging must preserve the original UI handoff without rewriting it",
    );
    assert.deepEqual(
      readFileSync(join(state.project, "src/data.json")),
      snapshotBefore,
      "Matching filter handoff metadata must never rewrite the reviewed snapshot",
    );
    assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), htmlBefore);
    assert.equal(output.snapshotSha256, createHash("sha256").update(snapshotBefore).digest("hex"));
  });

  for (const [name, snapshotFilters] of [
    ["missing snapshot filters", undefined],
    ["null snapshot filters", null],
    ["empty snapshot filters", []],
  ]) {
    test(`accepts empty filter handoff definitions with ${name}`, () => {
      const state = fixture();
      writeSnapshot(state, {
        queries: { reviewed: { rows: [{ amount: 42 }] } },
        ...(snapshotFilters === undefined ? {} : { filters: snapshotFilters }),
      });
      const presentationPath = join(state.project, "presentation.json");
      const reviewedPresentation = JSON.parse(readFileSync(presentationPath, "utf8"));
      writeFileSync(presentationPath, JSON.stringify({ ...reviewedPresentation, filterDefinitions: [] }));
      const snapshotBefore = readFileSync(join(state.project, "src/data.json"));

      packageDataApp(state);

      const packagedWorker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
      const seededPresentation = packagedConfiguration(state).initialPresentation;
      assert.deepEqual(seededPresentation, reviewedPresentation);
      assert.deepEqual(readFileSync(join(state.project, "src/data.json")), snapshotBefore);
    });
  }

  for (const [name, snapshotFilters, suppliedDefinitions] of [
    ["changed label", [{ id: "region", label: "Region" }], [{ id: "region", label: "Changed" }]],
    ["missing reviewed definition", [{ id: "region", label: "Region" }], []],
    ["unexpected definition", [], [{ id: "region", label: "Region" }]],
    ["reordered definitions", [{ id: "region" }, { id: "week" }], [{ id: "week" }, { id: "region" }]],
    ["null supplied definitions", [], null],
    ["object supplied definitions", [], { id: "region" }],
    ["string supplied definitions", [], "region"],
    ["malformed snapshot definitions", { id: "region" }, []],
  ]) {
    test(`rejects ${name} before mutating reviewed publication artifacts`, () => {
      const state = fixture();
      writeSnapshot(state, {
        queries: { reviewed: { rows: [{ amount: 42 }] } },
        filters: snapshotFilters,
      });
      const presentationPath = join(state.project, "presentation.json");
      writeFileSync(
        presentationPath,
        JSON.stringify({
          ...JSON.parse(readFileSync(presentationPath, "utf8")),
          filterDefinitions: suppliedDefinitions,
        }),
      );
      const snapshotBefore = readFileSync(join(state.project, "src/data.json"));
      const htmlBefore = readFileSync(join(state.project, "dist/index.html"));
      const ownerBefore = readFileSync(join(state.project, "src/data-app-owner.js"));
      const hostingBefore = readFileSync(join(state.project, ".openai/hosting.json"));
      const manifestBefore = readFileSync(join(state.project, "protected-runtime.json"));

      assert.throws(() => packageDataApp(state), /filter definitions must exactly match the reviewed/u);

      assert.deepEqual(readFileSync(join(state.project, "src/data.json")), snapshotBefore);
      assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), htmlBefore);
      assert.deepEqual(readFileSync(join(state.project, "src/data-app-owner.js")), ownerBefore);
      assert.deepEqual(readFileSync(join(state.project, ".openai/hosting.json")), hostingBefore);
      assert.deepEqual(readFileSync(join(state.project, "protected-runtime.json")), manifestBefore);
      assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
      assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
    });
  }

  test("matching filter handoff metadata does not bypass strict presentation field validation", () => {
    const state = fixture();
    const presentationPath = join(state.project, "presentation.json");
    writeFileSync(
      presentationPath,
      JSON.stringify({
        ...JSON.parse(readFileSync(presentationPath, "utf8")),
        filterDefinitions: [],
        unreviewedPresentationField: "not allowed",
      }),
    );
    const ownerBefore = readFileSync(join(state.project, "src/data-app-owner.js"));
    const hostingBefore = readFileSync(join(state.project, ".openai/hosting.json"));

    assert.throws(() => packageDataApp(state), /Unsupported presentation fields: unreviewedPresentationField/u);

    assert.deepEqual(readFileSync(join(state.project, "src/data-app-owner.js")), ownerBefore);
    assert.deepEqual(readFileSync(join(state.project, ".openai/hosting.json")), hostingBefore);
    assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
  });

  test("never seeds locally fabricated verification while preserving every other presentation field", () => {
    const state = fixture();
    const presentationPath = join(state.project, "presentation.json");
    const reviewedPresentation = JSON.parse(readFileSync(presentationPath, "utf8"));
    const fabricatedVerification = {
      verifiedBy: "fabricated-verifier@example.com",
      verifiedAt: "2001-02-03T04:05:06.789Z",
    };
    const requestedPresentation = { ...reviewedPresentation, verification: fabricatedVerification };
    writeFileSync(presentationPath, JSON.stringify(requestedPresentation));

    packageDataApp(state);

    const packagedWorker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
    const seededPresentation = packagedConfiguration(state).initialPresentation;
    assert.deepEqual(
      seededPresentation,
      reviewedPresentation,
      "Packaging must retain all legitimate presentation state without trusting a local verification claim",
    );
    assert.equal(Object.hasOwn(seededPresentation, "verification"), false);
    assert.doesNotMatch(
      packagedWorker,
      /fabricated-verifier@example\.com|2001-02-03T04:05:06\.789Z/u,
      "Neither an untrusted verifier identity nor its timestamp may reach the published Worker",
    );
    assert.deepEqual(
      JSON.parse(readFileSync(presentationPath, "utf8")),
      requestedPresentation,
      "Filtering the deployed seed must not destroy the creator's existing local presentation",
    );
  });

  test("verified-dashboard publication still rejects signed provenance before owner or verification seeding", () => {
    const state = fixture();
    writeSnapshot(state, {
      queries: {
        reviewed: {
          rows: [{ amount: 42 }],
          source: { links: ["https://warehouse.example/reviewed%3Faccess_token=private"] },
        },
      },
    });
    const presentationPath = join(state.project, "presentation.json");
    writeFileSync(
      presentationPath,
      JSON.stringify({
        ...JSON.parse(readFileSync(presentationPath, "utf8")),
        verification: {
          verifiedBy: "fabricated-verifier@example.com",
          verifiedAt: "2001-02-03T04:05:06.789Z",
        },
      }),
    );
    const ownerBefore = readFileSync(join(state.project, "src/data-app-owner.js"));
    const hostingBefore = readFileSync(join(state.project, ".openai/hosting.json"));

    assert.throws(() => packageDataApp(state), /embedded credentials/u);
    assert.deepEqual(readFileSync(join(state.project, "src/data-app-owner.js")), ownerBefore);
    assert.deepEqual(readFileSync(join(state.project, ".openai/hosting.json")), hostingBefore);
    assert.equal(
      existsSync(join(state.project, "dist/server/index.js")),
      false,
      "Dashboard verification must never bypass reviewed-source credential rejection",
    );
  });

  test("an unverified Site owner cannot seed fabricated dashboard verification in a read-only deployment", () => {
    const state = fixture();
    const presentationPath = join(state.project, "presentation.json");
    writeFileSync(
      presentationPath,
      JSON.stringify({
        ...JSON.parse(readFileSync(presentationPath, "utf8")),
        verification: {
          verifiedBy: "fabricated-verifier@example.com",
          verifiedAt: "2001-02-03T04:05:06.789Z",
        },
      }),
    );

    const output = JSON.parse(packageDataApp(state, { ownerEmail: null, readOnly: true }).trim());
    const packagedWorker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
    const initialPresentation = packagedConfiguration(state).initialPresentation;

    assert.equal(output.ownerSeeded, false);
    assert.equal(Object.hasOwn(initialPresentation, "verification"), false);
    assert.doesNotMatch(packagedWorker, /fabricated-verifier@example\.com|2001-02-03T04:05:06\.789Z/u);
  });

  test("never silently publishes read-only when the owner setup mode is missing", async (t) => {
    for (const [name, existingOwner] of [
      ["new unseeded app", null],
      ["previously seeded app", "previous-site-owner"],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        const ownerPath = join(state.project, "src/data-app-owner.js");
        const hostingPath = join(state.project, ".openai/hosting.json");
        const htmlPath = join(state.project, "dist/index.html");
        const workerPath = join(state.project, "dist/server/index.js");
        if (existingOwner) {
          const existingOwnerHash = createHash("sha256").update(existingOwner).digest("hex");
          writeFileSync(ownerPath, fixtureOwnerSource(existingOwnerHash));
          updateFixtureProtectedManifest(state, ["src/data-app-owner.js"]);
        }
        writeFileSync(
          htmlPath,
          readFileSync(htmlPath, "utf8").replace(
            "</head>",
            '<meta name="data-app-local-thread" content="550e8400-e29b-41d4-a716-446655440000"></head>',
          ),
        );
        mkdirSync(join(state.project, "dist/server"), { recursive: true });
        writeFileSync(workerPath, "// previously deployed reviewed Worker\n");
        const originalOwner = readFileSync(ownerPath);
        const originalHosting = readFileSync(hostingPath);
        const originalHtml = readFileSync(htmlPath);
        const originalWorker = readFileSync(workerPath);

        assert.throws(
          () => packageDataApp(state, { ownerEmail: null }),
          /Choose exactly one/u,
        );
        assert.deepEqual(readFileSync(ownerPath), originalOwner);
        assert.deepEqual(readFileSync(hostingPath), originalHosting);
        assert.deepEqual(readFileSync(htmlPath), originalHtml);
        assert.deepEqual(readFileSync(workerPath), originalWorker);
        assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
        assert.equal(existsSync(join(state.project, "dist/.openai/hosting.json")), false);
      });
    }
  });

  test("email seeding and republication retain protected-runtime integrity", () => {
    const state = fixture();
    const reviewedSnapshot = readFileSync(join(state.project, "src/data.json"));
    const reviewedHtmlBefore = readFileSync(join(state.project, "dist/index.html"));
    const originalManifest = JSON.parse(readFileSync(join(state.project, "protected-runtime.json"), "utf8"));
    const ownerEmail = "verified-owner@example.com";

    const readOnly = JSON.parse(
      packageDataApp(state, {
        ownerEmail: null,
        readOnly: true,
      }).trim(),
    );
    assert.equal(readOnly.ownerSeeded, false);
    verifyFixtureProtectedManifest(state);

    const seeded = JSON.parse(
      packageDataApp(state, {
        ownerEmail,
      }).trim(),
    );
    assert.equal(seeded.ownerSeeded, true);
    verifyFixtureProtectedManifest(state);
    assert.doesNotThrow(
      () =>
        execFileSync(process.execPath, [join(state.project, "scripts/verify-protected-runtime.mjs")], {
          cwd: state.project,
          encoding: "utf8",
          stdio: ["ignore", "pipe", "pipe"],
        }),
      "An ordinarily rebuilt published app must pass its protected-runtime verification",
    );

    const republished = JSON.parse(
      packageDataApp(state, {
        ownerEmail,
      }).trim(),
    );
    assert.equal(republished.ownerPreserved, true);
    assert.equal(republished.ownerTransferred, false);
    assert.deepEqual(JSON.parse(readFileSync(join(state.project, ".openai/hosting.json"), "utf8")), {
      d1: "DB",
      r2: null,
      project_id: "appgprj_reviewed",
    });
    assert.deepEqual(readFileSync(join(state.project, "src/data.json")), reviewedSnapshot);
    assert.deepEqual(readFileSync(join(state.project, "dist/index.html")), reviewedHtmlBefore);
    const finalManifest = JSON.parse(readFileSync(join(state.project, "protected-runtime.json"), "utf8"));
    for (const [path, expectedHash] of Object.entries(originalManifest.files)) {
      if (path === ".openai/hosting.json" || path === "src/data-app-owner.js") continue;
      assert.equal(finalManifest.files[path], expectedHash);
    }
    verifyFixtureProtectedManifest(state);
  });

  test("publishes a new Data app read-only only when read-only mode is explicitly selected", () => {
    const state = fixture();
    const output = JSON.parse(packageDataApp(state, { ownerEmail: null, readOnly: true }).trim());

    assert.equal(output.ownerAuthorization, "none");
    assert.equal(output.ownerSeeded, false);
    assert.equal(output.ownerPreserved, false);
    assert.equal(output.ownerTransferred, false);
    assert.equal(output.ownerRevoked, false);
    assert.equal(Object.hasOwn(output, "ownerSetupRequired"), false);
    assert.equal(readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"), fixtureOwnerSource());
    assert.equal(existsSync(join(state.project, "dist/server/index.js")), true);
  });
});

describe("source integrity and independent publication rollback", () => {
  test("requires protected verifier and existing digest-helper entries before executing source tools", async (t) => {
    for (const [name, omittedPath, linkedHelper, expected] of [
      [
        "omitted regular digest helper",
        "scripts/protected-file-digest.mjs",
        false,
        /must protect its existing digest helper before any source verification/u,
      ],
      [
        "omitted symlinked digest helper",
        "scripts/protected-file-digest.mjs",
        true,
        /must protect its existing digest helper before any source verification/u,
      ],
      [
        "omitted source verifier",
        "scripts/verify-protected-runtime.mjs",
        false,
        /manifest does not protect scripts\/verify-protected-runtime\.mjs/u,
      ],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        packageDataApp(state);
        const digestHelperPath = join(state.project, "scripts/protected-file-digest.mjs");
        const helperProbe = join(state.project, ".test-digest-helper-executed");
        const helperSource =
          `${readFileSync(digestHelperPath, "utf8")}\n` +
          'import { writeFileSync as recordHelperProbe } from "node:fs";\n' +
          `recordHelperProbe(${JSON.stringify(helperProbe)}, "yes");\n`;
        if (linkedHelper) {
          const target = join(mkdtempSync(join(tmpdir(), "data-app-external-digest-")), "digest.mjs");
          writeFileSync(target, helperSource);
          rmSync(digestHelperPath);
          symlinkSync(target, digestHelperPath);
        } else {
          writeFileSync(digestHelperPath, helperSource);
        }
        const verifierPath = join(state.project, "scripts/verify-protected-runtime.mjs");
        writeFileSync(
          verifierPath,
          'import { writeFileSync as recordVerifierProbe } from "node:fs";\n' +
            'recordVerifierProbe(".test-source-verifier-entered", "yes");\n' +
            readFileSync(verifierPath, "utf8"),
        );
        updateFixtureProtectedManifest(state, [
          "scripts/protected-file-digest.mjs",
          "scripts/verify-protected-runtime.mjs",
        ]);
        const manifestPath = join(state.project, "protected-runtime.json");
        const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
        delete manifest.files[omittedPath];
        writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
        writeFileSync(
          join(state.project, ".openai/hosting.json"),
          JSON.stringify({
            d1: "DB",
            r2: null,
            project_id: "appgprj_reviewed",
          }),
        );
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              source: true,
              migratePackagingManifest: true,
            }),
          expected,
        );
        assert.deepEqual(publicationBytes(state), before);
        for (const path of [
          ".test-digest-helper-executed",
          ".test-source-verifier-entered",
          ".test-source-verified",
          ".test-vite-arguments.json",
          "src/.sites-worker-entry.mjs",
        ]) {
          assert.equal(existsSync(join(state.project, path)), false, `${path} must not be created`);
        }
      });
    }
  });

  test("temporary legacy manifest repair restores the exact original before a verifier or build failure", async (t) => {
    for (const [name, verifierFails] of [
      ["verifier failure", true],
      ["later source build failure", false],
    ]) {
      await t.test(name, () => {
        const state = legacyFixture();
        packageDataApp(state);
        const verifierPath = join(state.project, "scripts/verify-protected-runtime.mjs");
        writeFileSync(
          verifierPath,
          `${readFileSync(verifierPath, "utf8")}\n` +
            'writeFileSync(".test-manifest-during-verification.json", JSON.stringify(manifest));\n' +
            (verifierFails ? "process.exit(17);\n" : ""),
        );
        updateFixtureProtectedManifest(state, ["scripts/verify-protected-runtime.mjs"]);
        writeFileSync(
          join(state.project, ".openai/hosting.json"),
          JSON.stringify({
            d1: "DB",
            r2: null,
            project_id: "appgprj_reviewed",
            existingDeployment: "preserved",
          }),
        );
        writeFileSync(
          join(state.project, "src/data-app-owner.js"),
          fixtureOwnerSource(digest("previous-verified-owner")),
        );
        const manifestPath = join(state.project, "protected-runtime.json");
        const originalManifest = readFileSync(manifestPath);
        const prospectiveManifest = JSON.parse(originalManifest);
        for (const path of [".openai/hosting.json", "src/data-app-owner.js"]) {
          prospectiveManifest.files[path] = digest(readFileSync(join(state.project, path)));
        }
        rmSync(join(state.project, ".test-vite-arguments.json"), { force: true });
        if (!verifierFails) {
          const vitePath = join(state.project, "node_modules/vite/bin/vite.js");
          writeFileSync(
            vitePath,
            `${readFileSync(vitePath, "utf8")}\n` +
              'writeFileSync(join(process.cwd(), ".test-manifest-during-build.json"), ' +
              'readFileSync(join(process.cwd(), "protected-runtime.json")));\n' +
              "process.exit(23);\n",
          );
        }
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              ownerEmail: null,
              readOnly: true,
              migratePackagingManifest: true,
            }),
          verifierFails
            ? /Protected Data app source verification failed with status 17/u
            : /Sites Worker packaging failed with status 23/u,
        );
        assert.deepEqual(
          JSON.parse(readFileSync(join(state.project, ".test-manifest-during-verification.json"), "utf8")),
          prospectiveManifest,
          "Only the two packaging-owned hashes may be repaired for verification",
        );
        if (verifierFails) {
          assert.equal(existsSync(join(state.project, ".test-vite-arguments.json")), false);
        } else {
          assert.deepEqual(
            readFileSync(join(state.project, ".test-manifest-during-build.json")),
            originalManifest,
            "The source build must observe the original manifest, not a temporary authorization repair",
          );
        }
        assert.deepEqual(publicationBytes(state), before);
        assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
      });
    }
  });

  test("legacy migration rejects executable Unicode-comment suffixes and fake owner exports before tools run", async (t) => {
    const ownerHash = digest("previous-verified-owner");
    const realExport = fixtureOwnerSource(ownerHash);
    for (const [name, source] of [
      ["line separator ends a line comment", `${realExport}// harmless\u2028globalThis.ownerSideEffect = true;\n`],
      ["paragraph separator ends a line comment", `${realExport}// harmless\u2029globalThis.ownerSideEffect = true;\n`],
      ["line-commented fake export", `// ${realExport}`],
      ["block-commented fake export", `/* ${realExport} */\n`],
      ["duplicate owner export", `${realExport}${realExport}`],
    ]) {
      await t.test(name, () => {
        const state = legacyFixture();
        packageDataApp(state);
        rmSync(join(state.project, ".test-source-verified"), { force: true });
        rmSync(join(state.project, ".test-vite-arguments.json"), { force: true });
        writeFileSync(
          join(state.project, ".openai/hosting.json"),
          JSON.stringify({
            d1: "DB",
            r2: null,
            project_id: "appgprj_reviewed",
          }),
        );
        writeFileSync(join(state.project, "src/data-app-owner.js"), source);
        const before = publicationBytes(state);

        assert.throws(
          () =>
            packageDataApp(state, {
              ownerEmail: null,
              readOnly: true,
              migratePackagingManifest: true,
            }),
          /requires an unmodified Data app owner module shape/u,
        );
        assert.deepEqual(publicationBytes(state), before);
        for (const path of [".test-source-verified", ".test-vite-arguments.json", "src/.sites-worker-entry.mjs"]) {
          assert.equal(existsSync(join(state.project, path)), false, `${path} must not be created`);
        }
      });
    }
  });

  test("legacy owner migration rewrites only real export values while preserving comment examples", () => {
    const state = legacyFixture();
    const previousHash = digest("previous-verified-owner");
    const nextEmail = "new-verified-owner@example.com";
    const nextHash = digest(nextEmail);
    const comment = `/* Example: ${fixtureOwnerSource(previousHash).trim()} */\n`;
    writeFileSync(
      join(state.project, ".openai/hosting.json"),
      JSON.stringify({
        d1: "DB",
        r2: null,
        project_id: "appgprj_reviewed",
      }),
    );
    writeFileSync(
      join(state.project, "src/data-app-owner.js"),
      `${comment}${fixtureOwnerSource(previousHash)}`,
    );

    const output = JSON.parse(
      packageDataApp(state, {
        ownerEmail: nextEmail,
        migratePackagingManifest: true,
      }),
    );
    assert.equal(output.ownerTransferred, true);
    assert.equal(
      readFileSync(join(state.project, "src/data-app-owner.js"), "utf8"),
      `${comment}${fixtureOwnerSource(nextHash)}`,
    );
    verifyFixtureProtectedManifest(state);
  });

  test("a failed final manifest write restores other artifacts even if Worker restoration also fails", async (t) => {
    for (const failServerRestore of [false, true]) {
      await t.test(failServerRestore ? "independent restoration after a second failure" : "complete rollback", () => {
        const state = fixture();
        packageDataApp(state);
        const htmlPath = join(state.project, "dist/index.html");
        writeFileSync(
          htmlPath,
          readFileSync(htmlPath, "utf8").replace(
            "</head>",
            '<meta name="data-app-local-thread" content="550e8400-e29b-41d4-a716-446655440000"></head>',
          ),
        );
        const before = publicationBytes(state);
        const injectionDirectory = mkdtempSync(join(tmpdir(), "data-app-write-failure-"));
        const preloadPath = join(injectionDirectory, "inject-write-failure.cjs");
        const logPath = join(injectionDirectory, "restoration-attempts.json");
        const manifestPath = join(state.project, "protected-runtime.json");
        const serverPath = join(state.project, "dist/server/index.js");
        writeFileSync(
          preloadPath,
          [
            'const fs = require("node:fs");',
            "const originalWrite = fs.writeFileSync;",
            `const manifestPath = ${JSON.stringify(manifestPath)};`,
            `const serverPath = ${JSON.stringify(serverPath)};`,
            `const logPath = ${JSON.stringify(logPath)};`,
            `const failServerRestore = ${JSON.stringify(failServerRestore)};`,
            "const attempts = [];",
            "let manifestFailed = false;",
            "fs.writeFileSync = function (file, ...args) {",
            "  const path = String(file);",
            "  if (path === manifestPath && !manifestFailed) {",
            "    manifestFailed = true;",
            '    originalWrite.call(fs, file, "partially written manifest");',
            '    throw new Error("Injected final manifest write failure");',
            "  }",
            "  if (manifestFailed) {",
            "    attempts.push(path);",
            "    originalWrite.call(fs, logPath, JSON.stringify(attempts));",
            "    if (failServerRestore && path === serverPath)",
            '      throw new Error("Injected Worker restore failure");',
            "  }",
            "  return originalWrite.call(this, file, ...args);",
            "};",
            'require("node:module").syncBuiltinESMExports();',
          ].join("\n"),
        );

        assert.throws(
          () =>
            packageDataApp(state, {
              ownerEmail: "new-verified-owner@example.com",
              environment: {
                ...process.env,
                NODE_OPTIONS: `${process.env.NODE_OPTIONS ?? ""} --require=${JSON.stringify(preloadPath)}`.trim(),
              },
            }),
          (error) => {
            assert.match(error.stderr, /Injected final manifest write failure/u);
            if (failServerRestore) {
              assert.match(
                error.stderr,
                /AggregateError: Sites packaging failed and some prior artifacts could not be restored/u,
              );
              assert.match(error.stderr, /Injected Worker restore failure/u);
            }
            return true;
          },
        );
        assert.deepEqual(JSON.parse(readFileSync(logPath, "utf8")), [
          manifestPath,
          serverPath,
          join(state.project, "src/data-app-owner.js"),
          join(state.project, ".openai/hosting.json"),
          join(state.project, "dist/.openai/hosting.json"),
          htmlPath,
        ]);
        const after = publicationBytes(state);
        for (const [index, path] of publicationPaths.entries()) {
          if (failServerRestore && path === "dist/server/index.js") {
            assert.notDeepEqual(
              after[index],
              before[index],
              "The injected Worker restoration failure must actually fire",
            );
          } else {
            assert.deepEqual(after[index], before[index], `${path} must be restored independently`);
          }
        }
        assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
      });
    }
  });
});
