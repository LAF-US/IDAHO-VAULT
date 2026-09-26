# X-WR Properties: Ecosystem Adoption, RFC 7986 Redundancy, and Recommendation

## Conclusion

Your intuition is correct: three `X-WR-` fields are **legacy community conventions with near-direct RFC 7986 successors**. The apparent “proposed revision” is no longer proposed—**RFC 7986 has been an IETF Standards Track update to RFC 5545 since 2016**.[1] The legacy fields are still useful as compatibility mirrors because support across importers is uneven, but the RFC 7986 fields should now be authoritative.

The right model for `cron_clock` is therefore **standards-first dual emission**: retain exact-value `X-WR-` aliases for legacy compatibility, while treating `NAME`, calendar-level `DESCRIPTION`, and VCALENDAR `UID` as canonical. The only X-WR sibling that should remain absent is `X-WR-TIMEZONE`, because it conflicts with the calendar’s explicitly chosen floating-local-time semantics.

## Field-by-Field Mapping

| Legacy convention | Standard counterpart | Relationship | Evidence of ecosystem use | Recommended treatment |
|---|---|---|---|---|
| `X-WR-CALNAME` | `NAME` at VCALENDAR | Direct semantic successor: calendar display name. | Microsoft documents import into a calendar folder’s display name and recommends it for calendar exports. Mozilla’s live tracking issue explicitly considers `NAME` **or** `X-WR-CALNAME`; legacy Apple/iPod behavior historically relied on the latter.[2] [3] | **Keep both**, with exactly the same text. Make `NAME` authoritative. |
| `X-WR-CALDESC` | Calendar-level `DESCRIPTION` | Direct semantic successor: calendar description. | Microsoft documents export support but recommends ignoring it on import. The iCal4j extension library still provides it, but labels it experimental.[4] [5] | **Keep only as a low-cost mirror** if Apple/Exchange legacy imports matter; otherwise it is the first X-WR field you could retire. Make `DESCRIPTION` authoritative. |
| `X-WR-RELCALID` | VCALENDAR `UID` | Functional successor: stable, globally unique identifier for an exported calendar. | Microsoft specifies that it helps decide whether an import updates an existing calendar or creates another, and asks exporters to keep it stable across exports. RFC 7986 gives VCALENDAR `UID` the same persistent-calendar identity role.[6] [1] | **Keep both**, with the same stable opaque value. Make VCALENDAR `UID` authoritative and pair it with `LAST-MODIFIED`. |
| `X-WR-TIMEZONE` | No direct one-line equivalent; use per-event `TZID` plus `VTIMEZONE`, or UTC. | Not superseded by a calendar-wide standard default-zone property. | iCal4j describes its meaning as unresolved and portability-sensitive. Strict RFC 5545 consumers may treat date-times without `TZID` as floating, while others infer the X-WR zone.[7] [8] | **Do not add it.** It would contradict the chosen floating local-time model. |

## What “Popular Consensus” Actually Means Here

`X-WR-*` is not an IANA-registered property family. The current IANA iCalendar property registry contains `NAME`, `DESCRIPTION`, `UID`, `LAST-MODIFIED`, `SOURCE`, and `COLOR`, but not the three X-WR property names.[9] The `X-` prefix makes them permissible nonstandard properties under RFC 5545; it does **not** turn them into a shared formal contract.

The practical consensus is nevertheless real. Microsoft has public import/export specifications for all three fields. Mozilla’s long-running calendar issue shows both historical Apple/iPod dependence on `X-WR-CALNAME` and continuing interest in recognizing either `NAME` or the legacy alias. iCal4j ships implementations of `X-WR-CALNAME`, `X-WR-CALDESC`, `X-WR-RELCALID`, and `X-WR-TIMEZONE`, but clearly categorizes them as experimental extensions rather than core properties.[2] [3] [5]

> The distinction is important: **widely encountered** is not the same as **universally interpreted**. Emit the standards fields for interoperable semantics; keep selected X-WR mirrors for legacy import ergonomics.

