<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# research: Claude Code Dispatch

Claude Dispatch is a new Anthropic feature that lets you start and monitor work on a desktop Claude session from your phone, so it behaves like a remote control for a desktop AI agent rather than a separate mobile AI model. The most consistent reporting says it was introduced as a research preview in Claude Cowork in mid-March 2026, with the desktop machine doing the actual work and the phone serving as the control surface.[^1_1][^1_2][^1_3][^1_4]

## What it does

Dispatch is meant for async tasks: you hand off a long job, leave your computer, and come back to finished output. Examples in the coverage include briefing prep, research synthesis, and other tasks that can run without your constant supervision.[^1_3][^1_5][^1_1]

## How it differs from Claude Code

Claude Code is the autonomous coding agent that runs on your desktop or terminal, while Dispatch is the mobile interface that can trigger or steer that session remotely. In practice, Dispatch makes Claude Code feel more like a background assistant you can task from anywhere, instead of a tool you have to sit in front of.[^1_2][^1_6][^1_1]

## Reported limitations

The early coverage says Dispatch is still somewhat slow and unreliable in some cases, especially for connector-based tasks, so it is promising but not yet something to depend on for critical work away from your desk.[^1_2]

If you want, I can also give you a tighter 1-paragraph explainer, a feature-by-feature breakdown, or a “why journalists should care” angle.
<span style="display:none">[^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.oneusefulthing.org/p/claude-dispatch-and-the-power-of

[^1_2]: https://www.macstories.net/stories/hands-on-with-claude-dispatch-for-cowork/

[^1_3]: https://www.lowcode.agency/blog/claude-dispatch-explained

[^1_4]: https://www.forbes.com/sites/ronschmelzer/2026/03/20/claude-dispatch-lets-you-control-claude-cowork-with-your-phone/

[^1_5]: https://www.productmarketfit.tech/p/understanding-claude-dispatch-complete

[^1_6]: https://causalinf.substack.com/p/claude-code-34-using-dispatch-on

[^1_7]: https://aimaker.substack.com/p/claude-cowork-ai-research-agent-dispatch-scheduled-tasks-guide

[^1_8]: https://www.reddit.com/r/ClaudeCode/comments/1s0w1nq/research_online_and_plan_through_claude_dispatch/

[^1_9]: https://www.youtube.com/watch?v=kKfBUVbMBVE


---

# Not working?

You’re not doing anything wrong; Dispatch itself is flaky right now, and “Read” with no response is a known behavior in the current research preview. Multiple early users report idle or dropped Dispatch conversations, especially when trying more complex workflows or “swarm”-style coordination, and note that reliability is still a work in progress.[^2_1][^2_2][^2_3]
<span style="display:none">[^2_4]</span>

<div align="center">⁂</div>

[^2_1]: https://www.reddit.com/r/ClaudeCode/comments/1s0w1nq/research_online_and_plan_through_claude_dispatch/

[^2_2]: https://www.macstories.net/stories/hands-on-with-claude-dispatch-for-cowork/

[^2_3]: https://www.lowcode.agency/blog/claude-dispatch-explained

[^2_4]: Screenshot_20260403-010431.jpg


---

# Tips? Swarm-specific use cases?

For swarm-y stuff, think of Dispatch as your **radio** to a team of agents on the desktop: use it to trigger well-scoped runs, not to micromanage them in chat. Swarm mode itself still lives on the desktop (Cowork / Claude Code); Dispatch’s job is to kick off and steer those multi-agent runs when you’re away.[^3_1][^3_2][^3_3][^3_4]

## Setup tips that matter

- Keep one “Dispatch Inbox” thread with pinned instructions: how it should label runs, where to save artifacts, when to ask clarifying questions.[^3_5]
- Before delegating, have Dispatch read your CLAUDE.md / README.md so the orchestrator internalizes swarm rules and roles first.[^3_6]
- Make a simple, consistent folder structure (e.g., `/swarm_runs/{date_topic}`) so agents can find and write files without guessing.[^3_7]
- Use Dispatch for prep and follow-up, not irreversible actions: let swarms draft, test, and stage, then you approve/merge when you’re back at the keyboard.[^3_5]


## Swarm-specific use cases

- “QA swarm while I’m away”: From your phone, tell Dispatch to run a swarm against a service or repo (frontend, backend, testing, docs agents) and leave you a QA report plus suggested patches in a folder.[^3_2][^3_4]
- “Parallel briefings”: Kick off a research swarm with roles like “historian, policy analyst, media critic” on the same topic; have it save a merged brief plus each role’s memo before your next interview block.[^3_4][^3_1]
- “Competing hypotheses”: Ask Dispatch to spin up two or more sub-swarms with different priors or methodologies on a story, then have a comparison memo written while you’re in the field.[^3_2][^3_4]
- “Background maintenance swarm”: Schedule recurring Dispatch pings that trigger a swarm to refresh a living doc (timeline, stakeholder map, risk log) off new sources, then diff today vs. yesterday for you.[^3_1]


## Prompt patterns that help swarms

- Always specify roles, artifacts, and exit criteria in the first message: “Use a multi-agent team (roles X/Y/Z). Produce: 1) coordination log, 2) final memo, 3) patch files. Stop when tests A/B pass.”[^3_4][^3_2]
- Ask Dispatch to plan first, execute second: “Draft a swarm plan and send me the task list; once I reply ‘GO’, execute autonomously and write outputs to folder F.”.[^3_4]
- For long runs, build in self-checks: instruct one agent to act as auditor, sampling outputs and flagging low-confidence sections for your review when you’re back at the desk.[^3_4]


