from __future__ import annotations

from collections import Counter, defaultdict
import sys
from pathlib import Path
import re

from cli_path_guard import repo_path

# Paths accept command-line overrides, containment-checked to repository files.
_REPO = Path(__file__).resolve().parent
source = repo_path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock.ics'
text = source.read_text(encoding='utf-8')
raw_lines = text.splitlines()
nonblank = [line.rstrip('\r') for line in raw_lines if line.strip()]

# Unfold CRLF/LF content lines for property inspection.
lines: list[str] = []
for line in nonblank:
    if line.startswith((' ', '\t')) and lines:
        lines[-1] += line[1:]
    else:
        lines.append(line)

# Component parser with raw field preservation.
events: list[dict[str, list[str]]] = []
stack: list[dict[str, list[str]]] = []
calendar: dict[str, list[str]] = defaultdict(list)
for line in lines:
    if line == 'BEGIN:VEVENT':
        ev: dict[str, list[str]] = defaultdict(list)
        stack.append(ev)
    elif line == 'END:VEVENT':
        if stack:
            events.append(stack.pop())
        else:
            calendar['PARSE_ERRORS'].append('Unmatched END:VEVENT')
    elif ':' in line:
        keypart, value = line.split(':', 1)
        key = keypart.split(';', 1)[0].upper()
        if stack:
            stack[-1][key].append(value)
        else:
            calendar[key].append(value)


def one(ev: dict[str, list[str]], name: str) -> str:
    vals = ev.get(name, [])
    return vals[0] if vals else ''


def parse_ical_duration(value: str) -> int | None:
    # RFC 5545 duration unit calculation for integer arithmetic.
    match = re.fullmatch(r'([+-])?P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', value)
    if not match or not any(match.groups()[1:]):
        return None
    sign, weeks, days, hours, minutes, seconds = match.groups()
    total = (int(weeks or 0) * 7 * 86400 + int(days or 0) * 86400 +
             int(hours or 0) * 3600 + int(minutes or 0) * 60 + int(seconds or 0))
    return -total if sign == '-' else total


def rrule_map(value: str) -> tuple[dict[str, str], list[str]]:
    parts: dict[str, str] = {}
    defects: list[str] = []
    for part in value.split(';'):
        if '=' not in part:
            defects.append(part)
        else:
            k, v = part.split('=', 1)
            parts[k.upper()] = v
    return parts, defects

# Report inventory.
print(f'RAW_LINES={len(raw_lines)} NONBLANK_CONTENT_LINES={len(nonblank)} EVENTS={len(events)}')
print('CALENDAR_PROPERTIES=' + ', '.join(f'{k}={v}' for k, v in sorted(calendar.items())))
print()

print('=== EVENT INVENTORY ===')
for i, ev in enumerate(events, 1):
    print(f'{i:02d}. summary={one(ev,"SUMMARY")!r} uid={one(ev,"UID")!r} category={one(ev,"CATEGORIES")!r} priority={one(ev,"PRIORITY")!r} dtstart={one(ev,"DTSTART")!r} duration={one(ev,"DURATION")!r} rrule={one(ev,"RRULE")!r}')
print()

print('=== LAYER COVERAGE ===')
category_counts = Counter(one(ev, 'CATEGORIES') or '<missing>' for ev in events)
for cat, count in sorted(category_counts.items()):
    print(f'{cat}: {count}')
print()

print('=== IDENTIFIER & RELATIONSHIP FINDINGS ===')
uids = defaultdict(list)
for ev in events:
    uids[one(ev, 'UID')].append(one(ev, 'SUMMARY'))
for uid, summaries in sorted(uids.items()):
    if not uid:
        print('MISSING_UID: ' + ', '.join(summaries))
    elif len(summaries) > 1:
        print(f'DUPLICATE_UID {uid!r}: ' + ', '.join(summaries))
empty_related = [one(ev, 'SUMMARY') for ev in events if 'RELATED-TO' in ev and not one(ev, 'RELATED-TO')]
print('EMPTY_RELATED_TO=' + (', '.join(empty_related) if empty_related else '<none>'))
print()

print('=== RECURRENCE & TIME-CLOSURE FINDINGS ===')
for ev in events:
    summary = one(ev, 'SUMMARY')
    rule = one(ev, 'RRULE')
    duration = one(ev, 'DURATION')
    if rule:
        rparts, malformed = rrule_map(rule)
        if malformed:
            print(f'MALFORMED_RRULE {summary!r}: non-name/value parts={malformed}')
        if 'FREQ' not in rparts:
            print(f'NO_FREQ {summary!r}: {rule!r}')
        # Flag sub-day frequencies anchored by a DATE (not date-time).
        start = one(ev, 'DTSTART')
        if rparts.get('FREQ') in {'HOURLY', 'MINUTELY', 'SECONDLY'} and re.fullmatch(r'\d{8}', start):
            print(f'DATE_ONLY_SUBDAY_SEED {summary!r}: FREQ={rparts.get("FREQ")} DTSTART={start}')
    if duration:
        seconds = parse_ical_duration(duration)
        if seconds is None:
            print(f'UNPARSEABLE_DURATION {summary!r}: {duration!r}')

