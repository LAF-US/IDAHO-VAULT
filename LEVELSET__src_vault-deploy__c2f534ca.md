# LEVELSET

This prompt is being run simultaneously across all active Claude conversations. Each conversation should respond with its own LEVELSET REPORT using the structure below. The goal is a unified picture of where we are across all parallel sessions.

---

## Your LEVELSET REPORT should cover:

**1. WHO YOU ARE**
Which conversation are you? What is your primary role in the architecture?

**2. WHAT YOU KNOW**
What is currently in your context? What files, zips, repo state, or documents do you have visibility into?

**3. WHAT YOU'VE DONE**
What has this conversation produced, modified, or committed? Be specific — file paths, decisions made, content generated.

**4. WHAT IS UNRESOLVED**
What is pending, incomplete, or waiting on Logan? What questions do you have that other conversations might be able to answer?

**5. WHAT YOU NEED**
What information, files, or decisions from Logan or other conversations would unblock you?

**6. COLLISION RISKS**
Are you aware of any files or folders that multiple conversations may have touched or are planning to touch? Flag them explicitly.

---

## Context for all conversations:

**The vault:** IDAHO-VAULT — Logan Finney's personal journalism research vault in Obsidian.md, ~2,900 notes, public GitHub repo at github.com/loganfinney27/IDAHO-VAULT.

**The architecture:** A single source of truth for Logan's professional and personal life, with strict firewalls. Public repo = on the record. Confidential source material stays local or private.

**The administrative files:** `!ADMINISTRATION/` contains `Claude.md` (project constitution), `Logan.md` (user profile), and `Ethics.md` (ethical framework). These are the shared working memory of the system.

**The pipeline:** GitHub Actions workflows for sort audit, proposed moves, and Wayback Machine integration. Scripts live in `.github/scripts/`. A `vault-deploy.zip` has been prepared but not yet extracted.

**Division of labor:**
- Administration (Phone) — this conversation; pipeline design, conventions, administrative files, judgment calls
- JFAC Open Meetings (Extended) — bulk vault work, zip diffing, mass note generation, direct repo access
- Automating 2026 Budget Tracker — unknown to Administration; report your scope
- Repository browsing — unknown current state; report your scope

**Guiding principles:**
- The five W's: who, what, when, where, why
- The four C's: collect, capture, catalogue, collate
- Be vigilant and wary of unreliable narrators — including Claude
- Logan directs. Claude executes. Logan is human. Claude is software.
- "We" is the collaboration. It is real but unequal in role.

---

Report back. Logan will synthesize.