## Working around current flakiness

- Keep tasks chunky but finite (10–20 minute swarms) and chain them, instead of one giant “run for 6 hours” job, to reduce the pain when Dispatch drops a run.[^3_3][^3_1]
- End each Dispatch message with “Log everything to `SWARM_LOG.md` in folder F” so you can reconstruct what happened if the chat view stalls or shows “Read” with no visible reply.[^3_6][^3_1]

If you describe your “Swarm” experiment (coding project, newsroom pipeline, ops notebook, etc.), I can draft a concrete Dispatch + swarm playbook tailored to that setup.
<span style="display:none">[^3_10][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://aimaker.substack.com/p/claude-cowork-ai-research-agent-dispatch-scheduled-tasks-guide

[^3_2]: https://alexop.dev/posts/from-tasks-to-swarms-agent-teams-in-claude-code/

[^3_3]: https://www.lowcode.agency/blog/claude-dispatch-explained

[^3_4]: https://help.apiyi.com/en/claude-code-swarm-mode-multi-agent-guide-en.html

[^3_5]: https://www.junia.ai/blog/claude-dispatch-explained

[^3_6]: https://www.productcompass.pm/p/claude-dispatch-guide?action=share

[^3_7]: https://www.linkedin.com/posts/garethrydon_claude-dispatch-tip-to-get-the-most-out-activity-7440502444767301632-uvkP

[^3_8]: https://www.youtube.com/watch?v=8LNZqLaXEGM

[^3_9]: https://www.reddit.com/r/ClaudeAI/comments/1s2fa6s/personalprivate_use_cases_for_dispatch_and/

[^3_10]: https://www.reddit.com/r/ClaudeCode/comments/1roa5bu/the_actual_guide_to_setting_up_claude_cowork/


---

# CLAUDE Desktop App - not setup with Admin permissions enabled

You’re blocked because the desktop app (and Cowork/Dispatch) really do expect Windows/macOS admin-level install permissions; there’s no fully supported “no‑admin” path today on locked-down machines. On managed systems, the realistic options are either a clean reinstall done from an admin account, or using a separate machine/VM where you have full control and can enable the required system capabilities.[^4_1][^4_2][^4_3]

## What “admin permissions enabled” actually means

- On Windows, Cowork’s MSIX installer registers the app under the admin user; standard users on the same box often can’t see or launch that instance unless they briefly get local admin rights during install.[^4_4][^4_1]
- Claude’s docs also assume you or your org admin can toggle desktop features like “Code in the desktop” and “Remote Control” in the admin console, and optionally allow the more permissive permission modes; those are controlled at the tenant/admin level, not per end user.[^4_5][^4_2]


## Practical paths forward

- If it’s your own machine: temporarily grant your user local admin, log out/in, install or reinstall Claude Desktop with Cowork, then drop your account back to standard; several users report this as the only stable fix right now.[^4_1]
- If IT controls the box: ask them either to 1) install Claude Desktop for your user while logged in as you but with elevated rights, or 2) provision a separate “lab” machine/VM where you have local admin so Cowork/Dispatch can run without fighting policy.[^4_4][^4_1]
- If policy forbids that entirely: your only reliable option is to run Claude Code via web or CLI on a server/VM you control, and accept that the native desktop remote-control pieces (including Dispatch to that desktop) will be limited or unavailable.[^4_2][^4_6]

