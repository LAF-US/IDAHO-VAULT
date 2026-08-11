// ESLint legacy (eslintrc) config — INERT against the ESLint this repo installs.
//
// MEASURED, not assumed. package.json pins eslint ^10.8.1. On 10.8.1:
//
//   - eslint.config.js is the only config format read.
//   - Moving eslint.config.js aside does NOT make ESLint fall back to this
//     file. It refuses to run: "ESLint couldn't find an
//     eslint.config.(js|mjs|cjs) file", plus a pointer to the migration guide.
//   - The ESLINT_USE_FLAT_CONFIG=false escape hatch from the v9 era is gone.
//   - `eslint --help` lists no eslintrc options at all.
//
// So this is not "the other half of a coin flip" — against the installed
// toolchain it is dead weight. It governs only if something runs ESLint 8 or
// older, which nothing here does. Codacy is the one plausible caller, if its
// image ships an older ESLint.
//
// It is kept, rather than deleted, because it costs nothing and covers that
// one case. But do not treat it as a live rule surface: a rule added here and
// not to eslint.config.js will have no effect on anything in this repo.
//
// It mirrors eslint.config.js's baseline so the two cannot disagree:
// `eslint:recommended` is the eslintrc spelling of the same rule set that
// eslint.config.js gets from @eslint/js. `env` supplies the globals that flat
// config supplies through the `globals` package — the two files reach the same
// place by different routes, which is the single clearest reason they cannot
// be copy-pasted between each other.
//
// `root: true` stops the upward search for parent .eslintrc files, so a run
// inside the vault cannot inherit config from someone's home directory.
//
// `ignorePatterns` is load-bearing: node_modules is COMMITTED under
// THE-GEMSTONE, and installing the devDependencies creates a second one at the
// repo root.

module.exports = {
  root: true,
  env: { node: true, browser: true, es2024: true },
  parserOptions: { ecmaVersion: 2024, sourceType: "script" },
  extends: ["eslint:recommended"],
  ignorePatterns: [
    "THE-GEMSTONE/",
    "node_modules/",
    ".venv/",
    ".uv-cache/",
  ],
};
