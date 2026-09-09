# Review of the Hand-Edited `cron_clock` Calendar

**Scope:** This review evaluates the submitted text as iCalendar / RFC 5545 content and against your stated requirement that scheduled event times be **floating local** rather than time-zone-bound.

## Verdict

The expanded design is coherent: the new century, decade, generic month, generic day, and sub-day marker layers fit the `cron_clock` idea well. **Do not import this revision yet.** It has a small number of high-impact syntax defects plus a set of consistency and performance choices to settle.

| Finding | Count | Severity | Required repair |
|---|---:|---|---|
| `INTERVAL:` uses a colon instead of an equals sign | 2 | Blocker | Change to `INTERVAL=100` and `INTERVAL=10`. |
| Empty `PRIORITY:` properties | 25 | Blocker | Remove the property or use `PRIORITY:0`. |
| `DTSTAMP` lacks UTC `Z` | 27 | Blocker | Use a real UTC revision stamp, for example `DTSTAMP:20260819T000000Z`. |
| `TZID=America/Boise` remains on floating event starts | 9 | Blocker for your floating-time requirement | Remove `TZID=America/Boise` and retain the bare local `DATE-TIME`. |
| Sub-day recurrence begins with DATE-only `DTSTART` | 3 | Major portability issue | Make Hour, Minute, and Second starts floating `DATE-TIME` values. |
| Unbounded `SECONDLY` recurrence | 1 | Major operational risk | Bound it with `UNTIL`/`COUNT`, or keep it out of a normally subscribed calendar. |

The automated audit parsed **42 VEVENTs** and reported **66 concrete violations** across the first five categories in the table. It also confirmed that `1810-01-01` is a Monday, so the historical epoch used for your Monday, generic Day, and generic Week markers has correct weekday alignment.

## Must-Fix Edits

### 1. Repair `RRULE` syntax

Your century and decade entries use a colon in `INTERVAL`. An RRULE is a semicolon-separated series of `NAME=VALUE` parts; the submitted values are not valid recurrence-rule grammar.[1]

```ics
BEGIN:VEVENT
UID:century-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART;VALUE=DATE:19000101
RRULE:FREQ=YEARLY;INTERVAL=100
SUMMARY:CENTURY
DESCRIPTION:Century
CATEGORIES:century
PRIORITY:0
TRANSP:TRANSPARENT
END:VEVENT

BEGIN:VEVENT
UID:decade-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART;VALUE=DATE:18100101
RRULE:FREQ=YEARLY;INTERVAL=10
SUMMARY:DECADE
DESCRIPTION:Decade
CATEGORIES:decade
PRIORITY:0
TRANSP:TRANSPARENT
END:VEVENT
```

### 2. Replace blank priorities

`PRIORITY:` with no value is invalid: the property must carry an integer from 0 through 9. Because the default is undefined priority, the cleanest repair is normally to **delete all empty priority lines**. If you want an explicit value, use `PRIORITY:0`.[2]

```ics
; Preferred: omit PRIORITY entirely

; Also valid: state the default explicitly
PRIORITY:0
```

### 3. Keep `DTSTAMP` UTC, but make only `DTSTART` floating

A floating event start is correctly written as a bare `DATE-TIME`, without either `TZID` or `Z`; this fixes the remaining nine zone-bound events, Dawn through Sethera.[3] `DTSTAMP` is different: it is revision metadata and must use UTC, so its trailing `Z` stays.[4]

```ics
BEGIN:VEVENT
UID:dawn-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART:18100101T000000
DURATION:PT8H
RRULE:FREQ=DAILY
SUMMARY:Dawn
DESCRIPTION:Dawn
PRIORITY:6
CATEGORIES:Hours
TRANSP:TRANSPARENT
END:VEVENT
```

Apply the same `DTSTART` conversion to **Noon, Dusk, Yan, Tan, Tethera, Methera, Pits, and Sethera**. Your hand-edited Azer entry already demonstrates the desired floating `DTSTART` form, although its `DTSTAMP` and blank priority still need repair.

### 4. Give sub-day clocks a floating date-time anchor

A `DATE` conveys only year, month, and day. The recurrence specification derives time-of-day information from `DTSTART`; therefore, `FREQ=HOURLY`, `FREQ=MINUTELY`, and `FREQ=SECONDLY` need a floating **DATE-TIME** start for predictable cross-client behavior.[1] [5]

