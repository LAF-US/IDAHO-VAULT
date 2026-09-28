# X-WR Ecosystem Research Notes

## Microsoft Exchange Documentation

Microsoft’s Open Specifications describe `X-WR-CALNAME`, `X-WR-CALDESC`, and `X-WR-RELCALID` as calendar-level properties with no RFC reference, demonstrating that the X-WR family has operational interoperability significance beyond Apple-origin feeds.

* `X-WR-CALNAME` specifies the calendar name. Microsoft documents import into the calendar folder display name and recommends export for calendar exports, but not single appointments.
* `X-WR-CALDESC` specifies a calendar description. Microsoft documents it as ignored on import, but potentially exported from owner-supplied calendar description text.
* `X-WR-RELCALID` is used to decide whether a calendar import overwrites an existing calendar or creates a new one; it should be stable across exports of the same calendar.

## Standards Counterparts

RFC 7986 standardizes VCALENDAR-level `NAME`, `DESCRIPTION`, and `UID` after these X-WR conventions were already in circulation. The mapping is conceptually direct but not universally equivalent at the import-behavior level.

Sources:

* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1da58449-b97e-46bd-b018-a1ce576f3e6d
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/9194db93-6de2-41b3-bebe-fc76a11e31e9
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/3ef9f606-0d63-4e56-a86d-73617afa7383
* https://www.rfc-editor.org/rfc/rfc7986.html

## Adoption Caveat: Standardization Is Not Full Replacement

A current Workiva import-requirements document (updated 2026-04-09) accepts both standardized and legacy alternatives: `UID` or `X-WR-RELCALID`, `NAME` or `X-WR-CALNAME`, and `DESCRIPTION`, `X-WR-CALDESC`, or `X-ALT-DESC`. It also recognizes `X-WR-TIMEZONE` as a default-zone source. This is direct evidence that later standard fields and legacy X-WR fields coexist in a current importer rather than one having universally displaced the other.

Mozilla Bug 168176 remains open and was updated in 2026. Its title explicitly requests use of `NAME` (RFC 7986) **or** `X-WR-CALNAME`, indicating neither field can be assumed universally consumed in that client.

RFC 9074 standardizes `UID` in a `VALARM` component, providing a formal successor concept for legacy alarm identifiers. The current iCal4j extensions catalog nevertheless still calls `X-WR-ALARMID`, `X-WR-CALDESC`, `X-WR-CALNAME`, `X-WR-RELCALID`, and `X-WR-TIMEZONE` experimental properties.

Sources:

* https://support.workiva.com/hc/en-us/articles/45063432279700-Calendar-import-requirements
* https://bugzilla.mozilla.org/show_bug.cgi?id=168176
* https://www.rfc-editor.org/rfc/rfc9074.html
* https://www.ical4j.org/extensions/
