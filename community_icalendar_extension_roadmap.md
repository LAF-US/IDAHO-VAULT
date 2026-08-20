# Community iCalendar Extensions: Integration Landscape and RFC Roadmap

**Prepared for:** Logan Finney  
**Purpose:** Identify the significant community extension families beyond `X-WR-*`, distinguish properties that already have a standards-track home from genuine open gaps, and describe what credible RFC integration would require.

## Executive Assessment

The community extension landscape is not a single backlog of fields waiting to be standardized. It has three distinct populations. First, there are fields whose semantics are already represented by a later RFC but whose client adoption remains incomplete. Second, there are fields that expose a genuine shared capability gap, but need independent implementation evidence and a precise data model before they should become an Internet-Draft. Third, there are opaque vendor-state fields that should remain private implementation data rather than become common interchange syntax.

> **The RFC threshold is not popularity alone.** A candidate needs a stable cross-vendor use case, semantics that cannot be expressed safely with existing fields, a backwards-compatible iCalendar and JSCalendar mapping, a defined iTIP effect, and an implementation/security/privacy story. This is consistent with the current CALEXT charter. [8]

RFC 7986 and RFC 9073 are the important precedents: both standardize capabilities that vendors had previously improvised through extensions. Conversely, RFC 8607 shows that even deployed code may be documented as Informational rather than advanced to Standards Track when its design is not a sound basis for new protocol work. [1] [2] [9]

## Scope and Evidence Standard

The inventory below uses community field families encountered in current calendar practice, including Apple, Google, Microsoft/Outlook, libical, Entourage, Kerio, and X-WR conventions. A survey of seven real feeds exposes a broad field set, but is ecosystem evidence—not a proof of adoption share or interoperability. [10]

The readiness labels therefore mean the following:

| Label | Meaning |
|---|---|
| **Existing standard; adoption work remains** | An RFC property/component already expresses the need. The next task is client implementation, exporter profiles, and round-trip testing—not another field RFC. |
| **Promising RFC candidate** | A portable cross-vendor problem remains after existing standards are considered. A requirements document and implementation cohort are justified before registering new syntax. |
| **Profile or mapping issue** | Existing iCalendar syntax can encode the intended semantics; divergent exporters need guidance, tests, or a profile. |
| **Keep vendor/private** | The field carries local UI state, server bookkeeping, opaque identifiers, or product-specific behavior whose exchange semantics are not stable enough for general registration. |

## Community Field Families and Their Real Standards Path

