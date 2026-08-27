# Missing Elements and Internal Logic Review: `cron_clock`

This review excludes the known `REFRESH-INTERVAL:P3M` duration problem. It treats your latest 52-event calendar as the authoritative design and distinguishes **hard gaps**, **internal contradictions**, and **optional operating metadata**.

## Bottom Line

The hierarchy is largely present: millennium, century, decade, year, quarter, six senaries, generic and named months, week, generic and named days, three eight-hour phases, generic hour, seven named 204-minute rhythms, fractional-minute ticks, minute, and second. The strongest structural omissions are the missing `VALUE=DATE` declarations on civil/all-day starts, meaningful relationship values, unique IDs for the fractional ticks, valid source retrieval, and update-version metadata.

The two principal internal logic contradictions are that the **six 60-day senaries do not partition either a common or leap Gregorian year**, and that the **seven named 204-minute rhythms leave twelve minutes of each day outside the named-rhythm system**. Neither is necessarily wrong if you intend deliberately unmarked remainder time, but neither is a closed subdivision.

## Findings Requiring Repair or an Explicit Rule

| Finding | Why it matters | Exact evidence | Conservative resolution |
|---|---|---|---|
| Date-only `DTSTART` values lack `VALUE=DATE`. | `DTSTART` defaults to DATE-TIME; a bare eight-digit date is not a valid default DATE-TIME value. | The civil events use fields such as `DTSTART:18100101` rather than `DTSTART;VALUE=DATE:18100101`. | Add `;VALUE=DATE` to every all-day/civil boundary event. Do **not** add it to sub-day layers. [1] |
| Sub-day tick events have no time-of-day seed. | `HOUR`, `HALF`, `SCORE`, `DOZEN`, `MINUTE`, and `SECOND` use hourly/minutely/secondly frequency while their starts are date-only. The source needs to state whether these are all-day markers or floating time-grid events. | All six use `DTSTART:18100101`. | If they are clocks, use `DTSTART:18100101T000000`; if they are date markers, re-evaluate the sub-day FREQ. |
| Half, Score, and Dozen are the same VEVENT identity. | Three independent recurrence masters cannot share one UID. | Each uses `UID:dozen-vault_time@cron_clock`. | Assign three stable, distinct UIDs. [2] |
| The hierarchy has no actual links. | Every event has an empty `RELATED-TO:` property, so the intended ancestry is absent from the calendar data. | 52 empty relationship values. | Either remove placeholder properties or add `RELATED-TO;RELTYPE=PARENT:<parent-UID>` values once the parent model is chosen. [3] |
| The declared `SOURCE` does not retrieve the feed. | A subscriber cannot refresh from a URI that returns HTTP 404. | The current GitHub URL redirects and then returns 404. | Publish the actual `.ics` at a stable URL, preferably raw file content or a pages endpoint, and set `SOURCE;VALUE=URI:` to that URL. [4] |
| Calendar revision metadata is incomplete. | A published source can be uniquely named, but a consumer has no standard calendar-level revision time. | VCALENDAR has `UID` but no `LAST-MODIFIED`; the existing VCALENDAR `DTSTAMP` is not a VCALENDAR property. | Use `LAST-MODIFIED` at VCALENDAR level. `SEQUENCE` and `CREATED` remain optional for `PUBLISH`. [1] [5] |

## Closed-Subdivision Tests

### Senaries: not a full-year partition

Each senary lasts `P60D`, so the six entries represent 360 days. A common year has 365 days; a leap year has 366. The chosen starts distribute the remainder unevenly:

| Year type | Senary coverage | Uncovered dates | Interpretation required |
|---|---:|---|---|
| Common year | 360 days | Five one-day gaps: **May 1, July 1, August 31, October 31, December 31** | Are these intended named intercalary/remainder days? |
| Leap year | 360 days | Six one-day gaps: **March 1, May 1, July 1, August 31, October 31, December 31** | The extra leap-year gap is a different rule from the common-year pattern. |

> The present design is coherent if `S1`–`S6` mean six **fixed 60-day blocks**, with deliberately unnamed remainder days. It is inconsistent only if “senary” is meant to partition every Gregorian year completely.

