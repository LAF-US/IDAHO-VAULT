import sys
from pathlib import Path
from collections import Counter

# Paths accept command-line overrides and default to this repository's copies.
_REPO = Path(__file__).resolve().parent
path = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock_visual_semantics.ics'
raw = path.read_bytes()
assert b'\n' not in raw.replace(b'\r\n', b''), 'Non-CRLF newline found'
assert b'\r\n\r\n' not in raw, 'Blank content line found'
text = raw.decode('utf-8')
assert text.startswith('BEGIN:VCALENDAR\r\n') and text.endswith('END:VCALENDAR\r\n')

blocks = text.split('BEGIN:VEVENT\r\n')[1:]
assert len(blocks) == 52, f'Expected 52 VEVENT blocks, found {len(blocks)}'
events = {}
seen_uids = []
for block in blocks:
    lines = block.split('END:VEVENT\r\n', 1)[0].split('\r\n')
    fields = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            fields.setdefault(key, []).append(value)
    uid = fields['UID'][0]
    seen_uids.append(uid)
    events[uid] = fields

duplicate_uids = {uid for uid in seen_uids if seen_uids.count(uid) > 1}
assert not duplicate_uids, f'Duplicate UIDs: {sorted(duplicate_uids)}'
assert len(events) == 52, f'Expected 52 events, found {len(events)}'
expected = {
    'millenium-vault_time@cron_clock': 'white',
    'century-vault_time@cron_clock': 'white',
    'decade-vault_time@cron_clock': 'white',
    'year-vault_time@cron_clock': 'white',
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
    'tick-vault_time@cron_clock': 'black',
}
for uid, color in expected.items():
    assert events[uid].get('COLOR') == [color], f'{uid}: expected {color}, found {events[uid].get("COLOR")}'
for uid, fields in events.items():
    if uid not in expected:
        assert 'COLOR' not in fields, f'{uid}: undecided color was retained: {fields["COLOR"]}'

summaries = {fields['SUMMARY'][0] for fields in events.values()}
for prohibited in ('DEMON', 'GRACE', 'REMAINDER', 'INTERSTICE'):
    assert prohibited not in summaries, f'Unexpected filler event: {prohibited}'

print('PASS: 52 events; CRLF; no blank content lines; color semantics correct; silent interstices preserved.')
print('explicit_colors=' + str(Counter(v['COLOR'][0] for v in events.values() if 'COLOR' in v)))
