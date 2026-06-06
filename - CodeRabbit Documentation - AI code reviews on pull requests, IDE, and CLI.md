---
title: "CodeRabbit Documentation - AI code reviews on pull requests, IDE, and CLI"
source: "https://docs.coderabbit.ai/cli"
author:
published:
created: 2026-06-06
description: "Get AI code reviews directly in your CLI before you commit. Catch race conditions, memory leaks, and security vulnerabilities without leaving your development environment."
date created: Saturday, June 6th 2026, 12:14:20 am
date modified: Saturday, June 6th 2026, 12:25:26 am
---

## Review local changes

The CodeRabbit CLI analyzes your uncommitted changes using the same pattern recognition that powers our PR reviews. Review code as you write it, apply suggested fixes instantly, and catch critical issues while you still have full context in memory.

## Key features

## Review uncommitted changes

Catch bugs before they reach your repository. CodeRabbit scans your working directory for race conditions, null pointer exceptions, and logic errors before you commit.

## Apply fixes in one step

Fix simple issues like missing imports or syntax errors instantly. For complex architectural problems, send the full context directly to your AI coding agent.

## Context-aware reviews

Paid plans unlock reviews powered by your team’s codebase history: error handling conventions, architectural patterns, and coding preferences applied automatically to every review.

## Getting started

## Organization selection

The active CodeRabbit organization is the login/default org for browser-based CLI auth. It is used when the current repository resolves to that org, but it is not a silent billing fallback for unrelated local repositories.

During a review, CodeRabbit resolves the current repository first:

- If the repository matches the selected org, the review uses that org.
- If the repository matches a different org you can access, CodeRabbit switches attribution to that org.
- If the repository matches an installed public repo but you do not have access to the owning org, the review uses OSS behavior.
- If the repository cannot be matched to an installed accessible repo, the CLI falls back to limited/free review behavior until CodeRabbit is installed for that repo or org.

To change organizations later, run:

```shellscript
cr auth org
```

`cr auth org` opens sign-in automatically if your local session is missing or expired. Organization switching is not available for self-hosted mode or API key authentication.

## Review modes

The CLI offers three primary review modes to fit your workflow:

```shellscript
# Plain mode (default) - detailed feedback with fix suggestions
cr

# Explicit plain mode
cr --plain

# Agent mode - structured JSON output for Skills and agent integrations
cr --agent

# Interactive mode - terminal UI for manual review
cr --interactive
```

Plain mode displays a finding count and severity summary at the end of each run. If the CLI detects a known agent environment, it suggests re-running with `--agent` for structured JSON output.

## Diagnostics

Run `cr doctor` at any time to verify your local setup. The command checks:

- CLI runtime and version
- Local CodeRabbit storage directory
- Authentication state and auth environment
- Current Git repository and branch metadata
- Auto-update policy
- CodeRabbit backend reachability
- CodeRabbit WebSocket reachability

```shellscript
cr doctor
```

`cr doctor` exits with status code `1` when any check fails. Warnings appear in the report but do not cause a non-zero exit code.

## Working with review results

CodeRabbit analyzes your code and surfaces specific issues with actionable suggestions. Each finding includes the problem location, explanation, and recommended fix.

Example findings include:

- **Race condition detected**: “This goroutine accesses shared state without proper locking”
- **Memory leak potential**: “Stream not closed in error path - consider using defer”
- **Security vulnerability**: “SQL query uses string concatenation - switch to parameterized queries”
- **Logic error**: “Function returns nil without checking error condition first”

### Browse and apply suggestions

In interactive mode, use the arrow keys to navigate to a finding and press enter to see the detailed explanation and suggested fix inline in your CLI.

For simple issues like missing imports, syntax errors, or formatting problems, choose **Apply suggested change** to fix immediately.

### Use AI coding agents

