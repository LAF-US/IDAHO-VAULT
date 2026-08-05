---
title: "Frequently asked questions"
source: "https://docs.mergefreeze.com/frequently-asked-questions#how-come-people-can-still-merge-even-though-i-have-frozen-my-project"
author:
published: 2025-01-13
created: 2026-07-02
description:
---
## What GitHub permissions does the app require?

### Repository permissions

**Administration: Read and write.** This is so we can add and remove protected branch rules on a repository when the "Toggle a protected branch" freeze method is being used.

**Metadata: Read-only.** So we can see which repositories a user has access to.

**Pull requests: Read-only.** So we know which pull requests to send commit statuses to when using the "Update all pull requests" freeze method.

**Commit statuses: Read and write.** So we can update commit statuses to either success or failure when using the "Update all pull requests" freeze method.

We're not able to read or write to your repository's code base.

### Organization permissions

**Members: Read only.** So we can determine a logged in user's role within an organization (an organization administrator has access to more settings in the Merge Freeze UI).

### User authorization permissions

We don't ask for any extra permissions at the user level beyond what is required to login via GitHub.

## Is self-hosted GitHub Enterprise supported?

Unfortunately we don’t yet support self-hosted GitHub Enterprise instances.

GitHub marketplace apps can’t be installed on self-hosted GitHub instances. Apps for these instances require a complex setup involving creating a new app on the self-hosted instance with all the same permissions and webhook configuration as the app found in the GitHub Marketplace.

The app’s code needs to be told the url of the self-hosted GitHub instance and is then run in either a container on the privately hosted machine, or it runs in the cloud (like the marketplace app) and is allowed to connect to the private server.

Both options involve complexity that we have decided not to undertake yet. We apologize to anyone who’s affected by this and hope to have a solution some time in the future.

## When I try and subscribe to a paid plan all I see is “Unfortunately, invoiced customers cannot purchase paid plans on the GitHub Marketplace.”

When an invoiced GitHub account tries to sign up for a subscription to Merge Freeze via the GitHub marketplace they are sadly met with the following message: “Unfortunately, invoiced customers cannot purchase paid plans on the GitHub Marketplace.”

We offer payment via Stripe for these customers. To do this you’ll need to **first sign up to the Open source plan** (which is free). Then visit your Installation's settings page by choosing Settings from the organizations menu.

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2F3804452385-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-Lq5EXtrdrxFiGoaLv7h%252Fuploads%252FniOinhm50SbnL6uwSQaG%252Fimage.png%3Falt%3Dmedia%26token%3D5ac4190a-d9a4-4a4a-b6cb-5d5ad268743e&width=768&dpr=3&quality=100&sign=baedb34f&sv=2)

On this page you'll see the option to start a free trial via credit card or ACH in the bottom left of the Plans section:

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2F3804452385-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-Lq5EXtrdrxFiGoaLv7h%252Fuploads%252F7VvWFw03BMAmzkGK4H2X%252Fimage.png%3Falt%3Dmedia%26token%3D31df80f6-5bf6-41eb-9e76-d11a2651c7bb&width=768&dpr=3&quality=100&sign=7c44281b&sv=2)

After choosing a plan (Reactive or Proactive) you'll be able to add a payment method and begin a 14 day free trial.

If you prefer to pay annually for a discount, simply start a free trial on a monthly plan, then modify your plan when the Installation view refreshes. From this portal you may upgrade, downgrade, switch to annual billing, and download previous invoices.

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2F3804452385-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-Lq5EXtrdrxFiGoaLv7h%252Fuploads%252FYPNMAFydSIUbiai831uG%252Fimage.png%3Falt%3Dmedia%26token%3D6db64f34-9abe-4d3b-8a39-22505c72dc0f&width=768&dpr=3&quality=100&sign=e06b71bf&sv=2)

## How do I fix a pull request that has a Merge Freeze status check that’s stuck on pending?

If a pull request is created or updated in GitHub it will send Merge Freeze a webhook. Merge Freeze then tries to find the current status of the relevant project (frozen or unfrozen) and sends the pull request a status update via the GitHub API.

If a network error occurs so that the webhook never reaches Merge Freeze, or some other error occurs so that the status update doesn’t make it to GitHub then the Merge Freeze status can be left in a “pending” state with a message that says something like “Expected - Waiting for status to be received”.

To fix this you can either send an update to your pull request so that it triggers another webhook, or you can force Merge Freeze to send another status update to all open pull requests by toggling a freeze off and on again.

New commits can be made to a repository without having to make code changes using the `--allow-empty` flag e.g.

```
git commit --allow-empty -m "Trigger update"
```

