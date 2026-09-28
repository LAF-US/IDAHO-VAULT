# RFC Standards Findings for `cron_clock`

## Base Specification: RFC 5545

RFC 5545 defines the iCalendar base format. It requires CRLF-delimited content lines, uses a complete DATE-TIME format (`YYYYMMDDTHHMMSS`) with `Z` for UTC, defines RRULE parts as `NAME=VALUE`, and specifies that VEVENT `DTSTAMP` values are UTC. It also defines the ordinary Gregorian date, duration, recurrence, `RELATED-TO`, `UID`, `PRIORITY`, and `TRANSP` behavior used by the calendar.[1]

## Applicable Updates

| RFC | Relevance to this calendar | Finding |
|---|---|---|
| RFC 6868 | Parameter-value escaping | No submitted parameter needs its `^` escape syntax. |
| RFC 7529 | Non-Gregorian recurrence | Not needed: the source correctly uses `CALSCALE:GREGORIAN` and does not use `RSCALE`. |
| RFC 7986 | Calendar-level properties | `NAME`, VCALENDAR `UID`, `SOURCE`, `REFRESH-INTERVAL`, and `COLOR` are standard extensions. `REFRESH-INTERVAL` requires `VALUE=DURATION`, and `SOURCE` should declare `VALUE=URI` for backward-compatible type handling.[2] |
| RFC 7953 | Availability components | Not applicable: no `VAVAILABILITY` or `AVAILABLE` component is present. |
| RFC 9073 | Event publishing extensions | Not applicable to the submitted property set; it adds structured publishing components and metadata. |
| RFC 9074 | VALARM extensions | Not applicable: no `VALARM` component is present. |
| RFC 9253 | Calendar relationships | Relevant only if populated `RELATED-TO` fields will model event relationships. It extends relationship types but does not make empty `RELATED-TO` values meaningful. |

## Source-Faithful Mechanical Repairs Derived from the RFCs

1. Serialize with CRLF and remove the trailing blank line.
2. Replace the VCALENDAR-level `DTSTAMP` with `LAST-MODIFIED:20270101T000000Z` if the intended meaning is calendar revision time; RFC 7986 permits `LAST-MODIFIED` at VCALENDAR level.
3. Change every VEVENT `DTSTAMP:20270101Z` to `DTSTAMP:20270101T000000Z`.
4. Use `REFRESH-INTERVAL;VALUE=DURATION:` and specify a legal RFC 5545 duration. `P3M` is not legal because iCalendar duration omits calendar months. A policy decision is needed before choosing the replacement duration.
5. Use `SOURCE;VALUE=URI:` for the GitHub URL.
6. Change the three `INTERVAL:` tokens to `INTERVAL=`.
7. Give Half, Score, and Dozen distinct UID values; three independent VEVENT masters cannot share the same UID.
8. Preserve your authored calendar hierarchy, labels, categories, priorities, colors, anchor dates, and placeholder properties unless separately directed.

## References

[1]: https://www.rfc-editor.org/rfc/rfc5545.html "RFC 5545: Internet Calendaring and Scheduling Core Object Specification"
[2]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[3]: https://www.rfc-editor.org/rfc/rfc6868.html "RFC 6868: Parameter Value Encoding in iCalendar and vCard"
[4]: https://www.rfc-editor.org/rfc/rfc7529.html "RFC 7529: Non-Gregorian Recurrence Rules in iCalendar"
[5]: https://www.rfc-editor.org/rfc/rfc7953.html "RFC 7953: Calendar Availability"
[6]: https://www.rfc-editor.org/rfc/rfc9073.html "RFC 9073: Event Publishing Extensions to iCalendar"
[7]: https://www.rfc-editor.org/rfc/rfc9074.html "RFC 9074: VALARM Extensions for iCalendar"
[8]: https://www.rfc-editor.org/rfc/rfc9253.html "RFC 9253: Support for iCalendar Relationships"
