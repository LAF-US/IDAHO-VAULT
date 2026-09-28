from __future__ import annotations

import re
from collections import Counter
import sys
from pathlib import Path

from icalendar import Calendar

from cli_path_guard import repo_path

# Paths accept command-line overrides, containment-checked to repository files.
_REPO = Path(__file__).resolve().parent
TARGET = repo_path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'eleanor_shellstrop_cron_clock.ics'
CONTENT_LINE = re.compile(r'^[A-Za-z0-9-]+(?:;[^:;=]+=(?:[^:;]*))*:.*$')


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    raw = TARGET.read_bytes()
    if b'\r\n' not in raw or b'\n' in raw.replace(b'\r\n', b''):
        fail('Content lines are not exclusively CRLF-delimited.')
    if not raw.endswith(b'\r\n'):
        fail('File does not end with CRLF.')

    lines = raw.decode('utf-8').split('\r\n')[:-1]
    stack: list[str] = []
    for number, line in enumerate(lines, start=1):
        if line == '':
            fail(f'Blank content line at line {number}.')
        if len(line.encode('utf-8')) > 75:
            fail(f'Unfolded content line exceeds 75 octets at line {number}.')
        if not CONTENT_LINE.fullmatch(line):
            fail(f'Malformed content line at line {number}: {line!r}')
        if line == 'PRIORITY:':
            fail(f'Empty PRIORITY at line {number}.')
        if line.startswith('RRULE:') and any('=' not in item for item in line[6:].split(';')):
            fail(f'Malformed RRULE separator at line {number}.')
        if line.startswith('DTSTAMP:') and not line.endswith('Z'):
            fail(f'Non-UTC DTSTAMP at line {number}.')
        if line.startswith('DTSTART;TZID='):
            fail(f'Non-floating DTSTART at line {number}.')
        if line.startswith('BEGIN:'):
            stack.append(line[6:])
        elif line.startswith('END:'):
            if not stack or stack.pop() != line[4:]:
                fail(f'Unbalanced component line {number}: {line}.')
    if stack:
        fail(f'Unclosed components: {stack}.')

    calendar = Calendar.from_ical(raw)
    events = [component for component in calendar.walk() if component.name == 'VEVENT']
    uids = [str(event['UID']) for event in events]
    if len(events) != 42:
        fail(f'Expected 42 VEVENTs; found {len(events)}.')
    duplicate_uids = [uid for uid, count in Counter(uids).items() if count > 1]
    if duplicate_uids:
        fail(f'Duplicate UIDs: {duplicate_uids}.')
    if any('TZID' in event['DTSTART'].params for event in events):
        fail('TZID remained on at least one DTSTART.')
    azer = next(event for event in events if str(event['UID']) == 'azer-vault_time@cron_clock')
    if azer['CATEGORIES'].to_ical().decode('utf-8') != 'Minutes':
        fail('Azer category was not aligned with the named minute-scale entries.')

    print('PASS: strict content-line, component-balance, and CRLF checks passed.')
    print('PASS: parser accepted 42 VEVENTs with 42 unique UIDs.')
    print('PASS: empty priorities, malformed intervals, non-UTC timestamps, and DTSTART TZIDs are absent.')
    print('PASS: Azer category is aligned with the named 204-minute sequence.')


if __name__ == '__main__':
    main()
