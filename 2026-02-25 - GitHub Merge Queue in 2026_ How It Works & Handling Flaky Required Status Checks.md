---
title: "GitHub Merge Queue in 2026: How It Works & Handling Flaky Required Status Checks"
source: "https://tenki.cloud/blog/github-merge-queue-setup"
author:
  - "[[Eddie Wang]]"
published: 2026-02-25
created: 2026-06-30
description: "GitHub's merge queue prevents broken merges on busy branches, but common gaps trip up most teams who enable it. Here's how the queue actually works, how to configure it properly, and how to stop flaky tests from blocking your entire pipeline."
---
If your team merges more than a handful of pull requests per day to a protected branch, you've probably hit this: two PRs pass CI independently, get merged back to back, and the combination breaks main. The second PR was tested against a base that no longer exists. GitHub's merge queue exists to fix exactly that problem. It serializes merges, tests each PR (or batch of PRs) against an up-to-date base, and only fast-forwards the branch when CI passes on the real combined result.

Sounds straightforward. In practice, teams turn it on, immediately hit a flaky test that blocks the entire queue, realize their workflows don't trigger on the right events, and turn it back off. That's not a merge queue problem — it's a configuration problem. Let's fix it.

## How the merge queue actually works

When you enable merge queue on a branch, the "Merge" button on a PR changes to "Merge when ready." Clicking it doesn't merge immediately. Instead, the PR enters a queue. GitHub then creates a temporary branch — a speculative merge commit — that combines the target branch, all PRs already ahead in the queue, and the new PR. CI runs against that temporary branch. If all checks pass, the target branch is fast-forwarded to include the changes.

The key insight is the **speculative merge commit**. If PRs A, B, and C are queued in that order, the queue doesn't just test each one against main. It tests A against main, B against main+A, and C against main+A+B. Each PR is validated against the state the branch will actually be in when that PR lands.

### Grouping and batching

Testing every PR individually is safe but slow. If your CI takes 15 minutes and you have 10 PRs queued, that's two and a half hours of serial waiting. Grouping solves this. You set a `maximum group size` (say, 5), and the queue batches up to 5 PRs into a single speculative merge commit. If the batch passes, all 5 merge at once.

If the batch fails, the queue bisects. It splits the group, retests the halves, and identifies which PR broke things. The failing PR gets ejected, and the passing ones proceed. This bisection behavior is automatic — you don't configure it. But you should know it happens, because a batch failure means at least two additional CI runs before anything merges.

You can also set a `minimum group size` with a `wait time`. If the minimum is 3 and the wait time is 5 minutes, the queue holds off on starting CI until either 3 PRs are queued or 5 minutes have passed, whichever comes first. For high-traffic repos this reduces the total number of CI runs. For low-traffic repos, it just adds latency — leave the minimum at 1.

### What happens when a queued PR fails

When a check fails on a queued entry, the PR is removed from the queue. Every PR that was behind it in the queue gets a new speculative merge commit, because their base changed. All those CI runs restart. This cascading restart is the single biggest source of frustration with merge queues, and it's the reason flaky tests are so damaging.

## Setting it up: branch protection and ruleset configuration

Merge queue lives inside branch protection rules (classic) or repository rulesets (the newer system GitHub is pushing teams toward). The configuration is the same either way. Navigate to your branch protection settings, check "Require merge queue," and you'll see four settings:

- **Merge method** — Squash, merge commit, or rebase. This overrides the per-PR merge method. Pick one and stick with it; the queue applies it uniformly.
- **Maximum group size** — How many PRs to batch into a single CI run. Start with 5 for most teams. Go higher only if your CI is slow and your test suite is reliable.
- **Minimum group size and wait time** — Set to 1 and 0 unless you're processing 20+ PRs daily and want to reduce CI runs.
- **Status check timeout** — How long the queue waits for checks to complete before considering the entry failed. Default is 60 minutes. If your CI takes 20 minutes, set this to 40. Too generous and a hung workflow blocks the queue for an hour.

### Required checks: the part most people get wrong

There are two layers of required checks and they're easily confused. Branch protection has its own "Require status checks to pass before merging" setting, and the merge queue has a separate set of checks it waits for. They're not the same list.

Branch protection required checks gate whether a PR can *enter* the queue. The merge queue's own checks determine whether a queued entry can *merge*. If you only configure the branch protection checks but don't set up workflows that run on the `merge_group` event, the queue will sit there waiting for checks that never start.

## Workflow triggers: pull\_request vs. merge\_group

This is the most common setup mistake. Your existing CI workflow probably triggers on `pull_request` and maybe `push`. The merge queue doesn't use either of those. It creates a temporary merge group branch and expects workflows to trigger on the `merge_group` event.

The fix is simple: add `merge_group` to your workflow triggers alongside your existing ones.

