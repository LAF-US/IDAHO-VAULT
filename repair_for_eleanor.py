import sys
from pathlib import Path

from cli_path_guard import repo_path

# Paths accept command-line overrides, containment-checked to repository files.
_REPO = Path(__file__).resolve().parent
source = repo_path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock.ics'
target = repo_path(sys.argv[2], must_exist=False) if len(sys.argv) > 2 else _REPO / 'eleanor_shellstrop_cron_clock.ics'

repaired: list[str] = []
for line in source.read_text(encoding='utf-8').splitlines():
    if line == '':
        continue
    if line == 'PRIORITY:':
        continue
    if line.startswith('RRULE:'):
        line = line.replace('INTERVAL:', 'INTERVAL=')
    if line.startswith('DTSTAMP:'):
        stamp = line[len('DTSTAMP:'):]
        if not stamp.endswith('Z'):
            stamp = f'{stamp}Z'
        # A date-only stamp such as 20270101Z gains an explicit UTC midnight.
        if 'T' not in stamp:
            stamp = f'{stamp[:-1]}T000000Z'
        line = f'DTSTAMP:{stamp}'
    if line.startswith('DTSTART;TZID=America/Boise:'):
        line = line.replace('DTSTART;TZID=America/Boise:', 'DTSTART:', 1)
    repaired.append(line)

# Align Azer with the six other named 204-minute entries without altering its
# timing: locate its VEVENT block explicitly and rewrite the CATEGORIES line
# found inside it, failing loudly if the block or the property is absent.
try:
    azer_uid_index = repaired.index('UID:azer-vault_time@cron_clock')
    azer_end = repaired.index('END:VEVENT', azer_uid_index)
except ValueError as error:
    raise AssertionError('Azer VEVENT block not found in source calendar') from error
for following in range(azer_uid_index + 1, azer_end):
    if repaired[following].startswith('CATEGORIES:'):
        repaired[following] = 'CATEGORIES:Minutes'
        break
else:
    raise AssertionError('Azer CATEGORIES property not found in its VEVENT block')

target.write_bytes(('\r\n'.join(repaired) + '\r\n').encode('utf-8'))
print(f'Wrote {target} with {len(repaired)} content lines.')
