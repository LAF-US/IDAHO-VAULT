# `cron_clock` Pre-Repair Expectations Review

**Status:** No calendar content has been changed. This document separates the **intended clock model** from the syntax repairs that will be made only after confirmation.

## Working Interpretation

The submitted calendar reads most coherently as a **transparent civil-time reference overlay**, not an appointment or availability calendar. Its events are intended to mark the boundaries of a nested Gregorian hierarchy: century, decade, year, quarter, month, week, day, hour, minute, and second. `TRANSP:TRANSPARENT` supports this interpretation because it prevents the events from reserving free/busy time.[1]

> The key design decision is whether each event is a **boundary marker**—a point or all-day label placed at the start of a unit—or a **visual band** that spans the unit. The submitted file currently mixes these models: week and day use durations, while year/month/quarter markers do not.

## Expectations That Appear Clear

| Aspect | Inferred expectation | Why it appears intentional |
|---|---|---|
| Calendar system | The standard Gregorian civil calendar. | `CALSCALE:GREGORIAN` is explicit and belongs at VCALENDAR level.[2] |
| Publication behavior | A published, read-only reference feed rather than an invitation workflow. | `METHOD:PUBLISH` and transparent events support this. |
| Event timing | Floating local time for sub-day entries. | You explicitly specified no time zone; a bare local `DATE-TIME` is floating under RFC 5545.[3] |
| Layering | One event family for each scale, from century to seconds. | The hand edit adds generic month/day/hour/minute/second layers alongside the named layers. |
| Week alignment | Monday is the intended first day of the week. | `1810-01-01` is a Monday, and the calendar’s generic week and Monday markers use that origin. |
| Persistence | The calendar is meant to recur without a natural end date. | No `UNTIL` or `COUNT` rules are present. An RRULE with neither repeats indefinitely.[4] |

## Expectations Requiring Your Decision

### 1. Boundary markers or full-period bands

A marker model is technically simple and scales well: Year, Month, and Quarter appear only on their first day, while week/day can remain day- or week-long bands. A full-period-band model is visually richer but cannot be represented with one uniform duration for calendar months, quarters, or years because their lengths vary.

| Option | Meaning | Recommended representation |
|---|---|---|
| **A. Boundary markers** | Each scale announces that a new unit has begun. | Use one-day all-day events for civil boundaries and instantaneous floating events for hour/minute/second ticks. |
| **B. Full-period bands where feasible** | Week/day/hour/minute/second visibly cover their whole unit; calendar-scale layers remain boundary markers. | Add durations to fixed-length units only: `P1W`, `P1D`, `PT1H`, `PT1M`, `PT1S`. |
| **C. Full-period bands at every scale** | Month/quarter/year should also appear as spans. | Requires generated individual instances or a richer system than a single ordinary RRULE; it is not a simple recurring iCalendar pattern. |

**Recommended expectation:** **B**. It preserves the visual clock concept without pretending that a month or year has a fixed duration.

### 2. Canonical epoch and historic scope

The submitted generic hierarchy begins in **1810**, while several retained weekday and sub-day events still begin in **2026**. Both are valid; the difference is semantic.

| Option | Meaning | Consequence |
|---|---|---|
| **A. 1810 is canonical** | The clock is a historical-to-future grid beginning at a chosen Monday epoch. | Convert every event family—including Tuesday through Sunday and all time layers—to the 1810 baseline. |
| **B. 2026 is canonical** | The clock is a present/future reference calendar. | Move all new century, decade, generic month/day, and sub-day events to a consistent 2026 baseline. |
| **C. Mixed origin is intentional** | Historic civil layers coexist with a contemporary operational clock. | Keep the mixed dates and document the distinction in calendar descriptions. |

**Recommended expectation:** **A**, since the generic Week, Day, Monday, Year, Month, and Decade layers already converge on 1810 and the chosen date aligns with Monday.

### 3. What does “century” mean?

`DTSTART;VALUE=DATE:19000101` represents the start of the **1900s block**. In formal ordinal Gregorian numbering, however, the 20th century begins on 1901-01-01 and ends on 2000-12-31. This is not a syntax question; it is an editorial convention.

| Option | Label and start | Meaning |
|---|---|---|
| **A. Ordinal centuries** | `20TH CENTURY`, `19010101` | Traditional ordinal-century convention. |
| **B. Hundreds blocks** | `1900S`, `19000101` | Groups by the leading digits of the year. |

**Recommended expectation:** **B**, because the submitted `19000101` anchor already expresses it. If selected, rename `SUMMARY:CENTURY` to `SUMMARY:1900S` or a similarly explicit label to avoid ambiguity.

### 4. Tick semantics

Hour, Minute, and Second can either be **zero-duration ticks** or **fixed-duration unit bands**. An event with `DTSTART` but neither `DTEND` nor `DURATION` is instantaneous; for a DATE-TIME VEVENT, it ends at its start.[1]

