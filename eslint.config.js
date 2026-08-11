// ESLint flat config — STUB.
//
// ONLY ONE OF THESE TWO FILES IS EVER READ:
//
//   eslint.config.js   (this file)  -- flat config, used by ESLint >= 9
//   .eslintrc.js                    -- legacy config, used by ESLint <= 8
//
// They are not layered and they do not merge. ESLint 9 finds this file and
// ignores .eslintrc.js entirely; ESLint 8 does the reverse. Which one governs
// is decided by whatever ESLint version happens to run — the installed
// dependency, a globally installed CLI, an editor extension shipping its own
// copy, or Codacy's. Both files exist here because both were asked for, but a
// rule written in one is invisible to the other half of the time. If you add a
// real rule, add it to BOTH or delete the file you are not using.
//
// This config is an empty array: no language options, no plugins, no rules.
// ESLint reads it, finds nothing to apply, and reports nothing.
//
// CommonJS (`module.exports`) rather than ESM (`export default`) because the
// root package.json declares no `"type": "module"`, so a bare .js file in this
// repo is CommonJS. Writing `export default` here would throw at load time.
//
// Nothing invokes ESLint in this repo: it is not in package.json's
// devDependencies (prettier is the only JS tool there), and no workflow calls
// it. Codacy may run its own copy and honor this file.
//
// Shape when this stops being a stub -- note that flat config has no `env` or
// `extends`; globals come from the `globals` package and shared configs are
// spread into the array:
//
//   module.exports = [
//     {
//       files: ["**/*.js"],
//       ignores: ["**/node_modules/**", "THE-GEMSTONE/**"],
//       languageOptions: { ecmaVersion: 2024, sourceType: "commonjs" },
//       rules: { "no-unused-vars": "warn" },
//     },
//   ];
//
// `ignores` matters more here than in most repos: node_modules is committed
// under THE-GEMSTONE, so a config without it will lint thousands of vendored
// files.

module.exports = [];
