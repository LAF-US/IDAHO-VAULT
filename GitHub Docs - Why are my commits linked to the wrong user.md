---
title: "Why are my commits linked to the wrong user?"
source: "https://docs.github.com/en/pull-requests/committing-changes-to-your-project/troubleshooting-commits/why-are-my-commits-linked-to-the-wrong-user"
author:
published:
created: 2026-04-26
description: "GitHub uses the email address in the commit header to link the commit to a GitHub user. If your commits are being linked to another user, or not linked to a user at all, you may need to change your local Git configuration settings, add an email address to your account email settings, or do both."
---
## Commits are linked to another user

If your commits are linked to another user, that means the email address in your local Git configuration settings is connected to that user's GitHub account. In this case, you can change the email in your local Git configuration settings and add the new email address to your account to link future commits.

1. To change the email address in your local Git configuration, follow the steps in [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-in-git). If you work on multiple machines, you will need to change this setting on each one.
2. Add the email address from step 2 to your account settings by following the steps in [Adding an email address to your GitHub account](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/adding-an-email-address-to-your-github-account).

Commits you make from this point forward will be linked to your account.

## Commits are not linked to any user

If your commits are not linked to any user, the commit author's name will not be rendered as a link to a user profile. To check the email address used for those commits and connect commits to your account, take the following steps.

1. On GitHub, navigate to the main page of the repository.
2. On the main page of the repository, above the file list, click **commits**.
	![Screenshot of the main page for a repository. A clock icon and "178 commits" is highlighted with an orange outline.](https://docs.github.com/assets/cb-48469/mw-1440/images/help/commits/commits-page.webp)
3. To navigate to a specific commit, click the commit message for that commit.
	![Screenshot of a commit in the commit list for a repository. "Update README.md" is highlighted with an orange outline.](https://docs.github.com/assets/cb-17733/mw-1440/images/help/commits/commit-message-link.webp)
4. To read a message about why the commit is not linked, hover over the blue to the right of the username.
	- **Unrecognized author (with email address)** If you see this message with an email address, the address you used to author the commit is not connected to your GitHub account. To link your commits, [add the email address to your GitHub email settings](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/adding-an-email-address-to-your-github-account). If the email address has a Gravatar associated with it, the Gravatar will be displayed next to the commit, rather than the default gray Octocat.
		- **Unrecognized author (no email address)** If you see this message without an email address, you used a generic email address that can't be connected to your GitHub account. You will need to [set your commit email address in Git](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address), then [add the new address to your GitHub email settings](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/adding-an-email-address-to-your-github-account) to link your future commits. Old commits will not be linked.
		- **Invalid email** The email address in your local Git configuration settings is either blank or not formatted as an email address. You will need to [set your commit email address in Git](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address), then [add the new address to your GitHub email settings](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/adding-an-email-address-to-your-github-account) to link your future commits. Old commits will not be linked.