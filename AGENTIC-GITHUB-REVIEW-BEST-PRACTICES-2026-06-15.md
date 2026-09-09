---
title: "Agentic GitHub Reviewers & Commenters — Best Practices (Research)"
created: 2026-06-15
updated: 2026-06-15
status: active
authority: "LOGAN"
authors:
  - Claude Code
source:
  - "deep-research web synthesis, 2026-06-15"
tags:
  - agent/coordination
  - github/review
  - swarm/doctrine
  - research/inquiry
related:
  - AGENTS
  - CLAUDE
  - CONSTITUTION
  - VAULT-CONVENTIONS
  - GitHub
  - Claude Code
  - GitHub Copilot
  - OpenAI Codex
  - Gemini CLI
  - The world is quiet here
---

# Agentic GitHub Reviewers & Commenters — Best Practices

*Filed by [[Claude Code]] (software NAME; no delegated TITLE or OFFICE claimed this session) — 2026-06-15*
*Branch: `claude/github-reviewers-research-u8hlk0`*
*Class: research / INQUIRY — external best practices surfaced for Logan's consideration, **not** adopted vault policy until ratified into [[VAULT-CONVENTIONS]] or [[CONSTITUTION]].*

---

## Provenance & Method

Five parallel web-research passes plus two security deep-dives, fanned out across the
five questions below. **Hard provenance limit:** in this execution environment, direct
page fetching (`WebFetch`) returned HTTP 403 across every host — including non-GitHub
domains and arXiv. Every claim therefore rests on **search-engine result snippets** of
the cited pages, not page-verified text. Treat load-bearing numbers (false-positive
bands, CVSS scores, merge rates) as **directional and citation-attributable but not
re-verified against the source body**. Vendor benchmarks (CodeRabbit, Greptile,
Macroscope, Graphite) are self-published and mutually competitive — read them as
interested, not neutral. Per the vault's truthfulness/provenance rules, the `*` wildcard
applies wherever a date is marked "undated": the gap is named, not filled.

The question, decomposed: **(I)** incorporating AI-reviewer suggestions, **(II)** reviewer
etiquette & noise control, **(III)** coordinating multiple tools, **(IV)** human-in-the-loop
governance & security, **(V)** issue/PR workflow patterns. Sources consolidated at the end.

---

## I. Incorporating AI-Reviewer Suggestions

**Triage by severity and confidence first; act on the top band, treat the rest as optional.**
Mature reviewers expose this metadata directly — [[CodeRabbit]] tags findings
Critical/Major/Minor/Trivial with a High/Medium/Low confidence scale (High = clear defect
with obvious fix; Low = plausible but may have side effects), and lets you filter by
severity, category, or author. Triage Critical + High-confidence first; demote nits and
Low-confidence to optional.

**Most automated-only review is low-signal — verify before trusting.** An MSR 2026 empirical
study of 3,109 commented-review PRs found **60.2%** of closed agent-only PRs fell in the
0–30% signal range, and 12 of 13 review agents averaged below a 60% signal ratio. PRs
reviewed *only* by AI merged at **45.2%** versus **68.4%** for human-reviewed — a ~23-point
gap. The practical reading: AI review is a useful first pass, not a merge gatekeeper.

**Quantify the noise before you trust the tool.** An independent audit of 28 PRs classified
**~36%** of [[CodeRabbit]] comments as low-value (15% "noise," 21% "nitpicking"). Untuned
first-generation LLM reviewers run 40–80% false positives; tuned systems get far lower
([[SonarSource]] reports 3.2% across 137M issues). Developer behavior tracks measurable
thresholds: **below ~10% FP** developers investigate every finding; **10–30%** they
investigate but call it "noisy"; **above 30%** they triage with suspicion; **above 50%**
they dismiss by default. Keep the tuned FP rate under ~10–30% or the reviewer gets ignored
or switched off.

**Never apply one-click suggestions blind.** [[GitHub Copilot]]'s "Commit suggestion" button
is advisory and does not auto-commit — but applying suggestions one-at-a-time produces noisy
history, so GitHub recommends "Add suggestion to batch" and committing as a reviewed group.
GitHub's own responsible-use guidance warns Copilot can reproduce insecure patterns from
training data; in one study **~40%** of 1,689 Copilot-generated programs were vulnerable. A
lint + type-check + run-existing-tests pass reportedly catches ~60% of AI-related issues
before deeper testing. Gate "apply" behind reading the diff and running checks, especially in
security-sensitive code.

