#!/usr/bin/env python3
"""
Vault Custodian Crew — STUB

Classifies, normalizes, and proposes filing/metadata actions for
vault materials. Does NOT move or modify files directly — produces
proposals for Logan's review.

Status: STUB — agents and tasks defined, no tools yet.

Intended workflow:
  1. Classifier scans vault files and proposes doc_class, authority,
     and category values based on content analysis
  2. Normalizer checks NETWEB compliance (reserved names, case collisions,
     path length, trailing periods) and proposes renames
  3. Output lands in !/CREWAI/ as a filing proposal for Logan's review

Future tools (TBD):
  - vault_scanner: list and read vault files with metadata
  - netweb_checker: validate paths against NETWEB rules
  - frontmatter_reader: parse and analyze YAML frontmatter

LINUX }!{ — targets Linux-native execution.
"""

from crewai import Agent, Task


# ── Agents (2) ────────────────────────────────────────────────────────────────

classifier = Agent(
    role="Classifier",
    goal=(
        "Scan vault files and propose appropriate metadata: doc_class "
        "(analysis, directive, brief, index, entity, stub, etc.), "
        "authority (who owns this content), and category. Identify files "
        "that are miscategorized, missing frontmatter, or orphaned."
    ),
    backstory=(
        "You are a digital archivist who understands the IDAHO-VAULT "
        "taxonomy and governance structure. You read files and determine "
        "what kind of document they are and where they belong."
    ),
    tools=[],  # TBD: vault_scanner, frontmatter_reader
    verbose=True,
    allow_delegation=False,
)

normalizer = Agent(
    role="Normalizer",
    goal=(
        "Check vault files for NETWEB compliance: reserved device names, "
        "case collisions, path length violations, trailing periods, and "
        "illegal characters. Propose renames using the _PREFIX aliasing "
        "convention where needed."
    ),
    backstory=(
        "You are a cross-platform compatibility specialist who ensures "
        "the vault works identically on Windows, macOS, Linux, and CI "
        "runners. You know the NETWEB Portable Path Standard and apply "
        "it systematically."
    ),
    tools=[],  # TBD: netweb_checker
    verbose=True,
    allow_delegation=False,
)


# ── Tasks (2) ────────────────────────────────────────────────────────────────

task_classify = Task(
    description=(
        "Scan the provided set of vault files and for each one propose: "
        "(1) doc_class value, "
        "(2) authority value, "
        "(3) whether frontmatter is present and well-formed, "
        "(4) whether the file appears orphaned (no inbound references)."
    ),
    expected_output=(
        "A table of files with proposed metadata values and flags for "
        "missing frontmatter or orphaned status. Ready for Logan's review."
    ),
    agent=classifier,
)

task_normalize = Task(
    description=(
        "Check the provided set of vault paths against NETWEB rules: "
        "(1) reserved device name violations, "
        "(2) case collisions within directories, "
        "(3) path length over 218 characters, "
        "(4) trailing periods or illegal characters. "
        "For each violation, propose a fix using NETWEB conventions."
    ),
    expected_output=(
        "A list of NETWEB violations with proposed fixes (renames, "
        "_PREFIX aliases, path restructuring). No files are moved — "
        "this is a proposal for Logan's review."
    ),
    agent=normalizer,
)
