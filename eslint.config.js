// ESLint flat config — Codacy toggle, ON. This is the file ESLint actually reads.
//
// .eslintrc.js SITS BESIDE THIS ONE AND IS DEAD AGAINST THE INSTALLED ESLINT.
// Measured on eslint 10.8.1 (the version in package.json): moving this file
// aside does not make ESLint fall back to .eslintrc.js — it refuses to run at
// all ("ESLint couldn't find an eslint.config.(js|mjs|cjs) file"). The
// ESLINT_USE_FLAT_CONFIG=false escape hatch is gone too. eslintrc only governs
// if something runs ESLint 8 or older, which nothing in this repo does.
//
// `require` rather than `import` because the root package.json declares no
// `"type": "module"`, so a bare .js file here is CommonJS.
//
// The four blocks below, in order, and why each is separate:
//
//   1. ignores, ALONE in its object. In flat config an `ignores` key with no
//      sibling keys is a global ignore; bundled into a config object it would
//      only apply to that object. node_modules is COMMITTED under
//      THE-GEMSTONE, so without this ESLint lints thousands of vendored files.
//   2. js.configs.recommended — ESLint's own baseline, from @eslint/js, which
//      is eslint's own dependency rather than a third-party plugin.
//   3. Node globals for everything. Flat config has NO `env` key, so globals
//      must be supplied explicitly; without them `no-undef` fires on `console`
//      and `process` in every script. Measured: 28 of 31 findings before this
//      block existed were exactly that, and they were the config's fault, not
//      the code's.
//   4. Browser globals for Obsidian plugins. They run in Electron's renderer,
//      so they legitimately reach both `window`/`document` AND `require`.
//      languageOptions merge rather than replace, so these files get node
//      globals from block 3 plus browser globals here — which is accurate.
//
// NOT CONFIGURED AWAY: two files under .codex/skills/.../slides/ fail to
// parse, and both are real defects rather than config gaps.
//     Note this description deliberately does NOT reproduce the marker glued
//     between two letters: that exact shape IS the corruption signature, and
//     check_redaction_damage.py fails any added line containing it — it cannot
//     tell a citation from the real thing. (Its own source dodges the same
//     trap by building the marker from pieces rather than writing it out.)
//   - pro_deck_quality_check.js:112 has a redaction marker spliced into the
//     middle of an object key, so the key reads as `cha` + marker + `count`
//     while its siblings are slide_count / media_count /
//     embedded_workbook_count. A redaction pass rewrote an identifier and
//     broke the file. The repo's check-redaction-damage guard is diff-based,
//     so it never saw the damage already sitting in that file.
//   - build_pro_deck_template.js uses ESM `import`. Its own header says the
//     init script writes a sibling package.json with type=module, so it is ESM
//     by design and simply is not loadable from this repo root.
// Both are left visible. Silencing them here would hide the first one, which
// is damage.

const js = require("@eslint/js");
const globals = require("globals");

module.exports = [
  {
    ignores: [
      "THE-GEMSTONE/**",
      "**/node_modules/**",
      ".venv/**",
      ".uv-cache/**",
    ],
  },

  js.configs.recommended,

  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: "commonjs",
      globals: { ...globals.node },
    },
  },

  {
    files: [".obsidian/plugins/**/*.js"],
    languageOptions: {
      globals: { ...globals.browser },
    },
  },
];