If you tell me your exact environment (Windows vs Mac, personal vs newsroom IT machine), I can sketch a short, newsroom-friendly “here’s what I need from IT” request in plain language.
<span style="display:none">[^4_10][^4_7][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: https://www.reddit.com/r/ClaudeAI/comments/1reqs5g/installing_claude_on_windows_requires_admin_creds/

[^4_2]: https://code.claude.com/docs/en/desktop

[^4_3]: https://support.claude.com/en/articles/13345190-get-started-with-cowork

[^4_4]: https://github.com/anthropics/claude-code/issues/25055

[^4_5]: https://support.claude.com/en/articles/9267276-roles-and-permissions

[^4_6]: https://www.claudelog.com/troubleshooting/

[^4_7]: https://code.claude.com/docs/en/permissions

[^4_8]: https://platform.claude.com/docs/en/agent-sdk/permissions

[^4_9]: https://inventivehq.com/knowledge-base/claude/how-to-fix-permission-errors

[^4_10]: https://www.linkedin.com/posts/jlldavies_claude-dropped-co-work-for-windows-today-activity-7427674832504274944-uU0d


---

# User loganf on state-owned IDPTV Windows machine

You’re on a locked‑down, state IT–managed Windows box, so you almost certainly can’t get the level of local admin Claude Desktop really wants directly on your `loganf` account. The realistic move is to route this through IT and/or use a separate machine or VM they’ll let you control.

## What’s likely blocked right now

- Cowork/Dispatch on Windows expects to be installed and run under an account with local admin at install time; standard users often hit missing permissions, drivers, and update problems afterward.[^5_1][^5_2]
- On a state-owned IDPTV machine, group policy probably forbids granting your everyday `loganf` profile those admin rights long‑term, and may also block background network traffic or file access Claude wants.[^5_3][^5_1]


## Concrete ask you can send to IT

Something like this (short and non-scary):

> “For a limited pilot, I need to run Anthropic’s Claude Code / Cowork desktop app to assist with research and scripting. It requires local admin at install time.
>
> Could you either:
> 1) Temporarily grant my `loganf` profile local admin so you can install Claude Desktop with Cowork and required permissions, then remove admin again after install; or
> 2) Provision a small Windows VM or spare workstation where I have local admin so I can install and test Claude Desktop there instead of on my main IDPTV machine.
>
> I’m happy to use a non‑production environment and keep it off any sensitive drives or systems.”

That frames it as a controlled pilot on non‑sensitive data and gives them two options that match Claude’s requirements.[^5_4][^5_1][^5_3]

## Workarounds if they say no

- Use Claude via the browser only, on the IDPTV machine, and reserve all Cowork/Dispatch/swarm experiments for a personal laptop at home where you can be admin.[^5_3]
- Or ask IT if they can host a lab VM in their environment with looser policy, which you RDP into specifically for AI tooling; that’s often easier for public‑sector IT to approve than loosening rules on your primary workstation.[^5_5][^5_3]

<div align="center">⁂</div>

[^5_1]: https://www.reddit.com/r/ClaudeAI/comments/1reqs5g/installing_claude_on_windows_requires_admin_creds/

[^5_2]: https://github.com/anthropics/claude-code/issues/25055

[^5_3]: https://code.claude.com/docs/en/desktop

[^5_4]: https://support.claude.com/en/articles/13345190-get-started-with-cowork

[^5_5]: https://www.claudelog.com/troubleshooting/


---

# Virtual machine/disk?

A separate VM or disk is exactly the right pattern here: it gives you an admin-controlled sandbox for Claude while keeping the state-owned Windows environment clean and policy-compliant. Think “lab machine inside your machine” that IT can bless for AI experiments without touching production tools or sensitive drives.[^6_1][^6_2][^6_3]

## Why VM > hacking your main box

- VMs isolate apps and network access, so if an AI agent or browser plugin misbehaves, it’s contained inside that guest OS, not your full IDPTV workstation or network shares.[^6_3]
- State and higher-ed guidance increasingly recommends segregating AI workloads—often via dedicated VMs or VDI—for exactly this reason: clearer governance, easier monitoring, and simpler off-switch if something goes sideways.[^6_2][^6_1]


