from pathlib import Path
import re
from collections import Counter

source = Path('/home/ubuntu/upload/pasted_content.txt')
raw = source.read_bytes()
text = raw.decode('utf-8')
lines = text.splitlines()

# CSS3 keyword subset covering every observed and recommended token. All are
# explicitly listed in CSS Color Module Level 3, Section 4.3.
css3 = {
    'black', 'white', 'silver', 'gold', 'red', 'orange', 'yellow', 'green',
    'blue', 'indigo', 'violet', 'orangered', 'yellowgreen', 'turquoise',
    'deepskyblue', 'lightseagreen', 'mediumaquamarine', 'mediumblue',
    'mediumorchid', 'mediumvioletred', 'lightskyblue', 'coral', 'seagreen',
    'goldenrod', 'darkgoldenrod', 'firebrick', 'saddlebrown', 'olive',
    'teal', 'navy', 'purple', 'maroon', 'aqua', 'fuchsia', 'lime', 'gray',
    'darkslategray', 'slategray', 'mediumslateblue', 'darkcyan', 'darkorange',
}

print('=== STRUCTURE ===')
print(f'lines={len(lines)} has_crlf={b"\\r\\n" in raw} has_lf_only={b"\\n" in raw.replace(b"\\r\\n", b"")}')
print(f'blank_lines={sum(1 for line in lines if not line.strip())}')
print(f'VEVENT_begin={sum(line == "BEGIN:VEVENT" for line in lines)} VEVENT_end={sum(line == "END:VEVENT" for line in lines)}')

print('\n=== CONTENT-LINE FORM ===')
for number, line in enumerate(lines, 1):
    if not line:
        continue
    if line.startswith((' ', '\t')):
        continue
    if ':' not in line:
        print(f'INVALID_CONTENT_LINE line={number}: {line!r}')

print('\n=== CSS3 COLOR VALUES ===')
colors = []
for number, line in enumerate(lines, 1):
    if line.startswith('COLOR:'):
        value = line.split(':', 1)[1].lower()
        colors.append(value)
        if not value:
            print(f'EMPTY_COLOR line={number}')
        elif value not in css3:
            print(f'NON_CSS3_COLOR line={number}: {value!r}')
print('color_counts=' + repr(Counter(colors)))
valid = [value for value in colors if value and value in css3]
print('valid_css3_values=' + ', '.join(sorted(set(valid))))

print('\n=== DATE, DURATION, AND RECURRENCE ===')
for number, line in enumerate(lines, 1):
    if line.startswith('DTSTART:'):
        value = line.split(':', 1)[1]
        if re.fullmatch(r'\d{8}', value):
            print(f'DATE_WITHOUT_VALUE_DATE line={number}: {line}')
    if line.startswith('DURATION:'):
        value = line.split(':', 1)[1]
        # RFC 5545 duration allows W, D, H, M, S but M only after T;
        # calendar-year and calendar-month units are not permitted.
        legal = re.fullmatch(r'[+-]?P(?:(?:\d+W)|(?:(?:\d+D)?(?:T(?:(?:\d+H)?(?:\d+M)?(?:\d+S)?)?)?))', value)
        if not legal:
            print(f'INVALID_RFC5545_DURATION line={number}: {value!r}')
    if line.startswith('RRULE:'):
        value = line.split(':', 1)[1]
        for part in value.split(';'):
            if '=' not in part:
                print(f'INVALID_RRULE_PART line={number}: {part!r}')

print('\n=== VCALENDAR AND RELATIONSHIP PROPERTIES ===')
in_event = False
for number, line in enumerate(lines, 1):
    if line == 'BEGIN:VEVENT':
        in_event = True
    elif line == 'END:VEVENT':
        in_event = False
    elif not in_event and line.startswith('DTSTAMP:'):
        print(f'VCALENDAR_DTSTAMP_NOT_STANDARD line={number}: use LAST-MODIFIED instead')
    elif line.startswith('REFRESH-INTERVAL'):
        if line != 'REFRESH-INTERVAL;VALUE=DURATION:P1W':
            print(f'REFRESH_INTERVAL_NEEDS_RFC7986_FORM line={number}: {line!r}')
    elif line.startswith('RELATED-TO:') and ',' in line:
        print(f'COMMA_SEPARATED_RELATED_TO line={number}: use separate RELATED-TO properties or escape the comma if literal')

print('\n=== SEMANTIC PLACEHOLDERS (SYNTAX-PERMITTED, NO TARGET) ===')
for number, line in enumerate(lines, 1):
    if line == 'RELATED-TO:':
        print(f'EMPTY_RELATED_TO line={number}')
