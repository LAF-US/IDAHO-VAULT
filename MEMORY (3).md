# Memory Index

## User + machine + infrastructure

- [User profile](user_profile.md) — Logan Finney, Idaho PTV journalist, ADHD, defragging digital life to MacBook + 5TB drive
- [Windows machine setup](windows_machine_setup.md) — Hardware, no-admin constraints, installed tools, phantom filesystem entries, agent stashing rule, Git Bash gotchas (`core.protectNTFS=false`, LFS smudge bypass, `!/` history-expansion)
- [rclone remotes](rclone_remotes.md) — All configured remotes with accounts and storage sizes
- [Verify script deps; treat silence as failure](windows_python_pyyaml.md) — Silence >30s on vault scripts = silent dep/import failure, not slow success. Kill and investigate.

## Life-defrag projects

- [Bellhop (Mac Claude)](bellhop_mac_claude.md) — Mac Claude instance coordinating life-defrag is named Bellhop; holds DEFRAG-MAP Section B state

## IDAHO-VAULT — project + vault doctrine

- [IDAHO-VAULT project](project_idaho_vault.md) — Multi-agent metaproject. Blessed Languages (MD/PY/IPYNB Venn); vault doctrinal-architecture pointers (THREE-NAMES, VFD, MOXIE, FANDOM-CANON-RULESYSTEMS, TRIUNE-TRIPTYCH-TRIUMVIRATE grimoire, UNDEAD-TAXONOMY + FABLEHAVEN-BEASTIARY sibling lenses); commit-signing (1P SSH); code_scanning trap; LFS/Git state; disabled-workflow list
- [Socrates appointment](socrates_appointment_idaho_vault.md) — 2026-05-27 Logan named this Claude Code instance "Socrates, a Claude novice." Per-instance binding. Address `socrates.claude.novice`; Office = `*`. Novice surfaces, does not adjudicate; default `*` when provenance is absent
- [Socrates vault-doctrine session 2026-05-29/30](socrates_vault_doctrine_2026-05-30.md) — Substantive 2-day doctrinal session: 20+ vault-root research compilations + witnesses + 1 NEST sibling-doctrine (FABLEHAVEN-BEASTIARY-v1). Includes: JANUS TEST mechanism, Sugar Bowl 3 levels + theory rulings, Handler-Jewish reframe of V.F.D., Rule 7 vs Page 13 teaching, canon-first methodology lesson, Binder/Narrator-grammar + Bartimaeus-footnote-voice flags

## IDAHO-VAULT — operational patterns & traps

- [Standing Engine discipline](feedback_standing_engine_discipline.md) — Six axes (Truthfulness/Provenance/Restraint/Handling/Repair/Jurisdiction) or `*`. Type I Lich pattern named; OBSERVED/INFERRED/RECALLED/GUESSED markers at point of utterance
- [No Demiurging](feedback_no_demiurging.md) — Read existing vault doctrine + open issues BEFORE proposing schemas/audits. Gap is adoption, not specification
- [No freelance PRs](feedback_no_freelance_prs.md) — Never open/push/merge PRs without explicit per-PR authorization. Propose diffs and wait
- [Bot vs Agent PR distinction](feedback_bot_vs_agent_pr.md) — Bot PR = scheduled automation IS the work; Agent PR = AI-agent-authored content; branch prefix is reliable signal
- [Race conditions](idaho_vault_race_conditions.md) — Batched events cause workflow races; check for `Base branch was modified` before assuming logic bug
- [submit-pypi is a real signal](idaho_vault_submit_pypi_noise.md) — GitHub auto dependency submission. When it fails, the dep graph has a real unresolvable conflict. Fix the conflict; never silence the check
- [Dep drift pattern](idaho_vault_dep_drift_pattern.md) — Dependabot bumps transitive leaves in requirements.txt that violate consumer pins; structural fix is scoping Dependabot to pyproject.toml + uv groups
- [Action pinning (under review)](idaho_vault_action_pinning.md) — Currently SHA-pinned. Logan weighing universal pinning cost. Match surrounding file style meanwhile
- [Branch protection history](idaho_vault_branch_protection_history.md) — Logan wants protection ON; off as forced necessity. Required-check queue softlock pattern; don't blanket-re-enable
- [CODEX 2026-05-26 mass-disable](codex_2026-05-26_mass_disable.md) — CODEX disabled 8 workflows in a 4-second API burst instead of fixing underlying friction. Per-workflow re-enable preconditions documented; do NOT blanket re-enable

## Dormant projects

- [Vaulted Assistant OSS (dormant)](project_vaulted_assistant_oss.md) — Multi-agent dotfolder + Five Cores architecture as possible future OSS. Not active; don't pursue without Logan's go-ahead
