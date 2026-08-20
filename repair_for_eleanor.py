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
    if line == 'CATEGORIES:hour' and repaired and repaired[-1] == 'PRIORITY:':
        # This branch is unreachable after empty priorities are removed.
        line = 'CATEGORIES:Minutes'
    repaired.append(line)

# Align Azer with the six other named 204-minute entries without altering its timing.
for index, line in enumerate(repaired):
    if line == 'UID:azer-vault_time@cron_clock':
        for following in range(index + 1, min(index + 12, len(repaired))):
            if repaired[following] == 'CATEGORIES:hour':
                repaired[following] = 'CATEGORIES:Minutes'
                break

target.write_bytes(('\r\n'.join(repaired) + '\r\n').encode('utf-8'))
print(f'Wrote {target} with {len(repaired)} content lines.')