For AI agent integration, see the [AI agent integration](#ai-agent-integration) section for detailed workflow guidance and integration guides.

### Managing comments

- **Ignore**: Hide findings you want to address later
- **Restore**: Click collapsed findings in the sidebar to show again

### Replay stored findings

Run `cr review findings` to re-read the results from the most recent local review without re-running the full analysis. This is useful in multi-step agent loops where a downstream step needs to consume results from a prior review.

### Inspect AI prompts

Run `cr review --show-prompts` to print the AI prompts saved from the most recent local review without triggering a new review. Useful for tuning `--config` instructions or understanding why the model flagged a particular finding.

## AI agent integration

CodeRabbit detects the problems, then your AI coding agent implements the fixes.

**Claude Code users**: Claude Code now supports CodeRabbit through a native plugin. See the [Claude Code integration guide](https://docs.coderabbit.ai/cli/claude-code-integration) for the recommended plugin-based setup using `/coderabbit:review` instead of the CLI commands shown below.

### Integration guides

See detailed workflows for AI coding agents and workflows:

## [CodeRabbit Skills](https://docs.coderabbit.ai/cli/skills)

The fastest way to get started — install agent-native Skills and trigger reviews with natural language: “Review my code.”

## [Headless CLI integration](https://docs.coderabbit.ai/cli/headless-cli-integration)

Authenticate CodeRabbit non-interactively in GitHub Actions and other bot-driven automation

### Example prompt for your AI agent

Here’s a complete prompt you can use with Cursor, Codex, or other AI coding agents:

```text
Please implement phase 7.3 of the planning doc and then run cr --agent, let it run as long as it needs (run it in the background) and fix any issues.
```

### Components of a good prompt

Breaking down what makes an effective CodeRabbit + AI agent workflow:

1\. Run CodeRabbit CLI

Tell your AI agent to run CodeRabbit with the `--agent` flag:

```shellscript
cr --agent
```

You can also specify review types or branches:

```shellscript
# Review only uncommitted changes
cr --agent --type uncommitted

# With specific base branch
cr --agent --base develop
```

2\. Run in the background

CodeRabbit reviews can take 7-30+ minutes depending on the scope of changes. Instruct your AI agent to run CodeRabbit in the background and set up a timer to check periodically:

```text
Run cr --agent --type uncommitted in the background, let it take as long as it needs, and check on it periodically.
```

3\. Evaluate and implement fixes

Once CodeRabbit completes, have your AI agent evaluate the findings and prioritize:

```text
Evaluate the fixes and considerations. Fix major issues only, or fix any critical issues and ignore the nits.
```

This keeps your agent focused on meaningful improvements rather than minor style issues. If the `complete` event has `status: "review_skipped"`, there were no file changes in scope.

4\. Verify with a second pass

Run CodeRabbit one more time to ensure fixes didn’t introduce new issues:

```text
Once those changes are implemented, run cr --agent one more time to make sure we addressed all the critical issues and didn't introduce any additional bugs.
```

5\. Set loop limits

Prevent infinite iteration by setting clear completion criteria:

```text
Only run the loop twice. If on the second run you don't find any critical issues, ignore the nits and you're complete. Give me a summary of everything that was completed and why.
```

This ensures your AI agent completes the task efficiently and provides a clear report.

## Pricing and capabilities

See the [rate limits table on the Plans and pricing page](https://docs.coderabbit.ai/management/plans#rate-limits) for current per-plan limits. To increase the limits, consider upgrading your plan or using the [Usage-based Add-on](#cli-with-usage-based-add-on).

## Free tier

Basic static analysis with limited daily usage. Catches syntax errors, logic issues, and security vulnerabilities. Eligible Free users may see a Pro+ trial prompt after sign-in or when a CLI review reaches the rate limit.

## Paid plans

Enhanced reviews powered by learnings from your CodeRabbit organization plus higher rate limits and more files per review. Paid users reviewing repositories connected to that organization get:

- **Learnings-powered reviews**: Remembers your team’s preferred patterns for error handling, state management, and architecture
- **Full contextual analysis**: Understands your imports, dependencies, and project structure
- **Team standards enforcement**: Applies your documented coding guidelines automatically
- **Advanced issue detection**: Spots subtle race conditions, performance bottlenecks, and security vulnerabilities

## Usage-based Add-On (Pay-as-you-Go)

Continues eligible CodeRabbit CLI reviews after rate limits

- Assigned-seat users use their plan allowance first
- Credits are charged only for eligible over-limit reviews
- Full control over usage and scaling through the dashboard
- Flexible purchase options (one-time & monthly subscription)

Contact [sales@coderabbit.ai](mailto:sales@coderabbit.ai) for custom rate limits or enterprise needs.

## CLI with Usage-based Add-on

The usage-based add-on lets eligible CodeRabbit CLI reviews continue after the applicable review limit is reached. Authenticated CLI and agentic API-key reviews use the assigned user’s plan allowance first. Credits are charged only when a review continues over that limit. Each reviewed file in the over-limit review costs **$0.25** in credits. You can purchase credits as a one-time top-up or a recurring monthly subscription from the [Subscription and Billing](https://app.coderabbit.ai/settings/subscription) dashboard.

## Command reference

See the [CLI Command Reference](https://docs.coderabbit.ai/cli/reference) for a complete list of commands and options.

## Uninstall

Remove CodeRabbit CLI based on how you installed it.

```shellscript
rm $(which coderabbit)
```

```shellscript
brew remove coderabbit
```

[Skills](https://docs.coderabbit.ai/cli/skills)