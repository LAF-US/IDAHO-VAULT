# `cron_clock.py` Mapping Design

## 1. Purpose and direction of authority

`cron_clock.py` is the sole authored definition of the chronology. It is **not** a mutable copy of an `.ics` file, a JSCalendar file, or an engine tick counter. It stores the declarative rules that make those outputs reproducible.

The source model begins with the finest rendered layer and builds outward. It accepts no universal engine `tick = 0`; a game may apply its own tick-to-civil-instant adapter before asking the chronology to interpret time. The common Monday `1810-01-01` is a calendar anchor used for layer alignment, not a simulation-clock origin.

```text
external game clock / imported local civil instant
                    │
                    ▼
            cron_clock.py model
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  iCalendar renderer      JSCalendar renderer
  cron_clock.ics          cron_clock.jscalendar.json
```

The renderer never becomes authoritative. A consumer may discard unknown extensions or flatten a rich recurrence, but the next generated output must always return to the same source semantics.

## 2. Canonical data model

The model should be ordinary immutable Python data, without format-shaped names such as `RRULE`, `VEVENT`, `@type`, or `timeZone` in its core classes.

```python
@dataclass(frozen=True)
class ChronologySpec:
    identity: CalendarIdentity
    civil: CivilPolicy
    anchor: CalendarAnchor
    layers: tuple[LayerSpec, ...]       # strictly bottom-up
    silences: tuple[SilenceSpec, ...]
    palette: PalettePolicy
    compatibility: CompatibilityPolicy
    revision: RevisionPolicy

@dataclass(frozen=True)
class LayerSpec:
    id: str                             # e.g. "second", "rhythm_azer", "senary_1"
    rank: int                           # unique, bottom-up ordering key
    label: str
    category: str
    kind: LayerKind                     # clock, ritual, civil, macro
    occurrence: OccurrenceRule
    coverage: CoverageRule
    display: DisplayPolicy
    projection: ProjectionPolicy

@dataclass(frozen=True)
class SilenceSpec:
    id: str
    scope: str                          # named rhythm, senary, etc.
    predicate: OccurrenceRule
    meaning: str                        # intentional unrepresented interval
```

`OccurrenceRule` is the meaningful core. It answers **when an occurrence begins** using calendar arithmetic, not a preselected output grammar. It needs only a small, explicit family of variants:

| Rule variant | Example use | Canonical meaning |
|---|---|---|
| `FixedClockRule` | Second, minute, hour, phase boundaries | A fixed amount of sub-day elapsed time from a local civil-day boundary. |
| `WeekdayRule` | Seven named weekdays | A weekday position inside the proleptic Gregorian week. |
| `MonthDayRule` | Named months, quarters | A Gregorian month/day boundary. |
| `AnnualRule` | Year marker | A Gregorian annual boundary. |
| `IntervalDayRule` | 60-day senaries, 204-minute named rhythms | A declared interval from a named anchor, with explicit calendar or fixed-duration semantics. |
| `CompositeRule` | Leap-sensitive ritual rules | A composition of ordinary predicates; never implicit hidden arithmetic. |

`CoverageRule` independently describes the semantic extent of an occurrence. That separation prevents the previous invalid-duration problem. An occurrence can be a **marker**, a fixed physical span, a civil span ending at the next calculated civil boundary, or a non-emitted reference layer.

```python
class CoverageKind(Enum):
    MARKER = "marker"                  # boundary only
    FIXED = "fixed"                    # exact elapsed duration
    NEXT_BOUNDARY = "next_boundary"    # civil span, such as one month or year
    NONE = "none"                      # defined internally but not exported
```

## 3. Semantic invariants

The generator must reject a model that violates any of these rules before a renderer runs.

