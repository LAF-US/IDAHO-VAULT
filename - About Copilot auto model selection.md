---
title: "About Copilot auto model selection"
source: "https://docs.github.com/en/copilot/concepts/models/auto-model-selection"
author:
published:
created: 2026-08-10
description: "Automatically select the best model for each task."
---
## Overview

More than just a model picker, auto model selection is an intelligent system delivering high quality results, better reliability, and one less decision to make as the model landscape rapidly evolves.

### Auto with task optimization

Auto model selection with task optimization combines two systems to provide high quality results and better reliability. One system tracks real-time system health and availability, while the other evaluates task complexity. Putting these together, auto model selection routes the task to the optimal model.

Routing occurs along natural cache boundaries to avoid additional cache related costs. Switching models mid-session has shown increased cost without ample improvements in quality. This helps you get more value from Copilot since it matches each task to the model that can solve it most efficiently. That means reserving higher-cost reasoning models for problems that truly need it, while routing straightforward tasks to faster, lower-cost models that still deliver great results.

Benefits of using auto model selection include:

- Matching each task to the model that can solve it most efficiently.
- Model choice based on real-time system health and availability.
- Language invariance: Routing decisions depend on what you are trying to do, not what language you're asking in.
- Improved cost efficiency due to intelligent task routing.

### Auto optimized for model reliability and availability

Experience less rate limiting by letting auto model selection choose the best available model on your behalf.

Auto model selection, optimized for model reliability and availability, intelligently chooses models based on real-time system health and model performance. You benefit from:

- Reduced rate limiting
- Lower latency and errors

### Policies and availability

When you select **Auto**, auto model selection chooses from supported models, subject to your policies and subscription type. Available models may change over time. See [Supported AI models in GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models#supported-ai-models-in-auto-model-selection).

Auto model selection **won't** include these models:

- Models not available in your plan.
- Models excluded by administrator policies. See [Configuring access to AI models in GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-access-to-ai-models).
- Models excluded by policies restricting Copilot to data-resident or FedRAMP-compliant models.
- Models excluded by policies restricting [Evaluation models](https://docs.github.com/en/copilot/reference/ai-models/supported-models#evaluation-models).

### Disabling evaluation models in auto model selection

Auto model selection may serve evaluation models to users on Copilot plans for individuals. Individuals can disable use of these models at any time. See [Supported AI models in GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models#evaluation-models).

### Discount for using auto model selection

If you are on a paid Copilot plan, you qualify for a 10% discount on model costs while using auto model selection in Copilot Chat, Copilot CLI, GitHub Copilot app, or Copilot cloud agent.

## Auto model selection in Copilot

Auto model selection, with task optimization, is generally available in these Copilot products:

- Copilot Chat, on the GitHub website and supported IDEs
- Copilot CLI
- Copilot cloud agent
- GitHub Copilot app

### Copilot Chat in IDEs

Auto model selection, with task optimization, is generally available in the following IDEs:

- VS Code

Auto model selection, optimized for model reliability and availability, is generally available in the following IDEs:

- JetBrains IDEs
- Eclipse
- Xcode

Auto model selection, optimized for model reliability and availability, is in public preview in the following IDEs:

- Visual Studio

#### Enabling access during public preview

During the public preview, if you're using a Copilot Business or Copilot Enterprise plan, the organization or enterprise that provides your plan must have the **Editor preview features** policy enabled. See [Managing policies and features for GitHub Copilot in your organization](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies#enabling-copilot-features-and-models-in-your-organization) or [Managing policies and features for GitHub Copilot in your enterprise](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies#defining-policies-for-your-enterprise).

## Auto model selection in third-party agents

When you select **Auto** in the OpenAI Codex or Anthropic Claude coding agents, Auto model selection chooses from the supported list of models, subject to your policies and subscription type.

### OpenAI Codex supported models

These models are available for Auto model selection in the OpenAI Codex coding agent.

For more information, see [OpenAI Codex](https://docs.github.com/en/copilot/concepts/agents/openai-codex).

### Anthropic Claude supported models

These models are available for Auto model selection in the Anthropic Claude coding agent.

For more information, see [Anthropic Claude](https://docs.github.com/en/copilot/concepts/agents/anthropic-claude).