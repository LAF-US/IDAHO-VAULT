---
title: "DRAFT Proposal - Controlled Intake Harbor for Unfinished Projects"
date created: 2026-04-17
authority: codex
doc_class: proposal
status: draft
related:
  - LAF-US
  - PRIVATE
  - LAF-PRIVATE
  - SECRET
  - PERSONAL
  - PUBLIC
  - PUBLISH
  - IDAHO-VAULT
  - THE-GEMSTONE
  - "!/AGENTS.md"
  - "!/LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md"
  - CONSTITUTION
---

# DRAFT Proposal - Controlled Intake Harbor for Unfinished Projects

*Filed 2026-04-17 for Logan's review. Draft only. Not live doctrine.*

## Summary

Logan is considering pulling unfinished projects, prototypes, and half-built
experiments inward for controlled review and parceling.

This proposal supports that move in principle, but with one crucial limit:

the non-public chamber should become an **intake harbor**, not a giant
undifferentiated junk drawer and not a permanent dumping ground for every
unfinished thing Logan has ever touched.

The goal is:

1. regain visibility
2. preserve provenance
3. classify unfinished work honestly
4. route each project toward the right chamber, child repo, archive, or death

## Canonical Baseline

Current canonical working interpretation from `!/AGENTS.md` and
`!/LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md`:

- `LAF-US` is the governing namespace.
- The repo-layer chamber anchors are:
  - `PRIVATE`
  - `SECRET`
  - `PERSONAL`
  - `PUBLIC`
  - `PUBLISH`
- Current flagship child repos explicitly named in that chambered model are:
  - `IDAHO-VAULT`
  - `THE-GEMSTONE`
- The team layer is separate and currently includes:
  - `LAF-PRIVATE`
  - `LAF-PUBLIC`
  - `LAF-USA`
  - `LAF-USB`
  - `LAF-USC`

That distinction matters here.

This draft uses the phrase **PRIVATE intake harbor** for the repo-layer target.
If Logan literally means a repository named `LAF-PRIVATE`, that should be
clarified explicitly, because the currently recorded canonical distinction is:

- `PRIVATE` = repo-layer chamber anchor
- `LAF-PRIVATE` = team-layer governance anchor

This proposal does not silently collapse those two.

## Proposal

Use the non-public chamber as a controlled intake harbor for unfinished
projects, prototypes, exports, abandoned codebases, loose folders, and
pre-repo artifacts that need review before they can be trusted, revived,
separated, or buried.

The harbor should do four jobs:

1. **inventory** what exists
2. **preserve** where it came from
3. **classify** what it is and how sensitive it is
4. **parcel** it toward the correct long-term home

The harbor should not be treated as:

- the permanent home of every unfinished project
- the one true monorepo of Logan's whole life
- a place where unrelated project histories are flattened together by default
- a place where imports gain legitimacy just because they have been copied inward

## Why This Fits The Five Cores

`IDAHO-VAULT` has functioned as an agentic workflow sandbox. That is useful,
but it is not the right permanent container for every prototype Logan has ever
made.

If the broader `LAF-US` order is chambered, then unfinished work needs a lawful
path inward before it can be sorted into:

- `SECRET`
- `PERSONAL`
- `PUBLIC`
- `PUBLISH`
- a flagship child repo
- an archive
- or abandonment

The intake harbor gives Logan a review chamber upstream of those choices.

That is especially useful while the system is still in beta and while cross-repo
and embedded-repo work is expected to grow.

## Intake Rule

Unfinished things may enter the harbor for review.

They do not become canonical by entering it.

Entry means:

- they are now visible
- they are now staged for judgment
- they now owe a manifest and a destination

It does not mean:

- they are active
- they are good
- they should stay together
- they belong in one shared worktree forever

## Intake Classes

Every inbound thing should be classified immediately as one of these:

### 1. Loose artifact drop

Examples:

- exported folder
- ZIP extraction
- scratch directory
- notes bundle
- partial prototype with no clear repo boundary

Default posture:

- allow import into the harbor
- preserve original folder name and source metadata
- do not pretend it already deserves repo dignity

### 2. Existing repo under review

Examples:

- dormant Git repo
- old side project
- forked prototype
- half-built tool with its own history

Default posture:

- preserve repo identity and origin
- do not flatten into a shared tree unless Logan explicitly chooses to
- prefer separate review record plus routing decision

