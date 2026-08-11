// ESLint legacy (eslintrc) config — STUB.
//
// ONLY ONE OF THESE TWO FILES IS EVER READ:
//
//   eslint.config.js   -- flat config, used by ESLint >= 9
//   .eslintrc.js       (this file) -- legacy config, used by ESLint <= 8
//
// They are not layered and they do not merge. ESLint 9 reads eslint.config.js
// and ignores this file entirely; ESLint 8 does the reverse. Which one governs
// is decided by whatever ESLint version happens to run — the installed
// dependency, a globally installed CLI, an editor extension shipping its own
// copy, or Codacy's. Both files exist here because both were asked for, but a
// rule written in one is invisible to the other half of the time. If you add a
// real rule, add it to BOTH or delete the file you are not using.
//
// `root: true` is the one setting that is not inert, and it is here on
// purpose: it stops ESLint's upward search for parent .eslintrc files, so a
// run inside the vault cannot inherit config from someone's home directory.
// `rules: {}` applies nothing.
//
// Nothing invokes ESLint in this repo: it is not in package.json's
// devDependencies (prettier is the only JS tool there), and no workflow calls
// it. Codacy may run its own copy and honor this file.
//
// Shape when this stops being a stub -- eslintrc uses `env` and `extends`,
// neither of which exists in flat config, which is why the two files cannot be
// copy-pasted between each other:
//
//   module.exports = {
//     root: true,
//     env: { node: true, es2024: true },
//     extends: ["eslint:recommended"],
//     ignorePatterns: ["node_modules/", "THE-GEMSTONE/"],
//     rules: { "no-unused-vars": "warn" },
//   };
//
// `ignorePatterns` matters more here than in most repos: node_modules is
// committed under THE-GEMSTONE, so a config without it will lint thousands of
// vendored files.

module.exports = {
  root: true,
  rules: {},
};
