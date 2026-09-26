# Examination of PR #981: `cron_clock.ics`

**Repository:** `LAF-US/IDAHO-VAULT`  
**PR:** [#981 — `cron_clock.ics: the map of time — 35 events on the year-wheel`](https://github.com/LAF-US/IDAHO-VAULT/pull/981)  
**State at examination:** Open, mergeable, no human review decision recorded; labels include `review/threads-open` and `review/pending`.[1]

## What #981 actually is

PR #981 is an earlier, iCalendar-first attempt to make `cron_clock.ics` itself the map of the full temporal system. Its stated working draft says that no line has been formally approved. The head changes 15 files and adds approximately 42,003 lines, primarily by importing an RFC reference library alongside the calendar file.[1]

The pull request description describes a 35-event, 1776-anchored year wheel. Direct inspection of the current PR-head `cron_clock.ics`, however, finds **52 VEVENTs** and several different anchors: millennium at 2001, century at 1601, and most ordinary clock layers at 1810. This discrepancy is a material design and review problem, not a cosmetic documentation mismatch.[1]

| PR body / stated intent | Actual PR-head calendar |
|---|---|
| 35 events, built as a year wheel. | 52 VEVENTs, ranging from millennium through second. |
| 1776 used as the central Monday anchor. | 1601, 1810, and 2001 all appear as layer anchors. |
| Wheel layers moved to valid starts-only markers. | Several current layers again use invalid calendar-unit durations, including `P1000Y`, `P100Y`, `P10Y`, `P1Y`, `P3M`, and `P1M`. |
| A stable working summary of the calendar. | The document and the bytes describe materially different models. |

## The temporal model embedded in the PR

The file takes a **top-down calendar rendering** approach. It begins with Millennium, Century, Decade, and Year, descends through quarter, senary, month, week, day, named weekdays, phase, named 204-minute rhythms, hour, half, score, dozen, minute, and second. This is the handwritten ordering you identified as worth reversing.

Its genuinely useful content is the vocabulary and intended geometry: the three eight-hour phases, seven 204-minute named rhythms, twelve unrepresented minutes, weekday ROYGBIV colors, a white calendar color, and the senary structure. It is a historical design specimen, not a reliable executable specification.

The PR also makes the wrong abstraction boundary for the current work. It represents `tick` as a VEVENT that the minute layer relates to. Under the clarified model, **`vault_tick` is upstream and out of scope**; `cron_clock` answers the question “what time is X?” and should produce `vault_time`. The Second may remain a *time-description layer*, but it must not stand in for the external tick source.

## Direct technical findings

The following issues are confirmed from the PR-head file itself. They are not merely accepted from automated-review text.

| Area | Direct finding | Implication for the generator design |
|---|---|---|
| Calendar-level properties | `REFRESH-INTERVAL=YEARLY` is malformed; calendar-level `DTSTAMP` is used; `SOURCE` points to an absent nested path. | Header data must be generated from a typed calendar metadata model, then lexically validated. |
| Durations | Civil month/year/macro spans use durations whose month/year units are unsupported by iCalendar `DURATION`. | The generator must render these as markers or calculated, bounded next-boundary spans. |
| Relationships | Many events have empty `RELATED-TO`; one event uses comma-separated relationship targets. | Parent relations belong in the neutral model and must only render when real, one-per-property targets exist. |
| Colors | Numerous `COLOR:` properties are blank. | Undecided colors must be omitted, never serialized as empty placeholders. |
| Recurrence grammar | `INTERVAL:20` and `INTERVAL:12` use a colon where RRULE requires `=`. | RRULEs must be rendered structurally, not hand-concatenated. |
| Public-client safety | The second layer exports an unbounded `SECONDLY` recurrence from 1810. | High-volume layers need a separate bounded technical profile or must remain outside ordinary `.ics` publication. |
| Identity | The event hierarchy uses UIDs and `RELATED-TO` as if it were a runtime ontology. | The generator should define stable neutral identifiers first, then project them only where a target format benefits. |

## Relevance to the current `cron_clock.py` direction

PR #981 makes the case for the new architecture by negative example. The file asks iCalendar to carry three jobs simultaneously: source of truth, game-time ontology, and public interchange artifact. Its stale body, mixed anchors, recurrence mistakes, and semantic overloading follow naturally from that burden.

The proposed `cron_clock.py` design separates those concerns. The neutral source owns the answer to **“what time is X?”**; the `.ics` file exposes a guarded, compatibility-oriented slice of that answer space; and JSCalendar can preserve more structure but still does not define the ritual system. Neither projection should define `vault_time`, and neither should know anything about the upstream `vault_tick` implementation.

| Keep from #981 | Move out of the `.ics` source model | Retire or redesign |
|---|---|---|
| Named layers, phase/rhythm geometry, deliberate silence, ROYGBIV, white year-family intention, and the calendar vocabulary. | Layer rank, silence classification, engine-facing names, canonical anchor selection, and all parent/containment logic. | Mixed layer anchors, empty properties, nonstandard civil durations, `tick` as a calendar event, and unbounded second-level public recurrence. |

## Bottom line

PR #981 is valuable as a **historical inventory of the desired time vocabulary** and as a record of prior standards research. It should not be treated as the source of truth for implementation. Its actual head is internally inconsistent with its own stated 35-event/1776 design, is still explicitly unapproved, and uses an iCalendar-first model that conflicts with the clarified `vault_tick → cron_clock → vault_time` boundary.

No repository files, reviews, comments, or pull-request state were changed during this examination.

## Reference

[1] [LAF-US/IDAHO-VAULT pull request #981](https://github.com/LAF-US/IDAHO-VAULT/pull/981)
