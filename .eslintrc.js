// ESLint legacy config — INERT against the ESLint this repo installs.
//
// Measured on eslint 10.8.1 (pinned in package.json): eslint.config.js is the
// only format read. Move it aside and ESLint refuses to run — "couldn't find
// an eslint.config.(js|mjs|cjs) file" — rather than falling back here. The
// ESLINT_USE_FLAT_CONFIG=false escape hatch is gone, and `eslint --help` lists
// no eslintrc options.
//
// Kept only for a Codacy image shipping ESLint 8 or older. A rule added here
// and not to eslint.config.js affects nothing in this repo.
//
// It mirrors eslint.config.js so the two cannot disagree: `eslint:recommended`
// is the eslintrc spelling of what @eslint/js provides there, and `env`
// supplies what the `globals` package supplies there.

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
