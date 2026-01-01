---
title: "Creating rulesets for a repository"
source: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#using-fnmatch-syntax"
author:
published:
created: 2026-06-11
description: "You can add rulesets to a repository to control how people can interact with specific branches and tags."
---
## Introduction

You can create rulesets to control how users can interact with selected branches and tags in a repository. You can control things like who can push commits to a certain branch and how the commits must be formatted, or who can delete or rename a tag. You can also prevent people from renaming repositories.

You can also create push rulesets to block pushes to a private or internal repository and the repository's entire fork network. Push rulesets allow you to block pushes based on file extensions, file path lengths, file and folder paths, and file sizes.

When you create a ruleset, you can allow certain users to bypass the rules in the ruleset.

For more information on rulesets, see [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

For customers on GitHub Team and GitHub Enterprise plans you can also create rulesets for repositories in an organization. For more information, see [Creating rulesets for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization).

## Importing prebuilt rulesets

To import one of the prebuilt rulesets by GitHub, see [`github/ruleset-recipes`](https://github.com/github/ruleset-recipes).

You can import an existing ruleset using a JSON file. This can be useful if you want to apply the same ruleset to multiple repositories or organizations. For more information, see [Managing rulesets for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-rulesets-for-repositories-in-your-organization#importing-a-ruleset).

## Using fnmatch syntax

You can use `fnmatch` syntax to define patterns to target when you create a ruleset.

You can use the `*` wildcard to match any string of characters. Because GitHub uses the `File::FNM_PATHNAME` flag for the `File.fnmatch` syntax, the `*` wildcard does not match directory separators (`/`). For example, `qa/*` will match all branches beginning with `qa/` and containing a single slash, but will not match `qa/foo/bar`. You can include any number of slashes after `qa` with `qa/**/*`, which would match, for example, `qa/foo/bar/foobar/hello-world`. You can also extend the `qa` string with `qa**/**/*` to make the rule more inclusive.

For more information about syntax options, see the [fnmatch documentation](https://ruby-doc.org/core-2.5.1/File.html#method-c-fnmatch).

### Unsupported fnmatch syntax

Not all expressions from the `fnmatch` syntax are supported in branch protection rules. Please be aware of the following constraints:

- You cannot use the backslash (`\`) character as a quoting character, as GitHub does not support the use of backslashes in branch protection rules.
- You can specify character sets within square brackets (`[]`), but you cannot currently complement a set with the `^` operator (e.g., `[^charset]`).
- Although GitHub supports `File::FNM_PATHNAME` in `fnmatch` syntax, `File::FNM_EXTGLOB` is not supported.

## Using ruleset enforcement statuses

While creating or editing your ruleset, you can use enforcement statuses to configure how your ruleset will be enforced.

You can select any of the following enforcement statuses for your ruleset.

- **Active:** your ruleset will be enforced upon creation.
- **Disabled:** your ruleset will not be enforced.

## Creating a branch or tag ruleset

1. On GitHub, navigate to the main page of the repository.
2. Under your repository name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then click **Settings**.
 ![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/cb-28260/mw-1440/images/help/repository/repo-actions-settings.webp)
3. In the left sidebar, under "Code and automation," click **Rules**, then click **Rulesets**.
 ![Screenshot of the sidebar of the "Settings" page for a repository. The "Rules" sub-menu is expanded, and the "Rulesets" option is outlined in orange.](https://docs.github.com/assets/cb-80504/mw-1440/images/help/repository/rulesets-settings.webp)
4. Click **New ruleset**.
5. To create a ruleset targeting branches, click **New branch ruleset**. Alternatively, to create a ruleset targeting tags, click **New tag ruleset**.
6. Under "Ruleset name," type a name for the ruleset.
7. Optionally, to change the default enforcement status, click **Disabled** and select an enforcement status.

### Granting bypass permissions for your branch or tag ruleset

You can grant certain roles, teams, or apps bypass permissions for your ruleset. The following are eligible for bypass access:

- Repository admins, organization owners, and enterprise owners
- The maintain or write role, or custom repository roles based on the write role
- Teams, excluding secret teams. See [About organization teams](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams#team-visibility).
- GitHub Apps
- Dependabot. For more information about Dependabot, see [Dependabot quickstart guide](https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide).

1. To grant bypass permissions for the ruleset, in the "Bypass list" section, click **Add bypass**.
2. In the "Add bypass" modal dialog that appears, search for the role, team, or app you would like to grant bypass permissions, then select the role, team, or app from the "Suggestions" section and click **Add Selected**.
3. Optionally, to grant bypass to an actor without allowing them to push directly to a repository, to the right of "Always allow," click , then click **For pull requests only**.
 The selected actor is now required to open a pull request to make changes to a repository, creating a clear trail of their changes in the pull request and audit log. The actor can then choose to bypass any branch protections and merge that pull request.

### Choosing which branches or tags to target

To target branches or tags, in the "Target branches" or "Target tags" section, select **Add a target**, then select how you want to include or exclude branches or tags. You can use `fnmatch` syntax to include or exclude branches or tags based on a pattern. For more information, see [Using `fnmatch` syntax](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#using-fnmatch-syntax).

You can add multiple targeting criteria to the same ruleset. For example, you could include the default branch, include any branches matching the pattern `*feature*`, and then specifically exclude a branch matching the pattern `not-a-feature`.

### Selecting branch or tag protections

In the "Branch protections" or "Tag protections" section, select the rules you want to include in the ruleset. When you select a rule, you may be able to enter additional settings for the rule. For more information on the rules, see [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).

### Adding metadata restrictions

Your metadata restrictions should be intended to increase consistency between commits in your repository. They are not intended to replace security measures such as requiring code review via pull requests.

1. To add a rule to control commit metadata or branch names, in the "Restrictions" section when creating or editing a ruleset, click **Restrict commit metadata** or **Restrict branch names**.
2. Configure the settings for the restriction, then click **Add**. You can add multiple restrictions to the same ruleset.
3. To match a given regex pattern, in the "Requirement" dropdown, select **Must match a given regex pattern**.
 For most requirements, such as "Must start with a matching pattern," the pattern you enter is interpreted literally, and wildcards are not supported. For example, the `*` character only represents the literal `*` character.
 For more complex patterns, you can select "Must match a given regex pattern" or "Must not match a given regex pattern," then use regular expression syntax to define the matching pattern. For more information, see [About regular expressions for commit metadata](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization#using-regular-expressions-for-commit-metadata) " in the GitHub Enterprise Cloud documentation.
 Anyone who views the rulesets for a repository will be able to see the description you provide.
4. Optionally, before enacting your ruleset with metadata restrictions, select the "Evaluate" enforcement status for your ruleset to test the effects of any metadata restrictions without impacting contributors. For more information on metadata restrictions, see [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#important-considerations-for-metadata-restrictions).

### Finalizing your branch or tag ruleset and next steps

To finish creating your ruleset, click **Create**. If the enforcement status of the ruleset is set to "Active", the ruleset takes effect immediately.

## Creating a push ruleset

You can create a push ruleset for private or internal repositories.

1. On GitHub, navigate to the main page of the repository.
2. Under your repository name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then click **Settings**.
 ![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/cb-28260/mw-1440/images/help/repository/repo-actions-settings.webp)
3. In the left sidebar, under "Code and automation," click **Rules**, then click **Rulesets**.
 ![Screenshot of the sidebar of the "Settings" page for a repository. The "Rules" sub-menu is expanded, and the "Rulesets" option is outlined in orange.](https://docs.github.com/assets/cb-80504/mw-1440/images/help/repository/rulesets-settings.webp)
4. Click **New ruleset**.
5. To create a ruleset targeting branches, click **New push ruleset**.
6. Under "Ruleset name," type a name for the ruleset.
7. Optionally, to change the default enforcement status, click **Disabled** and select an enforcement status.

### Granting bypass permissions for your push ruleset

You can grant certain roles, teams, or apps bypass permissions for your ruleset. The following are eligible for bypass access:

- Repository admins, organization owners, and enterprise owners
- The maintain or write role, or custom repository roles based on the write role
- Teams, excluding secret teams. See [About organization teams](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams#team-visibility).
- GitHub Apps
- Dependabot. For more information about Dependabot, see [Dependabot quickstart guide](https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide).

1. To grant bypass permissions for the ruleset, in the "Bypass list" section, click **Add bypass**.
2. In the "Add bypass" modal dialog that appears, search for the role, team, or app you would like to grant bypass permissions, then select the role, team, or app from the "Suggestions" section and click **Add Selected**.

### Selecting push protections

You can block pushes to this repository and this repository's entire fork network based on file extensions, file path lengths, file and folder paths, and file sizes.

Any push protections you configure will block pushes in this repository and throughout this repository's entire fork network.

1. Under "Push protections," click the restrictions you want to apply. Then fill in the details for the restrictions you select.
 For file path restrictions, you can use partial or full paths. You can use `fnmatch` syntax for this. For example, a restriction targeting `test/demo/**/*` prevents any pushes to files or folders in the `test/demo/` directory. A restriction targeting `test/docs/pushrules.md` prevents pushes specifically to the `pushrules.md` file in the `test/docs/` directory. For more information, see [Creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#using-fnmatch-syntax).