## Recommended VCALENDAR Header Shape

Use matching values, in this hierarchy:

```ical
BEGIN:VCALENDAR
VERSION:2.0
PRODID:~//VAULT//cron_clock//U+00BF
CALSCALE:GREGORIAN
METHOD:PUBLISH

NAME:cron_clock
DESCRIPTION:vault_time
UID:vault_time@cron_clock
LAST-MODIFIED:20270701T000000Z

X-WR-CALNAME:cron_clock
X-WR-CALDESC:vault_time
X-WR-RELCALID:vault_time@cron_clock
END:VCALENDAR
```

This is not a complete file; it demonstrates the identity and display metadata contract only. `UID` and `X-WR-RELCALID` should remain exact aliases unless you intentionally decide that one identifies a different object. `NAME` and `X-WR-CALNAME`, likewise, should not diverge. A mismatch creates an importer-dependent identity or display name.

## Compatibility Tiers

| Publishing objective | Header policy | Trade-off |
|---|---|---|
| Strict, clean standards feed | `NAME`, `DESCRIPTION`, `UID`, `LAST-MODIFIED`; omit X-WR fields. | Semantically cleanest, but some legacy tools may derive an unhelpful subscription name. |
| Recommended public feed | Standards fields plus exact `X-WR-CALNAME` and `X-WR-RELCALID` mirrors; optionally mirror `X-WR-CALDESC`. | Best balance of standard semantics and legacy importer support. |
| Apple/Exchange legacy target | Emit all three mirrors plus standards fields. | Redundant but robust, provided aliases always agree. |

For `cron_clock`, the **recommended public feed** is the best fit. It preserves a stable recognizable name and calendar identity for older importers while putting the standardized properties in the primary role.

## Timezone Warning: Particularly Important for This Calendar

Do not use `X-WR-TIMEZONE` as a harmless compatibility header. Its behavior is different from the name and identifier aliases: it can change how consumers interpret **every floating DATE-TIME**. iCal4j documents that it may be treated as a default time zone for properties with no `TZID`; older ecosystem analysis found some consumers honored it while strict parsers did not.[7] [8]

That outcome would defeat your requirement that phase, hour, minute, and second events remain floating local time. The absence of `X-WR-TIMEZONE`, `TZID`, and `VTIMEZONE` is therefore intentional semantic data, not missing metadata.

## Relationship Fields: A Separate Standardization Opportunity

The empty and informal `RELATED-TO` structure in the calendar is not an X-WR issue, but RFC 9253 is now relevant to your hierarchy. It adds `CONCEPT`, `REFID`, more `RELTYPE` values, and richer `RELATED-TO` semantics specifically because free-form categories and simple relationships did not provide enough structured grouping.[10] This is a better future path for expressing the millennium → century → decade → year and other structural relationships than inventing another `X-WR-*` extension.

## References

[1]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[2]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1da58449-b97e-46bd-b018-a1ce576f3e6d "Microsoft Open Specifications: X-WR-CALNAME"
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=168176 "Mozilla Bug 168176: NAME or X-WR-CALNAME"
[4]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/9194db93-6de2-41b3-bebe-fc76a11e31e9 "Microsoft Open Specifications: X-WR-CALDESC"
[5]: https://www.ical4j.org/extensions/ "iCal4j Extensions: Experimental X-WR Properties"
[6]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/3ef9f606-0d63-4e56-a86d-73617afa7383 "Microsoft Open Specifications: X-WR-RELCALID"
[7]: https://ical4j.github.io/2022/06/17/support-for-x-wr-timezone.html "iCal4j: Support for X-WR-TIMEZONE"
[8]: https://blog.jonudell.net/2011/10/17/x-wr-timezone-considered-harmful/ "X-WR-TIMEZONE considered harmful?"
[9]: https://www.iana.org/assignments/icalendar/icalendar.xhtml "IANA iCalendar Element Registries"
[10]: https://www.rfc-editor.org/rfc/rfc9253.html "RFC 9253: Support for iCalendar Relationships"
