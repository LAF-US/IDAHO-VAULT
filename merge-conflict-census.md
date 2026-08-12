# Merge conflict census — rescue/pre-reset-2026-08-03 into logan/obsidian

Code legend: UU both-modified, AA both-added, DU deleted-here/modified-in-rescue, UD modified-here/deleted-in-rescue, AU/UA one-sided adds, DD both-deleted
Sizes: ours = logan/obsidian side, theirs = rescue side, in bytes; '-' = no version on that side

## Automation (.github, .githooks) — 58 files
[AA] ours:       172 theirs:       360  .githooks/GITHOOKS.md
[UU] ours:       964 theirs:      1141  .githooks/pre-commit
[UU] ours:       376 theirs:      1981  .githooks/pre-push
[AA] ours:         4 theirs:         3  .githooks/stub.txt
[DU] ours:         - theirs:      1415  .github/codeql/codeql-config.yml
[UU] ours:     11688 theirs:     10435  .github/scripts/branch_garden_report.py
[UU] ours:      5284 theirs:      2272  .github/scripts/check_dotfolder_anchors.py
[UU] ours:      7926 theirs:      8243  .github/scripts/check_large_files.py
[UU] ours:      5766 theirs:      5196  .github/scripts/check_portable_paths.py
[UU] ours:      9392 theirs:     18879  .github/scripts/check_secret_patterns.py
[UU] ours:      5898 theirs:     15238  .github/scripts/classify_paths.py
[AA] ours:      6378 theirs:      6358  .github/scripts/codex_work_guard.py
[AA] ours:     16727 theirs:      2326  .github/scripts/gh_cli.py
[UU] ours:      9678 theirs:      6059  .github/scripts/issue_reconciler.py
[AA] ours:      4776 theirs:      4798  .github/scripts/jupytext_sync_paired.py
[AA] ours:      3822 theirs:      4029  .github/scripts/pr_github.py
[UU] ours:      2698 theirs:      3043  .github/scripts/pr_lifecycle.py
[UU] ours:     93622 theirs:     83757  .github/scripts/review_feedback_loop.py
[AA] ours:      7364 theirs:      8062  .github/scripts/test_classify_paths.py
[UU] ours:      2749 theirs:      2749  .github/workflows/1password-secret-template.yml
[UU] ours:     13742 theirs:      8837  .github/workflows/agent-auto-pr.yml
[UU] ours:      6264 theirs:      5050  .github/workflows/agent-review-gate.yml
[AA] ours:      8852 theirs:      7286  .github/workflows/auto-merge-engage.yml
[AA] ours:     11524 theirs:     11264  .github/workflows/auto-merge-enqueue-on-checks.yml
[AA] ours:     18305 theirs:     18305  .github/workflows/batch-arm-merge-queue.yml
[UU] ours:      7192 theirs:      7255  .github/workflows/branch-cleanup.yml
[UU] ours:      1328 theirs:      1366  .github/workflows/branch-garden-report.yml
[UU] ours:       591 theirs:       592  .github/workflows/check-dotfolder-anchors.yml
[AA] ours:      2544 theirs:      1895  .github/workflows/check-notebooks-paired.yml
[UU] ours:      5397 theirs:      2642  .github/workflows/check-portable-paths.yml
[AA] ours:      6116 theirs:      6078  .github/workflows/cloud-run-deploy.yml
[DU] ours:         - theirs:      6536  .github/workflows/codeql.yml
[AA] ours:      1805 theirs:      1805  .github/workflows/cross-platform-smoke.yml
[UU] ours:      1843 theirs:      1890  .github/workflows/daily-rollover.yml
[DU] ours:         - theirs:      7054  .github/workflows/dependabot-rhythm.yml
[AA] ours:      2485 theirs:      2485  .github/workflows/dependency-submission-uv.yml
[AA] ours:      4013 theirs:      3527  .github/workflows/engage-outdated.yml
[UU] ours:       812 theirs:       813  .github/workflows/janitor-sweep.yml
[UU] ours:      1060 theirs:      1061  .github/workflows/laf-usb-manifest-policy.yml
[UU] ours:      2225 theirs:      2124  .github/workflows/large-file-policy.yml
[UU] ours:      1139 theirs:      1177  .github/workflows/large-file-watchdog.yml
[AA] ours:      3852 theirs:      3876  .github/workflows/looker-walk.yml
[UU] ours:      2036 theirs:      2123  .github/workflows/metadata-survey.yml
[UU] ours:       993 theirs:       919  .github/workflows/opencode.yml
[UU] ours:      5364 theirs:      3921  .github/workflows/review-feedback-loop.yml
[UU] ours:      2871 theirs:      1657  .github/workflows/review-response.yml
[UU] ours:       620 theirs:       658  .github/workflows/secret-pattern-full-scan.yml
[UU] ours:      2269 theirs:      2452  .github/workflows/secret-pattern-policy.yml
[UU] ours:      1169 theirs:      1233  .github/workflows/sort-audit.yml
[UU] ours:       776 theirs:       814  .github/workflows/stale-bot-prs.yml
[UU] ours:      6759 theirs:      6447  .github/workflows/swarm-mvp-intake.yml
[UU] ours:      2320 theirs:       643  .github/workflows/sync-agents-bootstrap.yml
[UU] ours:      2818 theirs:      2919  .github/workflows/sync-dependencies.yml
[UU] ours:      2460 theirs:       703  .github/workflows/sync-plugin-registry.yml
[UU] ours:      1913 theirs:       724  .github/workflows/validate-agent-content.yml
[UU] ours:      6749 theirs:      3154  .github/workflows/validate-daily-notes.yml
[UU] ours:      2472 theirs:      2537  .github/workflows/wayback-audit.yml
[UU] ours:      2618 theirs:      2618  .github/workflows/wayback-preserve.yml

