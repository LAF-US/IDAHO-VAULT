// ESLint legacy config — INERT against the ESLint this repo installs.
//
// Measured on eslint 10.8.1 (pinned in package.json): eslint.config.js is the
// only format read. Move it aside and ESLint refuses to run — "couldn't find
// an eslint.config.(js|mjs|cjs) file" — rather than falling back here. The
// ESLINT_USE_FLAT_CONFIG=false escape hatch is gone, and `eslint --help` lists
// no eslintrc options.
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
