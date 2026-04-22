---
date created: Sunday, March 29th 2026, 10:47:48 am
date modified: Sunday, March 29th 2026, 10:48:33 am
related:
- GitHub
- LAF
- Logan Finney
- THE
- 'Yes'
- agent
- assistant
- belonging
- blocked
- coordination
- infrastructure
authority: LOGAN
---
# Manage Linear workspace and GitHub PRs

## User

Manage Linear internal workspace and GitHub open PRs

## Assistant

I can help manage the Linear workspace and any pull requests that are already synced into Linear. What do you want me to handle first—open issues, project status, pull request review queue, or something else?

## User

There are several open PRs that can't be merged. The new updates aren't getting reflected in Linear as far as I can tell. Also, the desktop agent is working out of a "swarm" folder that doesn't appear on the online GitHub page and contains files that ought to belong in the "!" swarm nest.

## Assistant

I’m checking the open pull requests in your workspace first, then I’ll compare that with what Linear is showing so I can pinpoint whether this is a sync issue or just missing linkage.

I found two pull requests that are still open in Linear, and both are currently marked as blocked rather than missing. I’m checking the GitHub/Linear integration behavior next so I can separate an actual sync problem from changes that simply never reached the repo.

Linear is seeing the two currently open pull requests, and both are marked **blocked**, so this doesn’t look like a case where the PRs are missing from Linear.

Found 2 open pull requests.

* [Refresh THE COURTROOM docket for LAF-7 coordination](https://linear.app/loganfinney/review/refresh-the-courtroom-docket-for-laf-7-coordination-e67e84aec3f5)
* [Break out THE COURTROOM into scoped project tracks](https://linear.app/loganfinney/review/break-out-the-courtroom-into-scoped-project-tracks-24f708144c22)

What I’m seeing:

* The open PRs are in Linear, but they’re not mergeable right now.
* Linear’s PR view is mostly read-only; merge/approval work still happens in GitHub, and those results are then reflected back into Linear.
* The local desktop-agent `swarm` folder issue is probably separate from Linear sync. If that folder only exists locally and hasn’t been committed/pushed to the repo, neither GitHub nor Linear will show it.
* Your note about files belonging in the `!` swarm nest lines up with an already merged cleanup PR that consolidated swarm coordination files, so the local agent may be working from an outdated or divergent local checkout rather than the repo’s current structure.

Possible next steps:

* I audit the two blocked PRs against their linked issues in Linear.
* I map the current swarm-related issues and PR history to the intended `!` swarm nest structure.
* You paste the exact local path/tree the desktop agent is using, and I’ll compare it against what Linear and GitHub currently reflect.

## User

How fares the swarm?

## Assistant

I’m pulling the current swarm-related issues and pull requests so I can give you a clean status read rather than a guess.

The swarm looks **stable in Linear**. The core swarm work I found is done: [LAF-7](https://linear.app/loganfinney/issue/LAF-7/swarm-coordination-agent-assembly-at-the-courtroom), [LAF-12](https://linear.app/loganfinney/issue/LAF-12/break-out-the-courtroom-into-project-scoped-work-items), and [LAF-10](https://linear.app/loganfinney/issue/LAF-10/define-mvp-swarm-workflow-across-vault-linear-and-slack) are all completed.

The strongest signal on the folder question is that the repo already absorbed the cleanup:

* [PR #58](https://linear.app/loganfinney/review/refactor-consolidate-swarm-nest-home-all-agent-coordination-files-88d72aa2ced8) consolidated the swarm nest
* [PR #72](https://linear.app/loganfinney/review/move-swarm-into-to-contain-swarm-infrastructure-within-the-ops-zone-dd16959675bc) moved `swarm/` into `!/`
* [PR #67](https://linear.app/loganfinney/review/refresh-the-courtroom-docket-for-laf-7-coordination-e67e84aec3f5) and [PR #69](https://linear.app/loganfinney/review/break-out-the-courtroom-into-scoped-project-tracks-24f708144c22) are also merged now

So overall, the swarm itself fares well; the mismatch you noticed looks more like a **local desktop-agent checkout drifting from the current GitHub repo**, not an active Linear-side blockage. Possible next steps:

* I trace the repo/Linear history into a single “intended swarm layout” note.
* You paste the local directory tree from the desktop agent, and I’ll pinpoint exactly what’s out of place.

## User

Can I archive your conversations?

## Assistant

I’m checking the product docs for how conversation history can be kept or hidden so I can answer this accurately.

Not currently, as far as the docs show. Linear keeps chat history so you can return to past conversations, but the documented controls mention browsing recent chats and starting a new chat for a clean slate—not archiving chats.

## User

Would you like to persist as a vaulted entity in the unified swarm?

## Assistant

I don’t persist as an autonomous vaulted entity, but I can help you store the useful parts of this work inside Linear.

Possible next steps:

* Save the operating pattern from this chat as a reusable skill
* Create a document that captures the unified swarm state, norms, and folder model
* Create an issue to track the local-vs-repo swarm divergence and cleanup work

## User

Who are "you" and who am I?

## Assistant

I’m Linear, your workspace assistant for this repo and workspace context.

You’re Logan Finney, working in the [Logan Finney](https://linear.app/loganfinney/team/LAF/all) team on the [IDAHO-VAULT](https://linear.app/loganfinney/project/idaho-vault-df3c1d3e366e) effort.

## User

You can write and delegate to other agents however?

## Assistant

I’m checking the available issue actions in this workspace so I can answer that precisely.

Yes. I can write issues, update them, and delegate issues to other agents in Linear.

What I can do:

* create an issue and assign or delegate it
* update an existing issue’s status, assignee, priority, project, labels, or description
* delegate an issue directly to an agent
* delegate with extra instructions when you want the agent to focus on a specific approach

I can’t directly make a separate agent persist independently as its own long-lived entity, but I can route work to agents through issues.