## Merge Freeze no longer updates the status of my pull request

It turns out that no single commit id can be given more than 1000 status updates from the same context (you can consider Merge Freeze to be a context). So if you have an old pull request that has been sitting there without any new commits it’s possible with many freezes and unfreezes that this limit is hit.

To fix this you’ll need to send a new commit to the pull request. New commits can be made to a repository without having to make code changes using the `--allow-empty` flag e.g.

```
git commit --allow-empty -m "Trigger update"
```

## Why does it take so long for all PRs to get updated when freezing / unfreezing?

If you’re using the default “Push a status update to all PRs” method of freezing then every time a project is frozen or unfrozen we need to make an API call to every open pull request.

These updates must be done serially, according to GitHub [app rules](https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits). If you have many open pull requests it may take some time to update them all (roughly one second per pull request).

If you have many pull requests that need updating you may wish to switch to the “Toggle a branch protection rule” method of freezing. This can be done in a project’s settings under “Freeze method.”

## How come people can still merge even though I have frozen my project?

By default GitHub will still let you merge even when status checks fail:

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2Fgblobscdn.gitbook.com%2Fassets%252F-Lq5EXtrdrxFiGoaLv7h%252F-Lzmv6k3Awb1EPejxZik%252F-Lzmvc53SzXK3oyvZ1G_%252Fgithub-mergefreeze-canmerge.png%3Falt%3Dmedia%26token%3Dc4c2adb4-065c-4419-ab4a-8789ad9f7e57&width=768&dpr=3&quality=100&sign=482818d1&sv=2)

To block merging completely: In your GitHub repository head to **Settings** -> **Branches** -> **Protected branches** and choose the branch that you'd like to be able to freeze (e.g. master).

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2Fgblobscdn.gitbook.com%2Fassets%252F-Lq5EXtrdrxFiGoaLv7h%252F-Lzmv6k3Awb1EPejxZik%252F-LzmvlIaydjfMnD3svob%252Fgithub-mergefreeze-step1.png%3Falt%3Dmedia%26token%3Dde9835e5-3c8f-4ef7-b299-a96eebbdc00c&width=768&dpr=3&quality=100&sign=9330117&sv=2)
- Check **Protect this branch**.
- Check **Require status checks to pass before merging**.
- Under **Status checks found in the last week for this repository** check **mergefreeze**.
- Optionally check **Include administrators** if you want admins to obey the rules too.
- Click **Save changes**
![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2Fgblobscdn.gitbook.com%2Fassets%252F-Lq5EXtrdrxFiGoaLv7h%252F-Lzmv6k3Awb1EPejxZik%252F-Lzmvt568QskU2rqEhR3%252Fgithub-mergefreeze-step2.png%3Falt%3Dmedia%26token%3Dd7991f8f-d50b-45f6-b70f-5fa7155883b5&width=768&dpr=3&quality=100&sign=c694b7b4&sv=2)

Now when the branch is frozen users will not be able to merge:

![](https://docs.mergefreeze.com/~gitbook/image?url=https%3A%2F%2Fgblobscdn.gitbook.com%2Fassets%252F-Lq5EXtrdrxFiGoaLv7h%252F-Lzmv6k3Awb1EPejxZik%252F-Lzmw1PiB19KBE3OH4Wn%252Fgithub-mergefreeze-cannot-merge.png%3Falt%3Dmedia%26token%3D9617b081-27ff-4fa2-b246-5ed0840f9d20&width=768&dpr=3&quality=100&sign=4a97c1c8&sv=2)

## Do I need to invite other users to my Merge Freeze project?

You don’t need to specifically invite users to your Merge Freeze project to allow them to freeze / unfreeze projects.

Merge Freeze uses GitHub permissions system to decide which projects a user should have access to. It does this by using the GitHub API to fetch all repositories that have the Merge Freeze app installed and that the user is a member of. These will automatically show in the user’s Merge Freeze control panel when they login.

## I want to freeze / unfreeze all of my repositories at the same time

You can batch freeze or unfreeze by selecting multiple projects on the Dashboard. GitHub only allows one update per second for each open pull request, however, so using this may lead to long update times if you update all PRs in every repository of your organization.

For reasons stated above, please be careful with this feature. Alternatively, consider using the Merge Freeze [API](https://docs.mergefreeze.com/web-api#post-freeze-status) with an [organization level access token](https://docs.mergefreeze.com/web-api#organization-access-tokens-organizations-only) to loop through each of your repos and freeze them 1 at a time programmatically, keeping in mind that a 1 req/sec [rate-limit](https://docs.mergefreeze.com/web-api#rate-limits) applies.

Last updated