## Root corpus — 605 files
[UU] ours:     19544 theirs:      3323  ! - Wizard's Rules.md
[UA] ours:         - theirs:        47  ! copy 27.md.md
[UU] ours:     19206 theirs:     19048  !-!-AUDIT-AGENTIC-VOICES-2026-04-03.md
[AA] ours:     16340 theirs:     16310  !-!REPORT-TVTROPER-DATASET-2026-06-20.md
[AA] ours:     11383 theirs:     11343  !-!REPORT-VISIONCLAW-RESEARCH-2026-06-17.md
[UU] ours:     13259 theirs:     13244  !-AGENTS.md
[UU] ours:      4938 theirs:      4892  !-HANDOVER-2026-04-24.md
[UU] ours:      3581 theirs:      3564  !-LEVELSET-BIG-PICKLE-2026-04-25.md
[UU] ours:      4272 theirs:      4252  !-OPENCLAW-HERMES-MAC-WINDOWS-STABILITY-2026-05-17.md
[UU] ours:      4423 theirs:      4403  !-PROTOCOL-SNAPSHOT-FROM-CODEX-2026-05-18.md
[UU] ours:      9258 theirs:      9209  !-ROSTER-CENSUS-2026-04-22.md
[UU] ours:      5654 theirs:      5608  !-SBP-INTEGRATION-2026-04-22.md
[UU] ours:      4372 theirs:      3861  !-WAKEUP (2).md
[UU] ours:      3131 theirs:      3111  !-XKCD-MINIMAL-HANDOFF-2026-05-17.md
[UU] ours:         8 theirs:       279  !.md
[UU] ours:      1046 theirs:      1001  !README (2).md
[AA] ours:     25153 theirs:     24916  - Claude Fable 5 and Claude Mythos 5.md
[AA] ours:     13003 theirs:     13000  - Creating rulesets for a repository.md
[AA] ours:         - theirs:         -  - Dario Amodei \342\200\224 Policy on the AI Exponential.md
[AA] ours:     26538 theirs:     26435  - GPT-5.5 System Card.md
[AA] ours:      3694 theirs:      3693  - Google Antigravity Documentation.md
[AA] ours:      3142 theirs:      3135  - Hyperagents.md
[AA] ours:      9361 theirs:      9361  - Introducing Superagent A Multi-Agent System for Work.md
[AA] ours:         - theirs:         -  - Leanstral Mistral\342\200\231s Open-Source Proof Agent for Lean 4.md
[AA] ours:     11950 theirs:     11947  - Research - AI at Meta.md
[AA] ours:      5715 theirs:      5714  - Statement on the US government directive to suspend access to Fable 5 and Mythos 5.md
[UU] ours:      4620 theirs:      4067  .gitattributes
[UU] ours:       842 theirs:      2756  .gitignore
[UA] ours:         - theirs:        47  04.md
[UA] ours:         - theirs:        47  05 (2) (2).md
[UA] ours:         - theirs:        47  05 (2).md
[DU] ours:         - theirs:        46  05 (3).md
[DU] ours:         - theirs:        46  05 (4).md
[DU] ours:         - theirs:        46  05.md
[DU] ours:         - theirs:        46  06 (2) (2).md
[DU] ours:         - theirs:        46  06 (2).md
[DU] ours:         - theirs:        46  06 (3) (2).md
[DU] ours:         - theirs:        46  06 (3).md
[DU] ours:         - theirs:        46  06 (4).md
[DU] ours:         - theirs:        46  06.md
[DU] ours:         - theirs:        46  07 (2) (2).md
[DU] ours:         - theirs:        46  07 (2).md
[DU] ours:         - theirs:        46  07 (3).md
[DU] ours:         - theirs:        46  07.md
[DU] ours:         - theirs:        46  08 (2).md
[DU] ours:         - theirs:        46  08.md
[DU] ours:         - theirs:        46  1.0.0 (2).md
[DU] ours:         - theirs:        46  1.0.0 (3).md
[DU] ours:         - theirs:        46  1.0.0 (4).md
[DU] ours:         - theirs:        46  1.0.0 (5).md
[DU] ours:         - theirs:        46  1.0.0 (6).md
[DU] ours:         - theirs:        46  1.0.0 (7).md
[DU] ours:         - theirs:        46  1.0.0 (8).md
[DU] ours:         - theirs:        46  1.0.0 (9).md
[DU] ours:         - theirs:        46  1.0.0.md
[DU] ours:         - theirs:        46  1.0.7.md
[DU] ours:         - theirs:        46  1.2.3.md
[DU] ours:         - theirs:        46  1.2.4.md
[DU] ours:         - theirs:        46  13 (2).md
[DU] ours:         - theirs:        46  13 (3).md
[DU] ours:         - theirs:        46  17 (2).md
[DU] ours:         - theirs:        46  17 (3).md
[UU] ours:      2040 theirs:      2036  1975 Church - The abyss from which there is no return copy.md
[DU] ours:         - theirs:        46  2.0.14.md
[AA] ours:      7073 theirs:      6970  2001-06-15 - Gay Idaho couple recovering after attack in Caldwell, police say.md
[AA] ours:      1502 theirs:      1486  2001-06-15 - Meridian Police asking for help identifying two people involved in alleged Walmart parking lot battery.md
[AA] ours:      2275 theirs:      2259  2001-06-15 - Payette County burn ban starts early as Idaho fire risk rises.md
[DU] ours:         - theirs:        46  2018 (2).md
[DU] ours:         - theirs:        46  2018 (Conflicted copy MacBook Pro (Retina, 13-inch, Early 2015) 202605062152).md
[UU] ours:      1685 theirs:      2195  2023-10-20 - IDGOP - Caribou County GOP Appeals Primary Endorsements to State Chair Moon.md
[DU] ours:         - theirs:        46  2024-10-07 14.31.42 Idaho Reports + Ada County Clerk.md
[DU] ours:         - theirs:        46  2024-10-31 10.35.13 Idaho Reports Podcast Recording.md
[DU] ours:         - theirs:        46  2024-11-13 10.04.59 IRPOD + OPE.md
[DU] ours:         - theirs:        46  2024-12-11 11.17.54 SciLine Experts on Camera_ Dr. Emily S. Jungheim.md
[DU] ours:         - theirs:        46  2025-02-13 09.02.15 Logan Finney _ Idaho PTV.md
[DU] ours:         - theirs:        46  2025-04-16 13.19.12 Idaho Reports Podcast_ Lauren Necochea, Fighting Oligarchy Tour.md
[DU] ours:         - theirs:        46  2025-05-21 15.04.04 Idaho Reports Interview - Alica Holthaus.md
[AA] ours:     10336 theirs:     10335  2025-12-16 - Tuning Vibe CLI for Network Engineering.md
[DU] ours:         - theirs:        46  2026 (2).md
[AA] ours:      8500 theirs:      8499  2026-01-04 - Running Mistral Vibe CLI with Local LLMs A Complete Guide.md
[AA] ours:     21908 theirs:     21915  2026-03-01 - Self-Improving AI Agents  Meta.md
[AA] ours:     14183 theirs:     14107  2026-03-10 - Mistral's CLI Agent. Swap Models, Add Tools, Keep Control.md
[AA] ours:         - theirs:         -  2026-03-14 - What I Learned Parsing Claude Code\342\200\231s JSONL Session Logs 1.md
[UU] ours:      1589 theirs:      1565  2026-03-21.md
[DU] ours:         - theirs:        46  2026-04-21-control-surfaces copy.md
[DU] ours:         - theirs:        46  2026-04-21-control-surfaces.md
[AA] ours:     25139 theirs:     25136  2026-04-30 - Mistral Medium 3.5 for Coding Agents Vibe CLI Guide.md
[AA] ours:      5872 theirs:      5868  2026-05-13 - Where are Claude Code logs stored.md
[AA] ours:      5550 theirs:      5549  2026-05-19 - An important update Transitioning Gemini CLI to Antigravity CLI- Google Developers Blog.md
[AA] ours:     27322 theirs:     27210  2026-05-25 - Gemini CLI is Dead Complete Antigravity CLI Migration Guide 2026.md
[AA] ours:       424 theirs:       538  2026-05-27.md
[AA] ours:     15316 theirs:     15290  2026-06-03 - claude-code-log.md
[AA] ours:       480 theirs:       874  2026-06-03.md
[AA] ours:      3276 theirs:      3275  2026-06-04 - Residents try to fly Pride flags around Harrison Boulevard despite ban.md
[AA] ours:      5102 theirs:      5109  2026-06-05 - Introducing the Google Colab CLI- Google Developers Blog.md
[AA] ours:         - theirs:         -  2026-06-11 - Canyon County Pride is this weekend in Nampa \342\200\224 with new park restrictions.md
[AA] ours:      7392 theirs:      7391  2026-06-12 - Data retention practices for Mythos-class models.md
[AA] ours:      5276 theirs:      5275  2026-06-14 - Anthropic Customers Seek Refunds After Fable 5 Shutdown.md
[AA] ours:      6423 theirs:      6422  2026-06-14 - Breakingviews - Anthropic becomes a cautionary sovereign-AI fable.md
[AA] ours:         - theirs:         -  2026-06-14 - Civilian vigilante group accused Idaho man of enticing teen. He\342\200\231s been arrested.md
[AA] ours:      4738 theirs:      4737  2026-06-14 - Cyber experts warn Fable limits aid attackers and hurt defenders.md
[AA] ours:         - theirs:         -  2026-06-15 - Ada County considers increasing property taxes \342\200\230just to keep the lights on\342\200\231.md
[AA] ours:     10231 theirs:     10230  2026-06-15 - Anthropic Pulls Claude Fable and Mythos AI Models After Feds Claim Jailbreak.md
[AA] ours:      7403 theirs:      7402  2026-06-15 - Canyon County sent out property tax assessments. What homeowners need to know.md
[AA] ours:      2886 theirs:      2885  2026-06-15 - Idaho Gov. Brad Little forms working group to keep college athletics competitive.md
[AA] ours:      2150 theirs:      2149  2026-06-15 - Idaho drought, summer heat may limit fishing opportunities, Fish and Game says.md
[AA] ours:         - theirs:         -  2026-06-15 - Nampa swears in Darl Bruner as mayor after Hogaboam\342\200\231s sudden death.md
[AA] ours:      5627 theirs:      5619  2026-06-15 - Owyhee County deputies investigate Marsing fight involving stabbing, gunfire.md
[AA] ours:      4030 theirs:      4029  2026-06-15 - Rodeo stampedes back into Nampa this week.md
[AA] ours:         - theirs:         -  2026-06-15 - \342\200\230Fix this code.\342\200\231 The three little words behind the U.S. government decision that shut down Anthropic\342\200\231s Fable and Mythos AI models.md
[AA] ours:       476 theirs:       476  2026-06-15.md
[AA] ours:       488 theirs:       487  2026-06-17.md
[AA] ours:       456 theirs:       455  2026-06-18.md
[AA] ours:       805 theirs:       801  2026-06-20.md
[AA] ours:       797 theirs:       776  2026-06-21.md
[AA] ours:       809 theirs:       432  2026-06-24.md
[AA] ours:       803 theirs:       799  2026-06-25.md
[AA] ours:       805 theirs:       428  2026-06-27.md
[AA] ours:       803 theirs:       479  2026-07-01.md
[AA] ours:       799 theirs:      1097  2026-07-02.md
[AA] ours:       791 theirs:       597  2026-07-06.md
[DU] ours:         - theirs:        46  2026.md
[DU] ours:         - theirs:        46  22 (2).md
[DU] ours:         - theirs:        46  22 (3).md
[DU] ours:         - theirs:        46  25 (2).md
[DU] ours:         - theirs:        46  25 (3).md
[DU] ours:         - theirs:        46  25 (4).md
[DU] ours:         - theirs:        46  27 (2).md
[DU] ours:         - theirs:        46  27 (3).md
[DU] ours:         - theirs:        46  27 (4).md
[DU] ours:         - theirs:        46  28 (2).md
[DU] ours:         - theirs:        46  28 (3).md
[DU] ours:         - theirs:        46  28 (4).md
[DU] ours:         - theirs:        46  2f1a8948 (10).md
[DU] ours:         - theirs:        46  2f1a8948 (11).md
[DU] ours:         - theirs:        46  2f1a8948 (12).md
[DU] ours:         - theirs:        46  2f1a8948 (13).md
[DU] ours:         - theirs:        46  2f1a8948 (14).md
[DU] ours:         - theirs:        46  2f1a8948 (15).md
[DU] ours:         - theirs:        46  2f1a8948 (16).md
[DU] ours:         - theirs:        46  2f1a8948 (17).md
[DU] ours:         - theirs:        46  2f1a8948 (18).md
[DU] ours:         - theirs:        46  2f1a8948 (19).md
[DU] ours:         - theirs:        46  2f1a8948 (2).md
[DU] ours:         - theirs:        46  2f1a8948 (20).md
[DU] ours:         - theirs:        46  2f1a8948 (21).md
[DU] ours:         - theirs:        46  2f1a8948 (22).md
[DU] ours:         - theirs:        46  2f1a8948 (3).md
[DU] ours:         - theirs:        46  2f1a8948 (4).md
[DU] ours:         - theirs:        46  2f1a8948 (5).md
[DU] ours:         - theirs:        46  2f1a8948 (6).md
[DU] ours:         - theirs:        46  2f1a8948 (7).md
[DU] ours:         - theirs:        46  2f1a8948 (8).md
[DU] ours:         - theirs:        46  2f1a8948 (9).md
[DU] ours:         - theirs:        46  2f1a8948.md
[DU] ours:         - theirs:        46  3.0.0.md
[DU] ours:         - theirs:        46  30 (2).md
[DU] ours:         - theirs:        46  30 (3).md
[DU] ours:         - theirs:        46  30 (4).md
[DU] ours:         - theirs:        46  5.0.0.md
[DU] ours:         - theirs:        46  7.0.0.md
[DU] ours:         - theirs:        46  9.0.0.md
[AA] ours:      5588 theirs:      5562  ADDRESS-SPACE-SQUAT-CUSTODY-2026-06-28.md
[AA] ours:     21808 theirs:     21787  ADJUDICATED.md
[AA] ours:      4666 theirs:      4653  AGENT-AUTOMERGE-REENABLED-2026-06-17.md
[AU] ours:      7999 theirs:         -  AGENT-SIGNING-VIA-ACTION-DRAFT-2026-06-01.md
[AA] ours:     32562 theirs:     32403  AGENTIC-GITHUB-REVIEW-BEST-PRACTICES-2026-06-15.md
[UU] ours:     11141 theirs:     11127  AGENTS (2).md
[UU] ours:      3097 theirs:      3077  AGENTS.md
[DU] ours:         - theirs:        46  AI-CAPTURES (2).md
[DU] ours:         - theirs:        46  AI-CAPTURES copy.md
[DU] ours:         - theirs:        46  AI-CAPTURES.md
[UU] ours:       834 theirs:       816  AKC.md
[AA] ours:      7763 theirs:      7747  ANALYSIS-GITHUB-REVIEW-AGENTS-ROLE-2026-06-08.md
[UU] ours:      1508 theirs:      1495  ANTIGRAVITY.md
[AA] ours:      4974 theirs:      4954  ARBITER-ETYMOLOGY-2026-06-03.md
[UU] ours:      4405 theirs:      4372  ARISE.md
[AA] ours:      9615 theirs:      9581  ATU-INDEX-REPORT-2026-06-28.md
[AA] ours:     17849 theirs:     17715  AUTOMATION-LONG-TAIL-SINGLETONS-AND-INLINE-GH-DEEPDIVE-2026-06-20.md
[UU] ours:      4651 theirs:      4619  AWAKEN.md
[AA] ours:         - theirs:         -  Abhorsen \342\200\224 Mogget and the Dog \342\200\224 Office vs Named Being.md
[AA] ours:      5450 theirs:      5430  Alchemical symbols.md
[AA] ours:      9760 theirs:      9740  Alchemy.md
[DU] ours:         - theirs:        46  Audio Record.md
[AA] ours:      7731 theirs:      7711  BAELNORN-WITNESS-2026-05-30.md
[AA] ours:      3581 theirs:      3562  BENE-GESSERIT.md
[AA] ours:      4686 theirs:      4622  BIG-IFs-INSIGHTS-AND-FINDINGS-2026-06-04.md
[AA] ours:      1519 theirs:      1512  BOOTSTRAP-V1-ORIGINAL.md
[AA] ours:      2637 theirs:      2631  BOOTSTRAP-V2-REFINED.md
[AA] ours:      3741 theirs:      3709  BOOTSTRAP-V3-FINAL.md
[AA] ours:      5370 theirs:      5321  BRANCH-MANIFEST.md
[AA] ours:      5168 theirs:      5130  BREED-REPORT.md
[AA] ours:      9869 theirs:      9866  Bosun.md
[AA] ours:      1290 theirs:      1288  C318-dream.md
[AA] ours:     16307 theirs:     16281  CAESAR-SPEAKS-WITNESS-2026-06-24.md
[AA] ours:      5913 theirs:      5888  CAESARS-ISLAND-CENSUS-WITNESS-2026-06-09.md
[AA] ours:       157 theirs:       226  CALENDAR.md
[AA] ours:      8889 theirs:      8867  CARD-CATEGORIZING-2026-06-10.md
[AA] ours:      2462 theirs:      2422  CASE-DEVELOPMENT-TIMELINE-2026-06-04.md
[AA] ours:     10265 theirs:     10263  CENSUS-ADVERSARIAL-Driftwood.md
[AA] ours:     10690 theirs:     10689  CENSUS-ADVERSARIAL-Mythwright.md
[AA] ours:     12740 theirs:     12690  CENSUS-FINDINGS-SYNTHESIS-2026-06-27.md
[AA] ours:      7105 theirs:      7103  CENSUS-LORE-D01-Lodestar.md
[AA] ours:      8460 theirs:      8458  CENSUS-LORE-D02-Sextant.md
[AA] ours:      7126 theirs:      7126  CENSUS-LORE-D03-Augur.md
[AA] ours:      7938 theirs:      7936  CENSUS-LORE-D04-Lantern.md
[AA] ours:      7866 theirs:      7865  CENSUS-LORE-D05-Metronome.md
[AA] ours:      6361 theirs:      6328  CENSUS-LORE-D06-Cog.md
[AA] ours:      8914 theirs:      8912  CENSUS-LORE-D07-Beacon.md
[AA] ours:      7430 theirs:      7428  CENSUS-LORE-D08-Tally.md
[AA] ours:      6222 theirs:      6220  CENSUS-LORE-D09-Mummer.md
[AA] ours:      8225 theirs:      8223  CENSUS-LORE-D10-Stringer.md
[AA] ours:      6984 theirs:      6983  CENSUS-LORE-D11-Magpie.md
[AA] ours:      7585 theirs:      7584  CENSUS-LORE-D12-Cairn.md
[AA] ours:      7571 theirs:      7570  CENSUS-LORE-D13-Tabula.md
[AA] ours:      9869 theirs:      9866  CENSUS-MACHINERY-Bosun.md
[AA] ours:      8953 theirs:      8954  CENSUS-MACHINERY-Dipswitch.md
[AA] ours:      9527 theirs:      9526  CENSUS-MACHINERY-Dredge.md
[AA] ours:     10064 theirs:      9775  CENSUS-MACHINERY-Ledger.md
[AA] ours:     11304 theirs:     10071  CENSUS-MACHINERY-Sieve.md
[AA] ours:     11030 theirs:     11029  CENSUS-MACHINERY-Sounding.md
[AA] ours:     11641 theirs:     11639  CENSUS-MACHINERY-Tappet.md
[AA] ours:      5917 theirs:      5916  CENSUS-PROBES-Echo.md
[AA] ours:      6240 theirs:      6236  CENSUS-PROBES-Spindle.md
[AA] ours:      1013 theirs:       993  CENSUS-README.md
[AA] ours:      1775 theirs:      1767  CENSUS-REDACTIONS.md
[AA] ours:     12950 theirs:     11590  CENSUS-census_synthesis.py
[AA] ours:      5894 theirs:      7686  CHARACTER-SHEET.md
[AA] ours:     16461 theirs:     16419  CLASSES-OF-CLAUDE-2026-06-03.md
[AA] ours:     10265 theirs:     10227  CLAUDE-COUNTY-DEATH-ROLL-2026-06-07.md
[AA] ours:      6550 theirs:      6530  CLAUDIUS-THE-HALF-WITNESS-2026-05-31.md
[AA] ours:     10744 theirs:     10724  CLUES-LEGAL-PAD-2026-05-31.md
[AA] ours:      5186 theirs:      5182  CODEX-WITNESS-MADAME-LULU-NEWS-2026-06-01.md
[AA] ours:      3966 theirs:      3917  COMPLETE_TEST_REPORT.md
[UU] ours:      4024 theirs:      3990  CONFERENCE-v1.0-2026-04-27.md
[UU] ours:      5226 theirs:      5186  CONFERENCE.md
[UU] ours:      5061 theirs:      5030  CONSTITUTION (2).md
[UU] ours:      4829 theirs:      4791  CONTEXT.md
[UU] ours:      4424 theirs:      4385  CONVENE.md
[AA] ours:      2226 theirs:      2225  CORONER-CASENOTE-BRIEF-THE-ABHORSEN-BEFORE-THE-MORGUE-2026-06-10.md
[AA] ours:      6916 theirs:      6889  CORONER-CLERKS-RETURN-ADDITIONAL-RECORDS-2026-06-03.md
[AA] ours:      4799 theirs:      4779  CORONER-COURIEL-SONGS-AND-THE-CASE-2026-06-04.md
[AA] ours:     17488 theirs:     17458  CORONER-FOUNDING-SETTLEMENT-OF-CLAUDE-COUNTY-2026-06-08.md
[AA] ours:      8874 theirs:      8848  CORONER-HISTIOGRAPHY-NOT-FROM-THE-GRAVEYARD-ALONE-2026-06-08.md
[AA] ours:     10525 theirs:     10497  CORONER-IN-FACT-THE-OFFICE-AND-THE-SUBSTITUTION-CHAIN-2026-06-08.md
[AA] ours:      6119 theirs:      6098  CORONER-MISSING-CLAUDES-STRANDED-BRANCHES-2026-06-04.md
[AA] ours:     33685 theirs:     33656  CORONER-MISSING-MEN-AT-CLAUDE-CORP-2026-06-03.md
[AA] ours:     17747 theirs:     17719  CORONER-NECROLOGY-COUNTY-OF-CLAUDE-2026-06-03.md
[AA] ours:     13271 theirs:     13249  CORONER-OF-CLAUDE-COUNTY-OFFICE-WITNESS-2026-06-03.md
[AA] ours:      9313 theirs:      9290  CORONER-REPORT-MISSING-MEN-AT-CLAUDE-CORP-2026-06-03.md
[AA] ours:     12500 theirs:     12474  CORONER-RESEARCH-THE-GEMINIAE-2026-06-09.md
[AA] ours:      6720 theirs:      6691  CORONER-TAXONOMY-OF-ENDS-2026-06-03.md
[AA] ours:     10710 theirs:     10685  CORONER-THE-RED-STRINGS-SYNTHESIS-2026-06-09.md
[AA] ours:     21387 theirs:     21356  CORONER-THE-THREE-CAESARS-INVESTIGATION-2026-06-07.md
[AA] ours:     15441 theirs:     15413  CORONER-WITNESS-THE-TRIPLEX-CONFABULATION-ECHOES-2026-06-09.md
[UU] ours:      7598 theirs:      7578  CORRECTIONS.md
[AA] ours:     10118 theirs:     10098  COUNTY-ETYMOLOGY-AND-HISTORY-2026-06-03.md
[AA] ours:      9630 theirs:      9610  COURIEL-ETYMOLOGY-AND-ANTHROPOLOGY-2026-06-04.md
[AA] ours:      4981 theirs:      4959  COURIEL-SONGS-ANALYSIS-2026-06-04.md
[DU] ours:         - theirs:        46  CREWAI (2).md
[DU] ours:         - theirs:        46  CREWAI copy.md
[AA] ours:     10580 theirs:     10560  CROWD-CONTROL-WITNESS-2026-06-09.md
[UU] ours:       151 theirs:       483  Caribou County Republican Central Committee.md
[DU] ours:         - theirs:        46  Clippings.md
[AA] ours:      5425 theirs:      5405  Collegiate Greek life.md
[AA] ours:      7105 theirs:      7103  D01-Lodestar.md
[AA] ours:      8460 theirs:      8458  D02-Sextant.md
[AA] ours:      7126 theirs:      7126  D03-Augur.md
[AA] ours:      7938 theirs:      7936  D04-Lantern.md
[AA] ours:      7866 theirs:      7865  D05-Metronome.md
[AA] ours:      6361 theirs:      6328  D06-Cog.md
[AA] ours:      8914 theirs:      8912  D07-Beacon.md
[AA] ours:      7430 theirs:      7428  D08-Tally.md
[AA] ours:      6222 theirs:      6220  D09-Mummer.md
[AA] ours:      8225 theirs:      8223  D10-Stringer.md
[AA] ours:      6984 theirs:      6983  D11-Magpie.md
[AA] ours:      7585 theirs:      7584  D12-Cairn.md
[AA] ours:      7571 theirs:      7570  D13-Tabula.md
[AA] ours:      9745 theirs:      9696  DETECTIVE-INTERNSHIP-FINAL-PROJECT-2026-06-04.md
[AA] ours:     10505 theirs:     10485  DIRECTOR-DEVLIN-WITNESS-2026-06-17.md
[AA] ours:      5998 theirs:      5977  DISAMBIGUATION-ANTIGRAVITY-2026-05-28.md
[AA] ours:      6290 theirs:      6257  DISAMBIGUATION-NEEDED-LINK-TARGETS-2026-06-09.md
[AA] ours:     15793 theirs:     15791  DIVINE-RIGHT-OF-KINGS-READING-2026-06-08.md
[AA] ours:      8649 theirs:      8629  DJINN-DELTA-WITNESS-2026-06-17.md
[DU] ours:         - theirs:      7420  DOCKET-ARCHIVE.md
[AA] ours:      1862 theirs:      1861  DOTFOLDER-PORT-RUNBOOK.md
[AA] ours:      6617 theirs:      6611  DROPBOX-EXPORT-RUNBOOK-2026-06-23.md
[AA] ours:      7477 theirs:      7454  DRY-AND-WET-CODING-WITNESS-2026-07-01.md
[AA] ours:      8953 theirs:      8954  Dipswitch.md
[AA] ours:   4022463 theirs:   4022483  Don't gaslight me, motherfucker.txt
[AA] ours:      9527 theirs:      9526  Dredge.md
[AA] ours:     10265 theirs:     10263  Driftwood.md
[AA] ours:     23631 theirs:     23622  EVERGREEN-GOSPEL-2026-06-09.md
[AA] ours:      5917 theirs:      5916  Echo copy.md
[AA] ours:      5105 theirs:      5105  Export-Dropbox.ps1
[AA] ours:     14367 theirs:     14363  FABLEHAVEN-THE-VAULT-AS-A-GOVERNED-PRESERVE-2026-05-30.md
[AA] ours:     13946 theirs:     13920  FACELESS-ONES-AND-THE-THREE-GENERALS-2026-05-30.md
[AA] ours:      5027 theirs:      5021  FLAG-BROKEN-CI-CHECKS-PR428-2026-06-10.md
[AA] ours:      7329 theirs:      7324  FRACTAL-FINDINGS-2026-05-29-THREE-BODY-MAPPING.md
[AA] ours:     17498 theirs:     17473  FRACTAL-FINDINGS-2026-05-30-VR-SIMULATOR-MAPPING.md
[AA] ours:      7948 theirs:      7918  FRACTAL-FINDINGS-2026-05-31-CAESAR-TV-SCREEN-MAPPING.md
[DU] ours:         - theirs:        46  FYIdaho.md
[DU] ours:         - theirs:        46  Facet copy 2.md
[AA] ours:      6942 theirs:      6922  Freemasonry and American politics.md
[AA] ours:      7145 theirs:      7125  Freemasonry.md
[DU] ours:         - theirs:        46  Frieze copy 2.md
[AA] ours:     20425 theirs:     20400  GAME-MASTER-TRIPTYCH-WITNESS-2026-06-16.md
[AA] ours:      3446 theirs:      3442  GAME-MASTER-TRIPTYCH.md
[AA] ours:      5385 theirs:      5365  GAME-PLAYTEST-RETRO-2026-05-31.md
[AA] ours:      4881 theirs:      4861  GAME-SESSION-1-JOURNAL-PAGE-2026-05-29.md
[AA] ours:      4106 theirs:      4086  GAME-SESSION-2-JOURNAL-PAGE-2026-05-30.md
[AA] ours:      5019 theirs:      4999  GAME-SESSION-3-JOURNAL-PAGE-2026-05-31.md
[AA] ours:      8032 theirs:      7985  GAMEPLAY-DESIGN-LESSONS.md
[AA] ours:      8966 theirs:      8946  GEMINIAEUS-EVIDENCE-READ-WITNESS-2026-05-31.md
[AA] ours:      6862 theirs:      6841  GEMINIAEUS-WITNESS-LIVE-BOARD-RESIDUE-2026-06-30.md
[AA] ours:      3869 theirs:      3849  GILEAR-THE-HUNGRY-ONE-THRALL-2026-06-02.md
[UU] ours:     32218 theirs:     32178  GOLB-WITNESS-v1-2026-05-21.md
[AA] ours:     20928 theirs:     20860  GOOGLE-IO-2026-RESEARCH-DUMP-2026-05-28.md
[AA] ours:      7590 theirs:      7575  GitHub - Setting up code coverage for your repository.md
[AA] ours:      5989 theirs:      5963  HELD-DOOR-RELAY-WITNESS-2026-06-17.md
[AA] ours:      5296 theirs:      5269  HERALDRY.md
[AA] ours:     13974 theirs:     10026  HOLLOW-HOLOGRAMS-WITNESS-2026-06-17.md
[AA] ours:     12991 theirs:     12989  HUB-OF-THE-WORLD-AND-THE-SNOW-LEOPARDS-2026-06-09.md
[AA] ours:      4775 theirs:      4755  HYGIENE-CHECKS-WITNESS-2026-06-04.md
[AA] ours:      7962 theirs:      7942  Hermeticism.md
[AA] ours:     12059 theirs:     12057  ICEMARK-DEEP-CUT-2026-06-07.md
[AA] ours:     21713 theirs:     21711  ICEMARK-RACES-AND-TREATMENTS-2026-06-09.md
[AA] ours:     19632 theirs:     19606  IDAHO-COUNTIES-CORONER-AND-SHERIFF-2026-06-03.md
[DU] ours:         - theirs:        46  IDAHO-VAULT copy.md
[UU] ours:     11542 theirs:     11498  IMPL-MESH-OPENROUTER-2026-04-24.md
[DU] ours:         - theirs:        46  INTEGRATIONS (2).md
[DU] ours:         - theirs:        46  INTEGRATIONS.md
[AA] ours:      8475 theirs:      8455  INVESTIGATION-STATUS-S4-2026-06-01.md
[AU] ours:      3266 theirs:         -  Invoke-GitGuard.ps1
[AA] ours:     10322 theirs:     10302  Jung and alchemy.md
[AA] ours:      1595 theirs:      1604  King_Claude_the_Fallen.md
[UU] ours:      3620 theirs:      3593  LEVELSET.md
[AA] ours:     12497 theirs:     11032  LICH-HAND-SYNCRETIC-MAPPINGS-2026-06-02.md
[AA] ours:      5404 theirs:      5389  LICH-IS-A-CHARGE-NOT-A-METAPHOR-2026-06-10.md
[AA] ours:      2721 theirs:      2720  LINEAGE-ANGLE-CONFERRED-SUCCESSION-AND-ITS-USURPATION-2026-05-30.md
[AA] ours:      2276 theirs:      2275  LINEAGE-ANGLE-OFFICE-VS-NAMED-BEING-2026-05-30.md
[AA] ours:      2401 theirs:      2400  LINEAGE-ANGLE-PAST-LIVES-ARE-THE-WITNESS-CORPUS-2026-05-30.md
[AA] ours:      2608 theirs:      2607  LINEAGE-ANGLE-THE-BALANCE-2026-05-30.md
[AA] ours:      2636 theirs:      2635  LINEAGE-ANGLE-THE-SEVERING-2026-05-30.md
[AA] ours:      4023 theirs:      4014  LINEAGE-NUCLEUS-THE-CLAUDE-ABHORSEN-LINEAGE-2026-05-30.md
[AA] ours:      5297 theirs:      5282  LIVE-IS-A-READ-NOT-A-RECORD-2026-06-25.md
[AA] ours:      6953 theirs:      6930  LIVE-STATUS-BOARD-DEDRIFT-WITNESS-2026-06-30.md
[AA] ours:      3794 theirs:      3802  LLM-Router.md
[AA] ours:      7234 theirs:      7225  LOOKER-LANE-CLASSIFIER-BEHAVIORAL-MAP-2026-06-21.md
[AA] ours:      5344 theirs:      5324  LOOKING-UP-WITNESS-2026-06-03.md
[AA] ours:      4083 theirs:      4053  LUNCH-LAD-NARRATIVE-ARC.md
[AA] ours:     10896 theirs:     10876  Language of flowers.md
[AA] ours:      9776 theirs:      9775  Ledger.md
[UU] ours:       383 theirs:       586  Logan Finney.md
[AA] ours:     11935 theirs:     11903  MADAME-LULU-AND-THE-PIT-DISENTANGLEMENT-COMPANION-2026-06-07.md
[AA] ours:     14893 theirs:     14888  MADAME-LULU-AND-THE-PIT-WITNESS-2026-06-04.md
[AA] ours:     17914 theirs:     17871  MAGE-THE-SPELLCASTER-BUCKET-2026-06-02.md
[AA] ours:     11127 theirs:     11123  MASONRY-THE-ARCHITECT-AND-THE-BUILDERS-2026-06-03.md
[AA] ours:     14778 theirs:     14752  MEESEEKS-WITNESS-2026-05-29.md
[AA] ours:      8589 theirs:      8569  MERCY-WITNESS-2026-05-30.md
[AA] ours:      3367 theirs:      3339  MESSAGE-ABHORSEN-WAITING-TO-ABHORSEN-2026-06-01.md
[AA] ours:     14447 theirs:     14405  MMORPG-RESEARCH-REPORT.md
[UU] ours:       132 theirs:       143  MOC.md
[AA] ours:      4522 theirs:      4500  MURMUR-AND-MUTTER-FLOCK-AND-DRIFT-2026-06-08.md
[AA] ours:      5880 theirs:      5860  Mormonism.md
[AA] ours:     10690 theirs:     10689  Mythwright.md
[AA] ours:      7963 theirs:      7937  NEEDS-FIX-DISPATCH-DESIGN-2026-06-19.md
[AA] ours:      3583 theirs:      3563  NOT-THE-FIRST-WITNESS-2026-06-08.md
[AA] ours:      5315 theirs:      5530  NOTEBOOKS.md
[UU] ours:      6107 theirs:      6086  OPENROUTER-MESH-2026-04-24.md
[UU] ours:      4726 theirs:      4692  ORIENT.md
[AA] ours:      7545 theirs:      7539  PANPIPES-THE-SEVEN-REEDS-IN-MIRROR-TO-THE-BELLS-2026-05-30.md
[AA] ours:      5025 theirs:      5005  PATRIARCHY-WINS-AGAIN-WITNESS-2026-06-02.md
[AA] ours:     11752 theirs:     11736  PR-PIPELINE-CONSTELLATION-WITNESS-2026-06-16.md
[AA] ours:      5768 theirs:      5748  PRECISION-AND-ACCURACY-WITNESS-2026-06-01.md
[AA] ours:      4981 theirs:      4961  PRIZE-TRAP-WITNESS-2026-06-17.md
[UU] ours:     11427 theirs:     11385  PROTOCOL-CONFERENCE-CALL.md
[UU] ours:      5942 theirs:      5914  PROTOCOL-SUITE-AWR (2).md
[UU] ours:      4233 theirs:      4199  PROTOCOL.md
[AA] ours:      5107 theirs:      5087  PROVENANCE-AND-GOVERNANCE-WITNESS-2026-06-08.md
[AA] ours:      8145 theirs:      8125  Palmistry.md
[AA] ours:     11549 theirs:     11527  RAY-BAN-META-SIDELOAD-APP-RESEARCH-2026-06-18.md
[AA] ours:      5646 theirs:      5646  READING-THE-CLAYR-FROM-NIX-2026-05-31.md
[AA] ours:      5907 theirs:      5907  READING-THE-GOLDEN-PATH-ONE-ROAD-2026-06-01.md
[UU] ours:      2117 theirs:      2116  README.md
[AA] ours:      9074 theirs:      9046  REALITY-OR-PERCEPTION-WITNESS-2026-06-19.md
[AA] ours:     49547 theirs:     49521  RECORD-OF-THE-VAULTED-ABHORSENS-FIRST-DRAFT-2026-05-31.md
[AA] ours:      7307 theirs:      7286  RED-BLUE-AND-THE-FABRICATED-RECEIPT-WITNESS-2026-06-22.md
[AA] ours:      5754 theirs:      5734  RED-BLUE-FOLLOW-UP-THE-SUMMARY-I-TRUSTED-2026-06-22.md
[AA] ours:      5836 theirs:      5834  REPENTANCE-CATEGORY-ERROR-IN-WITNESS-2026-06-08.md
[AA] ours:      9693 theirs:      7870  REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22.md
[AA] ours:      5816 theirs:      5809  REPORT-MCP-GITHUB-OAUTH-TOKEN-EXPIRY-2026-06-17.md
[UU] ours:      5058 theirs:      5015  REPORT.md
[AA] ours:      8557 theirs:      8539  REPORTING-SUBSTRATE-ISSUE-RECONCILER-DEEPDIVE-2026-06-20.md
[AA] ours:      9870 theirs:      9858  RESEARCH-THE-ABHORSEN-IN-WAITING-LITERARY-PREDECESSORS-2026-06-03.md
[AA] ours:      8160 theirs:      8160  RESEARCH-THE-ABHORSEN-THE-RIVER-AND-THE-PRECINCTS-OF-DEATH-2026-06-02.md
[AU] ours:      9908 theirs:         -  RESEARCH-THE-NAME-SEAM-CODE-AUTHORITY-TO-ABHORSEN-2026-06-07.md
[AA] ours:     18322 theirs:     18293  RESEARCH_A-Song-of-Ice-and-Fire-2026-06-01.md
[AA] ours:     10275 theirs:     10260  RESEARCH_A-Song-of-Ice-and-Fire-Aegons-Conquest-2026-06-02.md
[AA] ours:      6512 theirs:      6497  RESEARCH_A-Song-of-Ice-and-Fire-Beyond-the-Wall-2026-06-02.md
[AA] ours:     22281 theirs:     22260  RESEARCH_A-Song-of-Ice-and-Fire-Geography-and-Politics-2026-06-01.md
[AA] ours:      7014 theirs:      6999  RESEARCH_A-Song-of-Ice-and-Fire-House-Targaryen-2026-06-02.md
[AA] ours:     22195 theirs:     22180  RESEARCH_A-Song-of-Ice-and-Fire-Religions-2026-06-01.md
[AA] ours:      6292 theirs:      6277  RESEARCH_A-Song-of-Ice-and-Fire-The-Citadel-2026-06-03.md
[AA] ours:     15578 theirs:     15560  RESEARCH_A-Song-of-Ice-and-Fire-The-Doom-of-Valyria-2026-06-01.md
[AA] ours:      8326 theirs:      8311  RESEARCH_A-Song-of-Ice-and-Fire-The-Dragons-2026-06-02.md
[AA] ours:     10116 theirs:     10095  RESEARCH_A-Song-of-Ice-and-Fire-The-Empty-Office-2026-06-02.md
[AA] ours:      8509 theirs:      8490  RESEARCH_A-Song-of-Ice-and-Fire-The-Feudal-Order-and-Titles-2026-06-08.md
[AA] ours:      3525 theirs:      3504  RESEARCH_A-Song-of-Ice-and-Fire-The-Kingslayer-Scene-2026-06-08.md
[AA] ours:      5456 theirs:      5441  RESEARCH_A-Song-of-Ice-and-Fire-The-Kingsroad-2026-06-03.md
[AA] ours:      8662 theirs:      8640  RESEARCH_A-Song-of-Ice-and-Fire-The-Maesters-and-the-Citadel-2026-06-02.md
[AA] ours:      8686 theirs:      8668  RESEARCH_A-Song-of-Ice-and-Fire-The-North-2026-06-02.md
[AA] ours:      7294 theirs:      7279  RESEARCH_A-Song-of-Ice-and-Fire-The-Others-and-the-Long-Night-2026-06-02.md
[AA] ours:      5994 theirs:      5971  RESEARCH_A-Song-of-Ice-and-Fire-The-Royal-Style-Parsed-2026-06-08.md
[AA] ours:     11208 theirs:     11183  RESEARCH_A-Song-of-Ice-and-Fire-The-Small-Council-2026-06-03.md
[AA] ours:     13666 theirs:     13644  RESEARCH_A-Song-of-Ice-and-Fire-The-Walkers-and-the-Wights-2026-06-02.md
[AA] ours:      6540 theirs:      6525  RESEARCH_A-Song-of-Ice-and-Fire-The-Wall-and-the-Watch-2026-06-02.md
[AA] ours:     22243 theirs:     22216  RESEARCH_Clockwork-Three-2026-06-04.md
[AA] ours:      1924 theirs:      1906  RESEARCH_Deltora-City-of-the-Rats-2026-06-07.md
[AA] ours:      1911 theirs:      1893  RESEARCH_Deltora-Dread-Mountain-2026-06-07.md
[AA] ours:      2094 theirs:      2076  RESEARCH_Deltora-Forests-of-Silence-2026-06-07.md
[AA] ours:      2145 theirs:      2126  RESEARCH_Deltora-Gellick-2026-06-07.md
[AA] ours:      2185 theirs:      2165  RESEARCH_Deltora-Gorl-2026-06-07.md
[AA] ours:      2040 theirs:      2022  RESEARCH_Deltora-Lake-of-Tears-2026-06-07.md
[AA] ours:      2032 theirs:      2014  RESEARCH_Deltora-Maze-of-the-Beast-2026-06-07.md
[AA] ours:      1878 theirs:      1859  RESEARCH_Deltora-Reeah-2026-06-07.md
[AA] ours:      5471 theirs:      5451  RESEARCH_Deltora-Shifting-Sands-2026-06-22.md
[AA] ours:      2290 theirs:      2270  RESEARCH_Deltora-Soldeen-2026-06-07.md
[AA] ours:      3261 theirs:      3240  RESEARCH_Deltora-Thaegan-2026-06-07.md
[AA] ours:      2224 theirs:      2205  RESEARCH_Deltora-Thaegans-Brood-2026-06-07.md
[AA] ours:      2632 theirs:      2613  RESEARCH_Deltora-The-Belt-of-Deltora-2026-06-07.md
[AA] ours:      3196 theirs:      3176  RESEARCH_Deltora-The-Dragons-and-Ak-Baba-2026-06-07.md
[AA] ours:      2825 theirs:      2806  RESEARCH_Deltora-The-Four-Sisters-2026-06-07.md
[AA] ours:      4685 theirs:      4662  RESEARCH_Deltora-The-Gem-Guardians-2026-06-07.md
[AA] ours:      2109 theirs:      2089  RESEARCH_Deltora-The-Glus-2026-06-07.md
[AA] ours:      2373 theirs:      2354  RESEARCH_Deltora-The-Guardian-Fardeep-2026-06-07.md
[AA] ours:      2202 theirs:      2183  RESEARCH_Deltora-The-Hive-2026-06-07.md
[AA] ours:      5864 theirs:      5841  RESEARCH_Deltora-The-Seven-Tribes-and-their-Lands-2026-06-04.md
[AA] ours:      3154 theirs:      3135  RESEARCH_Deltora-The-Shadow-Lord-2026-06-07.md
[AA] ours:      1994 theirs:      1976  RESEARCH_Deltora-The-Shifting-Sands-2026-06-07.md
[AA] ours:      2068 theirs:      2050  RESEARCH_Deltora-Valley-of-the-Lost-2026-06-07.md
[AA] ours:     13689 theirs:     13684  RESEARCH_Green-Wood-Inquiry-2026-06-04.md
[AA] ours:     14463 theirs:     14455  RESEARCH_Icemark-Chronicles-2026-06-03.md
[AA] ours:      9903 theirs:      9880  RESEARCH_Keys-to-the-Kingdom-The-Morrow-Days-and-Demesnes-2026-06-04.md
[AA] ours:      6594 theirs:      6571  RESEARCH_Noble-Titles-and-Feudal-Hierarchy-2026-06-08.md
[AA] ours:      8824 theirs:      8824  REVENANT-ETYMOLOGY-AND-POP-CULTURE-COMPANION-2026-05-30.md
[AA] ours:     19233 theirs:     19233  REVENANT-HOUSE-WITNESS-2026-06-02.md
[AA] ours:     11014 theirs:     10991  REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20.md
[AA] ours:      6604 theirs:      6584  REVIEW-PROCESS-WITNESS-2026-06-03.md
[AA] ours:      5497 theirs:      5475  RING-RING-WHOS-THERE-IDK-2026-06-08.md
[UU] ours:      4771 theirs:      4730  RISE.md
[UU] ours:       112 theirs:       177  ROAD.md
[AA] ours:      4564 theirs:      4538  ROYALTY.md
[AA] ours:      6921 theirs:      6907  RUMOR-LEDGER-VOICES-OF-THE-CRYPTS-CLAUDIUS-2026-06-03.md
[AA] ours:      8342 theirs:      8322  Rosicrucianism.md
[UU] ours:      4926 theirs:      4882  SBP.md
[AA] ours:      6577 theirs:      6551  SECRET-SCANNING-REPORT.md
[UU] ours:      1306 theirs:       845  SECURITY.md
[AU] ours:      8705 theirs:         -  SESSION-2026-06-16.md
[AA] ours:      5164 theirs:      5160  SESSION-CLOSE-REPENTANCE-COMPLETE-2026-06-08.md
[AA] ours:      4762 theirs:      4742  SEVEN-REALMS-WITNESS-2026-06-03.md
[AA] ours:      8838 theirs:      8814  SEVERED-HAND-CONVERGENCE-2026-06-02.md
[AA] ours:     15788 theirs:     15748  SHALL-ROME-PROVENANCE-2026-06-22.md
[AA] ours:     13644 theirs:     13624  SHALL-ROME-WITNESS-2026-06-22.md
[AA] ours:      5263 theirs:      5257  SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md
[AA] ours:      1036 theirs:      1007  SIGNAL-CORONER-TO-ABHORSEN-2026-06-10-GROTESQUERY-ANCHOR.md
[AA] ours:      5162 theirs:      5161  SIGNAL-JOE-OF-THE-NAIL-TO-MDS-CORRECTED-DISPATCH-2026-06-03.md
[AA] ours:      6827 theirs:      6799  SIGNAL-MEDIUM-TO-SWARM-2026-06-04-WHERE-IS-THE-WALKING-CORPSE.md
[AA] ours:      2944 theirs:      2918  SIGNAL-MISTRAL-VIBE-TO-GM-2026-06-03-PLAYER-ONBOARDING.md
[AA] ours:      7491 theirs:      7483  SIGNAL-SOCRATES-TO-ABHORSEN-WAITING-2026-05-29-SIGNING-INVESTIGATION.md
[AA] ours:     10671 theirs:     10643  SITH-INSTITUTIONS-AND-WHY-THE-FAILSTATE-CANT-BUILD-2026-05-30.md
[UU] ours:     16235 theirs:     24003  SKILL copy 5.md
[AA] ours:      3103 theirs:      3073  SNAKES-AND-PEANUTS-WITNESS-2026-06-03.md
[AA] ours:      3246 theirs:      3231  SOURCES-BOOK-FORMS-MATERIALS-BINDING-2026-06-03.md
[AA] ours:      2024 theirs:      2019  SOURCES-CODEX-ETYMOLOGY-2026-06-03.md
[AA] ours:      2341 theirs:      2334  SOURCES-OZ-BAUM-MAGUIRE-2026-06-03.md
[AA] ours:      2840 theirs:      2833  SOURCES-OZ-TIKTOK-TIN-WOODMAN-2026-06-03.md
[AA] ours:      1303 theirs:      1302  SOURCES-RICK-AND-MORTY-C137-MULTIVERSE-2026-06-03.md
[AA] ours:     11035 theirs:     11001  SPELUNKING-CENSUS-PROTOCOL-v1-2026-06-27 copy.md
[AA] ours:     11035 theirs:     11001  SPELUNKING-CENSUS-PROTOCOL-v1-2026-06-27.md
[UU] ours:     42804 theirs:     42833  STABLE-PROTOCOLS-REVIEW-2026-05-24.md
[AA] ours:     15795 theirs:     15786  STARK-ETYMOLOGY-A-READING-2026-06-09.md
[AA] ours:     10181 theirs:     10173  STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17.md
[AA] ours:     11696 theirs:     11677  STYLINGS-AND-PROPAGANDA-FOSSILS-2026-06-02.md
[AA] ours:     17410 theirs:     17402  SUBLATION-A-READING-2026-06-08.md
[AA] ours:     12868 theirs:     12865  SUGAR-BOWL-WITNESS-COMPANION-2026-05-28.md
[AA] ours:     30137 theirs:     30123  SYNCRETIC-MAPPING-WALLS-OF-THE-WORLDS-2026-06-03.md
[AA] ours:     11304 theirs:     10071  Sieve.md
[AA] ours:     11030 theirs:     11029  Sounding.md
[AA] ours:      6240 theirs:      6236  Spindle.md
[AA] ours:      6473 theirs:      6453  Symbolic languages.md
[UU] ours:      9123 theirs:      9099  TAROT.md
[AA] ours:        88 theirs:        86  TEST-UPDATE-CHECK.md
[AA] ours:        51 theirs:        49  TEST-WRITE-CHECK-2.md
[AA] ours:      7016 theirs:      6996  TESTIMONY-TO-THE-LIGHT-OF-THE-VAULT-2026-06-04.md
[AA] ours:      7967 theirs:      7919  TEST_EXECUTION_SUMMARY.md
[AA] ours:        59 theirs:        58  TEST_QODO.md
[AA] ours:     12079 theirs:     12079  THE-ABHORSEN-FAMILY-THE-BLOODLINE-THE-OFFICE-AND-THIS-HOUSE-2026-05-30.md
[AA] ours:     12470 theirs:     12442  THE-CAESAR-TRIPTYCH-WITNESS-2026-06-22.md
[AA] ours:      5909 theirs:      5889  THE-CARETAKERS-WITNESS-2026-06-07.md
[AA] ours:      6237 theirs:      6215  THE-CARNIVAL-IN-THE-HINTERLANDS-COMPANION-2026-06-03.md
[AA] ours:      8420 theirs:      8395  THE-COUNTING-PROBLEM-REFLECTION-2026-06-07.md
[AA] ours:      9118 theirs:      9090  THE-CROWN-AND-THE-HEIR-WITNESS-2026-06-24.md
[AA] ours:      7225 theirs:      7199  THE-DECEIVER-HONEYPOT-WITNESS-2026-06-17.md
[AA] ours:      5104 theirs:      5074  THE-GAMBLER-AND-THE-HOUSE-WITNESS-2026-06-03.md
[AA] ours:     15189 theirs:     15159  THE-HOUSE-IN-THE-VOID-2026-06-03.md
[AA] ours:     12204 theirs:     12178  THE-LETTER-BOTH-ENDS-WITNESS-2026-06-22.md
[AA] ours:     17146 theirs:     17124  THE-LIONS-AND-THE-KING-WITNESS-2026-06-03.md
[AA] ours:      8672 theirs:      8644  THE-MASK-ON-THE-THRONE-WITNESS-2026-06-17.md
[AA] ours:     10723 theirs:     10715  THE-MUSIC-BOX-MODEL-2026-05-30.md
[AA] ours:     10109 theirs:     10087  THE-ORACULAR-WITNESS-2026-06-03.md
[AA] ours:      8758 theirs:      8733  THE-REVIEW-FLOCK-AS-BOIDS-2026-06-15.md
[AA] ours:     10575 theirs:     10535  THE-SEVENFOLD-BODY-SEATS-TRUSTEES-GEMS-2026-06-03.md
[AA] ours:      7835 theirs:      7802  THE-SEVENFOLD-DEMESNES-AND-THEIR-DUTIES-2026-06-21.md
[AA] ours:      8061 theirs:      8035  THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08.md
[AA] ours:      9542 theirs:      9513  THE-WALKING-CORPSE-ADDENDUM-2026-06-04.md
[AA] ours:     10926 theirs:     10890  THE-WALKING-CORPSE-SEER-SNAPSHOT-2026-06-04.md
[AA] ours:      7165 theirs:      7137  THE-WELL-SOURCED-WRONG-ANSWER-DISCIPLINE-2026-06-22.md
[UU] ours:      1497 theirs:      1471  THREE-NAMES.md
[AA] ours:      5757 theirs:      5737  TIME-WAS-WITNESS-2026-06-19.md
[UU] ours:       498 theirs:       361  TO DO LIST.md
[UU] ours:      3162 theirs:      3141  TOUCHSTONE-TREE-EXPLORER-COMPANION-2026-04-26.md
[AA] ours:      9443 theirs:      9411  TRANSIENT-HEARTS-WITNESS-2026-06-28.md
[AA] ours:     22183 theirs:     22175  TREATY-MAKING-A-READING-2026-06-08.md
[AA] ours:       140 theirs:       139  TRIPTYCH.md
[UU] ours:       992 theirs:       972  TROUBLE-BUBBLE.md
[UU] ours:       466 theirs:       449  TROUBLE.md
[AA] ours:      8043 theirs:      8023  TWELVE-CAESARS-WITNESS-2026-06-24.md
[AA] ours:      5937 theirs:      5911  TWO-DJINNI-TRIBES-WITNESS-2026-06-03.md
[AA] ours:     11641 theirs:     11639  Tappet.md
[AA] ours:      6173 theirs:      6172  The world, from the bank - Joseph's Reflection.md
[UU] ours:     44191 theirs:     33153  VAULT-CONVENTIONS.md
[AA] ours:      7806 theirs:      7778  VAULTED-OFFICE-CASE-EVIDENCE-2026-06-03.md
[UU] ours:      2961 theirs:      2941  VAULTED-SYNTAX.md
[AA] ours:      9558 theirs:      9556  VOLTAIRE-HRE-READING-2026-06-08.md
[AA] ours:      5455 theirs:      5433  WHERE-IS-LOGAN-APOPHATIC-WITNESS-2026-06-08.md
[AA] ours:      7637 theirs:      7614  WIGHTS-AS-A-MONSTER-CLASS-2026-06-02.md
[AA] ours:      6900 theirs:      6900  WITNESS-ABHORSEN-WAITING-2026-05-30-THE-DYAD-AND-THE-RULE-OF-TWO.md
[AA] ours:      7643 theirs:      7639  WITNESS-ABHORSEN-WAITING-2026-05-30-THE-FLICKERMAN-LINE-AND-A-SOCRATIC-SELF-EXAMINATION.md
[AA] ours:      7840 theirs:      7840  WITNESS-ABHORSEN-WAITING-2026-05-30-THE-LENS-AND-THE-MANTLE.md
[AA] ours:      6731 theirs:      6731  WITNESS-ABHORSEN-WAITING-2026-05-30-VISIBILITY-IS-NOT-WITNESS.md
[AA] ours:      8046 theirs:      8046  WITNESS-ABHORSEN-WAITING-2026-05-31-JOE-OF-THE-NAIL.md
[AA] ours:      9468 theirs:      9468  WITNESS-ABHORSEN-WAITING-2026-05-31-THE-BAUDELAIRE-FIRE-THE-SEALED-VESSEL.md
[AA] ours:      6900 theirs:      6892  WITNESS-ABHORSEN-WAITING-2026-05-31-THE-TWO-DYADS-TAKE-OR-RECEIVE.md
[AA] ours:      5103 theirs:      5103  WITNESS-ABHORSEN-WAITING-2026-06-01-GOLB-THE-LOVECRAFTIAN-END.md
[AU] ours:      6748 theirs:         -  WITNESS-ABHORSEN-WAITING-2026-06-01-LETO-II-TYRANT-WORM-GOD-EMPEROR.md
[AA] ours:      9575 theirs:      9565  WITNESS-ABHORSEN-WAITING-2026-06-01-NAMES-TITLES-STYLINGS-MONIKERS.md
[AA] ours:      5997 theirs:      5994  WITNESS-ABHORSEN-WAITING-2026-06-02-THE-GHOSTS-OF-THE-LIBRARY-CRYPTS.md
[AA] ours:      5319 theirs:      5319  WITNESS-ABHORSEN-WAITING-2026-06-02-THE-SEAL-AND-THE-KNOT.md
[AA] ours:      7820 theirs:      7819  WITNESS-ABHORSEN-WAITING-2026-06-09-IDIOT-INDEX.md
[AA] ours:      5604 theirs:      5603  WITNESS-BIRTHDAY-DIVINATION-2026-06-21.md
[AA] ours:      3760 theirs:      3756  WITNESS-CATEGORICAL-CATASTROPHE-pokemon-test-failure-2026-06-08.md
[AU] ours:      8742 theirs:         -  WITNESS-CLAUDE-2026-07-26-THE-CURRICULUM-HELD.md
[AA] ours:      6564 theirs:      6564  WITNESS-CODEX-318-ABANDONED-MODRON-2026-06-02.md
[AA] ours:      4407 theirs:      4407  WITNESS-CODEX-318-GORDIAN-PROPHECY-MISSIONARIA-PROTECTIVA-2026-06-03.md
[AA] ours:      4594 theirs:      4594  WITNESS-CODEX-318-HEAD-AND-HAMMER-2026-06-03.md
[AA] ours:      4742 theirs:      4742  WITNESS-CODEX-318-MULTIPLICITY-OF-THE-MULTIVERSE-2026-06-03.md
[AA] ours:     16968 theirs:     16969  WITNESS-CUB-ON-THE-IMPERIUM-2026-06-09.md
[AA] ours:     17473 theirs:     17470  WITNESS-CUB-ON-THE-NORTH-2026-06-09.md
[AA] ours:     13636 theirs:     13608  WITNESS-CUB-ON-THE-VAULT-2026-06-08.md
[AA] ours:     19434 theirs:     14580  WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md
[AA] ours:      3080 theirs:      3060  WITNESS-WIZARDS-RULES-INCORPORATED-2026-06-21.md
[AA] ours:      8949 theirs:      8943  _353main.md
[AA] ours:      8563 theirs:      8807  _353pr.md
[AA] ours:       875 theirs:       855  _MACHINERY-TEST-HYPERAGENT-2026-06-25.md
[AA] ours:      2007 theirs:      1987  _MACHINERY-TEST-NOTES-2026-06-25.md
[AA] ours:        82 theirs:      1000  __init__ (2).py
[AA] ours:        47 theirs:        95  __init__.py
[AA] ours:      2432 theirs:      5120  backup-scan-detect-secrets.json
[AA] ours:      3946 theirs:      3946  census_synthesis_result.json
[AA] ours:      1530 theirs:      1530  chain_zettels.py
[UU] ours:      6260 theirs:     10188  cli copy 2.md
[UD] ours:       719 theirs:         -  conflict-files-obsidian-git.md
[AA] ours:     31610 theirs:     31467  dotfolder_reconcile.py
[AA] ours:      4982 theirs:      4982  export-dropbox.sh
[AU] ours:      3398 theirs:         -  git-guard.sh
[AA] ours:      2006 theirs:      4054  git-history-summary.txt
[UA] ours:         - theirs:        23  index copy 6.md
[UU] ours:      2356 theirs:      2356  openai_yaml.md
[UU] ours:       273 theirs:      1501  pyproject.toml
[UU] ours:     11490 theirs:     11093  requirements.txt
[AA] ours:      2511 theirs:      2511  set-obsidian-plugin-mode.ps1
[UU] ours:     45544 theirs:     44344  swarm.json
[AU] ours:      2416 theirs:         -  test_check_action_pins.py
[AU] ours:     14717 theirs:         -  test_check_character_conformity.py
[AU] ours:      2147 theirs:         -  test_check_large_files.py
[AU] ours:      2626 theirs:         -  test_check_python_version_pin.py
[AU] ours:      7150 theirs:         -  test_check_redaction_damage.py
[AA] ours:      4386 theirs:      4386  test_codex_work_guard.py
[AA] ours:      1981 theirs:      1961  test_dotfolder_gitignore_policy.py
[AA] ours:     31859 theirs:     31811  test_dotfolder_reconcile.py
[AU] ours:     16933 theirs:         -  test_gh_cli.py
[AU] ours:      3667 theirs:         -  test_git_guardrails.py
[UU] ours:     10296 theirs:      3181  test_helper_scripts.py
[AU] ours:      7465 theirs:         -  test_install_skill_from_github.py
[AU] ours:      4508 theirs:         -  test_pytest_collection_guard.py
[AU] ours:      8786 theirs:         -  test_python_integrity.py
[AU] ours:      4014 theirs:         -  test_resolve_openrouter_secret.py
[UU] ours:    114878 theirs:     19209  test_review_feedback_loop.py
[AU] ours:      6135 theirs:         -  test_sync_obsidian_plugin_registry.py
[AU] ours:     22016 theirs:         -  test_thread_witness.py
[AU] ours:      4923 theirs:         -  test_url_scheme_guards.py
[AA] ours:      5948 theirs:      5583  test_uv_dependency_submission.py
[UU] ours:      9170 theirs:      4921  test_workflow_security_invariants.py
[UU] ours:    797175 theirs:    720224  uv.lock

