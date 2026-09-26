# Current iCalendar and Calendaring Proposals

**Research snapshot:** 19 August 2026  
**Scope:** Concrete changes appearing in current CALEXT/JMAP work, plus explicitly flagged revival candidates.  
**Status rule:** An Internet-Draft is not an RFC. “Active,” “in working-group last call,” “RFC Editor queue,” and “expired” are materially different stages.

## Executive assessment

The most immediate **iCalendar field-level update** is the CALEXT working-group-last-call draft that aligns iCalendar with JSCalendar. It would add two properties, broaden `COLOR`, deprecate the legacy `GEO` property, and add a participation role. In parallel, the task-extension draft is near publication and makes `VTODO` suitable for structured assignment, planning, and status reporting. The other large current change is architectural rather than a new `.ics` field: JSCalendar 2.0, its iCalendar conversion specification, and JMAP Calendars are being advanced as an interoperable JSON-based companion stack.[1] [2] [3] [4]

The agenda from IETF 126 is especially important because it labels the series, participant-only iTIP, subscription-upgrade, and VPOLL proposals as **expired drafts for possible revival**, rather than current adopted work. They remain real design proposals, but they should not be represented as pending iCalendar updates.[5]

## Live or near-publication work

| Proposal | Current status | Specific proposed change | Practical significance |
|---|---|---|---|
| `draft-ietf-calext-icalendar-jscalendar-extensions-06` | **WG last call**; Standards Track intent | Deprecates `GEO`; adds `COORDINATES;VALUE=URI` in `VLOCATION`; adds `SHOW-WITHOUT-TIME`; adds `ROLE=OWNER`; permits CSS3 six-digit RGB values in `COLOR` as well as named colors. | This is the clearest pending update to the `.ics` element set. |
| `draft-ietf-calext-ical-tasks-17` | Listed at IETF 126 as **RFC Editor queue** | Extends `VTODO` with richer task relationships, planning, assignment, an `ESTIMATED-DURATION` property, and a `VSTATUS` component for detailed task status. It also defines CalDAV behavior for automated task management. | It turns VTODO from a personal-reminder model into a more credible project/process-management model. |
| `draft-ietf-calext-jscalendar-icalendar-25` | **WG last call**; Standards Track intent | Defines round-trip conversion for registered iCalendar and JSCalendar elements, including treatment for unmatched/unknown elements so lossless conversion remains possible. It specifies stable JSCalendar IDs sourced from iCalendar `JSID` data where present. | This is the bridge specification for systems that need both `.ics` and JSON representations. |
| `draft-ietf-calext-jscalendarbis-18` | **IESG evaluation** / Proposed Standard processing | Replaces JSCalendar RFC 8984 with version 2.0, improves iCalendar compatibility, clarifies floating local date-times, recurrence, validation, versioning, and extensibility. | It is not an iCalendar revision, but it drives the companion iCalendar additions and mappings. |
| JMAP Calendars | RFC Editor queue, blocked on JSCalendar 2.0 | Standard JSON API for calendar synchronization, server-side recurrence expansion, calendar sharing, participant identities, free/busy queries, and notifications. | A protocol modernisation path rather than a replacement for `.ics` publishing. |

### What the pending iCalendar-extension draft would change

The proposed `COORDINATES` property moves location geometry into RFC 5870 `geo:` URIs inside a `VLOCATION` component. The draft deprecates `GEO` because a URI-valued revision of `GEO` did not interoperate in existing implementations; legacy `GEO` may still be emitted as `DERIVED=TRUE` compatibility material. This is a deliberate migration pattern rather than a hard overnight removal.[1]

`SHOW-WITHOUT-TIME;VALUE=BOOLEAN:TRUE` is a presentation hint for a time-specific event or task that should visually behave like an all-day item, while keeping its time span relevant to availability calculations. The property must be omitted instead of set to false. The draft also adds an `OWNER` role for a participant that can alter the calendar object for the group, and expands `COLOR` from named CSS3 colours to include six-digit RGB hexadecimal values.[1]

> **Important for `cron_clock`:** This draft does **not** relax `DURATION` to accept calendar months or years. Its companion JSCalendar 2.0 duration grammar still covers weeks, days, hours, minutes, and seconds—not `P1M` or `P1Y`. Nor does it add a special recurrence concept for custom Gregorian era units.[1] [4]

## New but not adopted work

| Proposal | Status | What it proposes | How to read it |
|---|---|---|---|
| `draft-kashyap-calext-ical-property-deps-00` | Individual Internet-Draft; Informational intent | A machine-readable YAML/JSON dependency graph for VEVENT properties, including merge-safety categories and constraints such as `RRULE → DTSTART`, `EXDATE` type matching, recurrence-override links, and scheduling side effects. | Useful validation/sync tooling work. It defines no new iCalendar fields and has no IETF endorsement yet. |

The property-dependency draft is relevant to the issues encountered in this calendar project: it would make the relationships among `DTSTART`, `RRULE`, `DURATION`, `EXDATE`, `RDATE`, `RECURRENCE-ID`, and `VALARM` executable rather than prose-only. It is a proposal for safer editing and merge behaviour, not a new syntax vocabulary.[6]

