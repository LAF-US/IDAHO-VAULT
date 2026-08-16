/* global module, require */
//
// Codacy does not read this repository's ESLint config. Its CLI prints
// "ESLint configuration created based on Codacy settings" and generates its own
// from the Code patterns page, so the `sourceType: "commonjs"` and
// `globals.node` declared in eslint.config.js never reach Codacy's run. These
// files really are CommonJS, so Codacy's generated config drew no-undef on
// `module` and `require`. Reproduced locally with codacy-cli-v2: exactly the
// four alerts code scanning reported, same files, same lines.
//
// The directive above states a fact rather than silencing a rule -- both are
// Node CommonJS modules and both globals exist at run time. `/* global */` is
// honoured by every ESLint config including a generated one; `eslint-env node`
// would not be, having been removed in ESLint 9.

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
// NO file fails to parse. Measured at head: `eslint .` reports 0 parse errors
// across the tree.
//
// This block used to say ONE did — pro_deck_quality_check.js:112, where a
// redaction marker had been spliced into an object key. That was true when
// written; ae357e178 repaired the damage, and line 112 is now a clean
// `chart_count: 0,` beside its slide_count and media_count siblings. The claim
// outlived its defect, which is the second time this header has done that (the
// first was build_pro_deck_template.js, fixed by the slides-templates block
// below and left asserted afterwards). Stated plainly so the next reader does
// not inherit a baseline that stopped being true.
//
// The slides-templates block below is NOT inert, despite a review claiming the
// directory does not exist: `git ls-files` tracks
// .codex/skills/codex-primary-runtime/slides/templates/build_pro_deck_template.js,
// which is exactly what that block parses as ESM.

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

  {
    // ESM by design — the file's own header says the init script writes a
    // sibling package.json with type=module. Parsing it as CommonJS produced a
    // permanent "Unexpected token import" in the baseline: a config artifact,
    // not a defect in the file.
    files: [".codex/skills/codex-primary-runtime/slides/templates/**/*.js"],
    languageOptions: {
      sourceType: "module",
      // Substitution placeholders. The init script replaces each with a JSON
      // literal before the template is ever executed, so they are defined at
      // run time and only look undefined to a linter reading the template
      // form. Enumerated from the file, not guessed.
      globals: {
        __DECK_ID_JSON__: "readonly",
        __OUT_DIR_JSON__: "readonly",
        __REFERENCE_DIR_JSON__: "readonly",
        __SLIDES_JSON__: "readonly",
      },
    },
  },
];
