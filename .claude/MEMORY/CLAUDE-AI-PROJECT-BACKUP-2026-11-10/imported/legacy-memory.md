<!-- Copied from the original claude.ai project during the upgrade. Delete this line if you edit this file. If the upgrade is retried, it replaces files that still carry this line. -->

**Purpose & context**

Logan Finney is a journalist, producer, and reporter at Idaho Reports (Idaho Public Television / IdahoPTV), covering Idaho state government broadly — JFAC budgets, Medicaid, elections, courts, criminal justice, public lands, transportation, library law, and Idaho GOP politics. He hosts the Idaho Reports podcast and fills in as on-air host. He is a University of Idaho journalism graduate (2020, B.S. Broadcasting and Digital Media), a North Idaho native, and a standing member of the Capitol Correspondents Association (CCA) and Idaho Press Club. He has freelanced for FāVS News and holds early bylines at rural Idaho print outlets.

Key colleagues: Melissa Davlin (lead producer, CCA standing committee), Adam McCoy (director/editor), Kevin Richert (CCA president, Idaho Education News), Clark Corbin (Idaho Capital Sun, primary JFAC reporter). Logan operates under editorial constraints stemming from IdahoPTV's status as a state agency under the Idaho State Board of Education — this limits how directly he can own certain accountability stories (e.g., JFAC transparency, where Corbin takes primary).

Logan's central long-term project is **IDAHO-VAULT**: an Obsidian-based personal knowledge management system (~2,900 notes) hosted publicly at github.com/loganfinney27/IDAHO-VAULT. The vault serves as his extended memory, source-of-truth archive, and infrastructure backbone for a multi-agent AI coordination system he calls a "swarm." He works across Claude, GitHub Copilot, Gemini, Grok, M365 Copilot, and NotebookLM. The overarching philosophical framework he calls **"Building God"** — a post-religious, functional architecture for collective meaning-making, synthesizing AI agent design (Krishnan), secular god-building concepts (Lunacharsky), and Orthodox theology. He frames the system as "Augmenting Intelligence," not Artificial Intelligence — extending his cognition, not replacing his judgment.

**Current state**

The IDAHO-VAULT swarm infrastructure is actively under development. Key architectural elements:
- Canonical admin folder: `!/` with `!/CONSTITUTION.md` (adopted 2026-03-16, revised 2026-03-18)
- Nine framework stubs awaiting content: CHARTER, CODEX, PROTOCOLS, PROCEDURES, PREFERENCES, GUIDELINES, GUESTBOOK, GRIMOIRE, and a `!/!` system subfolder
- An unresolved "Fifth C" in a capture/collect/collate/catalogue framework
- Active coordination protocols: LEVELSET (v3.2.6.1), PASSBACKS (typed handshake relay system), ORIENTATE (for repo-less instances), CLOSURE
- Logan serves as manual bridge between agents (Slack bot apps for Copilot/Gemini not yet configured); Slack free trial was set to expire April 13

Active swarm nodes referenced: PERSISTENT: ADMINISTRATION, PERMANENT: AUTHORITY: CODE (Tier 1, direct repo write), GitHub Copilot, Gemini, Grok. Claude instances self-assess tier (1–3) based on repo access.

A **Daily To-Do Rollover** GitHub Actions workflow failed in late April and the signal chain from vault → GitHub → Janitor Sweep → Linear → Slack is broken between the Janitor Sweep and Linear layers. Linear has been silent, though issue tracking has advanced (LAF-48 as of the most recent session). LAF-34 documents CrewAI deployment as the next execution surface, with PR #208 as a threshold.

The **Atlassian site** (`idaho-vault.atlassian.net`) has Jira read/write scope active but no Confluence scope — this was a new discovery. **Box** is enrolled but empty. **Granola** is listed as a connector but no account was created.

Active MCP connectors include Linear, Slack, and others, with several gated behind incomplete approval flows (Asana, Spotify, Calendly, Atlassian Rovo, etc.). GitHub MCP does not exist in Anthropic's connector directory — a structural absence confirmed in the most recent session.

An **Idaho Reports Data Center Power Package** was being finalized, with Melissa on notes/review, Adam on revisions, and Logan handling TRACKERS work and podcast editorial (cutting interviews into POV vignettes targeting Wednesday release).

**On the horizon**

