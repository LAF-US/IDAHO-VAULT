import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import test, { describe } from "node:test";

import {
  legacyFixture,
  fixtureOwnerSource,
  fixtureWorkerSource,
  packageDataApp,
  updateFixtureProtectedManifest,
  verifyFixtureProtectedManifest,
} from "./data-app-sites-package-fixtures.mjs";

// Older deployed apps keep their authorized source and raw manifest semantics.
describe("explicit legacy source compatibility", () => {
  const fixture = legacyFixture;

  test("existing monolithic source can revoke editing but cannot silently gain email authorization", () => {
    const state = fixture();
    const ownerPath = join(state.project, "src/data-app-owner.js");
    const workerPath = join(state.project, "src/worker.js");
    const oldHash = createHash("sha256").update("historical-user-id").digest("hex");
    writeFileSync(ownerPath, `export const dataAppOwnerUserIdSha256 = "${oldHash}";\n`);
    const oldWorker = [
      'import { dataAppOwnerUserIdSha256 } from "./data-app-owner.js";',
      'const id = "current";',
      'const store = (database) => database.prepare("presentation").bind(id, "{}", 0, new Date().toISOString()).run();',
      'export default { fetch() { return new Response("ok"); } };',
    ].join("\n");
    writeFileSync(workerPath, oldWorker);
    updateFixtureProtectedManifest(state);
    assert.throws(() => packageDataApp(state), /requires a confirmed, scoped protected runtime upgrade/u);
    assert.equal(readFileSync(ownerPath, "utf8"), `export const dataAppOwnerUserIdSha256 = "${oldHash}";\n`);
    assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);

    const output = JSON.parse(packageDataApp(state, { ownerEmail: null, readOnly: true }));
    assert.equal(output.ownerAuthorization, "none");
    assert.equal(output.ownerRevoked, true);
    assert.equal(readFileSync(workerPath, "utf8"), oldWorker);
    assert.equal(readFileSync(ownerPath, "utf8"), 'export const dataAppOwnerUserIdSha256 = "";\n');
    assert.doesNotMatch(readFileSync(join(state.project, "dist/server/index.js"), "utf8"), new RegExp(oldHash));
    verifyFixtureProtectedManifest(state);
  });

  test("an approved old dual factory uses only email and retains its reviewed source", () => {
    const state = fixture();
    const ownerPath = join(state.project, "src/data-app-owner.js");
    const workerPath = join(state.project, "src/worker.js");
    writeFileSync(ownerPath, 'export const dataAppOwnerUserIdSha256 = "";\n' + fixtureOwnerSource());
    const oldWorker = fixtureWorkerSource.replace(
      'import { dataAppOwnerEmailSha256 }',
      'import { dataAppOwnerUserIdSha256, dataAppOwnerEmailSha256 }',
    ).replace('  ownerEmailSha256:', '  ownerUserIdSha256: dataAppOwnerUserIdSha256,\n  ownerEmailSha256:');
    writeFileSync(workerPath, oldWorker);
    updateFixtureProtectedManifest(state);

    const output = JSON.parse(packageDataApp(state));
    assert.equal(output.ownerAuthorization, "email");
    assert.equal(readFileSync(workerPath, "utf8"), oldWorker);
    const worker = readFileSync(join(state.project, "dist/server/index.js"), "utf8");
    assert.match(worker, /const dataAppOwnerUserIdSha256 = "";/u);
    assert.match(worker, new RegExp(createHash("sha256").update("owner@example.com").digest("hex")));
    verifyFixtureProtectedManifest(state);
  });

  test("legacy packaged projects require explicit, narrowly scoped hosting and owner manifest migration", async (t) => {
    for (const [name, stalePaths] of [
      ["stale hosting and owner entries", [".openai/hosting.json", "src/data-app-owner.js"]],
      ["stale hosting entry only", [".openai/hosting.json"]],
      ["stale owner entry only", ["src/data-app-owner.js"]],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        const ownerEmail = "previous-owner@example.com";
        const ownerHash = createHash("sha256").update(ownerEmail).digest("hex");
        const ownerPath = join(state.project, "src/data-app-owner.js");
        const hostingPath = join(state.project, ".openai/hosting.json");
        const manifestPath = join(state.project, "protected-runtime.json");
        writeFileSync(
          hostingPath,
          JSON.stringify({
            d1: "DB",
            r2: null,
            project_id: "appgprj_reviewed",
            existingDeployment: "preserved",
          }),
        );
        writeFileSync(ownerPath, `// Verified prior owner\n${fixtureOwnerSource(ownerHash)}`);
        for (const path of [".openai/hosting.json", "src/data-app-owner.js"]) {
          if (!stalePaths.includes(path)) updateFixtureProtectedManifest(state, [path]);
        }
        const originalManifest = JSON.parse(readFileSync(manifestPath, "utf8"));
        const originalOwner = readFileSync(ownerPath);
        const originalHosting = readFileSync(hostingPath);

        assert.throws(
          () =>
            packageDataApp(state, {
              ownerEmail,
            }),
          /out of sync.*--migrate-packaging-manifest/u,
        );
        assert.deepEqual(readFileSync(ownerPath), originalOwner);
        assert.deepEqual(readFileSync(hostingPath), originalHosting);
        assert.deepEqual(JSON.parse(readFileSync(manifestPath, "utf8")), originalManifest);

        const output = JSON.parse(
          packageDataApp(state, {
            ownerEmail,
            migratePackagingManifest: true,
          }).trim(),
        );

        assert.equal(output.ownerPreserved, true);
        assert.equal(output.ownerSeeded, true);
        assert.equal(output.databaseBinding, "DB");
        assert.deepEqual(JSON.parse(readFileSync(hostingPath, "utf8")), {
          d1: "DB",
          r2: null,
          project_id: "appgprj_reviewed",
          existingDeployment: "preserved",
        });
        const migratedManifest = JSON.parse(readFileSync(manifestPath, "utf8"));
        for (const [path, expectedHash] of Object.entries(originalManifest.files)) {
          if (path === ".openai/hosting.json" || path === "src/data-app-owner.js") continue;
          assert.equal(
            migratedManifest.files[path],
            expectedHash,
            `Legacy packaging migration must never authorize ${path}`,
          );
        }
        verifyFixtureProtectedManifest(state);
        assert.doesNotThrow(
          () =>
            packageDataApp(state, {
              ownerEmail,
            }),
          "One-time packaging migration must leave ordinary republication available",
        );
        verifyFixtureProtectedManifest(state);
      });
    }
  });

  test("manifest migration rejects unrelated runtime tampering even when packaging-owned entries are stale", () => {
    const state = fixture();
    const ownerPath = join(state.project, "src/data-app-owner.js");
    const hostingPath = join(state.project, ".openai/hosting.json");
    const workerPath = join(state.project, "src/worker.js");
    const manifestPath = join(state.project, "protected-runtime.json");
    const previousOwnerHash = createHash("sha256").update("previous-verified-owner").digest("hex");
    writeFileSync(hostingPath, JSON.stringify({ d1: "DB", r2: null, project_id: "appgprj_reviewed" }));
    writeFileSync(ownerPath, fixtureOwnerSource(previousOwnerHash));
    writeFileSync(workerPath, `${readFileSync(workerPath, "utf8")}\n// unauthorized protected change\n`);
    const originalOwner = readFileSync(ownerPath);
    const originalHosting = readFileSync(hostingPath);
    const originalWorker = readFileSync(workerPath);
    const originalManifest = readFileSync(manifestPath);

    assert.throws(
      () =>
        packageDataApp(state, {
          ownerEmail: null,
          readOnly: true,
          migratePackagingManifest: true,
        }),
      /runtime files were modified outside packaging ownership: src\/worker\.js/u,
    );
    assert.deepEqual(readFileSync(ownerPath), originalOwner);
    assert.deepEqual(readFileSync(hostingPath), originalHosting);
    assert.deepEqual(readFileSync(workerPath), originalWorker);
    assert.deepEqual(readFileSync(manifestPath), originalManifest);
    assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
  });

  test("manifest migration rejects missing legacy mismatches, wrong project, wrong DB, and unsafe owner modules", async (t) => {
    const ownerEmail = "previous-owner@example.com";
    const ownerHash = createHash("sha256").update(ownerEmail).digest("hex");
    for (const [name, prepare, expected] of [
      ["no stale packaging entries", () => {}, /requires existing legacy hosting or owner hash mismatches/u],
      [
        "missing existing project identity",
        ({ project }) => {
          writeFileSync(join(project, ".openai/hosting.json"), JSON.stringify({ d1: "DB", r2: null }));
        },
        /requires the existing exact Sites project identity and DB binding/u,
      ],
      [
        "different existing project identity",
        ({ project }) => {
          writeFileSync(
            join(project, ".openai/hosting.json"),
            JSON.stringify({ d1: "DB", project_id: "appgprj_different" }),
          );
        },
        /does not belong to the requested Sites project/u,
      ],
      [
        "different database binding",
        ({ project }) => {
          writeFileSync(
            join(project, ".openai/hosting.json"),
            JSON.stringify({ d1: "OTHER_DB", project_id: "appgprj_reviewed" }),
          );
        },
        /requires the existing exact Sites project identity and DB binding/u,
      ],
      [
        "owner module with executable additions",
        ({ project }) => {
          writeFileSync(
            join(project, ".openai/hosting.json"),
            JSON.stringify({ d1: "DB", project_id: "appgprj_reviewed" }),
          );
          writeFileSync(
            join(project, "src/data-app-owner.js"),
            `export const dataAppOwnerUserIdSha256 = "${ownerHash}";\nconsole.log("unexpected");\n`,
          );
        },
        /requires an unmodified Data app owner module shape/u,
      ],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        prepare(state);
        const manifestPath = join(state.project, "protected-runtime.json");
        const ownerPath = join(state.project, "src/data-app-owner.js");
        const hostingPath = join(state.project, ".openai/hosting.json");
        const originalManifest = readFileSync(manifestPath);
        const originalOwner = readFileSync(ownerPath);
        const originalHosting = readFileSync(hostingPath);

        assert.throws(
          () =>
            packageDataApp(state, {
              ownerEmail: null,
              readOnly: true,
              migratePackagingManifest: true,
            }),
          expected,
        );
        assert.deepEqual(readFileSync(manifestPath), originalManifest);
        assert.deepEqual(readFileSync(ownerPath), originalOwner);
        assert.deepEqual(readFileSync(hostingPath), originalHosting);
        assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
      });
    }
  });

  test("failed legacy packaging migration restores the original manifest and previously deployed artifacts", () => {
    const state = fixture();
    const ownerPath = join(state.project, "src/data-app-owner.js");
    const hostingPath = join(state.project, ".openai/hosting.json");
    const manifestPath = join(state.project, "protected-runtime.json");
    const publishedWorkerPath = join(state.project, "dist/server/index.js");
    const previousOwnerHash = createHash("sha256").update("previous-verified-owner").digest("hex");
    writeFileSync(hostingPath, JSON.stringify({ d1: "DB", r2: null, project_id: "appgprj_reviewed" }));
    writeFileSync(ownerPath, fixtureOwnerSource(previousOwnerHash));
    mkdirSync(join(state.project, "dist/server"), { recursive: true });
    writeFileSync(publishedWorkerPath, "// previously deployed reviewed Worker\n");
    const vitePath = join(state.project, "node_modules/vite/bin/vite.js");
    writeFileSync(vitePath, `${readFileSync(vitePath, "utf8")}\nprocess.exit(23);\n`);
    const originalManifest = readFileSync(manifestPath);
    const originalOwner = readFileSync(ownerPath);
    const originalHosting = readFileSync(hostingPath);
    const originalWorker = readFileSync(publishedWorkerPath);

    assert.throws(
      () =>
        packageDataApp(state, {
          ownerEmail: null,
          readOnly: true,
          migratePackagingManifest: true,
        }),
      /Sites Worker packaging failed with status 23/u,
    );
    assert.deepEqual(
      readFileSync(manifestPath),
      originalManifest,
      "Failed one-time migration must restore the exact preexisting protected manifest",
    );
    assert.deepEqual(readFileSync(ownerPath), originalOwner);
    assert.deepEqual(readFileSync(hostingPath), originalHosting);
    assert.deepEqual(readFileSync(publishedWorkerPath), originalWorker);
    assert.equal(existsSync(join(state.project, "dist/.openai/hosting.json")), false);
    assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
  });

  test("rejects malformed dual-runtime owner digests and simultaneous active authorization seeds", async (t) => {
    const validOwnerHash = createHash("sha256").update("verified-owner").digest("hex");
    for (const [name, userIdHash, emailHash, expected] of [
      ["malformed Site-scoped ID digest", "abc", "", /existing Data app owner seed is invalid/u],
      ["malformed legacy-email digest", "", "abc", /existing Data app owner seed is invalid/u],
      [
        "both active authorization digests",
        validOwnerHash,
        validOwnerHash,
        /must not contain multiple active owner authorization seeds/u,
      ],
    ]) {
      await t.test(name, () => {
        const state = fixture();
        const ownerPath = join(state.project, "src/data-app-owner.js");
        writeFileSync(
          ownerPath,
          `export const dataAppOwnerUserIdSha256 = "${userIdHash}";\n` +
            `export const dataAppOwnerEmailSha256 = "${emailHash}";\n`,
        );
        updateFixtureProtectedManifest(state, ["src/data-app-owner.js"]);
        const originalOwner = readFileSync(ownerPath);
        const originalHosting = readFileSync(join(state.project, ".openai/hosting.json"));
        const originalManifest = readFileSync(join(state.project, "protected-runtime.json"));

        assert.throws(() => packageDataApp(state), expected);
        assert.deepEqual(readFileSync(ownerPath), originalOwner);
        assert.deepEqual(readFileSync(join(state.project, ".openai/hosting.json")), originalHosting);
        assert.deepEqual(readFileSync(join(state.project, "protected-runtime.json")), originalManifest);
        assert.equal(existsSync(join(state.project, "dist/server/index.js")), false);
      });
    }
  });

  test("failed legacy source owner transfer restores all previously published artifacts", () => {
    const state = fixture();
    const threadId = "550e8400-e29b-41d4-a716-446655440000";
    packageDataApp(state);
    const htmlPath = join(state.project, "dist/index.html");
    writeFileSync(
      htmlPath,
      readFileSync(htmlPath, "utf8").replace(
        "</head>",
        `<meta name="data-app-local-thread" content="${threadId}"></head>`,
      ),
    );
    const vitePath = join(state.project, "node_modules/vite/bin/vite.js");
    writeFileSync(vitePath, `${readFileSync(vitePath, "utf8")}\nprocess.exit(23);\n`);
    const originalArtifacts = Object.fromEntries(
      [
        "src/data-app-owner.js",
        ".openai/hosting.json",
        "protected-runtime.json",
        "dist/index.html",
        "dist/server/index.js",
        "dist/.openai/hosting.json",
        "src/data.json",
      ].map((path) => [path, readFileSync(join(state.project, path))]),
    );

    assert.throws(
      () =>
        packageDataApp(state, {
          ownerEmail: "new-owner@example.com",
          environment: { ...process.env, CODEX_SESSION_ID: threadId },
        }),
      (error) => {
        assert.match(error.stderr, /Sites Worker packaging failed with status 23/u);
        assert.doesNotMatch(`${error.stdout}\n${error.stderr}`, /owner@example\.com/iu);
        return true;
      },
    );
    for (const [path, original] of Object.entries(originalArtifacts)) {
      assert.deepEqual(
        readFileSync(join(state.project, path)),
        original,
        `A failed legacy authorization transfer must restore ${path} byte-for-byte`,
      );
    }
    assert.equal(existsSync(join(state.project, "src/.sites-worker-entry.mjs")), false);
  });
});
