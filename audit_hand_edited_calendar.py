from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

from icalendar import Calendar

SOURCE = Path('/home/ubuntu/upload/pasted_content.txt')


def main() -> None:
    raw = SOURCE.read_bytes()
    calendar = Calendar.from_ical(raw)
    events = [component for component in calendar.walk() if component.name == 'VEVENT']
    print(f'Parsed calendar with {len(events)} VEVENTs.')

    issues: list[str] = []
    issues += [
        f'Line {line_no}: malformed empty PRIORITY property.'
        for line_no, line in enumerate(raw.decode('utf-8').splitlines(), 1)
        if line == 'PRIORITY:'
    ]
    issues += [
        f'Line {line_no}: RRULE uses INTERVAL: rather than INTERVAL=.'
        for line_no, line in enumerate(raw.decode('utf-8').splitlines(), 1)
        if 'INTERVAL:' in line
    ]

    uid_counts = Counter(str(event.get('UID')) for event in events)
    issues += [f'Duplicate UID: {uid}' for uid, count in uid_counts.items() if count > 1]

    for event in events:
        uid = str(event.get('UID'))
        dtstamp = event['DTSTAMP'].to_ical().decode('utf-8')
        if not dtstamp.endswith('Z'):
            issues.append(f'{uid}: DTSTAMP is not UTC (missing trailing Z).')

        start = event['DTSTART'].dt
        tzid = event['DTSTART'].params.get('TZID')
        if tzid:
            issues.append(f'{uid}: DTSTART uses TZID={tzid}, so it is not floating.')

        rrule_value = str(event.get('RRULE').to_ical(), 'utf-8') if event.get('RRULE') else ''
        if isinstance(start, datetime) is False and any(freq in rrule_value for freq in ('FREQ=HOURLY', 'FREQ=MINUTELY', 'FREQ=SECONDLY')):
            issues.append(f'{uid}: DATE DTSTART cannot reliably express {rrule_value}; use a floating DATE-TIME DTSTART.')

    print('\n'.join(f'ISSUE: {issue}' for issue in issues))
    print(f'Total issues reported: {len(issues)}')


if __name__ == '__main__':
    main()
