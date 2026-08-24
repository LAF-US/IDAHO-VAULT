from __future__ import annotations

from collections import Counter
from datetime import date
import sys
from pathlib import Path

from icalendar import Calendar

# Paths accept command-line overrides and default to this repository's copies.
_REPO = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock.ics'
WEEKDAY_UIDS = {
    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
    'friday': 4, 'saturday': 5, 'sunday': 6,
}
MONTH_UIDS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
}


def line_numbers(lines: list[str], predicate) -> list[int]:
    return [number for number, line in enumerate(lines, start=1) if predicate(line)]


def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8')
    lines = text.splitlines()
    findings: list[tuple[str, str]] = []

    if b'\r\n' not in raw:
        findings.append(('File formatting', 'Submitted text has LF line endings rather than RFC 5545 CRLF content lines.'))

    stack: list[str] = []
    for number, line in enumerate(lines, start=1):
        if line.startswith('BEGIN:'):
            stack.append(line[6:])
        elif line.startswith('END:'):
            name = line[4:]
            if not stack or stack.pop() != name:
                findings.append(('Component balance', f'Line {number} has unmatched {line}.'))
    if stack:
        findings.append(('Component balance', f'Unclosed components: {", ".join(stack)}.'))

    for number in line_numbers(lines, lambda line: line == 'PRIORITY:'):
        findings.append(('Empty required value', f'Line {number}: PRIORITY has no integer value.'))

    for number, line in enumerate(lines, start=1):
        if line.startswith('RRULE:'):
            bad_parts = [part for part in line[6:].split(';') if '=' not in part]
            if bad_parts:
                findings.append(('RRULE delimiter', f'Line {number}: rule part(s) must use =, not {", ".join(bad_parts)}.'))

    for number, line in enumerate(lines, start=1):
        if line.startswith('DTSTAMP:') and not line.endswith('Z'):
            findings.append(('DTSTAMP form', f'Line {number}: DTSTAMP is missing its UTC Z suffix.'))

    for number, line in enumerate(lines, start=1):
        if line.startswith('DTSTART;TZID='):
            findings.append(('Floating-time mismatch', f'Line {number}: DTSTART still has TZID={line.split("=", 1)[1].split(":", 1)[0]}.'))

    calendar = Calendar.from_ical(raw)
    events = [component for component in calendar.walk() if component.name == 'VEVENT']
    uids = [str(event['UID']) for event in events]
    duplicates = [uid for uid, count in Counter(uids).items() if count > 1]
    for uid in duplicates:
        findings.append(('UID uniqueness', f'Duplicate UID: {uid}.'))

    for event in events:
        uid = str(event['UID']).split('-vault_time@', 1)[0].lower()
        start = event['DTSTART'].dt
        if type(start) is date:
            if uid in WEEKDAY_UIDS and start.weekday() != WEEKDAY_UIDS[uid]:
                findings.append(('Weekday label mismatch', f'{uid}: DTSTART {start.isoformat()} is not a {uid.title()}.'))
            if uid in MONTH_UIDS and start.month != MONTH_UIDS[uid]:
                findings.append(('Month label mismatch', f'{uid}: DTSTART {start.isoformat()} is not in {uid.title()}.'))

    azer = next((event for event in events if str(event['UID']) == 'azer-vault_time@cron_clock'), None)
    if azer is not None and str(azer.get('CATEGORIES', '')).lower() != 'minutes':
        findings.append(('Category mismatch', f'Azer is CATEGORIES:{azer.get("CATEGORIES")}; the surrounding named 204-minute entries use CATEGORIES:Minutes.'))

    print(f'PARSE: success ({len(events)} VEVENTs, {len(set(uids))} unique UIDs).')
    print(f'FINDINGS: {len(findings)}')
    for category, detail in findings:
        print(f'[{category}] {detail}')


if __name__ == '__main__':
    main()