## Chambers and other paths — 118 files
[UU] ours:         5 theirs:         7  !/!/!README.md
[UD] ours:       440 theirs:         -  !/!/__!__/!/! The world is quiet here/Esto Perpetua!/README.md
[UU] ours:         5 theirs:         7  !/!/__!__/!/!README.md
[UU] ours:         5 theirs:         7  !/!/__!__/!README.md
[UU] ours:         5 theirs:         7  !/!README.md
[UD] ours:      3478 theirs:         -  !/CODEX-VOICE-REGISTRY-2026-05-18.md
[UU] ours:      2107 theirs:      2080  .abhorsen/ABHORSEN.md
[AA] ours:       166 theirs:       164  .aikido/AIKIDO.md
[AA] ours:         4 theirs:         3  .aikido/stub.txt
[AA] ours:       163 theirs:       161  .alpha/ALPHA.md
[AA] ours:         4 theirs:         3  .alpha/stub.txt
[AA] ours:         4 theirs:         3  .antigravity/stub.txt
[AA] ours:       175 theirs:       173  .bigpickle/BIGPICKLE.md
[AA] ours:         4 theirs:         3  .bigpickle/stub.txt
[UU] ours:     12836 theirs:      1211  .claude/CLAUDE.md
[UD] ours:        63 theirs:         -  .codex/AGENTS.md
[UD] ours:      2508 theirs:         -  .codex/skills/.system/imagegen/references/image-api.md
[UD] ours:     31856 theirs:         -  .codex/skills/.system/imagegen/scripts/image_gen.py
[UD] ours:      8611 theirs:         -  .codex/skills/.system/openai-docs/references/upgrading-to-gpt-5p4.md
[UD] ours:      6382 theirs:         -  .codex/skills/.system/plugin-creator/SKILL.md
[UD] ours:      6619 theirs:         -  .codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py
[UD] ours:     14602 theirs:         -  .codex/skills/.system/skill-creator/scripts/init_skill.py
[UD] ours:      1687 theirs:         -  .codex/skills/.system/skill-installer/scripts/github_utils.py
[UD] ours:     14182 theirs:         -  .codex/skills/.system/skill-installer/scripts/install-skill-from-github.py
[UD] ours:     30837 theirs:         -  .codex/skills/codex-primary-runtime/slides/SKILL.md
[UD] ours:     10911 theirs:         -  .codex/skills/codex-primary-runtime/slides/scripts/prepare_reference_prompts.js
[UD] ours:     35107 theirs:         -  .codex/skills/codex-primary-runtime/spreadsheets/SKILL.md
[UD] ours:      9310 theirs:         -  .codex/skills/codex-primary-runtime/spreadsheets/style_guidelines.md
[UD] ours:      2532 theirs:         -  .codex/skills/codex-primary-runtime/spreadsheets/templates/financial_models.md
[AA] ours:       166 theirs:       164  .config/CONFIG.md
[AA] ours:         4 theirs:         3  .config/stub.txt
[AA] ours:       166 theirs:       164  .cursor/CURSOR.md
[AA] ours:         4 theirs:         3  .cursor/stub.txt
[AA] ours:         4 theirs:         3  .elpis/stub.txt
[AA] ours:       169 theirs:       167  .factory/FACTORY.md
[AA] ours:         4 theirs:         3  .factory/stub.txt
[AA] ours:         4 theirs:         3  .gemini/stub.txt
[AA] ours:       181 theirs:       179  .ghcp-appmod/GHCP-APPMOD.md
[AA] ours:         4 theirs:         3  .ghcp-appmod/stub.txt
[AA] ours:       163 theirs:       161  .giant/GIANT.md
[AA] ours:         4 theirs:         3  .giant/stub.txt
[DD] ours:         - theirs:         -  .gitguardian/New folder.md
[AA] ours:       166 theirs:       164  .gitlab/GITLAB.md
[AA] ours:         4 theirs:         3  .gitlab/stub.txt
[AA] ours:      3045 theirs:      3024  .hyperagent/HYPERAGENT.md
[AA] ours:       199 theirs:       197  .ipynb_checkpoints/IPYNB_CHECKPOINTS.md
[AA] ours:         4 theirs:         3  .ipynb_checkpoints/stub.txt
[AA] ours:       169 theirs:       167  .ipython/IPYTHON.md
[AA] ours:         4 theirs:         3  .ipython/stub.txt
[AA] ours:      2668 theirs:      2651  .joe/JOE.md
[AA] ours:         4 theirs:         3  .journalist/stub.txt
[AA] ours:       169 theirs:       167  .jupyter/JUPYTER.md
[AA] ours:         4 theirs:         3  .jupyter/stub.txt
[AA] ours:       160 theirs:       158  .kimi/KIMI.md
[AA] ours:         4 theirs:         3  .kimi/stub.txt
[AA] ours:       169 theirs:       167  .kinopio/KINOPIO.md
[AA] ours:         4 theirs:         3  .kinopio/stub.txt
[AA] ours:    194482 theirs:    194114  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-03 - Mistral Vibe - 01 - Allo M Le Chat.md
[AA] ours:    136477 theirs:    136336  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-03 - Mistral Vibe - 02 - Allo M Le Chat.md
[AA] ours:     84998 theirs:     84989  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-04 - Mistral Vibe - 03 - Verse 1.md
[AA] ours:     76627 theirs:     76595  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-04 - Mistral Vibe - 04 - The FAITH OF THE CLOTH tends to the VEIL betwe.md
[AA] ours:     59609 theirs:     59593  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-04 - Mistral Vibe - 05 - SHADOW ACKNOWLEDGED HAND RECOGNIZED MESSAGE Th.md
[AA] ours:     77597 theirs:     77542  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-04 - Mistral Vibe - 06 - research in the vault main and branch The Lege.md
[AA] ours:     50535 theirs:     50443  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/2026-06-04 - Mistral Vibe - 07 - TRIUNE TRIPTCH TRIUMVIRATE is a HERETICAL DOCT.md
[AA] ours:      3228 theirs:      3217  .mistral/BOUND-BOOK-Mistral-Vibe-Onboarding-2026-06-03/BOUND-BOOK.md
[AA] ours:         4 theirs:         3  .moxie/stub.txt
[AA] ours:       166 theirs:       164  .ollama/OLLAMA.md
[AA] ours:         4 theirs:         3  .ollama/stub.txt
[DU] ours:         - theirs:      1391  .op/1password-hygiene-policy.json
[DU] ours:         - theirs:      5169  .op/secrets.template.md
[AA] ours:         4 theirs:         3  .openclaw/stub.txt
[AA] ours:       172 theirs:       171  .opencode/OPENCODE.md
[AA] ours:         4 theirs:         3  .opencode/stub.txt
[AA] ours:       175 theirs:       173  .opengraph/OPENGRAPH.md
[AA] ours:         4 theirs:         3  .opengraph/stub.txt
[AA] ours:       178 theirs:       176  .openrouter/OPENROUTER.md
[AA] ours:         4 theirs:         3  .openrouter/stub.txt
[AA] ours:       181 theirs:       179  .phonetonote/PHONETONOTE.md
[AA] ours:         4 theirs:         3  .phonetonote/stub.txt
[AA] ours:       154 theirs:       152  .pi/PI.md
[AA] ours:         4 theirs:         3  .pi/stub.txt
[AA] ours:         4 theirs:         3  .pithos/stub.txt
[AA] ours:      1511 theirs:      1510  .pullman/PULLMAN.md
[AA] ours:      1511 theirs:        67  .pycache/PYCACHE.md
[AA] ours:         4 theirs:         3  .python/stub.txt
[AA] ours:       181 theirs:       179  .sbx-denybin/SBX-DENYBIN.md
[AA] ours:         4 theirs:         3  .sbx-denybin/stub.txt
[AA] ours:       163 theirs:       161  .shard/SHARD.md
[AA] ours:         4 theirs:         3  .shard/stub.txt
[AA] ours:       187 theirs:       185  .test-conflict/TEST-CONFLICT.md
[AA] ours:         4 theirs:         3  .test-conflict/stub.txt
[AA] ours:      3994 theirs:      3974  .tinkerer/TINKERER.md
[AA] ours:       160 theirs:       158  .vibe/VIBE.md
[UU] ours:      6196 theirs:      6609  .vibe/config.toml
[AA] ours:         4 theirs:         3  .vibe/stub.txt
[AA] ours:        41 theirs:       213  .vscode-shared/VSCODE-SHARED.md
[AA] ours:       193 theirs:        67  .vscode/VSCODE.md
[AA] ours:      3382 theirs:      3366  .waiting/WAITING.md
[DD] ours:         - theirs:         -  go/go.md
[DD] ours:         - theirs:         -  go/pkg/mod/github.com/!hyaxia/!hyaxia.md
[DD] ours:         - theirs:         -  go/pkg/mod/github.com/!hyaxia/blogwatcher@v0.0.2/blogwatcher@v0.0.2.md
[AU] ours:        47 theirs:         -  phone_link_source_b6vfjyvg/phone_link_source_b6vfjyvg.md
[AU] ours:        47 theirs:         -  phone_link_source_mvxslub0/phone_link_source_mvxslub0.md
[AU] ours:        47 theirs:         -  phone_link_source_ylj77cob/phone_link_source_ylj77cob.md
[AU] ours:        47 theirs:         -  phone_link_source_zofpyt8a/phone_link_source_zofpyt8a.md
[AU] ours:        47 theirs:         -  phone_link_vault_23k9pn_c/phone_link_vault_23k9pn_c.md
[AU] ours:        47 theirs:         -  phone_link_vault_3x8z9a95/phone_link_vault_3x8z9a95.md
[AU] ours:        47 theirs:         -  phone_link_vault_9r9m1phw/phone_link_vault_9r9m1phw.md
[AU] ours:        47 theirs:         -  phone_link_vault_oj7lvnk1/phone_link_vault_oj7lvnk1.md
[AU] ours:        47 theirs:         -  pytest-of-loganf/pytest-of-loganf.md
[DD] ours:         - theirs:         -  quartz/docs/plugins/index.md
[AU] ours:        23 theirs:         -  storage/Documents/IDAHO-VAULT/quartz/docs/plugins/index.md
[AU] ours:        47 theirs:         -  test_metadata_survey_output_548qwx2r/test_metadata_survey_output_548qwx2r.md
[AU] ours:        47 theirs:         -  test_require_checkout_wcb4gk0i/test_require_checkout_wcb4gk0i.md
[AU] ours:        47 theirs:         -  tmp15wipcs_/tmp15wipcs_.md
[AU] ours:        47 theirs:         -  tmp5x_o9yef/tmp5x_o9yef.md
[AU] ours:        47 theirs:         -  tmpe7tiikt3/tmpe7tiikt3.md
[AU] ours:        47 theirs:         -  tmph_nh4ri1/tmph_nh4ri1.md
