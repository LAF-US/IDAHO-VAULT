# cron_clock-rfc — the iCalendar standards suite

Upstream reference texts for `cron_clock.ics`, web-clipped from their
rfc-editor.org info pages (clipped 2026-08-18, PR #981) as root-flat
vault notes, matching the frontmatter convention of every other
clipping in this vault (`title`/`source`/`author`/`published`/`created`/
`description`/`tags: [clippings]`). Each note's body is the RFC's
plaintext, fenced verbatim, exactly as the info page renders it.

The roster follows the RFC Editor's own chain, as Logan traced it:
RFC 2445's info page points to RFC 5545 (which obsoletes it), and
RFC 5545's page points to the RFCs that update it.

## The chain

| note | RFC | title | relation |
| --- | --- | --- | --- |
| [[- RFC Editor - RFC 2445 - Internet Calendaring and Scheduling Core Object Specification (iCalendar)\|RFC 2445]] | 2445 (1998) | iCalendar (original) | obsoleted by 5545 |
| [[- RFC Editor - RFC 5545 - Internet Calendaring and Scheduling Core Object Specification (iCalendar)\|RFC 5545]] | 5545 (2009) | iCalendar core | the operative spec |
| [[- RFC Editor - RFC 5546 - iCalendar Transport-Independent Interoperability Protocol (iTIP)\|RFC 5546]] | 5546 (2009) | iTIP scheduling | obsoletes 2446; updates 5545 |
| [[- RFC Editor - RFC 6868 - Parameter Value Encoding in iCalendar and vCard\|RFC 6868]] | 6868 (2013) | parameter value encoding | updates 5545, 6321, 6350, 6351 |
| [[- RFC Editor - RFC 7529 - Non-Gregorian Recurrence Rules in the Internet Calendaring and Scheduling Core Object Specification (iCalendar)\|RFC 7529]] | 7529 (2015) | RSCALE / SKIP (non-Gregorian recurrence) | updates 5545, 6321, 7265 |
| [[- RFC Editor - RFC 7953 - Calendar Availability\|RFC 7953]] | 7953 (2016) | VAVAILABILITY | updates 4791, 5545, 6638 |
| [[- RFC Editor - RFC 7986 - New Properties for iCalendar\|RFC 7986]] | 7986 (2016) | new properties (NAME, COLOR, calendar-level UID…) | updates 5545 |
| [[- RFC Editor - RFC 9073 - Event Publishing Extensions to iCalendar\|RFC 9073]] | 9073 (2021) | event publishing extensions | updates 5545 |
| [[- RFC Editor - RFC 9074 - 'VALARM' Extensions for iCalendar\|RFC 9074]] | 9074 (2021) | VALARM extensions | updates 5545 |
| [[- RFC Editor - RFC 9253 - Support for iCalendar Relationships\|RFC 9253]] | 9253 (2022) | relationships (LINK, CONCEPT, REFID, RELATED-TO) | updates 5545 |

### Bibliographic fields

Pulled from each file's own header block, verbatim.

| RFC | Author(s) | Organization(s) | Date | Category | ISSN | Status page |
| --- | --- | --- | --- | --- | --- | --- |
| 2445 | F. Dawson; D. Stenerson | Lotus; Microsoft | November 1998 | Standards Track | — (predates the ISSN series) | [info/rfc2445](https://www.rfc-editor.org/info/rfc2445/) |
| 5545 | B. Desruisseaux, Ed. | Oracle | September 2009 | Standards Track | — | [info/rfc5545](https://www.rfc-editor.org/info/rfc5545/) |
| 5546 | C. Daboo, Ed. | Apple Inc. | December 2009 | Standards Track | — | [info/rfc5546](https://www.rfc-editor.org/info/rfc5546/) |
| 6868 | C. Daboo | Apple | February 2013 | Standards Track | 2070-1721 | [info/rfc6868](https://www.rfc-editor.org/info/rfc6868/) |
| 7529 | C. Daboo; G. Yakushev | Apple Inc.; Google Inc. | May 2015 | Standards Track | 2070-1721 | [info/rfc7529](https://www.rfc-editor.org/info/rfc7529/) |
| 7953 | C. Daboo; M. Douglass | Apple; Spherical Cow Group | August 2016 | Standards Track | 2070-1721 | [info/rfc7953](https://www.rfc-editor.org/info/rfc7953/) |
| 7986 | C. Daboo | Apple Inc. | October 2016 | Standards Track | 2070-1721 | [info/rfc7986](https://www.rfc-editor.org/info/rfc7986/) |
| 9073 | M. Douglass | Bedework | August 2021 | Standards Track | 2070-1721 | [info/rfc9073](https://www.rfc-editor.org/info/rfc9073/) |
| 9074 | C. Daboo; K. Murchison, Ed. | Apple; Fastmail | August 2021 | Standards Track | 2070-1721 | [info/rfc9074](https://www.rfc-editor.org/info/rfc9074/) |
| 9253 | M. Douglass | Bedework | August 2022 | Standards Track | 2070-1721 | [info/rfc9253](https://www.rfc-editor.org/info/rfc9253/) |

## Adjacent texts (outside the update chain)

Pulled during the same reading; kept for reference. None of these three
obsoletes or updates another document in this suite.

| note | RFC | title |
| --- | --- | --- |
| [[- RFC Editor - RFC 6047 - iCalendar Message-Based Interoperability Protocol (iMIP)\|RFC 6047]] | 6047 (2010) | iMIP (iCalendar over email) |
| [[- RFC Editor - RFC 7808 - Time Zone Data Distribution Service\|RFC 7808]] | 7808 (2016) | tzdist (time zone data distribution) |
| [[- RFC Editor - RFC 8984 - JSCalendar - A JSON Representation of Calendar Data\|RFC 8984]] | 8984 (2021) | JSCalendar (the JSON successor format) |

### Bibliographic fields

| RFC | Author(s) | Organization(s) | Date | Category | ISSN | Obsoletes | Status page |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6047 | A. Melnikov, Ed. | Isode Ltd | December 2010 | Standards Track | 2070-1721 | 2447 | [info/rfc6047](https://www.rfc-editor.org/info/rfc6047/) |
| 7808 | M. Douglass; C. Daboo | Spherical Cow Group; Apple | March 2016 | Standards Track | 2070-1721 | — | [info/rfc7808](https://www.rfc-editor.org/info/rfc7808/) |
| 8984 | N. Jenkins; R. Stepanek | Fastmail | July 2021 | Standards Track | 2070-1721 | — | [info/rfc8984](https://www.rfc-editor.org/info/rfc8984/) |

## Notes

- Each note's `source` frontmatter field is the exact info-page URL
  Logan gave; the RFC Editor remains the source of truth there.
- Clipped body content is the RFC's plaintext rendering (what the info
  page displays in its content block), reproduced verbatim inside a
  fenced code block to preserve fixed-width formatting — indentation,
  ABNF grammar, and the original page-break footers.
- Four of the thirteen (RFC 8984, 9073, 9074, 9253) begin their fenced
  text with a UTF-8 BOM — that is how rfc-editor.org serves them, kept
  byte-for-byte.
- `author` and `published` in each note's frontmatter are filled from
  the RFC's own front-matter block (verified against the fenced text),
  not from an HTML `<meta>` tag — the info pages don't expose one.
