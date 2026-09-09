# Native Pull-Request Branch Updater

These two files use GitHub’s native **Update a pull request branch** endpoint. GitHub merges the PR’s own base branch into its head; it does not rebase or force-push.[1]

> The endpoint updates only PRs whose base is the requested branch. A PR based on another branch is reported as `SKIP: base is …`; it is not silently updated from `main`.

## Files

| File | Purpose |
| --- | --- |
| `update-open-pr-branches-from-main.sh` | Local `gh api` loop. Default: read-only dry run. |
| `.github/workflows/update-open-pr-branches-from-main.yml` | Manually dispatched, read-only GitHub Actions audit. |

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

## GitHub Actions Audit

1. Keep the Bash script at repository root as `update-open-pr-branches-from-main.sh`.
2. Add the workflow to `.github/workflows/update-open-pr-branches-from-main.yml`.
3. Open **Actions → Audit open PR branches against main → Run workflow**.
4. Review the uploaded summary artifact and the run summary.

The workflow is intentionally **manual-dispatch only and read-only**. It uses no user-controlled workflow inputs and requests only `contents: read` and `pull-requests: read`. That makes it a visible, repeatable audit without granting a workflow run authority to mutate active PR heads.

> To perform a native branch update, use the explicit local `./update-open-pr-branches-from-main.sh --apply` command after reviewing its dry-run output and current hold list. This keeps the write decision outside untrusted workflow input handling while retaining GitHub's normal base-into-head update semantics.[1]

## Operational Guarantees

| Behavior | Result |
| --- | --- |
| Default invocation | Read-only classification; no update requests. |
| Clean, behind PR in apply mode | GitHub accepts a normal base-into-head update. |
| Conflict or changed head | GitHub rejects/holds the update; no force-push or rebase occurs. |
| Explicit PR/branch hold | The PR is skipped. |
| Duplicate PRs sharing one source head | Only the first source branch is processed. |
| Non-`main` PR base | Skipped, because native update would merge that other base instead of `main`. |

## References

[1]: https://docs.github.com/en/rest/pulls/pulls#update-a-pull-request-branch "GitHub REST API: Update a pull request branch"