| Layer | Tick model | Band model | Recommended expectation |
|---|---|---|---|
| Hour | `FREQ=HOURLY`, no duration | `DURATION:PT1H` | Band, if it will be visually displayed. |
| Minute | `FREQ=MINUTELY`, no duration | `DURATION:PT1M` | Tick or separate feed; a minute band is dense. |
| Second | `FREQ=SECONDLY`, no duration | `DURATION:PT1S` | Tick only, and separate/bounded. |

A perpetual second-level RRULE is syntactically allowed—`SECONDLY` is an RFC-defined frequency—but it represents 86,400 instances per day and can be expensive for calendar viewers to expand.[4] Its intended purpose should therefore be explicit: **experimental/symbolic**, **short-window diagnostic**, or **continuously subscribed live clock**.

### 5. Visual hierarchy and priorities

The original values establish a useful scale hierarchy: Year = 1, Quarter = 2, Month = 3, Week = 4, Day = 5, Hours = 6, Minutes = 7. RFC 5545 treats lower numbers as higher priority, but clients may not render or sort by it consistently.[5]

| Decision | Recommended expectation |
|---|---|
| Century / Decade priority | Either omit priority (undefined) or use 1 and shift the rest down only if you want the hierarchy strictly ordered. |
| Generic vs named layers | Use the same category and priority at the same scale: e.g., Month and JANUARY are both `month`/priority 3. |
| Blank priority fields | Never represent “no priority” with `PRIORITY:`; either omit it or set `PRIORITY:0`.[5] |

### 6. Client and performance policy

The calendar should be treated as a **reference overlay**, not a workload scheduler. The published master may reasonably contain layers through hours; minute and especially second layers should be delivered deliberately.

| Profile | Recommended contents | Intended use |
|---|---|---|
| **Core** | Century through Day | Stable, broadly importable historical/civil overlay. |
| **Clock** | Core + Hour + named 204-minute segments | Practical daily rhythm overlay. |
| **Dense** | Clock + Minute | Specialized view, likely not suitable for broad subscription. |
| **Experimental** | Dense + Second | Testing, demonstration, or a controlled client only. |

## Non-Negotiable Standards Expectations

These are implementation constraints, not content choices. They will be repaired once the semantic choices above are confirmed.

| Constraint | Required implementation |
|---|---|
| RRULE parts | Use `NAME=VALUE`; therefore `INTERVAL=100`, not `INTERVAL:100`.[4] |
| Floating starts | Use bare `DTSTART:YYYYMMDDTHHMMSS`; do not add `TZID` or a `Z` suffix.[3] |
| Revision stamp | Use UTC `DTSTAMP:…Z`; this is metadata and does not make the event itself zone-bound.[6] |
| Priority | Omit the property or supply an integer 0–9.[5] |
| Sub-day recurrence | Give Hour, Minute, and Second a DATE-TIME start rather than `VALUE=DATE`, because the time-of-day must come from the start value.[4] |
| Calendar transport | Use CRLF content lines; fold any line longer than 75 octets.[7] |

## Proposed Confirmation Set

Before I produce a repaired file, please confirm or override the following set:

1. **Model B:** full-period bands for week/day/hour where useful; boundary markers for variable calendar periods; minute/second as ticks.
2. **Epoch A:** 1810 is the canonical origin for every layer.
3. **Century B:** preserve `19000101` as a “1900s” boundary and revise its label accordingly.
4. Publish two practical feeds: **Core** (through Day) and **Clock** (through Hour and named daily segments); keep Minute and Second out of normal subscriptions.
5. Keep all event `DTSTART` values floating, preserve UTC only for `DTSTAMP`, and retain `METHOD:PUBLISH`.

## References

[1]: https://icalendar.org/iCalendar-RFC-5545/3-6-1-event-component.html "RFC 5545 §3.6.1: Event Component"
[2]: https://icalendar.org/iCalendar-RFC-5545/3-7-1-calendar-scale.html "RFC 5545 §3.7.1: Calendar Scale"
[3]: https://icalendar.org/iCalendar-RFC-5545/3-3-5-date-time.html "RFC 5545 §3.3.5: Date-Time"
[4]: https://icalendar.org/iCalendar-RFC-5545/3-3-10-recurrence-rule.html "RFC 5545 §3.3.10: Recurrence Rule"
[5]: https://icalendar.org/iCalendar-RFC-5545/3-8-1-9-priority.html "RFC 5545 §3.8.1.9: Priority"
[6]: https://icalendar.org/iCalendar-RFC-5545/3-8-7-2-date-time-stamp.html "RFC 5545 §3.8.7.2: Date-Time Stamp"
[7]: https://icalendar.org/iCalendar-RFC-5545/3-1-content-lines.html "RFC 5545 §3.1: Content Lines"
