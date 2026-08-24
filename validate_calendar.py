from __future__ import annotations

from collections import Counter
from datetime import date, datetime
import sys
from pathlib import Path

from dateutil.rrule import rrulestr
from icalendar import Calendar

# Paths accept command-line overrides and default to this repository's copies.
_REPO = Path(__file__).resolve().parent
CALENDAR_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock_gregorian_floating.ics'


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    raw = CALENDAR_PATH.read_bytes()
    if b'\r\n' not in raw or raw.replace(b'\r\n', b'').find(b'\n') != -1:
        fail('Calendar content lines must use CRLF exclusively.')
    if not raw.endswith(b'\r\n'):
        fail('Calendar must end with CRLF.')

    for number, line in enumerate(raw.split(b'\r\n'), start=1):
        if len(line) > 75:
            fail(f'Line {number} exceeds the 75-octet content-line limit.')
        if line == b'X-':
            fail('Malformed extension property X- found.')

    calendar = Calendar.from_ical(raw)
    if calendar.get('VERSION') != '2.0':
        fail('VERSION must be 2.0.')
    if calendar.get('CALSCALE') != 'GREGORIAN':
        fail('CALSCALE must be GREGORIAN.')

    events = [component for component in calendar.walk() if component.name == 'VEVENT']
    if len(events) != 35:
        fail(f'Expected 35 VEVENTs, found {len(events)}.')

    uids = [str(event.get('UID')) for event in events]
    duplicates = [uid for uid, count in Counter(uids).items() if count > 1]
    if duplicates:
        fail(f'Duplicate UID(s): {duplicates}')

    expected_date_only = {
        'year-vault_time@cron_clock', 'q1-vault_time@cron_clock',
        'q2-vault_time@cron_clock', 'q3-vault_time@cron_clock',
        'q4-vault_time@cron_clock', 'january-vault_time@cron_clock',
        'february-vault_time@cron_clock', 'march-vault_time@cron_clock',
        'april-vault_time@cron_clock', 'may-vault_time@cron_clock',
        'june-vault_time@cron_clock', 'july-vault_time@cron_clock',
        'august-vault_time@cron_clock', 'september-vault_time@cron_clock',
        'october-vault_time@cron_clock', 'november-vault_time@cron_clock',
        'december-vault_time@cron_clock', 'week-vault_time@cron_clock',
        'monday-vault_time@cron_clock', 'tuesday-vault_time@cron_clock',
        'wednesday-vault_time@cron_clock', 'thursday-vault_time@cron_clock',
        'friday-vault_time@cron_clock', 'saturday-vault_time@cron_clock',
        'sunday-vault_time@cron_clock',
    }

    for event in events:
        uid = str(event.get('UID'))
        for required in ('UID', 'DTSTAMP', 'DTSTART', 'RRULE', 'SUMMARY', 'TRANSP'):
            if event.get(required) is None:
                fail(f'{uid}: missing {required}.')

        start_property = event['DTSTART']
        start = start_property.dt
        if 'TZID' in start_property.params:
            fail(f'{uid}: contains a TZID; all time entries must float.')
        if isinstance(start, datetime) and start.tzinfo is not None:
            fail(f'{uid}: DTSTART is not floating local time.')
        if uid in expected_date_only:
            if type(start) is not date:
                fail(f'{uid}: expected a DATE DTSTART.')
            duration = event.get('DURATION')
            local = uid.split('-', 1)[0]
            if local in {'week'} | {d.lower() for d in
                         ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')}:
                if duration is None:
                    fail(f'{uid}: Day/Week event must carry its P1D/P1W duration.')
            elif duration is not None:
                # Months, quarters, and the Year are starts-only markers.
                fail(f'{uid}: wheel event must not carry a DURATION.')
        else:
            if not isinstance(start, datetime) or start.tzinfo is not None:
                fail(f'{uid}: expected a floating DATE-TIME DTSTART.')
            if event.get('DURATION') is None:
                fail(f'{uid}: timed span must carry a DURATION.')

        rule = str(event['RRULE'].to_ical(), 'utf-8')
        first_rule_instance = next(iter(rrulestr(rule, dtstart=start)))
        comparable_start = datetime.combine(start, datetime.min.time()) if type(start) is date else start
        if first_rule_instance != comparable_start:
            fail(f'{uid}: DTSTART is not synchronized with its RRULE.')

    print('PASS: parsed RFC-style calendar syntax and all 35 VEVENTs.')
    print('PASS: CALSCALE:GREGORIAN and unique UIDs verified.')
    print('PASS: all DATE-TIME DTSTARTs are floating; no TZID or UTC conversion remains.')
    print('PASS: RRULE DTSTART alignment, all-day durations, and 75-octet line limit verified.')


if __name__ == '__main__':
    main()
