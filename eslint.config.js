// ESLint flat config — Codacy toggle, ON.
//
// ONLY ONE OF THESE TWO FILES IS EVER READ:
//
//   eslint.config.js   (this file)  -- flat config, used by ESLint >= 9
//   .eslintrc.js                    -- legacy config, used by ESLint <= 8
//
// They are not layered and they do not merge. ESLint 9 finds this file and
// ignores .eslintrc.js entirely; ESLint 8 does the reverse. Which one governs
// depends on whichever ESLint runs — Codacy's, a global CLI, or an editor
// extension shipping its own copy. Both files exist here because both were
// asked for, and both are set to the SAME baseline so that whichever wins, the
// answer is the same. If you change a rule, change it in both or the two
// halves drift apart silently.
//
// `@eslint/js` is not a third-party plugin — it is ESLint's own package, a
// direct dependency of `eslint`. Wherever ESLint 9 is installed, this require
// resolves. It is how flat config reaches the same rule set that eslintrc
// spells `extends: ["eslint:recommended"]`; flat config has no string
// `extends`, which is the single biggest reason the two files cannot be
// copy-pasted between each other.
//
// CommonJS (`module.exports`) rather than ESM (`export default`) because the
// root package.json declares no `"type": "module"`, so a bare .js file here is
// CommonJS. `export default` would throw at load time.
//
// The `ignores` block comes FIRST and is alone in its object on purpose: in
// flat config, an `ignores` key with no other key in the same object is a
// global ignore. Bundled into the object below it would only apply to that
// one config entry. This matters more here than in most repos — node_modules
// is COMMITTED under THE-GEMSTONE, so without a global ignore ESLint lints
// thousands of vendored files and the real findings are unreachable.

const js = require("@eslint/js");

module.exports = [
  { ignores: ["THE-GEMSTONE/**", "**/node_modules/**", ".venv/**", ".uv-cache/**"] },
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: "commonjs",
    },
  },
];
