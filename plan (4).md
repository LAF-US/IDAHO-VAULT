Problem: Work the currently open GitHub issues that are addressable in-repo without trampling unrelated dirty-tree changes.

Approach:
- Fix the highest-confidence automation gap first: branch cleanup coverage for orphaned automation branches.
- Add staged metadata enforcement only for the currently governed automation lane, then bring the affected generators into compliance so validation stays behavior-safe.
- Reduce the large-file watchdog offender by replacing the obsolete oversized sort-audit artifact with a compact stub, and make the legacy move helper fall back to older compatible reports.
- Make a small, low-risk PR-loop hardening change only if it is grounded in the current repo state rather than outdated audit notes.
- Keep issue #235 called out as partially blocked on repository settings.

Execution notes:
- Do not revert unrelated local changes.
- Prefer changes that are exercised by existing or new Python unit tests.
- Keep governance/doc updates minimal and directly tied to the behavior being changed.
