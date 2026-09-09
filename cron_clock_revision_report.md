# cron_clock iCalendar Revision Report

**Prepared by:** Manus AI  
**Scope:** Gregorian iCalendar recurrence file refined to preserve the supplied calendar’s intended event inventory while using **floating local time** for every date-time event.

## Result

The corrected file is `cron_clock_gregorian_floating.ics`. It contains **35 unique VEVENT components** and uses `CALSCALE:GREGORIAN`. The Gregorian calendar scale is the RFC 5545 default, but retaining it as an explicit calendar-level declaration makes the intended scale unmistakable; it is not an `RRULE` value.[1]

> A floating `DATE-TIME` is written without a `TZID` parameter and without a trailing `Z`. It therefore preserves the same wall-clock time wherever the calendar is viewed, which is the behavior requested for this file.[2]

| Area | Revision | Rationale |
|---|---|---|
| Calendar syntax | Removed the orphaned `X-` line. | Every content line requires a valid name, and an experimental `X-` property requires a nonempty suffix.[3] |
| Gregorian recurrence | Retained `CALSCALE:GREGORIAN`; made yearly marker rules explicit with `BYMONTH` and `BYMONTHDAY`. | The occurrence set remains the same while the annual intent is clear and synchronized with each `DTSTART`.[1] [4] |
| Week and weekday markers | Added the exact weekday selector (`BYDAY`) and explicit Monday week start (`WKST=MO`) to the weekly rules. | This makes the calendar’s civil-week convention explicit and keeps each recurrence aligned with its initial date.[4] |
| Floating event times | Replaced all ten `DTSTART;TZID=America/Boise:…` values with bare local `DTSTART:…` values. | Bare local `DATE-TIME` values are floating time under RFC 5545; `TZID` would create a zone-bound event.[2] |
| All-day events | Retained `VALUE=DATE` for years, quarters, months, weeks, and weekdays, with only day/week durations. | Date-valued VEVENTs may use day- or week-based durations; a date-only event lacking a duration is one day long.[5] |
| File transport | Normalized content lines to CRLF and confirmed each line is no more than 75 octets. | RFC 5545 defines CRLF-delimited content lines and recommends folding lines longer than 75 octets.[3] |
| Metadata timestamps | Kept `DTSTAMP` values in UTC (`Z`). | `DTSTAMP` is revision metadata, not event scheduling time, and RFC 5545 requires UTC for it.[6] |

## Validation Performed

The revised file was parsed with the maintained [`collective/icalendar`](https://github.com/collective/icalendar) library and checked for valid calendar structure, 35 VEVENTs, unique UIDs, `CALSCALE:GREGORIAN`, absence of `TZID` on all event `DTSTART` values, floating date-time semantics, all-day duration form, initial `DTSTART`/RRULE synchronization, CRLF line endings, absence of the malformed extension, and the 75-octet line limit. All checks passed.

## Intentional Semantics

The **Year**, **Quarter**, **Month**, **Week**, and **Day** markers are all-day transparent events. **Dawn**, **Noon**, **Dusk**, and the seven named minute segments are transparent, recurring, floating local-time events. The `DTSTAMP` values still end in `Z` by design: that UTC indicator concerns the record’s revision timestamp only, and does not time-zone-bind an event’s `DTSTART`.[2] [6]

## References

[1]: https://icalendar.org/iCalendar-RFC-5545/3-7-1-calendar-scale.html "RFC 5545 §3.7.1: Calendar Scale"
[2]: https://icalendar.org/iCalendar-RFC-5545/3-3-5-date-time.html "RFC 5545 §3.3.5: Date-Time"
[3]: https://icalendar.org/iCalendar-RFC-5545/3-1-content-lines.html "RFC 5545 §3.1: Content Lines"
[4]: https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html "RFC 5545 §3.8.5.3: Recurrence Rule"
[5]: https://icalendar.org/iCalendar-RFC-5545/3-6-1-event-component.html "RFC 5545 §3.6.1: Event Component"
[6]: https://icalendar.org/iCalendar-RFC-5545/3-8-7-2-date-time-stamp.html "RFC 5545 §3.8.7.2: Date-Time Stamp"
