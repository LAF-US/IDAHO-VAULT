# Plan: Commit outstanding main changes + LEVELSET refresh

## Context

After the Sunday swarm session, `main` has 4 modified files and 2 untracked reference docs sitting uncommitted. The changes are clean and understood. Logan has directed: commit the infra docs, commit the reference docs, skip `swarm/app.py` (CRLF artifact only), and then do a LEVELSET refresh on a branch.

---

## Commit 1 — Infrastructure docs (direct to main)

Files:
- `.claude/CLAUDE.md` — Windows Prerequisite section added (Git Bash + PATH env var)
- `AGENTS.md` — Claude Code row updated with same Windows Git Bash note

Message: `docs: add Windows Git Bash prerequisite to CLAUDE.md and AGENTS.md`

---

## Commit 2 — Reference captures (direct to main)

Files:
- `- - Model Context Protocol – Codex OpenAI Developers.md` (untracked)
- `OpenAI - Documentation - CLI – Codex OpenAI Developers.md` (untracked)
- `- and.md` — Obsidian auto-frontmatter only; bundle here to clear the diff

Message: `chore: commit Obsidian reference captures and auto-frontmatter touch`

---

## Skip

- `swarm/app.py` — CRLF warning only, no content diff. No commit.

---

## Step 3 — LEVELSET refresh (branch)

Branch: `claude/levelset-refresh-2026-03-29`

Update `!/!/LEVELSET-CURRENT.md`:
- Date → 2026-03-29
- Active branch → `main` (no active feature branch)
- Last commit → reflect today's commits
- Open PRs → verify current state via `gh pr list`
- Active mesh → Gemini terminated; Claude Code + Logan + CodeRabbit (passive) + Qodo (down)
- UNRESOLVED / NEXT ACTIONS → reflect Sunday swarm outcomes: LINEAR_API_KEY provisioned, Gemini cowork live, Spring Clean in-progress, stash on `claude/mcp-phase-0-discovery` still present

Then push branch and open PR targeting `main`.

---

## Verification

- `git status` clean after commits 1 + 2
- LEVELSET-CURRENT date and state fields accurate
- PR opens cleanly against `main`
