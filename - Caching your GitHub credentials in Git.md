---
title: "Caching your GitHub credentials in Git"
source: "https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git"
author:
published:
created: 2026-08-12
description: "If you're cloning GitHub repositories using HTTPS, we recommend you use GitHub CLI or Git Credential Manager (GCM) to remember your credentials."
---
## GitHub CLI

GitHub CLI will automatically store your Git credentials for you when you choose `HTTPS` as your preferred protocol for Git operations and answer "yes" to the prompt asking if you would like to authenticate to Git with your GitHub credentials.

1. [Install](https://github.com/cli/cli#installation) GitHub CLI on macOS, Windows, or Linux.
2. In the command line, enter `gh auth login`, then follow the prompts.
	- When prompted for your preferred protocol for Git operations, select `HTTPS`.
		- When asked if you would like to authenticate to Git with your GitHub credentials, enter `Y`.

For more information about authenticating with GitHub CLI, see [`gh auth login`](https://cli.github.com/manual/gh_auth_login).

## Git Credential Manager

[Git Credential Manager](https://github.com/GitCredentialManager/git-credential-manager) (GCM) is another way to store your credentials securely and connect to GitHub over HTTPS. With GCM, you don't have to manually [create and store a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), as GCM manages authentication on your behalf, including 2FA (two-factor authentication).

1. Install Git for Windows, which includes GCM. For more information, see [Git for Windows releases](https://github.com/git-for-windows/git/releases/latest) from its [releases page](https://github.com/git-for-windows/git/releases/latest).

We recommend always installing the latest version. At a minimum, install version 2.29 or higher, which is the first version offering OAuth support for GitHub.

The next time you clone an HTTPS URL that requires authentication, Git will prompt you to log in using a browser window. You may first be asked to authorize an OAuth app. If your account or organization requires [two-factor auth](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa), you'll also need to complete the 2FA challenge.

If you're a member of an enterprise that uses Enterprise Managed Users, your enterprise view has the "Users managed by ACCOUNT NAME" header bar at the top of the screen. In that case you will need to disable account filtering locally in GCM to prevent getting prompted for authentication each time a remote Git operation is performed. For more details, see the [`git-credential-manager` repository](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/configuration.md#credentialgithubaccountfiltering).

To configure the Git Credential Manager run the following command:

```bash
git config --global credential.gitHubAccountFiltering "false"
```

Once you've authenticated successfully, your credentials are stored in the Windows credential manager and will be used every time you clone an HTTPS URL. Git will not require you to type your credentials in the command line again unless you change your credentials.

For more information or to report issues with GCM, see the official GCM docs at [Git Credential Manager](https://github.com/GitCredentialManager/git-credential-manager).