## Explicit revival candidates, not active updates

| Expired draft | Proposed feature set | Current classification |
|---|---|---|
| iCalendar Series | `SRULE`, `SDATE`, `SXDATE`, `SERIES-UID`, `SERIES-ID`, `LAST-SERIES-ID`, look-ahead controls, and `RELTYPE=SERIES-MASTER` for a generated set of separately addressable instances. | A response to heavily modified recurrences; expired in 2021 and listed only for possible revival. |
| iTIP using PARTICIPANT only | Scheduling based on RFC 9073 `PARTICIPANT` components rather than `ATTENDEE`/`ORGANIZER`, with structured participant roles and reply/scheduling-state fields. | Expired in 2025; merely a revival candidate. |
| Calendar subscription upgrades | HTTP Link discovery for CalDAV/WebDAV/enhanced GET, incremental sync tokens, paging, and `STATUS:DELETED` tombstones. | Expired in 2025; merely a revival candidate. |
| VPOLL | A `VPOLL` component with alternatives, participant votes, poll completion modes, and new voting-related properties. | Expired in 2025; merely a revival candidate. |

The `Series` proposal is potentially the closest conceptual fit for calendars with large, individually meaningful generated units, but it has no current standards-track momentum. It should not be used in a public interoperability feed without a dual representation or a clearly private audience. The subscription-upgrade draft is relevant to a published `.ics` feed, but it should not cause a publisher to emit `STATUS:DELETED` or enhanced-GET headers until the work is reactivated and client support is demonstrated.[5] [7] [8] [9]

## What is *not* currently on the active CALEXT path

The August 2026 active agenda does not show a live proposal to standardize the Apple/Google/Microsoft `X-` property families wholesale, to make `X-WR-*` unnecessary in deployed clients, to legalize month/year durations, or to create native Gregorian “millennium/century/senary” recurrence units. Those remain either ecosystem-compatibility concerns or bespoke calendar modelling decisions.

The strongest current pattern is **not** “replace every legacy field.” It is to introduce narrowly scoped, interoperable primitives only when a clear data-model gap survives the existing RFCs and client evidence. The `GEO`/`COORDINATES` approach illustrates this: standardize a new field, retain a bounded compatibility path, and avoid assuming formal publication alone achieves de facto adoption.[1]

## Implications for `cron_clock`

| Question | Current answer |
|---|---|
| Can the palette move from CSS3 names to hex? | The active draft would permit it, but the existing named CSS3 palette is already standards-safe. There is no present need to change it. |
| Does any live work validate `P1Y`, `P100Y`, or `P3M` duration syntax? | No. Keep civil-unit spans expressed through recurrence/boundary modelling, not nonstandard `DURATION` tokens. |
| Does any live work add a standards analogue for the silent demon/grace intervals? | No. They remain a deliberate absence of VEVENT coverage, which is valid as a design convention but not expressed as an iCalendar primitive. |
| Should `X-WR-*` be stripped now? | No. The current proposals do not establish the demonstrated adoption required to retire legacy X-WR compatibility mirrors. |
| Should the feed implement subscription-upgrade proposals now? | No. The draft is expired; conventional HTTP validators and an ordinary `.ics` endpoint remain the interoperable baseline. |

## References

[1] [IETF, *iCalendar Format Extensions for JSCalendar*, draft-ietf-calext-icalendar-jscalendar-extensions-06](https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-jscalendar-extensions-06)

[2] [IETF, *Task Extensions to iCalendar*, draft-ietf-calext-ical-tasks-17](https://datatracker.ietf.org/doc/html/draft-ietf-calext-ical-tasks-17)

[3] [IETF, *JSCalendar: Converting from and to iCalendar*, draft-ietf-calext-jscalendar-icalendar-25](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendar-icalendar-25)

[4] [IETF, *JSCalendar 2.0*, draft-ietf-calext-jscalendarbis-18](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendarbis-18)

[5] [IETF, *JMAP/CALEXT Joint Session Agenda, IETF 126*](https://datatracker.ietf.org/doc/agenda-126-jmap/)

[6] [R. Kashyap, *Machine-Readable Property Dependencies for iCalendar*, draft-kashyap-calext-ical-property-deps-00](https://datatracker.ietf.org/doc/html/draft-kashyap-calext-ical-property-deps-00)

[7] [IETF, *Support for Series in iCalendar*, draft-ietf-calext-icalendar-series-03](https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-series-03)

[8] [IETF, *Calendar Subscription Upgrades*, draft-ietf-calext-subscription-upgrade-13](https://datatracker.ietf.org/doc/html/draft-ietf-calext-subscription-upgrade-13)

[9] [IETF, *VPOLL: Consensus Scheduling Component for iCalendar*, draft-ietf-calext-vpoll-07](https://datatracker.ietf.org/doc/html/draft-ietf-calext-vpoll-07)

[10] [IETF, *Calendaring Extensions Working Group Documents*](https://datatracker.ietf.org/group/calext/documents/)
