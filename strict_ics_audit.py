from __future__ import annotations

import re
import sys
from pathlib import Path

# Paths accept command-line overrides and default to this repository's copies.
_REPO = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock.ics'
CONTENT_LINE = re.compile(r'^(?P<name>[A-Za-z0-9-]+)(?P<params>(?:;[^:;=]+=(?:[^:;]*))*):(?P<value>.*)$')


def main() -> None:
    raw = SOURCE.read_bytes()
    findings: list[str] = []
    if b'\r\n' not in raw:
        findings.append('File uses no CRLF delimiters.')
    if b'\n' in raw.replace(b'\r\n', b''):
        findings.append('File contains bare LF delimiters.')

    text = raw.decode('utf-8')
    lines = text.splitlines()
    stack: list[str] = []
    events = 0
    for number, line in enumerate(lines, start=1):
        if line == '':
            findings.append(f'Line {number}: blank line is not an iCalendar content line.')
            continue
        if len(line.encode('utf-8')) > 75:
            findings.append(f'Line {number}: content line exceeds 75 octets without folding.')
        match = CONTENT_LINE.fullmatch(line)
        if not match:
            findings.append(f'Line {number}: malformed content line: {line!r}')
            continue
        name = match.group('name').upper()
        value = match.group('value')
        if name == 'BEGIN':
            stack.append(value.upper())
            if value.upper() == 'VEVENT':
                events += 1
        elif name == 'END':
            if not stack:
                findings.append(f'Line {number}: END:{value} has no matching BEGIN.')
            elif stack.pop() != value.upper():
                findings.append(f'Line {number}: END:{value} does not match open component.')
        elif name == 'PRIORITY' and value == '':
            findings.append(f'Line {number}: PRIORITY requires an integer value or omission.')
        elif name == 'RRULE':
            for part in value.split(';'):
                if '=' not in part:
                    findings.append(f'Line {number}: RRULE part {part!r} requires an equals sign.')
        elif name == 'DTSTAMP' and not value.endswith('Z'):
            findings.append(f'Line {number}: DTSTAMP must be a UTC date-time ending in Z.')

    if stack:
        findings.append(f'Unclosed component(s): {", ".join(stack)}.')
    print(f'VEVENT count: {events}')
    print(f'STRICT FINDINGS: {len(findings)}')
    for finding in findings:
        print(finding)


if __name__ == '__main__':
    main()
