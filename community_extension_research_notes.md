# Community Extension Research Notes

## Existing Paths from Community Practice to RFCs

RFC 7986 explicitly describes its purpose as collecting ad hoc vendor extensions into registered standard variants with defined semantics. It provides standardized VCALENDAR display metadata and refresh mechanisms, including `REFRESH-INTERVAL;VALUE=DURATION`, `SOURCE;VALUE=URI`, `COLOR`, `IMAGE`, and `CONFERENCE`.

Microsoft documents `X-PUBLISHED-TTL` as an unregistered duration-based publication refresh hint, recommends it be ignored on import, and conditionally emits it on export. This makes it a good example of community practice whose standardized direction is RFC 7986 `REFRESH-INTERVAL`, but whose live client support cannot be assumed.

RFC 9073 states that vendors had relied on nonstandard properties for rich text and metadata. It standardizes `STYLED-DESCRIPTION` for rich text (including HTML), plus `STRUCTURED-DATA`, `VLOCATION`, `VRESOURCE`, `PARTICIPANT`, and typed metadata. This provides an intentional standards path for the most common Apple/Google/Microsoft travel, location, resource, and rich-description extensions.

RFC 8607 is an important counterexample: it documents a deployed CalDAV managed-attachment extension as Informational because its existing design conflicted with HTTP best practices. Widespread implementation alone did not make it appropriate for Standards Track publication.

Sources:

* https://www.rfc-editor.org/rfc/rfc7986.html
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1fc7b244-ecd1-4d28-ac0c-2bb4df855a1f
* https://www.rfc-editor.org/rfc/rfc9073.html
* https://www.rfc-editor.org/rfc/rfc8607.html

## Standards Integration Path

The active IETF CALEXT working group is the appropriate standards venue. Its current charter specifically includes evaluating new calendaring extensions where demand exists and generating documents for existing vendor extensions in common usage. The charter requires backwards compatibility, a robust iCalendar/JSCalendar mapping for calendar extensions, and examination of iTIP impact.

Microsoft’s current iCalendar conversion documentation demonstrates that its extension inventory is broad and mixed: it includes all-day flags, busy-status fields, scheduling control fields, conference fields, and work-hours metadata. The documented `X-MICROSOFT-CDO-BUSYSTATUS` maps four values (FREE, TENTATIVE, BUSY, OOF) to a Microsoft busy-status model. This is a genuine semantic capability gap for VEVENT: RFC 5545 TRANSP is binary, whereas RFC 7953 BUSYTYPE has a richer vocabulary but applies to availability components, not a general VEVENT busy-state field.

Sources:

* https://datatracker.ietf.org/wg/calext/about/
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/cd68eae7-ed65-4dd3-8ea7-ad585c76c736
* https://www.rfc-editor.org/rfc/rfc7953.html

## Field Inventory and Semantic Gaps

A 2023 ICS Calendar survey of seven production feeds found a broad set of vendor fields spanning Apple (`X-APPLE-*`), Google (`X-GOOGLE-*`), Microsoft (`X-MICROSOFT-*` and `X-MS-OLK-*`), Entourage, Kerio, libical, and X-WR conventions. The survey is ecosystem evidence rather than standards authority, but it provides a useful taxonomy of fields encountered in imports.

Microsoft’s X-ALT-DESC documentation specifies an HTML alternative description, imported when `FMTTYPE=text/HTML` and exported from compressed RTF as HTML. RFC 9073 provides the more general `STYLED-DESCRIPTION` property with media-type support and rich-text semantics. This is a strong semantic match, but current support overlap must be demonstrated before retiring the legacy property.

Microsoft’s X-MICROSOFT-CDO-BUSYSTATUS maps FREE, TENTATIVE, BUSY, and OOF to its busy-status model. RFC 7953 has BUSYTYPE values BUSY, BUSY-UNAVAILABLE, and BUSY-TENTATIVE, but only for VAVAILABILITY. This leaves a plausible standards question for per-VEVENT busy-state semantics, which must be distinguished carefully from RFC 5545 TRANSP and evaluated for iTIP and JSCalendar effects.

Sources:

* https://icscalendar.com/which-icalendar-fields-should-ics-calendar-support/
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/d7f285da-9c7a-4597-803b-b74193c898a8
* https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/cd68eae7-ed65-4dd3-8ea7-ad585c76c736
* https://www.rfc-editor.org/rfc/rfc9073.html
* https://www.rfc-editor.org/rfc/rfc7953.html
