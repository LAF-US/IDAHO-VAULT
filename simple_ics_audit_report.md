# Narrow Syntax and Consistency Audit

**Scope:** This report is deliberately limited to **simple syntax defects and internal mismatches** in the submitted text. It does not recommend changes to epoch, hierarchy, recurrence design, duration design, feed topology, or performance policy.

## Mechanical Result

The file **parses successfully** as a calendar containing **42 VEVENTs**, with **42 unique UIDs**. Its `BEGIN`/`END` component structure is balanced. The named weekday and month events agree with their respective all-day start dates.

| Finding | Count | Lines / events | Simple correction |
|---|---:|---|---|
| Empty `PRIORITY:` property | 25 | Lines 18, 29, 40, 51, 62, 73, 84, 95, 106, 117, 128, 139, 150, 161, 172, 183, 194, 205, 216, 227, 239, 251, 478, 490, 501 | Delete the property or use `PRIORITY:0`; a priority must be an integer from 0 to 9.[1] |
| Incorrect RRULE delimiter | 2 | Lines 14 and 25 | Replace `INTERVAL:100` with `INTERVAL=100`, and `INTERVAL:10` with `INTERVAL=10`. RRULE parts use `NAME=VALUE` form.[2] |
| `DTSTAMP` missing UTC suffix | 27 | Lines 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 244, 259, 472, 484, 495, 506 | Append `Z` to a genuine UTC stamp, e.g. `DTSTAMP:20270101T000000Z`. `DTSTAMP` must be UTC; this is separate from floating event time.[3] |
| Remaining zone-bound starts | 9 | Dawn, Noon, Dusk, Yan, Tan, Tethera, Methera, Pits, Sethera | Remove `TZID=America/Boise` if the intended convention remains floating local time. A bare DATE-TIME is floating.[4] |
| Category mismatch | 1 | Azer, line 479 | Change `CATEGORIES:hour` to `CATEGORIES:Minutes` if Azer belongs to the named 204-minute sequence. |

## Conditional File-Formatting Note

The submitted attachment uses **LF** newlines. If that is the file’s actual byte-level form—not merely the platform’s pasted-text representation—normalize it to **CRLF** before distribution. RFC 5545 content lines are CRLF-delimited.[5]

## Confirmed Clean Checks

| Check | Result |
|---|---|
| VCALENDAR / VEVENT nesting | Balanced |
| Calendar parser | Success |
| VEVENT count | 42 |
| UID uniqueness | 42 unique UIDs |
| Named weekday vs start date | No mismatch found |
| Named month vs start date | No mismatch found |
| `CALSCALE:GREGORIAN` | Correct calendar-level form |
| `METHOD:PUBLISH` | Syntactically valid |
| `DURATION:PT204M` | Valid ISO 8601 duration syntax; it is simply a different spelling from `PT3H24M` |

## Intentionally Not Reviewed

This pass does **not** decide whether `1810-01-01 — a common Monday` is the correct epoch, whether the century label convention is right, whether layers should be markers or spans, whether generic minute/second entries should exist, or whether recurrences should be bounded. Those are semantic choices, not simple syntax/mismatch defects.

## References

[1]: https://icalendar.org/iCalendar-RFC-5545/3-8-1-9-priority.html "RFC 5545 §3.8.1.9: Priority"
[2]: https://icalendar.org/iCalendar-RFC-5545/3-3-10-recurrence-rule.html "RFC 5545 §3.3.10: Recurrence Rule"
[3]: https://icalendar.org/iCalendar-RFC-5545/3-8-7-2-date-time-stamp.html "RFC 5545 §3.8.7.2: Date-Time Stamp"
[4]: https://icalendar.org/iCalendar-RFC-5545/3-3-5-date-time.html "RFC 5545 §3.3.5: Date-Time"
[5]: https://icalendar.org/iCalendar-RFC-5545/3-1-content-lines.html "RFC 5545 §3.1: Content Lines"
