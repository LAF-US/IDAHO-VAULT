---
title: "Configuring a publishing source for your GitHub Pages site"
source: "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow"
author:
published:
created: 2026-08-13
description: "You can configure your GitHub Pages site to publish when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site."
---
## About publishing sources

You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.

If you do not need any control over the build process for your site, we recommend that you publish your site when changes are pushed to a specific branch. You can specify which branch and folder to use as your publishing source. The source branch can be any branch in your repository, and the source folder can either be the root of the repository (`/`) on the source branch or a `/docs` folder on the source branch. Whenever changes are pushed to the source branch, the changes in the source folder will be published to your GitHub Pages site.

If you want to use a build process other than Jekyll or you do not want a dedicated branch to hold your compiled static files, we recommend that you write a GitHub Actions workflow to publish your site. GitHub provides workflow templates for common publishing scenarios to help you write your workflow.

## Publishing from a branch

1. Make sure the branch you want to use as your publishing source already exists in your repository.
2. On GitHub, navigate to your site's repository.
3. Under your repository name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then click **Settings**.
	![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/cb-28260/mw-1440/images/help/repository/repo-actions-settings.webp)
4. In the "Code and automation" section of the sidebar, click **Pages**.
5. Under "Build and deployment", under "Source", select **Deploy from a branch**.
6. Under "Build and deployment", use the branch dropdown menu and select a publishing source. ![Screenshot of Pages settings in a GitHub repository. A menu to select a branch for a publishing source, labeled "None," is outlined in dark orange.](https://docs.github.com/assets/cb-47265/mw-1440/images/help/pages/publishing-source-drop-down.webp)
7. Optionally, use the folder dropdown menu to select a folder for your publishing source. ![Screenshot of Pages settings in a GitHub repository. A menu to select a folder for a publishing source, labeled "/(root)," is outlined in dark orange.](https://docs.github.com/assets/cb-24510/mw-1440/images/help/pages/publishing-source-folder-drop-down.webp)
8. Click **Save**.

### Troubleshooting publishing from a branch

If you choose the `docs` folder on any branch as your publishing source, then later remove the `/docs` folder from that branch in your repository, your site won't build and you'll get a page build error message for a missing `/docs` folder. For more information, see [Troubleshooting Jekyll build errors for GitHub Pages sites](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/troubleshooting-jekyll-build-errors-for-github-pages-sites#missing-docs-folder).

Your GitHub Pages site will always be deployed with a GitHub Actions workflow run, even if you've configured your GitHub Pages site to be built using a different CI tool. Most external CI workflows "deploy" to GitHub Pages by committing the build output to the `gh-pages` branch of the repository, and typically include a `.nojekyll` file. When this happens, the GitHub Actions workflow will detect the state that the branch does not need a build step, and will execute only the steps necessary to deploy the site to GitHub Pages servers.

To find potential errors with either the build or deployment, you can check the workflow run for your GitHub Pages site by reviewing your repository's workflow runs. For more information, see [Viewing workflow run history](https://docs.github.com/en/actions/how-tos/monitor-workflows/view-workflow-run-history). For more information about how to re-run the workflow in case of an error, see [Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs).

## Publishing with a custom GitHub Actions workflow

To configure your site to publish with GitHub Actions:

1. On GitHub, navigate to your site's repository.
2. Under your repository name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then click **Settings**.
	![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/cb-28260/mw-1440/images/help/repository/repo-actions-settings.webp)
3. In the "Code and automation" section of the sidebar, click **Pages**.
4. Under "Build and deployment", under "Source", select **GitHub Actions**.
5. GitHub will suggest several workflow templates. If you already have a workflow to publish your site, you can skip this step. Otherwise, choose one of the options to create a GitHub Actions workflow. For more information about creating your custom workflow, see [Creating a custom GitHub Actions workflow to publish your site](#creating-a-custom-github-actions-workflow-to-publish-your-site).
	GitHub Pages does not associate a specific workflow to the GitHub Pages settings. However, the GitHub Pages settings will link to the workflow run that most recently deployed your site.

### Creating a custom GitHub Actions workflow to publish your site

For more information about GitHub Actions, see [GitHub Actions documentation](https://docs.github.com/en/actions).

When you configure your site to publish with GitHub Actions, GitHub will suggest workflow templates for common publishing scenarios. The general flow of a workflow is to:

1. Trigger whenever there is a push to the default branch of the repository or whenever the workflow is run manually from the Actions tab.
2. Use the [`actions/checkout`](https://github.com/actions/checkout) action to check out the repository contents.
3. If required by your site, build any static site files.
4. Use the [`actions/upload-pages-artifact`](https://github.com/actions/upload-pages-artifact) action to upload the static files as an artifact.
5. If the workflow was triggered by a push to the default branch, use the [`actions/deploy-pages`](https://github.com/actions/deploy-pages) action to deploy the artifact. This step is skipped if the workflow was triggered by a pull request.

The workflow templates use a deployment environment called `github-pages`. If your repository does not already include an environment called `github-pages`, the environment will be created automatically. We recommend that you add a deployment protection rule so that only the default branch can deploy to this environment. For more information, see [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).