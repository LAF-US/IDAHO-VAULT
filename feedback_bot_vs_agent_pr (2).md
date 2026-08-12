# Feedback: Bot PR vs Agent PR — terminology discipline

**Witnessed**: 2026-05-28, during closed-PR corpus triage
**Logan's correction**: *"NOTE: Be more deliberate about distinguishing between 'bot' PR and 'agent' PR."*

## Definitions

**Bot PR** = scheduled or event-triggered automation whose output IS the work product. The bot is the author in both attribution and substance. Examples:
- Dependabot dependency bumps
- daily-rollover.yml's rollover commits
- sync-dependencies.yml's requirements.txt + uv.lock sync
- wayback-audit, ingest pipelines

**Agent PR** = an AI agent (Codex/Claude/Antigravity/Copilot) authored the actual content. The PR opener may differ from the agent. Examples:
- `codex/worm-watch-hardening` (Codex authored, github-actions[bot] may have opened the PR via agent-auto-pr workflow)
- `antigravity/pullman-oidc-pipeline` (Antigravity authored content, Logan committed/pushed)
- `claude/update-claude-files-PRWCJ` (Claude agent generated content)
- `copilot/coordinating-hexagonal-hub` (Copilot SWE agent)

## How to identify agent provenance

The PR author account is NOT the most reliable signal — that's the opener, not necessarily the content-generator. More reliable:

1. **Branch prefix**: `codex/`, `claude/`, `antigravity/`, `gemini/`, `copilot/` indicate the agent that generated the work
2. **Author account on commits** (vs. PR author): commits often retain the agent-account or carry agent-attribution in trailers
3. **PR body**: agent-generated PRs frequently include the agent's session/task ID

## Why the distinction matters

- **Bot PRs**: usually fungible — losing one nightly-rollover PR loses one day of rollover state; the next successful run absorbs it
- **Agent PRs**: often non-fungible — represent specific design choices, security hardening artifacts, or doctrine work that doesn't naturally regenerate

When triaging closed PRs:
- A lost bot PR is mostly noise (LOW revival priority)
- A lost agent PR is potentially substantial work (HIGH revival priority, especially WORM-WATCH-style named-witness artifacts)

## Examples from 2026-05-28 triage

- #341 `codex/worm-watch-hardening` — PR author is `app/github-actions[bot]` but the work is Codex's. **Agent PR. HIGH revival priority.**
- #227 `antigravity/pullman-oidc-pipeline` — PR author is `loganfinney27` but the design is Antigravity's. **Agent PR. HIGH revival priority.**
- #305 `bot/daily-rollover-2026-04-26` — PR author is `app/github-actions[bot]` and the work IS the rollover. **Bot PR. LOW revival priority.**

The distinction also clarifies which closures are losses worth recovering vs. routine retry noise.