### Named rhythms: not a full-day partition

The seven named events each last 204 minutes, totalling 1,428 minutes. A day contains 1,440 minutes, leaving **12 minutes** uncovered. The starts distribute those twelve minutes as eight gaps: 1 minute before Yan; then 2, 2, 1, 1, 2, and 2 minutes between successive rhythms; and 1 minute after Azer ends at 23:59.

> This is coherent if the named words are seven deliberately separated 204-minute observances. If they are meant as a seven-part day clock, define a named or generic **remainder/gap** layer, or change the rhythm arithmetic to close at 1,440 minutes.

### Phases: internally closed

Dawn, Noon, and Dusk each last eight hours and begin at 00:00, 08:00, and 16:00. They exactly cover 24 hours with no overlap or gap. This layer is internally consistent.

## Anchor and Taxonomy Findings

| Area | Finding | Consequence |
|---|---|---|
| Common-Monday epoch | `1810-01-01` is correctly a Monday in a Gregorian common year. | The Week, Day, named weekday, and phase anchors support your stated epoch rule. |
| Century anchor | `1601-01-01` is also a common Monday, but repeating it every 100 years produces 1701 Saturday, 1801 Thursday, 1901 Tuesday, then 2001 Monday. | A century recurrence cannot also represent a recurring common-Monday anchor. This is harmless if “CENTURY” only marks ordinal centuries; it conflicts only if you expect every century event to preserve epoch alignment. |
| Millennium anchor | `2001-01-01` is a common Monday. | It aligns with a 400-year Gregorian weekday cycle but is not linked to the century/decade hierarchy. |
| Layer representation | Quarters have four named objects rather than a generic Quarter; senaries have six named objects rather than generic Senary; weekdays have seven named objects plus generic Day. | No element is technically missing, but this is an intentional **mixed model**: named parallel markers at some layers and a generic cadence at others. Decide whether this asymmetry is a feature. |
| Category model | Millennium, Century, Decade, and Year all use `CATEGORIES:year`; named rhythms and generic Hour all use `CATEGORIES:hour`. | Fine for visual grouping, but category alone cannot reconstruct the hierarchy. Relationships or a new `CONCEPT`/`REFID` model would be needed for machine-readable topology. [3] |
| Blank colors | Most civil marker events contain `COLOR:` with no value. | `COLOR` is optional; empty values are neither useful metadata nor CSS color names. Omit them or assign colors deliberately. [4] |
| Priority system | Values are consistently layered from 9 (large scale) through 1 (seconds). | This is internally consistent as a visual sort convention, though clients may not use PRIORITY for z-order. |

## Optional but Worth Adding

`CREATED`, VEVENT `LAST-MODIFIED`, and `SEQUENCE` are not mandatory for a `PUBLISH` feed; add them only if you want explicit content-version history. A calendar-level `URL` could provide a human-readable canonical page, while `SOURCE` should remain the machine-refresh endpoint. If the taxonomy will be used programmatically, RFC 9253’s `CONCEPT` or `REFID` is more expressive than free-text categories.[3] [4] [5]

## Recommended Order of Decisions

First decide whether **senary remainder days** and **twelve named-rhythm gaps** are intentional. Second, decide whether the clock layers are true floating DATE-TIME grids. Then define the parent graph and stable raw source URL. Those four decisions make the file’s semantics complete; the remaining changes are mechanical serialization and metadata work.

## References

[1]: https://www.rfc-editor.org/rfc/rfc5545.html "RFC 5545, Sections 3.8.2.4 and 3.6.1"
[2]: https://www.rfc-editor.org/rfc/rfc5545.html "RFC 5545, Section 3.8.4.7"
[3]: https://www.rfc-editor.org/rfc/rfc9253.html "RFC 9253: Support for iCalendar Relationships"
[4]: https://www.rfc-editor.org/rfc/rfc7986.html "RFC 7986: New Properties for iCalendar"
[5]: https://www.rfc-editor.org/rfc/rfc5546.html "RFC 5546, Section 3.2.1: PUBLISH"