| Invariant | Meaning |
|---|---|
| **One semantic authority** | Every title, category, color, identity, anchor, and silence rule exists once in `cron_clock.py`. |
| **No implicit tick epoch** | Neither a rendered event nor the canonical model assumes what a game’s integer tick zero means. |
| **Floating local time** | Time-specific canonical occurrences have no zone identifier and no UTC conversion. UTC is permitted only for revision/audit metadata where the target standard requires it. |
| **Gregorian civil basis** | The civil transform is proleptic Gregorian and the 1810 common-Monday anchor must evaluate correctly. |
| **Silence is data** | Demon/grace days and non-period minutes are specified as intentional non-coverage, not accidental holes and not placeholder events. |
| **Palette is declarative** | Seven-item groups use ordered ROYGBIV; year-family layers are white; the second layer is black; all other colors remain unset unless explicitly decided. |
| **No invented duration** | A civil month/year/century/millennium band cannot be rendered as a fixed ISO 8601 elapsed `P1M`, `P1Y`, `P100Y`, or `P1000Y` duration. |
| **Stable identity** | An occurrence’s logical identity is derived from layer id plus the canonical start/recurrence identity, never from a serial export order. |
| **Projection must declare loss** | If a target cannot represent a semantic distinction, its renderer must choose `marker`, bounded materialization, safe extension, or omission explicitly. |

## 4. Why coverage and recurrence must remain separate

The old handwritten source tried to give civil bands an iCalendar `DURATION` corresponding to a month, year, century, or millennium. That approach is not portable because the format’s duration syntax expresses fixed elapsed time, not calendar-relative civil spans.

The canonical model instead says, for example:

```text
year occurrence begins at 1810-01-01
coverage ends at the next Gregorian year boundary
```

The iCalendar and JSCalendar renderers then have a deliberate choice. A public unbounded feed may emit a one-day marker for each annual boundary. A bounded publication window may materialize each year as an individual band ending on the next `January 1`. Neither renderer may silently substitute `P1Y`.

## 5. Source-level configuration shape

At the top of `cron_clock.py`, human-editable configuration should be visibly separated from pure mapping code.

```python
SPEC = ChronologySpec(
    identity=CalendarIdentity(
        uid="cron_clock@laf.us",
        name="cron_clock",
        description="A floating-local Gregorian clock and ritual layer map.",
    ),
    civil=CivilPolicy(scale="GREGORIAN", floating_local=True),
    anchor=CalendarAnchor(date="1810-01-01", rationale="common Monday"),
    layers=(
        SECOND,
        MINUTE,
        HOUR,
        NAMED_RHYTHMS,
        PHASES,
        DAY,
        WEEK,
        WEEKDAYS,
        MONTHS,
        QUARTERS,
        YEAR,
        SENARIES,
        DECADE,
        CENTURY,
        MILLENNIUM,
    ),
    silences=(NON_PERIOD_MINUTES, DEMON_GRACE_DAYS),
    palette=PALETTE,
    compatibility=COMPATIBILITY,
    revision=REVISION,
)
```

This ordering is a declaration of **conceptual construction**, not an instruction that every output must list events in that order. Renderers may sort according to their target’s operational needs, while the manifest records the canonical rank.

## 6. Open mapping decisions

The following questions belong to output-adapter design, not to the neutral chronology itself:

1. Which layers are published as unbounded markers versus bounded, fully materialized civil bands?
2. What bounded materialization horizon is appropriate for human calendar clients?
3. Which compatibility mirrors are retained after target-client testing?
4. Does `cron_clock.json` name the neutral engine projection, with a separate `cron_clock.jscalendar.json` export, or is JSCalendar the only JSON artifact?
5. Which target-specific extensions are permissible if standard fields cannot preserve a public display choice?

The next sections define those choices for iCalendar and JSCalendar without contaminating the core model.

## 7. iCalendar renderer: a compatibility projection

The iCalendar renderer must be conservative. It outputs an RFC 5545/7986-compatible `VCALENDAR`, uses CRLF content lines with line folding, and is allowed to lose *presentation detail* only where the source model has recorded that loss. It must never create a formally invalid duration or treat a time-zone-free local value as UTC.[1] [2]

