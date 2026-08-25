# Non-RFC iCalendar Fields vs. a Full JSCalendar Move

**Decision context:** `cron_clock` is a public, floating-local-time calendar with intentional silent intervals, layered recurrence semantics, and a need to remain useful in conventional calendar clients.

## Bottom line

A **full immediate cutover to JSCalendar is not justified** for a public calendar subscription. JSCalendar 2.0 is technically cleaner and increasingly credible, but the current deployment evidence still describes client support as emerging; the current draft is also not yet a published RFC.[1] [2]

The strongest strategy is a **canonical-model, dual-publication approach**. Keep a strict, broadly consumable `.ics` feed as the compatibility surface, retaining only those legacy fields that demonstrably preserve intended behaviour in deployed importers. Publish a parallel JSCalendar 2.0 representation for controlled consumers and future adopters. Neither serialization should be manually authored; both should be generated from one neutral calendar model and validated against explicit invariants.

> **The real choice is not “old format versus new format.” It is whether the calendar has one semantic source of truth and two accountable serializations.**

## Case for retaining selected non-RFC fields

The RFC status of a field and its deployed utility are distinct. A non-RFC field has a reasonable case for retention when it carries presentation or identity information that a material installed client population still consumes, when it is safely ignorable elsewhere, and when its standard counterpart is emitted with exactly the same value.

| Field | Argument for retaining it | Constraint | Position for `cron_clock` |
|---|---|---|---|
| `X-WR-CALNAME` | Microsoft continues to document import/export handling. A current Python iCalendar library added dual emission after a maintainer reported that Google Calendar uses the legacy field. This is evidence of compatibility value, not a universal interoperability guarantee.[3] [4] | Must exactly mirror RFC 7986 `NAME`; test equality during generation. | **Retain as a mirror.** |
| `X-WR-CALDESC` | It can preserve a calendar-level description for importers that recognise it. | Emit standard calendar-level `DESCRIPTION` first; do not create diverging prose. | **Retain only if a real calendar-level description is published.** |
| `X-WR-RELCALID` | Historical identity continuity can matter to import/export paths. | Mirror the stable VCALENDAR `UID`; never use it as a second identity authority. | **Retain as a mirror while testing legacy import paths.** |
| `X-WR-TIMEZONE` | Some legacy exports use it as a presentation convenience. | It implies a default zone and conflicts with this calendar’s intentional floating-local-time model. | **Do not emit.** |
| `X-WR-ALARMUID` / `X-WR-ALARMID` | Relevant only to old alarm persistence paths. | No alarms exist here; the two spellings are not proven interchangeable. | **Do not emit.** |

The principal risk of keeping legacy fields is not that they are nonstandard; iCalendar processors are designed to ignore unknown `X-` extensions. The material risk is **duplicated semantic authority**. If `NAME` and `X-WR-CALNAME`, or `UID` and `X-WR-RELCALID`, drift apart, the document becomes internally ambiguous. The remedy is generation-time equivalence checks and a stated precedence rule: **standard value first; legacy mirror second; never independent edits.**

## Case for a full JSCalendar-native implementation

A JSCalendar-native model has strong engineering merits. JSCalendar 2.0 is designed to reduce ambiguity, uses ordinary JSON structures, explicitly models floating local date-times, and makes structured extensions and validation less fragile than folded iCalendar content lines. Its design specifically acknowledges that iCalendar’s local/UTC forms, time-zone embedding, recurrence semantics, and line serialization lead to interoperability mistakes.[1]

The conversion draft has another strategic advantage: it defines a route for preserving unknown or unmatched elements during iCalendar↔JSCalendar conversion. That makes a JSON-native internal model viable without forcing an immediate loss of the current feed’s legacy compatibility data.[2]

A full JSCalendar move is appropriate when all material consumers are controlled clients or documented API integrators; when recurrence and structural metadata need reliable machine manipulation; when a JMAP-capable service operates the calendar; and when the publisher can reject or update incompatible clients. It is especially attractive for an authoring, validation, or archival API around `cron_clock`.

## Arguments against an immediate complete cutover

A JSON format does not itself create a public subscription ecosystem. Existing public calendar workflows use `.ics` files, `webcal:` links, and long-established iCalendar imports. The current standards situation remains transitional: JSCalendar 2.0 is still a draft in IESG evaluation, its iCalendar conversion companion remains in working-group last call, and JMAP Calendars is tied to that work.[1] [2] [5]