| Community family and examples | Observable purpose | Current standard position | Readiness | Recommended next move |
|---|---|---|---|---|
| Rich description: `X-ALT-DESC` | Alternate HTML representation of an event description. Microsoft imports `FMTTYPE=text/HTML` and exports HTML from its rich-text representation. [6] | RFC 9073 defines `STYLED-DESCRIPTION` for rich text, including HTML and other media types. [2] | **Existing standard; adoption work remains** | Publish a plain `DESCRIPTION`, an RFC 9073 `STYLED-DESCRIPTION`, and—where Outlook compatibility is required—a matching `X-ALT-DESC`. Build a client matrix before retiring the legacy mirror. |
| Subscription hint: `X-PUBLISHED-TTL` | Suggested polling/download interval. Microsoft documents the extension but recommends ignoring it on import. [7] | RFC 7986 defines `REFRESH-INTERVAL;VALUE=DURATION` and `SOURCE;VALUE=URI` specifically for polling and refresh origin. [1] | **Existing standard; adoption work remains** | Prefer valid RFC 7986 fields. Preserve `X-PUBLISHED-TTL` only for a known legacy client profile; do not assert that it is obsolete until import behavior is measured. |
| Online meeting metadata: `X-GOOGLE-CONFERENCE`, `X-GOOGLE-HANGOUT`, `X-MICROSOFT-ONLINEMEETING*`, `X-MICROSOFT-SKYPETEAMS*` | Conference URI, dial-in material, service-specific data, and access controls. | RFC 7986 defines repeatable `CONFERENCE` with a URI plus `FEATURE` and `LABEL` parameters. [1] | **Existing standard; adoption work remains** | Test `CONFERENCE` against Google, Microsoft, Apple, Thunderbird, and CalDAV consumers. Standardize an interoperability profile for labels/features if needed; do not create another provider-neutral URI field. |
| Structured location: `X-APPLE-STRUCTURED-LOCATION`; `X-MICROSOFT-LOCATION*`; `X-MICROSOFT-LATITUDE/LONGITUDE` | Venue address, coordinates, geocoding source, multiple locations, and place metadata. | RFC 9073 supplies `VLOCATION`, `LOCATION-TYPE`, and `STRUCTURED-DATA`, explicitly addressing the limitations of a single unstructured `LOCATION` string. [2] | **Existing standard; adoption work remains** | Define sample mappings from Apple and Microsoft fields into RFC 9073 structures, including coordinate and privacy rules. Measure whether clients preserve rather than discard these components. |
| Alarm lifecycle: `X-APPLE-SNOOZE-TIME`, `X-NEXT-ALARM`, `X-ALARM-TRIGGER`, `X-WR-ALARMUID`/`X-WR-ALARMID` | Snooze state, next firing time, alarm identity, and acknowledgment behavior. | RFC 9074 adds VALARM identity and alarm lifecycle extensions, including a standard basis for alarm relationships and state. [3] | **Existing standard; adoption work remains** | Build test vectors that cover a snoozed alarm through import, dismiss, reschedule, export, and recurrence. Keep legacy Apple fields only where tested clients require them. |
| All-day flags: `X-MICROSOFT-CDO-ALLDAYEVENT`, `X-MICROSOFT-MSNCALENDAR-ALLDAYEVENT`, `X-FUNAMBOL-ALLDAY` | Explicitly mark events as all-day. | RFC 5545’s `DTSTART;VALUE=DATE` and matching exclusive `DTEND;VALUE=DATE` are the portable representation. | **Profile or mapping issue** | Publish a rigorous all-day profile and conformance tests. New generic all-day syntax would duplicate existing semantics. |
| Event busy state: `X-MICROSOFT-CDO-BUSYSTATUS`, `X-MICROSOFT-CDO-INTENDEDSTATUS`, `X-MICROSOFT-MSNCALENDAR-BUSYSTATUS` | More than binary availability: Microsoft maps FREE, TENTATIVE, BUSY, and OOF. [5] | RFC 5545 `TRANSP` only expresses opaque versus transparent event time. RFC 7953’s richer `BUSYTYPE` values apply to `VAVAILABILITY`, not ordinary `VEVENT` components. [4] | **Promising RFC candidate** | Develop a requirements draft for a **per-VEVENT busy-type** model. It must differentiate organizer intent, attendee-local state, privacy, `VFREEBUSY`/`VAVAILABILITY` calculation, iTIP scheduling behavior, and JSCalendar conversion. |
| Travel behavior: `X-APPLE-TRAVEL-ADVISORY-BEHAVIOR` and related Apple travel metadata | Client routing and travel-time suggestions around an event. | RFC 9073 can represent the associated locations, but the reviewed standards do not provide a general portable event travel-policy or travel-duration model. | **Potential candidate, not RFC-ready** | First establish independent use cases outside one CUA: fixed travel buffers, routing-derived duration, suggested departure, privacy controls, and route provider provenance. A shared model may be useful; today the Apple field is too UI-specific to register directly. |
| Work-hours/calendar policy: `X-MS-WKHRDAYS`, `X-MS-WKHRSTART`, `X-MS-WKHREND`, `X-PRIMARY-CALENDAR` | User working hours and client-specific calendar role. | RFC 7953 `VAVAILABILITY` can express repeating availability and unavailability; it does not claim to be a complete UI-preference profile. [4] | **Profile or mapping issue** | Specify mapping guidance from work-hour preferences to `VAVAILABILITY`; avoid turning every client preference into an exchange property. |
| Scheduling-control and reply fields: `X-MICROSOFT-DISALLOW-COUNTER`, `X-MICROSOFT-DONOTFORWARDMEETING`, `X-MS-OLK-*` response/sender fields | Invitation policy, counterproposal limits, local reply state, and client controls. | No simple generic equivalent in the reviewed iCalendar fields. These interact directly with iTIP and authorization policy. | **Potential candidate only after requirements work** | Separate portable scheduling policy from client UX. Any draft must define iTIP impacts, authorization, downgrade behavior, and recipient privacy; a property copied from Outlook is not sufficient. |
| Internal provenance and synchronization: `X-ENTOURAGE_UUID`, `X-KERIO-ORIGINAL-PRODID`, `X-BUSYMAC-LASTMODBY`, Apple suggestion opaque keys, Microsoft owner IDs/sequences | Internal reconciliation, product provenance, local state, opaque synchronization identifiers. | These values generally have no stable cross-product meaning and may leak implementation or personal information. | **Keep vendor/private** | Do not seek generic registration. Use existing `UID`, `SEQUENCE`, `DTSTAMP`, `LAST-MODIFIED`, and authenticated service APIs for portable behavior. |
| Timezone labeling: `X-LIC-LOCATION`, `X-WR-TIMEZONE` | Help a CUA resolve a timezone or impose a calendar-default zone. | Standard iCalendar uses `TZID` references plus `VTIMEZONE` or referenced-zone mechanisms; a floating calendar deliberately has no default zone. | **Profile or mapping issue** | Avoid emitting an extra default-zone field for floating feeds. Timezone-distribution work belongs with timezone standards, not a new ad hoc VCALENDAR property. |

## Prioritized Integration Roadmap

### Track 1 — Adopt Existing RFC Semantics Before Proposing New Fields