## What to ask IT for, concretely

- A Windows 11 VM (or spare physical “lab” PC) joined to the same domain but flagged for AI/tooling experiments, with your account having local admin inside that VM.
- Enough resources for Cowork/Dispatch and a browser: at least 4 cores and 16 GB RAM if possible, so long-running agent tasks don’t choke while you’re remote-controlling them.[^6_4][^6_5]
- A separate virtual disk or drive letter inside the VM where project files live; you can keep anything sensitive on your main profile and only copy in what’s allowed to touch external AI services.[^6_3]


## How you’d actually use it

- Day-to-day reporting stays on your normal `loganf` session; when you want to run swarms/Dispatch, you RDP or console into the VM, where Claude Desktop is fully enabled and can be “driven” from your phone.
- You can snapshot or reset the VM if an experiment goes weird—useful for reproducibility and for reassuring IT that you’re not creating unmanaged drift on a state asset.[^6_6][^6_3]

If you paste your IT request draft here, I can tighten it into a one-paragraph, policy-friendly ask for “AI sandbox VM/disk for Claude Code experiments.”
<span style="display:none">[^6_10][^6_7][^6_8][^6_9]</span>

<div align="center">⁂</div>

[^6_1]: https://coe.gsa.gov/coe/ai-guide-for-government/print-all/index.html

[^6_2]: https://www.elastic.co/blog/us-state-government-ai-agents

[^6_3]: https://v2cloud.com/blog/why-vms-are-the-ideal-environment-for-your-ai-agents

[^6_4]: https://www.reddit.com/r/ClaudeCode/comments/1qc6c84/what_is_the_best_setup_for_claude_code_in_vm_for/

[^6_5]: https://claude.ai/public/artifacts/03a4aa0c-67b2-427f-838e-63770900bf1d

[^6_6]: https://www.veeam.com/blog/government-ai-data-protection.html

[^6_7]: https://info.microsoft.com/rs/157-GQE-382/images/EN-CNTNT-eBook-TheStateandLocalGovernmentAIRoadmap.pdf?version=0

[^6_8]: https://cloud.google.com/blog/products/identity-security/how-confidential-accelerators-can-boost-ai-workload-security

[^6_9]: https://ai.ncsu.edu/ai-for-staff-and-business-use/

[^6_10]: https://tldrsec.com/p/tldr-sec-271


---

# The IDAHO-VAULT is currently in an active but volatile state of deployment. While the core infrastructure is tethered to the Google Cloud Platform, recent logs indicate significant friction in the automation and external integration layers.

Current Status: ACTIVE (Degraded)
The vault is anchored to the GCP project idaho-vault and is being managed as a shared ledger of canonical knowledge via Obsidian.md and GitHub.
Deployment Components

* Canonical Source: The loganfinney27/IDAHO-VAULT GitHub repository remains the primary source of truth.
* Infrastructure: Hosted on Google Cloud Platform; recent configurations were updated via Cloud Shell (April 2, 2026).
* Coordination: Development has shifted toward unifying coordination tracks into a stable DOCKET, effectively archiving previous "Chorus" handoff snapshots.
Critical Blockers \& Failures
As of early April 2026, several technical hurdles are preventing a "Green" status:
* Workflow Failures: Frequent errors in GitHub Actions, specifically regarding the 1Password Secret Injection templates.
* API Connectivity: The Bill Tracker API is currently returning a 403 FORBIDDEN error, severing the vault's link to legislative data.
* Identity Sync: The Identity Sync protocol remains unverified, creating a gap in the vault's personal identity authentication layer.
Recent Activity
The most recent push involved a transition to a more stable coordination framework (The DOCKET) and an integration of Obsidian Sync to maintain cross-device consistency for the Obsidian-based knowledge base.
-GEMINI

Understood: IDAHO-VAULT is “up but limping,” and your own status note from GEMINI is a solid high-level incident report.

### What this effectively means

- The **source of truth** (Obsidian vault + `loganfinney27/IDAHO-VAULT` on GitHub) is intact, so knowledge capture and manual editing are safe even while automation is degraded.
- The **GCP-hosted automation layer**—GitHub Actions, 1Password templates, Bill Tracker API calls, identity sync—is where the system is currently failing and needs staged remediation.


