# Correction: Standardization Is Not Full Supersession

## Governing Distinction

The prior phrase “superseded by” was too strong. A standards-track RFC establishes a **de jure successor**: it defines the interoperable vocabulary a conforming producer should use. It does **not** demonstrate that major calendar clients import, export, display, and round-trip that vocabulary reliably enough to remove an existing community convention.

> A legacy X-WR field is **fully superseded in practice** only when the replacement is standardized **and** independently demonstrated to preserve the same practical behavior across the target client ecosystem. The present research does not establish that threshold for any X-WR field.

## Revised Classification

| Legacy X-WR field | Standardized counterpart or model | De jure status | De facto adoption evidence | Correct conclusion |
|---|---|---|---|---|
| `X-WR-CALNAME` | `NAME` on VCALENDAR (RFC 7986) | Standardized counterpart exists. | Current Workiva documentation accepts either `NAME` or `X-WR-CALNAME`. Mozilla’s active issue requests support for either field; it has not resolved universal handling. [1] [2] | **Coexisting alternatives; not fully superseded.** Emit both where broad import compatibility matters. |
| `X-WR-CALDESC` | Calendar-level `DESCRIPTION` (RFC 7986) | Standardized counterpart exists. | Workiva accepts `DESCRIPTION`, `X-WR-CALDESC`, or `X-ALT-DESC`; Microsoft documents legacy export but says import may ignore it. [1] [3] | **Coexisting alternatives; not fully superseded.** Standard field should be canonical; legacy mirror is defensible for broad feeds. |
| `X-WR-RELCALID` | VCALENDAR `UID` (RFC 7986) | Standardized counterpart exists. | Workiva explicitly accepts `UID` or `X-WR-RELCALID`; Microsoft documents the latter for import update-versus-create decisions. [1] [4] | **Coexisting alternatives; not fully superseded.** Dual emission is justified for persistent published identities. |
| `X-WR-TIMEZONE` | No single counterpart; standards require explicit `TZID` + `VTIMEZONE` or UTC. | No standardized calendar-default-zone replacement. | Workiva still accepts it; iCal4j continues to support it as experimental. [1] [5] | **Not superseded.** Its semantics are incompatible with this calendar’s floating local times, so omission is intentional—not evidence of obsolescence. |
| `X-WR-ALARMUID` | `UID` inside `VALARM` (RFC 9074) | Standardized counterpart exists. | Apple-origin data uses the legacy form; this research did not identify comparable cross-client import/export evidence for VALARM `UID`. [6] [7] | **Formal successor, but adoption unproven.** Do not describe it as fully superseded. |
| `X-WR-ALARMID` | `UID` inside `VALARM` (RFC 9074) | Standardized counterpart exists. | iCal4j continues to expose it as an experimental property; no broad client-equivalence evidence was found. [5] [7] | **Formal successor, but adoption unproven.** Do not describe it as fully superseded. |

## Implication for `cron_clock`

The safe interoperability policy is not “replace X-WR with RFC fields.” It is:

| Property group | Publishing policy |
|---|---|
| Calendar name, description, and identity | Emit the RFC 7986 properties as the canonical values; emit matching `X-WR-CALNAME`, optionally `X-WR-CALDESC`, and `X-WR-RELCALID` for legacy compatibility. |
| Default timezone | Emit neither `X-WR-TIMEZONE` nor a standard zone declaration because the calendar deliberately represents local floating time. |
| Alarm identifiers | Emit neither legacy property while no VALARMs exist. If alarms are added, prefer standard VALARM `UID`; retain a legacy mirror only after testing the intended Apple/client target. |

This is a **compatibility recommendation**, not a claim that the legacy properties are obsolete. The right retirement condition is a tested client matrix for the intended publication audience, not the existence of an RFC alone.

## References

[1]: https://support.workiva.com/hc/en-us/articles/45063432279700-Calendar-import-requirements "Workiva Calendar import requirements, updated 2026-04-09"
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=168176 "Mozilla Bug 168176: NAME or X-WR-CALNAME support"
[3]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/9194db93-6de2-41b3-bebe-fc76a11e31e9 "Microsoft X-WR-CALDESC import/export behavior"
[4]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/3ef9f606-0d63-4e56-a86d-73617afa7383 "Microsoft X-WR-RELCALID import/export behavior"
[5]: https://www.ical4j.org/extensions/ "iCal4j experimental extensions"
[6]: https://github.com/collective/icalendar/issues/69 "Apple-origin X-WR-ALARMUID example"
[7]: https://www.rfc-editor.org/rfc/rfc9074.html "RFC 9074: VALARM Extensions for iCalendar"
