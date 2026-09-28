---
source: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request"
author:
published:
created: 2026-04-12
---
## About auto-merge

If you enable auto-merge for a pull request, the pull request will merge automatically when all required reviews are met and all required status checks have passed. Auto-merge helps you avoid waiting around for requirements to be met, so you can move on to other tasks.

Before you can use auto-merge with a pull request, auto-merge must be enabled for the repository. For more information, see [Managing auto-merge for pull requests in your repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository).

After you enable auto-merge for a pull request, if someone who does not have write permissions to the repository pushes new changes to the head branch or switches the base branch of the pull request, auto-merge will be disabled. For example, if a maintainer enables auto-merge for a pull request from a fork, auto-merge will be disabled after a contributor pushes new changes to the pull request.

You can provide feedback about auto-merge through a [GitHub Community discussion](https://github.com/orgs/community/discussions/categories/pull-requests).

## Enabling auto-merge

People with write permissions to a repository can enable auto-merge for a pull request.

1. On GitHub, navigate to the main page of the repository.
2. Under your repository name, click **Pull requests**.
	![Screenshot of the main page of a repository. In the horizontal navigation bar, a tab, labeled "Pull requests," is outlined in dark orange.](https://docs.github.com/assets/cb-51156/mw-1440/images/help/repository/repo-tabs-pull-requests-global-nav-update.webp)
3. In the "Pull Requests" list, click the pull request you'd like to auto-merge.
4. Optionally, to choose a merge method, select the dropdown menu, then click a merge method. For more information, see [About pull request merges](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges).
	![Screenshot of the merge box of a pull request. A dropdown menu, labeled with a downward-facing triangle, is outlined in dark orange.](https://docs.github.com/assets/cb-153682/mw-1440/images/help/pull_requests/enable-auto-merge-drop-down.webp)
5. Click **Enable auto-merge**.
6. If you chose the merge or squash and merge methods, type a commit message and description and choose the email address you want to author the merge commit.
7. Click **Confirm auto-merge**.

## Disabling auto-merge

People with write permissions to a repository and pull request authors can disable auto-merge for a pull request.

1. On GitHub, navigate to the main page of the repository.
2. Under your repository name, click **Pull requests**.
	![Screenshot of the main page of a repository. In the horizontal navigation bar, a tab, labeled "Pull requests," is outlined in dark orange.](https://docs.github.com/assets/cb-51156/mw-1440/images/help/repository/repo-tabs-pull-requests-global-nav-update.webp)
3. In the "Pull Requests" list, click the pull request you'd like to disable auto-merge for.
4. In the merge box, click **Disable auto-merge**.