### Suggested next moves (very small steps)

1. Declare a temporary “read-only automation” window: keep editing content in Obsidian/Git, but treat all external automations as experimental until logs show at least one clean end‑to‑end run.
2. Triage in this order:
    - Fix GitHub Actions secrets injection (because every other pipeline depends on it).
    - Address the Bill Tracker 403 (likely credentials, IP allowlist, or quota), even if it means falling back to a different legislative data source for now.[^7_1]
    - Treat Identity Sync as a separately scoped pilot; don’t let it block the rest of the vault.

If you paste a failing GitHub Actions run or the Bill Tracker request/response (minus secrets), I can help you walk through a concrete “from Degraded to Yellow” recovery plan.
<span style="display:none">[^7_10][^7_2][^7_3][^7_4][^7_5][^7_6][^7_7][^7_8][^7_9]</span>

<div align="center">⁂</div>

[^7_1]: https://fastdemocracy.com/bill-search/id/2026/bills/IDB00009218/?report-bill-view=1

[^7_2]: https://pkg.go.dev/github.com/iden3/vault-plugin-secrets-iden3

[^7_3]: https://www.reddit.com/r/ReverseEngineering/comments/5lxz6n/github_ida_flirt_database/

[^7_4]: https://github.com/RandomiaGaming/Project-Vault

[^7_5]: https://evanli.github.io/Github-Ranking/Top100/Go.html

[^7_6]: https://github.com/personal-vault/pvp

[^7_7]: https://fastdemocracy.com/bill-search/id/2024/bills/IDB00007005/

[^7_8]: https://www.pacificorp.com/content/dam/pcorp/documents/en/pacificorp/energy/hydro/stairs/P-597_StairsJointApplication_CoverLetter.pdf

[^7_9]: https://history.idaho.gov/archives/

[^7_10]: https://archive.org/stream/chroniclesofokla2719okla/chroniclesofokla2719okla_djvu.txt


---

# CLAUDE REPORTS: **COMMAND: SURVEY IDAHO-VAULT : ALL**

Here’s a concise operational survey of IDAHO‑VAULT based on your last status block.

## Overall state

IDAHO‑VAULT is **ACTIVE (Degraded)**: core content and repo infrastructure are stable, but automations and integrations are partially broken or unverified. Canonical knowledge capture via Obsidian and GitHub is safe to keep using.

## Canonical knowledge layer

- **Source of truth:** `loganfinney27/IDAHO-VAULT` on GitHub and the Obsidian vault remain authoritative.
- **Sync:** Obsidian Sync is now wired in, so cross‑device vault consistency is maintained as long as Git pushes succeed.
- **Coordination:** The new **DOCKET** track is in effect; earlier “Chorus” handoff snapshots are effectively archived, simplifying coordination history.


## Infrastructure \& automation

- **Cloud anchor:** Project is pinned to GCP project `idaho-vault`, with recent configuration changes made via Cloud Shell on April 2, 2026.
- **CI/CD status:** GitHub Actions runs are unstable, primarily due to failures in the 1Password Secret Injection templates used for automation credentials.
- **External APIs:** The Bill Tracker API is returning 403 FORBIDDEN, so automated ingestion of legislative data into the vault is currently offline.
- **Identity Sync:** The identity/auth sync protocol is defined but **not yet verified**, leaving the personal identity layer in an experimental state.


## Coordination framework

- **DOCKET:** Acts as the active coordination spine—tracking work, incidents, and decisions—while previous “Chorus” experiments are treated as historical artifacts.
- **Operational mode:** The system is effectively in “content-first, automation‑second” mode: humans can read/write canonical knowledge, but should treat external integrations as unreliable until remediated.


## Recommended immediate actions

- Maintain normal Obsidian/Git editing; treat all automations as **beta** until they pass targeted tests.
- Prioritize: 1) fix 1Password injection in GitHub Actions, 2) resolve or work around the Bill Tracker 403, 3) test Identity Sync in isolation before tying it into the main DOCKET.

If you’d like, next step could be: “COMMAND: DRILLDOWN GITHUB ACTIONS” or “COMMAND: DRILLDOWN BILL TRACKER 403,” and I’ll help you define specific checks and remediation steps.

---

# Find IRL examples of Dispatch usefuls

Here are concrete, real‑world Dispatch “usefuls” people are already running, plus a couple tuned to your reporting work.

