# Current CALEXT Proposal Notes — August 2026

## Current Work-Item Status

The CALEXT documents page and IETF 126 joint CALEXT/JMAP agenda identify the current landscape:

* `draft-ietf-calext-icalendar-jscalendar-extensions-06` is in working-group last call.
* `draft-ietf-calext-jscalendar-icalendar-25` is in working-group last call and defines conversion rules.
* `draft-ietf-calext-jscalendarbis-18` is in IESG evaluation / Proposed Standard processing and would obsolete RFC 8984.
* `draft-ietf-calext-ical-tasks-17` was listed at IETF 126 as in the RFC Editor queue.
* The agenda explicitly listed expired drafts on series, iTIP participants, subscription upgrade, and VPOLL for possible revival—not as active approved work.
* `draft-kashyap-calext-ical-property-deps-00` was presented as new work.

## Concrete iCalendar Changes in draft-ietf-calext-icalendar-jscalendar-extensions-06

This draft updates RFCs 5545, 7986, and 9073. It proposes to deprecate `GEO`, introduce `COORDINATES;VALUE=URI` in `VLOCATION` using the `geo:` URI scheme, and allow the old GEO only as `DERIVED=TRUE` compatibility data. It expands `COLOR` from CSS3 names to also allow six-digit CSS3 RGB hexadecimal values. It adds `SHOW-WITHOUT-TIME;VALUE=BOOLEAN:TRUE` for date-time events/tasks whose exact times should not dominate presentation while remaining relevant to free-busy logic. It introduces the `OWNER` attendee role.

## Other Draft Directions

`draft-ietf-calext-ical-tasks-17` would substantially extend VTODO: explicit task typing/context, relationships, estimated duration, improved planning/deadline semantics, scheduling/assignment, and a `VSTATUS` component for richer status reporting. It also contains CalDAV behavior for automated task management.

`draft-ietf-calext-jscalendar-icalendar-25` aims to map every registered iCalendar and JSCalendar element and preserve unmatched elements through conversion-specific containers. `draft-ietf-calext-jscalendarbis-18` would replace JSCalendar RFC 8984 with a more iCalendar-compatible version 2.0 and explicitly retains floating local date-time semantics.

Sources:

* https://datatracker.ietf.org/group/calext/documents/
* https://datatracker.ietf.org/doc/agenda-126-jmap/
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-jscalendar-extensions-06
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-ical-tasks-17
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendar-icalendar-25
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendarbis-18

## New Work and Revival Candidates

`draft-kashyap-calext-ical-property-deps-00` is an individual, Informational proposal—not a CALEXT adopted work item. It defines a machine-readable VEVENT dependency graph (YAML/JSON) for 27 properties, 20 dependency edges, and merge-safety classifications. Its purpose is to let CalDAV implementations safely identify conflicts in concurrent property-level edits; it introduces no new iCalendar elements or IANA actions.

The IETF 126 agenda listed several expired drafts only for a possible revival discussion. Their proposals should not be described as current standards work:

* `draft-ietf-calext-icalendar-series-03` proposes a distinct repeating-series model in which generated members have unique UIDs and relate to a series master via `SERIES-UID`, `SERIES-ID`, `SRULE`, `SDATE`, `SXDATE`, `LAST-SERIES-ID`, and `RELTYPE=SERIES-MASTER`. It addresses heavily customized recurring events but expired in 2021.
* `draft-ietf-calext-itip-participants-00` proposes iTIP scheduling centered on RFC 9073 PARTICIPANT components rather than legacy ATTENDEE/ORGANIZER fields. It adds `REPLY-URL`, `KIND`, `PARTICIPATION-STATUS`, delegation, `MEMBER-OF`, `EXPECT-REPLY`, and scheduling state fields. It expired in 2025.
* `draft-ietf-calext-subscription-upgrade-13` proposes an upgrade path from polling `.ics` feeds via HTTP Link relations to CalDAV/WebDAV/enhanced GET; it adds `STATUS:DELETED`, Sync-Token use, `subscribe-enhanced-get` and `limit` HTTP preferences, and subscription relation types. It expired in 2025.

Sources:

* https://datatracker.ietf.org/doc/html/draft-kashyap-calext-ical-property-deps-00
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-series-03
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-itip-participants-00
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-subscription-upgrade-13

## Further Proposal Details

`draft-ietf-calext-vpoll-07` is expired but was explicitly listed as a revival candidate at IETF 126. It defines a VPOLL component for consensus scheduling across alternative events/tasks, participant voting, VOTE components, POLL-MODE, POLL-COMPLETION, POLL-ITEM-ID, POLL-PROPERTIES, and new iTIP STATUS/REQUEST behavior. It is exploratory until a new revision or formal revival occurs.

The current JMAP calendar work is relevant to future calendaring, but it is not a new iCalendar field specification. It defines server synchronization, sharing, push notifications, participant identities, recurrence expansion, free-busy queries, and multi-calendar event membership using JSCalendar Event representations. IETF 126 identified it as RFC Editor queue work blocked on the JSCalendar 2.0 document.

Sources:

* https://datatracker.ietf.org/doc/html/draft-ietf-calext-vpoll-07
* https://datatracker.ietf.org/doc/html/draft-ietf-jmap-calendars-26
