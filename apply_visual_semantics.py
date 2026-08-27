import sys
from pathlib import Path

from cli_path_guard import repo_path

# Paths accept command-line overrides, containment-checked to repository files.
_REPO = Path(__file__).resolve().parent
source = repo_path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock.ics'
target = repo_path(sys.argv[2], must_exist=False) if len(sys.argv) > 2 else _REPO / 'cron_clock_visual_semantics.ics'
ledger = repo_path(sys.argv[3], must_exist=False) if len(sys.argv) > 3 else _REPO / 'cron_clock_visual_semantics_changes.md'
if ledger in (source, target):
    # The Markdown ledger is written last and would clobber calendar bytes.
    raise SystemExit('The ledger path must be distinct from the source and target paths.')

# Ordered palette for every authored seven-item group.
roygbiv = {
    'monday-vault_time@cron_clock': 'red',
    'tuesday-vault_time@cron_clock': 'orange',
    'wednesday-vault_time@cron_clock': 'yellow',
    'thursday-vault_time@cron_clock': 'green',
    'friday-vault_time@cron_clock': 'blue',
    'saturday-vault_time@cron_clock': 'indigo',
    'sunday-vault_time@cron_clock': 'violet',
    'yan-vault_time@cron_clock': 'red',
    'tan-vault_time@cron_clock': 'orange',
    'tethera-vault_time@cron_clock': 'yellow',
    'methera-vault_time@cron_clock': 'green',
    'pits-vault_time@cron_clock': 'blue',
    'sethera-vault_time@cron_clock': 'indigo',
    'azer-vault_time@cron_clock': 'violet',
}

colors = {
    'millenium-vault_time@cron_clock': 'white',
    'century-vault_time@cron_clock': 'white',
    'decade-vault_time@cron_clock': 'white',
    'year-vault_time@cron_clock': 'white',
    'tick-vault_time@cron_clock': 'black',
    **roygbiv,
}

lines = source.read_text(encoding='utf-8').splitlines()
result: list[str] = []
changes: list[tuple[str, str, str]] = []
i = 0
while i < len(lines):
    if lines[i] != 'BEGIN:VEVENT':
        result.append(lines[i])
        i += 1
        continue
    j = i
    event: list[str] = []
    while j < len(lines):
        event.append(lines[j])
        if lines[j] == 'END:VEVENT':
            break
        j += 1
    else:
        raise SystemExit(f'Malformed calendar: VEVENT at line {i + 1} has no END:VEVENT.')
    uid = next((line[4:] for line in event if line.startswith('UID:')), '')
    wanted = colors.get(uid)
    original_colors = [line for line in event if line.startswith('COLOR:')]
    event = [line for line in event if not line.startswith('COLOR:')]
    if wanted is not None:
        insertion = next((k for k, line in enumerate(event) if line == 'END:VEVENT'), len(event))
        event.insert(insertion, f'COLOR:{wanted}')
        before = original_colors[0] if original_colors else '<absent>'
        after = f'COLOR:{wanted}'
        if before != after:
            changes.append((uid, before, after))
    elif original_colors:
        changes.append((uid, original_colors[0], '<removed: undecided>'))
    result.extend(event)
    i = j + 1

# Preserve intentional absence: no demon/grace or non-period-minute VEVENTs are created.
target.write_bytes(('\r\n'.join(result) + '\r\n').encode('utf-8'))

lines_out = [
    '# Visual-Semantics Change Ledger',
    '',
    'This transformation applies only the confirmed color rules and preserves silent interstices. It creates no VEVENT for demon/grace days or non-period minutes.',
    '',
    '| UID | Prior color field | Result |',
    '|---|---|---|',
]
for uid, before, after in changes:
    lines_out.append(f'| `{uid}` | `{before}` | `{after}` |')
lines_out.extend([
    '',
    '## Preserved Silence',
    '',
    'The five internal senary demon/grace days, leap-year additional grace day, and non-period minutes between named 204-minute rhythms remain absent from the output. No placeholder or filler event was created.',
    '',
    '## Unchanged Outside Scope',
    '',
    'All DTSTART, DURATION, RRULE, UID, RELATED-TO, category, priority, description, and calendar-level values were preserved exactly from the supplied source. The output uses CRLF content-line delimiters.',
])
ledger.write_text('\n'.join(lines_out) + '\n', encoding='utf-8')

print(f'events with explicit color treatment: {len(changes)}')
print(f'output: {target}')
print(f'ledger: {ledger}')