```yaml
name: CI
on:
  pull_request:
    branches: [main]
  merge_group:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

The check names must match between the `pull_request` trigger (so the PR can enter the queue) and the `merge_group` trigger (so the queue can verify the merge). If you have a matrix build that produces check names like "test (ubuntu, 18)" and "test (ubuntu, 20)", all of those names need to appear as passing under both event triggers. Mismatched names are an instant queue stall.

One gotcha with the `push` event: the merge queue's temporary branches won't trigger `push` workflows unless you explicitly include the `gh-readonly-queue/**` branch pattern. But don't do that — use the `merge_group` event instead. It's what GitHub designed for this purpose, and it gives you the right context variables.

## The flaky check problem (and how to solve it)

Here's the scenario that makes people hate merge queues. You have 8 PRs in the queue. PR #3 has a flaky integration test that fails 10% of the time. It fails. The queue ejects PR #3. PRs #4 through #8 all get new speculative merge commits and restart CI from scratch. Twenty minutes later, a different flaky test fails on PR #6. Cascade restart again. Your team has been waiting over an hour and nothing has merged.

This isn't hypothetical. It's the number one reason teams disable merge queue. The queue amplifies flaky tests from a mild annoyance into a pipeline-stopping event. A test that fails 5% of the time on a single PR run now has a 5% chance of blowing up the entire queue on every cycle.

There's no magic fix, but there are concrete strategies that work.

### 1\. Separate required checks from informational checks

Not every CI job needs to block the merge queue. Split your workflow into two categories: a lean, reliable set of required checks (unit tests, type checking, linting, security scans) and a separate set of informational checks (end-to-end tests, visual regression, performance benchmarks). Only the required checks should be listed in branch protection. The informational checks still run and report status, but they don't block the queue.

```yaml
# .github/workflows/required-checks.yml
name: Required Checks
on:
  pull_request:
    branches: [main]
  merge_group:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:unit

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run typecheck
```
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests (Informational)
on:
  pull_request:
    branches: [main]
  # Not triggered on merge_group — intentionally non-blocking

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:e2e
```

This is the single highest-impact change you can make. If your flaky tests aren't in the required set, they can't block the queue.

### 2\. Quarantine known flaky tests

Most test frameworks support tagging or annotations. When a test is identified as flaky, tag it and exclude it from the required CI run. Run quarantined tests in a separate job that reports but doesn't gate the merge.

In Jest, you can use `test.skip` with a wrapper or filter by test file path. In pytest, the `@pytest.mark.flaky` decorator from pytest-rerunfailures gives you explicit control. Tools like BuildPulse and Trunk Flaky Tests can automatically detect and quarantine flaky tests based on historical pass/fail rates. The important thing is having a process: flaky test gets flagged, moved to quarantine, and tracked for fixing. Don't just skip it and forget.

### 3\. Add retry logic to your workflow

GitHub doesn't offer native retry for merge queue checks. But you can build it into your workflow. The simplest approach: use a test runner's built-in retry (Jest's `--retries` flag, pytest-rerunfailures, or Vitest's `retry` option). A test that fails once then passes on retry still reports as passing.

```
{
  "jest": {
    "retryTimes": 2,
    "retryImmediately": true
  }
}
```

Be careful with this. Retries mask the flakiness instead of fixing it. Use retries as a short-term mitigation while you track down the root cause, not as a permanent solution. If you're retrying 50 tests across every CI run, you have a test reliability problem that retries won't solve.

### 4\. Reduce your required check surface area

Every additional required check is another thing that can flake and block the queue. Ask yourself: does this check actually catch bugs that would break production, or is it a nice-to-have? Linting, type checking, and fast unit tests belong in the required set. Slow integration tests that depend on external services, browser-based E2E suites, and anything hitting a staging environment should probably be informational. You can always run them post-merge on main.

## When merge queue helps vs. when it hurts

Merge queue isn't universally beneficial. It adds latency to every merge, and that latency only pays off if you're actually hitting merge conflicts or broken-main scenarios at a meaningful rate.

**Merge queue makes sense when:**

- Your team merges 10+ PRs per day to a single branch
- You've had incidents where main broke because two independently-passing PRs conflicted
- You deploy from main continuously and a broken main means a broken deploy
- Your monorepo has cross-package dependencies where a change in package A can break package B's tests

**Merge queue probably isn't worth it when:**

- Your team is small (under 5 people) and rarely has concurrent PRs
- You have a polyrepo setup where each service has its own repo and merges don't interact
- Your CI is slow (30+ minutes) and your test suite has known flakiness you haven't addressed
- You merge a few PRs a week and "require branches to be up to date" in branch protection already catches conflicts

The "require branches to be up to date" option in branch protection is the simpler alternative. It forces PRs to rebase on the latest target before merging, which catches semantic conflicts but requires manual rebasing. For teams merging fewer than 10 PRs per day, the manual rebase flow is usually fast enough and doesn't have the cascading failure problem.

## Monorepo considerations

Monorepos benefit the most from merge queues, but they also stress them the hardest. In a monorepo, a change to a shared library can break any downstream package. Without a merge queue, two PRs touching different packages can each pass CI and then break main when combined through a shared dependency.

The downside: monorepo CI suites tend to be large. Running the full suite on every merge group entry is expensive. If you use a build tool like Turborepo, Nx, or Bazel, leverage affected-package detection to run only the tests relevant to each queued change. This means your merge queue CI workflow needs to compute the affected packages and run a scoped test command, not just `npm test` at the repo root.

## Alternatives: Mergify, Aviator, and the Bors legacy

GitHub's merge queue is the native option, but it's not the only one. The concept predates GitHub's implementation by years.

**Bors-NG** was the original open-source merge queue bot, inspired by Rust's infrastructure. It pioneered the "test the merge result before merging" approach. As of 2026, Bors-NG is effectively in maintenance mode. Most teams that were using it have migrated to GitHub's native queue or to a commercial alternative. It still works, but you're on your own for support.

**Mergify** offers a merge queue as part of a broader PR automation platform. Its advantage over native merge queue is configurability: you get priority lanes (urgent PRs jump the queue), per-label queue rules, and built-in retry logic for failed checks. If your team needs more control than GitHub's four settings, Mergify is the most mature option. It does mean giving a third-party app write access to your repos.

**Aviator** (formerly MergeQueue) focuses specifically on merge automation for high-velocity teams. Its standout feature is parallel mode: instead of testing PRs sequentially, Aviator tests multiple speculative merge combinations in parallel and only commits the ones that pass. This can dramatically reduce queue latency for teams with fast CI and lots of concurrent PRs. Aviator also integrates flaky test detection directly into the queue logic, which is a meaningful differentiator if flaky checks are your main pain point.

For most teams, GitHub's native merge queue is good enough. It's free, it requires no third-party integration, and it covers the core use case. The alternatives earn their keep when you need priority queuing, automatic retry, or parallel speculative testing. If you're evaluating, start native and switch to a third-party tool only when you hit a specific limitation.

## A practical rollout plan

If you're turning on merge queue for the first time, don't just flip the switch on your busiest repo. Do it in steps:

1. **Audit your flaky tests first.** Run your test suite 20 times in a row. If any test fails even once, quarantine it or fix it before enabling the queue.
2. **Add the merge\_group trigger** to your required CI workflow. Verify check names match between pull\_request and merge\_group events.
3. **Separate required from informational checks.** Be aggressive about keeping the required set small and fast.
4. **Enable merge queue on a low-traffic repo first.** Let it run for a week. Watch for stalls and timeouts. Tune the timeout setting.
5. **Roll out to your main repo** with a conservative group size (3-5). Increase it once you're confident your checks are stable.
6. **Monitor the queue.** GitHub shows queue status on the branch protection page. Track how often PRs get ejected and why. If the same test keeps ejecting PRs, that's your priority fix.

The merge queue rewards teams that have invested in CI reliability. If your tests are fast and deterministic, the queue is almost invisible — PRs just merge faster and main stays green. If your tests are slow and flaky, the queue will make that pain visible in ways you can't ignore. Either way, you end up in a better place.

Tags

#github-actions#ci-cd#merge-queue

[![Complete guide to migrating CI/CD pipelines from Jenkins to GitHub Actions](https://assets.blog.tenki.cloud/Jenkins%20to%20GitHub%20Actions%20Migration%20Guide.png)](https://tenki.cloud/blog/jenkins-github-actions-migration)

[GitHub Actions](https://tenki.cloud/blog/jenkins-github-actions-migration)

[·Jun 2026

Jenkins to GitHub Actions Migration Guide

Eddie Wang

](https://tenki.cloud/blog/jenkins-github-actions-migration)[![Guide to migrating GitHub Actions to Node.js 24 before the deprecation deadline](https://assets.blog.tenki.cloud/Migrate%20GitHub%20Actions%20to%20Nodejs%2024%20Before%20the%20Deadline.png)

GitHub Actions

·May 2026

Migrate GitHub Actions to Node.js 24 Before the Deadline

Hayssem Vazquez-Elsayed

](https://tenki.cloud/blog/migrate-github-actions-node-24)[![GitHub Actions runner images 2026 - complete guide to selecting the right runner for your workflows](https://assets.blog.tenki.cloud/GitHub%20Actions%20Runner%20Images%20in%202026%20The%20Complete%20Selection%20Guide.png)

GitHub Actions

·Jun 2026

GitHub Actions Runner Images in 2026: The Complete Selection Guide

Eddie Wang

](https://tenki.cloud/blog/github-actions-runner-image-selection-2026)