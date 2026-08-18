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
| `rfc5546.txt` | 5546 (2009) | iTIP scheduling | companion to 5545 |
| `rfc6868.txt` | 6868 (2013) | parameter value encoding | updates 5545 |
| `rfc7529.txt` | 7529 (2015) | RSCALE / SKIP (non-Gregorian recurrence) | updates 5545 |
| `rfc7953.txt` | 7953 (2016) | VAVAILABILITY | updates 5545 |
| `rfc7986.txt` | 7986 (2016) | new properties (NAME, COLOR, calendar-level UID…) | updates 5545 |
| `rfc9073.txt` | 9073 (2021) | event publishing extensions | updates 5545 |
| `rfc9074.txt` | 9074 (2021) | VALARM extensions | updates 5545 |
| `rfc9253.txt` | 9253 (2022) | relationships (LINK, CONCEPT, REFID, RELATED-TO) | updates 5545 |

## Adjacent texts (outside the update chain)

Pulled during the same reading; kept for reference:

| file | RFC | title |
| --- | --- | --- |
| `rfc6047.txt` | 6047 (2010) | iMIP (iCalendar over email) |
| `rfc7808.txt` | 7808 (2016) | tzdist (time zone data distribution) |
| `rfc8984.txt` | 8984 (2021) | JSCalendar (the JSON successor format) |

## Notes

- These are plain-text mirrors for offline grounding; the RFC Editor
  remains the source of truth at `https://www.rfc-editor.org/info/rfc<n>/`.
- The four newest files (`rfc8984.txt`, `rfc9073.txt`, `rfc9074.txt`,
  `rfc9253.txt`) begin with a UTF-8 BOM — that is how rfc-editor.org
  serves them, and the mirrors keep the bytes verbatim.
