---
URL: https://docs.github.com/en/early-access/github/articles/plan-ask-questions-and-iterate-on-code-with-copilot-coding-agent
date-accessed: 2026-03-19
date-published: '[ ? ]'
date-updated: 03/19/2026
related:
- '2026-03-19'
- Copilot
- View
- agent
authority: LOGAN
---
# Plan, ask questions, and iterate on code with Copilot coding agent
Copilot coding agent can now plan, answer questions about your codebase, and make code changes, all from a single conversation.

You can now ask Copilot coding agent to plan or ask questions about your codebase. This feature is available from:

* Agents tab in the repository
* Agents page ([github.com/copilot/agents](https://github.com/copilot/agents))
* Agents panel
* Copilot chat ([github.com/copilot](https://github.com/copilot))

## Code changes

When making code changes with Copilot coding agent, you can choose when Copilot creates a pull request, enabling you to iterate in a more private way until you are ready for a review.

There are two ways to ask Copilot to produce a pull request.

![Animation showing Copilot coding agent entry points and workflows in the product experience](/assets/images/early-access/help/images/coding.gif)

### 1. Upon session completion

When the session completes, click **Create Pull Request**. To build confidence that you are ready for a review, click **Diff** to review your changes. The diff will appear only when the session is complete.

### 2. Indicating in your prompt

Specify in your prompt that you'd like a pull request. For example, you can prompt Copilot "Create a pull request to \[insert your requested fix here]". When Copilot is prompted to create a pull request, you will see **View Pull Request** at the bottom of your session logs.

## Planning

To get started with planning, simply ask Copilot a planning related prompt. For example: "Create a plan for \[your desired project]". You can combine planning with implementation by asking Copilot to implement its plan in a follow-up session.

Unless requested, plans will not output code changes.

![Planning](/assets/images/early-access/help/images/planning.png)

## Questions and answers

Use Copilot coding agent to ask questions about your codebase—useful for understanding unfamiliar code, exploring how a feature is implemented, or getting up to speed on a new area. To get started, simply ask Copilot a question.

### Accessing via Copilot chat

You can also access Q\&A capabilities from Copilot coding agent via Copilot chat. After selecting a repository and asking Copilot to do research, Copilot chat will prompt you for permission to conduct a deep research session.

![Deep research in chat skill](/assets/images/early-access/help/images/deep-research-chat.png)