from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

AUTHORITATIVE = Path('/home/ubuntu/upload/pasted_content.txt')
DELIVERED = Path('/home/ubuntu/ics/eleanor_shellstrop_cron_clock.ics')
DATE_TIME_UTC = re.compile(r'^\d{8}T\d{6}Z$')


def split_property(line: str) -> tuple[str, str]:
    left, value = line.split(':', 1)
    return left.split(';', 1)[0].upper(), value


def parse_calendar(path: Path) -> tuple[list[str], list[dict[str, object]], list[int]]:
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    lines = text.splitlines()
    calendar_lines: list[str] = []
    events: list[dict[str, object]] = []
    event_lines: list[tuple[int, str]] | None = None
    blank_lines: list[int] = []
    for number, line in enumerate(lines, start=1):
        if line == '':
            blank_lines.append(number)
            continue
        if line == 'BEGIN:VEVENT':
            event_lines = [(number, line)]
            continue
        if event_lines is not None:
            event_lines.append((number, line))
            if line == 'END:VEVENT':
                properties: list[tuple[str, str, int, str]] = []
                for line_number, event_line in event_lines[1:-1]:
                    name, value = split_property(event_line)
                    properties.append((name, value, line_number, event_line))
                uid = next((value for name, value, _, _ in properties if name == 'UID'), '<missing-uid>')
                events.append({'uid': uid, 'properties': properties, 'start': event_lines[0][0], 'end': event_lines[-1][0]})
                event_lines = None
            continue
        calendar_lines.append(line)
    return calendar_lines, events, blank_lines


def rendered_properties(event: dict[str, object]) -> tuple[str, ...]:
    return tuple(line for _, _, _, line in event['properties'])


def main() -> None:
    auth_cal, auth_events, auth_blank = parse_calendar(AUTHORITATIVE)
    del_cal, del_events, del_blank = parse_calendar(DELIVERED)

    auth_count = Counter(event['uid'] for event in auth_events)
    del_count = Counter(event['uid'] for event in del_events)
    source_only = sorted((uid, count) for uid, count in (auth_count - del_count).items())
    delivered_only = sorted((uid, count) for uid, count in (del_count - auth_count).items())

    auth_by_occurrence: dict[tuple[str, int], dict[str, object]] = {}
    del_by_occurrence: dict[tuple[str, int], dict[str, object]] = {}
    for events, target in ((auth_events, auth_by_occurrence), (del_events, del_by_occurrence)):
        seen: Counter[str] = Counter()
        for event in events:
            seen[event['uid']] += 1
            target[(event['uid'], seen[event['uid']])] = event

    changed_matches: list[str] = []
    for key in sorted(auth_by_occurrence.keys() & del_by_occurrence.keys()):
        if rendered_properties(auth_by_occurrence[key]) != rendered_properties(del_by_occurrence[key]):
            changed_matches.append(f'{key[0]} occurrence {key[1]}')

    strict_findings: list[str] = []
    auth_raw = AUTHORITATIVE.read_bytes()
    if b'\r\n' not in auth_raw or b'\n' in auth_raw.replace(b'\r\n', b''):
        strict_findings.append('Source as pasted is LF-delimited rather than CRLF-delimited.')
    for number in auth_blank:
        strict_findings.append(f'Blank content line at source line {number}.')
    for number, line in enumerate(AUTHORITATIVE.read_text(encoding='utf-8').splitlines(), start=1):
        if line.startswith('DTSTAMP:') and not DATE_TIME_UTC.fullmatch(line[8:]):
            strict_findings.append(f'Line {number}: invalid DTSTAMP DATE-TIME value {line[8:]!r}.')
        if line.startswith('RRULE:') and any('=' not in part for part in line[6:].split(';')):
            strict_findings.append(f'Line {number}: RRULE contains a part without =.')
    for uid, count in sorted(auth_count.items()):
        if count > 1:
            strict_findings.append(f'UID {uid!r} is duplicated {count} times.')

    print(f'AUTHORITATIVE EVENTS: {len(auth_events)}')
    print(f'DELIVERED EVENTS: {len(del_events)}')
    print(f'AUTHORITATIVE BLANK LINES: {auth_blank or "none"}')
    print(f'DELIVERED BLANK LINES: {del_blank or "none"}')
    print('\nSOURCE-ONLY EVENT OCCURRENCES:')
    for uid, count in source_only:
        print(f'  {uid} x{count}')
    print('\nDELIVERED-ONLY EVENT OCCURRENCES:')
    for uid, count in delivered_only:
        print(f'  {uid} x{count}')
    print(f'\nMATCHED EVENTS WITH PROPERTY DIFFERENCES: {len(changed_matches)}')
    for entry in changed_matches:
        print(f'  {entry}')
    print(f'\nCALENDAR-LEVEL LINES AUTHORITATIVE: {len(auth_cal)}; DELIVERED: {len(del_cal)}')
    print('\nSTRICT SOURCE FINDINGS:')
    for finding in strict_findings:
        print(f'  {finding}')
    print(f'TOTAL STRICT SOURCE FINDINGS: {len(strict_findings)}')


if __name__ == '__main__':
    main()
