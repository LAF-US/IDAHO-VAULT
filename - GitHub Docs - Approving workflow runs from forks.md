---
source: "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks"
author:
  - "[[GitHub Docs]]"
published:
created: 2026-03-29
---
Workflow runs triggered by a contributor's pull request from a fork may require manual approval from a maintainer with write access. You can configure workflow approval requirements for a [repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-required-approval-for-workflows-from-public-forks), [organization](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#configuring-required-approval-for-workflows-from-public-forks), or [enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#enforcing-a-policy-for-fork-pull-requests-in-your-enterprise).

Workflow runs that have been awaiting approval for more than 30 days are automatically deleted.

## Approving workflow runs on a pull request from a public fork

Maintainers with write access to a repository can use the following procedure to review and run workflows on pull requests from contributors that require approval.

1. Under your repository name, click **Pull requests**.
	![Screenshot of the main page of a repository. In the horizontal navigation bar, a tab, labeled "Pull requests," is outlined in dark orange.](https://docs.github.com/assets/cb-51156/mw-1440/images/help/repository/repo-tabs-pull-requests-global-nav-update.webp)
2. In the list of pull requests, click the pull request you'd like to review.
3. On the pull request, click **Files changed**.
	![Screenshot of the tabs for a pull request. The "Files changed" tab is outlined in dark orange.](https://docs.github.com/assets/cb-23571/mw-1440/images/help/pull_requests/pull-request-tabs-changed-files.webp)
4. Inspect the proposed changes in the pull request and ensure that you are comfortable running your workflows on the pull request branch. You should be especially alert to any proposed changes in the `.github/workflows/` directory that affect workflow files.
5. If you are comfortable with running workflows on the pull request branch, return to the **Conversation** tab, and in the section " *n* workflow(s) awaiting approval", click **Approve workflows to run**.