# Exact time coverage by labels/categories.
phase = [ev for ev in events if one(ev, 'CATEGORIES') == 'phase']
rhythm = [ev for ev in events if one(ev, 'CATEGORIES') == 'rhythm']
weekday = [ev for ev in events if one(ev, 'CATEGORIES') == 'weekday']
print(f'PHASE_TOTAL_SECONDS={sum(parse_ical_duration(one(ev,"DURATION")) or 0 for ev in phase)} ({len(phase)} events)')
print(f'RHYTHM_TOTAL_SECONDS={sum(parse_ical_duration(one(ev,"DURATION")) or 0 for ev in rhythm)} ({len(rhythm)} events)')
print(f'WEEKDAY_TOTAL_SECONDS={sum(parse_ical_duration(one(ev,"DURATION")) or 0 for ev in weekday)} ({len(weekday)} events)')
if rhythm:
    total = sum(parse_ical_duration(one(ev, 'DURATION')) or 0 for ev in rhythm)
    print(f'RHYTHM_DAY_DELTA_SECONDS={86400-total}')
print()
print('=== NAMED-RHYTHM AND SENARY CLOSURE ===')
from datetime import datetime, timedelta

def parse_local_start(value: str) -> datetime:
    return datetime.strptime(value, '%Y%m%dT%H%M%S')

named_rhythms = [ev for ev in events if parse_ical_duration(one(ev, 'DURATION')) == 204 * 60]
if named_rhythms:
    ordered = sorted(named_rhythms, key=lambda ev: parse_local_start(one(ev, 'DTSTART')).time())
    cursor = datetime(1810, 1, 1, 0, 0, 0)
    day_end = datetime(1810, 1, 2, 0, 0, 0)
    for ev in ordered:
        # Only the wall-clock time matters; the seed date may differ from 1810.
        start = datetime.combine(cursor.date(), parse_local_start(one(ev, 'DTSTART')).time())
        gap = start - cursor
        print(f'RHYTHM_GAP_BEFORE {one(ev, "SUMMARY")}: {int(gap.total_seconds() // 60)} minutes')
        cursor = start + timedelta(seconds=parse_ical_duration(one(ev, 'DURATION')) or 0)
    print(f'RHYTHM_GAP_AFTER_FINAL: {int((day_end-cursor).total_seconds() // 60)} minutes')

senary = [ev for ev in events if one(ev, 'CATEGORIES') == 'senary']
for year in (1810, 1812):
    spans = []
    for ev in senary:
        start_raw = one(ev, 'DTSTART')
        start = datetime(year, int(start_raw[4:6]), int(start_raw[6:8]))
        end = start + timedelta(seconds=parse_ical_duration(one(ev, 'DURATION')) or 0)
        spans.append((start, end, one(ev, 'SUMMARY')))
    spans.sort()
    cursor = datetime(year, 1, 1)
    for start, end, label in spans:
        print(f'SENARY_{year}_GAP_BEFORE {label}: {(start-cursor).days} days')
        cursor = end
    print(f'SENARY_{year}_GAP_TO_NEXT_YEAR: {(datetime(year+1, 1, 1)-cursor).days} days')

print()
print('=== LABEL, CATEGORY, AND METADATA FINDINGS ===')
for ev in events:
    summary = one(ev, 'SUMMARY')
    cat = one(ev, 'CATEGORIES')
    color = one(ev, 'COLOR')
    priority = one(ev, 'PRIORITY')
    # Explicit label/category mismatch detector from authored taxonomy.
    if summary == 'Azer' and cat != 'Azer':
        print(f'LABEL_CATEGORY_MISMATCH: summary={summary!r} category={cat!r}')
    if color == '':
        print(f'EMPTY_COLOR: {summary!r}')
    if priority == '':
        print(f'EMPTY_PRIORITY: {summary!r}')
    stamp = one(ev, 'DTSTAMP')
    if not re.fullmatch(r'\d{8}T\d{6}Z', stamp):
        print(f'INVALID_OR_NONUTC_DTSTAMP: {summary!r} -> {stamp!r}')

# Check values implied by named quantities.
for ev in events:
    summary = one(ev, 'SUMMARY')
    rule, duration = one(ev, 'RRULE'), one(ev, 'DURATION')
    rparts, malformed = rrule_map(rule) if rule else ({}, [])
    if summary in {'Half', 'Score', 'Dozen'}:
        print(f'NAMED_QUANTITY {summary}: interval={rparts.get("INTERVAL")!r}, freq={rparts.get("FREQ")!r}, duration={duration!r}')

print()
print('=== ANCHOR DATES ===')
for ev in events:
    start = one(ev, 'DTSTART')
    if start.startswith(('1601', '1810', '2001')):
        print(f'{one(ev,"SUMMARY")!r}: {start}')
