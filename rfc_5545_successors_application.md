# RFC 5545 and Successors: Application to `cron_clock`

## Scope and Standard Set

This review uses the iCalendar base specification, RFC 5545, and the updates relevant to the properties present in your authoritative source. RFC 5546 confirms that `METHOD:PUBLISH` is the non-interactive publication method appropriate for a public reference calendar. RFC 7986 is essential here: it standardizes several calendar-level fields you deliberately use, including `NAME`, `UID`, `SOURCE`, `REFRESH-INTERVAL`, and `COLOR`.[1] [2]

| RFC | Applies? | Effect on this calendar |
|---|---|---|
| RFC 5545 | Yes | Governs content lines, VEVENT, DATE/DATE-TIME, DURATION, RRULE, UID, DTSTAMP, PRIORITY, TRANSP, RELATED-TO, METHOD, and `CALSCALE:GREGORIAN`. |
| RFC 5546 | Yes | Confirms `METHOD:PUBLISH` as a publication, rather than interactive scheduling, method. |
| RFC 6868 | Not materially | Its `^` escaping applies to parameter values; no source parameter requires it. |
| RFC 7529 | No | It adds `RSCALE` for non-Gregorian recurrence. Your source remains correctly Gregorian and should not add `RSCALE`. |
| RFC 7953 | No | Adds availability components that are absent from this calendar. |
| RFC 7986 | Yes | Makes the calendar-level metadata in your source standard, subject to exact value-type syntax. |
| RFC 9073 | No | Adds event-publishing components/properties absent from this source. |
| RFC 9074 | No | Applies only to VALARM extensions; your source has no alarms. |
| RFC 9253 | Conditionally | Extends `RELATED-TO` semantics, but only once relationship values are actually populated. |

## Correct in the Authoritative Design

The source correctly uses `CALSCALE:GREGORIAN` for the calendar scale. The use of all-day `DATE` values for civil boundary events, bare local `DATE-TIME` values for the phase and named rhythm events, valid day/week and fixed-hour/minute durations, transparent events, published method, priority levels, CSS color names, and RFC 7986 calendar-level identity/presentation fields is consistent with the standards framework.[1] [2]

`METHOD:PUBLISH` does **not** require attendee negotiation: RFC 5546 defines it as a non-interactive publishing method, matching the source’s reference-calendar purpose.[2]

## Required Source-Preserving Repairs

The following are standard conformance changes, not redesigns.

| Source field | RFC requirement | Source-preserving repair |
|---|---|---|
| VCALENDAR `DTSTAMP:20270101Z` | `DTSTAMP` is not a VCALENDAR property. RFC 7986 permits `LAST-MODIFIED` at VCALENDAR level; DATE-TIME requires full date and time. | Replace with `LAST-MODIFIED:20270101T000000Z`. |
| VEVENT `DTSTAMP:20270101Z` | VEVENT `DTSTAMP` is required and must be a UTC DATE-TIME. | Replace each with `DTSTAMP:20270101T000000Z`. |
| `REFRESH-INTERVAL:P3M` | RFC 7986 requires `VALUE=DURATION`; RFC 5545 duration excludes months (`M` is permitted only after `T`, for minutes). | Replace with `REFRESH-INTERVAL;VALUE=DURATION:<confirmed fixed duration>`. |
| `SOURCE:https://…` | RFC 7986 defines SOURCE as URI with no default type. | Preserve the URL and add `;VALUE=URI`. |
| `INTERVAL:30`, `INTERVAL:20`, `INTERVAL:12` | RRULE parts use `NAME=VALUE`. | Change only `:` to `=`. |
| Repeated `UID:dozen-vault_time@cron_clock` | Each independent VEVENT must have a persistent globally unique UID. | Use three distinct UID values for Half, Score, and Dozen while retaining every other property. |
| LF/new trailing blank | iCalendar content lines are CRLF-delimited and an object ends with `END:VCALENDAR` followed by CRLF. | Serialize exactly with CRLF and no extra blank content line. |

## Items That Need a Rule, Not a Guess

### Refresh interval

`P3M` cannot represent “three months” in an RFC 5545 DURATION: calendar months are intentionally excluded from iCalendar durations because they do not have a fixed length. The replacement must be a **fixed** duration such as `P90D`, `P13W`, or another explicit day/week/clock duration you choose. RFC 7986 additionally requires the `VALUE=DURATION` parameter.[1] [3]

### Relationship placeholders

The empty `RELATED-TO:` values are syntactically possible text values but do not identify another component and therefore do not form a meaningful relationship. RFC 9253 can enrich relationships once you decide the hierarchy: it provides `RELTYPE` values such as `PARENT`, `CHILD`, `SIBLING`, `FIRST`, and `NEXT`.[4] The conservative repair is to preserve them as placeholders; the interoperable repair is to populate them using the event UIDs and a declared relationship direction.

### Sub-day recurrence anchors

The generic Hour, Half, Score, Dozen, Minute, and Second layers use a DATE-only `DTSTART` alongside hourly/minutely/secondly frequencies. The RFC does not explicitly prohibit that `FREQ`/DATE combination, but it supplies no time-of-day seed. For portable, unambiguous sub-day expansion, the eventual semantic repair should give those events a floating DATE-TIME anchor, such as `DTSTART:18100101T000000`. This is an **interoperability clarification**, not an unambiguous mechanical alteration, so it should wait for your rule.

## Standards-Grounded Repair Baseline

A faithful reconstruction should therefore retain all **52 VEVENTs**, the millennium/senary/quarter/month/week/day/phase/rhythm hierarchy, epoch dates, labels, colors, categories, priorities, and transparent publication model. It should alter only the seven mechanical classes above after you select the fixed refresh duration and the three stable UID names for Half, Score, and Dozen.

## References

[1]: https://www.rfc-editor.org/rfc/rfc5545.html "RFC 5545: Internet Calendaring and Scheduling Core Object Specification"
[2]: https://www.rfc-editor.org/rfc/rfc5546.html "RFC 5546: iCalendar Transport-Independent Interoperability Protocol"
[3]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[4]: https://www.rfc-editor.org/rfc/rfc9253.html "RFC 9253: Support for iCalendar Relationships"
[5]: https://www.rfc-editor.org/rfc/rfc6868.html "RFC 6868: Parameter Value Encoding in iCalendar and vCard"
[6]: https://www.rfc-editor.org/rfc/rfc7529.html "RFC 7529: Non-Gregorian Recurrence Rules in iCalendar"
[7]: https://www.rfc-editor.org/rfc/rfc7953.html "RFC 7953: Calendar Availability"
[8]: https://www.rfc-editor.org/rfc/rfc9073.html "RFC 9073: Event Publishing Extensions to iCalendar"
[9]: https://www.rfc-editor.org/rfc/rfc9074.html "RFC 9074: VALARM Extensions for iCalendar"