```ics
BEGIN:VEVENT
UID:hour-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART:18100101T000000
RRULE:FREQ=HOURLY
SUMMARY:HOUR
DESCRIPTION:Hour
CATEGORIES:hour
PRIORITY:0
TRANSP:TRANSPARENT
END:VEVENT

BEGIN:VEVENT
UID:minute-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART:18100101T000000
RRULE:FREQ=MINUTELY
SUMMARY:MINUTE
DESCRIPTION:Minute
CATEGORIES:minute
PRIORITY:0
TRANSP:TRANSPARENT
END:VEVENT
```

Whether these are **point markers** or **spans** is a product choice. Without `DTEND` or `DURATION`, an event is instantaneous. If you intend bands, add `DURATION:PT1H` to Hour and `DURATION:PT1M` to Minute. The same convention would make Second use `DURATION:PT1S`.

### 5. Contain the `SECONDLY` feed

`FREQ=SECONDLY` is legal, but without `COUNT` or `UNTIL` the recurrence repeats forever.[1] A single such VEVENT represents **86,400 occurrences per day**. Many calendar clients will lag, reject the import, or aggressively truncate expansion. A bounded diagnostic variant is safer:

```ics
BEGIN:VEVENT
UID:tick-vault_time@cron_clock
DTSTAMP:20260819T000000Z
DTSTART:20260819T000000
DURATION:PT1S
RRULE:FREQ=SECONDLY;COUNT=60
SUMMARY:SECOND
DESCRIPTION:Second
CATEGORIES:second
PRIORITY:0
TRANSP:TRANSPARENT
END:VEVENT
```

If continuous seconds are essential, I recommend separating that one marker into a non-subscribed experimental calendar rather than publishing it with the day-, week-, and year-scale events.

## Coherence Improvements

The following adjustments are not RFC blockers, but they would make the file easier to reason about and maintain.

| Topic | Current state | Recommended decision |
|---|---|---|
| Epoch | Generic markers and Monday start in 1810; Tuesday through Sunday start in 2026. | Choose one coverage rule. For a historical clock grid, use 1810 for all weekdays: Tuesday `18100102`, Wednesday `18100103`, through Sunday `18100107`. If the calendar only needs current/future events, use 2026 consistently. |
| Named annual markers | `FREQ=YEARLY` plus matching `DTSTART`. | Valid as written. Optional `BYMONTH` and `BYMONTHDAY` make the month/quarter meaning explicit but do not change the matching recurrence. |
| `DTSTAMP` date | Newly added events use `20270101T000000`, a future revision date relative to this review. | Use the actual UTC date/time when the file is generated or last revised. |
| `X-WR-COLOR:white` | Valid nonstandard extension syntax, but client support is not universal. | Keep it if your target client honors it; do not rely on it for essential meaning. |
| Period labels | Century, decade, month, and year entries are one-day all-day markers, not full-duration bands. | Keep them as boundary markers unless you specifically want multi-day visual spans. Calendar durations cannot express a variable-length calendar month with one simple repeating rule. |

## What Is Already Good

`METHOD:PUBLISH`, `CALSCALE:GREGORIAN`, the three-level event organization, transparent time handling, unique UIDs, and the all-day `VALUE=DATE` treatment of civil calendar boundaries are all sensible. `CALSCALE:GREGORIAN` belongs at calendar level and is exactly the appropriate way to state Gregorian semantics.[6] Your 1810 weekly origin is also sound: January 1, 1810 was a Monday.

## References

[1]: https://icalendar.org/iCalendar-RFC-5545/3-3-10-recurrence-rule.html "RFC 5545 §3.3.10: Recurrence Rule"
[2]: https://icalendar.org/iCalendar-RFC-5545/3-8-1-9-priority.html "RFC 5545 §3.8.1.9: Priority"
[3]: https://icalendar.org/iCalendar-RFC-5545/3-3-5-date-time.html "RFC 5545 §3.3.5: Date-Time"
[4]: https://icalendar.org/iCalendar-RFC-5545/3-8-7-2-date-time-stamp.html "RFC 5545 §3.8.7.2: Date-Time Stamp"
[5]: https://icalendar.org/iCalendar-RFC-5545/3-3-4-date.html "RFC 5545 §3.3.4: Date"
[6]: https://icalendar.org/iCalendar-RFC-5545/3-7-1-calendar-scale.html "RFC 5545 §3.7.1: Calendar Scale"
