<!-- Copied from the original claude.ai project during the upgrade. Delete this line if you edit this file. If the upgrade is retried, it replaces files that still carry this line. -->

---
name: overview
description: IDAHO-VAULT project purpose, Logan's role and colleagues at Idaho Reports, vault architecture, and current state of the multi-agent swarm build
sources: [backfill]
aliases: [IDAHO-VAULT, Building God, swarm, Logan Finney]
---

## Who and where

- [stated] Logan Finney is a journalist, producer, and reporter at Idaho Reports (Idaho Public Television / IdahoPTV)
- [stated] Covers Idaho state government broadly — JFAC budgets, Medicaid, elections, courts, criminal justice, public lands, transportation, library law, Idaho GOP politics
- [stated] Hosts the Idaho Reports podcast and fills in as on-air host
- [stated] University of Idaho journalism graduate (2020, B.S. Broadcasting and Digital Media)
- [stated] North Idaho native
- [stated] Standing member of the Capitol Correspondents Association (CCA) and Idaho Press Club
- [stated] Has freelanced for FāVS News; holds early bylines at rural Idaho print outlets
- [stated] Studied French (University of Idaho minor)
- [stated] Member of Phi Mu Alpha Sinfonia (national music fraternity); played alto saxophone in the University of Idaho Vandal marching band
- [stated] Personal site: loganfinney.com

## Colleagues

- [stated] Melissa Davlin — lead producer, CCA standing committee
- [stated] Adam McCoy — director/editor
- [stated] Kevin Richert — CCA president, Idaho Education News
- [stated] Clark Corbin — Idaho Capital Sun, primary JFAC reporter

## Editorial constraint

- [stated] Logan operates under editorial constraints stemming from IdahoPTV's status as a state agency under the Idaho State Board of Education — this limits how directly he can own certain accountability stories (e.g. JFAC transparency, where Corbin takes primary)

## Project purpose

- [stated] IDAHO-VAULT is Logan's central long-term project: an Obsidian-based personal knowledge management system (~2,900 notes) hosted publicly at github.com/loganfinney27/IDAHO-VAULT
- [stated] The vault serves as extended memory, source-of-truth archive, and infrastructure backbone for a multi-agent AI coordination system he calls a "swarm"
- [stated] Works across Claude, GitHub Copilot, Gemini, Grok, M365 Copilot, and NotebookLM
- [stated] Overarching philosophical framework is called "Building God" — a post-religious, functional architecture for collective meaning-making, synthesizing AI agent design (Krishnan), secular god-building concepts (Lunacharsky), and Orthodox theology
- [stated] Frames the system as "Augmenting Intelligence," not Artificial Intelligence — extending his cognition, not replacing his judgment

## Current state — swarm architecture

- [stated] Canonical admin folder: `!/` with `!/CONSTITUTION.md` (adopted 2026-03-16, revised 2026-03-18)
- [stated] Nine framework stubs awaiting content: CHARTER, CODEX, PROTOCOLS, PROCEDURES, PREFERENCES, GUIDELINES, GUESTBOOK, GRIMOIRE, and a `!/!` system subfolder
- [stated] An unresolved "Fifth C" in a capture/collect/collate/catalogue framework
- [stated] Active coordination protocols: LEVELSET (v3.2.6.1), PASSBACKS (typed handshake relay system), ORIENTATE (for repo-less instances), CLOSURE
- [stated] Logan serves as manual bridge between agents — Slack bot apps for Copilot/Gemini not yet configured; Slack free trial was set to expire April 13
- [stated] Active swarm nodes referenced: PERSISTENT: ADMINISTRATION, PERMANENT: AUTHORITY: CODE (Tier 1, direct repo write), GitHub Copilot, Gemini, Grok
- [stated] Claude instances self-assess tier (1–3) based on repo access

## Current state — broken pipelines and infrastructure findings

- [stated] A Daily To-Do Rollover GitHub Actions workflow failed in late April; the signal chain from vault → GitHub → Janitor Sweep → Linear → Slack is broken between the Janitor Sweep and Linear layers
- [stated] Linear has been silent, though issue tracking has advanced (LAF-48 as of the most recent session)
- [stated] LAF-34 documents CrewAI deployment as the next execution surface, with PR #208 as a threshold
- [stated] Atlassian site (idaho-vault.atlassian.net) has Jira read/write scope active but no Confluence scope — a new discovery
- [stated] Box is enrolled but empty
- [stated] Granola is listed as a connector but no account was created
- [stated] Active MCP connectors include Linear, Slack, and others, with several gated behind incomplete approval flows (Asana, Spotify, Calendly, Atlassian Rovo, etc.)
- [stated] GitHub MCP does not exist in Anthropic's connector directory — a structural absence confirmed in the most recent session

## Current state — Idaho Reports work in motion

- [stated] An Idaho Reports Data Center Power Package was being finalized, with Melissa on notes/review, Adam on revisions, and Logan handling TRACKERS work and podcast editorial (cutting interviews into POV vignettes targeting Wednesday release)

## On the horizon

- [stated] Resolving the broken swarm signal chain (vault → GitHub Actions → Linear → Slack)
- [stated] CrewAI deployment (LAF-34, PR #208 threshold)
- [stated] Constitution.md V2: must explicitly encode that Logan's authority exists prior to and outside the swarm; needs agent succession/failover rules; should hardcode Wizard's Rules (14 rules from Terry Goodkind's Sword of Truth) by reference
- [stated] Formalizing AGENTS.md v0.2
- [stated] Completing the nine framework stubs in `!/`
- [stated] Resolving the "Fifth C" in the cataloguing framework
- [stated] Slack bot app provisioning for Copilot and Gemini (enabling automated inter-agent coordination)
- [stated] Bitchat BT (Jack Dorsey's Bluetooth mesh app) flagged as a potential swarm coordination vector for internet-independent environments
- [stated] MAGNUSNET / PROTOCOL: MAGNUS (mesh routing layer modeled on OIAR architecture from Magnus Archives) — conceptually defined, spec work pending canonical hydration
- [stated] GOLEMSWARM (GitHub Actions as automated swarm heartbeat — needs sunset conditions defined)
- [stated] LSO data firehose access (contact named Bybee) as alternative to scraping the legislative site for the budget tracker pipeline
- [stated] CourtListener scraper reactivation once automated pipeline architecture is functional
- [stated] Period tracker / mood journaling app analysis for potential swarm integration
- [stated] Personal media consumption tracker (Letterboxd RSS, TMDb, Open Library, OpenAlex, Crossref stack — Part A personal, Part B institutional/Idaho Reports)
- [stated] Idaho opioid settlement expenditure tracking using KFF/Johns Hopkins methodology