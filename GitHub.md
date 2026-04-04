---
---
CodeRabbit GitHub integration (AI code review)

- Documentation index: https://docs.coderabbit.ai/llms.txt (lists all docs). Primary GitHub guide: https://docs.coderabbit.ai/platforms/github-com
- Prerequisites: GitHub admin/owner rights on the org or repo to install apps; ability to authorize GitHub Marketplace apps; write access on the target repo so the bot can comment.
- Install & authorize: sign in at https://app.coderabbit.ai/ with “Log in with GitHub,” review the requested permissions, and click **Authorize coderabbitai**.
- Choose scope: during installation select either all repositories or only specific ones (recommended); adjust anytime in GitHub > Settings > Applications > Installed GitHub Apps > CodeRabbit.
- Permissions requested (typical): read org/user metadata; read repo metadata; read/write pull requests, checks/statuses, issues, and code contents so reviews can post inline comments.
- Repo configuration (optional): add `.coderabbit.yaml` at repo root to tune review scope, ignored paths, and behavior; commit changes to apply.
- Verify: open or update a pull request to trigger CodeRabbit; the bot should post a summary and inline comments. If nothing appears, recheck app installation scope and repo write access.
