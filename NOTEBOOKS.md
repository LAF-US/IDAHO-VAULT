---
title: "Notebooks in the Vault — the Jupyter/Jupytext middle"
status: proposed
authority: LOGAN
related:
  - CONSTITUTION
  - jupytext.toml
  - VAULT-CONVENTIONS
---

# Notebooks in the Vault — the Jupyter/Jupytext middle

*Proposed by Claude (`*.claude.*`); Logan inscribes via merge. `authority: LOGAN` is a recorded
field, not a claim that Logan authored these lines.*

## Why

`CONSTITUTION.md` § I names three substance-types: **Markdown = human, Python = machine,
Jupyter = the overlap.** Logan decreed Jupyter/Jupytext as the layer that **marries the machine
and plaintext halves of the vault** — so the vault's Python can be **wrapped in its own
documentation** and read by AI agents *intent-alongside-code*. This file is the convention that
puts the decree into practice.

The problem it solves: a raw `.ipynb` is one large JSON blob — un-diffable, merge-hostile, and
**poorly readable by agents** (a corrupt one is unreadable; see *Known corrupt* below). Jupytext
keeps a plaintext **twin** of each notebook that agents and git can both read.

## The rule

- Every notebook is **paired to a Markdown twin** (`ipynb,md`), set in `jupytext.toml`.
- The **Markdown twin is the source of truth** — it holds the code wrapped in prose, diffs
  cleanly, and is what reviewers and agents read. The `.ipynb` is a **regenerable run-surface**
  that carries outputs.
- After editing **either** side, run **`jupytext --sync <notebook>`** to bring the pair into
  agreement. The pre-commit hook (`.githooks/pre-commit`) does this for staged notebooks; the
  `check-notebooks-paired` CI fails a PR if any twin has drifted.

## How to work

```sh
jupytext --set-formats ipynb,md path/to/Notebook.ipynb   # pair a new notebook (one time)
jupytext --sync path/to/Notebook.ipynb                   # reconcile the pair after edits
```

To give an existing **plain `.py` module** agent-readable documentation, pair it the same way
(`jupytext --set-formats py:percent,md module.py`) — this is the intended next step for the real
package under `src/idaho_vault/`.

## Hygiene

- `.ipynb_checkpoints/` is gitignored (autosave artifacts, never source of truth).
- Twin filenames must obey the NETWEB portable-path standard (`VAULT-CONVENTIONS.md`).

## Known corrupt (pending decision)

`StabilizationSystem.ipynb` is **invalid JSON** — multiply malformed (unescaped control
characters *and* a structural break), beyond a faithful automatic repair. It was **not** paired
or auto-"fixed" (reconstructing unreadable cells would invent content). It is a stray
test/experiment swept into the monorepo; **Logan decides** whether to rebuild it by hand or
remove it.

## Dependency note

`jupytext` is declared in `pyproject.toml` `[dependency-groups] dev`. The uv-generated
`requirements.txt` should be refreshed with `uv lock && uv export ...` by a maintainer with the
full toolchain; CI installs `jupytext` directly, so the check does not depend on that refresh.
