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
documentation** and read by AI agents *intent-alongside-code*. A raw `.ipynb` is a JSON blob:
un-diffable, merge-hostile, and **poorly readable by agents** (a corrupt one is unreadable). The
Markdown twin is what agents and git read.

## The rule

- Pairing is **explicit and per-notebook (opt-in)** — *not* a global default. Each notebook that
  should be paired declares `ipynb,md` in its own metadata (via `--set-formats`).
- The **Markdown twin is the source of truth** — code wrapped in prose, diffs cleanly, what
  reviewers and agents read. The `.ipynb` is a **regenerable run-surface** that carries outputs.
- After editing **either** side, run **`jupytext --sync <notebook>`**. The `.githooks/pre-commit`
  hook does this for staged notebooks; the `check-notebooks-paired` CI fails a PR on twin drift.

## How to work

```sh
jupytext --set-formats ipynb,md path/to/Notebook.ipynb   # pair a notebook (one time)
jupytext --sync          path/to/Notebook.ipynb          # reconcile the pair after edits
```

To give an existing plain `.py` module agent-readable documentation, pair it the same way
(`jupytext --set-formats py:percent,md module.py`) — the intended next step for the real package
under `src/idaho_vault/`.

## ⚠️ Footgun (learned the hard way)

**Never run `--set-formats` on a notebook that already has a same-named `.md`** unless you have
checked that `.md` first. `jupytext --sync` picks its direction by modification time; if a stale
same-named `.md` is newer, it will **overwrite the notebook's code from the (possibly empty) `.md`.**
This is exactly why pairing is explicit and per-notebook here, and why there is **no global pairing
default** in `jupytext.toml`. `Untitled.ipynb` already had an unrelated `Untitled.md` stub and is
therefore **left unpaired** on purpose.

## Hygiene

- `.ipynb_checkpoints/` is gitignored (autosave artifacts, never source of truth).
- Twin filenames must obey the NETWEB portable-path standard (`VAULT-CONVENTIONS.md`).

## Currently paired

- `LLM-Router.ipynb` ↔ `LLM-Router.md` (round-trip verified identical).

## Known corrupt / unpaired (pending decision)

- `StabilizationSystem.ipynb` is **invalid JSON** — multiply malformed (unescaped control
  characters *and* a structural break), beyond a faithful automatic repair. **Not** paired or
  auto-"fixed" (reconstructing unreadable cells would invent content). Stray test/experiment;
  **Logan decides** rebuild-by-hand vs remove.
- `Untitled.ipynb` (the CourtListener scraper) is **left unpaired** — see the footgun above.

## Dependency note

`jupytext` is declared in `pyproject.toml` `[dependency-groups] dev`. The uv-generated
`requirements.txt` should be refreshed with `uv lock && uv export ...` by a maintainer with the
full toolchain; CI installs `jupytext` directly, so the check does not depend on that refresh.
