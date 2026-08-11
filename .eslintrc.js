// ESLint legacy config — NOT MERELY INERT. IT BREAKS MODERN ESLINT RUNS.
//
// Measured on eslint 10.8.1 (pinned in package.json): eslint.config.js is the
// only format read. Move it aside and ESLint refuses to run — "couldn't find
// an eslint.config.(js|mjs|cjs) file" — rather than falling back here. The
// ESLINT_USE_FLAT_CONFIG=false escape hatch is gone, and `eslint --help` lists
// no eslintrc options.
//
// THE COST IS NOT ZERO, and an earlier version of this header said it was.
// "Inert" is only true while nothing points ESLint at this file. The moment
// something does, the whole run dies:
//
//     $ eslint --config .eslintrc.js <anything>
//     A config object is using the "root" key, which is not supported in
//     flat config system.
//
// Not one bad key, either — removing `root` moves the error to `env`, and
// after that would come `extends`, `overrides`, `ignorePatterns`. This is an
// eslintrc file; ESLint 10 cannot load it at all, by design.
//
// This is not hypothetical. CodeRabbit's ESLint integration detects this file,
// points ESLint 10.8.1 at it, and fails — so its ESLint tool currently reports
// nothing on this repo, on every PR, because this file exists. Reproduced
// locally with the exact error above.
//
// WHY THE FILE STAYS ANYWAY. Codacy runs two separate ESLint tools, and each
// reads a different filename:
//
//     Codacy ESLint 8.57.0  ->  .eslintrc.js, .eslintrc.cjs, .eslintrc.{yaml,yml,json}
//     Codacy ESLint 9.39.5  ->  eslint.config.js, eslint.config.mjs, eslint.config.cjs
//
// So this file is the config for a toggle that is available to enable, not a
// relic. An earlier version of this header argued the opposite — that upstream
// ESLint 8 going EOL in October 2024 made the file dead weight. That is a fact
// about upstream and says nothing about which tools Codacy offers; deleting
// the file would silently remove one of the two options.
//
// Note also that Codacy's v9 is 9.39.5, NOT the 10.8.1 pinned in package.json.
// eslint.config.js is verified against 9.39.5 as well: it loads, applies
// js.configs.recommended, and correctly leaves `document` undefined outside
// .obsidian/plugins/** — checked against fixtures, since a clean exit and "no
// files matched" produce identical output.
//
// The CodeRabbit breakage is therefore not an argument for deleting this file.
// It is an argument for telling CodeRabbit not to run its own ESLint, which is
// duplicating Codacy and currently reporting nothing:
//
//     # .coderabbit.yaml
//     reviews:
//       tools:
//         eslint:
//           enabled: false
//
// (`reviews.tools.eslint.enabled` confirmed against CodeRabbit's published
// schema.v2.json.) That change belongs in .coderabbit.yaml, a shared surface,
// and has not been made here.
//
// Which of the two files governs therefore depends on which ESLint tool is
// enabled on the Code patterns page, not on a version guess. Both are present
// so either choice finds a config, and a rule added here but not to
// eslint.config.js affects nothing when the v9 tool is the one enabled.
//
// This file is verified against the tool it exists for. eslint 8.57.0 loads it
// and reports through it:
//
//     $ eslint@8.57.0 --no-eslintrc -c .eslintrc.js broken.js
//       1:13  error  'undefinedThing' is not defined         no-undef
//       2:5   error  'x' is assigned a value but never used  no-unused-vars
//
// including `env.es2024`, which a reviewer believed ESLint 8 did not define. A
// clean run alone would not have settled that — an ignored key and an accepted
// key look identical — so the control: the same file with `es2024` changed to
// a bogus `es9999` fails hard with "Error: --config". ESLint 8.57.0 rejects
// unknown environments, so es2024 passing means it is really in the table.
//
// It mirrors eslint.config.js so the two cannot disagree: `eslint:recommended`
// is the eslintrc spelling of what @eslint/js provides there, and `env`
// supplies what the `globals` package supplies there.

module.exports = {
  root: true,
  env: { node: true, es2024: true },
  parserOptions: { ecmaVersion: 2024, sourceType: "script" },
  extends: ["eslint:recommended"],
  ignorePatterns: [
    "THE-GEMSTONE/",
    "node_modules/",
    ".venv/",
    ".uv-cache/",
  ],
  overrides: [
    {
      // Electron renderer: browser globals ON TOP of node. Scoped here rather
      // than set at the root, so a stray `window` in a non-plugin script is
      // still reported. Mirrors the flat config's per-path globals block.
      files: [".obsidian/plugins/**/*.js"],
      env: { browser: true },
    },
    {
      // Mirrors the flat config's ESM block; see eslint.config.js.
      files: [".codex/skills/codex-primary-runtime/slides/templates/*.js"],
      parserOptions: { sourceType: "module" },
      globals: {
        __DECK_ID_JSON__: "readonly",
        __OUT_DIR_JSON__: "readonly",
        __REFERENCE_DIR_JSON__: "readonly",
        __SLIDES_JSON__: "readonly",
      },
    },
  ],
};