### 3. Embedded-repo candidate

Examples:

- nested `.git` directory inside a broader folder
- project that may later live as a child repo or subtree
- bundle that contains multiple distinct project bodies

Default posture:

- mark the embedded boundary explicitly
- preserve the fact that this is not one seamless body
- require Logan review before flattening, absorbing, or splitting

## Intake Manifest

Every imported project or artifact group should receive a small manifest with at
least these fields:

- `intake_id`
- `source_name`
- `source_kind`
- `source_origin`
- `captured_on`
- `visibility_guess`
- `sensitivity`
- `chamber_guess`
- `history_present`
- `nested_repo_boundary`
- `current_state`
- `suggested_destination`
- `steward`
- `notes`

Suggested values:

- `source_kind`: `repo`, `folder-drop`, `export`, `archive`, `embedded-repo`
- `sensitivity`: `secret`, `personal`, `private-shared`, `public-candidate`, `unknown`
- `current_state`: `untriaged`, `under-review`, `incubating`, `parcel-ready`, `archive-only`, `superseded`, `abandoned`

The point is not bureaucracy for its own sake.

The point is to make sure every unfinished thing can answer:

- what is this
- where did it come from
- how sensitive is it
- who decides its fate
- where should it go next

## Routing Logic

Default routing from the harbor should look like this:

| Destination | Use when | Default action |
| --- | --- | --- |
| `SECRET` | high-sensitivity material, restricted operational knowledge, deeply private records | move inward fast; minimize surface area |
| `PERSONAL` | Logan-owned private work, journals, private experiments, unfinished personal systems | rehome as personal chamber material |
| `PRIVATE` | still under joint non-public review, not yet sorted, potentially shared internal tooling | keep incubating temporarily |
| `PUBLIC` | open-facing project work that is not yet publication-grade | extract and rehome once safe |
| `PUBLISH` | release-ready publication or distribution surface | promote only by explicit Logan decision |
| flagship child repo | work genuinely deserves its own continuing body | split cleanly and preserve identity |
| archive | historically worth keeping, not live | preserve without pretending it is active |
| abandonment | no value in continued maintenance | bury cleanly and record the ending |

## Boundary Rules

These should be treated as hard intake rules:

1. Do not discard history silently.
2. Do not flatten unrelated repos into one body by default.
3. Do not erase embedded repo boundaries just because they are inconvenient.
4. Do not let imports become canonical by survival alone.
5. Do not route anything outward into `PUBLIC` or `PUBLISH` without explicit Logan review.
6. Do not leave unfinished imports forever in a nameless holding pattern.

## Decision Rights

Agents may:

- inventory
- summarize
- diff
- detect boundaries
- suggest sensitivity
- suggest destination
- prepare manifests
- draft parceling plans

Agents may not, without Logan's explicit direction:

- flatten multiple repos into one
- discard commit history
- delete historically meaningful material
- promote harbor material into public or canonical surfaces
- treat a staging import as settled architecture

## Recommended First Pass

Do not start by dragging the whole graveyard inward at once.

Start with a narrow first wave:

1. choose 5 to 10 unfinished projects or prototypes
2. import them with manifests intact
3. classify each one as:
   - keep incubating
   - split to own repo
   - absorb into a chamber
   - archive
   - abandon
4. complete one full parceling cycle end to end
5. only then widen the harbor intake

This keeps the harbor from becoming another weather system before its rules are
proven.

## Specific Tension To Resolve

This proposal depends on one naming clarification that should be made explicit
before execution:

- Is the intended intake repo actually the repo-layer chamber anchor `PRIVATE`?
- Or is there now a live repository named `LAF-PRIVATE` that supersedes the
  migration note's wording?

Until that is clarified, the most faithful reading of the current canonical
surfaces is:

- `PRIVATE` is the repo-layer chamber anchor
- `LAF-PRIVATE` is the team-layer governance anchor

So the harbor concept is sound, but the exact target name still needs Logan's
confirmation.

## Recommendation

Adopt the harbor model.

Do not adopt the "one giant repo of all unfinished things" model.

The correct move is:

- inward review
- explicit manifests
- preserved provenance
- chamber-aware routing
- small-batch parceling

If this works, `LAF-US` gains a lawful intake chamber for unfinished work
without turning its non-public side into a blurrier second vault.
