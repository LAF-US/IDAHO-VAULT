/* global module, require */

// This is a CommonJS configuration file. The language options below supply
// Node globals to linted repository files. The declaration above makes the
// configuration file itself analyzable by external ESLint integrations.

// ESLint flat config — Codacy toggle. The only config format ESLint 10 reads.
//
// `ignores` is ALONE in its object deliberately — in flat config that makes it
// global; bundled with other keys it would apply to that entry only.
// node_modules is committed under THE-GEMSTONE, and installing the
// devDependencies creates a second one at the root.
//
// Flat config has no `env`, so globals must be supplied explicitly. Without
// the `globals` block below, 28 of 31 findings were `no-undef` on console,
// process, document and window — the config's fault, not the code's. Bundled
// Obsidian plugins are third-party artifacts and are excluded from this baseline.
// languageOptions merge rather than replace.
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
// The slides-templates block below is reachable ONLY because of the negation
// patterns in the global ignores: `.codex/skills/**` is globally ignored, and
// global ignores are not overridden by a later `files` entry — a previous
// version of this header argued the block was "NOT inert" by pointing at the
// tracked file (.codex/skills/codex-primary-runtime/slides/templates/
// build_pro_deck_template.js), which answered the wrong question: the file
// existed, but eslint never saw it. Existence is not reachability.

const js = require("@eslint/js");
const globals = require("globals");

module.exports = [
  {
    ignores: [
      "THE-GEMSTONE/**",
      "**/node_modules/**",
      ".venv/**",
      ".uv-cache/**",
      ".obsidian/plugins/**",
      // Ignore-all-except ladder, replacing a flat `.codex/skills/**`. Three
      // reviewers (codereviewbot x2, coderabbit) caught that the `**` form
      // swallowed the whole subtree, leaving the slides-templates ESM block
      // below with nothing to match — and a plain `!` negation cannot cut
      // through an ignored parent directory. The documented shape is this
      // ladder: at each level ignore the siblings with `/*`, un-ignore the one
      // directory to descend. Verified by running eslint on both sides:
      // the template file is linted; slides/scripts stays ignored.
      ".codex/skills/*",
      "!.codex/skills/codex-primary-runtime",
      ".codex/skills/codex-primary-runtime/*",
      "!.codex/skills/codex-primary-runtime/slides",
      ".codex/skills/codex-primary-runtime/slides/*",
      "!.codex/skills/codex-primary-runtime/slides/templates",
      "eslint.config.js",
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