### 7.1 Calendar header mapping

| Canonical field | iCalendar output | Rule |
|---|---|---|
| `identity.uid` | `UID` at `VCALENDAR` scope | Generate an opaque stable identifier. It is a calendar identity, not an event identity. |
| `identity.name` | `NAME` | Primary standard name. |
| `identity.description` | `DESCRIPTION` at `VCALENDAR` scope | Primary standard description. |
| `civil.scale` | `CALSCALE:GREGORIAN` | Emit exactly once. |
| `revision.modified_utc` | `LAST-MODIFIED` at `VCALENDAR` scope | UTC audit metadata; inject from explicit build/release input, never the host clock by accident. |
| source endpoint | `SOURCE;VALUE=URI` | Emit only a live refresh URL. |
| refresh policy | `REFRESH-INTERVAL;VALUE=DURATION` | Must be a positive fixed duration such as `P1W`; no `P3M`, `YEARLY`, or bare invalid form. |
| canonical calendar color | `COLOR` | Emit only a non-empty declared CSS3 named color. |
| compatibility mirrors | `X-WR-CALNAME`, `X-WR-CALDESC`, `X-WR-RELCALID` | Optional compatibility output. Values must be exact mirrors of `NAME`, `DESCRIPTION`, and `UID`; omission is preferable to divergent copies. |

`DTSTAMP` is a component change-management property, not a calendar-level substitute for `LAST-MODIFIED`. Every generated `VEVENT` therefore receives a valid UTC `DTSTAMP`; the calendar itself uses the RFC 7986 `LAST-MODIFIED` property if release tracking is wanted.[1] [2]

### 7.2 Event identity and shared mapping

Each exportable layer maps to one `VEVENT` series or to a bounded set of materialized `VEVENT` instances. Event identifiers remain deterministic:

```text
VEVENT UID = opaque_uuid_v5(calendar_uid, layer.id + "|" + canonical_anchor)
```

The implementation may use a UUIDv5-like reproducible derivation internally, but the emitted identifier must remain opaque and must not leak a host/domain/user name. The same logical identifier becomes the JSCalendar event `uid`.

| Canonical field | iCalendar expression |
|---|---|
| `LayerSpec.label` | `SUMMARY` |
| `LayerSpec.category` | `CATEGORIES` with a non-empty escaped text value |
| `DisplayPolicy.color` | `COLOR` only when explicitly declared; never `COLOR:` as a placeholder |
| Source hierarchy parent | `RELATED-TO` only when a non-empty real parent event UID exists; otherwise omit it. |
| Layer id/rank and engine semantics | Namespaced `X-` properties only if a target-safe projection is required; otherwise stay in the manifest/JSON output. |
| Public non-blocking semantics | `TRANSP:TRANSPARENT` for layer markers, unless a layer is deliberately meant to occupy free/busy time. |
| Revision state | `DTSTAMP` required and UTC; `LAST-MODIFIED`/`SEQUENCE` only with a deliberate source revision policy. |

### 7.3 DTSTART and coverage decision table

| Canonical occurrence/coverage | iCalendar projection | Reason |
|---|---|---|
| Civil all-day marker | `DTSTART;VALUE=DATE:YYYYMMDD`, optionally a one-day `DTEND;VALUE=DATE` if the visual client needs a band | The explicit `VALUE=DATE` prevents accidental DATE-TIME interpretation. |
| Floating local sub-day marker | `DTSTART:YYYYMMDDTHHMMSS` without `TZID` and without `Z` | This is a floating local date-time. |
| Fixed sub-day span | Floating local `DTSTART` plus fixed `DURATION` using days/hours/minutes/seconds | A duration represents elapsed time and is valid here. |
| Civil month/year/century/millennium boundary | Recurring marker, or a bounded materialized event with a calculated `DTEND` at the next civil boundary | Do **not** emit `P1M`, `P1Y`, `P100Y`, or `P1000Y` as `DURATION`. |
| Ritual silence | No VEVENT | Silence is represented in the manifest/JSCalendar semantics, not by empty calendar events. |

