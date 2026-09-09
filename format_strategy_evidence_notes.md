# Format Strategy Evidence Notes

## Current deployment evidence

Stalwart reported in October 2025 that it was the first complete JMAP server to support the new calendaring protocols; it described client support as still emerging and named Mailtemi and OpenCloud as projects developing clients. This supports JSCalendar/JMAP as a viable controlled-stack or early-adopter choice, but not as a drop-in replacement for the installed public calendar-client ecosystem.

Microsoft’s Exchange iCalendar conversion specification documents `X-WR-CALNAME` as an import/export property for calendar exports, with a direct mapping to the calendar folder display name. This is current published Microsoft interoperability documentation, even though the field has no RFC reference.

The Python `icalendar` project’s 2025/26 issue and merged release note a request for dual `NAME` and `X-WR-CALNAME` output based on a maintainer-reported Google Calendar compatibility constraint. This is ecosystem evidence rather than official Google documentation, so it supports a conservative dual-emission strategy but not a universal compatibility claim.

Sources:

* https://stalw.art/blog/jmap-collaboration/
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1da58449-b97e-46bd-b018-a1ce576f3e6d
* https://github.com/collective/icalendar/issues/918
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendarbis-18
* https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendar-icalendar-25
