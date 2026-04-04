#!/usr/bin/env python3
"""
Task-to-Code Bridge Crew — STUB

Converts scoped work items (Linear issues, GitHub Issues) into
implementation plans or code tasks.

Status: STUB — agents and tasks defined, no tools yet.

Intended workflow:
  1. Task Analyst reads a work item (title, description, labels, context)
  2. Plan Drafter generates an implementation plan:
     - Files to create/modify
     - Steps in execution order
     - Verification criteria
  3. Output lands in !/CREWAI/ as a plan brief for Logan's review

Future tools (TBD):
  - linear_reader: fetch issue details from Linear API
  - github_issue_reader: fetch issue details from GitHub API
  - codebase_scanner: read file structure and symbol overview

LINUX }!{ — targets Linux-native execution.
"""

from crewai import Agent, Task


# ── Agents (2) ────────────────────────────────────────────────────────────────

task_analyst = Agent(
    role="Task Analyst",
    goal=(
        "Read a scoped work item and extract the requirements, constraints, "
        "acceptance criteria, and any referenced files or prior work. Produce "
        "a structured requirements summary."
    ),
    backstory=(
        "You are a technical project manager who reads issue descriptions "
        "and extracts actionable requirements. You identify what needs to "
        "change, what constraints apply, and what 'done' looks like."
    ),
    tools=[],  # TBD: linear_reader, github_issue_reader
    verbose=True,
    allow_delegation=False,
)

plan_drafter = Agent(
    role="Plan Drafter",
    goal=(
        "Given a requirements summary, generate a concrete implementation "
        "plan listing files to create or modify, steps in execution order, "
        "and verification criteria. The plan should be actionable by a "
        "coding agent (Claude Code, Codex, Copilot)."
    ),
    backstory=(
        "You are a software architect who translates requirements into "
        "step-by-step implementation plans. You know the IDAHO-VAULT "
        "repository structure and can specify exact file paths and changes."
    ),
    tools=[],  # TBD: codebase_scanner
    verbose=True,
    allow_delegation=False,
)


# ── Tasks (2) ────────────────────────────────────────────────────────────────

task_extract = Task(
    description=(
        "Read the provided work item and extract: "
        "(1) what needs to be done, "
        "(2) what constraints or dependencies exist, "
        "(3) what acceptance criteria define 'done', "
        "(4) any referenced files, PRs, or prior work."
    ),
    expected_output=(
        "A structured requirements summary with sections for: scope, "
        "constraints, acceptance criteria, and references."
    ),
    agent=task_analyst,
)

task_plan = Task(
    description=(
        "Given the requirements summary, produce an implementation plan: "
        "(1) files to create or modify (with paths), "
        "(2) steps in execution order, "
        "(3) verification criteria (how to confirm each step worked), "
        "(4) estimated complexity (trivial/moderate/complex)."
    ),
    expected_output=(
        "A step-by-step implementation plan in markdown format, ready "
        "for a coding agent to execute. Each step specifies the file, "
        "the change, and how to verify it."
    ),
    agent=plan_drafter,
)
