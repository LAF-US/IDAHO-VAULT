---
title: "Troubleshooting required status checks"
source: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks"
author:
published:
created: 2026-06-30
description: "You can check for common errors and resolve issues with required status checks."
---
If you have a check and a status with the same name, and you select that name as a required status check, both the check and the status are required. For more information, see [REST API endpoints for checks](https://docs.github.com/en/rest/checks).

After you enable required status checks, your branch may need to be up-to-date with the base branch before merging. This ensures that your branch has been tested with the latest code from the base branch. If your branch is out of date, you'll need to merge the base branch into your branch. For more information, see [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging).

You won't be able to push local changes to a protected branch until all required status checks pass. Instead, you'll receive an error message similar to the following.

```shell
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Required status check "ci-build" is failing
```

## Required check needs to succeed against the latest commit SHA

In order for a pull request to be merged, all required checks must pass against the latest commit SHA. This ensures that the most recent changes are validated and meet the required standards before merging. Checks that were triggered using a previous commit SHA will not be used as part of required checks. Successful check statuses are: `success`, `skipped`, and `neutral`. For more information, see [About status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks).

## Conflicts between head commit and test merge commit

Sometimes, the results of the status checks for the test merge commit and head commit will conflict. If the test merge commit has a status, the test merge commit must pass. Otherwise, the status of the head commit must pass before you can merge the branch.

If there is a conflict between the test merge commit and head commit, the checks for the test merge commit are shown in the pull request status checks box. This is indicated in the pull request status box by a line starting with `Showing checks for the merge commit`. For more information about test merge commits, see [REST API endpoints for pull requests](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request).

## Handling skipped but required checks

### Example

The following example shows a workflow that requires a "Successful" completion status for the `build` job, but the workflow will be skipped if the pull request does not change any files in the `scripts` directory.

```yaml
name: ci
on:
  pull_request:
    paths:
      - 'scripts/**'
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [12.x, 14.x, 16.x]
    steps:
    - uses: actions/checkout@v6
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test
```

Due to [path filtering](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore), a pull request that only changes a file in the root of the repository will not trigger this workflow and is blocked from merging. On the pull request, you would see "Waiting for status to be reported."

### Status checks with GitHub Actions and a Merge queue

You **must** use the `merge_group` event to trigger your GitHub Actions workflow when a pull request is added to a merge queue.

A workflow that reports a check which is required by the target branch's protections would look like this:

```yaml
on:
  pull_request:
  merge_group:
```

For more information on the `merge_group` event, see [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#merge_group).

## Required status checks from unexpected sources

It's also possible for a protected branch to require a status check from a specific GitHub App. If you see a message similar to the following, then you should verify that the check listed in the merge box was set by the expected app.

```
Required status check "build" was not set by the expected GitHub App.
```