Current implementation evidence reinforces the caution. Stalwart described itself in late 2025 as the first complete JMAP server for the new collaboration protocols and said client support was still emerging, naming active implementers rather than a broad consumer calendar-client base.[5] That is promising adoption evidence, but it is also evidence that a `.json` endpoint alone cannot yet substitute for a public `.ics` subscription.

A cutover also would not solve every modelling issue in this project. JSCalendar’s duration grammar still covers weeks, days, hours, minutes, and seconds—not civil calendar months or years. Moving formats does not make `P1Y`, `P100Y`, or `P3M` valid span values. Likewise, the demon/grace days and non-period minutes remain intentional absence-of-event semantics rather than a standard primitive in either format.[1] [6]

## The recommended architecture

| Layer | Responsibility | Recommended representation |
|---|---|---|
| Canonical calendar model | Stores the layer hierarchy, anchors, palette rules, silent intervals, labels, and relationships once. | A versioned neutral data model under source control, not a hand-edited `.ics` or `.json` file. |
| Compatibility feed | Serves conventional subscription/import clients. | Standards-valid `.ics` with RFC 5545/7986/9073 fields and tightly bounded legacy mirrors (`X-WR-CALNAME`, possibly `X-WR-CALDESC` and `X-WR-RELCALID`). |
| Modern structured feed | Serves controlled tools, validators, APIs, and early adopters. | JSCalendar 2.0 document identified by its exact draft/RFC version. |
| Manifest and tests | Declares format versions, endpoints, semantic invariants, and conversion loss rules. | Human-readable metadata plus automated round-trip and equivalence tests. |

This approach permits JSCalendar to become the **authoring and operational format** without asking ordinary calendar users to adopt it first. The `.ics` feed remains a deliberately constrained projection: it should carry all behaviour necessary for interoperable calendar rendering, while project-specific lore or internal generation rules live in the canonical model and documentation rather than uncontrolled `X-` fields.

## Migration guardrails

A format migration can be advanced in stages. First, build deterministic generators for both outputs and compare all ordinary event identity, start, recurrence, duration, and public labels. Second, mark the JSCalendar endpoint as beta or developer-oriented rather than changing the public subscription URL. Third, test the `.ics` feed in the target client matrix and test the JSCalendar output in independent implementations. Fourth, only reconsider a JSCalendar-first public endpoint after JSCalendar 2.0 and the conversion specification are published RFCs and demonstrated consumer-client subscription support exists.

The following decision gate is conservative but practical:

| Condition | Needed before ending `.ics` as the primary public feed? |
|---|---|
| JSCalendar 2.0 and iCalendar conversion specifications reach RFC status | Yes. |
| At least two independent maintained consumer/calendar implementations render the calendar correctly, including floating local time and recurrence | Yes. |
| At least one ordinary hosted calendar workflow can subscribe to or import the JSCalendar endpoint without custom tooling | Yes. |
| Legacy X-WR data can be dropped without an identified target-client regression | Yes. |
| Every `cron_clock` semantic has a tested mapping or documented intentional loss rule | Yes. |

Until those gates are met, a `.ics` compatibility feed plus a JSCalendar companion is the least risky path. It preserves reach today, collects evidence for future adoption, and avoids locking the project’s semantic model into either 2009-era iCalendar limitations or an evolving 2026 draft.

## References

[1] [IETF, *JSCalendar 2.0*, draft-ietf-calext-jscalendarbis-18](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendarbis-18)

[2] [IETF, *JSCalendar: Converting from and to iCalendar*, draft-ietf-calext-jscalendar-icalendar-25](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendar-icalendar-25)

[3] [Microsoft, *MS-OXCICAL: Property X-WR-CALNAME*](https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxcical/1da58449-b97e-46bd-b018-a1ce576f3e6d)

[4] [collective/icalendar, *Getting out an ical with NAME and X-WR-CALNAME*, issue #918](https://github.com/collective/icalendar/issues/918)

[5] [Stalwart, *JMAP for Calendars, Contacts and Files now in Stalwart*](https://stalw.art/blog/jmap-collaboration/)

[6] [IETF, *iCalendar Format Extensions for JSCalendar*, draft-ietf-calext-icalendar-jscalendar-extensions-06](https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-jscalendar-extensions-06)
