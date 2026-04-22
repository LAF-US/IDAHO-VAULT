---
authority: LOGAN
related:
  - '!/AGENTS'
  - '!/SIGNALS/README'
  - '!/SIGNALS/SIG-001-FROM-ABHORSEN-TO-VAULT-ADVISOR-RE-LAF44-EXHIBIT-A'
  - '!/INBOX/README'
  - '!/INBOX/AI-CAPTURES/README'
  - '!/INBOX/PHONE-LINK/phone-link-auto-sweep.ps1'
  - '!/__!__/! The world is quiet here/DOCKET'
date created: 2026-04-13
status: exploratory companion
---

# Signals and Inbox - Explorer Companion

This note accompanies the Nest's communication and intake surfaces: the durable
agent bus, the protocol face of intake, and the Janus split between swarm-facing
rules and Logan-facing file drops.

Primary surfaces observed in this passage:

- `!/SIGNALS/README.md`
- `!/SIGNALS/SIG-001-FROM-ABHORSEN-TO-VAULT-ADVISOR-RE-LAF44-EXHIBIT-A.md`
- `!/INBOX/README.md`
- `!/INBOX/AI-CAPTURES/README.md`
- `!/INBOX/PHONE-LINK/phone-link-auto-sweep.ps1`
- `!/__!__/! The world is quiet here/DOCKET.md`

## What These Surfaces Seem To Do

The Nest has more than one mouth.

Observed roles:

- `!/SIGNALS/` is the durable async bus for agent-to-agent speech; a signal is
  a committed, on-record message with sender, recipient, thread, and lifecycle
  status
- `DOCKET.md` reflects signal visibility, but it is not the signal channel
  itself; the courtroom sees open threads without becoming the archive of each
  exchange
- `!/INBOX/` is the protocol and automation face of intake, aimed at the swarm
- root `INBOX/` is the file-drop face of intake, aimed at Logan
- `AI-CAPTURES` exists to solve the "book-binding problem": chat insight that
  stays only in a web sandbox dies with the tab unless it is dropped into the
  vault
- `PHONE-LINK` automates one narrow physical intake path by sweeping files from
  a Windows downloads folder into the root inbox

## Direction Matters Here

These surfaces are easy to confuse because both deal in arrivals, but they move
different kinds of things.

- `SIGNALS` carries speech already inside the swarm
- `INBOX` carries material arriving from outside the swarm

One is inter-agent communication.

The other is world-to-vault intake.

Both are durable.
Both preserve provenance.
But they face different directions.

## The Janus Split

`!/INBOX/README.md` names the intake layer as JANUS structure, and that feels
exact.

- protocol face: `!/INBOX/{SOURCE}/`
- drop face: root `INBOX/{SOURCE}/`

That split keeps explanation near the automation while keeping the actual file
landing zone where Logan can use it directly.

## Field Note

If the Courtroom is where voices convene, then `SIGNALS` is where they write to
one another across distance, and `INBOX` is where the outside world knocks.

The house does not treat these as the same act.

To speak within the swarm is one thing.
To admit matter from beyond it is another.
