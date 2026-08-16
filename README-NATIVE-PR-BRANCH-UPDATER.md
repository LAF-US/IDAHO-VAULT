# Native Pull-Request Branch Updater

These two files use GitHub’s native **Update a pull request branch** endpoint. GitHub merges the PR’s own base branch into its head; it does not rebase or force-push.[1]

> The endpoint updates only PRs whose base is the requested branch. A PR based on another branch is reported as `SKIP: base is …`; it is not silently updated from `main`.

## Files

| File | Purpose |
|---|---|
| `update-open-pr-branches-from-main.sh` | Local `gh api` loop. Default: read-only dry run. |
| `.github/workflows/update-open-pr-branches-from-main.yml` | Manually dispatched GitHub Actions wrapper. Default: read-only dry run. |

## Bash Usage

The script sits at the repository root as `update-open-pr-branches-from-main.sh`. It requires an authenticated `gh` CLI with access to write the PR head branches and `jq`.

```bash
chmod +x ./update-open-pr-branches-from-main.sh

# Default: no writes. Lists current, excluded, and candidate PRs.
./update-open-pr-branches-from-main.sh

# Explicitly request native updates for clean branches.
./update-open-pr-branches-from-main.sh --apply

# Maintain the standing Obsidian hold and add any temporary human holds.
./update-open-pr-branches-from-main.sh \
  --exclude-pr 980 \
  --exclude-branch logan/obsidian \
  --exclude-branch active-human-branch
```

The script sends the observed `expected_head_sha` with every update request. If a branch changes after enumeration, GitHub returns `422` instead of updating a head that the run did not inspect.[1]

## GitHub Actions Usage

1. Keep the Bash script at repository root as `update-open-pr-branches-from-main.sh`.
2. Add the workflow to `.github/workflows/update-open-pr-branches-from-main.yml`.
3. Open **Actions → Update open PR branches from main → Run workflow**.
4. Start with `apply = false`. Review the uploaded summary artifact and the run summary.
5. Re-run with `apply = true` only after setting any current human/agent holds in the two denylist inputs.

The workflow is intentionally **manual-dispatch only**. That keeps a useful bulk maintenance operation from racing a human or agent working on a live branch. It has `contents: write` and `pull-requests: write` permissions because GitHub’s endpoint needs write access to the PR head.[1]

## Operational Guarantees

| Behavior | Result |
|---|---|
| Default invocation | Read-only classification; no update requests. |
| Clean, behind PR in apply mode | GitHub accepts a normal base-into-head update. |
| Conflict or changed head | GitHub rejects/holds the update; no force-push or rebase occurs. |
| Explicit PR/branch hold | The PR is skipped. |
| Duplicate PRs sharing one source head | Only the first source branch is processed. |
| Non-`main` PR base | Skipped, because native update would merge that other base instead of `main`. |

## References

[1]: https://docs.github.com/en/rest/pulls/pulls#update-a-pull-request-branch "GitHub REST API: Update a pull request branch"
