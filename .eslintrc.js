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
// So the trade is real and worth stating plainly: this file buys a config for
// Codacy's ESLint-8 toggle (a tool nobody has enabled, for an ESLint that went
// EOL in October 2024) and costs a working ESLint in any modern tool that
// finds it. Deleting it is a one-line change and probably the right call —
// Logan's, not this file's.
//
// Kept because CODACY TREATS THE TWO AS SEPARATE TOOLS, and its supported-files
// table maps them by filename:
//
//   ESLint v8 -> .eslintrc.js, .eslintrc.cjs, .eslintrc.yaml/.yml/.json
//   ESLint v9 -> eslint.config.js, eslint.config.mjs, eslint.config.cjs
//
// So which of the two files governs depends on which ESLint tool is enabled
// on the Code patterns page -- not on a version guess. Both are present so
// either choice finds a config. A rule added here and not to eslint.config.js
// affects nothing when the v9 tool is the one enabled.
//
// Either way this is inert until Code patterns -> ESLint -> "use a
// configuration file" is toggled on.
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
