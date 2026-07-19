---
source: https://docs.qodo.ai/code-review/migrating-to-qodo-v2
author:
- Qodo Documentation
published: null
created: 2026-03-29
related:
- '2026-03-29'
- Cloud
- GitHub
- ONE
- agent
authority: LOGAN
---
Starting February 4, 2026, new Qodo accounts will not have access to the Qodo v1 code review experience.

This guide explains how you can transition from Qodo v1 to Qodo v2’s new code review experience safely and incrementally. The goal is to let you test and validate the new review behavior before enabling it broadly across your organization. To use the new code review experience, you update your repository configuration and enable new review commands. During migration, you can run the new review alongside existing commands for testing purposes, then remove duplicates once validation is complete.

### Step 1: Update your repository configuration

Configuration for code review lives in your repository’s [configuration](https://docs.qodo.ai/code-review/get-started/configuration-overview). In the `.pr_agent.toml` you can see which review commands are enabled and how feedback is generated.

#### Add the new review commands

In the `git_provider` section (varies depending on your provider), add the new review commands (prefixed with `/agentic`):

```toml
⚠️ Select ONLY ONE section below — the one that matches your git provider.
# Do not include multiple provider sections in the same configuration file.

# GitHub App
[github_app]
pr_commands = [
  "/agentic_describe",
  "/agentic_review"
]

# GitLab
[gitlab]
pr_commands = [
  "/agentic_describe",
  "/agentic_review"
]

# Bitbucket Cloud / App
[bitbucket_app]
pr_commands = [
  "/agentic_describe",
  "/agentic_review"
]

# Bitbucket Server / Data Center
[bitbucket_server]
pr_commands = [
  "/agentic_describe",
  "/agentic_review"
]

# Azure DevOps Server
[azure_devops_server]
pr_commands = [
  "/agentic_describe",
  "/agentic_review"
]
```

The new commands combine and replace multiple legacy commands, including `/improve` `/review` `/describe` & `/compliance`

During testing, both old and new review commands may run in parallel for comparison, but once migration is complete, older commands should be removed to avoid duplicate feedback and noise.

**Optional: Test the new review manually** Manual testing is an optional way to preview the new code review experience before or during configuration. In any pull request comment, enter:

```shellscript
/agentic_describe 
/agentic_review
```

This enables you to:
- Validate the new review output on real pull requests
- Compare results with existing review behavior
- Test without changing repository configuration

Manual invocation is intended for testing and validation.

### Step 2: Enable on a pilot repository

Before rolling out the new code review experience across your organization, we recommend enabling it on a pilot repository. This helps you:
- Evaluate signal quality and noise levels
- Confirm the new review behavior meets expectations
- Adjust configuration if needed
- Remove duplicate commands after validation
**Configuration details** To learn how to configure options such as severity thresholds, display modes, verbosity levels, and ignore rules, see [Configuration](https://docs.qodo.ai/code-review/get-started/configuration-overview) fundamentals.

### Step 3: Enable on entire organization

After you’ve validated the new code review experience in a pilot repository, you can roll it out across your organization by applying the configuration at the organization level. To enable the new review commands across all repositories, define them in the **global organization configuration**: After this change is merged, the configuration applies as the default for all repositories in the organization (unless overridden by a repo-level or wiki configuration).

### Step 4: Remove Qodo v1 configuration

Once you enable the new commands broadly, remove older review commands from any configuration location where they are still defined (wiki, repo-level, or global). See [Configuration](https://docs.qodo.ai/code-review/get-started/configuration-overview) fundamentals for more details.

## What you’ll notice in your PRs

After rollout, review output will be consolidated and more structured:
- Compliance and Code Suggestions will no longer appear as separate outputs (they are incorporated into the new review experience)
- Issues are grouped by priority (for example, Action Required vs Remediation Recommended)
- Findings include clearer explanations and direct references to relevant code
- Reviews include agent-assisted fix prompts to help resolve issues faster
These changes are expected and reflect a more coordinated and prioritized review flow.