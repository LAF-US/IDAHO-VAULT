# Complete X-WR Property Matrix

## Correction to the Prior Review

The earlier review was incomplete because it covered only the three `X-WR-*` properties already in the calendar header. The broader, attested ecosystem includes two alarm-identifier variants as well as the timezone convention. The practical family is therefore:

| Property | Where observed | Core status |
|---|---|---|
| `X-WR-CALNAME` | Apple-origin ICS exports; Microsoft import/export documentation; Mozilla compatibility work; iCal4j extensions | Widely recognized legacy calendar-name alias |
| `X-WR-CALDESC` | Apple-origin ICS exports; Microsoft export documentation; iCal4j extensions | Legacy calendar-description alias |
| `X-WR-RELCALID` | Apple-origin ICS exports; Microsoft import/export documentation; iCal4j extensions | Legacy stable calendar-identity alias |
| `X-WR-TIMEZONE` | Apple/Google-era feeds and iCal4j compatibility analysis | Nonstandard calendar-default time-zone convention |
| `X-WR-ALARMUID` | Apple iCal/Calendar VALARM examples and compatibility tests | Apple alarm-identifier spelling |
| `X-WR-ALARMID` | iCal4j extension implementation and fixtures | Library/ecosystem alarm-identifier spelling |

The two alarm tokens are **not interchangeable in deployed data**. Apple-origin material attests `X-WR-ALARMUID`; current iCal4j extension code implements `X-WR-ALARMID`. Neither is in the current main IANA iCalendar Property Registry.[1] [2] [3]

## Full Standards and Interoperability Matrix

| Legacy field | Component scope | Practical meaning | Modern standards equivalent | Interoperability assessment | `cron_clock` policy |
|---|---|---|---|---|---|
| `X-WR-CALNAME` | VCALENDAR | Human display name for an imported/subscribed calendar | `NAME` on VCALENDAR, RFC 7986 §5.1 | Strongest legacy X-WR field. Microsoft specifies import into the calendar display name; Mozilla still tracks handling of `NAME` or this legacy field. [4] [5] | **Keep as an exact mirror of `NAME`**. |
| `X-WR-CALDESC` | VCALENDAR | Human description of an exported calendar | `DESCRIPTION` on VCALENDAR, RFC 7986 §5.2 | Medium legacy value. Microsoft documents it but recommends ignoring it on import; iCal4j labels it experimental. [6] [7] | **Optional mirror** of `DESCRIPTION`; retain only for legacy export tolerance. |
| `X-WR-RELCALID` | VCALENDAR | Stable, globally unique calendar-export identifier, used by importers to distinguish update from new calendar | `UID` on VCALENDAR, RFC 7986 §5.3, with `LAST-MODIFIED` | Strong legacy value for import identity. Microsoft explicitly recommends persisting it for overwrite/new-calendar decisions. [8] [9] | **Keep as an exact mirror of VCALENDAR `UID`**. |
| `X-WR-TIMEZONE` | VCALENDAR | An assumed default zone for DATE-TIMEs without `TZID` | No direct property. Standards use `TZID` on each local DATE-TIME plus a matching `VTIMEZONE`, or UTC. | Risky. Consumers disagree on whether to honor it; it can silently change floating-time interpretation. [10] [11] | **Do not emit**. The calendar intentionally uses floating local time. |
| `X-WR-ALARMUID` | VALARM | Apple-origin unique alarm identifier | `UID` inside `VALARM`, RFC 9074 §4 | Historical Apple compatibility detail. It is not needed for an event without alarms. [3] [12] | **Do not emit**. If alarms are later added, use standard VALARM `UID`. |
| `X-WR-ALARMID` | VALARM | Alternative library ecosystem unique alarm identifier | `UID` inside `VALARM`, RFC 9074 §4 | iCal4j explicitly implements it as a nonstandard extension; it should not be confused with Apple’s `...ALARMUID`. [2] [12] | **Do not emit**. Use standard VALARM `UID` if needed. |

## What Is Actually Redundant

The redundancy is straightforward for the first three fields:

| Canonical standard field | Legacy compatibility mirrors | Rule |
|---|---|---|
| `NAME` | `X-WR-CALNAME` | Values must be byte-for-byte equivalent after normal iCalendar text escaping. |
| Calendar-level `DESCRIPTION` | `X-WR-CALDESC` | Use the standard value as authority; omit the mirror if legacy tolerance is not required. |
| VCALENDAR `UID` | `X-WR-RELCALID` | Values must be identical and remain stable across revisions of the same published calendar. |

`X-WR-TIMEZONE` and the two alarm identifiers are different: they are **not harmless aliases**. A timezone changes interpretation; alarm IDs only matter if VALARMs exist. They should not be added merely to make the header look complete.

## Proposed Header Policy for `cron_clock`

```ical
NAME:cron_clock
DESCRIPTION:vault_time
UID:vault_time@cron_clock
LAST-MODIFIED:20270701T000000Z

X-WR-CALNAME:cron_clock
X-WR-CALDESC:vault_time
X-WR-RELCALID:vault_time@cron_clock
```

This is the compatibility maximum that remains semantically safe for this file. Omit `X-WR-CALDESC` if the intent is strict minimalism; retain the other two mirrors for public-feed import ergonomics. Do **not** add any `X-WR-TIMEZONE`, `X-WR-ALARMUID`, or `X-WR-ALARMID` property.

## Additional X-WR Names: Research Boundary

A search across current standards, Microsoft’s iCalendar conversion specification, Apple-origin compatibility material, maintained open-source extensions, and broad public-code evidence did **not** produce a separate, stable X-WR field beyond the six names above. Search fragments such as `X-WR-CALID`, `X-WR-DESC`, or `X-WR-GEO` did not yield credible iCalendar property definitions; they should not be treated as part of the family without a source feed and target-client test.

One caveat is worth preserving: iCal4j’s current `WrAlarmId` source links to an old IANA `icalendar-extensions` path, but that endpoint no longer resolves, while the current IANA main registry has no X-WR entries. Treat `X-WR-ALARMID` as an attested library extension—not as a currently registered standard.[1] [2]

## References

[1]: https://www.iana.org/assignments/icalendar/icalendar.xhtml "IANA iCalendar Element Registries"
[2]: https://github.com/ical4j/ical4j-extensions/blob/8c2ad6df9376423dbf245cc4331bf5d6d8c23f19/src/main/java/net/fortuna/ical4j/extensions/model/property/WrAlarmId.java "iCal4j WrAlarmId source"
[3]: https://github.com/collective/icalendar/issues/69 "Apple-origin X-WR-ALARMUID compatibility example"
[4]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[5]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1da58449-b97e-46bd-b018-a1ce576f3e6d "Microsoft X-WR-CALNAME import/export behavior"
[6]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/9194db93-6de2-41b3-bebe-fc76a11e31e9 "Microsoft X-WR-CALDESC import/export behavior"
[7]: https://www.ical4j.org/extensions/ "iCal4j experimental extension catalog"
[8]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/3ef9f606-0d63-4e56-a86d-73617afa7383 "Microsoft X-WR-RELCALID import/export behavior"
[9]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986 VCALENDAR UID and LAST-MODIFIED"
[10]: https://ical4j.github.io/2022/06/17/support-for-x-wr-timezone.html "iCal4j X-WR-TIMEZONE portability analysis"
[11]: https://blog.jonudell.net/2011/10/17/x-wr-timezone-considered-harmful/ "Cross-client X-WR-TIMEZONE interoperability analysis"
[12]: https://www.rfc-editor.org/rfc/rfc9074.html "RFC 9074: VALARM UID and alarm extensions"
