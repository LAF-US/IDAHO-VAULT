# Confirmed Senary Rule

> **A Gregorian year contains six fixed 60-day senaries. The five boundaries within that year—S1→S2, S2→S3, S3→S4, S4→S5, and S5→S6—each contain at least one deliberate demon/grace day. The S6→next-year-S1 transition is the civil year boundary, not a senary boundary.**

This is the confirmed **non-circular** interpretation. It preserves six equal 60-day senaries and distributes the five ordinary common-year remainder days between them, rather than grouping them at year end.

## Canonical Starts and Spans

| Senary | DTSTART | Inclusive span in a common year | Internal grace day before next senary |
|---|---|---|---|
| S1 | January 1 | January 1–March 1 | March 2 |
| S2 | March 3 | March 3–May 1 | May 2 |
| S3 | May 3 | May 3–July 1 | July 2 |
| S4 | July 3 | July 3–August 31 | September 1 |
| S5 | September 2 | September 2–October 31 | November 1 |
| S6 | November 2 | November 2–December 31 | None: January 1 begins next year’s S1 |

The calendar therefore uses `6 × 60 + 5 = 365` days in a common year. The annual wrap is intentionally contiguous and falls outside the senary-boundary rule.

## Leap-Year Grace

The same civil start dates remain fixed in leap years. S1 then runs January 1–February 29, while S2 still begins March 3. The first internal boundary therefore contains a **two-day grace** on March 1–2. Each of the remaining four internal boundaries retains its one-day grace.

| Year type | Internal demon/grace allocation |
|---|---|
| Common Gregorian year | March 2; May 2; July 2; September 1; November 1 |
| Leap Gregorian year | March 1–2; May 2; July 2; September 1; November 1 |

## iCalendar Implementation Rule

The six senary VEVENTs should retain a `P60D` duration and use fixed annual DATE starts: January 1, March 3, May 3, July 3, September 2, and November 2. Every civil start must declare `VALUE=DATE`.

## Silent Interstices

The demon/grace days are **deliberate visual silence**, not omitted data and not named VEVENTs. They follow the same design rule as the non-period minutes between the seven named 204-minute rhythms: a meaningful unrepresented interval remains visible through the absence of a span. Future repairs must preserve these spaces, must not fill them with generic demon/remainder events, and must not treat non-closure as an error.
