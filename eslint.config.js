// ESLint flat config — Codacy toggle. The only config format ESLint 10 reads.
//
// Measured on eslint 10.8.1: move this file aside and ESLint refuses to run
// rather than falling back to .eslintrc.js, and ESLINT_USE_FLAT_CONFIG=false
// is gone. See that file's header.
//
// `ignores` is ALONE in its object deliberately — in flat config that makes it
// global; bundled with other keys it would apply to that entry only.
// node_modules is committed under THE-GEMSTONE, and installing the
// devDependencies creates a second one at the root.
//
// Flat config has no `env`, so globals must be supplied explicitly. Without
// the `globals` block below, 28 of 31 findings were `no-undef` on console,
// process, document and window — the config's fault, not the code's. Obsidian
// plugins get browser globals on top of node: they run in Electron's renderer
// and legitimately reach both. languageOptions merge rather than replace.
//
// Two files still fail to parse, and both are real defects, left visible:
//   - build_pro_deck_template.js is ESM by design (its header says the init
//     script writes a sibling package.json with type=module).
//   - pro_deck_quality_check.js:112 has a redaction marker spliced into an
//     object key, which reads as `cha` + marker + `count` where its siblings
//     are slide_count and media_count. This description avoids pasting the
//     marker glued between letters, because that shape IS the corruption
//     signature and check_redaction_damage.py fails any added line containing
//     it — do not "fix" the wording back.

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
