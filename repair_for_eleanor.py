from pathlib import Path

source = Path('/home/ubuntu/upload/pasted_content.txt')
target = Path('/home/ubuntu/ics/eleanor_shellstrop_cron_clock.ics')

repaired: list[str] = []
for line in source.read_text(encoding='utf-8').splitlines():
    if line == '':
        continue
    if line == 'PRIORITY:':
        continue
    if line.startswith('RRULE:'):
        line = line.replace('INTERVAL:', 'INTERVAL=')
    if line.startswith('DTSTAMP:') and not line.endswith('Z'):
        line = f'{line}Z'
    if line.startswith('DTSTART;TZID=America/Boise:'):
        line = line.replace('DTSTART;TZID=America/Boise:', 'DTSTART:', 1)
    repaired.append(line)

# Align Azer with the six other named 204-minute entries without altering its
# timing: locate its VEVENT block explicitly and rewrite the CATEGORIES line
# found inside it, failing loudly if the block or the property is absent.
azer_uid_index = repaired.index('UID:azer-vault_time@cron_clock')
azer_end = repaired.index('END:VEVENT', azer_uid_index)
for following in range(azer_uid_index + 1, azer_end):
    if repaired[following].startswith('CATEGORIES:'):
        repaired[following] = 'CATEGORIES:Minutes'
        break
else:
    raise AssertionError('Azer CATEGORIES property not found in its VEVENT block')

target.write_bytes(('\r\n'.join(repaired) + '\r\n').encode('utf-8'))
print(f'Wrote {target} with {len(repaired)} content lines.')