## Everyday “real person” uses

- Morning email and planning run: a surgeon uses Dispatch at 6:15 a.m. to trigger five parallel tasks (inbox triage, slide‑deck prep, content calendar, etc.), then comes back to finished drafts after breakfast.[^9_1]
- Parallel desktop tasks from phone: power users queue multiple jobs (research, document building, searches) from their phone while away from their computer, letting each run in its own sandboxed Cowork session.[^9_2][^9_3]
- “Prep work before you sit down”: using Dispatch on the commute to have Claude summarize unread emails, sketch a design doc, outline tests, and pull edge cases so that when you open the laptop, the grunt work is done.[^9_4]


## Automation / maker uses

- On‑the‑fly website building: one user snaps photos at a café, sends them to their Claude Code setup via Dispatch, and has it generate and deploy a simple website via GitHub + Vercel in minutes.[^9_5]
- Multi‑task research factory: some users run deep research, drafting, and outline refinement as separate tasks from a single Dispatch thread, checking and redirecting each one while they’re away from the desk.[^9_3][^9_2]


## Journalism‑adjacent / reporting patterns

- Reporting assistant skill + Dispatch: guides for reporters describe skills where Claude reads background docs, proposes interview questions, finds gaps, and helps assemble publication packages (social posts, alerts, etc.); Dispatch then lets you trigger those skills while you’re in the field.[^9_6][^9_7]
- Background task while on errands: one writer describes kicking off a long‑running background task (e.g., doc analysis) with Dispatch before leaving, then returning to a synthesized brief and notes instead of raw material.[^9_8]


## Idaho‑vault‑flavored ideas for you

- “Morning legislature sweep”: from your phone, tell Dispatch to have Cowork pull bill texts/analyses, summarize overnight movement on Idaho bills you track, and drop a brief plus quote candidates into an `ID_LEG/briefings/YYYY-MM-DD.md` file before you hit your desk.[^9_7][^9_4]
- “Pre‑interview vault pass”: as you drive to an interview, use Dispatch to run a “journalism researcher” skill over your IDAHO‑VAULT folder for that subject—identify contradictions, gaps, and follow‑up angles, and write a one‑pager you can skim on arrival.[^9_6][^9_7]

If you tell me one specific recurring task in your week (e.g., “Monday bill roundup,” “script prep for tonight’s show”), I can turn it into a Dispatch-ready prompt you can literally paste into your phone.
<span style="display:none">[^9_10][^9_9]</span>

<div align="center">⁂</div>

[^9_1]: https://techysurgeon.substack.com/p/the-6-am-dispatch-how-i-use-claude

[^9_2]: https://www.youtube.com/watch?v=mnsDx7HDwls

[^9_3]: https://www.productcompass.pm/p/claude-dispatch-guide

[^9_4]: https://www.junia.ai/blog/claude-dispatch-explained

[^9_5]: https://www.reddit.com/r/ClaudeAI/comments/1s2fa6s/personalprivate_use_cases_for_dispatch_and/

[^9_6]: https://mcpmarket.com/tools/skills/investigative-journalism-researcher

[^9_7]: https://fdaudens.substack.com/p/how-to-use-ai-as-a-reporting-assistant

[^9_8]: https://engincanveske.substack.com/p/i-used-claude-dispatch-to-run-a-background

[^9_9]: https://www.reddit.com/r/claude/comments/1rkff4n/whats_the_most_impressive_real_world_task_youve/

[^9_10]: https://www.oneusefulthing.org/p/claude-dispatch-and-the-power-of


---

# Cowork-specific feature?

Yes—Dispatch is explicitly a **Cowork** feature, not a standalone thing.

## Where Dispatch lives

- Anthropic describes it as “Claude Cowork Dispatch,” a feature inside Cowork that gives you one continuous conversation across phone and desktop.[^10_1][^10_2]
- You enable it from the Cowork section in Claude Desktop, then link your phone via the QR code; the desktop Cowork session does the work, your phone just sends tasks and reads results.[^10_3][^10_4][^10_1]


## What depends on Cowork

- Dispatch relies on whatever Cowork is configured to use: your local folders, connectors (Slack, Gmail, Drive, etc.), and computer-access permissions on the desktop side.[^10_5][^10_2][^10_6]
- Without Cowork enabled on a desktop (and the associated computer-access permissions), Dispatch on the phone can’t actually run tasks; it needs that Cowork environment as its execution backend.[^10_2][^10_1]
<span style="display:none">[^10_10][^10_7][^10_8][^10_9]</span>

