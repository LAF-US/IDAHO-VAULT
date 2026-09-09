# Authoritative Comparison Ledger

## Finding

The previously delivered `eleanor_shellstrop_cron_clock.ics` was **not rebuilt from your latest calendar**. It was a mechanically repaired version of an earlier, materially smaller draft. Your criticism is warranted.

| Comparison | Your authoritative source | Prior delivery | Consequence |
|---|---:|---:|---|
| VEVENTs | 52 | 42 | The delivery omitted 10 event occurrences. |
| Calendar-level content lines | 16 | 10 | It omitted the new calendar identity, source, refresh, and standard color metadata. |
| Shared events with different properties | 42 of 42 | 42 of 42 | Even the matching events were not faithful copies; their epoch, labels, categories, priorities, colors, and metadata came from the earlier draft. |
| Source-only event occurrences | 10 | 0 | Millennium; S1–S6 senaries; Half, Score, and Dozen. |

> The prior file was therefore not a valid “repair of yours”; it was a repair of the wrong source. No property from the authoritative structure should be inferred from that delivery.

## What Your Authoritative Source Adds or Changes

Your source establishes the following structure, none of which was preserved in the prior delivery: the VCALENDAR-level `NAME`, `UID`, `SOURCE`, `REFRESH-INTERVAL`, `COLOR`, and revised `PRODID`; a millennium layer; six senary events; colored weekday, phase, and named 204-minute layers; priority/category assignments; and the Half, Score, Dozen, Minute, and Second layers.

The source also establishes **1810-01-01 as the common-Monday origin** for the weekly, daily, phase, and named daily-rhythm layers. The earlier delivery retained legacy 2026 anchors in numerous matching events instead of preserving this rule.

## Strict Mechanical Defects in the Authoritative Text

These are defects in the pasted source itself, independent of the prior delivery. They can be repaired without changing the intended hierarchy or visual metadata.

| Mechanical issue | Quantity | Conservative treatment |
|---|---:|---|
| Invalid `DTSTAMP` values such as `20270101Z` | 53: one VCALENDAR-level line and 52 event lines | Replace the VCALENDAR-level stamp with `LAST-MODIFIED:20270101T000000Z` and make every VEVENT stamp a full UTC DATE-TIME, e.g. `DTSTAMP:20270101T000000Z`.[1] |
| Invalid refresh interval `P3M` | 1 VCALENDAR property | RFC 5545 duration syntax has no calendar-month unit. Confirm whether the intended policy is a fixed 90-day interval, a different day/week interval, or a publisher-specific extension before replacing it.[2] |
| `INTERVAL:` rather than `INTERVAL=` | 3: Half, Score, Dozen | Replace only the separator with `=`.[3] |
| Duplicate UID `dozen-vault_time@cron_clock` | 3 event masters | Assign distinct stable UIDs to Half, Score, and Dozen; no three independent masters may share one UID.[4] |
| LF delimiters and trailing blank line | 1 formatting condition and line 719 | Serialize content lines using CRLF and remove the empty line.[5] |

The fields `RELATED-TO:` and blank `COLOR:` values are retained in this ledger as user-authored placeholders. They are not being silently deleted or reinterpreted.

## Exact Missing Event Occurrences

| Omitted from prior delivery | Count |
|---|---:|
| `millenium-vault_time@cron_clock` | 1 |
| `s1-vault_time@cron_clock` through `s6-vault_time@cron_clock` | 6 |
| `dozen-vault_time@cron_clock` | 3 |

## Non-Mechanical Items Deliberately Not Changed

The following are source semantics, not simple repair decisions: `DTSTART;VALUE=DATE` on hourly/minutely/secondly events; the selected 1601/1810/2001 anchors; empty placeholder relationship/color values; the spelling embedded in the millennium UID; exact labels; category and priority system; and recurrence duration/volume. They must be preserved unless you expressly request a semantic revision.

## References

[1]: https://icalendar.org/iCalendar-RFC-5545/3-8-7-2-date-time-stamp.html "RFC 5545 §3.8.7.2: Date-Time Stamp"
[2]: https://www.rfc-editor.org/rfc/rfc5545.txt "RFC 5545 §3.3.6: Duration"
[3]: https://icalendar.org/iCalendar-RFC-5545/3-3-10-recurrence-rule.html "RFC 5545 §3.3.10: Recurrence Rule"
[4]: https://icalendar.org/iCalendar-RFC-5545/3-8-4-7-unique-identifier.html "RFC 5545 §3.8.4.7: Unique Identifier"
[5]: https://icalendar.org/iCalendar-RFC-5545/3-1-content-lines.html "RFC 5545 §3.1: Content Lines"
