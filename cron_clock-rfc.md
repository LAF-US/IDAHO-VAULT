# cron_clock-rfc — the iCalendar standards suite

Upstream reference texts for `cron_clock.ics`, saved verbatim from
rfc-editor.org (fetched 2026-08-18, PR #981) as root-flat siblings of
this note, per vault structure: the root carries flat files; new
top-level directories outside `!/` and the dotfolders are invalid.

The roster follows the RFC Editor's own chain, as Logan traced it:
RFC 2445's info page points to RFC 5545 (which obsoletes it), and
RFC 5545's page points to the RFCs that update it.

## The chain

| file | RFC | title | relation |
| --- | --- | --- | --- |
| `rfc2445.txt` | 2445 (1998) | iCalendar (original) | obsoleted by 5545 |
| `rfc5545.txt` | 5545 (2009) | iCalendar core | the operative spec |
| `rfc5546.txt` | 5546 (2009) | iTIP scheduling | obsoletes 2446; updates 5545 |
| `rfc6868.txt` | 6868 (2013) | parameter value encoding | updates 5545, 6321, 6350, 6351 |
| `rfc7529.txt` | 7529 (2015) | RSCALE / SKIP (non-Gregorian recurrence) | updates 5545, 6321, 7265 |
| `rfc7953.txt` | 7953 (2016) | VAVAILABILITY | updates 4791, 5545, 6638 |
| `rfc7986.txt` | 7986 (2016) | new properties (NAME, COLOR, calendar-level UID…) | updates 5545 |
| `rfc9073.txt` | 9073 (2021) | event publishing extensions | updates 5545 |
| `rfc9074.txt` | 9074 (2021) | VALARM extensions | updates 5545 |
| `rfc9253.txt` | 9253 (2022) | relationships (LINK, CONCEPT, REFID, RELATED-TO) | updates 5545 |

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

| file | RFC | title |
| --- | --- | --- |
| `rfc6047.txt` | 6047 (2010) | iMIP (iCalendar over email) |
| `rfc7808.txt` | 7808 (2016) | tzdist (time zone data distribution) |
| `rfc8984.txt` | 8984 (2021) | JSCalendar (the JSON successor format) |

### Bibliographic fields

| RFC | Author(s) | Organization(s) | Date | Category | ISSN | Obsoletes | Status page |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6047 | A. Melnikov, Ed. | Isode Ltd | December 2010 | Standards Track | 2070-1721 | 2447 | [info/rfc6047](https://www.rfc-editor.org/info/rfc6047/) |
| 7808 | M. Douglass; C. Daboo | Spherical Cow Group; Apple | March 2016 | Standards Track | 2070-1721 | — | [info/rfc7808](https://www.rfc-editor.org/info/rfc7808/) |
| 8984 | N. Jenkins; R. Stepanek | Fastmail | July 2021 | Standards Track | 2070-1721 | — | [info/rfc8984](https://www.rfc-editor.org/info/rfc8984/) |

## Notes

- These are plain-text mirrors for offline grounding; the RFC Editor
  remains the source of truth at `https://www.rfc-editor.org/info/rfc<n>/`.
- The four newest files (`rfc8984.txt`, `rfc9073.txt`, `rfc9074.txt`,
  `rfc9253.txt`) begin with a UTF-8 BOM — that is how rfc-editor.org
  serves them, and the mirrors keep the bytes verbatim.