The highest-value work is not a new IETF draft. It is a set of cross-client test fixtures and recommended publication profiles for `STYLED-DESCRIPTION`, `REFRESH-INTERVAL`, `CONFERENCE`, `VLOCATION`, `STRUCTURED-DATA`, and RFC 9074 VALARM state. These fields already exist precisely because prior vendor practice revealed a gap. Their standards path is incomplete only in adoption, documentation, and round-trip support. [1] [2] [3]

A useful deliverable would be a public corpus with each event expressed in three forms: baseline RFC 5545, standards-extension form, and legacy-compatibility dual-emission form. A client matrix should record **import**, **render**, **export**, and **round-trip preservation** separately. Until that matrix is populated across independent implementations, it is inappropriate to call legacy fields superseded.

### Track 2 — Requirements Work for Per-VEVENT Busy Type

The strongest open candidate is the Outlook-style busy-status family. It has a clear multi-state model, a documented enterprise implementation, and a nearby but insufficient standardized vocabulary. A proposed draft should not simply register `X-MICROSOFT-CDO-BUSYSTATUS` under a neutral name. It must decide whether state is organizer-authored or recipient-local; define how FREE, TENTATIVE, BUSY, and OOF map to `TRANSP`, `FREEBUSY`, and RFC 7953 `BUSYTYPE`; specify privacy rules; and define behavior for scheduling messages and JSCalendar conversion. [4] [5] [8]

### Track 3 — Travel-Time Requirements, Not a Property Draft Yet

Travel advisory fields represent a real user need, but not yet a stable exchange model. A requirements document should collect examples from at least Apple, Google, Microsoft, CalDAV servers, and navigation providers. It must distinguish immutable publisher-provided buffer from a recipient-specific route prediction; the latter is inherently privacy-sensitive and changes with location, mode, and traffic. A generic property can be considered only after that separation is established.

### Track 4 — Deliberately Exclude Client-State Fields

Opaque keys, local suggestion state, UI window controls, internal owner IDs, and provider-specific meeting payloads should not be treated as defects in iCalendar. They are often necessary within a product, but their semantics are not portable. Their appropriate path is either private `X-` data, a vendor API, or a server-side capability—not an IANA property registration.

## Practical Path into IETF Work

CALEXT is the current IETF home for calendaring extensions. Its charter calls for backwards-compatible extensions, a robust mapping between iCalendar and JSCalendar, and an explicit review of any iTIP impact. It also explicitly contemplates documents describing vendor extensions that are common in the wild. [8]

A credible proposal should proceed in this order:

1. **Publish a problem statement.** Define the user outcome, the failure of existing RFC properties, and the minimum data needed to interoperate.
2. **Collect independent evidence.** Obtain import/export/round-trip examples from at least two distinct vendor or open-source ecosystems; popularity inside one CUA is insufficient.
3. **Write a neutral data model.** Do not reuse a vendor token or encode a vendor UI assumption in the standard property.
4. **Map the model.** Define iCalendar and JSCalendar representations and an unambiguous downgrade behavior for older clients.
5. **Specify scheduling and privacy effects.** Address iTIP delivery, attendee visibility, free-busy computation, authentication, data leakage, and tracking.
6. **Prototype and test.** Demonstrate at least two interoperable implementations against a shared vector suite before arguing that a new registration is warranted.
7. **Engage CALEXT.** Bring the problem statement and evidence to the CALEXT list/Zulip, then develop an Internet-Draft with the working group if there is consensus.

## Relevance to `cron_clock`

`cron_clock` is a public floating-time taxonomy calendar, not a scheduling, travel, location, alarm, or conferencing workload. The research supports a conservative header policy: retain standards-first calendar metadata and, where intended client evidence warrants it, matching legacy `X-WR-*` compatibility mirrors. None of the additional community extension families should be added merely to make the file look more complete. In particular, no timezone, all-day flag, busy-state, travel, or private synchronization extension adds semantic value to this calendar.

## References

[1]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[2]: https://www.rfc-editor.org/rfc/rfc9073.html "RFC 9073: Event Publishing Extensions to iCalendar"
[3]: https://www.rfc-editor.org/rfc/rfc9074.html "RFC 9074: VALARM Extensions for iCalendar"
[4]: https://www.rfc-editor.org/rfc/rfc7953.html "RFC 7953: Calendar Availability"
[5]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/cd68eae7-ed65-4dd3-8ea7-ad585c76c736 "Microsoft: X-MICROSOFT-CDO-BUSYSTATUS"
[6]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/d7f285da-9c7a-4597-803b-b74193c898a8 "Microsoft: X-ALT-DESC"
[7]: https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1fc7b244-ecd1-4d28-ac0c-2bb4df855a1f "Microsoft: X-PUBLISHED-TTL"
[8]: https://datatracker.ietf.org/wg/calext/about/ "IETF CALEXT Working Group Charter"
[9]: https://www.rfc-editor.org/rfc/rfc8607.html "RFC 8607: CalDAV Managed Attachments"
[10]: https://icscalendar.com/which-icalendar-fields-should-ics-calendar-support/ "ICS Calendar: Which iCalendar Fields Should ICS Calendar Support?"
