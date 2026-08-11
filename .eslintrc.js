// ESLint legacy (eslintrc) config — Codacy toggle, ON.
//
// ONLY ONE OF THESE TWO FILES IS EVER READ:
//
//   eslint.config.js   -- flat config, used by ESLint >= 9
//   .eslintrc.js       (this file) -- legacy config, used by ESLint <= 8
//
// They are not layered and they do not merge. ESLint 9 reads eslint.config.js
// and ignores this file entirely; ESLint 8 does the reverse. Which one governs
// depends on whichever ESLint runs — Codacy's, a global CLI, or an editor
// extension shipping its own copy. Both files exist here because both were
// asked for, and both are set to the SAME baseline so that whichever wins, the
// answer is the same. If you change a rule, change it in both or the two
// halves drift apart silently.
//
// `eslint:recommended` is built into ESLint itself — no plugin package, no
// npm install, nothing to resolve. That is why it is the baseline here rather
// than a shareable config like `airbnb` or `standard`: those are packages, and
// a config naming a package that the runner does not have does not fall back
// to defaults, it errors.
//
// `root: true` stops ESLint searching upward for parent .eslintrc files, so a
// run inside the vault cannot inherit config from someone's home directory.
//
// `ignorePatterns` is load-bearing, not tidiness: node_modules is COMMITTED
// under THE-GEMSTONE. Without these lines ESLint lints thousands of vendored
// files and the real findings are unreachable.

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
};