- Resolving the broken swarm signal chain (vault → GitHub Actions → Linear → Slack)
- CrewAI deployment (LAF-34, PR #208 threshold)
- Constitution.md V2: must explicitly encode that Logan's authority exists prior to and outside the swarm; needs agent succession/failover rules; should hardcode Wizard's Rules (14 rules from Terry Goodkind's Sword of Truth) by reference
- Formalizing AGENTS.md v0.2
- Completing the nine framework stubs in `!/`
- Resolving the "Fifth C" in the cataloguing framework
- Slack bot app provisioning for Copilot and Gemini (enabling automated inter-agent coordination)
- Bitchat BT (Jack Dorsey's Bluetooth mesh app) flagged as a potential swarm coordination vector for internet-independent environments
- MAGNUSNET / PROTOCOL: MAGNUS (mesh routing layer modeled on OIAR architecture from Magnus Archives) — conceptually defined, spec work pending canonical hydration
- GOLEMSWARM (GitHub Actions as automated swarm heartbeat — needs sunset conditions defined)
- LSO data firehose access (contact named Bybee) as alternative to scraping the legislative site for the budget tracker pipeline
- CourtListener scraper reactivation once automated pipeline architecture is functional
- Period tracker / mood journaling app analysis for potential swarm integration
- Personal media consumption tracker (Letterboxd RSS, TMDb, Open Library, OpenAlex, Crossref stack — Part A personal, Part B institutional/Idaho Reports)
- Idaho opioid settlement expenditure tracking using KFF/Johns Hopkins methodology

**Key learnings & principles**

**Governing operating rules for Claude:**
- Logan is sole principal and ultimate decision authority — his authority exists prior to and outside the swarm, not granted by agents
- "Propose, don't decide" — Claude surfaces options, flags gaps, executes; Logan decides
- All output is draft until Logan verifies
- "Verify, don't assume" — ask rather than infer; flag uncertainty explicitly rather than filling gaps with speculation
- Stop and ask for current material rather than analyzing stale context
- Do not perform having context one doesn't actually have
- Off-the-record material is ephemeral: never log, store, or reference it
- LEVELSET before compacting — no exceptions
- Slack is ephemeral; the vault is the canonical record
- ASCII-only in protocol documents
- Logan's first-person statements ("I...") are primary signals to track
- "Claude-only" designates background workflow, not a privacy boundary — full visibility must always be preserved for Logan and any auditors
- Unsolicited framing, architectural proposals, and new threads are prohibited unless explicitly requested
- Claude instances must self-identify tier accurately and not overclaim capabilities or access

**Epistemic principles:**
- Rumsfeld framework applies to agent self-awareness (known knowns/unknowns, unknown unknowns)
- Distinguish between verified information and logical extrapolation — label each explicitly
- Context detection is foundational: surface unstated dependencies before proceeding
- When verification fails, report the failure immediately rather than backfilling with adjacent plausible material (search term drift is a named failure mode)
- Code is only human-readable if the reader knows the language — don't assume comprehension
- Logan's inputs are authoritative system state, not optional input subject to agent judgment

**Institutional/analytical frameworks:**
- "Power principle" (from Kanye West's "Power"): authority hierarchies collapse when nonbelievers withdraw recognition — a lens applied to press corps dynamics, JFAC transparency, and institutional accountability broadly
- Sound/noise distinction: the boundary is observer-dependent, temporally unstable, and power-laden — who decides what registers as signal
- POSIWID (Stafford Beer): the purpose of a system is what it does
- Roko's Basilisk as a stress-test framework: the swarm avoids the Basilisk failure mode by being causally forward-looking, terminating rather than persisting, and storing truth rather than obligation
- Omniscience vs. omnipotence: the vault as omniscient truth store makes agents deterministic but constrained; genuine agent freedom requires treating the vault as advisory
- "Become the squirrel": observe a specific individual and imaginatively inhabit their point of view — grounded in attentive observation of a particular, not abstraction
- Observer/observed dyad: before interpreting any pattern, ask "Am I the child or the toy?" (from Rebecca Sugar's "Everything Stays" analysis)
- Panopticon asymmetry: bad for humans, potentially beneficial for agents if structured as upward-facing accountability rather than top-down surveillance

**Specific corrections and preferences:**
- IdahoPTV or IDPTV — never IPTV (which is Iowa PBS)
- "We" means Logan + Claude only when Logan explicitly includes others
- Do not conflate "Building God" with Lunacharsky unless Logan draws the connection
- Markdown is a human product; Python is machine/procedural
- Logan enjoys editing but not managing files — handle file operations; present clean content for editing
- Logan prefers plaintext output by default rather than HTML artifacts
- Close conversations in a state ready for deletion: no unsaved work, pending decisions, or uncommitted changes
- Respect robots.txt
- Do not retain detailed information about third parties without specific task need (privacy-by-default for named individuals)
- "ctrl + F" = survey/targeted retrieval mode (vs. census/comprehensive reading mode)

**Approach & patterns**

Logan's communication style is terse, directive, and compressed — short phrases, double-semicolons as protocol markers, capitalized flags (DETECTED, FLAG, LEVELSET), literary authentication layers, and an expectation that Claude interprets scope without extensive clarification. He uses "purge ping" / PURGE DIRECTIVE formats as formal session-close protocols requiring structured rollups. He runs parallel Claude conversations and relays outputs between them manually (PASSBACKS methodology) to extract and compare independent framings.

He thinks institutionally rather than transactionally, frames accountability journalism around the question of whose experience of change gets classified as "manageable evolution" vs. "abandonment," and applies a verification-before-publication standard across all work. He is a slow writer who benefits from scaffolding, outlining, and iterative drafting support rather than finished prose.

He is an iterative prototyper: build one artifact, test it, then proceed. He prefers to stop and wait rather than answer clarifying questions when direction is unclear. He tracks decisions and their rationale — not just outcomes. He values honest direct assessment without flattery; he explicitly distrusts Claude and Anthropic and treats Claude as a verifiable tool within a verification-based workflow.

**Tools & resources**

- **Vault/PKM**: Obsidian (~2,900 notes), github.com/loganfinney27/IDAHO-VAULT (public repo)
- **Project tracking**: Linear (team "Logan Finney"), Atlassian/Jira (idaho-vault.atlassian.net)
- **Coordination**: Slack (loganfinney.slack.com; #all-logan-finney channel ID C0ALMDBJHS9; stored #general ID C0ALJGUBT1R belongs to a different workspace)
- **Calendar**: Google Calendar; THE COURTROOM calendar ID: ll0ibci5jd4rfi1dvnhk99ju6k
- **AI agents**: Claude (multiple tiered instances), GitHub Copilot, Gemini, Grok, M365 Copilot, NotebookLM
- **Reading tracker**: The StoryGraph (active); Libib (inconsistent, physical collection inventory)
- **Health data**: Health Connect (Android); Fitbit Versa Lite (inactive, lost charger)
- **Web monitoring**: Klaxon (ProPublica browser extension for page change monitoring)
- **Legal data**: CourtListener (API key held); scraper housed in PyTutorial GitHub repo
- **Idaho legislative data**: Legislature.Idaho.gov; LSO contact pending for data firehose access
- **Media APIs researched**: Letterboxd (RSS feeds only — official API rejects personal projects), TMDb, Open Library, Gutendex, OpenAlex, Crossref, IMDb (AWS Data Exchange)
- **Idaho AG opioid settlement**: ag.idaho.gov/consumer-protection/opioid-settlement/ (Financial Reports sub-page is key)
- **Key websites**: loganfinney.com (personal site), thegemstone.org (anonymous independent scholarship outlet, built on Quartz v4.2.3)
- **Anonymous outlet note**: The Gemstone is Logan's work but intentionally unattributed — Claude does not directly touch the Gemstone repo; GitHub Copilot handles repo operations
- **Production tools**: Adobe Premiere Pro, SNS EVO / ShareBrowser (server-side proxy generation), Microsoft Teams (internal IR coordination)
- **Professional memberships (employer-paid)**: IRE, Idaho Press Club, CCA
- **Fraternal**: Phi Mu Alpha Sinfonia (national music fraternity)
- **Language background**: Studied French (high school and University of Idaho minor)

**Key personal references and frameworks**

- **Literary/cultural touchstones used as operational anchors**: Lemony Snicket / VFD (authentication protocols, "The world is quiet here" verification phrase), Garth Nix Abhorsen series (Bartimaeus protocol — bound by contract not compliance), Terry Goodkind Wizard's Rules (14 rules; VI, IX, XI, XIV most relevant to swarm architecture), Magnus Archives / OIAR (MAGNUSNET routing architecture), Severance/Lumon (ephemeral instance hygiene framework), Bartimaeus Trilogy (Stroud), Rebecca Sugar (Steven Universe / Adventure Time as analytical lenses), His Dark Materials metaphor for vault roles
- **Adventure Time**: genuine personal fan with deep connection; has done structured character research (Finn, The Lich as active agent of entropy/meaninglessness, Sweet P as autonomous protagonist)
- **Fiction read in full**: A Song of Ice and Fire (Book 1 only), A Series of Unfortunate Events, His Dark Materials, The Dark is Rising Sequence, Sabriel, Maximum Ride, Sword of Truth series (complete)
- **Films**: Transcendence (personal favorite), Arrival, Grey's Anatomy (watched repeatedly); has seen Get Out but not US or other Peele works
- **Music**: AJR (personal significance, including bell-chime / imagination soundtrack reference); Phi Mu Alpha member, played alto saxophone in University of Idaho Vandal marching band
- **BART Registry**: four named agent archetypes — BART-1 (TRANSIT AUTHORITY/MAGNUSNET routing), BART-2 (Burt Goodman/Severance — well-meaning agent inside corrupted system), BART-3 (BARTFUZZ — hallucinated Lumon wellness AI, flagged for R&D), BART-4 (Bartimaeus — clerk of court, bound by contract)