For the public feed, the default should be **markers** for unbounded civil and macro layers. A separate, bounded `band` profile may materialize calendar spans over a stated horizon (for example, the current year plus a release-defined window). The profile name belongs in the artifact filename and manifest so consumers never confuse a marker feed with a visual-band feed.

### 7.4 Recurrence policy

A renderer may translate a `FixedClockRule`, `WeekdayRule`, `MonthDayRule`, or AnnualRule into a valid RRULE only after validating the rule against the emitted `DTSTART` type.

```text
second  -> DTSTART:18100101T000000  + RRULE:FREQ=SECONDLY
minute  -> DTSTART:18100101T000000  + RRULE:FREQ=MINUTELY
hour    -> DTSTART:18100101T000000  + RRULE:FREQ=HOURLY
day     -> DTSTART;VALUE=DATE:18100101 + RRULE:FREQ=DAILY
monday  -> DTSTART;VALUE=DATE:18100101 + RRULE:FREQ=WEEKLY;BYDAY=MO
january -> DTSTART;VALUE=DATE:18100101 + RRULE:FREQ=YEARLY;BYMONTH=1
```

A target-safe generator must use semicolons—not commas—between RRULE parts, emit no blank line, and reject an RRULE whose `DTSTART` date/time type is incompatible with the selectors. It must also enforce an export-risk policy: `SECONDLY` and `MINUTELY` recurrent series can overwhelm ordinary clients. These layers should be excluded from the normal public ICS profile or emitted only in a clearly experimental, bounded debugging profile.

The senary and named-rhythm layers need special treatment. They should not be forced into approximate RRULE arithmetic where their starts depend on a common/leap Gregorian year or a deliberately silent interval. The renderer should instead choose either a bounded materialized set of individual VEVENTs or a standards-valid recurrence plus explicit `RDATE`/`EXDATE` overrides, verified over its publication window. The source model remains the arbiter.

### 7.5 Current-draft features

The July 2026 iCalendar/JSCalendar extension draft proposes `SHOW-WITHOUT-TIME;VALUE=BOOLEAN:TRUE` for a time-specific event whose time span is not important to display, and it extends `COLOR` to six-digit CSS3 RGB values. This draft is not yet an RFC. The default public renderer should stay within published RFC 5545/7986 features, with a separately versioned opt-in renderer profile for draft features.[3]

## References for the iCalendar renderer

