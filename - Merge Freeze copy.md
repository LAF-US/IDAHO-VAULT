---
title: "Merge Freeze"
source: "https://app.mergefreeze.com/installations/5238/branches/10977?tab=api"
author:
published:
created: 2026-07-01
description: "Stop team members from merging and deploying. For one-off situations or at set times."
---
![](https://avatars.githubusercontent.com/u/275429250?v=4) LAF-US ![user](https://avatars.githubusercontent.com/u/136375980?v=4)

> [!success] Success
> Access token successfully updated.

![GitHub](https://app.mergefreeze.com/assets/app/github-1940ef69572443d7ba085e82cb81af49c0b8e4b8.png)

[LAF-US/IDAHO-VAULT main](https://github.com/LAF-US/IDAHO-VAULT/pulls) Unfrozen

Edit

### Scheduled Freezes

Scheduled freezes let you set a schedule of times when merging is forbidden, for example every week night after 5pm.

Recurring schedules

<table><thead><tr><th>Freezes</th><th>Unfreezes</th><th>Description</th><th>Next Freeze Occurs</th><th>Actions</th></tr></thead><tbody><tr><td colspan="5">No Scheduled Freezes set</td></tr></tbody></table>

One-time freezes

<table><thead><tr><th>Starts</th><th>Ends</th><th>Description</th><th>Actions</th></tr></thead><tbody><tr><td colspan="4">No One-Time Freezes set</td></tr></tbody></table>

### Freeze Method

There are two ways to implement a merge freeze. [Read the docs](https://docs.mergefreeze.com/frequently-asked-questions#how-come-people-can-still-merge-even-though-i-have-frozen-my-project)

### Web API

The web API provides access to view the freeze status of projects, create new projects, toggle freezes on and off, and schedule one-off freezes. [Read the docs](https://docs.mergefreeze.com/web-api)

`[REDACTED]`

Get branch details

`curl https://app.mergefreeze.com/api/branches/LAF-US/IDAHO-VAULT/main/?access_token=`

Freeze / Unfreeze

`curl -d "frozen=true&user_name=Example User&note=testing freeze api" -X POST https://app.mergefreeze.com/api/branches/LAF-US/IDAHO-VAULT/main/?access_token=`

Freeze / Unfreeze a specific PR

`curl -d "frozen=true&user_name=Example User&unblocked_prs=[3]" -X POST https://app.mergefreeze.com/api/branches/LAF-US/IDAHO-VAULT/main/?access_token=`

Example response

```
{
"branch": main,
"repository": LAF-US/IDAHO-VAULT,
"frozen": true,
"frozen_by": "Example User"
}
```

### Access Control

Restrict "freeze/unfreeze" Web and API access to certain members in your GitHub repository. Access control can be managed by the user's repository access. [Learn more](https://docs.mergefreeze.com/connecting-to-github#who-can-implement-a-merge-freeze)

### Freeze Logs

No Freeze Logs found

<iframe allow="clipboard-write; web-share" src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>