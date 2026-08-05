<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# best practices "Linear.app" project management

Linear works best when you keep it **lean, cyclical, and tightly connected to real product goals**. The core pattern is: set direction, run work in short cycles, keep a manageable backlog, and use projects for bigger initiatives rather than every task.[^1_1][^1_2]

## How to structure work

Use projects for longer-lived outcomes, issues for discrete work items, and cycles for sprint-like execution. Linear’s own docs recommend that projects have a clear start and end, and that you break larger efforts into smaller time-based chunks when needed.[^1_3][^1_4]

## Workflow habits

A good Linear workflow usually starts with triage, then backlog, in progress, review, and done. Keep the status set minimal and meaningful, and make the handoff criteria for each stage clear so people don’t have to guess what “ready” means.[^1_5][^1_6]

## Planning practice

Set useful goals, prioritize blockers and enablers, and scope projects down aggressively. Linear’s method emphasizes concise specs, focused planning, and making sure cycles stay reasonable rather than overloaded.[^1_2][^1_4]

## Team operating rules

- Keep the backlog small and current instead of collecting every idea forever.[^1_1]
- Use recurring project updates so stakeholders stay informed without meetings.[^1_4]
- Automate as much as possible with integrations and templates to reduce manual status churn.[^1_6][^1_5]
- Tie issues to projects and cycles so daily work connects back to strategy.[^1_3][^1_1]


## A practical setup

For a small product team, a solid setup is: one project per major initiative, 1–2 week cycles, issue templates for bugs/features/refactors, and a weekly triage pass to clean the backlog. That gives you enough structure to stay aligned without turning Linear into a heavy PM system.[^1_5][^1_4][^1_1]

Would you like a Linear workflow template for a solo operator, a startup team, or an engineering org?
<span style="display:none">[^1_10][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://linear.app/method/introduction

[^1_2]: https://linear.app/method

[^1_3]: https://linear.app/docs/projects

[^1_4]: https://linear.app/now/how-we-run-projects-at-linear

[^1_5]: https://www.morgen.so/blog-posts/linear-project-management

[^1_6]: https://onehorizon.ai/blog/linear-app-review

[^1_7]: https://linear.app/docs/start-guide

[^1_8]: https://www.youtube.com/watch?v=7oN7aFzfIvQ

[^1_9]: https://www.reddit.com/r/Linear/comments/1h87cou/recommended_workfloworganization_for_managing/

[^1_10]: https://linear.app


---

# AI agent integration?

Linear supports AI agent integration natively through its Agents directory, API, and MCP (Model Context Protocol) for seamless delegation of issues and automation. Agents act as teammates: assign issues to them, @mention in comments, or use them for triage, code gen, and routing.[^2_1][^2_2][^2_3]

## Key Agents

Use these popular agents directly from Linear's directory:

- **Codex**: Delegates issues, generates code/PRs, reviews pull requests.[^2_4][^2_1]
- **Cursor/GitHub Copilot**: Turns issues into code or PRs.[^2_1]
- **Factory/Blocks**: Assigns backlog issues to droids for execution.[^2_1]
- **Sentry Agent/Oz/Warp**: Resolves issues, orchestrates agents.[^2_4][^2_1]


## Setup Steps

Workspace admins install via the Integrations Directory or agent-specific instructions. Assign issues to agents (you stay responsible), and they pull context automatically. Linear's own team uses this for CX triage, bug routing, and initial code passes before human review.[^2_3][^2_4]

## Automation Tools

For broader AI workflows:

- Zapier/n8n/Relay.app: Connect Linear to AI apps without code.[^2_5][^2_6]
- Lindy/Reclaim.ai: AI scheduling and task automation.[^2_5]
- Custom via API: Build agents for code gen or querying (e.g., Relevance AI, Potpie).[^2_7][^2_8]


## Pro Tips

Start small: Delegate repetitive tasks like triage or test plans to free engineers for high-value work. Monitor agent output since humans approve finals. For dev teams, chain agents (e.g., Linear → Codex → Copilot) for end-to-end issue resolution.[^2_9][^2_4]

This fits well with lean PM—agents handle the grind, you focus on strategy. Need setup for a specific agent?[^2_4][^2_1]
<span style="display:none">[^2_10]</span>

<div align="center">⁂</div>

[^2_1]: https://linear.app/integrations/agents

[^2_2]: https://linear.app/agents

[^2_3]: https://linear.app/docs/agents-in-linear

[^2_4]: https://linear.app/now/how-we-use-linear-agent-at-linear

[^2_5]: https://linear.app/integrations/automations

[^2_6]: https://sourceforge.net/software/ai-agent-builders/integrates-with-linear/

[^2_7]: https://marketplace.relevanceai.com/integrations/linear

[^2_8]: https://www.reddit.com/r/AI_Agents/comments/1jbppyc/i_integrated_a_code_generation_ai_agent_with/

[^2_9]: https://linear.app/integrations/ai-clients

[^2_10]: https://www.reddit.com/r/Linear/comments/1ovyym5/ai_tool_for_querying_projects/


---

# How to install AI agents in Linear workspace

Only workspace admins can install AI agents in Linear, treating them as "app users" that integrate like teammates for delegation and @-mentions. Installation happens via the Integrations Directory or agent-specific setup, with control over team access.

## Installation Steps

1. Go to **Settings > Integrations > Agents** (or browse https://linear.app/integrations/agents).
2. Select an agent like Codex, Cursor, or Factory, then follow the developer's setup instructions.
3. Choose teams the agent accesses during install—once done, any team member can use it.
4. Manage via **Settings > Applications** (uninstall) or **Settings > Administration > Members** (suspend).[^3_1]

## Post-Install Usage

Assign issues to agents for delegation (you stay responsible), @mention in comments, or ask for help. Track activity on agent user pages, My issues view, custom views filtered by Delegate, or Insights.

## Customization Tips

Add workspace/team guidance in **Settings > Agents > Additional guidance** (markdown with history) to enforce conventions like repo use or commit formats. Agents don't count as billable seats but check provider pricing.

Agents like Codex delegate issues, GitHub Copilot generates code from them, and Factory assigns backlog work—pick based on needs like code gen or triage.[^3_1]

<div align="center">⁂</div>

[^3_1]: https://linear.app/method/introduction