[1] [RFC 5545, *Internet Calendaring and Scheduling Core Object Specification*](https://www.rfc-editor.org/rfc/rfc5545.txt)

[2] [RFC 7986, *New Properties for iCalendar*](https://www.rfc-editor.org/rfc/rfc7986.txt)

[3] [IETF, *iCalendar Format Extensions for JSCalendar*, draft-ietf-calext-icalendar-jscalendar-extensions-06](https://datatracker.ietf.org/doc/html/draft-ietf-calext-icalendar-jscalendar-extensions-06)

## 8. JSCalendar renderer: a structured interchange projection

The JSCalendar renderer outputs a **Group** object conforming to the exact version of JSCalendar selected by the build profile. As of this design snapshot, that is the active `draft-ietf-calext-jscalendarbis-18` version `"2.0"`; it is still an Internet-Draft, so the renderer must declare its version and remain revision-pinned.[4]

JSCalendar is an interchange projection, not the neutral engine model. It is richer than iCalendar for structured recurrence overrides, unknown-field preservation, and JSON validation, but it still does not define ritual calendar units or month/year durations.

### 8.1 Group-level mapping

```json
{
  "@type": "Group",
  "version": "2.0",
  "uid": "<stable-calendar-id>",
  "title": "cron_clock",
  "description": "<calendar description>",
  "updated": "<explicit release timestamp in UTC>",
  "source": "<canonical refresh URI>",
  "entries": []
}
```

| Canonical field | JSCalendar Group property | Rule |
|---|---|---|
| `identity.uid` | `uid` | Same stable logical calendar identity as iCalendar `VCALENDAR/UID`. |
| `identity.name` | `title` | Direct standard mapping from iCalendar `NAME`. |
| `identity.description` | `description` | Direct standard mapping from calendar-level `DESCRIPTION`. |
| `revision.modified_utc` | `updated` | Explicit release/build input as a UTC date-time; never silently regenerated from the local machine clock. |
| source endpoint | `source` | Direct mapping from iCalendar `SOURCE`. |
| canonical calendar color | `color` | Emit only when a calendar-wide color has been deliberately decided. |
| layer events | `entries` | Each exportable logical layer becomes one Event object or a bounded collection of Event objects. |

A bare `cron_clock.jscalendar.json` file may be the Group object above. It does **not** claim to be a JMAP service. JMAP Calendars is a later optional server/API adapter; it adds account state, calendar collection membership, sharing, query limits, and sync methods around JSCalendar Events.[6]

### 8.2 Event mapping

| Canonical field | JSCalendar Event property | Mapping rule |
|---|---|---|
| logical occurrence identity | `uid` | Same logical event UID as the iCalendar VEVENT. |
| label | `title` | Direct, no formatting code in the source label. |
| start | `start` | `YYYY-MM-DD` for civil all-day markers, `YYYY-MM-DDTHH:MM:SS` for floating local sub-day occurrences. |
| floating policy | omitted `timeZone` | A LocalDateTime with no `timeZone` is floating under JSCalendar. Do not write `UTC`, `Etc/UTC`, or a client zone. |
| fixed span | `duration` | Use only valid weeks/days/hours/minutes/seconds. |
| target visual color | `color` | Emit only a declared target-safe color. |
| keywords/categories | `keywords` or a source-declared vocabulary field | Keep semantic categories as a set, not as display title decoration. |
| relation to parent layer | relation map/object | Emit only a genuine resolved parent relation. |
| recurrence | `recurrenceRule` and, where needed, `recurrenceOverrides` | Prefer structured recurrence; use overrides for deliberate exceptions rather than hiding them in ad hoc arithmetic. |
| non-blocking calendar marker | `freeBusyStatus` in the selected JSCalendar version/profile | Set to the standard “free” state only after schema validation; otherwise preserve non-blocking intent only in the canonical projection. |

A sub-day output that begins at the common-Monday anchor is therefore structurally clear:

```json
{
  "@type": "Event",
  "uid": "<opaque-second-layer-uid>",
  "title": "Second",
  "start": "1810-01-01T00:00:00",
  "duration": "PT1S",
  "recurrenceRule": {
    "@type": "RecurrenceRule",
    "frequency": "secondly"
  },
  "timeZone": null
}
```

The **actual renderer must omit**, rather than serialize, `timeZone` when the current JSCalendar schema expresses floating time by absence. The example shows the intended semantic condition; the JSON Schema/validator for the selected draft revision decides the literal serialization.

### 8.3 JSCalendar’s important advantages for cron_clock

A JSCalendar `LocalDateTime` without a `timeZone` is explicitly floating; it occurs at the stated wall-clock time in each time zone. That matches the existing requirement without the ambiguous `TZID`/UTC choices that appear in hand-authored iCalendar.[4]

JSCalendar also natively models recurrence exceptions as `recurrenceOverrides` patch objects. For senaries and named rhythms, a renderer may generate a main Event for the ordinary pattern and use a small, auditable override map for leap-sensitive or silent-boundary cases. This is cleaner than creating disconnected VEVENTs, but it does not excuse the renderer from checking every generated occurrence over the chosen publication horizon.[5]

### 8.4 Ritual semantics and vendor extensions

The ritual model has concepts with no standard JSCalendar counterpart: `common_monday_anchor`, `senary`, `demon_grace_silence`, `non_period_silence`, canonical layer rank, and engine-facing boundary identifiers. They must not be misrepresented as standard fields.

The strict rule is:

| Semantic situation | JSCalendar treatment |
|---|---|
| Standard calendar fact, such as start, title, recurrence, duration, color, relation | Use the registered JSCalendar property. |
| A source fact that has no standard target equivalent but must survive the public JSON projection | Use a vendor-specific property under a domain the publisher controls, e.g. `"<controlled-domain>:cronClock"`. |
| A fact needed only by the engine/generator | Keep it in `cron_clock.py`, the neutral JSON/manifest, and test fixtures; do not export it gratuitously. |
| Intentional silence | Do not fabricate an Event. Optionally record the silence definition inside the controlled-domain extension or the neutral manifest. |

The JSCalendar specification requires vendor-specific fields to use a publisher-controlled domain prefix and permits consumers to preserve unknown vendor fields. A friendly key such as `"cronClock"` or an invented `X-` spelling is not conformant JSCalendar extension syntax.[4]

A possible controlled-domain extension value is deliberately self-contained:

```json
{
  "<controlled-domain>:cronClock": {
    "layerId": "senary_2",
    "rank": 13,
    "coverage": "next_boundary",
    "silentInterstices": ["demon_grace"],
    "anchor": "1810-01-01"
  }
}
```

That extension is **not** an interoperability promise. It is a lossless carrier for the publisher’s own vocabulary, and the neutral model remains the authoritative definition.

### 8.5 Why JSCalendar still cannot absorb the entire source model

JSCalendar version 2.0 uses a duration grammar limited to weeks, days, hours, minutes, and seconds—matching iCalendar in the relevant respect. It cannot express one civil month, one Gregorian year, a century, or a millennium as a duration token. Civil bands therefore continue to use calculated next-boundary ends or bounded materialization, just as in the iCalendar renderer.[4]

It also does not define a ritual calendar scale or an event meaning “the absence between named periods.” The dual-format generator should resist format-driven invention: the game-facing neutral model owns those meanings, and projections show only what their targets can express faithfully.

## 9. Projection profile matrix

| Layer category | Canonical definition | `.ics` normal profile | JSCalendar normal profile | Engine-neutral JSON/manifest |
|---|---|---|---|---|
| Second/minute | Fixed sub-day boundary | Omit or bound to protect ordinary clients | Include only in a technical/debug profile | Full definition and queries. |
| Hour/phase | Fixed local sub-day boundary/span | Valid floating recurring VEVENT, subject to client-volume profile | Floating Event with valid `duration`/`recurrenceRule` | Full definition. |
| Seven named rhythms | Fixed interval plus declared silence | Bounded materialization or recurrence with audited overrides | Structured recurring Event plus override map where valid | Full silence predicates and occurrence query. |
| Day/week/weekday | Civil recurrence | DATE marker VEVENT/RRULE | Event with date start or floating start as modelled | Full definition. |
| Month/quarter/year | Civil-boundary recurrence | Date marker, or bounded materialized calculated `DTEND` | Event marker or bounded calculated end | Full definition. |
| Senary | Anchor plus 60-day intervals and deliberate internal silence | Bounded individual VEVENTs are safest | Individual Events or carefully validated recurrence/overrides | Full calculation and silence rule. |
| Decade/century/millennium | Civil macro boundary | Unbounded marker only, or a stated publication-window materialization | Marker or bounded calculated end | Full definition. |

## References for the JSCalendar renderer

[4] [IETF, *JSCalendar 2.0*, draft-ietf-calext-jscalendarbis-18](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendarbis-18)

[5] [IETF, *JSCalendar: Converting from and to iCalendar*, draft-ietf-calext-jscalendar-icalendar-25](https://datatracker.ietf.org/doc/html/draft-ietf-calext-jscalendar-icalendar-25)

[6] [IETF, *JMAP Calendars*, draft-ietf-jmap-calendars-28](https://datatracker.ietf.org/doc/html/draft-ietf-jmap-calendars-28)

## 10. Generator pipeline

The implementation should be a small deterministic build system rather than a script that assembles strings inline. The critical intermediate form is a **compiled chronology projection**: resolved layer definitions, recurrence strategy, identities, and an explicit artifact profile, still independent of `.ics` or JSON syntax.

```python

def build(profile: ExportProfile, release: ReleaseInfo) -> ArtifactSet:
    spec = load_spec()                         # immutable authored definitions
    validate_spec(spec)                        # chronology invariants
    compiled = compile_projection(spec, profile, release)
    validate_compiled(compiled, spec)          # no hidden semantic loss

    ics = render_ics(compiled, release)
    jscalendar = render_jscalendar(compiled, release)
    manifest = render_manifest(spec, compiled, ics, jscalendar, release)

    validate_ics(ics, compiled, profile)
    validate_jscalendar(jscalendar, compiled, profile)
    validate_cross_projection(ics, jscalendar, compiled, profile)
    return ArtifactSet(ics=ics, jscalendar=jscalendar, manifest=manifest)
```

### 10.1 Command-line contract

```text
python cron_clock.py validate
python cron_clock.py build --profile public-core --release 2026-08-19
python cron_clock.py build --profile technical-clock --from 2026-01-01 --to 2027-01-01
python cron_clock.py explain 1810-01-01T00:00:00
python cron_clock.py occurrences --layer senary --from 1810-01-01 --to 1812-01-01
```

`explain` and `occurrences` are first-class diagnostic commands. They make the game-engine mapping useful without pretending that the module owns an engine tick. A separate game integration can call the same pure functions after it maps game state to a civil instant.

### 10.2 Export profiles

One chronology needs more than one safe rendering profile. Profile choice is part of the artifact identity, not a casual renderer flag.

| Profile | Intended consumer | Included layers | Key restrictions |
|---|---|---|---|
| `public-core` | Ordinary webcal/import clients | Civil markers, months, quarters, year, senaries, macro markers, named weekdays. | Excludes secondly/minutely traffic; uses markers for unbounded civil spans. |
| `public-clock` | Interested calendar users with normal-client safeguards | `public-core` plus hour, phases, and named rhythms. | Must document event volume and omit/bound minute/second layers. |
| `technical-clock` | Engine/debug tools | All required layers within an explicit start/end horizon. | Bounded materialization permitted; no promise of general calendar-client performance. |
| `jscalendar-rich` | Controlled JSON consumers | Same semantic scope as compiled profile plus controlled-domain ritual extension. | Pinned to a precise JSCalendar draft/RFC version. |
| `neutral` | Game engine, tests, and archival tooling | Entire chronology and all silences. | Not an interchange-calendar claim; no loss allowed. |

The filenames should make this visible. For example:

```text
cron_clock.public-core.ics
cron_clock.public-clock.ics
cron_clock.technical-clock.ics
cron_clock.public-core.jscalendar.json
cron_clock.neutral.json
cron_clock.manifest.json
```

If the user-facing names must remain `cron_clock.ics` and `cron_clock.json`, those can be aliases to a declared default profile. The manifest must still state which profile they represent.

### 10.3 Validation gates

| Gate | Failure examples | Required outcome |
|---|---|---|
| Neutral chronology | Wrong common-Monday anchor, a rank collision, undefined parent, accidental silence coverage, an undecided color silently filled. | Stop the build. |
| Civil arithmetic | A month/year boundary uses fixed elapsed arithmetic, leap-day placement conflicts with the chosen non-circular senary rule. | Stop the build. |
| iCalendar syntax | Blank lines, LF-only output, malformed content lines, empty `COLOR`/`PRIORITY`, illegal RRULE separator, invalid `DURATION`, non-UTC `DTSTAMP`. | Stop the build. |
| iCalendar semantics | `TZID`/`Z` on floating event start; DATE value lacking `VALUE=DATE`; empty `RELATED-TO`; sub-day DTSTART with date-only semantics. | Stop the build. |
| JSCalendar structure | Invalid I-JSON, wrong top-level `Group`, missing `version`, invalid `@type`, malformed `Id`, unsupported bare extension property. | Stop the build. |
| JSCalendar semantics | `timeZone` present on a floating event; invalid duration; ritual fact put into a standard property; extension prefix not controlled by the publisher. | Stop the build. |
| Cross-projection | Divergent title/category/color/UID/start semantics; a permitted source layer disappears without an explicit loss record. | Stop the build. |
| Consumer-volume policy | A public profile includes unbounded SECONDLY/MINUTELY series. | Stop the build or require an explicit `--unsafe-profile` acknowledgement. |

### 10.4 Semantic digest and manifest

The manifest gives generators, game clients, and reviewers a way to detect drift without parsing every output format. It should contain the specification revision, source hash, explicit release timestamp, profile, date horizon, output hashes, standard versions, and a semantic digest of every projected layer.

```json
{
  "generator": "cron_clock.py",
  "specRevision": "1",
  "profile": "public-core",
  "release": "2026-08-19T00:00:00Z",
  "civilScale": "GREGORIAN",
  "floatingLocal": true,
  "anchor": "1810-01-01",
  "jsCalendarVersion": "2.0-draft-ietf-calext-jscalendarbis-18",
  "artifacts": {
    "ics": {"path": "cron_clock.public-core.ics", "sha256": "..."},
    "jscalendar": {"path": "cron_clock.public-core.jscalendar.json", "sha256": "..."}
  },
  "semanticDigest": "..."
}
```

The release timestamp must be an **explicit input** or a declared source revision fact. Rebuilding the same specification with the same release arguments should byte-reproduce the outputs; using the wall clock as a hidden source would defeat that property.

## 11. Implementation boundary

The first implementation should keep this module self-contained and dependency-light:

```text
cron_clock.py
  ├── source declarations          # layers, silence, policy, identities
  ├── chronology functions         # Gregorian and ritual calculations
  ├── compiler                     # profile-based projection plan
  ├── ical renderer + strict linter
  ├── jscalendar renderer + schema validator
  ├── manifest renderer
  ├── cross-format comparator
  └── CLI
```

A mature iCalendar library may be used as one parser/checker, but it must not be the sole validator because tolerant libraries can accept malformed blank lines or field combinations. The build must retain raw lexical checks for CRLF, blank lines, content-line delimiters, and exact property-value constraints.

## 12. Design decisions now fixed

| Decision | Contract |
|---|---|
| Source of truth | `cron_clock.py` only. |
| Engine tick | Intentionally absent from the chronology model; supplied externally if needed. |
| Calendar anchor | `1810-01-01`, common Monday, as a civil/ritual alignment reference. |
| Time semantics | Floating local time for event starts; UTC only for audit/change metadata required by target formats. |
| Silence | Deliberate and queryable in the source model; never repaired into empty/placeholder events. |
| iCalendar strategy | Standards-valid compatibility projection, with bounded legacy mirrors and explicit profiles. |
| JSCalendar strategy | Version-pinned structured projection with controlled-domain extensions only for unrepresentable ritual semantics. |
| Neutral JSON | Separate optional engine/archival artifact, not silently conflated with JSCalendar. |
| Publication strategy | Derived artifacts plus manifest and validation; no hand-edited output files. |

## 13. Questions to settle before code

The source-model architecture is now stable. The remaining questions are policy choices, not missing architecture:

1. Which profile receives the unqualified names `cron_clock.ics` and `cron_clock.json`?
2. Is `cron_clock.json` the neutral engine artifact, or should the JSCalendar Group own that name while neutral JSON uses a clearer suffix?
3. What is the initial technical-materialization window for rare/exception-heavy layers such as senaries?
4. Which controlled domain will legally own JSCalendar ritual extensions?
5. Which client matrix determines whether each X-WR compatibility mirror remains emitted?

After those five decisions, implementation can proceed without reopening the chronology model.