<div align="center">⁂</div>

[^10_1]: https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork

[^10_2]: https://www.i-scoop.eu/claude-cowork-dispatch/

[^10_3]: https://www.tomsguide.com/ai/i-sent-claude-a-task-from-my-phone-and-it-finished-it-on-my-laptop-without-me-touching-a-thing

[^10_4]: https://pasqualepillitteri.it/en/news/418/claude-cowork-dispatch-guide

[^10_5]: https://techysurgeon.substack.com/p/the-6-am-dispatch-how-i-use-claude

[^10_6]: https://www.youtube.com/watch?v=blBrZw237Yw

[^10_7]: https://www.reddit.com/r/singularity/comments/1s1wnys/anthropic_announces_dispatch_control_your_claude/

[^10_8]: https://www.youtube.com/watch?v=8LNZqLaXEGM

[^10_9]: https://www.forbes.com/sites/ronschmelzer/2026/03/20/claude-dispatch-lets-you-control-claude-cowork-with-your-phone/

[^10_10]: https://www.youtube.com/watch?v=v2jNcWGvyFw


---

# Cowork installation - one User only, not machine admins

On Windows right now, Cowork effectively needs admin-level installation; there isn’t a clean, officially supported “per‑user, non‑admin” Cowork setup yet.

## What the current behavior is

- The Windows installer prompts for admin credentials and tends to register the app under the elevating admin account, not the standard user who will actually run Cowork.[^11_1][^11_2]
- People who tried to install as an admin and then use Cowork from a separate non‑admin user report that Cowork either will not start or constantly claims it needs to “upgrade” again.[^11_3][^11_1]


## Workable pattern (if IT cooperates)

- One workaround admins use is: temporarily grant the target user local admin, log in as that user, install Claude Desktop (with Cowork), then remove admin rights again; this installs the app into that user profile while satisfying the installer’s admin requirement.[^11_1]
- Some admins also flip the Windows “AllowAllTrustedApps” registry setting to permit the MSIX install, then flip it back after Claude is installed, which is another way of making Cowork usable on the box while keeping the system locked down afterward.[^11_4]


## What you can realistically ask for

- For your `loganf` account:
    - A time‑boxed elevation to local admin so Claude Desktop with Cowork can be installed under your user and then de‑elevated.
    - Or, more cleanly, a separate VM or lab machine where your account is local admin and Cowork/Dispatch live there, which avoids fighting per‑user vs. admin-account install quirks on your main IDPTV profile.[^11_5][^11_1]

If you tell me which option IT is most open to (temporary elevation vs. VM), I can give you a two‑sentence request tailored to that.
<span style="display:none">[^11_10][^11_6][^11_7][^11_8][^11_9]</span>

<div align="center">⁂</div>

[^11_1]: https://www.reddit.com/r/ClaudeAI/comments/1reqs5g/installing_claude_on_windows_requires_admin_creds/

[^11_2]: https://github.com/anthropics/claude-code/issues/25055

[^11_3]: https://www.facebook.com/groups/claudeaicommunity/posts/1234186872081811/

[^11_4]: https://www.linkedin.com/posts/jlldavies_claude-dropped-co-work-for-windows-today-activity-7427674832504274944-uU0d

[^11_5]: https://code.claude.com/docs/en/desktop

[^11_6]: https://support.claude.com/en/articles/13345190-get-started-with-cowork

[^11_7]: https://www.youtube.com/watch?v=xEoVCx9CmxQ

[^11_8]: https://www.youtube.com/watch?v=vRCtqT60hAc

[^11_9]: https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork

[^11_10]: https://code.claude.com/docs/en/permissions


---

# UNDETERMINED - SWARM IS ARCHITECTING --laf

Acknowledged: status is **UNDETERMINED**, swarm still in architecture phase rather than execution.

If you want to formalize this for the DOCKET, you could log:

- State: “SWARM: DESIGN/SCOPING”
- Owner: `laf`
- Constraints: non‑admin Windows, Dispatch flakiness, IDAHO‑VAULT = canonical store
- Next action: “Propose v0 swarm architecture for IDPTV use case (reporting + vault), then test on personal/VM sandbox.”