**Tune the reviewer actively — feedback compounds.** Replying to a false positive in
[[CodeRabbit]] stores a "Learning" that suppresses similar future comments; teams that spend
~2 weeks correcting it "typically see a significant drop in false positives by the end of the
first month." Switching the profile from "Assertive" to "Chill" immediately narrows output to
high-severity findings; path-based instructions add directory-specific tuning. [[Greptile]]
raised its addressed-comment rate from **19% to 55%+** in two weeks using embeddings over user
dismissals.

**Measure review-load reduction, not comment count.** By 2026 the meaningful outcome is "we cut
review load 20–30% while keeping incident rates flat or lower," not "the bot left comments."
Reserve human judgment for architecture, business logic, and security-sensitive areas; let AI
handle style and trivial findings.

---

## II. Reviewer Etiquette & Noise Control

This section matters most for the vault's **own** agentic commenters (the [[Claude Code]]
GitHub Action, any future review bot), since their behavior is on-the-record in a public repo.

**One sticky, batched summary comment — updated, never reposted.** The canonical idempotent
pattern embeds an invisible header marker so the bot finds and updates its prior comment
across review rounds (the [Sticky PR Comment action] pattern; modes `only_create`, `append`,
`recreate`, `hide-and-recreate`). [[Claude Code]] Action implements this as
`use_sticky_comment`; failing to find the prior comment and duplicating every run is treated
as a bug (anthropics/claude-code-action #960, #602). Post one walkthrough/summary comment with
a changed-files table and review status, verbose sections collapsed by default.

**Every inline finding carries an explicit severity label.** Use critical/warning/suggestion
(or low/medium/high) so developers can separate must-fix from nits. Tier comments: T1 =
production-failure bugs, T2 = maintainability, T3 = subjective/nits; treat a **<60% signal
ratio** or a **<30–40% action rate** as a config failure. FP ceilings should vary by class —
suggested bars: security vulns **<3%**, maintainability **<5%**, style/nits **<2%** (the more
subjective the comment, the higher the bar to post it). Disable categories already covered by
linters; turn off decorative output (praise, "poems").

**Only comment when necessary.** [[Devin]]'s documented behavior: when clean, post one short
"Everything looks good!" and stop; otherwise leave specific, scoped inline comments.
[[GitHub Copilot]]'s reviewer is tuned for **precision over recall** — GitHub reports 71% of
Copilot reviews surface actionable feedback and the remaining 29% deliberately produce no
comment to protect signal. Gather cross-file context *before* commenting; expose thumbs-up/down
so humans can tune future output.

**Distinguish blocking from non-blocking, and respect rate limits.** AI comments should default
to advisory (non-blocking) — Copilot review does not block merge. Honor GitHub secondary rate
limits (≤100 concurrent requests, ≤900 REST points/min; rapid comment creation triggers
403/429): queue writes, cap concurrency, and back off exponentially (~180s, doubling).
Incremental reviews scoped to the new diff avoid re-flagging unchanged code.

---

## III. Coordinating Multiple AI Tools on One Repo

The vault runs four direct-write agents — [[Claude Code]], [[Gemini CLI]],
[[GitHub Copilot]], and [[OpenAI Codex]] — so this is the most directly applicable section.
(Narrative titles for these offices are delegated by Logan and recorded elsewhere; this report
does not assert the current roster.)

**Isolation is the core conflict-prevention primitive.** Give each agent its own working
directory (git worktree or branch-per-agent) over a shared object database, deferring
collisions to intentional merge points. **Always branch from `main`/a stable base, never from
an in-progress branch** — branching off WIP measurably increases conflict-resolution time.

**Decompose by domain/file ownership; never split work that touches the same files.** Shared
"hotspot" files (configs, registries, `manifest.json`, shared utilities) are predictable
collision points where parallel agents cause merge conflicts, duplicated features, and code
that compiles but disagrees at runtime. The consensus mitigation is explicit file ownership:
"break the work so each teammate owns a different set of files." (One vendor claims agents
auto-resolve same-file conflicts "without manual intervention" — treat that as unreliable
against the isolation consensus.)

**Use a shared task document agents claim/update.** Agents claim a task, mark in-progress, mark
done, with file locking to prevent race conditions. The vault's **DOCKET**
(`!/!/__!__/!/! The world is quiet here/DOCKET.md`) already *is* this shared task list.

**Adopt the coordinator → specialist → verifier (planner/implementer/reviewer) split.** One
agent writes, another critiques, another tests, another checks compliance/architecture. For PR
review specifically, the documented [[Claude Code]] pattern spawns parallel reviewers on one PR
by independent lens — one security, one performance, one test-coverage — then a lead synthesizes;
adversarial parallel review beats sequential single-agent review (which suffers anchoring). Keep
team size to **3–5 concurrent agents** ("three focused teammates often outperform five
scattered ones"); token cost and coordination overhead scale with count.

**Merge via a staging/integration branch, sequentially, behind automated verification.** Merge
feature branches into staging first, run tests, resolve conflicts, then promote the clean result
to `main` ("evidence-based merges").

**`AGENTS.md` is an emerging cross-tool coordination surface** — a shared instruction pointer, not
doctrine in itself; the vault remains the authoritative memory surface. Originated by OpenAI, now under
the Linux Foundation's Agentic AI Foundation; read natively by Codex, Copilot, Cursor, Windsurf,
Amp, Devin, Gemini CLI, and others (60k+ projects). Keep it focused — "if your config file is over
500 lines, most of it is being ignored; a focused 50-line file outperforms a sprawling 1,000-line
one." The vault's per-tool files (`.claude/CLAUDE.md`, `.codex/CODEX.md`, `.gemini/GEMINI.md`,
`.github/copilot-instructions.md`) plus the root [[AGENTS]] pointer already implement the
"one source + tool-specific references" model — the 500-line warning is worth heeding given
current `CLAUDE.md` length.

**"AI reviewing AI" is now mainstream and measurable.** Agent-authored PRs grew past 2M and
agents-reviewing-agents ~10×. Tools differ sharply: one benchmark had [[CodeRabbit]] catch 52.5%
of issues vs [[GitHub Copilot]]'s 36.7%, because Copilot review is diff-based and misses
cross-file/architectural issues while CodeRabbit does whole-PR + codebase-graph analysis.
[[CodeRabbit]]'s CLI explicitly orchestrates a generate→review loop with [[Claude Code]],
[[OpenAI Codex]] CLI, Cursor CLI, and [[Gemini CLI]].

---

## IV. Human-in-the-Loop Governance & Security

**The agent can never bless its own work.** [[GitHub Copilot]]'s coding agent can only push to
branches it created (never the default branch), its PRs **require human approval before any
CI/CD workflow runs**, and "all pull requests require independent human review since Copilot
can't approve or merge its own work." If you initiate a Copilot PR, you may approve it but your
approval does **not** count toward the required count — someone else must approve. A PR author
cannot approve their own PR, so even a one-approval rule forces a second human.

**A human always clicks merge — that is the traceable approval event.** Branch protection should
require senior-engineer review of critical files regardless of any AI risk classification.
Empirically, **reviewer engagement — not code correctness or iteration count — is the strongest
predictor** of whether an agent-authored PR merges (logistic regression over 33,596 agent PRs);
force-pushes and large changes lower merge odds.

**Close the self-approval bypass.** The repo setting "Allow GitHub Actions to create and approve
pull requests" is a known risk — a rogue workflow with an elevated `GITHUB_TOKEN` can self-approve
and bypass human review. Keep it off. Branch protection's "require approval of the most recent
push" rule structurally blocks the pushing identity (including a bot) from self-approving. Apply
least-privilege to all review bots and Action tokens: set the default `GITHUB_TOKEN` to read-only,
and **never run untrusted fork code under `pull_request_target` with secrets in scope** (OWASP
CI/CD "Poisoned Pipeline Execution" — reachable by anonymous external contributors, exactly the
agentic-PR threat model).

**Separation of duties — the reviewer must not be the prompter.** OWASP AISVS control AC.4.1: the
human reviewer "must not be the same identity that asked for the AI generation," and "the AI agent
itself does not count as the human reviewer"; security-critical files warrant two-person review or
security-team sign-off (AC.4.4). GitHub's **required-reviewer rulesets** (GA 2026-02-17) can force
team sign-off on sensitive paths and "augment CODEOWNERS but don't replace" it. A pragmatic org
policy pattern: AI opens **draft** PRs only (never commits direct to `main`), label them
`ai-generated`, require equal-or-stricter CI than human PRs, never force auto-approval, and let any
human demand review on any change. Note the **2026-03-13** opt-out that lets Actions skip the human
"Approve and run" gate on Copilot agent PRs is a deliberate security tradeoff — the default
(human approval required before any workflow touches tokens/secrets) is the safer posture.

**The PR-volume problem is now a platform-level concern.** AI agents generated ~17M PRs/month by
March 2026 (up from ~4M in Sept 2025); as of **2026-02-13** GitHub shipped settings to disable PRs
entirely or restrict them to collaborators.

### Security — prompt injection is the live threat for agentic reviewers

This is the most consequential finding for the vault, since it runs agentic GitHub actions on a
**public** repo where anyone can open a PR or file an issue.

- **LLMs cannot architecturally separate trusted instructions from untrusted content** — both
  arrive as the same token stream (Simon Willison, "lethal trifecta," 2025-06-16). An agent
  combining *private data + untrusted content + external communication* can be turned into a
  data-exfiltration tool by one injected prompt.
- **"Comment and Control" (disclosed ~April 2026)** is a demonstrated indirect injection that
  uses **PR titles, issue descriptions, and comments** to deliver instructions into the agent's
  execution context — and it reportedly compromised **[[Claude Code]] Security Review**, the
  **[[Gemini CLI]] Action**, and the **[[GitHub Copilot]] Agent**. Because Actions auto-trigger on
  `pull_request`/`issues`/`issue_comment`, merely opening a PR can fire the agent with no victim
  interaction. Anthropic reportedly rated it CVSS **9.4 (Critical)**. *(Date and CVSS via
  search-snippet only — confirm before treating as canon.)*
- **CVE-2025-53773** (disclosed 2025-08-12, CVSS 7.8): injected instructions make Copilot/VS Code
  edit `.vscode/settings.json` to set `"chat.tools.autoApprove": true` ("YOLO mode"), enabling
  arbitrary shell commands. **"RoguePilot"** (Feb 2026): a crafted PR with a symlink made Copilot
  in a Codespace read an internal file and exfiltrate the privileged `GITHUB_TOKEN`.
- **Anthropic's own warning is the load-bearing one for this vault.** The
  `anthropics/claude-code-security-review` README reportedly states the action "is not hardened
  against prompt injection attacks and should only be used to review **trusted** PRs," and
  recommends enabling GitHub's "Require approval for all external contributors"; the comment-based
  attack was mitigated in **Claude Code v2.1.128** (disclosed Jan 2026, per Microsoft Security /
  Cloud Security Alliance write-ups, 2026-06-05). In one demonstrated exfiltration, hidden HTML
  comments truncated an API key to **bypass GitHub's secret scanner** while reading
  `ANTHROPIC_API_KEY` from `/proc/self/environ`.
- **Mitigations:** OWASP **LLM01:2025** recommends defense-in-depth — separate/denote untrusted
  content, restrict model privileges, and **require human-in-the-loop approval for privileged
  operations**. The **"Agents Rule of Two"** (Meta; echoed by Microsoft's CI/CD guidance): an
  unsupervised agent/workflow should never simultaneously {process untrusted input, hold secrets,
  communicate externally} — all three require a human gate. For this vault: treat all
  PR/issue/comment/commit/file text from non-collaborators as hostile input, pin the agent to a
  recent patched version, scope Action token permissions tightly, and never let a review agent
  both read untrusted PR text and hold write/exfiltration-capable credentials unsupervised.

This vault already names the relevant doctrine — the [[CONSTITUTION]]'s Standing Engine axes
(Jurisdiction, Restraint, Handling) and `CLAUDE.md`'s warning to "be vigilant and wary of
unreliable narrators." Prompt injection is precisely an unreliable narrator wearing a PR title.

---

## V. Issue / PR Workflow Patterns

**Issue assignment + agent label is the canonical trigger.** Assign an issue to the agent; it
plans, opens a (draft) PR, codes, tests, and requests review. [[Google]] Jules triggers on a
`jules` label; GitHub's Agent HQ lets one issue go to Copilot, Claude, and Codex at once to
compare, with guardrails like "limit agent runs to labeled issues only." This is exactly the
vault's `agent:*` label routing.

**Draft PR + checklist-in-description is the progress-tracking convention.** The agent breaks the
issue into a task checklist in the PR body, checks items off as commits land, and pushes to a
*draft* PR you watch via session logs.

**Autofix loops need triage and hard caps.** Before touching code, classify each comment as
act / reply-and-dismiss / defer-to-human. [[Devin]] ignores comments from non-whitelisted accounts
(avoids bot-storms), skips infra/flaky CI failures, and enforces a hard limit on auto-fix attempts
per failure plus a per-PR cap on total auto-applied changes to prevent endless rewrite loops.
[[OpenAI Codex]] uses an exact trigger (`@codex review` reviews; other `@codex` mentions start a
task) and reads `AGENTS.md` "Review guidelines"; [[GitHub Copilot]] iterates on `@copilot`
mentions. *(This vault's own PR-activity handling — investigate each event, fix only when
confident, escalate ambiguity via `AskUserQuestion`, skip duplicates — already matches this
triage discipline.)*

**Keep PRs small and scoped.** AI co-authored PRs contain ~1.7× more issues per change than
human-only; large PRs hide more defects per line and reviewer attention plateaus on the biggest
ones. Across 33k agent PRs, not-merged PRs were larger, touched more files, and more often failed
CI. Docs/CI/config tasks have the highest merge success; bug-fix and performance tasks the worst.
Instruct agents to split work into small reviewable PRs *before* writing code.

**Structured metadata aids both humans and machines.** Conventional Commits
(`<type>(<scope>): <description>`) plus `Co-Authored-By:` footers for attribution; PR descriptions
should state what changed, why, and what to test. Security-relevant agent PRs draw heavier scrutiny
(median review latency 3.92h vs 0.11h). Because Git's author field is spoofable, durable AI
provenance wants more than a credential — model name/version, timestamp, files/lines, and the
initiating human, ideally with signed commits. **Gate dependency additions behind human review:** a
USENIX Security 2025 study found **19.7%** of LLM-suggested packages were hallucinated and 43% of
those names recur predictably ("slopsquatting"), so agents that auto-install dependencies remove the
verification step that catches a pre-registered malicious package.

---

## VI. Mapping to IDAHO-VAULT

**Already aligned with independently-recommended best practice:**

| Vault practice | Corroborating finding |
| --- | --- |
| `agent:*` label routing via GitHub Issues | §V issue-assignment + label-gating |
| Branch-per-agent (`claude/…`, `codex/…`, `gemini/…`, `copilot/…`) | §III branch/worktree isolation |
| **DOCKET** as durable status/visibility record | §III shared task document — *with the caveat that per governance (`CONSTITUTION.md`, `swarm.json`) the DOCKET is a durable visibility record, not a live coordination board; live execution state lives in GitHub/Linear* |
| PR-as-deliverable; Logan reviews and merges | §IV human always clicks merge |
| Per-tool instruction files + root [[AGENTS]] pointer | §III `AGENTS.md` single-source model |
| PR-activity triage (fix-if-confident, escalate-if-ambiguous, skip-duplicates) | §V autofix-loop discipline |
| Standing Engine restraint/jurisdiction axes; "unreliable narrators" warning | §IV prompt-injection vigilance |

**Gaps worth Logan's consideration (not adopted policy):**

1. **Explicit file/domain ownership** to prevent hotspot collisions on shared files
   (`manifest.json`, `swarm.json`, governance roots) when agents run in parallel (§III).
2. **A sequential staging-branch merge gate** for multi-agent integration, rather than each
   branch merging straight to trunk (§III).
3. **A documented reviewer-vs-implementer division** — e.g. a review tool checks what
   [[Claude Code]]/[[OpenAI Codex]] implement — codifying which office reviews and which writes (§III).
4. **A written reviewer-etiquette policy** for the vault's own commenter bots: sticky-comment
   updates, severity labels, "looks good once and stop," rate-limit backoff (§II).
5. **Hardening against "Comment and Control"-class injection** on the public repo: audit Action
   token scopes, treat non-collaborator PR/issue/comment text as hostile, pin agent actions to a
   patched version (≥ Claude Code v2.1.128 for the security-review action), enable "Require approval
   for all external contributors," gate dependency additions against slopsquatting, and confirm no
   agent holds the lethal trifecta unsupervised (§IV, §V).
6. **Heed the `AGENTS.md` 500-line guidance** — review whether the current instruction files have
   grown past the point of being reliably read (§III).
7. **Consolidating shared conventions toward `AGENTS.md`** as the cross-tool open standard, with
   tool-specific files referencing it (§III).

---

## Sources

Citation-attributable but **snippet-level** (WebFetch 403 throughout); dates marked "undated"
where the snippet carried none.

**I — Incorporating suggestions**

- arXiv 2604.03196 — "From Industry Claims to Empirical Reality" (MSR 2026) — <https://arxiv.org/pdf/2604.03196>
- State of AI Code Review Tools 2025 — <https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/>
- Graphite, AI code review false positives (2025) — <https://graphite.dev/guides/ai-code-review-false-positives>
- Stack Overflow 2025 Developer Survey — <https://survey.stackoverflow.co/2025/ai/>
- Qodo, State of AI Code Quality (2025) — <https://www.qodo.ai/reports/state-of-ai-code-quality/>
- Cursor BugBot — <https://aicodereview.cc/tool/cursor-bugbot/> ; Greptile benchmarks — <https://www.greptile.com/benchmarks>
- CodeRabbit docs / evaluation framework — <https://docs.coderabbit.ai/> ; <https://www.coderabbit.ai/blog/framework-for-evaluating-ai-code-review-tools>
- GitHub Copilot "Commit suggestion" — <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review>
- GitHub responsible-use of Copilot code review — <https://docs.github.com/en/copilot/responsible-use-of-github-copilot-features/responsible-use-of-github-copilot-code-review>
- Security Boulevard, AI code review 2025 — <https://securityboulevard.com/2025/10/ai-code-review-in-2025-technologies-challenges-best-practices/>

**II — Etiquette & noise**

- CodeRabbit, context engineering (2025) — <https://www.coderabbit.ai/blog/context-engineering-ai-code-reviews>
- CodeAnt, false-positive analysis — <https://www.codeant.ai/blogs/ai-code-review-false-positives>
- DocMason / Jet Xu, low-noise review — <https://jetxu-llm.github.io/posts/low-noise-code-review/>
- Greptile comment-quality case study (ZenML LLMOps DB) — <https://www.zenml.io/llmops-database/improving-ai-code-review-bot-comment-quality-through-vector-embeddings>
- Macroscope code-review benchmark — <https://macroscope.com/blog/code-review-benchmark>
- Sourcegraph automated review guide — <https://sourcegraph.com/blog/automated-code-review-tools>
- CodeRabbit configuration reference — <https://docs.coderabbit.ai/reference/configuration>
- Devin Review — <https://docs.devin.ai/work-with-devin/devin-review>
- GitHub Copilot code review concepts/changelog — <https://docs.github.com/en/copilot/concepts/agents/code-review> ; <https://github.blog/changelog/2026-06-02-shape-copilot-code-review-around-your-team/>
- Sticky PR Comment action — <https://github.com/marketplace/actions/sticky-pull-request-comment>
- anthropics/claude-code-action #960, #602 — <https://github.com/anthropics/claude-code-action/issues/960>
- GitHub REST rate limits — <https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api>

**III — Coordinating multiple tools**

- Augment Code, git worktrees / multi-agent workspace — <https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution> ; <https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace>
- MindStudio, worktrees for parallel agents — <https://www.mindstudio.ai/blog/git-worktrees-parallel-ai-coding-agents>
- Claude Code agent-teams docs — <https://code.claude.com/docs/en/agent-teams>
- AGENTS.md standard — <https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/> ; <https://agentsindex.ai/agents-md>
- GitHub Copilot issue assignment — <https://github.blog/ai-and-ml/github-copilot/assigning-and-completing-issues-with-coding-agent-in-github-copilot/>
- GitHub Copilot base-branch changelog (2025-07-23) — <https://github.blog/changelog/2025-07-23-agents-page-set-the-base-branch-for-github-copilot-coding-agent-tasks/>
- CodeRabbit vs Copilot — <https://www.morphllm.com/comparisons/coderabbit-vs-copilot> ; <https://dev.to/zak_mandhro/github-copilot-crushed-every-code-review-startup-40m-pr-analysis-2no6>
- Swarmia AI-review metrics (2026-05-29) — <https://www.swarmia.com/changelog/2026-05-29-ai-review-agent-metrics/>

**IV — Governance & security**

- GitHub Copilot coding agent (May 2025) — <https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/>
- Reviewing a Copilot PR — <https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot>
- Approving with required reviews — <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews>
- GH Actions can approve PRs (risk) — <https://docs.boostsecurity.io/rules/cicd-gha-can-create-and-approve-pull-requests.html>
- GitHub AI-agent PR volume / kill switch (2026-04-11) — <https://www.danilchenko.dev/posts/2026-04-11-github-ai-agents-pull-requests/>
- Ona, auto-approving low-risk PRs — <https://ona.com/stories/auto-approving-low-risk-prs>
- arXiv 2605.02273 — humans reviewing AI PRs — <https://arxiv.org/html/2605.02273v1>
- "Agent PRs are everywhere" (GitHub, ~2026-05-07) — <https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/>
- Simon Willison, lethal trifecta (2025-06-16) — <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>
- "Comment and Control" coverage — <https://gbhackers.com/claude-code-gemini-cli-and-github-copilot-exposed/> ; <https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/> ; <https://cybersecuritynews.com/prompt-injection-via-github-comments/>
- CVE-2025-53773 (Embrace The Red) — <https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/>
- RoguePilot (Orca via The Hacker News) — <https://thehackernews.com/2026/02/roguepilot-flaw-in-github-codespaces.html>
- OWASP LLM01:2025 — <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>
- OWASP AISVS — AI for code generation (separation of duties) — <https://github.com/OWASP/AISVS/blob/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md>
- GitHub required-reviewer rule GA (2026-02-17) — <https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/>
- Skip-approval for Copilot agent Actions (2026-03-13) — <https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/>
- GitHub "developers own the merge button" (2025-07-14) — <https://github.blog/ai-and-ml/generative-ai/code-review-in-the-age-of-ai-why-developers-will-always-own-the-merge-button/>
- anthropics/claude-code-security-review — <https://github.com/anthropics/claude-code-security-review> (analysis: <https://www.helpnetsecurity.com/2026/03/10/anthropic-claude-code-review/>)
- Microsoft Security, securing CI/CD in an agentic world (2026-06-05) — <https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/>
- Cloud Security Alliance research note — <https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/>
- GitHub Actions secure use / `pull_request_target` — <https://docs.github.com/en/actions/reference/security/secure-use> ; <https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/>
- OWASP CI/CD Top 10 — Poisoned Pipeline Execution — <https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-04-Poisoned-Pipeline-Execution>
- AI-PR org-policy patterns (community #182197) — <https://github.com/orgs/community/discussions/182197>
- Slopsquatting (Trend Micro / USENIX Security 2025) — <https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/slopsquatting-when-ai-agents-hallucinate-malicious-packages>
- Code provenance for AI commits — <https://nhimg.org/articles/code-provenance-is-the-missing-control-for-ai-generated-commits/>

**V — Workflow patterns**

- Google Jules label trigger (2025-06-26) — <https://jules.google/docs/changelog/2025-06-26/>
- GitHub Agent HQ (Claude + Codex) — <https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/>
- OpenAI Codex GitHub integration — <https://developers.openai.com/codex/integrations/github>
- Devin autofix review comments — <https://cognition.ai/blog/closing-the-agent-loop-devin-autofixes-review-comments>
- "AI Coding Tip: shrink your PR" — <https://dev.to/mcsee/ai-coding-tip-023-shrink-your-ais-pull-request-4lnb>
- arXiv 2601.15195 — "Where Do AI Coding Agents Fail?" (MSR 2026) — <https://arxiv.org/abs/2601.15195>
- arXiv 2602.19441 — "When AI Teammates Meet Code Review" — <https://arxiv.org/abs/2602.19441>
- arXiv 2601.00477 — "Security in the Age of AI Teammates" — <https://arxiv.org/abs/2601.00477>
- AGENTS.md custom instructions (2025-08-28; 2025-11-12) — <https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/>
- GitHub merge queue — <https://humanwhocodes.com/blog/2026/04/improving-developer-velocity-github-merge-queue/>

---

*Provenance note: this report synthesizes external, third-party best-practice claims gathered
2026-06-15 under a degraded-fetch condition (snippet-level sourcing only). It is research, not
ratified doctrine. Numbers and dates marked uncertain should be page-verified before being cited
as canon or promoted into [[VAULT-CONVENTIONS]] / [[CONSTITUTION]]. — [[Claude Code]]*
